# serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class AdminCreationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # create a superuser (is_staff & is_superuser True)
        return User.objects.create_superuser(
            username=validated_data['username'],
            password=validated_data['password'],
        )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        data['user'] = user
        return data

class AddUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # creates a normal user (is_staff/is_superuser False)
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        # adjust fields as needed
        fields = ('id', 'username','password')
        read_only_fields = fields

class ResetPasswordSerializer(serializers.Serializer):
    password         = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        pw  = attrs.get('password')
        pw2 = attrs.get('confirm_password')
        if pw != pw2:
            raise serializers.ValidationError({
                'confirm_password': "Passwords do not match."
            })
        return attrs
