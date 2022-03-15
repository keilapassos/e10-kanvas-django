from rest_framework import serializers

class CourseSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(format='hex_verbose')
  name = serializers.CharField()
  demo_time = serializers.TimeField()
  created_at = serializers.DateTimeField()
  link_repo = serializers.CharField()