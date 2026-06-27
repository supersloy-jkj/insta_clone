from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),           # Feed is at /
    path('users/', include('users.urls')),
    path('stories/', include('stories.urls')),
    path('messages/', include('messaging.urls')),
]

# MEDIA is served by Django in both dev AND prod, since WhiteNoise only
# handles STATIC files, not user-uploaded MEDIA files.
# Note: this is a functional stopgap for the free tier — Render's disk is
# ephemeral, so uploads still won't survive a restart/redeploy. Cloudinary
# (or similar) is the real long-term fix — see README.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
