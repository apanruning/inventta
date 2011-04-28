    (function( $ ) {

    $( ".ui-autocomplete-input" ).live( "autocompleteopen", function() {
        var autocomplete = $( this ).data( "autocomplete" ),
            menu = autocomplete.menu;
        menu.activate( $.Event({ type: "mouseenter" }), menu.element.children().first() );
    });

    }( jQuery ));
    $(document).ready(function(){
        var hash = window.location.hash;
        if (hash){
            $(window).scrollTop($(hash).offset().top-55)
        }
        
		function split( val ) {
			return val.split( /,\s*/ );
		}
		function extractLast( term ) {
			return split( term ).pop();
		}

        $('.control').click(function(){
            target = $(this).attr('href');
            $(target).toggle('blind', 300);
            if (target === '#idea-form'){
                window.setTimeout(function(){
                    $('#id_description').focus();
                    $('#idea-form').bind( "keydown", function(event) {
			                if ( event.keyCode === $.ui.keyCode.ESCAPE) {
				                $('#idea-form').hide('blind', 300)
				                               .unbind('keydown');
			                }
		                });

                },400)

            }
            return false;
            
        });
        $('.edit').click(function(){
            url = $(this).attr('href');
            $.getJSON(url, function(data){
                $('#idea-form').attr('action', url);
                form_fields = $('#idea-form :input');
                for (x in data) {
                    $('#id_'+x).val(data[x]);
                }
            });
            $('#new-idea').click();
            return false;
        })
        $('#login-form').submit(function(){
            data = $(this).serializeArray();
            action = $(this).attr('action');
            $.post(action, data, function(data, st, request){
                if (st === 'success'){
                    window.location=data['next'];

                };

            });
            return false;
        })
		$( "#id_tags" )
			.bind( "keydown", function( event ) {
			// don't navigate away from the field on tab when selecting an item
				if ( event.keyCode === $.ui.keyCode.TAB &&
						$( this ).data( "autocomplete" ).menu.active ) {
					event.preventDefault();
				}
			})
			.autocomplete({
				source: function( request, response ) {
					$.getJSON( "/tags/", {
						tag_name: extractLast( request.term )
					}, response );
				},
				search: function() {
					var term = extractLast( this.value );
					if ( term.length < 2 ) {
						return false;
					}
				},
				focus: function() {
					return false;
				},
				select: function( event, ui ) {
					var terms = split( this.value );
					terms.pop();
					terms.push( ui.item.value );
					terms.push( "" );
					this.value = terms.join( ", " );
					return false;
				}
			});
            window.setTimeout(function(){
                $('#messages .control').click()
                }, 1000);
    })

