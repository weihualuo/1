from django.conf.urls import patterns, include, url

from rest_framework import routers
from invt.views import MetaView, Information, Task
from users.views import UserViewSet, AuthView
from templates.views import TemplateViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet, 'user')
router.register(r'templates', TemplateViewSet, 'templates')
# router.register(r'(?P<name>\w+)/(?P<id>\d+)/comments', CommentViewSet, 'comments')

from django.contrib import admin
admin.autodiscover()

#from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api/meta$', ensure_csrf_cookie(MetaView.as_view()), name='meta'),
    url(r'^info/(?P<app>\w+)/(?P<item>\w+)$', Information.as_view(), name='info'),
    url(r'^task/(?P<id>\w+)$', Task.as_view(), name='task'),
    url(r'^auth/(?P<id>\w+)$', AuthView.as_view(), name='auth'),
)

from invt import settings
import os
#Serve media file
if not 'SERVER_SOFTWARE' in os.environ:
    urlpatterns += patterns('',
        (r'^u/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
# Serve static files for admin, use this for debug usage only
# `python manage.py collectstatic` is preferred.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()