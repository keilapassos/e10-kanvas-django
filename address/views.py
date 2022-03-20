from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import authenticate, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from users.models import User
# from .permissions import IsAdmin

from address.models import Address
from address.serializers import AddressSerializer

# Create your views here.

class AddressView(APIView): 

  authentication_classes = [TokenAuthentication]
    
  def put(self, request):

    user = User.objects.get(uuid=request.user.uuid)

    serialized = AddressSerializer(data=request.data)

    if not serialized.is_valid():
      return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
      address = Address.objects.get(zip_code=request.data['zip_code'])

    except Address.DoesNotExist:
      address = Address.objects.create(
        zip_code = request.data['zip_code'],
        street = request.data['street'],
        house_number = request.data['house_number'],
        city = request.data['city'],
        state = request.data['state'],
        country = request.data['country'],
      )
        
    user = request.user
        
    user.user_address = address
    user.save()

    serialized = AddressSerializer(address)

    return Response(serialized.data)