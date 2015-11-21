$(document).ready(function(){

		$("#calculate").click(function(){
		    $.getJSON($SCRIPT_ROOT + '/add',
		        {
                    a: $('input[name="a"]').val(),
                    b: $('input[name="b"]').val(),
                    now: new Date().getTime()
                },
            function(data)
                {
                    $('#result').text(data.result);
                }
                  )
		})

	})