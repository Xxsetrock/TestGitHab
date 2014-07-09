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



    url(r'^ver_productoss/$', 'sisventas.apps.producto.views.listadodeTodoo'),
    url(r'^listado_por_categoriass/(?P<categoria>\d+)/$','sisventas.apps.producto.views.ListadoPorCategoriaa'),





    url(r'^eliminar_usuario/([0-9]{1,2})/$', 'sisventas.apps.inicio.views.eliminar_usuario'),

    url(r'^modificar_usuario/([0-9]{1,2})/$', 'sisventas.apps.inicio.views.modificar_usuario'),
    url(r'^listar_usuario/$', 'sisventas.apps.inicio.views.listar_usuario'),


    url(r'^listar_cliente/$', 'sisventas.apps.cliente.views.listar_cliente'),
    url(r'^eliminar_cliente/([0-9]{1,2})/$', 'sisventas.apps.cliente.views.eliminar_cliente'),
    url(r'^modificar_cliente/([0-9]{1,2})/$','sisventas.apps.cliente.views.modificar_cliente'),


    url(r'^new_venta/$', 'sisventas.apps.venta.views.new_venta'),
    url(r'^detalle/(?P<id>\d+)/$', 'sisventas.apps.venta.views.detalleventa'),
    url(r'^cancelarVenta/$','sisventas.apps.venta.views.cancelarVenta'),



    url(r'^factura/$', 'sisventas.apps.venta.views.facturaV'),
    url(r'^ReporteUsuario/$', 'sisventas.apps.venta.views.ReporteUsuario'),
    url(r'^buscar/$', 'sisventas.apps.venta.views.buscar'),


    url(r'^ReporteDiario/$', 'sisventas.apps.inicio.views.ReporteDiario'),
    url(r'^ReporteAnual/$', 'sisventas.apps.inicio.views.ReporteAnual'),
    url(r'^ReporteMensual/$', 'sisventas.apps.inicio.views.ReporteMensual'),
    url(r'^Calendario/$', 'sisventas.apps.venta.views.Calendario'),


    url(r'^aumentarStock/([0-9]{1,2})/$', 'sisventas.apps.producto.views.aumentarStock'),
    url(r'^listaFacturas/$', 'sisventas.apps.venta.views.listaFacturas'),
    url(r'^VerFactura/([0-9]{1,2})/([0-9]{1,2})/$', 'sisventas.apps.venta.views.VerFactura'),


    url(r'^androi/$', 'sisventas.apps.venta.views.androi'),
    





)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
