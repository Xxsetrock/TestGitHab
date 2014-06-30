from models import newventa,detalle
from django.forms import ModelForm
from  django import forms
class buscarCliente(forms.Form):
	buscarcliente=forms.CharField(max_length=200)
class new_ventaForm(ModelForm):
	idCliente=forms.HiddenInput()
	#User=forms.HiddenInput()
	class Meta:
		#exclude=["user"]
		model = newventa
		



class detalleForm(ModelForm):
	#idCliente=forms.HiddenInput()
	class Meta:
		model = detalle