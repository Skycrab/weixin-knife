from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'brain.views.home', name='home'),
    # url(r'^brain/', include('brain.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^do$', 'question.views.do'),
    url(r'^oauth', 'question.views.oauth'),
    url(r'^share', 'question.views.share'),
    url(r'^wxpay/', 'question.views.pay'),
    url(r'^paydetail', 'question.views.paydetail'),
    url(r'^payback', 'question.views.payback'),
)
