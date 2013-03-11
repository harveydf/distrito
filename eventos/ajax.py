import datetime

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dateutil.relativedelta import relativedelta
from django.template import RequestContext
from django.template.loader import render_to_string
from eventos.templatetags.eventos_tags import show_eventos_mensuales

@dajaxice_register
def cargar_calendario_mensual(request, datos):
	dajax = Dajax()

	option, tipo = datos['option'].split('-')
	month = datos['month']
	year = datos['year']

	date_calendar = datetime.date(year, month, 1)

	if option == 'next':
		if tipo == 'month':
			print date_calendar
			date_calendar += relativedelta(months=+1)
			print date_calendar
		elif tipo == 'year':
			date_calendar += relativedelta(years=+1)
	elif option == 'last':
		if tipo == 'month':
			date_calendar += relativedelta(months=-1)
		elif tipo == 'year':
			date_calendar += relativedelta(years=-1)

	fecha = {'year': date_calendar.year, 'month': date_calendar.month, 'day': None}

	data = show_eventos_mensuales(context=RequestContext(request), fecha=fecha)

	jquery = "$('.sortable').sortable({ \
					connectWith: '.sortable', \
					placeholder: 'ui-state-highlight', \
					receive: eventos.sortable_receive \
			  }).disableSelection();"

	dajax.assign('#calendario', 'innerHTML', render_to_string('eventos_mensuales.jade', data))
	dajax.script(jquery)
	return dajax.json()

@dajaxice_register
def update_evento_dia(request, datos):
	print datos

	# llamada a la vista para actualizar el evento

	dajax = Dajax()
	return dajax.json()
