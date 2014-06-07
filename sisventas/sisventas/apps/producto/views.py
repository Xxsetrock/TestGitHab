from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from forms import new_productoForm,new_categoriaForm
from models import newproducto,Categoria

from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

@login_required(login_url='/user/login')
def new_producto(request):
	if request.method=="POST":
		form=new_productoForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/administrador/')
	else:
		form=new_productoForm()
	return render_to_response('new_producto.html',{'new_producto':form},context_instance = RequestContext(request))

@login_required(login_url='/user/login')
def new_categoria(request):
	if request.method=="POST":
		form=new_categoriaForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/administrador/')
	else:
		form=new_categoriaForm()
	return render_to_response('new_categoria.html',{'new_categoria':form},context_instance = RequestContext(request))


@login_required(login_url='/user/login')
def listar_producto(request):
	producto=newproducto.objects.all()
	return render_to_response('eliminar_producto.html',{'eliminar':producto},context_instance=RequestContext(request))

@login_required(login_url='/user/login')
def eliminar(request,id):
	dato=get_object_or_404(newproducto,pk=id)
	dato.delete()
	return render_to_response('eliminado.html',{'dato':dato},context_instance=RequestContext(request))

@login_required(login_url='/user/login')
def modificar_producto(request,id):
	producto=get_object_or_404(newproducto,pk=id)
	if request.method=='POST':
		formulario=new_productoForm(request.POST,instance=producto)
		formulario.save()
		return HttpResponseRedirect('/')
	else:
		formulario=new_productoForm(instance=producto)
	return render_to_response('modificar_cliente.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/user/login')
def listadodeTodo(request):
	lista=newproducto.objects.all()
	categorialista=Categoria.objects.all()
	return render_to_response('listar_productos.html',{'lista':lista,'cate':categorialista},RequestContext(request))	

@login_required(login_url='/user/login')
def ListadoPorCategoria(request,categoria):
	lista=list(newproducto.objects.filter(cat__id=categoria))
	categorialista=Categoria.objects.all()
	return render_to_response("listar_productos.html",{"lista":lista,"cate":categorialista},RequestContext(request))

@login_required(login_url='/user/login')
def borrarRel(request,idp,idc):
	pro=newproducto.objects.get(id=idp)
	cat=Categoria.objects.get(id=idc)
	pro.cat.remove(cat)
	lista=newproducto.objects.all()
	categorialista=Categoria.objects.all()
	pro.save()
	return render_to_response("listar_productos.html",{"lista":lista,"cate":categorialista},RequestContext(request))