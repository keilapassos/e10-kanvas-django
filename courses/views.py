from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer
from rest_framework.authentication import authenticate, TokenAuthentication
from users.permissions import IsAdmin

# Create your views here.

class CourseView(APIView): 

  # authentication_classes = [TokenAuthentication]
  # permission_classes = [IsAdmin]

  def post(self, request):

    try:
      name = request.data['name']
      demo_time = request.data['demo_time']
      link_repo = request.data['link_repo']

    except KeyError:
      return status.HTTP_400_BAD_REQUEST

    if Course.objects.filter(name=name).exists() == True:
      response = {"message": "Course already exists"}
      return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    course = Course.objects.create(
      name = name,
      demo_time = demo_time,
      created_at = datetime.now(),
      link_repo = link_repo,
      # instructor_id = "90df7edb-2f90-487a-9c18-091890bae59f", #instrutor1
      # instructor_id = "b6f9b354-f14c-4025-b3b1-e0040dbdde6d", #instrutor2
      # instructor_id = "9fdf7d44-b3f1-45c5-a198-9639f879c87d", #instrutor3
      # instructor = "006285de-3a0f-406f-8e2d-520dd9442306", #instrutor4
      # instructor = "006285de-3a0f-406f-8e2d-520dd9442306", #instrutor5
      # instructor = "", #instrutor6
      # students = []
    )

    serialized = CourseSerializer(course)

    return Response(serialized.data, status=status.HTTP_201_CREATED)

  def get(self, request):

    courses = Course.objects.all()

    serialized = CourseSerializer(courses, many=True)

    return Response(serialized.data)

class CourseByIdView(APIView):

  def get(self, request, course_id=''):

    course = Course.objects.get(uuid=course_id)
    # course = Course.objects.filter(uuid=course_id)

    # if Course.objects.filter(uuid=course_id).exists() == False:
    #   return Response({"message": "Uuid Not Founded"}, status.HTTP_404_NOT_FOUND)

    serialized = CourseSerializer(course)
    return Response(serialized.data)

