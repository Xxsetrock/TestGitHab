from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'sisventas.views.home', name='home'),
    #url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    ##url(r'^$',principal),


    url(r'^', include('sisventas.apps.inicio.urls')),
    url(r'^registrarse/', include('sisventas.apps.inicio.urls')),


    url(r'^user/login/$', 'sisventas.apps.autenticacion.views.loguet_in'),
    url(r'^private/$', 'sisventas.apps.autenticacion.views.private'),
    url(r'^user/resetpass/$', 'sisventas.apps.autenticacion.views.reset_pass'),
    url(r'^salir/$', 'sisventas.apps.autenticacion.views.loguet_out'),
	#url(r'^auth/', include('sisventas.apps.autenticacion.urls')),  


    url(r'^administrador/$', 'sisventas.apps.autenticacion.views.administrador'),
    url(r'^cliente/$', 'sisventas.apps.cliente.views.new_cliente'),
    url(r'^new_producto/$', 'sisventas.apps.producto.views.new_producto'),
    url(r'^new_categoria/$', 'sisventas.apps.producto.views.new_categoria'),
    url(r'^listar_producto/$', 'sisventas.apps.producto.views.listar_producto'),
    url(r'^eliminar_producto/([0-9]{1,2})/$', 'sisventas.apps.producto.views.eliminar'),
    url(r'^listar_producto/$', 'sisventas.apps.producto.views.listar_producto'),
    url(r'^modificar_producto/([0-9]{1,2})/$','sisventas.apps.producto.views.modificar_producto'),
    url(r'^ver_productos/$', 'sisventas.apps.producto.views.listadodeTodo'),

    url(r'^listado_por_categorias/(?P<categoria>\d+)/$','sisventas.apps.producto.views.ListadoPorCategoria'),
    url(r'^listado_por_categorias/(?P<idp>\d+)/(?P<idc>\d+)/$','sisventas.apps.producto.views.borrarRel'),



    url(r'^eliminar_usuario/([0-9]{1,2})/$', 'sisventas.apps.inicio.views.eliminar_usuario'),

    url(r'^modificar_usuario/([0-9]{1,2})/$', 'sisventas.apps.inicio.views.modificar_usuario'),
    url(r'^listar_usuario/$', 'sisventas.apps.inicio.views.listar_usuario'),


    url(r'^listar_cliente/$', 'sisventas.apps.cliente.views.listar_cliente'),
    url(r'^eliminar_cliente/([0-9]{1,2})/$', 'sisventas.apps.cliente.views.eliminar_cliente'),
    url(r'^modificar_cliente/([0-9]{1,2})/$','sisventas.apps.cliente.views.modificar_cliente'),


    url(r'^new_venta/$', 'sisventas.apps.venta.views.new_venta'),


    url(r'^reporte/$', 'sisventas.apps.venta.views.reporte'),
    url(r'^buscar/$', 'sisventas.apps.venta.views.buscar'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
