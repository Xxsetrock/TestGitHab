from django.conf.urls import patterns, include, url
from .views import index
from .views import registro
from .views import loguet_out,loguet_in,reset_pass,administrador
urlpatterns = patterns('',
 	#url(r'^$','django.contrib.auth.views.login',{'template_name':'index.html'},name='login'),

 	#url(r'^cerrar/$','django.contrib.auth.views.logout_then_login',name='logout'),
 	#url(r'^registrarse/$',Registrarse.as_view(),name='registrarse')
	url(r'^salir/',loguet_out),
	url(r'^user/login/',loguet_in),
	url(r'^user/reset/',reset_pass),
	#registro de usuario
)

