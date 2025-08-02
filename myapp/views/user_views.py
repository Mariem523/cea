from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers.user_serializers import (
    AdminCreationSerializer,
    LoginSerializer,
    AddUserSerializer,UserSerializer,ResetPasswordSerializer
)

User = get_user_model()

class AdminCreationView(APIView):
    authentication_classes = []  # open
    permission_classes = []      # open

    def post(self, request, *args, **kwargs):
        # simply create the admin user
        serializer = AdminCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin = serializer.save()
        return Response(
            {"username": admin.username, "role": "admin"},
            status=201
        )

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        role = 'admin' if user.is_staff else 'user'
        return Response({'token': token.key, 'role': role})

class AddUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = AddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        return Response(
            {"username": new_user.username, "role": "user"},
            status=201
        )

class UserListView(generics.ListAPIView):
    """
    List all users excluding any admin accounts.
    Only accessible to token‑authenticated admins.
    """
    serializer_class    = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        # exclude staff/superuser accounts
        return User.objects.filter(is_staff=False, is_superuser=False)
    

class ResetUserPasswordView(APIView):
    """
    POST a new password for a given user ID,
    overwriting their old one.
    Only accessible to token‑authenticated admins.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(
            {'detail': f"Password for user `{user.username}` has been reset."},
            status=status.HTTP_200_OK
        )
