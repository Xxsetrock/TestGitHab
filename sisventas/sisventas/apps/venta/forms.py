from models import newventa
from django.forms import ModelForm
from  django import forms
class buscarCliente(forms.Form):
	buscarcliente=forms.CharField(max_length=200)
class new_ventaForm(ModelForm):
	idCliente=forms.HiddenInput()
	class Meta:
		model = newventa
		#exclude=["cliente"]