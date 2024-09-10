// setTimeout(function () {
//   location.reload();
// }, 1000);
const usuarioJSON = JSON.parse(localStorage.getItem("usuario"));
function populateDateSelectors() {
  const monthSelect = document.getElementById("month");
  const yearSelect = document.getElementById("year");
  const today = new Date();
  const currentYear = today.getFullYear();

  // Meses
  for (let month = 0; month < 12; month++) {
    const option = document.createElement("option");
    option.value = month;
    option.textContent = new Date(currentYear, month).toLocaleString(
      "default",
      { month: "long" }
    );
    monthSelect.appendChild(option);
  }

  // Años
  for (let year = currentYear - 50; year <= currentYear + 10; year++) {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
  }

  // Set default values
  monthSelect.value = today.getMonth();
  yearSelect.value = currentYear;

  // Initialize calendar
  updateCalendar();
}

function updateCalendar() {
  const monthSelect = document.getElementById("month");
  const yearSelect = document.getElementById("year");
  const calendarBody = document.querySelector(".calendar-body");
  const month = parseInt(monthSelect.value);
  const year = parseInt(yearSelect.value);

  // Clear previous days
  calendarBody.querySelectorAll(".day").forEach((day) => day.remove());

  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  // Add empty cells for days before the first day of the month
  for (let i = 0; i < firstDay; i++) {
    const emptyCell = document.createElement("div");
    calendarBody.appendChild(emptyCell);
  }

  // Add cells for each day of the month
  for (let day = 1; day <= daysInMonth; day++) {
    const dayCell = document.createElement("div");
    dayCell.className = "day";
    dayCell.textContent = day;
    dayCell.addEventListener("click", () => {
      calendarBody
        .querySelectorAll(".day")
        .forEach((d) => d.classList.remove("selected"));
      dayCell.classList.add("selected");
      document.getElementById("selectedDate").value = `${day}/${
        month + 1
      }/${year}`;
    });
    calendarBody.appendChild(dayCell);
  }
}

document.getElementById("month").addEventListener("change", updateCalendar);
document.getElementById("year").addEventListener("change", updateCalendar);

// Inicializar
populateDateSelectors();

//Cargar datos de auto
const autoGuardado = JSON.parse(localStorage.getItem("autoSeleccionado"));
console.log(autoGuardado);

// Seleccionar los elementos del HTML donde se insertará la información
const patenteElement = document.querySelector(".titulo");
const marcaElement = document.querySelector(
  ".auto-info-text-section:nth-child(2) p"
);
const modeloElement = document.querySelector(
  ".auto-info-text-section:nth-child(3) p"
);
const anoElement = document.querySelector(
  ".auto-info-text-section:nth-child(4) p"
);
const vimElement = document.querySelector(
  ".auto-info-text-section:nth-child(5) p"
);
const kilometrajeElement = document.querySelector(
  ".auto-info-text-section:nth-child(6) p"
);

// Asignar los valores del objeto 'auto' a los elementos del HTML
patenteElement.textContent = autoGuardado.patente.toUpperCase();
marcaElement.textContent =
  autoGuardado.marca.charAt(0).toUpperCase() +
  autoGuardado.marca.slice(1).toLowerCase();
modeloElement.textContent =
  autoGuardado.modelo.charAt(0).toUpperCase() +
  autoGuardado.modelo.slice(1).toLowerCase();
anoElement.textContent = new Date(autoGuardado.fechaFabricacion).getFullYear();
vimElement.textContent = autoGuardado.vim;
kilometrajeElement.textContent = `${autoGuardado.cantKm} Km`;

///
function eliminarOpcionViaje() {
  if (!usuarioJSON.esParticular) {
    const selectRubro = document.getElementById("campo_rubro");
    const opcionViaje = selectRubro.querySelector('option[value="viaje"]');
    opcionViaje.style.display = "none";
  }
}
eliminarOpcionViaje();
//Cargar fomulario de alerta
document
  .querySelector(".btn-form")
  .addEventListener("click", async function (event) {
    event.preventDefault(); // Previene el comportamiento por defecto del botón

    // Obtener el valor seleccionado del tipo de alerta
    const tipoAlerta = document.getElementById("campo_rubro").value;
    const tipoAlertaFormateada = transfromarAlerta(tipoAlerta);
    console.log(tipoAlertaFormateada);
    if (usuarioJSON.esParticular) {
      if (tipoAlertaFormateada == "viaje") {
        const fechaInicio = formatearFecha(
          document.getElementById("selectedDate").value
        );
        const nombreViaje = document.getElementById("nombreViaje").value;
        const kilometrosViaje =
          document.getElementById("kilometrosViaje").value;
        const data = {
          fechaInicio: fechaInicio,
          distanciaKM: parseInt(kilometrosViaje, 10), // Convertir a número
          nombre: nombreViaje,
          patente: autoGuardado.patente,
        };
        console.log(data);
        try {
          const response = await fetch(
            "https://back-gestion-p1.vercel.app/users/ingresarViaje",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(data),
            }
          );

          if (!response.ok) {
            throw new Error("Error en el envío de la revisión");
          }

          const result = await response.json();
          alert("Revisión guardada con éxito");
          console.log(result); // Puedes hacer algo más con la respuesta
          location.reload(true);
        } catch (error) {
          alert("Hubo un error al guardar la revisión: " + error.message);
        }
      } else {
        // Obtener la fecha seleccionada del input de fecha
        const fechaUltimaRevision = formatearFecha(
          document.getElementById("selectedDate").value
        );
        console.log(fechaUltimaRevision);
        // Asignar una patente de ejemplo, si tienes un input para la patente puedes usar su valor
        // Puedes reemplazar esto por el valor dinámico

        // Verifica si el tipo de alerta y la fecha han sido seleccionados
        if (!tipoAlerta || !fechaUltimaRevision) {
          alert("Por favor, complete todos los campos.");
          return;
        }

        // Definir la fecha de próxima revisión (esto puede depender de la lógica de tu negocio)
        const fechaProximaRevision = fechaUltimaRevision;

        // Definir el estado de la revisión (puedes cambiarlo según la lógica de tu aplicación)
        const estado = "a";

        // Construir el cuerpo del JSON
        const data = [
          {
            nombre: tipoAlertaFormateada,
            fechaUltRevision: fechaUltimaRevision,
            fechaProxRevision: fechaProximaRevision,
            estado: estado,
            patente: autoGuardado.patente,
          },
        ];

        try {
          const response = await fetch(
            "https://back-gestion-p1.vercel.app/users/agregarRevisionesVehiculoParticular",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(data),
            }
          );

          if (!response.ok) {
            throw new Error("Error en el envío de la revisión");
          }

          const result = await response.json();
          alert("Revisión guardada con éxito");
          console.log(result); // Puedes hacer algo más con la respuesta
          location.reload(true);
        } catch (error) {
          alert("Hubo un error al guardar la revisión: " + error.message);
        }
      }
    } else {
      // Obtener la fecha seleccionada del input de fecha
      const fechaUltimaRevision = formatearFecha(
        document.getElementById("selectedDate").value
      );
      console.log(fechaUltimaRevision);
      // Asignar una patente de ejemplo, si tienes un input para la patente puedes usar su valor
      // Puedes reemplazar esto por el valor dinámico

      // Verifica si el tipo de alerta y la fecha han sido seleccionados
      if (!tipoAlerta || !fechaUltimaRevision) {
        alert("Por favor, complete todos los campos.");
        return;
      }

      // Definir la fecha de próxima revisión (esto puede depender de la lógica de tu negocio)
      const fechaProximaRevision = fechaUltimaRevision;

      // Definir el estado de la revisión (puedes cambiarlo según la lógica de tu aplicación)
      const estado = "a";

      // Construir el cuerpo del JSON
      const data = [
        {
          nombre: tipoAlertaFormateada,
          fechaUltRevision: fechaUltimaRevision,
          fechaProxRevision: fechaProximaRevision,
          estado: estado,
          patente: autoGuardado.patente,
        },
      ];

      try {
        const response = await fetch(
          "https://back-gestion-p1.vercel.app/users/agregarRevisionesVehiculoOrganizacion",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          }
        );

        if (!response.ok) {
          throw new Error("Error en el envío de la revisión");
        }

        const result = await response.json();
        alert("Revisión guardada con éxito");
        console.log(result); // Puedes hacer algo más con la respuesta
        location.reload(true);
      } catch (error) {
        alert("Hubo un error al guardar la revisión: " + error.message);
      }
    }
  });
function transfromarAlerta(tipoAlerta) {
  switch (tipoAlerta) {
    case "aceite":
      return "cambio_aceite";
    case "neumatico":
      return "revision_neumaticos";
    case "fluidos":
      return "revision_fluidos";
    case "servicio":
      return "servicio_completo";
    case "escape":
      return "revision_escape";
    case "bateria":
      return "revision_bateria";
    case "enfriamiento":
      return "revision_refrig";
    case "viaje":
      return "viaje";
    case "vtv":
      return "revision_vtv";
    default:
      return ""; // Devuelve vacío si no coincide con ninguna alerta
  }
}
function formatearFecha(fecha) {
  const [dia, mes, año] = fecha.split("/");
  return `${año}-${mes.padStart(2, "0")}-${dia.padStart(2, "0")}`;
}

//Editar campos
// Seleccionar todas las imágenes con la clase 'edit-icon'
document.querySelectorAll(".edit-icon").forEach((icon) => {
  icon.addEventListener("click", function () {
    const fieldId = this.getAttribute("data-field"); // Obtener el campo que se va a editar
    const fieldElement = document.getElementById(fieldId);

    if (fieldElement.tagName === "P") {
      const currentValue = fieldElement.innerText.trim();
      fieldElement.innerHTML = `<input type="text" id="input-${fieldId}" value="${currentValue}" />`;
    }

    document.getElementById("save-btn").style.display = "block"; // Mostrar botón de guardar
  });
});

// Guardar los cambios cuando se hace clic en "Guardar"
document.getElementById("save-btn").addEventListener("click", function () {
  // Obtener los valores de los campos y actualizar en caso de que sean inputs

  const modelo = document.getElementById("modelo").querySelector("input")
    ? document.getElementById("modelo").querySelector("input").value
    : document.getElementById("modelo").innerText.trim();

  const marca = document.getElementById("marca").querySelector("input")
    ? document.getElementById("marca").querySelector("input").value
    : document.getElementById("marca").innerText.trim();

  const fecha = document.getElementById("anio").querySelector("input")
    ? document.getElementById("anio").querySelector("input").value
    : document.getElementById("anio").innerText.trim();

  const vim = document.getElementById("chasis").querySelector("input")
    ? document.getElementById("chasis").querySelector("input").value
    : document.getElementById("chasis").innerText.trim();

  const cantKM = document.getElementById("kilometraje").querySelector("input")
    ? document.getElementById("kilometraje").querySelector("input").value
    : document.getElementById("kilometraje").innerText.trim();

  // Reemplazar los inputs por los valores guardados
  document.querySelectorAll("input").forEach((input) => {
    const fieldId = input.id.replace("input-", ""); // Obtener el ID del campo
    const newValue = input.value;
    document.getElementById(fieldId).innerHTML = newValue; // Actualizar el campo de texto
  });

  // Enviar la solicitud a través de fetch
  const data = {
    patente: autoGuardado.patente,
    modelo: modelo,
    marca: marca,
    fecha: fecha + "-01-02",
    vim: vim,
    cantKM: parseInt(cantKM),
  };
  console.log(data);
  if (usuarioJSON.esParticular) {
    fetch(
      `https://back-gestion-p1.vercel.app/users/modificarVehiculoParticular`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        alert("Datos del vehículo actualizados correctamente");
        window.location.href = "../views/inicio.html";
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Hubo un error al actualizar los datos");
      });
  } else {
    fetch(
      `https://back-gestion-p1.vercel.app/users/modificarVehiculoOrganizacion`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        alert("Datos del vehículo actualizados correctamente");
        window.location.href = "../views/inicio.html";
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Hubo un error al actualizar los datos");
      });
  }

  // Ocultar el botón de guardar después de guardar los cambios
  document.getElementById("save-btn").style.display = "none";
});

//Seleccionar viajeProgramado
document.getElementById("campo_rubro").addEventListener("change", function () {
  const viajeInputs = document.getElementById("viaje-programado-inputs");
  const labelViaje = document.getElementById("label-viaje");
  const labelPatente = document.getElementById("label-patente");

  if (this.value === "viaje") {
    // Mostrar los campos adicionales
    viajeInputs.style.display = "block";
    labelViaje.style.display = "block";
    labelPatente.style.display = "none";
  } else {
    // Ocultar los campos si se selecciona otra opción
    viajeInputs.style.display = "none";
    labelViaje.style.display = "none";
    labelPatente.style.display = "block";
  }
});

////Cargar alertas del vechiculo///
// Asumiendo que 'alertas' es el ID del contenedor donde quieres agregar las tarjetas
const contenedorAlertas = document.getElementById("alertas");

// Función para obtener notificaciones y crear las tarjetas
async function cargarNotificacionesParticular() {
  try {
    const response = await fetch(
      `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesParticular?patente=${autoGuardado.patente}`
    );
    const data = await response.json();

    // Verifica que `listaNotif` existe y es un array
    if (Array.isArray(data.listaNotif)) {
      data.listaNotif.forEach((notificacion) => {
        // Crear el elemento tarjeta
        const alertaDiv = document.createElement("div");
        alertaDiv.className = "alerta";

        // Crear la estructura interna de la tarjeta
        alertaDiv.innerHTML = `
          <div class="box-avatar-text">
            <div class="avatar">
              <img src="../assets/logos/${
                notificacion.nombre
              }.png" alt="perfil-imagen" />
            </div>
            <div class="box-text">
              <div class="text-patente">
                <p>${
                  notificacion.nombre.charAt(0).toUpperCase() +
                  notificacion.nombre.slice(1).toLowerCase().replace("_", " ")
                }</p>
              </div>
              <div class="text-flex">
                Fecha de alerta:
                <p>${
                  new Date(notificacion.fechaVence).toLocaleDateString() ||
                  "Fecha no disponible"
                }</p>
              </div>
            </div>
          </div>
          <div class="box-img">
            <img src="../assets/logos/eliminar.png" alt="" class="user-pic-pic eliminar-alerta" />
          </div>
        `;
        const eliminarIcono = alertaDiv.querySelector(".eliminar-alerta");
        eliminarIcono.addEventListener("click", async () => {
          try {
            // Enviar solicitud DELETE al backend para eliminar la notificación
            const response = await fetch(
              `https://back-gestion-p1.vercel.app/users/eliminarRevisionVehiculoParticular?patente=${notificacion.patente}&nombreRevision=${notificacion.nombre}`,
              {
                method: "DELETE",
              }
            );

            if (response.ok) {
              location.reload(true);
              // Si la respuesta es exitosa, eliminar el div del DOM
              alertaDiv.remove();
            } else {
              console.error("Error al eliminar la notificación en el backend");
            }
          } catch (error) {
            console.error(
              "Error al enviar la solicitud de eliminación:",
              error
            );
          }
        });

        // Añadir la tarjeta al contenedor
        contenedorAlertas.appendChild(alertaDiv);
      });
    } else {
      console.error("La propiedad listaNotif no es un array");
    }
  } catch (error) {
    console.error("Error al obtener las notificaciones:", error);
  }
}

///

async function cargarNotificacionesOrganizacion() {
  try {
    const response = await fetch(
      `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesOrganizacion?patente=${autoGuardado.patente}`
    );
    const data = await response.json();

    // Verifica que `listaNotif` existe y es un array
    if (Array.isArray(data.listaNotif)) {
      data.listaNotif.forEach((notificacion) => {
        // Crear el elemento tarjeta
        const alertaDiv = document.createElement("div");
        alertaDiv.className = "alerta";

        // Crear la estructura interna de la tarjeta
        alertaDiv.innerHTML = `
          <div class="box-avatar-text">
            <div class="avatar">
              <img src="../assets/logos/${
                notificacion.nombre
              }.png" alt="perfil-imagen" />
            </div>
            <div class="box-text">
              <div class="text-patente">
                <p>${
                  notificacion.nombre.charAt(0).toUpperCase() +
                  notificacion.nombre.slice(1).toLowerCase().replace("_", " ")
                }</p>
              </div>
              <div class="text-flex">
                Fecha de alerta:
                <p>${
                  new Date(notificacion.fechaVence).toLocaleDateString() ||
                  "Fecha no disponible"
                }</p>
              </div>
            </div>
          </div>
          <div class="box-img">
            <img src="../assets/logos/eliminar.png" alt="" class="user-pic-pic eliminar-alerta" />
          </div>
        `;
        const eliminarIcono = alertaDiv.querySelector(".eliminar-alerta");
        eliminarIcono.addEventListener("click", async () => {
          try {
            // Enviar solicitud DELETE al backend para eliminar la notificación
            const response = await fetch(
              `https://back-gestion-p1.vercel.app/users/eliminarRevisionVehiculoOrganizacion?patente=${notificacion.patente}&nombreRevision=${notificacion.nombre}`,
              {
                method: "DELETE",
              }
            );

            if (response.ok) {
              location.reload(true);
              // Si la respuesta es exitosa, eliminar el div del DOM
              alertaDiv.remove();
            } else {
              console.error("Error al eliminar la notificación en el backend");
            }
          } catch (error) {
            console.error(
              "Error al enviar la solicitud de eliminación:",
              error
            );
          }
        });

        // Añadir la tarjeta al contenedor
        contenedorAlertas.appendChild(alertaDiv);
      });
    } else {
      console.error("La propiedad listaNotif no es un array");
    }
  } catch (error) {
    console.error("Error al obtener las notificaciones:", error);
  }
}

//
const contenedorAlertasViajes = document.getElementById("alertas");
////Agregar Viajes Programados/////////
async function cargarViajes() {
  try {
    const response = await fetch(
      `https://back-gestion-p1.vercel.app/users/obtenerViajesVehiculo?patente=${autoGuardado.patente}`
    );
    const data = await response.json();

    // Verifica que `listaNotif` existe y es un array
    if (Array.isArray(data)) {
      data.forEach((notificacion) => {
        // Crear el elemento tarjeta
        const alertaDiv = document.createElement("div");
        alertaDiv.className = "alerta";

        // Crear la estructura interna de la tarjeta
        alertaDiv.innerHTML = `
          <div class="box-avatar-text">
            <div class="avatar">
              <img src="../assets/logos/viaje.png" alt="perfil-imagen" />
            </div>
            <div class="box-text">
              <div class="text-patente">
                <p>${notificacion.nombreViaje}</p>
              </div>
              <div class="text-flex">
                Fecha de alerta:
                <p>${
                  new Date(notificacion.fechaInicio).toLocaleDateString() ||
                  "Fecha no disponible"
                }</p>
              </div>
            </div>
          </div>
          <div class="box-img">
            <img src="../assets/logos/eliminar.png" alt="" class="user-pic-pic eliminar-viaje" />
          </div>
        `;
        contenedorAlertasViajes.appendChild(alertaDiv);
        const eliminarIcono = alertaDiv.querySelector(".eliminar-viaje");

        eliminarIcono.addEventListener("click", async () => {
          console.log(eliminarIcono);
          try {
            // Enviar solicitud DELETE al backend para eliminar la notificación
            const response = await fetch(
              `https://back-gestion-p1.vercel.app/users/eliminarViaje?id=${notificacion.idViaje}`,
              {
                method: "DELETE",
              }
            );

            if (response.ok) {
              location.reload(true);
              // Si la respuesta es exitosa, eliminar el div del DOM
              alertaDiv.remove();
            } else {
              console.error("Error al eliminar la notificación en el backend");
            }
          } catch (error) {
            console.error(
              "Error al enviar la solicitud de eliminación:",
              error
            );
          }
        });

        // Añadir la tarjeta al contenedor
      });
    } else {
      console.error("La propiedad listaNotif no es un array");
    }
  } catch (error) {
    console.error("Error al obtener las notificaciones:", error);
  }
}
if (usuarioJSON.esParticular) {
  cargarNotificacionesParticular();
  cargarViajes();
} else {
  cargarNotificacionesOrganizacion();
}

// Función para crear una tarjeta
// Función para crear una tarjeta
// function crearTarjeta(viaje) {
//   // Crear los elementos
//   const alertaDiv = document.createElement("div");
//   alertaDiv.className = "alerta";

//   const boxAvatarTextDiv = document.createElement("div");
//   boxAvatarTextDiv.className = "box-avatar-text";

//   const avatarDiv = document.createElement("div");
//   avatarDiv.className = "avatar";

//   const imgAvatar = document.createElement("img");
//   imgAvatar.src = "../assets/logos/vtv.png";
//   imgAvatar.alt = "perfil-imagen";

//   avatarDiv.appendChild(imgAvatar);

//   const boxTextDiv = document.createElement("div");
//   boxTextDiv.className = "box-text";

//   const textPatenteDiv = document.createElement("div");
//   textPatenteDiv.className = "text-patente";

//   const pPatente = document.createElement("p");
//   pPatente.textContent = "VTV"; // Cambiar esto según el tipo de alerta o viaje

//   textPatenteDiv.appendChild(pPatente);

//   const textFlexDiv = document.createElement("div");
//   textFlexDiv.className = "text-flex";

//   const fechaTexto = document.createElement("p");
//   fechaTexto.textContent = `Fecha de alerta: ${viaje.fechaInicio}`; // Modificar según el formato de fecha que tengas

//   textFlexDiv.appendChild(fechaTexto);

//   boxTextDiv.appendChild(textPatenteDiv);
//   boxTextDiv.appendChild(textFlexDiv);

//   boxAvatarTextDiv.appendChild(avatarDiv);
//   boxAvatarTextDiv.appendChild(boxTextDiv);

//   const boxImgDiv = document.createElement("div");
//   boxImgDiv.className = "box-img";

//   const imgEliminar = document.createElement("img");
//   imgEliminar.src = "../assets/logos/eliminar.png";
//   imgEliminar.alt = "";
//   imgEliminar.className = "eliminar-alerta"; // Cambiado de 'user-pic-pic' a 'eliminar-alerta'

//   // Agregar evento de clic para eliminar el div
//   imgEliminar.addEventListener("click", async () => {
//     try {
//       // Enviar solicitud de eliminación al backend
//       await fetch(
//         `https://back-gestion-p1.vercel.app/users/eliminarRevisionVehiculoParticular?patente=${viaje.patente}&nombre=${viaje.nombre}`,
//         {
//           method: "DELETE",
//         }
//       );

//       // Eliminar el div del DOM
//       alertaDiv.remove();
//     } catch (error) {
//       console.error("Error al eliminar la revisión:", error);
//     }
//   });

//   boxImgDiv.appendChild(imgEliminar);

//   alertaDiv.appendChild(boxAvatarTextDiv);
//   alertaDiv.appendChild(boxImgDiv);

//   return alertaDiv;
// }

// // Función para cargar los viajes y crear las tarjetas
// async function cargarViajes() {
//   try {
//     const response = await fetch(
//       `https://back-gestion-p1.vercel.app/users/obtenerViajesVehiculo?patente=${autoGuardado.patente}`
//     );
//     const viajes = await response.json();

//     const contenedorAlertas = document.getElementById("alertas");
//     // Limpiar el contenedor antes de añadir nuevas tarjetas

//     viajes.forEach((viaje) => {
//       const tarjeta = crearTarjeta(viaje);
//       contenedorAlertas.appendChild(tarjeta);
//     });
//   } catch (error) {
//     console.error("Error al cargar los viajes:", error);
//   }
// }

// Llamar a la función para cargar los viajes al cargar la página
