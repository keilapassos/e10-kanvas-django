from django.urls import path
from users.views import UserView, UserLoginView

urlpatterns = [
  path('accounts/', UserView.as_view()),
  path('login/', UserLoginView.as_view()),
]
