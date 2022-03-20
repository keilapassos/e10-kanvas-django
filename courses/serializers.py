from rest_framework import serializers

from users.serializers import UserSerializer

class CourseSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(format='hex_verbose', read_only=True)
  name = serializers.CharField()
  demo_time = serializers.TimeField()
  created_at = serializers.DateTimeField(read_only=True)
  link_repo = serializers.CharField()
    
  instructor = UserSerializer(read_only=True)
  students = UserSerializer(many=True, read_only=True)