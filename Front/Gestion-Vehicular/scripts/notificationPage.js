const autos = JSON.parse(localStorage.getItem("patentes") || "[]");
const urlGetNotificacion = `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesSinLeerParticular?patente=`;
const urlDeleteNotificacion = `https://back-gestion-p1.vercel.app/users/marcarNotificacionLeidaPart?idNotif=`;
let subMenu = document.getElementById("subMenu");
function toggleMenu() {
  subMenu.classList.toggle("open-menu");
}

// Función para cargar notificaciones
async function cargarNotificaciones(auto) {
  try {
    const response = await fetch(urlGetNotificacion + `${auto}`);
    const data = await response.json();
    console.log(data);
    const container = document.querySelector(".notifications");
    let contador = 0;
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
              <a href="#" class="name">${notificacion.patente.toUpperCase()}</a> necesita <span class="name">${notificacion.nombre.replace(
        "_",
        " "
      )}</span> para el <span class="name">${notificacion.fechaVence}</span>
            </p>
            
          </div>
        </div>
        <div class="box-img">
          <a href="#" class="delete" data-id="${notificacion.id}">
            <img src="../assets/logos/eliminar.png" alt="eliminar" class="user-pic-pic" />
          </a>
        </div>
      `;

      container.appendChild(card);
      contador++;
      // Evento para eliminar notificación
      const deleteBtn = card.querySelector(".delete");
      deleteBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        const notificacionId = deleteBtn.getAttribute("data-id");
        await eliminarNotificacion(notificacionId, card);
      });
    });
    localStorage.setItem("contadorNotificaciones", contador);
    document.getElementById("num").textContent = contador;
  } catch (error) {
    console.error("Error al cargar notificaciones:", error);
  }
}

// Función para eliminar una notificación
async function eliminarNotificacion(id, card) {
  try {
    const response = await fetch(urlDeleteNotificacion + `${id}`, {
      method: "PUT",
    });
    if (response.ok) {
      console.log("Notificación eliminada");
      card.remove(); // Elimina la tarjeta del DOM
      location.reload(true);
    } else {
      console.error("Error al eliminar notificación");
    }
  } catch (error) {
    console.error("Error al eliminar notificación:", error);
  }
}

// Llama a la función para cargar notificaciones cuando la página cargue
autos.forEach((auto) => cargarNotificaciones(auto));
