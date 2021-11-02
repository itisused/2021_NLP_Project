"use strict";

const button = document.querySelector(".translate_btn");
const loadingBox = document.querySelector(".loading_box");
const translatedText = document.querySelector(".translate-text");
const textBox = document.querySelectorAll(".main__text-box");
button.addEventListener("click", () => {
  console.log("click");
  loadingBox.classList.add("visible");
  translatedText.textContent = "";
  textBox[1].style.borderColor = "var(--color-main)";
  textBox[1].style.borderWidth = "2px";
});

// Nav menu move
const navMenu = document.querySelector(".nav__menu");
navMenu.addEventListener("click", event => {
  const target = event.target;
  const link = target.dataset.link;
  console.log(link);
  if (link == null) {
    return;
  }
  navMenu.classList.remove("open");
  scrollIntoView(link);
});

// Nav toggle button
const navToggleBtn = document.querySelector(".nav__btn");
navToggleBtn.addEventListener("click", () => {
  navMenu.classList.toggle("open");
});

function scrollIntoView(selector) {
  const scrollTo = document.querySelector(selector);
  scrollTo.scrollIntoView({ behavior: "smooth" });
}

const home = document.querySelector(".main__container");
const homeHeight = home.getBoundingClientRect().height;

const arrowUp = document.querySelector(".arrow-up");
document.addEventListener("scroll", () => {
  if (window.scrollY > homeHeight / 2) {
    arrowUp.classList.add("visible");
  } else {
    arrowUp.classList.remove("visible");
  }
});

// Handle click on the "arrow up" button
arrowUp.addEventListener("click", () => {
  scrollIntoView("#main");
});
