$(document).ready(function() {

	$('#myButton').click(function() {

	/*	var formData = new FormData($('form')[0]);

		$.ajax({
			xhr : function() {
				var xhr = new window.XMLHttpRequest();

				xhr.upload.addEventListener('progress', function(e) {

					if (e.lengthComputable) {

						console.log('Bytes Loaded: ' + e.loaded);
						console.log('Total Size: ' + e.total);
						console.log('Percentage Uploaded: ' + (e.loaded / e.total))

						var percent = Math.round((e.loaded / e.total) * 100);

						$('#load').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');

					}

				});

				return xhr;
			},
			type : 'POST',
			url : '/comparaison',
			data : formData,
			processData : false,
			contentType : false,
			success : function() {
				alert('File uploaded!');
			} 
			
			
		});*/
				var timerId, percent;

		  // reset progress bar
		  percent = 0;
		  
		  $('#load').css('width', '0px');


		  timerId = setInterval(function() {

			// increment progress bar
			percent += 0.85;
			roun=Math.round(percent);
			$('#load').css('width', percent + '%');
			$('#load').html(roun + '%');


			// complete
			if (percent >= 100) {
			  clearInterval(timerId);
			  $('#pay').attr('disabled', false);
			  $('#load').removeClass('progress-bar-striped active');
			  $('#load').html('calculs terminés');

			}

		  }, 200);
	});

});

/*$(document).ready(function() {
$('#myButton').click(function() {

  var timerId, percent;

  // reset progress bar
  percent = 0;
  $('#myButton').attr('disabled', true);
  $('#load').css('width', '0px');
  $('#load').addClass('progress-bar-striped active');


  timerId = setInterval(function() {

    // increment progress bar
    percent += 5;
    $('#load').css('width', percent + '%');
    $('#load').html(percent + '%');


    // complete
    if (percent >= 100) {
      clearInterval(timerId);
      $('#myButton').attr('disabled', false);
      $('#load').removeClass('progress-bar-striped active');
      $('#load').html('calculs fini');

      // do more ...

    }

  }, 200);


});
});
*/