from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from myapp.permissions import IsMember
from ..models.catalog import Catalog
from ..serializers.catalog_serializer import CatalogSerializer
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import SessionAuthentication


# Optionally: custom permission for "members"
from rest_framework.permissions import BasePermission
class IsMember(BasePermission):
    message = "Members only."
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.groups.filter(name="members").exists())


class PublicCatalogListView(generics.ListAPIView):
    queryset = Catalog.objects.filter(type=Catalog.PUBLIC).order_by("created_at")
    serializer_class = CatalogSerializer
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]


class PrivateCatalogListView(generics.ListAPIView):
    queryset = Catalog.objects.filter(type=Catalog.PRIVATE).order_by("created_at")
    serializer_class = CatalogSerializer
    permission_classes = [IsAuthenticated, IsMember]
    authentication_classes = [SessionAuthentication]


class CatalogCreateView(generics.CreateAPIView):
    """
    Admins can create a new Catalog by sending multipart/form-data:
      - title: string
      - type: "public" or "private"
      - image: file (optional)
      - pdf_file: file (required)
    """
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated, IsAdminUser]

    # enable file uploads
    parser_classes = [MultiPartParser, FormParser]
    
# class PrivateCatalogListView(generics.ListAPIView):
#     queryset = Catalog.objects.filter(type=Catalog.PRIVATE)
#     serializer_class = CatalogSerializer
#     authentication_classes = [TokenAuthentication]  # or SessionAuth if you switch
#     permission_classes = [IsAuthenticated, IsMember]  # ✅ members only

class CatalogPDFDownloadView(APIView):
    authentication_classes = [TokenAuthentication]  # or SessionAuth later
    permission_classes = [AllowAny]  # keep; we’ll branch inside

    def get(self, request, pk, *args, **kwargs):
        catalog = get_object_or_404(Catalog, pk=pk)

        if catalog.type == Catalog.PRIVATE:
            # ✅ strictly require membership
            if not (request.user and request.user.is_authenticated
                    and request.user.groups.filter(name="members").exists()):
                return Response({"detail": "Members only."}, status=status.HTTP_403_FORBIDDEN)

        file = catalog.pdf_file
        if not file or not file.name:
            raise Http404("No PDF found.")

        handle = file.open('rb')
        filename = file.name.rsplit('/', 1)[-1]
        resp = FileResponse(handle, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="{filename}"'
        # Optional hardening:
        resp['X-Content-Type-Options'] = 'nosniff'
        return resp