from rest_framework.generics import RetrieveAPIView

from apps.core.models import Theme

from .serializers import ThemeSerializer


class ThemeView(RetrieveAPIView):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()
