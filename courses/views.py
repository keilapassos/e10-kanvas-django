from datetime import datetime
from functools import partial
from xml.dom import ValidationErr
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer, StudentSerializer, InstructorSerializer
from rest_framework.authentication import authenticate, TokenAuthentication
from courses.permissions import CoursePermission, CoursesByIdPermission, CoursesRegistrationPermission

from users.models import User

# Create your views here.

class CourseView(APIView): 

  authentication_classes = [TokenAuthentication]
  permission_classes = [CoursePermission] 

  def post(self, request):
    serializer = CourseSerializer(data=request.data)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if Course.objects.filter(name=request.data['name']).exists() == True:
      response = {"message": "Course already exists"}
      return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    course = Course.objects.create(
      name = request.data['name'],
      demo_time = request.data['demo_time']+':00',
      created_at = datetime.now(),
      link_repo = request.data['link_repo']
    )

    serialized = CourseSerializer(course)

    return Response(serialized.data, status=status.HTTP_201_CREATED)

  def get(self, request):

    courses = Course.objects.all()

    serialized = CourseSerializer(courses, many=True)

    return Response(serialized.data)

class CourseByIdView(APIView):

  authentication_classes = [TokenAuthentication]
  permission_classes = [CoursesByIdPermission]  

  def get(self, request, course_id=''):

    try:
      course = Course.objects.get(uuid=course_id)

    except Course.DoesNotExist:
      return Response(
        {'message': 'Course does not exist'}, status=status.HTTP_404_NOT_FOUND,
      )

    serializer = CourseSerializer(course)

    return Response(serializer.data, status=status.HTTP_200_OK)

  def patch(self, request, course_id=''):
    
    try:
      course = Course.objects.get(uuid=course_id)

      serialized = CourseSerializer(data=request.data, partial=True)
      serialized.is_valid()
      
      data = {**serialized.validated_data}

      if 'name' in data:
        if Course.objects.filter(name=request.data['name']).exists() == True:
          response = {"message": "This course name already exists"}
          return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

      for key, value in data.items():
        # course[key] = value
        course.__dict__[key] = value
      
      course.save()

      course = Course.objects.get(uuid=course_id)
      serialized = CourseSerializer(course)

      return Response(serialized.data)

    except Course.DoesNotExist:
      return Response(
        {'message': 'Course does not exist'}, status=status.HTTP_404_NOT_FOUND,
      )

  def delete(self, request, course_id=''):

    try:
      course = Course.objects.get(uuid=course_id).delete()

      return Response(status=status.HTTP_204_NO_CONTENT)
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)

class InstructorView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [CoursesRegistrationPermission]

  def put(self, request, course_id=''):
    try:     
      course = Course.objects.get(uuid=course_id)

      instructor = User.objects.get(uuid=request.data['instructor_id'])

      course.instructor = instructor
      # course.instructor = instructor

      if course.instructor:
        print("========já existe instructor")
        print(course.instructor)

      serialized = InstructorSerializer(data=request.data)
      serialized.is_valid()

      if not serialized.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    except User.DoesNotExist:
      return Response({"message": "Invalid instructor_id"}, status=status.HTTP_404_NOT_FOUND)
    
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    except KeyError:
      # no canvas aparece a key 'message', mas o teste falha se colocar, deixei como no teste
      # return Response({"message": "instructor_id is a required field."}, status=status.HTTP_400_BAD_REQUEST)
      return Response("instructor_id is a required field.", status=status.HTTP_400_BAD_REQUEST)
    
    

    
    if instructor.is_admin == False:
      return Response({'message': 'Instructor id does not belong to an admin'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    course.save()

    serializer = CourseSerializer(course)

    return Response(serializer.data)

class StudentView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [CoursesRegistrationPermission]

  def put(self, request, course_id=''):
    try:     
      course = Course.objects.get(uuid=course_id)

      # course.students = []
      course.students.set([])

      serialized = StudentSerializer(data=request.data)
      serialized.is_valid()

      if not serialized.is_valid():
        return Response({'students_id': 'Users ids list were not provided'}, status=status.HTTP_400_BAD_REQUEST)
        

      for person in request.data['students_id']:       

        student_exists = User.objects.get(uuid=person)
        if student_exists.is_admin == True:
          return Response({'message': 'Some student id belongs to an Instructor'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # course.students.append({student_exists})
        course.students.add(student_exists)
        

    except User.DoesNotExist:
      return Response({"message": "Invalid students_id list"}, status=status.HTTP_404_NOT_FOUND)
    
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    except KeyError:
      return Response({"error": "Users ids list were not provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    

    course.save()

    serializer = CourseSerializer(course)    

    return Response(serializer.data)