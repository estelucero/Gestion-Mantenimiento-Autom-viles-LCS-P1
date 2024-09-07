const usuarioJSON = JSON.parse(localStorage.getItem("usuario"));

const patenteRegex = /^(?:[A-Za-z]{3}[0-9]{3}|[A-Za-z]{2}[0-9]{3}[A-Za-z]{2})$/;
const modeloMarcaRegex = /^[A-Za-z]+$/;
const fechaRegex = /^\d{4}-\d{2}-\d{2}$/;
const chasisRegex = /^[A-HJ-NPR-Z0-9]{17}$/;
const kilometrosMax = 450000;

console.log(usuarioJSON);
//Resgistro de auto
document
  .getElementById("guardar-btn")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    // Captura los valores de los campos
    const patente = document.getElementById("patente").value;
    const modelo = document.getElementById("modelo").value;
    const marca = document.getElementById("marca").value;
    const anioFab = document.getElementById("anio-fab").value;
    const chasis = document.getElementById("chasis").value;
    const km = document.getElementById("km").value;
    const imagen = document.getElementById("imagen").files[0]; // Captura el archivo de imagen

    // Validar que los campos no estén vacíos
    if (!patente || !modelo || !marca || !anioFab || !chasis || !km) {
      alert("Por favor, completa todos los campos.");
      return;
    }

    // Crear un objeto JSON con los datos del formulario
    const data = {
      patente,
      modelo,
      marca,
      fechaFabricacion: anioFab,
      vim: chasis,
      cantKm: parseInt(km, 10),
      cuilDueño: usuarioJSON.cuil, // Asume que usuarioJSON es un objeto global con el cuilDueño
    };

    // Enviar el JSON a la API usando fetch
    fetch(
      "https://back-gestion-p1.vercel.app/users/registrarVehiculoUsuarioParticular",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        alert("Vehículo guardado con éxito");
        // Aquí puedes hacer alguna acción tras el éxito, como redirigir o limpiar el formulario
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Hubo un problema al guardar el vehículo.");
      });
  });

// Realizamos la solicitud GET
fetch(
  `https://back-gestion-p1.vercel.app/users/obtenerVehiculosParticular?cuilDueño=${encodeURIComponent(
    usuarioJSON.cuilDueño
  )}`
)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Error en la solicitud: " + response.statusText);
    }
    return response.json(); // Convertimos la respuesta a JSON
  })
  .then((data) => {
    // Aquí puedes procesar los datos recibidos
    console.log("Vehículos obtenidos:", data);
  })
  .catch((error) => {
    console.error("Error:", error);
  });


function mostrarError(input, feedbackId) {
  input.classList.remove("is-valid");
  input.classList.add("is-invalid");
  document.getElementById(feedbackId).style.display = "block";
}

function mostrarExito(input, feedbackId) {
  input.classList.remove("is-invalid");
  input.classList.add("is-valid");
  document.getElementById(feedbackId).style.display = "none";
}

function validarCampo(input, regex, feedbackId) {
  if (!regex.test(input.value) || input.value.trim() === "") {
    mostrarError(input, feedbackId);
    return false;
  } else {
    mostrarExito(input, feedbackId);
    return true;
  }
}

function validarKilometros() {
  const km = document.getElementById("km");
  const kmFeedback = document.getElementById("km-feedback");

  if (km.value < 0 || km.value > kilometrosMax || km.value === "") {
    mostrarError(km, "km-feedback");
    return false;
  } else {
    mostrarExito(km, "km-feedback");
    return true;
  }
}

document.getElementById("patente").addEventListener("input", function () {
  this.value = this.value.toLowerCase();
  validarCampo(this, patenteRegex, "patente-feedback");
});

document.getElementById("modelo").addEventListener("input", function () {
  this.value = this.value.toLowerCase();
  validarCampo(this, modeloMarcaRegex, "modelo-feedback");
});

document.getElementById("marca").addEventListener("input", function () {
  this.value = this.value.toLowerCase();
  validarCampo(this, modeloMarcaRegex, "marca-feedback");
});

document.getElementById("anio-fab").addEventListener("input", function () {
  validarCampo(this, fechaRegex, "anio-fab-feedback");
});

document.getElementById("chasis").addEventListener("input", function () {
  validarCampo(this, chasisRegex, "chasis-feedback");
});

document.getElementById("km").addEventListener("input", function () {
  validarKilometros();
});

function validarFormulario() {
  let isValid = true;

  const patente = document.getElementById("patente");
  const modelo = document.getElementById("modelo");
  const marca = document.getElementById("marca");
  const anioFab = document.getElementById("anio-fab");
  const chasis = document.getElementById("chasis");
  const km = document.getElementById("km");

  isValid = validarCampo(patente, patenteRegex, "patente-feedback") && isValid;
  isValid = validarCampo(modelo, modeloMarcaRegex, "modelo-feedback") && isValid;
  isValid = validarCampo(marca, modeloMarcaRegex, "marca-feedback") && isValid;
  isValid = validarCampo(anioFab, fechaRegex, "anio-fab-feedback") && isValid;
  isValid = validarCampo(chasis, chasisRegex, "chasis-feedback") && isValid;
  isValid = validarKilometros() && isValid;

  if (!isValid) {
    alert("Por favor, completa correctamente todos los campos.");
    return false;
  }

  alert("Formulario enviado correctamente.");
  return true;
}

function limpiarFormulario() {
  const inputs = document.querySelectorAll(".form input");
  inputs.forEach((input) => {
    input.value = "";
    input.classList.remove("is-valid", "is-invalid");
  });

  const feedbacks = document.querySelectorAll(".invalid-feedback");
  feedbacks.forEach((feedback) => {
    feedback.style.display = "none";
  });
}

document.getElementById("guardar-btn").addEventListener("click", function (event) {
  event.preventDefault();

  const formularioEsValido = validarFormulario();

  if (formularioEsValido) {
    console.log("Formulario guardado o enviado");
    document.getElementById("formulario").submit();
  } else {
    console.log("No se puede guardar, hay campos inválidos.");
  }
});

document.querySelector(".btn-form:nth-child(2)").addEventListener("click", function (event) {
  event.preventDefault();
  limpiarFormulario();
});

document.querySelector(".close-btn").addEventListener("click", function () {
  limpiarFormulario();
});