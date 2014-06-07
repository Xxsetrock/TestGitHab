from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from forms import ClienteForm
from django.contrib.auth.decorators import login_required, permission_required
from models import client

# Create your views here.

@login_required(login_url='/user/login')
def new_cliente(request):
	if request.method=="POST":
		form=ClienteForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/new_venta/')
	else:
		form=ClienteForm()
	return render_to_response('cliente.html',{'cliente':form},context_instance = RequestContext(request))

@login_required(login_url='/user/login')
def listar_cliente(request):
	producto=client.objects.all()
	return render_to_response('Eliminar_modificar_cliente.html',{'eliminar':producto},context_instance=RequestContext(request))
@login_required(login_url='/user/login')
def eliminar_cliente(request,id):
	dato=get_object_or_404(client,pk=id)
	dato.delete()
	return render_to_response('eliminado.html',{'dato':dato},context_instance=RequestContext(request))
@login_required(login_url='/user/login')
def modificar_cliente(request,id):
	producto=get_object_or_404(client,pk=id)
	if request.method=='POST':
		formulario=ClienteForm(request.POST,instance=producto)
		formulario.save()
		return HttpResponseRedirect('/')
	else:
		formulario=ClienteForm(instance=producto)
	return render_to_response('modificar_cliente.html',{'formulario':formulario},context_instance=RequestContext(request))