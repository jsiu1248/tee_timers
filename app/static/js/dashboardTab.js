$(document).ready(function() {
  // Get the initial tab from the URL hash (e.g. #total). The hash value will be used to determine which is active initally.
  var initialTab = window.location.hash;

  // Activate the initial tab. Finds the href that matches the hash value. tab('show') activates that tab.
  $('.nav-tabs a[href="' + initialTab + '"]').tab('show');

  // Switch to the tab that was clicked. 
  $('.nav-tabs a').on('click', function(e) {
    // Update the title variable to the text of the clicked tab
    title = $(this).text().trim();

    // Update the URL hash to reflect the current tab.
    window.location.hash = $(this).attr('href');
  });
});