let subMenu = document.getElementById("subMenu");
function toggleMenu() {
  subMenu.classList.toggle("open-menu");
}

document.querySelector("#show-car").addEventListener("click", function () {
  document.querySelector(".popup").classList.add("active");
  document.querySelector(".header-desactive").classList.add("active");
  document.querySelector(".popup-container").classList.add("active");
});

document
  .querySelector(".popup .close-btn")
  .addEventListener("click", function () {
    document.querySelector(".popup").classList.remove("active");
    document.querySelector(".header-desactive").classList.remove("active");
    document.querySelector(".popup-container").classList.remove("active");
  });

document
  .querySelector(".btn-form:nth-of-type(2)")
  .addEventListener("click", function () {
    document.querySelector(".popup").classList.remove("active");
    document.querySelector(".header-desactive").classList.remove("active");
    document.querySelector(".popup-container").classList.remove("active");
  });
