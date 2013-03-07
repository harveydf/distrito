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
		fecha['day'] = None
	if not fecha['day']:
		dia_inicio = 1
		dia_fin =  calendar.mdays[fecha['month']]
	else:
		dia_inicio = dia_fin = fecha['day']

	fecha_inicio = pytz.timezone(tz).localize(datetime.datetime(fecha['year'], fecha['month'], dia_inicio, 0, 0))
	fecha_fin = pytz.timezone(tz).localize(datetime.datetime(fecha['year'], fecha['month'], dia_fin, 23, 59, 59, 999999))

	return {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}

def get_eventos(request, fechas):
	user_group = request.user.groups.get()

	eventos = Eventos.objects.filter(grupo = user_group, desde__range=(fechas['fecha_inicio'].astimezone(pytz.utc), fechas['fecha_fin'].astimezone(pytz.utc))).order_by('desde')
	return eventos

def crear_calendario_mensual(request, eventos, fechas):
	ftzinfo = fechas['fecha_inicio'].tzinfo
	year = fechas['fecha_inicio'].year
	month = fechas['fecha_inicio'].month

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
				fecha_dia = {'year': year, 'month': month, 'day': day}
				fecha_dia = get_fechas(fecha_dia, ftzinfo.zone)
				clase = 'dia evento'
		
				eventos_dia = eventos.filter(Q(desde__range=(fecha_dia['fecha_inicio'], fecha_dia['fecha_fin'])) | Q(hasta__range=(fecha_dia['fecha_inicio'], fecha_dia['fecha_fin'])) | Q(desde__lte=fecha_dia['fecha_inicio'], hasta__gte=fecha_dia['fecha_fin']), Q(personal_id=None) | Q(personal_id=request.user.id))

			else:
				eventos_dia = None
				clase = 'dia'

			if year == now.year and month == now.month and day == now.day:
					clase = 'dia hoy'

			calendario_eventos[index].append((day, eventos_dia, clase))

	return calendario_eventos

