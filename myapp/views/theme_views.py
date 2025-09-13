from ..models.collection import Collection
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import permissions, generics
from rest_framework import serializers
from django.db.models import Prefetch
from ..models.theme_color import Theme
from ..models.color import Color
from ..models.format import Format

from ..serializers.theme_serializer import ThemeCreateSerializer, ThemeWithColorsSerializer


class ThemeCreateView(generics.CreateAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeCreateSerializer
    permission_classes = [permissions.AllowAny]


class ThemesWithColorsByCollectionView(generics.ListAPIView):
    """
    GET /api/collections/<collection_id>/themes-with-colors/
    Only valid for collections of type DIRECT_COLORS.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ThemeWithColorsSerializer

    def get_queryset(self):
        collection_id = self.kwargs['collection_id']
        collection = get_object_or_404(
            Collection.objects.only('id', 'type'),
            pk=collection_id
        )

        # Hard-rule: this endpoint is NOT allowed for WITH_FORMATS
        if collection.type != Collection.CollectionType.DIRECT_COLORS:
            # 404 so clients switch to the formats endpoint
            raise Http404(
                f"Collection {collection_id} requires format context. "
                f"Use /api/collections/{collection_id}/formats/<format_id>/themes-with-colors/."
            )

        filtered_colors = Color.objects.filter(
            collection_id=collection_id
        ).order_by('id')

        return (
            Theme.objects.filter(
                collection_themes__collection_id=collection_id,
                collection_themes__is_active=True,
                colors__collection_id=collection_id,
            )
            .distinct()
            .prefetch_related(Prefetch('colors', queryset=filtered_colors))
            .order_by('id')
        )


class ThemesWithColorsByFormatView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ThemeWithColorsSerializer

    def get_queryset(self):
        collection_id = self.kwargs['collection_id']
        format_id = self.kwargs['format_id']

        # Ensure the format belongs to the collection
        get_object_or_404(
            Format.objects.only('id', 'collection_id'),
            pk=format_id, collection_id=collection_id
        )

        filtered_colors = Color.objects.filter(
            collection_id=collection_id,
            format_id=format_id
        ).order_by('id')

        return (
            Theme.objects.filter(
                # 🔽 rely solely on Color FK linkage
                colors__collection_id=collection_id,
                colors__format_id=format_id,
            )
            .distinct()
            .prefetch_related(Prefetch('colors', queryset=filtered_colors))
            .order_by('id')
        )
