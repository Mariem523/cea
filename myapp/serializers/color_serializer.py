# serializers.py
from rest_framework import serializers
from ..models.color import Color

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ColorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'title', 'description', 'image', 'collection', 'format', 'theme']

    def validate(self, attrs):
        # Let model.clean() do most checks
        return attrs

    def create(self, validated_data):
        color = Color(**validated_data)
        color.full_clean()  # triggers `clean()` rules
        color.save()
        return color
