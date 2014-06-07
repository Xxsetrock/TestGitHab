from django.conf.urls import patterns, include, url
from .views import index
from .views import registro
urlpatterns = patterns('',
 	#url(r'^$','django.contrib.auth.views.login',{'template_name':'index.html'},name='login'),

 	#url(r'^cerrar/$','django.contrib.auth.views.logout_then_login',name='logout'),
 	#url(r'^registrarse/$',Registrarse.as_view(),name='registrarse')
 	url(r'^$',index),
	#url(r'^index/',index),
	url(r'^registrarse/',registro),
	#url(r'^registrarse/','registro',name='vista_registro'),
	#registro de usuario
	#url(r'^$', 'myapp.views.main', name='main'),
    #url(r'^signup$', 'myapp.views.signup', name='signup'),

)
