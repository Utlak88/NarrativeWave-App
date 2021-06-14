from rest_framework import serializers


class AssetColumnSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    value = serializers.FloatField(allow_null=True, default='')
