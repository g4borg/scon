from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crafting/', 'dj.scon.views.crafting', name='scon_crafting'),
)

if settings.DEBUG or getattr(settings, 'SERVE_INTERNAL', False):
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views.serve'),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )