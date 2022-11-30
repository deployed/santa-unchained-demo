from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from santa_unchained.accounts import urls as accounts_urls
from santa_unchained.wishes import urls as wishes_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include(accounts_urls)),
    path("wishes/", include(wishes_urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
