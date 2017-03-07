from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import notifications.urls

urlpatterns = [
    url(r'^', include('job.urls')),
    url(r'^admin/', admin.site.urls),
     url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
