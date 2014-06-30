from django import forms
#from models import Registro

from  django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
class UsuarioForm(forms.Form):
	class Meta:
		form=User
		exclude=["username"]


#class RegistroForm(ModelForm):
   # username= forms.CharField(label="Nombre de usuario", widget=forms.TextInput())
    #email= forms.EmailField(label="Correo Electronico", widget=forms.TextInput())
   # password_one= forms.CharField(label="password", widget=forms.PasswordInput(render_value=False))
   # password_two= forms.CharField(label="Confirmar password", widget=forms.PasswordInput(render_value=False))
#class RegistroForm(ModelForm):
#	contrasena=forms.CharField(widget=forms.PasswordInput)
#	class Meta:
#		model=Registro
#		fields=["correo","usuario"]

#class LoginForm(ModelForm):
#	contrasena=forms.CharField(widget=forms.PasswordInput)
#	class Meta:
#		model=Registro
#		fields=["usuario"]
 

#registro de formulario 
#class SignUpForm(ModelForm):
 #   class Meta:
  #      model = User
   #     fields = ['username', 'password', 'email', 'first_name', 'last_name']
    #    widgets = {
     #       'password': forms.PasswordInput(),
      #  }
