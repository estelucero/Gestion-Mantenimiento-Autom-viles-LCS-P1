document.getElementById("searchButton").addEventListener("click", function () {
  const inputValue = document.getElementById("patenteInput").value.toLowerCase();
  const vehiculos = JSON.parse(localStorage.getItem("autos")) || [];

  const vehiculosFiltrados = vehiculos.filter((vehiculo) =>
    vehiculo.patente.toLowerCase().includes(inputValue)
  );
  console.log(vehiculosFiltrados);

  const sectionCard = document.querySelector(".section-card .wrapper .notifications");

  const tarjetasVehiculos = sectionCard.querySelectorAll(".single-box");
  tarjetasVehiculos.forEach((tarjeta) => tarjeta.remove());

  if (vehiculosFiltrados.length > 0) {
    vehiculosFiltrados.forEach((vehiculo) => {
      const divAuto = document.createElement("div");
      divAuto.classList.add("single-box");
      divAuto.innerHTML = `
        <div class="box-avatar-text">
          <div class="avatar">
            <img src="../assets/imagenes/corolla.png" alt="perfil-imagen" />
          </div>
          <div class="box-text">
            <div class="text-patente">
              <p class="patente-p">${vehiculo.patente.toUpperCase()}</p>
            </div>
            <div class="text-flex">
              Marca: <p>${vehiculo.marca.charAt(0).toUpperCase() + vehiculo.marca.slice(1).toLowerCase()}</p>
            </div>
            <div class="text-flex">
              Modelo: <p>${vehiculo.modelo.charAt(0).toUpperCase() + vehiculo.modelo.slice(1).toLowerCase()}</p>
            </div>
            <div class="text-flex">
              Año de Fabricación: <p>${new Date(vehiculo.fechaFabricacion).getFullYear()}</p>
            </div>
          </div>
        </div>
        <div class="box-img">
          <a href="../views/auto.html">
            <img src="../assets/logos/edit-solid-24.png" alt="Editar" class="user-pic-pic" />
          </a>
          <img src="../assets/logos/eliminar.png" alt="Eliminar" class="user-pic-pic eliminar-auto" />
        </div>
      `;

      sectionCard.appendChild(divAuto);
    });
  } else {
    const mensaje = document.createElement("p");
    mensaje.textContent = "No se encontraron vehículos con esa patente.";
    sectionCard.appendChild(mensaje);
  }
});
