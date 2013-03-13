eventos = ''


main = ->
	setInitial()
	$(window).on 'resize', resizeWindow

	$('nav ul li').not(':nth-last-child(2), :last-child').on('click','a', selectMenu) 
	return

setInitial = ->
	height = Math.round $(window).height() / 16
	
	$('#main').height height + 'em'

	$('#main section').waypoint ((direction) -> 
		if direction is 'right'
			$('.selected').removeClass 'selected'
			$('a[href="#' + @id + '"]').parent().addClass 'selected'
		return
		),
		offset: '50%'
		horizontal: true

	$('#main section').waypoint ((direction) -> 
		if direction is 'left'
			$('.selected').removeClass 'selected'
			$('a[href="#' + @id + '"]').parent().addClass 'selected'
		return
		),
		horizontal: true

	eventos = new Eventos()

	return

selectMenu = (data) ->
	$.waypoints 'disable'

	$('.selected').removeClass 'selected'

	li = data.delegateTarget
	$(li).addClass 'selected'

	headerWidth = parseInt $('#main').css 'margin-left'
	section = data.currentTarget.hash
	sectionPositionLeft = $(section).position().left - headerWidth
	$('html, body').animate({
		scrollLeft: sectionPositionLeft
	},
	->
		$.waypoints 'enable'
		return
	)
	return

resizeWindow = ->
	$('#main').height $(window).height()
	return
	
$(document).on 'ready', main