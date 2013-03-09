var Eventos = function(){

	that = this;

	// Main Calendario
	this.cargar_calendario = function(data){
		Dajaxice.eventos.cargar_calendario_mensual(Dajax.process, {
			datos: {
				'option': data.currentTarget.id,
				'month': $('#fecha-mensual').data('month'),
				'year': $('#fecha-mensual').data('year')
			}
		});
	}

	// Modal info evento functions
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

		if (parent.parentNode.cellIndex != 6){
			info.attr('class', 'info-right');

			var css = {
				top: position.top - info.height()/2 + $('#calendario').scrollTop(),
				left: position.left + width/2
			};
		}

		else{
			info.attr('class', 'info-left');
			
			var css = {
				top: position.top - info.height()/2 + $('#calendario').scrollTop(),
				left: position.left  - info.width() + width/2
			};
		}

		info.css(css);

		info.show('drop', { direction: 'right' }, 200);

		data.stopPropagation();

		$(document).on('click', '#calendario', that.cerrar_info_evento);
	}

	$.datepicker.setDefaults({
		inline: true,
		nextText: '&#59238;',
		prevText: '&#59237;',
		showOtherMonths: true,
		dateFormat: 'd MM yy',
		dayNamesMin: $.datepicker.regional[ "es" ].dayNamesShort,
		monthNames: $.datepicker.regional[ "es" ].monthNames,
		firstDay: 0,
		constrainInput: true,
	});

	// Datepicker functions
	this.set_datepicker = function(){
		$('#id_desde').datepicker({
			onClose: function( selectedDate ) {
		        		$( "#id_hasta" ).datepicker( "option", "minDate", selectedDate );
					},
		});

		$('#id_hasta').datepicker({
			onClose: function( selectedDate ) {
		        		$( "#id_desde" ).datepicker( "option", "maxDate", selectedDate );
					},
		});
	}

	this.set_datepicker();

	// Sortable functions
	this.actualizar_dataset = function(element) {
		var fechas = [];
		var evento = $('a[data-titulo="'+ element.data('titulo') +'"]');
		var data_mes = $('#fecha-mensual').data();

		evento.each(function() {
			fechas.push($(this).parents('.dia').data('dia'));
		});


		var date_desde = new Date(data_mes.year, data_mes.month-1, $(fechas).first()[0]);
		var date_hasta = new Date(data_mes.year, data_mes.month-1, $(fechas).last()[0]);

		evento.each(function() {
			$(this).data('fecha-desde', $(fechas).first()[0]);
			$(this).data('fecha-hasta', $(fechas).last()[0]);
			$(this).data('dia-desde', $.datepicker.regional[ "es" ].dayNamesShort[date_desde.getDay()])
			$(this).data('dia-hasta', $.datepicker.regional[ "es" ].dayNamesShort[date_hasta.getDay()])
		});
	}

	this.cambiar_clase = function() {
		$('.dia ul').each(function(){
			var div = $(this).parents('div');

			if($(this).find('li').length == 0){
				div.removeClass('evento');
			}
			else{
				if(!div.hasClass('hoy')) {
					div.addClass('evento');
				}
			}
		});
	}

	this.sortable_receive = function(event, ui) {
		var a = ui.item.find('a');
		var dia = parseInt($(this).parents('div').data('dia'));
		var ul = $('.dia[data-dia="'+ (dia + 1) +'"] ul');
		
		$('a[data-titulo="'+ a.data('titulo') +'"]').parents('li').not(ui.item).each(function(){
			ul.append(this);
			dia = parseInt($(this).parents('div').data('dia'));
			ul = $('.dia[data-dia="'+ (dia + 1) +'"] ul');
		});

		that.actualizar_dataset(a);

		that.cambiar_clase();
	}

	$('.sortable').sortable({
		connectWith: ".sortable", 
		placeholder: "ui-state-highlight",
		receive: this.sortable_receive
	}).disableSelection();

	$(document).on('click', '#cabecera-eventos a', this.cargar_calendario);

	$(document).on('click', '#calendario table a', this.cargar_info_evento);

	// $(document).on('dblclick', '.dia', this.cargar_crear_evento);


}