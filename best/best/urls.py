from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'best.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/css'}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/img'}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/js'}),
    url(r'^font-awesome/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/font-awesome'}),
    url(r'', 'fork.views.compare'),
    url(r'^admin/', include(admin.site.urls)),
)
