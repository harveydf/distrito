import datetime, pytz, calendar

from django.db.models import Q
from django.utils import timezone
from eventos.models import Eventos, Group

def get_fechas(fecha, tz):
	if not fecha:
		fecha = {}
		now = datetime.datetime.now()
		fecha['year'] = now.year
		fecha['month'] = now.month
	
	if not 'day_from' in fecha:
		dia_inicio = 1
		dia_fin =  calendar.mdays[fecha['month']]
	
	else:
		dia_inicio = fecha['day_from']
		dia_fin = dia_inicio if not 'day_to' in fecha else fecha['day_to']

	if not 'hour_from' in fecha:
		hour_from = min_from = 0
	
	else:
		hour_from = fecha['hour_from']
		min_from = 0 if not 'min_from' in fecha else fecha['min_from']

	if not 'hour_to' in fecha:
		hour_to = 23
		min_to = 59

	else:
		hour_to = fecha['hour_to']
		min_to = 59 if not 'min_to' in fecha else fecha['min_to']



	fecha_inicio = pytz.timezone(tz).localize(datetime.datetime(fecha['year'], fecha['month'], dia_inicio, hour_from, min_from))
	fecha_fin = pytz.timezone(tz).localize(datetime.datetime(fecha['year'], fecha['month'], dia_fin, hour_to, min_to, 59, 999999))

	return {'inicio': fecha_inicio, 'fin': fecha_fin}

def get_eventos(request, fechas):
	user_group = request.user.groups.get()

	eventos = Eventos.objects.filter(grupo = user_group, desde__range=(fechas['inicio'].astimezone(pytz.utc), fechas['fin'].astimezone(pytz.utc))).order_by('desde')
	return eventos

def crear_calendario_mensual(request, eventos, fechas):
	ftzinfo = fechas['inicio'].tzinfo
	year = fechas['inicio'].year
	month = fechas['inicio'].month

	calendario_eventos = []
	calendario = calendar.Calendar(calendar.SUNDAY).monthdayscalendar(year, month)
	now = datetime.datetime.now()

	for index, week in enumerate(calendario):
		calendario_eventos.append([])
		for day in week:
			if day == 0:
				day = ''
				eventos_dia = None
				clase = 'empty'
			
			elif any(d.desde.astimezone(ftzinfo).day <= day and d.hasta.astimezone(ftzinfo).day >= day for d in eventos):
				fecha_dia = {'year': year, 'month': month, 'day_from': day}
				fecha_dia = get_fechas(fecha_dia, ftzinfo.zone)
				clase = 'dia evento'
		
				eventos_dia = eventos.filter(Q(desde__range=(fecha_dia['inicio'], fecha_dia['fin'])) | Q(hasta__range=(fecha_dia['inicio'], fecha_dia['fin'])) | Q(desde__lte=fecha_dia['inicio'], hasta__gte=fecha_dia['fin']), Q(personal_id=None) | Q(personal_id=request.user.id))

			else:
				eventos_dia = None
				clase = 'dia'

			if year == now.year and month == now.month and day == now.day:
					clase = 'dia hoy'

			calendario_eventos[index].append((day, eventos_dia, clase))

	return calendario_eventos

def update_dia(request, datos):

	tz = request.META['TZ']

	hora_desde, min_desde = datos['hora_desde'].split(':')
	hora_hasta, min_hasta = datos['hora_hasta'].split(':')

	date = {'year': datos['year'], 'month': datos['month'], 'day_from': datos['dia_desde'], 'day_to': datos['dia_hasta'], 'hour_from': int(hora_desde), 'min_from': int(min_desde), 'hour_to': int(hora_hasta), 'min_to': int(min_hasta)}

	fecha = get_fechas(date, tz)

	eventos = Eventos.objects.get(titulo=datos['titulo'])
	eventos.desde = fecha['inicio']
	eventos.hasta = fecha['fin']

	eventos.save()

def agregar_nuevo_evento(request, datos):

	print datos
