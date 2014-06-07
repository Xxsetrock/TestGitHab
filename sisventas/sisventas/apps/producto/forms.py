from models import newproducto,Categoria

from django.forms import ModelForm


class new_productoForm(ModelForm):
	class Meta:
		model = newproducto

class new_categoriaForm(ModelForm):
	class Meta:
		model = Categoria

