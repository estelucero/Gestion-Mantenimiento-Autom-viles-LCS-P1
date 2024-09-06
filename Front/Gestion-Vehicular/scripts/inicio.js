const usuarioJSON = JSON.parse(localStorage.getItem("usuario"));
let subMenu = document.getElementById("subMenu");
function toggleMenu() {
  subMenu.classList.toggle("open-menu");
}

document.querySelector("#show-car").addEventListener("click", function () {
  document.querySelector(".popup").classList.add("active");
  document.querySelector(".header-desactive").classList.add("active");
  document.querySelector(".popup-container").classList.add("active");
});

document
  .querySelector(".popup .close-btn")
  .addEventListener("click", function () {
    document.querySelector(".popup").classList.remove("active");
    document.querySelector(".header-desactive").classList.remove("active");
    document.querySelector(".popup-container").classList.remove("active");
  });

document
  .querySelector(".btn-form:nth-of-type(2)")
  .addEventListener("click", function () {
    document.querySelector(".popup").classList.remove("active");
    document.querySelector(".header-desactive").classList.remove("active");
    document.querySelector(".popup-container").classList.remove("active");
  });
console.log(usuarioJSON);
//Resgistro de auto
document
  .getElementById("guardar-btn")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    // Captura los valores de los campos
    const patente = document.getElementById("patente").value;
    const modelo = document.getElementById("modelo").value;
    const marca = document.getElementById("marca").value;
    const anioFab = document.getElementById("anio-fab").value;
    const chasis = document.getElementById("chasis").value;
    const km = document.getElementById("km").value;
    const imagen = document.getElementById("imagen").files[0]; // Captura el archivo de imagen

    // Validar que los campos no estén vacíos
    if (!patente || !modelo || !marca || !anioFab || !chasis || !km) {
      alert("Por favor, completa todos los campos.");
      return;
    }

    // Crear un objeto JSON con los datos del formulario
    const data = {
      patente,
      modelo,
      marca,
      fechaFabricacion: anioFab,
      vim: chasis,
      cantKm: parseInt(km, 10),
      cuilDueño: usuarioJSON.cuil, // Asume que usuarioJSON es un objeto global con el cuilDueño
    };

    // Enviar el JSON a la API usando fetch
    fetch(
      "https://back-gestion-p1.vercel.app/users/registrarVehiculoUsuarioParticular",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        alert("Vehículo guardado con éxito");
        // Aquí puedes hacer alguna acción tras el éxito, como redirigir o limpiar el formulario
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Hubo un problema al guardar el vehículo.");
      });
  });

// Realizamos la solicitud GET
fetch(
  `https://back-gestion-p1.vercel.app/users/obtenerVehiculosParticular?cuilDueño=${encodeURIComponent(
    usuarioJSON.cuil
  )}`
)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Error en la solicitud: " + response.statusText);
    }
    return response.json(); // Convertimos la respuesta a JSON
  })
  .then((data) => {
    // Aquí puedes procesar los datos recibidos
    console.log("Vehículos obtenidos:", data);
  })
  .catch((error) => {
    console.error("Error:", error);
  });
