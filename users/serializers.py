from rest_framework import serializers
from users.models import User
from courses.models import Course
# from courses.serializers import CourseSerializer

class UserSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(format='hex_verbose', read_only=True)
  first_name = serializers.CharField()
  last_name = serializers.CharField()
  email = serializers.CharField()
  is_admin = serializers.BooleanField()

  # course = CourseSerializer(read_only=True)

  # def create(self, validated_data):
  #   return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()    