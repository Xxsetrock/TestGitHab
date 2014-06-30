from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from forms import new_ventaForm,buscarCliente,detalleForm
from models import newventa,detalle
from django.contrib.auth.decorators import login_required, permission_required
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sisventas.settings import MEDIA_ROOT
from sisventas.apps.cliente.models import client
from sisventas.apps.producto.models import newproducto,Categoria
from datetime import datetime 
# Create your views here.
import csv
import  json
from django.http import HttpResponse
@login_required(login_url='/user/login')
def new_venta(request):
	lista=newproducto.objects.all()
	categorialista=Categoria.objects.all()
	if request.method=="POST":
		print  request.POST
		form=new_ventaForm(request.POST)
		if form.is_valid():
			form.save()
			venta=newventa.objects.last()
			venta2=int(venta.id)-1
			
			de=detalle.objects.filter(activo=0)
			#return HttpResponse(venta2)
			suma=0
			cant=0
			aux=0
			for i in de:
				i.activo=1
				i.venta=venta
				i.save()
				suma=float(suma+float(i.precio))
				cant=int(cant+int(i.cantidad))
			
			vv=newventa.objects.get(id=venta.id)
			#return HttpResponse(cant)
			vv.PrecioTotal=float(suma)
			vv.CantidadTotal=int(cant)
			vv.save()
			#return HttpResponse(vv.PrecioTotal,vv.CantidadTotal)
			
			
			return HttpResponseRedirect('/factura/')
	else:
		form=new_ventaForm()
	buscar=buscarCliente()
	return render_to_response('registrar_venta.html',{'new_venta':form,'buscar':buscar,'lista':lista,'cate':categorialista},context_instance = RequestContext(request))

@login_required(login_url='/user/login')
def cancelarVenta(request):
	#id_detalle=detalle.objects.last()
	lista_detalle=detalle.objects.filter(activo=0).delete()
	return HttpResponse(lista_detalle)
	
@login_required(login_url='/user/login')
def detalleventa(request,id):
	if request.method=="POST":
		producto=newproducto.objects.get(id=int(id))
		v=newventa.objects.last()
		pre=int(producto.precio)
		cant=request.POST["cantidad"]
		preci=float(float(cant)*float(pre))
		
		producto.cantidad=int(producto.cantidad)-int(cant)
		if producto.cantidad>=-1:
			
			d=detalle.objects.create(venta=v,producto=producto,cantidad=cant,precio=preci,activo=0)
			producto.save()
			return HttpResponse("Se registro la compra")
		else:
			d=detalle.objects.create(venta=v,producto=producto,cantidad=0,precio=preci,activo=0)
			return HttpResponse("No quedan productos en el stock")
	else:
		producto=newproducto.objects.get(id=int(id))
		form=detalleForm(instance=producto)
		idpro=id
	return render_to_response("detalle.html",{"detalle":form,"idpro":idpro},context_instance=RequestContext(request))

@login_required(login_url='/user/login')
def factura(request):
	from reportlab.pdfgen import canvas
	from reportlab.lib.pagesizes import letter,A4
	from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Image,Table,TableStyle #librerias para ejustar el texto
	from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
	from reportlab.lib.enums import TA_JUSTIFY 
	from reportlab.lib import colors
	url=os.path.join(MEDIA_ROOT,"pdf\proyecto.pdf")
	venta=newventa.objects.last()

	c=canvas.Canvas(url,pagesize=letter)
	c.setFont("Helvetica",15)
	c.setFillColorRGB(0,0,0.5)
	c.drawString(210,730,"FACTURA")

	c.setFont("Helvetica",10)
	c.drawString(370,750,"NIT: 3712482014")
	c.setFont("Helvetica",10)
	c.drawString(385,740,"FACTURA")

	c.setFont("Helvetica",12)
	c.setFillColorRGB(5,0,0)
	c.drawString(375,725,"Nro 017845")

	c.setFont("Helvetica",8)
	c.setFillColorRGB(0,0,0.5)
	c.drawString(330,715,"Nro DE AUTORIZACION 50213546134648")

	c.setFont("Helvetica",12)
	c.setFillColorRGB(5,0,0)
	c.drawString(352,695,"ORIGINAL CLIENTE")

	c.setFont("Helvetica",10)
	c.setFillColorRGB(0,0,0.5)
	c.drawString(60,745,"VENTAS POTOSI")
	c.drawString(57,725,"POTOSI - BOLIVIA")
	c.setFont("Helvetica",12)
	c.drawString(20,650,"Potosi,                                                                                                 NIT/CI:")
	c.drawString(20,620,"Senor(es),")
	c.drawString(80,620,"%s %s"%(venta.cliente.nombre,venta.cliente.apellido))
	#c.drawString(200,620,"%s %s"%(venta.cliente.apellido,""))
	c.drawString(420,650,"%s %s"%(venta.cliente.ci,""))
	c.drawString(60,650,"%s %s"%(venta.cliente.fecha.date(),""))
	c.line(20,600,545,600)
	c.line(20,600,20,400)
	c.line(545,600,545,400)
	c.line(20,400,545,400)

	c.line(20,570,545,570)

	c.line(90,600,90,400)
	c.line(150,600,150,400)
	c.line(370,600,370,400)
	c.line(440,600,440,400)

	c.line(20,390,545,390)
	c.line(20,390,20,350)
	c.line(545,390,545,350)
	c.line(20,350,545,350)

	c.setFont("Helvetica",9)
	c.drawString(27,583,"CANTIDAD")
	#c.drawString(103,583,"UNIDAD")
	c.drawString(230,583,"DESCRIPCION")
	c.drawString(380,583,"P. UNITARIO")
	c.drawString(460,583,"PRECIO TOTAL")

	c.setFont("Helvetica",8)
	c.setFillColorRGB(0,0,0.5)
	c.drawString(30,372,"Son : .................................................................................................................................................")
	c.drawString(50,358,"................................................................................................................................ Bolivianos")
	c.line(380,390,380,350)
	c.setFont("Helvetica",13)
	c.drawString(385,368,"TOTAL")

	c.save()
	return HttpResponseRedirect("/media/pdf/proyecto.pdf")


@login_required(login_url='/user/login')
def buscar(request):
	if request.method=='POST':
		form=buscarCliente(request.POST)
		print form
		cliente=client.objects.filter(ci=request.POST["buscarcliente"])
		if len(cliente)==0:
			return  HttpResponse(json.dumps({"idCli":-1}),content_type="application/json")
		return HttpResponse(json.dumps({"nombre":cliente[0].nombre,"idCli":cliente[0].id}),content_type="application/json")





@login_required(login_url='/user/login')
def ReporteUsuario(request):
	from reportlab.pdfgen import canvas
	from reportlab.lib.pagesizes import letter,A4
	from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Image,Table,TableStyle #librerias para ejustar el texto
	from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
	from reportlab.lib.enums import TA_JUSTIFY 
	from reportlab.lib import colors
	url=os.path.join(MEDIA_ROOT,"pdf\ReporteUsuario.pdf")
	c=canvas.Canvas(url,pagesize=letter)



	styleSheet=getSampleStyleSheet()
	story=[]
	h1=styleSheet['Heading1']
	h1.pageBreakBefore=1
	h1.keepWithNext=1
	h1.backColor=colors.red
	P1=Paragraph("Estilo Cabecerah1 ",h1)
	story.append(P1)
	style=styleSheet['BodyText']
	P2=Paragraph("EstiloBodyText",style)
	story.append(P2)



	c.setFont("Helvetica",15)
	c.setFillColorRGB(0,0,0)
	c.drawString(240,750,"VENTAS DEL DIA")

	c.setFillColorRGB(0.8,0,0)
	venta=newventa.objects.last()
	#venta=newventa.objects.get(fecha=datetime.now())
	c.drawString(120,720,"%s "%("Usuario:"))
	c.drawString(180,720,"%s "%(venta.user))
	c.drawString(340,720,"%s "%("Fecha:"))
	c.drawString(390,720,"%s "%(venta.fecha))
	c.line(30,700,580,700)
	c.line(30,697,580,697)
	#c.drawString(120,690,"%s "%(vent))
	lista=newventa.objects.filter(user=venta.user,fecha=datetime.now())

	#venta_pro=lista.producto.all()
	#ll=newventa.producto()
	#c.drawString(30,640,"%s "%(lista))
	
	
	p=650
	for i in lista:
		c.setFillColorRGB(0,0.8,0.5)
		c.drawString(50,p,"%s "%("      CLIENTE                  PRODUCTO                  CANTIDAD              PRECIO"))
		p=p-25;
		c.setFillColorRGB(0,0,0)
		c.drawString(70,p,"%s "%(i.cliente.nombre))
		#c.drawString(130,p,"%s "%(i.cliente.ci))
		venta_pro=i.producto.all()
		pp=p
		for j in venta_pro:
			aaa=detalle.objects.get(venta=i.id,producto=j.id)
			if aaa.cantidad > 0:
				c.drawString(200,pp,"%s "%(newproducto.objects.get(id=j.id)))
				c.drawString(400,pp,"%s "%(aaa.cantidad))
				c.drawString(490,pp,"%s "%(aaa.precio))
				pp=pp-20
		p=pp-70
		c.drawString(380,p+60,"%s "%("TOTAL"))
		c.drawString(490,p+60,"%s "%(i.PrecioTotal))
		c.line(70,p+80,570,p+80)

	c.save();

	return HttpResponseRedirect("/media/pdf/ReporteUsuario.pdf")