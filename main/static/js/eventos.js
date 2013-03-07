var Eventos = function(){

	that = this;

	this.cargar_calendario = function(data){
		Dajaxice.eventos.cargar_calendario_mensual(Dajax.process, {
			datos: {
				'option': data.currentTarget.id,
				'month': $('#fecha-mensual').data('month'),
				'year': $('#fecha-mensual').data('year')
			}
		});
	}

	this.cerrar_info_evento = function(){
		var info = $('#calendario-info');

		if(info.is(':visible')){

			info.hide('drop', { direction: 'right' }, 200);

			$(document).off('click', '#calendario', that.cerrar_info_evento);
		}
	}

	this.cargar_info_evento = function(data){

		var parent = data.currentTarget.parentElement;

		var info = $('#calendario-info');

		var h3 = $('<h3>').append($(this).data('titulo')); 
		var desde = $('<p>').append('Desde: ' + $(this).data('dia-desde') + 
									', ' + $(this).data('fecha-desde') + 
									' a las ' + $(this).data('hora-desde'));

		var hasta = $('<p>').append('Hasta:  ' + $(this).data('dia-hasta') + 
									', ' + $(this).data('fecha-hasta') + 
									' a las ' + $(this).data('hora-hasta'));

		info.html('');
		info.append(h3);
		info.append(desde);
		info.append(hasta);

		var position = $(parent).position();
		var width = $(parent).width();
		var height = $(parent).height();

		var css = {};
		var clase = '';

		if (parent.parentNode.cellIndex != 6){
			info.attr('class', 'info-right');

			css = {
				top: position.top - info.height()/2 + $('#calendario').scrollTop(),
				left: position.left + width/2
			};
		}

		else{
			info.attr('class', 'info-left');
			
			css = {
				top: position.top - info.height()/2 + $('#calendario').scrollTop(),
				left: position.left  - info.width() + width/2
			};
		}

		info.css(css);

		info.show('drop', { direction: 'right' }, 200);

		data.stopPropagation();

		$(document).on('click', '#calendario', that.cerrar_info_evento);
	}

	$(document).on('click', '#cabecera-eventos a', this.cargar_calendario);

	$(document).on('click', '#calendario table a', this.cargar_info_evento);

}