from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from forms import new_ventaForm,buscarCliente
from models import newventa
from django.contrib.auth.decorators import login_required, permission_required
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sisventas.settings import MEDIA_ROOT
from sisventas.apps.cliente.models import client
# Create your views here.
import csv
import  json
from django.http import HttpResponse
@login_required(login_url='/user/login')
def new_venta(request):
	if request.method=="POST":
		form=new_ventaForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/private/')
	else:
		form=new_ventaForm()
	buscar=buscarCliente()
	return render_to_response('registrar_venta.html',{'new_venta':form,'buscar':buscar},context_instance = RequestContext(request))



def reporte(request):
	from reportlab.pdfgen import canvas
	from reportlab.lib.pagesizes import letter
	from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer #librerias para ejustar el texto
	from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
	from reportlab.lib.enums import TA_JUSTIFY
	url=os.path.join(MEDIA_ROOT,"pdf\proyecto.pdf")
	c=canvas.Canvas(url,pagesize=letter)
	c.line(40,700,500,700)
	c.line(500,700,500,680)
	c.line(500,680,40,680)
	c.line(40,680,40,700)
	c.save()
	return HttpResponseRedirect("/media/pdf/proyecto.pdf")
def buscar(request):
	if request.method=='POST':
		form=buscarCliente(request.POST)
		print form
		cliente=client.objects.filter(ci=request.POST["buscarcliente"])
		if len(cliente)==0:
			return  HttpResponse(json.dumps({"idCli":-1}),content_type="application/json")
		return HttpResponse(json.dumps({"nombre":cliente[0].nombre,"idCli":cliente[0].id}),content_type="application/json")