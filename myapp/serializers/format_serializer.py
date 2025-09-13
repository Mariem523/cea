# serializers/format_serializer.py
from rest_framework import serializers
from ..models.format import Format
from ..models.bridges import FormatTheme
# If your model class is ThemeColor, import it like this:
from ..models.theme_color import Theme as Theme
# from ..serializers.color_serializer import ColorSerializer  # uncomment if you actually need nested colors

class RelativeImageField(serializers.ImageField):
    """
    Return a relative URL like '/media/formats/file.png' (no scheme/host).
    """
    def to_representation(self, value):
        if not value:
            return None
        return value.url  # uses settings.MEDIA_URL; stays relative

class FormatSerializer(serializers.ModelSerializer):
    image = RelativeImageField(read_only=True)
    # colors = ColorSerializer(many=True, read_only=True)  # keep if needed

    class Meta:
        model = Format
        fields = '__all__'

class FormatCreateSerializer(serializers.ModelSerializer):
    image = RelativeImageField(required=False, allow_null=True)
    theme_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )

    class Meta:
        model = Format
        fields = ['id', 'title', 'description', 'image', 'collection', 'theme_ids']

    def validate_theme_ids(self, value):
        missing = [tid for tid in value if not Theme.objects.filter(pk=tid).exists()]
        if missing:
            raise serializers.ValidationError(f"Unknown theme_ids: {missing}")
        return value

    def validate(self, attrs):
        if not attrs.get('collection'):
            raise serializers.ValidationError("Collection is required.")
        return attrs

    def create(self, validated_data):
        theme_ids = validated_data.pop('theme_ids', [])
        fmt = super().create(validated_data)
        for tid in theme_ids:
            theme = Theme.objects.get(pk=tid)
            FormatTheme.objects.get_or_create(format=fmt, theme=theme)
        return fmt
