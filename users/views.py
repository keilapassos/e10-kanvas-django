from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer

# Create your views here.

class UserView(APIView):

  def post(self, request):

    try:
      first_name = request.data['first_name']
      last_name = request.data['last_name']
      password = request.data['password']
      is_admin = request.data['is_admin']
      email = request.data['email']

    except KeyError:
      return status.HTTP_400_BAD_REQUEST

    except IntegrityError:
      return IntegrityError('user email is not unique')

    if User.objects.filter(email=email).exists() == True:
      response = {"message": "User already exists"}
      return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    user = User.objects.create_user(
      first_name = first_name,
      last_name = last_name,
      is_admin = is_admin,
      password = password,
      email = email,
    )

    serialized = UserSerializer(user)

    return Response(serialized.data, status=status.HTTP_201_CREATED)

  def get(self, request):
    users = User.objects.all()

    serialized = UserSerializer(users, many=True)

    return Response(serialized.data, status=status.HTTP_200_OK)




