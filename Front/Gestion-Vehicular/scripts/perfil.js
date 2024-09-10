// Obtener datos del usuario almacenado en localStorage
const usuarioSesion = JSON.parse(localStorage.getItem("usuario"));
console.log(usuarioSesion.nombre);
// Verificar si existe el objeto usuario
if (usuarioSesion) {
  // Obtener los elementos con la clase 'nombre-perfil-sesion'
  const nombrePerfilElements = document.querySelectorAll(
    ".nombre-perfil-sesion"
  );

  // Verificar si es una entidad o un usuario particular
  let nombreMostrar = "";

  if (usuarioSesion.tipo === "entidad") {
    nombreMostrar = usuarioSesion.nombreEntidad; // En caso de ser entidad
  } else {
    nombreMostrar = `${usuarioSesion.nombre} ${usuarioSesion.apellido}`; // En caso de ser particular
  }

  // Asignar el nombre a todos los elementos con la clase 'nombre-perfil-sesion'
  nombrePerfilElements.forEach((element) => {
    element.textContent = nombreMostrar;
  });
} else {
  console.log("No hay datos de usuario en el localStorage");
}

//Obtener todas las petentes
// Hacer la solicitud al endpoint
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

const obtenerPatentes = () => {
  return JSON.parse(localStorage.getItem("patentes") || "[]");
};

// Función para verificar si hay notificaciones para una patente
const hayNotificacionesParaPatente = async (patente) => {
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

// Función principal para verificar todas las patentes
const verificarNotificaciones = async () => {
  const patentes = obtenerPatentes();
  const logoAlerta = document.getElementById("logo-alerta");
  if (patentes.length === 0) {
    console.log("No hay patentes en localStorage");
    return false;
  }

  for (const patente of patentes) {
    const hayNotificaciones = await hayNotificacionesParaPatente(patente);
    if (hayNotificaciones) {
      logoAlerta.src = "../assets/logos/notificacionLLegada.png";
      console.log(`Hay notificaciones para la patente ${patente}`);
      return true; // Salir si se encuentra al menos una notificación
    }
  }

  console.log("No hay notificaciones sin leer");
  return false;
};
verificarNotificaciones();
setInterval(() => {
  verificarNotificaciones();
}, 10000);
