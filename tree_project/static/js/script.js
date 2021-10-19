"use strict";

const button = document.querySelector(".translate_btn");
const loadingBox = document.querySelector(".loading_box");
const translatedText = document.querySelector(".translate-text");
button.addEventListener("click", () => {
  console.log("click");
  loadingBox.classList.add("visible");
  translatedText.textContent = "";
});
