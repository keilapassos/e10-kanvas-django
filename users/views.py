from django import http
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import authenticate, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from .permissions import IsAdmin

from users.models import User
from users.serializers import UserSerializer, LoginSerializer

# Create your views here.

class UserView(APIView): 

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdmin]

# inicio testes
  # def post(self, request):
  #   serializer = UserSerializer(data=request.data)
  #   print("==================")
  #   print(serializer)
  #   print("======fim serializer=========")

  #   if serializer.is_valid():
  #     serializer.save()
  #     return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

  #   return Response({'message':'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)

# fim testes

  def post(self, request):

    try:
      first_name = request.data['first_name']
      last_name = request.data['last_name']
      password = request.data['password']
      is_admin = request.data['is_admin']
      email = request.data['email']

    except KeyError:
      return status.HTTP_400_BAD_REQUEST

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


class UserLoginView(APIView):
  def post(self, request):
    try:
      email = request.data['email']
      password = request.data['password']
    except KeyError:
      return status.HTTP_400_BAD_REQUEST

    user = authenticate(email=email, password=password)

    if user:
      token = Token.objects.get_or_create(user=user)[0]
      return Response({'token': token.key})
    if not user:
      return Response(status=status.HTTP_401_UNAUTHORIZED)



