const autoGuardado = JSON.parse(localStorage.getItem("autoSeleccionado"));
const urlGetNotificacion = `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesSinLeerParticular?patente=${autoGuardado.patente}`;
const urlDeleteNotificacion = `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesSinLeerParticular?idNotif`;
let subMenu = document.getElementById("subMenu");
function toggleMenu() {
  subMenu.classList.toggle("open-menu");
}

// Función para cargar notificaciones
async function cargarNotificaciones() {
  try {
    const response = await fetch(urlGetNotificacion);
    const data = await response.json();

    const container = document.querySelector(".notifications");
    data.forEach((notificacion) => {
      const card = document.createElement("div");
      card.classList.add("single-box", "unseen");
      card.innerHTML = `
        <div class="avatar-box-text">
          <div class="avatar">
            <img src="../assets/imagenes/corolla.png" alt="perfil-imagen" />
          </div>
          <div class="box-text">
            <p class="notifi">
              <a href="#" class="name">${notificacion.modelo}</a> necesita ${notificacion.descripcion}
            </p>
            <p class="time">${notificacion.tiempo}</p>
          </div>
        </div>
        <div class="box-img">
          <a href="#" class="delete" data-id="${notificacion.id}">
            <img src="../assets/logos/eliminar.png" alt="eliminar" class="user-pic-pic" />
          </a>
        </div>
      `;

      container.appendChild(card);

      // Evento para eliminar notificación
      const deleteBtn = card.querySelector(".delete");
      deleteBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        const notificacionId = deleteBtn.getAttribute("data-id");
        await eliminarNotificacion(notificacionId);
      });
    });
  } catch (error) {
    console.error("Error al cargar notificaciones:", error);
  }
}

// Función para eliminar una notificación
async function eliminarNotificacion(id) {
  try {
    const response = await fetch(`${urlDeleteNotificacion}/${id}`, {
      method: "DELETE",
    });
    if (response.ok) {
      console.log("Notificación eliminada");
      card.remove(); // Elimina la tarjeta del DOM
    } else {
      console.error("Error al eliminar notificación");
    }
  } catch (error) {
    console.error("Error al eliminar notificación:", error);
  }
}

// Llama a la función para cargar notificaciones cuando la página cargue
window.addEventListener("DOMContentLoaded", cargarNotificaciones);
