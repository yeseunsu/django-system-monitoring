from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
#admin.autodiscover()

#router = routers.DefaultRouter()
#router.register(r'server', views.ServerViewSet)
#router.register(r'process', views.ProcessViewSet)
#router.register(r'processStatus', views.ProcessStatusViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'as_monitoring.views.home', name='home'),
    # url(r'^as_monitoring/', include('as_monitoring.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # url(r'^', include(router.urls)),
    
    # For rest api    
    url(r'^server/$', 'as_status.views.server_list'),
    url(r'^server/(?P<pk>[0-9]+)', 'as_status.views.server_detail'),
    
    url(r'^process/$', 'as_status.views.process_list'),
    url(r'^process/(?P<pk>[0-9]+)', 'as_status.views.process_detail'),
    
    url(r'^processStatus/$', 'as_status.views.processStatus_list'),
    url(r'^processStatus/(?P<pk>[0-9]+)', 'as_status.views.processStatus_detail'),

    url(r'^serverStatus/$', 'as_status.views.serverStatus_list'),
    url(r'^serverStatus/(?P<pk>[0-9]+)', 'as_status.views.serverStatus_detail'),
    
    url(r'^openstackServiceStatus/$', 'as_status.views.openstackServiceStatus_list'),
    url(r'^openstackServiceStatus/(?P<pk>[0-9]+)', 'as_status.views.openstackServiceStatus_detail'),

    url(r'^openstackResourceStatus/$', 'as_status.views.openstackResourceStatus_list'),
    url(r'^openstackResourceStatus/(?P<pk>[0-9]+)', 'as_status.views.openstackResourceStatus_detail'),

    url(r'^znodeStatus/$', 'as_status.views.znodeStatus_list'),
    url(r'^znodeStatus/(?P<pk>[0-9]+)', 'as_status.views.znodeStatus_detail'),
    
    url(r'^mongoStatus/$', 'as_status.views.mongoStatus_list'),
    url(r'^mongoStatus/(?P<pk>[0-9]+)', 'as_status.views.mongoStatus_detail'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # For front web
    url(r'^status','as_status_web.views.index', name='index'),
    
    # For login
    url(r'^login/$', 'django.contrib.auth.views.login',name="my_login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    
)
