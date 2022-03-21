from datetime import datetime
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer
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

    except User.DoesNotExist:
      return Response({"message": "Invalid instructor_id"}, status=status.HTTP_404_NOT_FOUND)
    
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    except KeyError:
      # no canvas aparece a key 'message', mas o teste falha se colocar, deixei como no teste
      # return Response({"message": "instructor_id is a required field."}, status=status.HTTP_400_BAD_REQUEST)
      return Response("instructor_id is a required field.", status=status.HTTP_400_BAD_REQUEST)

    # except IntegrityError:
    #   return Response({'message': 'Instructor already registered in a course'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if instructor.is_admin == False:
      return Response({'message': 'Instructor id does not belong to an admin'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    print("==============")
    print(course.instructor)

    course.save()

    print("===22222======")
    print(course.instructor)

    # if course.instructor in course:
    #   return Response({'message': 'Instructor already registered'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    serializer = CourseSerializer(course)

    return Response(serializer.data)