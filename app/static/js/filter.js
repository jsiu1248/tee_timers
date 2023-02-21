function filterFunction() {
    // Locate the username elements
    let users = document.querySelectorAll('.usernameList')
    // Locate the search input
    let search_query = document.getElementById("filterBox").value;
    // Loop through the users
    for (var i = 0; i < users.length; i++) {
      // If the text is within usernames...
      if(users[i].innerText.toLowerCase()
        // ...and the text matches the search query...
        .includes(search_query.toLowerCase())) {
          // ...remove the `.is-hidden` class.
          users[i].classList.remove("is-hidden");
      } else {
        // Otherwise, add the class.
        users[i].classList.add("is-hidden");
      }
    }
  }