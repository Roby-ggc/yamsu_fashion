from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from shop.views import create_admin, load_products


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('shop.urls')),

    # temporaire : création admin Render
    path('create-admin/', create_admin),

    # temporaire : import produits
    path('load-products/', load_products),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )