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

    const container = document.getElementById("notifications"); // Selecciona el contenedor donde se añadirán los divs

    data.forEach((auto) => {
      console.log(auto);
      const divAuto = document.createElement("div");
      divAuto.classList.add("single-box");

      divAuto.innerHTML = `
    <div class="box-avatar-text">
      <div class="avatar">
        <img
          src="../assets/imagenes/corolla.png"
          alt="perfil-imagen"
        />
      </div>
      <div class="box-text">
        <div class="text-patente">
          <p class="patente-p">${auto.patente}</p>
        </div>
        <div class="text-flex">
          Marca:
          <p>${auto.marca}</p>
        </div>
        <div class="text-flex">
          Modelo:
          <p>${auto.modelo}</p>
        </div>
        <div class="text-flex">
          Año de Fabricación:
          <p>${new Date(auto.fechaFabricacion).getFullYear()}</p>
        </div>
      </div>
    </div>
    <div class="box-img">
      <a href="../views/auto.html">
        <img
          src="../assets/logos/edit-solid-24.png"
          alt="Editar"
          class="user-pic-pic"
        />
      </a>
      <img
        src="../assets/logos/eliminar.png"
        alt="Eliminar"
        class="user-pic-pic"
      />
    </div>
  `;
      divAuto.addEventListener("click", () => {
        localStorage.setItem("autoSeleccionado", JSON.stringify(auto));
        console.log(`Auto ${auto.patente} guardado en el localStorage`);
      });

      container.appendChild(divAuto);
    });
  })
  .catch((error) => {
    console.error("Error:", error);
  });
