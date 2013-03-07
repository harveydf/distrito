from django import template
from eventos.views import get_eventos, get_fechas, crear_calendario_mensual

register = template.Library()

@register.inclusion_tag('eventos_mensuales.jade', takes_context=True)
def show_eventos_mensuales(context, fecha=None):
	request = context['request']
	tz = context['TIME_ZONE']

	fechas = get_fechas(fecha, tz)
	eventos = get_eventos(request, fechas)
	calendario = crear_calendario_mensual(request, eventos, fechas)
	
	return {'calendario': calendario, 'fecha': fechas}