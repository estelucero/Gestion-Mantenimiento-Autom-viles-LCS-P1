// Obtener datos del usuario almacenado en localStorage
const usuario = JSON.parse(localStorage.getItem("usuario"));
console.log(usuario.nombre);
// Verificar si existe el objeto usuario
if (usuarioJSON) {
    // Obtener los elementos con la clase 'nombre-perfil-sesion'
    const nombrePerfilElements = document.querySelectorAll(".nombre-perfil-sesion");

    // Verificar si es una entidad o un usuario particular
    let nombreMostrar = "";

    if (usuarioJSON.tipo === "entidad") {
        nombreMostrar = usuarioJSON.nombreEntidad; // En caso de ser entidad
    } else {
        nombreMostrar = `${usuarioJSON.nombre} ${usuarioJSON.apellido}`; // En caso de ser particular
    }

    // Asignar el nombre a todos los elementos con la clase 'nombre-perfil-sesion'
    nombrePerfilElements.forEach(element => {
        element.textContent = nombreMostrar;
    });
} else {
    console.log("No hay datos de usuario en el localStorage");
}