from rest_framework.serializers import ModelSerializer

from apps.core.models import Theme


class ThemeSerializer(ModelSerializer):

    class Meta:
        model = Theme
        fields = ['primary_color', 'css', 'supported_theme']
        read_only_fields = fields
