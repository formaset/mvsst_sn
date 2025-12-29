from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.defaults import page_not_found, server_error
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls


def custom_page_not_found(request, exception):
    return page_not_found(request, exception, template_name="errors/404.html")


def custom_server_error(request):
    return server_error(request, template_name="errors/500.html")


urlpatterns = [
    path(f"{settings.ADMIN_PATH}/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]

handler404 = "mvsst.urls.custom_page_not_found"
handler500 = "mvsst.urls.custom_server_error"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
