from django.db import models

# Create your models here.


class Categoria(models.Model):
	nombreCategoria=models.CharField(max_length=200)
	fecha=models.DateField(auto_now=True)
	def __unicode__(self):
		return "%s"%(self.nombreCategoria)

class newproducto(models.Model):
	NombredelProcuto=models.CharField(max_length=200)
	cantidad=models.IntegerField()
	precio=models.DecimalField(max_digits=10,decimal_places=1)
	fecha=models.DateField(auto_now=True)
	cat=models.ManyToManyField(Categoria)
	def __unicode__(self):
		return "%s"%(self.NombredelProcuto)


		
#class  newproducto(models.Model):
#	Nombre = models.CharField(max_length = '50')
#	Descripcion=models.CharField(max_length='50')
#	Precio=models.DecimalField(max_digits=10, decimal_places=2)
#	Cantidad=models.IntegerField()
#	def __unicode__(self):
#		return "%s %s"%(self.Nombre,self.Descripcion)