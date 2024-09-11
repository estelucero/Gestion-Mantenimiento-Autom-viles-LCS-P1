document.getElementById("searchButton").addEventListener("click", function () {
  const inputValue = document.getElementById("patenteInput").value.toLowerCase();
  const vehiculos = JSON.parse(localStorage.getItem("autos")) || [];

  // Filtrar vehículos por patente
  const vehiculosFiltrados = vehiculos.filter((vehiculo) =>
    vehiculo.patente.toLowerCase().includes(inputValue)
  );
  console.log(vehiculosFiltrados);

  // Obtener la sección donde se mostrarán los vehículos
  const sectionCard = document.querySelector(".section-card .wrapper .notifications");

  // Eliminar solo las tarjetas de vehículos (mantener el botón de agregar auto)
  const tarjetasVehiculos = sectionCard.querySelectorAll(".single-box");
  tarjetasVehiculos.forEach((tarjeta) => tarjeta.remove());

  if (vehiculosFiltrados.length > 0) {
    vehiculosFiltrados.forEach((vehiculo) => {
      // Crear la tarjeta del vehículo
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

      // Añadir la tarjeta a la sección
      sectionCard.appendChild(divAuto);

      // Asignar evento de eliminar después de agregar la tarjeta al DOM
      const eliminarIcon = divAuto.querySelector(".eliminar-auto");
      eliminarIcon.addEventListener("click", async (event) => {
        event.stopPropagation(); // Evita que el click se propague al evento de la tarjeta

        // Confirmar antes de eliminar
        const confirmacion = confirm(`¿Estás seguro de que quieres eliminar el vehículo con patente ${vehiculo.patente}?`);
        if (!confirmacion) return;

        try {
          const response = await fetch(`https://back-gestion-p1.vercel.app/users/eliminarVehiculoUsuarioParticular?patente=${vehiculo.patente}`, {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
          });

          if (response.ok) {
            console.log(`Vehículo con patente ${vehiculo.patente} eliminado con éxito`);
            divAuto.remove(); // Eliminar la tarjeta sin recargar la página
          } else {
            const errorData = await response.json();
            console.error("Error al eliminar el vehículo:", errorData);
            alert("Hubo un problema al eliminar el vehículo.");
          }
        } catch (error) {
          console.error("Hubo un problema con la solicitud de eliminación:", error);
          alert("Error de red al intentar eliminar el vehículo.");
        }
      });
    });
  } else {
    // Si no hay resultados, se muestra este mensaje
    const mensaje = document.createElement("p");
    mensaje.textContent = "No se encontraron vehículos con esa patente.";
    sectionCard.appendChild(mensaje);
  }
});
