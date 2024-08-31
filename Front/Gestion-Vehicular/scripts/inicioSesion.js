const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn1 = document.querySelector("#sign-up-btn-p");
const sign_up_btn2 = document.querySelector("#sign-up-btn-e");
const sign_up_p = document.getElementById("form-particular");
const sign_up_e = document.getElementById("form-entidad");
const container = document.querySelector(".sec-container");

sign_up_btn1.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
  sign_up_e.style.display = 'none';
});
sign_up_btn2.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
  sign_up_p.style.display = 'none';
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
  sign_up_e.style.display = 'flex';
  sign_up_p.style.display = 'flex';
});