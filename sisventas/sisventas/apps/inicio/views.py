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
#from forms import RegistroForm

def index(request):
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

