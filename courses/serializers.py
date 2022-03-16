from rest_framework import serializers

from users.serializers import UserSerializer

class CourseSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(format='hex_verbose')
  name = serializers.CharField()
  demo_time = serializers.TimeField()
  created_at = serializers.DateTimeField()
  link_repo = serializers.CharField()

  # instructor = serializers.CharField()
  # student = UserSerializer(many=True, read_only=True)
  # student = serializers.ListField(default=[])