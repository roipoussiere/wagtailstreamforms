from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls


urlpatterns = [
    re_path(r'^admin/', include(wagtailadmin_urls)),
    re_path(r'', include(wagtail_urls)),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
