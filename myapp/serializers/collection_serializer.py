# serializers.py
from rest_framework import serializers
from ..models.collection import Collection
from ..models.format import Format
from ..models.color import Color
from ..models.theme_color import Theme as Theme      # ← your model is ThemeColor
from ..models.bridges import CollectionTheme, FormatTheme
from ..serializers.color_serializer import ColorSerializer
from ..serializers.format_serializer import FormatSerializer


class RelativeImageField(serializers.ImageField):
    """
    Return a relative URL like '/media/collections/Basic_Zellige.png'
    (no scheme/host). If no image, return None.
    """
    def to_representation(self, value):
        if not value:
            return None
        # value.url respects MEDIA_URL and will be relative (e.g., '/media/...') if MEDIA_URL is relative
        return value.url


class CollectionSerializer(serializers.ModelSerializer):
    image = RelativeImageField(read_only=True)
    formats = FormatSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'


class CollectionCreateSerializer(serializers.ModelSerializer):
    """
    Create-only serializer. Accepts an uploaded image and a list of theme IDs to
    link at the collection level. Returns image as a relative URL.
    """
    theme_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )
    image = RelativeImageField(required=False, allow_null=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'description', 'type', 'image', 'theme_ids']

    def validate_theme_ids(self, value):
        # Ensure all theme ids exist; DRF will still accept repeated form-data keys
        missing = []
        for tid in value:
            if not Theme.objects.filter(pk=tid).exists():
                missing.append(tid)
        if missing:
            raise serializers.ValidationError(f"Unknown theme_ids: {missing}")
        return value

    def create(self, validated_data):
        theme_ids = validated_data.pop('theme_ids', [])
        collection = super().create(validated_data)

        for tid in theme_ids:
            theme = Theme.objects.get(pk=tid)
            CollectionTheme.objects.get_or_create(collection=collection, theme=theme)

        return collection

    # Ensure response also shows relative image path after create
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # image already handled by RelativeImageField; just return
        return data
