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
patenteElement.textContent = autoGuardado.patente;
marcaElement.textContent = autoGuardado.marca;
modeloElement.textContent = autoGuardado.modelo;
anoElement.textContent = new Date(autoGuardado.fechaFabricacion).getFullYear();
vimElement.textContent = autoGuardado.vim;
kilometrajeElement.textContent = `${autoGuardado.cantKm} Km`;

//Cargar fomulario de alerta
document
  .querySelector(".btn-form")
  .addEventListener("click", async function (event) {
    event.preventDefault(); // Previene el comportamiento por defecto del botón

    // Obtener el valor seleccionado del tipo de alerta
    const tipoAlerta = document.getElementById("campo_rubro").value;
    const tipoAlertaFormateada = transfromarAlerta(tipoAlerta);
    console.log(tipoAlertaFormateada);

    if (tipoAlertaFormateada == "viaje") {
      const fechaInicio = formatearFecha(
        document.getElementById("selectedDate").value
      );
      const nombreViaje = document.getElementById("nombreViaje").value;
      const kilometrosViaje = document.getElementById("kilometrosViaje").value;
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
    default:
      return ""; // Devuelve vacío si no coincide con ninguna alerta
  }
}
function formatearFecha(fecha) {
  const [dia, mes, año] = fecha.split("/");
  return `${año}-${mes.padStart(2, "0")}-${dia.padStart(2, "0")}`;
}

//Cargar alertas
// Realizar una solicitud GET al endpoint de obtener notificaciones
fetch(
  `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesParticular?patente=${autoGuardado.patente}`
)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Error en la solicitud");
    }
    return response.json(); // Convertir la respuesta a JSON
  })
  .then((data) => {
    const contenedorAlertas = document.getElementById("alertas");

    // Función para crear el HTML de la alerta con evento de eliminar
    const crearAlertaHTML = (nombre, fechaVence, patente) => {
      return `
        <div class="alerta">
          <div class="box-avatar-text">
            <div class="avatar">
              <img src="../assets/logos/${nombre}.png" alt="${nombre}" />
            </div>
            <div class="box-text">
              <div class="text-patente">
                <p>${nombre.replace("_", " ")}</p>
              </div>
              <div class="text-flex">
                Fecha de alerta:
                <p>${new Date(fechaVence).toLocaleDateString()}</p>
              </div>
            </div>
          </div>
          <div class="box-img">
            <img src="../assets/logos/eliminar.png" alt="Eliminar" class="user-pic-pic eliminar" data-nombre="${nombre}" data-patente="${patente}"  />
          </div>
        </div>
      `;
    };

    // Iterar sobre las notificaciones y generar las alertas
    data.listaNotif.forEach((notif) => {
      const alertaHTML = crearAlertaHTML(
        notif.nombre,
        notif.fechaVence,
        notif.patente
      );
      contenedorAlertas.insertAdjacentHTML("beforeend", alertaHTML);
    });

    // Agregar evento de click a cada ícono de eliminar
    document.querySelectorAll(".eliminar").forEach((el) => {
      el.addEventListener("click", (e) => {
        const nombreAlerta = e.target.getAttribute("data-nombre");
        const patente = e.target.getAttribute("data-patente");

        // Confirmar eliminación
        if (
          confirm(
            `¿Estás seguro de que deseas eliminar la alerta ${nombreAlerta}?`
          )
        ) {
          // Hacer la solicitud DELETE al endpoint de eliminación
          fetch(
            `https://back-gestion-p1.vercel.app/users/eliminarRevisionVehiculoParticular?patente=${patente}&nombreRevision=${nombreAlerta}`,
            {
              method: "DELETE",
              headers: {
                "Content-Type": "application/json",
              },
            }
          )
            .then((response) => {
              if (!response.ok) {
                throw new Error("Error al eliminar la alerta");
              }
              return response.json();
            })
            .then(() => {
              // Remover la alerta del DOM después de eliminarla
              e.target.closest(".alerta").remove();
              alert(`La alerta ${nombreAlerta} ha sido eliminada.`);
            })
            .catch((error) => {
              console.error("Hubo un problema con la eliminación:", error);
            });
        }
      });
    });
  })
  .catch((error) => {
    console.error("Hubo un problema con la solicitud:", error);
  });

///Agregar Viaje Programado
fetch(
  `https://back-gestion-p1.vercel.app/users/obtenerViajesVehiculo?patente=${autoGuardado.patente}`
)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Error en la solicitud");
    }
    return response.json(); // Convertir la respuesta a JSON
  })
  .then((data) => {
    const contenedorAlertas = document.getElementById("alertas");

    // Función para crear el HTML de la alerta con evento de eliminar
    const crearAlertaHTML = (nombre, fechaVence, patente, id) => {
      return `
        <div class="alerta">
          <div class="box-avatar-text">
            <div class="avatar">
              <img src="../assets/logos/viaje.png" alt="${nombre}" />
            </div>
            <div class="box-text">
              <div class="text-patente">
                <p>${nombre.replace("_", " ")}</p>
              </div>
              <div class="text-flex">
                Fecha de alerta:
                <p>${new Date(fechaVence).toLocaleDateString()}</p>
              </div>
            </div>
          </div>
          <div class="box-img">
            <img src="../assets/logos/eliminar.png" alt="Eliminar" class="user-pic-pic eliminar-viaje" data-nombre="${nombre}" data-patente="${patente}" data-id="${id}" />
          </div>
        </div>
      `;
    };

    // Iterar sobre las notificaciones y generar las alertas
    data.forEach((notif) => {
      const alertaHTML = crearAlertaHTML(
        notif.nombreViaje,
        notif.fechaInicio,
        notif.patenteVehiculo,
        notif.idViaje
      );
      contenedorAlertas.insertAdjacentHTML("beforeend", alertaHTML);
    });

    // Agregar evento de click a cada ícono de eliminar
    document.querySelectorAll(".eliminar-viaje").forEach((el) => {
      el.addEventListener("click", (e) => {
        const id = e.target.getAttribute("data-id");
        const nombreAlerta = e.target.getAttribute("data-nombre");
        console.log(id);
        // Confirmar eliminación
        if (
          confirm(
            `¿Estás seguro de que deseas eliminar la alerta ${nombreAlerta}?`
          )
        ) {
          // Hacer la solicitud DELETE al endpoint de eliminación
          fetch(
            `https://back-gestion-p1.vercel.app/users/eliminarViaje?id=${id}`,
            {
              method: "DELETE",
              headers: {
                "Content-Type": "application/json",
              },
            }
          )
            .then((response) => {
              if (!response.ok) {
                throw new Error("Error al eliminar la alerta");
              }
              return response.json();
            })
            .then(() => {
              // Remover la alerta del DOM después de eliminarla
              e.target.closest(".alerta").remove();
              alert(`La alerta ${nombreAlerta} ha sido eliminada.`);
            })
            .catch((error) => {
              console.error("Hubo un problema con la eliminación:", error);
            });
        }
      });
    });
  })
  .catch((error) => {
    console.error("Hubo un problema con la solicitud:", error);
  });
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
