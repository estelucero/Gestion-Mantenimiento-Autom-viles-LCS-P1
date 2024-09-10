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
    const km = document.getElementById("kilometrosViaje");
    const kmFeedback = document.getElementById("kilometroViajeFeedback");
    const kmValor = parseInt(km.value, 10);
    const kilometrosRegex = /^\d+$/; // Regex para validar solo números
  
    if (
      !kilometrosRegex.test(km.value) ||
      kmValor < 200 ||
      kmValor > 1000
    ) {
      mostrarError(km, "kilometroViajeFeedback");
      return false;
    } else {
      mostrarExito(km, "kilometroViajeFeedback");
      return true;
    }
  }
  
  document.getElementById("nombreViaje").addEventListener("input", function () {
    const regexNombreViaje = /^[A-Za-z\s]+$/; // Regex para validar letras
    validarCampo(this, regexNombreViaje, "nombreViajeFeedback");
  });
  
  document.getElementById("kilometrosViaje").addEventListener("input", function () {
    validarKilometros();
  });
  
  document.getElementById("guardar-btn").addEventListener("click", function (event) {
    event.preventDefault();
    const nombreViajeInput = document.getElementById("nombreViaje");
    const kilometrosViajeInput = document.getElementById("kilometrosViaje");
  
    const nombreValido = validarCampo(nombreViajeInput, /^[A-Za-z\s]+$/, "nombreViajeFeedback");
    const kilometrosValido = validarKilometros();
  
    if (nombreValido && kilometrosValido) {
      console.log("Formulario guardado o enviado");
      // Aquí puedes agregar la lógica para enviar el formulario o guardar los datos
    } else {
      console.log("No se puede guardar, hay campos inválidos.");
    }
  });
  
  // Función para limpiar el formulario
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
  
  // Limpiar formulario al cerrar el popup
  document.querySelector(".close-btn").addEventListener("click", function () {
    limpiarFormulario();
  });