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
