from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'distrito.views.home', name='home'),
    # url(r'^distrito/', include('distrito.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.home', name='home'),
    url(r'^login/$', 'login.views.login_user', name='login_user'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),
)
