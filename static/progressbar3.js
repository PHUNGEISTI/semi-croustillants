$(document).ready(function() {

	$('#start').click(function() {

				var timerId, percent;

		  // reset progress bar
		  percent = 0;
		  
		  $('progress').css('width', '0px');


		  timerId = setInterval(function() {

			// increment progress bar
			percent += 1;
			$('progress').css('width', percent + '%');
			$('#progressbar').html(percent + '%');


			// complete
			if (percent >= 100) {
			  clearInterval(timerId);
			  $('progress').attr('disabled', false);
			  $('progress').removeClass('progress-bar-striped active');
			  $('progress').html('calculs terminés');

			}

		  }, 200);
	});

});

