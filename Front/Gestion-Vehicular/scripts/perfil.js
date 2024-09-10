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
