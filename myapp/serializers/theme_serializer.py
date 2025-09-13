from rest_framework import serializers
from ..models.theme_color import Theme
from ..models.color import Color


class ThemeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'title']
class RelativeImageField(serializers.ImageField):
    def to_representation(self, value):
        return value.url if value else None

class ColorBriefSerializer(serializers.ModelSerializer):
    image = RelativeImageField(read_only=True)

    class Meta:
        model = Color
        fields = ['id', 'title', 'description', 'image', 'collection', 'format']

class ThemeWithColorsSerializer(serializers.ModelSerializer):
    # We’ll rely on a prefetched, *filtered* `colors` relation from the view,
    # so here we just read whatever is in `obj.colors.all()`.
    colors = ColorBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ['id', 'title', 'colors']