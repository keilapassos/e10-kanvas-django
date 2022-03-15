from rest_framework import serializers

class AddressSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(format='hex_verbose')
  street = serializers.CharField()
  house_number = serializers.CharField()
  city = serializers.CharField()
  state = serializers.CharField()
  zip_code = serializers.CharField()
  country = serializers.CharField()