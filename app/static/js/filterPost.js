function filterPostFunction() {
    // Locate the post elements
    let posts = document.querySelectorAll('.post')
    // Locate the search input
    let search_query = document.getElementById("filterBox").value;
    // Loop through the posts
    for (var i = 0; i < posts.length; i++) {
      // If the text is within title...
      if(posts[i].innerText.toLowerCase()
        // ...and the text matches the search query...
        .includes(search_query.toLowerCase())) {
          // ...remove the `.is-hidden` class.
          posts[i].classList.remove("is-hidden");
      } else {
        // Otherwise, add the class.
        posts[i].classList.add("is-hidden");
      }
    }
  }