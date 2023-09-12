$(document).ready(function () {
    $.getScript("/codinglab.js", function () {});
});

function openMenu(evt, cityName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("tabs");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(
            " menuselected",
            ""
        );
    }
    document.getElementById(cityName).style.display = "block";
    // console.log(evt.currentTarget)
    evt.currentTarget.className += " menuselected";
    var linkName = evt.currentTarget.querySelector(".link_name").textContent;
    document.getElementById("title").textContent = linkName;
}

function msgBox(text) {
    alert(text);
}

// eel.getTitle()(function (callback) {
//     // console.log(callback);
//     document.title = callback;
// });
