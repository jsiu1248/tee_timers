/*returns static Nodelist of document elements that match specified group of selectors*/
/* NOTE: that isn't being used. Before, it was a feature that hid the items instead of reordering them.*/
var tabs = document.querySelectorAll(".tabs_wrap_two ul li");
var find = document.querySelectorAll(".find");
var message = document.querySelectorAll(".message");
var play = document.querySelectorAll(".play");
var all = document.querySelectorAll(".item_wrap_two");

/* forEach calls a fuction for each element in the array*/
tabs.forEach((tab) => {
    /*sets up function that will be called whenever the specified event is delivered to the target*/
    tab.addEventListener("click", () => {

        /*for loop that removes the active*/
        // tabs.forEach((tab) => {
        //     tab.classList.remove("active");
        // })
        tab.classList.toggle("active");

        /*returns the value of a specified attribute on the element*/
        var tabval = tab.getAttribute("data-tabs");

        // all.forEach((item) => {
        //     item.style.display = "none";
        // })

        if (tabval == "find") {
            find.forEach((find) => {
                if (getComputedStyle(find).display == "block") {
                    find.style.display = "none";
                }
                else if (getComputedStyle(find).display == "none") {

                    find.style.display = "block";
                }
            })
        }
        else if (tabval == "message") {
            message.forEach((message) => {

                if (getComputedStyle(message).display == "block") {
                    message.style.display = "none";
                }
                else if (getComputedStyle(message).display == "none") {
                    message.style.display = "block";
                    console.log("does it work?")
                }

            })
        }
        else if (tabval == "play") {
            play.forEach((play) => {
                if (getComputedStyle(play).display == "block") {
                    play.style.display = "none";

                }
                else if (getComputedStyle(play).display == "none") {
                    play.style.display = "block";
                }
            })
        }
        else {
            all.forEach((item) => {
                item.style.display = "block";
            })
        }


    })
})