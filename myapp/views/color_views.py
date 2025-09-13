# views.py
from rest_framework import viewsets
from rest_framework import permissions, generics
from ..models.color import Color
from ..serializers.color_serializer import ColorSerializer,ColorCreateSerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class ColorCreateView(generics.CreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorCreateSerializer
    permission_classes = [permissions.AllowAny]