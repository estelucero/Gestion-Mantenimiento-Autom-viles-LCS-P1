//Obtener todas las petentes
// Hacer la solicitud al endpoint
if (usuarioSesion.esParticular) {
  fetch(
    `https://back-gestion-p1.vercel.app/users/obtenerVehiculosParticular?cuilDueño=${encodeURIComponent(
      usuarioSesion.cuil
    )}`
  )
    .then((response) => response.json()) // Convierte la respuesta a JSON
    .then((data) => {
      // Guarda los datos en localStorage
      const patentes = data.map((vehiculo) => vehiculo.patente);

      // Guarda las patentes en localStorage
      localStorage.setItem("patentes", JSON.stringify(patentes));
    })
    .catch((error) => {
      console.error("Error al recuperar los datos:", error);
    });
} else {
  fetch(
    `https://back-gestion-p1.vercel.app/users/obtenerVehiculosOrganizacion?cuitDueño=${encodeURIComponent(
      usuarioSesion.cuit
    )}`
  )
    .then((response) => response.json()) // Convierte la respuesta a JSON
    .then((data) => {
      // Guarda los datos en localStorage
      const patentes = data.map((vehiculo) => vehiculo.patente);

      // Guarda las patentes en localStorage
      localStorage.setItem("patentes", JSON.stringify(patentes));
    })
    .catch((error) => {
      console.error("Error al recuperar los datos:", error);
    });
}

const obtenerPatentes = () => {
  return JSON.parse(localStorage.getItem("patentes") || "[]");
};

// Función para verificar si hay notificaciones para una patente
const hayNotificacionesParaPatenteParticular = async (patente) => {
  try {
    const response = await fetch(
      `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesSinLeerParticular?patente=${patente}`
    );
    const data = await response.json();
    return data && data.length > 0; // Devuelve true si hay notificaciones
  } catch (error) {
    console.error(
      `Error al obtener notificaciones para la patente ${patente}:`,
      error
    );
    return false;
  }
};

//
const hayNotificacionesParaPatenteOrganizacion = async (patente) => {
  try {
    const response = await fetch(
      `https://back-gestion-p1.vercel.app/users/obtenerNotificacionesSinLeerOrganizacion?patente=${patente}`
    );
    const data = await response.json();
    return data && data.length > 0; // Devuelve true si hay notificaciones
  } catch (error) {
    console.error(
      `Error al obtener notificaciones para la patente ${patente}:`,
      error
    );
    return false;
  }
};

// Función principal para verificar todas las patentes
const verificarNotificaciones = async () => {
  const patentes = obtenerPatentes();
  const logoAlerta = document.getElementById("logo-alerta");
  if (patentes.length === 0) {
    console.log("No hay patentes en localStorage");
    return false;
  }
  if (usuarioSesion.esParticular) {
    for (const patente of patentes) {
      const hayNotificaciones = await hayNotificacionesParaPatenteParticular(
        patente
      );

      if (hayNotificaciones) {
        logoAlerta.src = "../assets/logos/notificacionLLegada.png";
        document.getElementById("logo-alerta2").src =
          "../assets/logos/notificacionLLegada.png";
        console.log(`Hay notificaciones para la patente ${patente}`);
        return true; // Salir si se encuentra al menos una notificación
      }
    }
  } else {
    for (const patente of patentes) {
      const hayNotificaciones = await hayNotificacionesParaPatenteOrganizacion(
        patente
      );

      if (hayNotificaciones) {
        logoAlerta.src = "../assets/logos/notificacionLLegada.png";
        document.getElementById("logo-alerta2").src =
          "../assets/logos/notificacionLLegada.png";
        console.log(`Hay notificaciones para la patente ${patente}`);
        return true; // Salir si se encuentra al menos una notificación
      }
    }
  }

  console.log("No hay notificaciones sin leer");
  return false;
};

verificarNotificaciones();
setInterval(() => {
  verificarNotificaciones();
}, 10000);
