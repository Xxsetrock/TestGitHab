from django.db import models
from sisventas.apps.cliente.models import client
from sisventas.apps.producto.models import newproducto
from django.contrib.auth.models import User
# Create your models here.
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sisventas.settings import MEDIA_ROOT

class  newventa(models.Model):
	user=models.ForeignKey(User)
	cliente=models.ForeignKey(client)
	producto = models.ManyToManyField(newproducto)
	PrecioTotal=models.DecimalField(max_digits=20, decimal_places=5)
	CantidadTotal=models.IntegerField()
	fecha=models.DateField(auto_now=True)
	def __unicode__(self):
		return "%s %s"%(self.cliente,self.producto)

class detalle(models.Model):
	venta=models.ForeignKey(newventa)
	producto=models.ForeignKey(newproducto)
	cantidad = models.IntegerField()
	precio=models.DecimalField(max_digits=20, decimal_places=5)
	activo=models.IntegerField()
	def __unicode__(self):
		return "%s %s"%(self.cantidad,self.precio)


class factura(models.Model):
	cliente=models.ForeignKey(client)
	user=models.ForeignKey(User)
	codigo= models.CharField(max_length=200)
	venta=models.ForeignKey(newventa)
	def __unicode__(self):
		return "%s %s"%(self.codigo,self.cliente)


		