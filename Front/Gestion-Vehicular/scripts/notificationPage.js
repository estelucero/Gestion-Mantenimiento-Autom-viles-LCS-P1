const usuario = JSON.parse(localStorage.getItem("usuario"));
const autos = JSON.parse(localStorage.getItem("patentes") || "[]");
const urlGetNotificacion = `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesSinLeerParticular?patente=`;
const urlDeleteNotificacion = `https://back-gestion-p1.vercel.app/users/marcarNotificacionLeidaPart?idNotif=`;
const urlGetNotificacionORG = `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesSinLeerOrganizacion?patente=`;
const urlDeleteNotificacionORG = `https://back-gestion-p1.vercel.app/users/marcarNotificacionLeidaOrg?idNotif=`;
let subMenu = document.getElementById("subMenu");
function toggleMenu() {
  subMenu.classList.toggle("open-menu");
}

// Función para cargar notificaciones
async function cargarNotificacionesParticular(auto) {
  try {
    const response = await fetch(urlGetNotificacion + `${auto}`);
    const data = await response.json();
    console.log(data);
    if (data == false) {
      return;
    }
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
        await eliminarNotificacionParticular(notificacionId, card);
      });
    });
    localStorage.setItem("contadorNotificaciones", contador);
    document.getElementById("num").textContent = contador;
  } catch (error) {
    console.error("Error al cargar notificaciones:", error);
  }
}

// Función para eliminar una notificación
async function eliminarNotificacionParticular(id, card) {
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
if (usuario.esParticular == true) {
  autos.forEach((auto) => cargarNotificacionesParticular(auto));
}

////Eliminar todas
function eliminarTodasParticular() {
  document.getElementById("read").addEventListener("click", function (event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto del enlace

    // Obtener todas las notificaciones
    const notifications = document.querySelectorAll(
      ".notifications .single-box"
    );
    const notificationIds = [];

    notifications.forEach((notification) => {
      // Obtener el id del notification
      const id = notification.id.replace("single-box", ""); // Por ejemplo, si el ID es 'single-box1', obtenemos '1'
      notificationIds.push(id); // Guardamos el ID en el array
    });

    // Para cada notificación, hacer la solicitud PUT al endpoint
    Promise.all(
      notificationIds.map((id) => {
        return fetch(
          `https://back-gestion-p1.vercel.app/users/marcarNotificacionLeidaPart?idNotif=${id}`,
          {
            method: "PUT",
          }
        ).then((response) => {
          if (!response.ok) {
            throw new Error(
              `Error al marcar notificación con id ${id} como leída`
            );
          }
          return response.json();
        });
      })
    )
      .then((results) => {
        // Si todas las solicitudes PUT fueron exitosas, eliminamos visualmente las notificaciones
        notifications.forEach((notification) => {
          notification.remove();
        });

        // Actualizar el contador de notificaciones a 0
        document.getElementById("num").textContent = "0";
        console.log(
          "Todas las notificaciones han sido eliminadas exitosamente"
        );
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Hubo un error al eliminar las notificaciones.");
      });
  });
}
if (usuario.esParticular) {
  eliminarTodasParticular();
}

//Organizacion

// Función para cargar notificaciones
async function cargarNotificacionesOrganizacion(auto) {
  console.log(auto);
  try {
    const response = await fetch(urlGetNotificacionORG + `${auto}`);
    const data = await response.json();
    console.log(data);
    if (!data) {
      return;
    }
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
        await eliminarNotificacionParticular(notificacionId, card);
      });
    });
    localStorage.setItem("contadorNotificaciones", contador);
    document.getElementById("num").textContent = contador;
  } catch (error) {
    console.error("Error al cargar notificaciones:", error);
  }
}

// Función para eliminar una notificación
async function eliminarNotificacionOrganizacion(id, card) {
  try {
    const response = await fetch(urlDeleteNotificacionORG + `${id}`, {
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
if (usuario.esParticular == false) {
  autos.forEach((auto) => cargarNotificacionesOrganizacion(auto));
}

////Eliminar todas
// function eliminarTodasOrganizacion() {
//   document.getElementById("read").addEventListener("click", function (event) {
//     event.preventDefault(); // Prevenir el comportamiento por defecto del enlace

//     // Obtener todas las notificaciones
//     const notifications = document.querySelectorAll(
//       ".notifications .single-box"
//     );
//     const notificationIds = [];
//     console.log(notifications);
//     notifications.forEach((notification) => {
//       // Obtener el id del notification
//       const id = notification.id.replace("single-box", ""); // Por ejemplo, si el ID es 'single-box1', obtenemos '1'
//       notificationIds.push(id); // Guardamos el ID en el array
//     });

//     // Para cada notificación, hacer la solicitud PUT al endpoint
//     Promise.all(
//       notificationIds.map((id) => {
//         return fetch(
//           `https://back-gestion-p1.vercel.app/users/marcarNotificacionLeidaOrg?idNotif=${id}`,
//           {
//             method: "PUT",
//           }
//         ).then((response) => {
//           if (!response.ok) {
//             throw new Error(
//               `Error al marcar notificación con id ${id} como leída`
//             );
//           }
//           return response.json();
//         });
//       })
//     )
//       .then((results) => {
//         // Si todas las solicitudes PUT fueron exitosas, eliminamos visualmente las notificaciones
//         notifications.forEach((notification) => {
//           notification.remove();
//         });

//         // Actualizar el contador de notificaciones a 0
//         document.getElementById("num").textContent = "0";
//         console.log(
//           "Todas las notificaciones han sido eliminadas exitosamente"
//         );
//       })
//       .catch((error) => {
//         console.error("Error:", error);
//         alert("Hubo un error al eliminar las notificaciones.");
//       });
//   });
// }

async function eliminarTodasOrganizacion() {
  document
    .getElementById("read")
    .addEventListener("click", async function (event) {
      event.preventDefault(); // Prevenir el comportamiento por defecto del enlace

      // Obtener todas las notificaciones
      const notifications = document.querySelectorAll(
        ".notifications .single-box"
      );
      const notificationIds = [];
      console.log(notifications);

      notifications.forEach((notification) => {
        // Obtener el id del notification
        const id = notification.id.replace("single-box", ""); // Por ejemplo, si el ID es 'single-box1', obtenemos '1'
        notificationIds.push(id); // Guardamos el ID en el array
      });

      try {
        // Para cada notificación, hacer la solicitud PUT al endpoint de forma secuencial
        for (const id of notificationIds) {
          const response = await fetch(
            `https://back-gestion-p1.vercel.app/users/marcarNotificacionLeidaOrg?idNotif=${id}`,
            {
              method: "PUT",
            }
          );

          if (!response.ok) {
            throw new Error(
              `Error al marcar notificación con id ${id} como leída`
            );
          }
        }

        // Si todas las solicitudes PUT fueron exitosas, eliminamos visualmente las notificaciones
        notifications.forEach((notification) => {
          notification.remove();
        });

        // Actualizar el contador de notificaciones a 0
        document.getElementById("num").textContent = "0";
        console.log(
          "Todas las notificaciones han sido eliminadas exitosamente"
        );
      } catch (error) {
        console.error("Error:", error);
        alert("Hubo un error al eliminar las notificaciones.");
      }
    });
}

if (usuario.esParticular == false) {
  eliminarTodasOrganizacion();
}
