from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^conf$', include(admin.site.urls)),
    url(r'^confirm/(?P<activation_key>[a-f0-9]{40})$', 'list.views.confirm_email'),
    url(r'^unsubscribe/(?P<activation_key>[a-f0-9]{40})$', 'list.views.unsubscribe'),
    url(r'^subscribe/(?P<group_name>\w+)$', 'list.views.subscribe')
)
