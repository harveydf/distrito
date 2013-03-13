Eventos = ->

	_this = @
	_ultimo_evento_creado = ''

	###
	Main Calendario
	###
	@cargar_calendario = (data) ->
		Dajaxice.eventos.cargar_calendario_mensual(Dajax.process, {
			datos: {
				'option': data.currentTarget.id
				'month': $('#fecha-mensual').data 'month'
				'year': $('#fecha-mensual').data 'year'
			}
		})
		return

	### 
	Modal info evento functions 
	###
	@cerrar_info_evento = (data) ->
		info = $(data.data.popup)
		
		if info.is ':visible'
			info.hide('drop', {direction: 'right'}, 200)
			$(document).off 'click', '#calendario', _this.cerrar_info_evento

		return


	@evento_popup = (element, popup) ->
		parent = $(element).parent()

		info = $(popup)

		position = $(parent).position()
		width = $(parent).width()
		height = $(parent).height()

		if $(parent).parents('td')[0].cellIndex isnt 6
			info.attr 'class', 'info-right'

			css = {
				top: position.top - info.height() / 2 + $('#calendario').scrollTop()
				left: position.left + width/2
			}
		else
			info.attr 'class', 'info-left'

			css = {
				top: position.top - info.height()/2 + $('#calendario').scrollTop(),
				left: position.left  - info.width() + width/2
			}

		info.css(css)

		info.show('drop', {direction: 'right'}, 200)

		return

	@cargar_info_evento = (data) ->
		parent = data.currentTarget.parentElement

		info = $('#calendario-info')

		h3 = $('<h3>').append $(this).data 'titulo'
		desde = $('<p>').append "Desde: #{$(this).data('dia-desde')}, #{$(this).data('fecha-desde')} a las #{$(this).data('hora-desde')}"

		hasta = $('<p>').append "Hasta: #{$(this).data('dia-hasta')}, #{$(this).data('fecha-hasta')} a las #{$(this).data('hora-hasta')}"

		info.html ''
		info.append h3
		info.append desde
		info.append hasta

		_this.evento_popup(data.currentTarget, '#calendario-info')

		data.stopPropagation()

		$(document).on('click', '#calendario', {'popup': '#calendario-info'}, _this.cerrar_info_evento);

		return

	@form_crear_evento = (data) ->
		div_dia = $(data.currentTarget)
		fecha = div_dia.data 'dia'
		dia_desde = $.datepicker.regional['es'].dayNamesShort[div_dia.parents('td')[0].cellIndex]

		li = $('<li>')
		div = $('<div>')
		a = $("<a data-titulo='Nuevo Evento' data-dia-desde=\"" + dia_desde + "\" data-hora-desde='12:00' data-fecha-desde=\"" + fecha + "\" data-dia-hasta=\"" + dia_desde + "\" data-hora-hasta='13:00' data-fecha-hasta=\"" + fecha + "\">")

		a.html 'Nuevo Evento'

		div.append a
		li.append div
		div_dia.find('ul').append li

		_this.cambiar_clase()

		fecha_mensual = $('#fecha-mensual').data()
		month_name = $.datepicker.regional['es'].monthNames[fecha_mensual.month - 1 ]

		$('[name="titulo"]').val 'Nuevo Evento'
		$('[name="fecha_desde"]').datepicker 'setDate', "#{fecha} #{month_name} #{fecha_mensual.year}"
		$('[name="fecha_hasta"]').datepicker 'setDate', "#{fecha} #{month_name} #{fecha_mensual.year}"
		$('[name="hora_desde"]').val '12:00'
		$('[name="hora_hasta"]').val '13:00'

		_this.evento_popup(a[0], '#agregar-evento')

		_ultimo_evento_creado = li

		$('#cancelar-agregar-evento').on 'click', ->
			$('#agregar-evento').hide('drop', { direction: 'right' }, 200)
			_ultimo_evento_creado.remove()
			_this.cambiar_clase()
			return

		$('#aceptar-agregar-evento').on 'click', ->
			Dajaxice.eventos.nuevo_evento(_this.enviar_actualizar_eventos, {
				datos: {
					'titulo': $('[name="titulo"]').val()
					'fecha_desde': $('[name="fecha_desde"]').datepicker('getDate')
				}
			})
			return

		return

	$.datepicker.setDefaults({
		inline: true
		nextText: '&#59238'
		prevText: '&#59237;'
		showOtherMonths: true
		dateFormat: 'd MM yy'
		dayNamesMin: $.datepicker.regional[ "es" ].dayNamesShort
		monthNames: $.datepicker.regional[ "es" ].monthNames
		firstDay: 0
		constrainInput: true
	})

	@set_datepicker = ->
		$('[name="fecha_desde"]').datepicker({
			onClose: (selectedDate) ->
				$('[name="fecha_hasta"]').datepicker('option', 'minDate', selectedDate)
				return
		})

		$('[name="fecha_hasta"]').datepicker({
			onClose: (selectedDate) ->
				$('[name="fecha_desde"]').datepicker('option', 'maxDate', selectedDate)
				return
		})

		return

	@set_datepicker()

	###
	Sortable functions
	###

	@enviar_actualizar_eventos = ->
		###
		Enviar mensajes de actualizar calendario
		###
		return

	@actualizar_dataset = (element) ->
		fechas = []
		evento = $("a[data-titulo=\"" + element.data("titulo") + "\"]")
		data_mes = $('#fecha-mensual').data()

		evento.each( -> 
			fechas.push($(@).parents('.dia').data 'dia')
			return
		)

		date_desde = new Date(data_mes.year, data_mes.month-1, $(fechas).first()[0])
		date_hasta = new Date(data_mes.year, data_mes.month-1, $(fechas).last()[0])

		evento.each( ->
			$(@).data('fecha-desde', $(fechas).first()[0])
			$(@).data('fecha-hasta', $(fechas).last()[0]);
			$(@).data('dia-desde', $.datepicker.regional['es'].dayNamesShort[date_desde.getDay()])
			$(@).data('dia-hasta', $.datepicker.regional['es'].dayNamesShort[date_hasta.getDay()])
			return
		)

		data_ajax = {
			datos: {
				'titulo': evento.first().data('titulo')
				'dia_desde': evento.first().data('fecha-desde')
				'dia_hasta': evento.first().data('fecha-hasta')
				'hora_desde': evento.first().data('hora-desde')
				'hora_hasta': evento.first().data('hora-hasta')
				'month': data_mes.month
				'year': data_mes.year	
			}
		}

		Dajaxice.eventos.update_evento_dia(_this.enviar_actualizar_eventos, data_ajax)

		return

	@cambiar_clase = ->
		$('.dia ul').each(->
			div = $(@).parents 'div'

			if $(@).find('li').length is 0
				div.removeClass 'evento'

			else
				if not div.hasClass 'hoy'
					div.addClass 'evento'
				
			return	
		)

		return

	@sortable_receive = (event, ui) ->
		a = ui.item.find 'a'
		dia = parseInt($(@).parents('div').data('dia'))
		ul = $(".dia[data-dia=\"" + (dia + 1) + "\"] ul")

		$("a[data-titulo=\"" + a.data("titulo") + "\"]").parents('li').not(ui.item).each(->
			ul.append(@)
			dia = parseInt($(@).parents('div').data('dia'))
			ul = $(".dia[data-dia=\"" + (dia + 1) + "\"] ul")
			return
		)

		_this.actualizar_dataset a
		_this.cambiar_clase()

		return

	$('.sortable').sortable({
		connectWith: ".sortable"
		placeholder: "ui-state-highlight"
		receive: _this.sortable_receive
	})

	$(document).on 'click', '#cabecera-eventos a', @.cargar_calendario
	$(document).on 'click', '#calendario table a', @.cargar_info_evento
	$(document).on 'dblclick', '.dia', @.form_crear_evento

	return

