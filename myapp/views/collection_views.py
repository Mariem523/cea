# views.py
from rest_framework.views import APIView
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from ..models.collection import Collection
from ..serializers.collection_serializer import CollectionSerializer,CollectionCreateSerializer

class CollectionCreateView(generics.CreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionCreateSerializer
    permission_classes = [permissions.AllowAny]
    
# class CollectionCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = CollectionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CollectionListView(APIView):
    def get(self, request, *args, **kwargs):
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)