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
            <img src="../assets/logos/eliminar.png" alt="Eliminar" class="user-pic-pic" data-nombre="${nombre}" data-patente="${patente}" />
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
    document.querySelectorAll(".user-pic-pic").forEach((el) => {
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
