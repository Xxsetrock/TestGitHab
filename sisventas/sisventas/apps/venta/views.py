from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from forms import new_ventaForm,buscarCliente,detalleForm
from models import newventa,detalle,factura
from django.contrib.auth.decorators import login_required, permission_required
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sisventas.settings import MEDIA_ROOT
from sisventas.apps.cliente.models import client
from sisventas.apps.producto.models import newproducto,Categoria
from sisventas.apps.inicio.models import Temporal
from django.contrib.auth.models import User
from datetime import datetime 
# Create your views here.
import csv
import  json
from django.http import HttpResponse
@login_required(login_url='/user/login')
def new_venta(request):
	tempo=Temporal.objects.get(id=1)
	#return HttpResponse(tempo.id)
	if tempo.activo==0:
		uuu=User.objects.last()
		ccc=client.objects.last()
		ppp=newproducto.objects.all()
		#return HttpResponse(ppp)
		vvvv=newventa.objects.create(user=uuu,cliente=ccc,PrecioTotal=0,CantidadTotal=0,fecha=datetime.now())
		vvvv.producto=ppp
		tempo.activo=1
		tempo.save()
		vvvv.save()
		#ddd=detalle.objects.create(venta=vvvv,producto=ppp,cantidad=0,precio=0,activo=0)
		




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
			if tempo.activo==1:
				eliminar=newventa.objects.get(id=1).delete()
				eli=client.objects.get(id=1).delete()
				tempo.activo=2
				tempo.save()
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
		if producto.cantidad>=1:
			
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
def Calendario(request):
	return render_to_response("Calendario.html",{})
 
@login_required(login_url='/user/login')
def listaFacturas(request):
	facturas=factura.objects.all()
	return render_to_response("listaFacturas.html",{"factura":facturas},context_instance=RequestContext(request))


def androi(request):
	lista=newproducto.objects.all()
	return render_to_response("androi.html",{"lista":lista},context_instance=RequestContext(request))




@login_required(login_url='/user/login')
def VerFactura(request,id,id_f):
	from reportlab.pdfgen import canvas
	from reportlab.lib.pagesizes import letter,A4
	from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Image,Table,TableStyle #librerias para ejustar el texto
	from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
	from reportlab.lib.enums import TA_JUSTIFY 
	from reportlab.lib import colors
	url=os.path.join(MEDIA_ROOT,"pdf\proyecto.pdf")
	venta=newventa.objects.get(id=id)

	
	c=canvas.Canvas(url,pagesize=letter)
	c.setFillColorRGB(0,0,0.5)
	fecha = datetime.now()
	fecha = fecha.strftime('%Y%m%d')
	preciott=int(venta.PrecioTotal)
	codigo = calculo('50213546134648', str(venta.id),str(venta.cliente.ci),str(fecha),str(preciott),"!@#$%&/()=? ")

	c.drawString(362,675,"%s "%(codigo))



	
	c.setFont("Helvetica",15)
	c.setFillColorRGB(0,0,0.5)
	c.drawString(210,730,"FACTURA")

	c.setFont("Helvetica",10)
	c.drawString(370,750,"NIT: 3712482014")
	c.setFont("Helvetica",10)
	c.drawString(385,740,"FACTURA")

	c.setFont("Helvetica",12)
	c.setFillColorRGB(5,0,0)
	c.drawString(375,725,"Nro")
	c.drawString(400,725,"%s "%(id_f))

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
	venta_pro=venta.producto.all()
	pp=550
	for j in venta_pro:
		aaa=detalle.objects.get(venta=venta.id,producto=j.id)
		produ=newproducto.objects.get(id=aaa.producto.id)
		if aaa.cantidad > 0:
			c.drawString(380,pp,"%s "%(produ.precio))
			c.drawString(40,pp,"%s "%(aaa.cantidad))
			c.drawString(100,pp,"%s "%(newproducto.objects.get(id=j.id)))
			c.drawString(450,pp,"%s "%(aaa.precio))
			pp=pp-20
	c.drawString(450,368,"%s "%(venta.PrecioTotal))


	
	#vvvv=newventa.objects.create(user=uuu,cliente=ccc,PrecioTotal=0,CantidadTotal=0,fecha=datetime.now())


	c.save()
	return HttpResponseRedirect("/media/pdf/proyecto.pdf")


@login_required(login_url='/user/login')
def facturaV(request):
	from reportlab.pdfgen import canvas
	from reportlab.lib.pagesizes import letter,A4
	from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Image,Table,TableStyle #librerias para ejustar el texto
	from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
	from reportlab.lib.enums import TA_JUSTIFY 
	from reportlab.lib import colors
	url=os.path.join(MEDIA_ROOT,"pdf\proyecto.pdf")
	venta=newventa.objects.last()

	
	c=canvas.Canvas(url,pagesize=letter)
	c.setFillColorRGB(0,0,0.5)
	fecha = datetime.now()
	fecha = fecha.strftime('%Y%m%d')
	preciott=int(venta.PrecioTotal)
	codigo = calculo('50213546134648', str(venta.id),str(venta.cliente.ci),str(fecha),str(preciott),"!@#$%&/()=? ")

	c.drawString(362,675,"%s "%(codigo))

	ff=factura.objects.create(cliente=venta.cliente,user=venta.user,codigo=codigo,venta=venta)


	
	c.setFont("Helvetica",15)
	c.setFillColorRGB(0,0,0.5)
	c.drawString(210,730,"FACTURA")

	c.setFont("Helvetica",10)
	c.drawString(370,750,"NIT: 3712482014")
	c.setFont("Helvetica",10)
	c.drawString(385,740,"FACTURA")

	c.setFont("Helvetica",12)
	c.setFillColorRGB(5,0,0)
	c.drawString(375,725,"Nro")
	c.drawString(400,725,"%s "%(ff.id))

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
	venta_pro=venta.producto.all()
	pp=550
	for j in venta_pro:
		aaa=detalle.objects.get(venta=venta.id,producto=j.id)
		produ=newproducto.objects.get(id=aaa.producto.id)
		if aaa.cantidad > 0:
			c.drawString(380,pp,"%s "%(produ.precio))
			c.drawString(40,pp,"%s "%(aaa.cantidad))
			c.drawString(100,pp,"%s "%(newproducto.objects.get(id=j.id)))
			c.drawString(450,pp,"%s "%(aaa.precio))
			pp=pp-20
	c.drawString(450,368,"%s "%(venta.PrecioTotal))


	
	#vvvv=newventa.objects.create(user=uuu,cliente=ccc,PrecioTotal=0,CantidadTotal=0,fecha=datetime.now())


	c.save()
	return HttpResponseRedirect("/media/pdf/proyecto.pdf")

def calculo(auto,factura,nit,fecha,monto,llave):
	auto=auto+str(digito(auto))
	factura=factura+str(digito(factura))
	nit=nit+str(digito(nit))
	fecha=fecha+str(digito(fecha))
	monto=monto+str(digito(monto))
	suma=int(auto)+int(factura)+int(nit)+int(fecha)+int(monto)
	modulo=getModulo(suma)
	base64=getBase64(modulo)
	return getRC4(base64,llave)
	




def getBase64(numero):
	diccionario=["0", "1", "2", "3", "4", "5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K" ,"L","M","N","O","P","Q","R","S","T","U","V" ,"W","X","Y","Z","a","b","c","d","e","f","g" ,"h","i","j","k","l","m","n","o","p","q","r" ,"s","t","u","v","w","x","y","z","+","/"]
	cociente=1
	resto=0
	palabra=""
	while cociente > 0:
		cociente=numero/64
		resto=numero%64
		palabra=diccionario[resto]+palabra
		numero=cociente
	return palabra
	
def invertir(numero):
	return numero[::-1]

def digito(numero):
	inv=[0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
	mul=[ [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ], [ 1, 2, 3, 4, 0, 6, 7, 8, 9, 5 ], [ 2, 3, 4, 0, 1, 7, 8, 9, 5, 6 ], [ 3, 4, 0, 1, 2, 8, 9, 5, 6, 7 ], [ 4, 0, 1, 2, 3, 9, 5, 6, 7, 8 ], [ 5, 9, 8, 7, 6, 0, 4, 3, 2, 1 ], [ 6, 5, 9, 8, 7, 1, 0, 4, 3, 2 ], [ 7, 6, 5, 9, 8, 2, 1, 0, 4, 3 ], [ 8, 7, 6, 5, 9, 3, 2, 1, 0, 4 ], [ 9, 8, 7, 6, 5, 4, 3, 2, 1, 0 ] ]
	per=[ [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ], [ 1, 5, 7, 6, 2, 8, 3, 0, 9, 4 ], [ 5, 8, 0, 3, 7, 9, 6, 1, 4, 2 ], [ 8, 9, 1, 6, 0, 4, 3, 5, 2, 7 ], [ 9, 4, 5, 3, 1, 2, 6, 8, 7, 0 ], [ 4, 2, 8, 6, 5, 7, 3, 9, 0, 1 ], [ 2, 7, 9, 3, 8, 0, 6, 4, 1, 5 ], [ 7, 0, 4, 6, 9, 1, 3, 2, 5, 8 ] ]
	num_inv=invertir(numero)
	i=0
	check=0
	while i<len(num_inv):
		aux1= (i+1)%8
		aux2= int(num_inv[i])

		aux3= per[aux1][aux2]
		check=mul[check][aux3]
		i=i+1
	return inv[check]

def getModulo(numero):
	return numero % 1073741823

def getRC4(numero,llave):
	estado=[]
	codigo=""
	nrohex=""
	x,y,index1,index2,nmen,i,op1,aux,op2=0,0,0,0,0,0,0,0,0
	while i<=255:
		estado.append(1)
		estado[i]=i
		i=i+1
	i=0
	while(i<=255):
		if llave[index1]==" ":
			op1=191
		else:
			op1=ord(llave[index1])
		index2=(op1 + estado[i] + index2) % 256
		aux = estado[i]
		estado[i] = estado[index2]
		estado[index2] = aux
		index1=(index1 + 1) % len(llave)
		i=i+1
	i=0
	while(i<len(numero)):
		x=(x + 1) % 256
		y=(estado[x] + y) % 256
		aux=estado[x]
		estado[x]=estado[y]
		estado[y]=aux
		op1=ord(numero[i])
		op2=estado[(estado[x] + estado[y]) % 256]
		nmen=op1^op2
		nrohex=hex(nmen).upper()[2:]
		if len(nrohex)==1:
			nrohex="0"+nrohex
		codigo=codigo+nrohex+"-"
		i=i+1
	return codigo[0:len(codigo)-1]


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
	from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Image,Table,TableStyle,PageBreak #librerias para ejustar el texto
	from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
	from reportlab.lib.enums import TA_JUSTIFY 
	from reportlab.lib import colors
	url=os.path.join(MEDIA_ROOT,"pdf\ReporteUsuario.pdf")
	c=canvas.Canvas(url,pagesize=letter)






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
	total_dia=0
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
				if pp<40:
					pp=670
					c.showPage()
		p=pp-70
		if p<40:
			p=670
			c.showPage()
		c.drawString(380,p+60,"%s "%("TOTAL"))
		c.drawString(490,p+60,"%s "%(i.PrecioTotal))
		total_dia=total_dia+i.PrecioTotal
		c.line(70,p+80,570,p+80)
	c.setFillColorRGB(8,0,0)
	c.drawString(80,p,"%s "%("Total dia : "))
	c.drawString(170,p,"%s "%(total_dia))
	c.save();

	return HttpResponseRedirect("/media/pdf/ReporteUsuario.pdf")