from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer

# Create your views here.
class AllCoursesViews(APIView):
  def get(self, request):

    courses = Course.objects.all()

    serialized = CourseSerializer(courses, many=True)

    return Response(serialized.data)

class CourseByIdView(APIView):
  def get(self, request, id=''):

    course = Course.objects.get(id=id)

    serialized = CourseSerializer(course)

    return Response(serialized.data)
