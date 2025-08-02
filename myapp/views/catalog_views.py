from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ..models.catalog import Catalog
from ..serializers.catalog_serializer import CatalogSerializer
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser


class PublicCatalogListView(generics.ListAPIView):
    """
    Anyone can see public catalogs.
    """
    queryset = Catalog.objects.filter(type=Catalog.PUBLIC)
    serializer_class = CatalogSerializer
    permission_classes = [AllowAny]

class PrivateCatalogListView(generics.ListAPIView):
    """
    Only authenticated admins can see private catalogs.
    """
    queryset = Catalog.objects.filter(type=Catalog.PRIVATE)
    serializer_class = CatalogSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


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


class CatalogPDFDownloadView(APIView):
    """
    Stream the catalog's PDF as a downloadable attachment.
    - Public: anyone
    - Private: only authenticated admins
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # we'll enforce admin for private below

    def get(self, request, pk, *args, **kwargs):
        catalog = get_object_or_404(Catalog, pk=pk)

        # enforce admin-only for private catalogs
        if catalog.type == Catalog.PRIVATE:
            user = request.user
            if not (user and user.is_authenticated):
                return Response(
                    {"detail": "You do not have permission to download this file."},
                    status=status.HTTP_403_FORBIDDEN
                )

        # try to open and stream the PDF
        file = catalog.pdf_file
        if not file or not file.name:
            raise Http404("No PDF found for this catalog.")

        try:
            handle = file.open('rb')
        except Exception:
            raise Http404("Could not open file.")

        # build response
        filename = file.name.rsplit('/', 1)[-1]
        response = FileResponse(handle, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
