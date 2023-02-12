$(function() {
  console.log("submit-button")
    $( ".submit-container > .btn" ).click(function() {
      console.log("3-4")
      console.log($.fn.jquery)
      $( ".submit-container > .btn" ).addClass( "onclic");
      validate();
    });
  
    function validate() {
      console.log("validate")
      setTimeout(function() {
        console.log("validate-timeout")
        $( ".submit-container > .btn" ).removeClass( "onclic" );
        $( ".submit-container > .btn" ).addClass( "validate");
        callback();
      }, 2250 );
    }
    function callback() {
      console.log("callback")
      setTimeout(function() {
        console.log("callback-timeout")
        $( ".submit-container > .btn" ).removeClass( "validate" );
      }, 2250 );
    }
});