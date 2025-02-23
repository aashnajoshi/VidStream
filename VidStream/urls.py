import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('debug/', include(debug_toolbar.urls)),
    path('home/', include('home.urls')),
    path('stream/', include('stream.urls')),
    path('accounts/', include('allauth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)