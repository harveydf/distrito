$(document).on('ready', main);

function main(){

	setInitial();
	$(window).on('resize', resizeWindow);

	$('nav ul li').not(':nth-last-child(2), :last-child').on('click','a', selectMenu);
}

function setInitial(){
	var height = Math.round($(window).height() / 16);
	$('#main').height(height+'em');

	$('#main section').waypoint(function(direction){
		if(direction === 'right'){
			$('.selected').removeClass('selected');
			$('a[href="#' + this.id + '"]').parent().addClass('selected');
		}
	},
	{
		offset: '50%', 
		horizontal: true
	});

	$('#main section').waypoint(function(direction){
		if(direction === 'left'){
			$('.selected').removeClass('selected');
			$('a[href="#' + this.id + '"]').parent().addClass('selected');
		}
	},
	{
		horizontal: true
	});
}

function selectMenu(data){

	$.waypoints('disable');

	$('.selected').removeClass('selected');

	var li = data.delegateTarget;
	$(li).addClass('selected');

	var headerWidth = parseInt($('#main').css('margin-left'));
	var section = data.currentTarget.hash;
	var sectionPositionLeft = $(section).position().left - headerWidth;
	$('html, body').animate({
		scrollLeft: sectionPositionLeft
	}, function(){
		$.waypoints('enable');
	});

}

function resizeWindow() {
	$('#main').height($(window).height());
}