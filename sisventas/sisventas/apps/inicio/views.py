from django.shortcuts import render,render_to_response,get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required, permission_required
#from models import Registro
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.models import User
from forms import UsuarioForm
import os
from sisventas.apps.venta.models import newventa,detalle
from sisventas.settings import MEDIA_ROOT
from sisventas.apps.cliente.models import client
from sisventas.apps.producto.models import newproducto,Categoria
from sisventas.apps.venta.forms import new_ventaForm,buscarCliente,detalleForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime 
from models import Temporal
#from forms import RegistroForm

def index(request):
  d=Temporal.objects.create(activo=0)
  dd=Temporal.objects.last()
  if dd.id==1:
    c=client.objects.create(nombre="o",apellido="l",ci=1,direccion="a",telefono=1,fecha=datetime.now())
  return render_to_response("index.html",{},RequestContext(request))

@login_required(login_url='/user/login')
def registro(request):
  if request.method=='POST':
    formulario=UserCreationForm(request.POST)
    tipou=request.POST['stipo']
    #return HttpResponse(tipou)
    usuario=request.POST['username']
    if formulario.is_valid():
      formulario.save()
      u=User.objects.get(username=usuario)
      if tipou[0] == '1':
        u.is_superuser=True
        if tipou[1] == '1':
          u.is_staff=True
        else:
          u.is_staff=False
      else:
        u.is_staff=True
        if tipou[1] == '1':
          u.is_staff=True
        else:
          u.is_staff=False
      u.save()

      return HttpResponseRedirect('/user/login/')
  else:
    formulario=UserCreationForm()
  return render_to_response('registrarse.html',{'registro':formulario},context_instance=RequestContext(request))

@login_required(login_url='/user/login')
def eliminar_usuario(request,id):
  dato=get_object_or_404(User,pk=id)
  dato.delete()
  return render_to_response('eliminado.html',{'dato':dato},context_instance=RequestContext(request))

@login_required(login_url='/user/login')
def listar_usuario(request):
  producto=User.objects.all()
  return render_to_response('eliminar_usuario.html',{'eliminar':producto},context_instance=RequestContext(request))

@login_required(login_url='/user/login')
def modificar_usuario(request,id):
  cliente=get_object_or_404(User,pk=id)
  if request.method=='POST':
    formulario=UserCreationForm(request.POST,instance=cliente)
    formulario.save()
    return HttpResponseRedirect('/')
  else:
    formulario=UserCreationForm(instance=cliente)
  return render_to_response('modificar_usuario.html',{'formulario':formulario},context_instance=RequestContext(request))



@login_required(login_url='/user/login')
def ReporteDiario(request):
  from reportlab.pdfgen import canvas
  from reportlab.lib.pagesizes import letter,A4
  from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Image,Table,TableStyle,PageBreak #librerias para ejustar el texto
  from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
  from reportlab.lib.enums import TA_JUSTIFY 
  from reportlab.lib import colors
  url=os.path.join(MEDIA_ROOT,"pdf\ReporteDiario.pdf")
  c=canvas.Canvas(url,pagesize=letter)

  c.setFont("Helvetica",15)
  c.setFillColorRGB(0,0,0)
  c.drawString(240,750,"VENTAS DEL DIA")

  fe=datetime.now()
  c.drawString(265,730,"%s "%(fe.date()))

  total_dia=0
  #ll=newventa.objects.all().group_by('user')
  venta=newventa.objects.filter(fecha=datetime.now())
  p=700
  for i in venta:
    c.setFont("Helvetica",15)
    c.setFillColorRGB(0.8,0,0)
    c.drawString(120,p,"%s "%("Usuario:"))
    c.drawString(180,p,"%s "%(i.user))
    
    p=p-20
    c.line(30,p,580,p)
    p=p-3
    c.line(30,p,580,p)
    p=p-30

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
          pp=750
          c.showPage()
    p=pp-70
    if p<40:
      p=750
      c.showPage()
    c.drawString(380,p+60,"%s "%("TOTAL"))
    c.drawString(490,p+60,"%s "%(i.PrecioTotal))
    total_dia=total_dia+i.PrecioTotal
    c.line(70,p+80,570,p+80)

  c.setFillColorRGB(8,0,0)
  c.drawString(80,p,"%s "%("Total dia : "))
  c.drawString(170,p,"%s "%(total_dia))
  c.save()
  return HttpResponseRedirect("/media/pdf/ReporteDiario.pdf")


@login_required(login_url='/user/login')
def ReporteAnual(request):
  from reportlab.pdfgen import canvas
  from reportlab.lib.pagesizes import letter,A4
  from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Image,Table,TableStyle,PageBreak #librerias para ejustar el texto
  from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
  from reportlab.lib.enums import TA_JUSTIFY 
  from reportlab.lib import colors
  url=os.path.join(MEDIA_ROOT,"pdf\ReporteAnual.pdf")
  c=canvas.Canvas(url,pagesize=letter)

  c.setFont("Helvetica",15)
  c.setFillColorRGB(0,0,0)
  c.drawString(240,750,"VENTAS ANUAL")

  fe=datetime.now()
  fe=fe.date()
  c.drawString(280,730,"%s "%(fe.year))

  total_dia=0
  venta=newventa.objects.filter(fecha__year=fe.year)
  p=700
  for i in venta:
    c.setFont("Helvetica",15)
    c.setFillColorRGB(0.8,0,0)
    c.drawString(120,p,"%s "%("Usuario:"))
    c.drawString(180,p,"%s "%(i.user))
    c.drawString(340,p,"%s "%("Fecha:"))
    c.drawString(390,p,"%s "%(i.fecha))
    p=p-20
    c.line(30,p,580,p)
    p=p-3
    c.line(30,p,580,p)
    p=p-30

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
          pp=750
          c.showPage()
    p=pp-70
    if p<40:
      p=750
      c.showPage()
    c.drawString(380,p+60,"%s "%("TOTAL"))
    c.drawString(490,p+60,"%s "%(i.PrecioTotal))
    total_dia=total_dia+i.PrecioTotal
    c.line(70,p+80,570,p+80)

  c.setFillColorRGB(8,0,0)
  c.drawString(80,p,"%s "%("Total mes : "))
  c.drawString(170,p,"%s "%(total_dia))
  c.save()
  return HttpResponseRedirect("/media/pdf/ReporteAnual.pdf")



@login_required(login_url='/user/login')
def ReporteMensual(request):
  from reportlab.pdfgen import canvas
  from reportlab.lib.pagesizes import letter,A4
  from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Image,Table,TableStyle,PageBreak #librerias para ejustar el texto
  from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
  from reportlab.lib.enums import TA_JUSTIFY 
  from reportlab.lib import colors
  url=os.path.join(MEDIA_ROOT,"pdf\ReporteMensual.pdf")
  c=canvas.Canvas(url,pagesize=letter)

  c.setFont("Helvetica",15)
  c.setFillColorRGB(0,0,0)
  c.drawString(240,750,"VENTAS MENSUAL")

  fe=datetime.now()
  fe=fe.date()
  if fe.month==7:
    c.drawString(290,730,"%s "%("Julio"))
  if fe.month==8:
    c.drawString(290,730,"%s "%("Agosto"))

  total_dia=0
  venta=newventa.objects.filter(fecha__month=fe.month)
  p=700
  for i in venta:
    c.setFont("Helvetica",15)
    c.setFillColorRGB(0.8,0,0)
    c.drawString(120,p,"%s "%("Usuario:"))
    c.drawString(180,p,"%s "%(i.user))
    c.drawString(340,p,"%s "%("Fecha:"))
    c.drawString(390,p,"%s "%(i.fecha))
    p=p-20
    c.line(30,p,580,p)
    p=p-3
    c.line(30,p,580,p)
    p=p-30

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
          pp=750
          c.showPage()
    p=pp-70
    if p<40:
      p=750
      c.showPage()
    c.drawString(380,p+60,"%s "%("TOTAL"))
    c.drawString(490,p+60,"%s "%(i.PrecioTotal))
    total_dia=total_dia+i.PrecioTotal
    c.line(70,p+80,570,p+80)

  c.setFillColorRGB(8,0,0)
  c.drawString(80,p,"%s "%("Total mes : "))
  c.drawString(170,p,"%s "%(total_dia))
  c.save()
  return HttpResponseRedirect("/media/pdf/ReporteMensual.pdf")





@login_required(login_url='/user/login')
def ReporteGeneral(request):
  from reportlab.pdfgen import canvas
  from reportlab.lib.pagesizes import letter,A4
  from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Image,Table,TableStyle,PageBreak #librerias para ejustar el texto
  from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
  from reportlab.lib.enums import TA_JUSTIFY 
  from reportlab.lib import colors
  url=os.path.join(MEDIA_ROOT,"pdf\ReporteMensual.pdf")
  c=canvas.Canvas(url,pagesize=letter)

  c.setFont("Helvetica",15)
  c.setFillColorRGB(0,0,0)
  c.drawString(240,750,"VENTAS MENSUAL")

  fe=datetime.now()
  fe=fe.date()
  if fe.month==7:
    c.drawString(290,730,"%s "%("Julio"))
  if fe.month==8:
    c.drawString(290,730,"%s "%("Agosto"))

  total_dia=0
  venta=newventa.objects.filter(fecha__month=fe.month)
  p=700
  for i in venta:
    c.setFont("Helvetica",15)
    c.setFillColorRGB(0.8,0,0)
    c.drawString(120,p,"%s "%("Usuario:"))
    c.drawString(180,p,"%s "%(i.user))
    c.drawString(340,p,"%s "%("Fecha:"))
    c.drawString(390,p,"%s "%(i.fecha))
    p=p-20
    c.line(30,p,580,p)
    p=p-3
    c.line(30,p,580,p)
    p=p-30

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
          pp=750
          c.showPage()
    p=pp-70
    if p<40:
      p=750
      c.showPage()
    c.drawString(380,p+60,"%s "%("TOTAL"))
    c.drawString(490,p+60,"%s "%(i.PrecioTotal))
    total_dia=total_dia+i.PrecioTotal
    c.line(70,p+80,570,p+80)

  c.setFillColorRGB(8,0,0)
  c.drawString(80,p,"%s "%("Total mes : "))
  c.drawString(170,p,"%s "%(total_dia))
  c.save()
  return HttpResponseRedirect("/media/pdf/ReporteMensual.pdf")