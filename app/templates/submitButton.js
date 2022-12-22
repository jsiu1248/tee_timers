$(function() {
    $( "#submit" ).click(function() {
      $( "#submit" ).addClass( "onclic", 250, validate);
    });
  
    function validate() {
      setTimeout(function() {
        $( "#submit" ).removeClass( "onclic" );
        $( "#submit" ).addClass( "validate", 450, callback );
      }, 2250 );
    }
      function callback() {
        setTimeout(function() {
          $( "#submit" ).removeClass( "validate" );
        }, 1250 );
      }
    });