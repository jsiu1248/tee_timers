$(document).ready(function() {
    // Activate the first tab on page load
    $('.nav-tabs a:first').tab('show');
  
    // Switch to the tab that was clicked
    $('.nav-tabs a').on('click', function(e) {
      e.preventDefault();
      $(this).tab('show');
    });
  });