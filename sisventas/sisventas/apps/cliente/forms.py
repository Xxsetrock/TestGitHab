from models import client
from django import forms# para canbiar el texto de las tablas
from django.forms import ModelForm


class ClienteForm(ModelForm):
	class Meta:
		model = client
