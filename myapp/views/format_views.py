# views.py
from rest_framework import permissions, generics
from rest_framework import viewsets
from ..models.format import  Format
from ..serializers.format_serializer import  FormatSerializer,FormatCreateSerializer

class FormatViewSet(viewsets.ModelViewSet):
    queryset = Format.objects.select_related('collection').all()
    serializer_class = FormatSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        collection_id = self.request.query_params.get('collection')
        if collection_id:
            qs = qs.filter(collection_id=collection_id)
        return qs
    
class CollectionFormatsListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FormatSerializer

    def get_queryset(self):
        collection_id = self.kwargs["collection_id"]
        return Format.objects.select_related("collection").filter(collection_id=collection_id)

class FormatCreateView(generics.CreateAPIView):
    queryset = Format.objects.all()
    serializer_class = FormatCreateSerializer
    permission_classes = [permissions.AllowAny]