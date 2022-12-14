from rest_framework import serializers


class JSONTokenSchema(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)