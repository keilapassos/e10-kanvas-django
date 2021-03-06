from django.urls import path
from courses.views import CourseView, CourseByIdView, InstructorView, StudentView

urlpatterns = [
  path('courses/', CourseView.as_view()),
  path('courses/<str:course_id>/', CourseByIdView.as_view()),
  path('courses/<str:course_id>/registrations/instructor/', InstructorView.as_view()),
  path('courses/<str:course_id>/registrations/students/', StudentView.as_view())
]
