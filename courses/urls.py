from django.urls import path
from courses.views import AllCoursesViews, CourseByIdView

urlpatterns = [
  path('courses_list/', AllCoursesViews.as_view()),
  path('courses/<str:course_id>', CourseByIdView.as_view()),
]
