from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer
from rest_framework.authentication import authenticate, TokenAuthentication
from courses.permissions import CoursePermission, CoursesByIdPermission


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

