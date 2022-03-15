from rest_framework import serializers

class UserSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(format='hex_verbose')
  first_name = serializers.CharField()
  last_name = serializers.CharField()
  email = serializers.CharField()
  is_admin = serializers.BooleanField()