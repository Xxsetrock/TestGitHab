from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 
# Create your models here.


class  client(models.Model):
	nombre = models.CharField(max_length = '50')
	apellido = models.CharField(max_length = '50')
	ci = models.CharField(max_length = '12', unique='true')
	direccion = models.CharField(max_length = '50')
	telefono = models.CharField(max_length = '15')
	fecha=models.DateTimeField(auto_now=True)
	#usuario=models.User()
	def __unicode__(self):
		return "%s %s"%(self.nombre,self.ci)