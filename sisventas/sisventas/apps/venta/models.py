from django.db import models
from sisventas.apps.cliente.models import client
from sisventas.apps.producto.models import newproducto
# Create your models here.
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sisventas.settings import MEDIA_ROOT

class  newventa(models.Model):
	cliente=models.ForeignKey(client)
	producto = models.ManyToManyField(newproducto)
	Precio=models.DecimalField(max_digits=10, decimal_places=2)
	Cantidad=models.IntegerField()
	def __unicode__(self):
		return "%s %s"%(self.cliente,self.producto)



		