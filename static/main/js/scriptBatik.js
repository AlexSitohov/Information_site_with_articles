"use strict"

let body = document.querySelector("body");
let popup = document.querySelector(".popup");
let popupForm = document.querySelector(".popup__edit");
let popupOpen = document.querySelectorAll(".popup-open");
let popupClose = document.querySelector(".popup__close");

popupOpen.forEach(function (item) {
    item.addEventListener("click", function (event) {
        if (event.target.classList.contains("popup-open")) {
            popup.classList.add("popup_active");
            body.classList.add("body_lock");
        }
    });
});

popup.addEventListener("click", function (event) {
    if (event.target.classList.contains("popup") || event.target.classList.contains("popup__close")) {
        popup.classList.remove("popup_active");
        setTimeout(function () {
            body.classList.remove("body_lock");
        }, 300);
    }
});

console.log(body.offsetWidth + " " + body.clientWidth);