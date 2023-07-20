from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls', namespace='app')),
    path('dash/',include('dash.urls', namespace='dash'))
]+ static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
