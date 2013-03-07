from django.db import models
from django.contrib.auth.models import User, Group

class Eventos(models.Model):
	REPETIR_CHOICES = (
		('NL', 'Ninguno'),
		('DY', 'Diario'),
		('WK', 'Semanal'),
		('MT', 'Mensual'),
		('YR', 'Anual'),
	)
	titulo = models.CharField(max_length=255)
	desde = models.DateTimeField()
	hasta = models.DateTimeField()
	repeat = models.CharField(max_length=2, choices=REPETIR_CHOICES, default='NL')
	personal = models.ForeignKey(User, blank=True, null=True)
	grupo = models.ManyToManyField(Group)

	def __unicode__(self):
		return self.titulo