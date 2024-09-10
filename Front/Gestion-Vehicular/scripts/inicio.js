const usuarioJSON = JSON.parse(localStorage.getItem("usuario"));

const patenteRegex = /^(?:[A-Za-z]{3}[0-9]{3}|[A-Za-z]{2}[0-9]{3}[A-Za-z]{2})$/;
const modeloMarcaRegex = /^[A-Za-z]+$/;
const fechaRegex = /^\d{4}-\d{2}-\d{2}$/;
const chasisRegex = /^[a-zA-Z0-9]{17}$/;
const kilometrosMax = 450000;
const kilometrosRegex = /^([0-9]|[1-9][0-9]{1,5})$/;

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
    if (usuarioJSON.esParticular) {
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
          location.reload(true);
          // Aquí puedes hacer alguna acción tras el éxito, como redirigir o limpiar el formulario
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Hubo un problema al guardar el vehículo.");
        });
    } else {
      const data = {
        patente,
        modelo,
        marca,
        fechaFabricacion: anioFab,
        vim: chasis,
        cantKm: parseInt(km, 10),
        cuitDueño: usuarioJSON.cuit, // Asume que usuarioJSON es un objeto global con el cuilDueño
      };

      // Enviar el JSON a la API usando fetch
      fetch(
        "https://back-gestion-p1.vercel.app/users/registrarVehiculoUsuarioOrganizacion",
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
          location.reload(true);
          // Aquí puedes hacer alguna acción tras el éxito, como redirigir o limpiar el formulario
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Hubo un problema al guardar el vehículo.");
        });
    }
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

function validarFecha(input) {
  const fechaStr = input.value;
  const fechaRegex = /^\d{4}-\d{2}-\d{2}$/;
  if (!fechaRegex.test(fechaStr)) {
    mostrarError(input, "anio-fab-feedback");
    return false;
  }

  const [anio, mes, dia] = fechaStr.split("-").map(Number);
  const fechaIngresada = new Date(anio, mes - 1, dia);
  const fechaActual = new Date();

  if (
    fechaIngresada.getFullYear() !== anio ||
    fechaIngresada.getMonth() !== mes - 1 ||
    fechaIngresada.getDate() !== dia
  ) {
    mostrarError(input, "anio-fab-feedback");
    return false;
  }

  if (fechaIngresada > fechaActual) {
    mostrarError(input, "anio-fab-feedback");
    return false;
  } else {
    mostrarExito(input, "anio-fab-feedback");
    return true;
  }
}

function validarKilometros() {
  const km = document.getElementById("km");
  const kmFeedback = document.getElementById("km-feedback");
  const kmValor = parseInt(km.value, 10);

  // Validar si el valor coincide con la expresión regular y si está dentro del rango
  if (
    !kilometrosRegex.test(km.value) ||
    kmValor < 0 ||
    kmValor > kilometrosMax
  ) {
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
  validarFecha(this);
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
  isValid =
    validarCampo(modelo, modeloMarcaRegex, "modelo-feedback") && isValid;
  isValid = validarCampo(marca, modeloMarcaRegex, "marca-feedback") && isValid;
  isValid = validarFecha(anioFab) && isValid;
  isValid = validarCampo(chasis, chasisRegex, "chasis-feedback") && isValid;
  isValid = validarKilometros() && isValid;

  if (!isValid) {
    alert("Por favor, completa correctamente todos los campos.");
    return false;
  }

  //alert("Formulario enviado correctamente.");
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

document
  .getElementById("guardar-btn")
  .addEventListener("click", function (event) {
    event.preventDefault();

    const formularioEsValido = validarFormulario();

    if (formularioEsValido) {
      console.log("Formulario guardado o enviado");
      //document.getElementById("formulario").submit();
    } else {
      console.log("No se puede guardar, hay campos inválidos.");
    }
  });

document
  .querySelector(".btn-form:nth-child(2)")
  .addEventListener("click", function (event) {
    event.preventDefault();
    limpiarFormulario();
  });

document.querySelector(".close-btn").addEventListener("click", function () {
  limpiarFormulario();
});

// Realizamos la solicitud GET
if (usuarioJSON.esParticular === true) {
  fetch(
    `https://back-gestion-p1.vercel.app/users/obtenerVehiculosParticular?cuilDueño=${encodeURIComponent(
      usuarioJSON.cuil
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
      localStorage.setItem("autos", JSON.stringify(data));
      const container = document.getElementById("notifications"); // Selecciona el contenedor donde se añadirán los divs

      data.forEach((auto) => {
        console.log(auto);
        const divAuto = document.createElement("div");
        divAuto.classList.add("single-box");

        divAuto.innerHTML = `
    <div class="box-avatar-text">
      <div class="avatar">
        <img
          src="../assets/imagenes/corolla.png"
          alt="perfil-imagen"
        />
      </div>
      <div class="box-text">
        <div class="text-patente">
          <p class="patente-p">${auto.patente.toUpperCase()}</p>
        </div>
        <div class="text-flex">
          Marca:
          <p>${
            auto.marca.charAt(0).toUpperCase() +
            auto.marca.slice(1).toLowerCase()
          }</p>
        </div>
        <div class="text-flex">
          Modelo:
          <p>${
            auto.modelo.charAt(0).toUpperCase() +
            auto.modelo.slice(1).toLowerCase()
          }</p>
        </div>
        <div class="text-flex">
          Año de Fabricación:
          <p>${new Date(auto.fechaFabricacion).getFullYear()}</p>
        </div>
      </div>
    </div>
    <div class="box-img">
      <a href="../views/auto.html">
        <img
          src="../assets/logos/edit-solid-24.png"
          alt="Editar"
          class="user-pic-pic"
        />
      </a>
      <img
        src="../assets/logos/eliminar.png"
        alt="Eliminar"
        class="user-pic-pic eliminar-auto"
      />
    </div>
  `;
        divAuto.addEventListener("click", () => {
          localStorage.setItem("autoSeleccionado", JSON.stringify(auto));
          console.log(`Auto ${auto.patente} guardado en el localStorage`);
        });

        // Agregar evento para guardar en localStorage cuando se haga clic en la tarjeta
        divAuto.addEventListener("click", () => {
          localStorage.setItem("autoSeleccionado", JSON.stringify(auto));
          console.log(`Auto ${auto.patente} guardado en el localStorage`);
        });

        // Seleccionar el ícono de eliminar y añadir un evento para la solicitud de eliminación
        const eliminarIcon = divAuto.querySelector(".eliminar-auto");
        eliminarIcon.addEventListener("click", async (event) => {
          event.stopPropagation(); // Evita que el click se propague al evento de la tarjeta

          // Confirmar antes de eliminar
          const confirmacion = confirm(
            `¿Estás seguro de que quieres eliminar el vehículo con patente ${auto.patente}?`
          );
          if (!confirmacion) return;

          try {
            const response = await fetch(
              `https://back-gestion-p1.vercel.app/users/eliminarVehiculoUsuarioParticular?patente=${auto.patente}`,
              {
                method: "DELETE",
                headers: {
                  "Content-Type": "application/json",
                },
              }
            );

            if (response.ok) {
              console.log(
                `Vehículo con patente ${auto.patente} eliminado con éxito`
              );

              // Opcionalmente, eliminar la tarjeta del DOM
              divAuto.remove();
              window.location.reload();
            } else {
              const errorData = await response.json();
              console.error("Error al eliminar el vehículo:", errorData);
            }
          } catch (error) {
            console.error(
              "Hubo un problema con la solicitud de eliminación:",
              error
            );
          }
        });

        container.appendChild(divAuto);
      });
    })
    .catch((error) => {
      console.error("Error:", error);
    });
} else {
  fetch(
    `https://back-gestion-p1.vercel.app/users/obtenerVehiculosOrganizacion?cuitDueño=${encodeURIComponent(
      usuarioJSON.cuit
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
      localStorage.setItem("autos", JSON.stringify(data));
      const container = document.getElementById("notifications"); // Selecciona el contenedor donde se añadirán los divs

      data.forEach((auto) => {
        console.log(auto);
        const divAuto = document.createElement("div");
        divAuto.classList.add("single-box");

        divAuto.innerHTML = `
    <div class="box-avatar-text">
      <div class="avatar">
        <img
          src="../assets/imagenes/corolla.png"
          alt="perfil-imagen"
        />
      </div>
      <div class="box-text">
        <div class="text-patente">
          <p class="patente-p">${auto.patente.toUpperCase()}</p>
        </div>
        <div class="text-flex">
          Marca:
          <p>${
            auto.marca.charAt(0).toUpperCase() +
            auto.marca.slice(1).toLowerCase()
          }</p>
        </div>
        <div class="text-flex">
          Modelo:
          <p>${
            auto.modelo.charAt(0).toUpperCase() +
            auto.modelo.slice(1).toLowerCase()
          }</p>
        </div>
        <div class="text-flex">
          Año de Fabricación:
          <p>${new Date(auto.fechaFabricacion).getFullYear()}</p>
        </div>
      </div>
    </div>
    <div class="box-img">
      <a href="../views/auto.html">
        <img
          src="../assets/logos/edit-solid-24.png"
          alt="Editar"
          class="user-pic-pic"
        />
      </a>
      <img
        src="../assets/logos/eliminar.png"
        alt="Eliminar"
        class="user-pic-pic eliminar-auto"
      />
    </div>
  `;
        divAuto.addEventListener("click", () => {
          localStorage.setItem("autoSeleccionado", JSON.stringify(auto));
          console.log(`Auto ${auto.patente} guardado en el localStorage`);
        });

        // Agregar evento para guardar en localStorage cuando se haga clic en la tarjeta
        divAuto.addEventListener("click", () => {
          localStorage.setItem("autoSeleccionado", JSON.stringify(auto));
          console.log(`Auto ${auto.patente} guardado en el localStorage`);
        });

        // Seleccionar el ícono de eliminar y añadir un evento para la solicitud de eliminación
        const eliminarIcon = divAuto.querySelector(".eliminar-auto");
        eliminarIcon.addEventListener("click", async (event) => {
          event.stopPropagation(); // Evita que el click se propague al evento de la tarjeta

          // Confirmar antes de eliminar
          const confirmacion = confirm(
            `¿Estás seguro de que quieres eliminar el vehículo con patente ${auto.patente}?`
          );
          if (!confirmacion) return;

          try {
            const response = await fetch(
              `https://back-gestion-p1.vercel.app/users/eliminarVehiculoUsuarioOrganizacion?patente=${auto.patente}`,
              {
                method: "DELETE",
                headers: {
                  "Content-Type": "application/json",
                },
              }
            );

            if (response.ok) {
              console.log(
                `Vehículo con patente ${auto.patente} eliminado con éxito`
              );

              // Opcionalmente, eliminar la tarjeta del DOM
              divAuto.remove();
              window.location.reload();
            } else {
              const errorData = await response.json();
              console.error("Error al eliminar el vehículo:", errorData);
            }
          } catch (error) {
            console.error(
              "Hubo un problema con la solicitud de eliminación:",
              error
            );
          }
        });

        container.appendChild(divAuto);
      });
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
