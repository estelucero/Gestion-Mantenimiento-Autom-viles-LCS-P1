// document.getElementById("searchButton").addEventListener("click", function () {
//   const inputValue = document.getElementById("patenteInput").value.toLowerCase();
//   const vehiculos = JSON.parse(localStorage.getItem("autos")) || [];

//   // Filtrar vehículos por patente
//   const vehiculosFiltrados = vehiculos.filter((vehiculo) =>
//     vehiculo.patente.toLowerCase().includes(inputValue)
//   );
//   console.log(vehiculosFiltrados);
//   // Limpiar la sección de tarjetas
//   const sectionCard = document.querySelector(".section-card .wrapper .notifications");
//   sectionCard.innerHTML = "";

//   if (vehiculosFiltrados.length > 0) {
//     vehiculosFiltrados.forEach((vehiculos) => {
//       // Crear la tarjeta del vehículo
//       const divAuto = document.createElement("div");
//       divAuto.classList.add("single-box");
//       divAuto.innerHTML = `
//     <div class="box-avatar-text">
//       <div class="avatar">
//         <img
//           src="../assets/imagenes/corolla.png"
//           alt="perfil-imagen"
//         />
//       </div>
//       <div class="box-text">
//         <div class="text-patente">
//           <p class="patente-p">${vehiculos.patente.toUpperCase()}</p>
//         </div>
//         <div class="text-flex">
//           Marca:
//           <p>${vehiculos.marca.charAt(0).toUpperCase() +
//         vehiculos.marca.slice(1).toLowerCase()
//         }</p>
//         </div>
//         <div class="text-flex">
//           Modelo:
//           <p>${vehiculos.modelo.charAt(0).toUpperCase() +
//         vehiculos.modelo.slice(1).toLowerCase()
//         }</p>
//         </div>
//         <div class="text-flex">
//           Año de Fabricación:
//           <p>${new Date(vehiculos.fechaFabricacion).getFullYear()}</p>
//         </div>
//       </div>
//     </div>
//     <div class="box-img">
//       <a href="../views/auto.html">
//         <img
//           src="../assets/logos/edit-solid-24.png"
//           alt="Editar"
//           class="user-pic-pic"
//         />
//       </a>
//       <img
//         src="../assets/logos/eliminar.png"
//         alt="Eliminar"
//         class="user-pic-pic eliminar-auto"
//       />
//     </div>
//   `;
//       divAuto.addEventListener("click", () => {
//         localStorage.setItem("autoSeleccionado", JSON.stringify(vehiculos));
//         console.log(`Auto ${vehiculos.patente} guardado en el localStorage`);
//       });

//       // Agregar evento para guardar en localStorage cuando se haga clic en la tarjeta
//       divAuto.addEventListener("click", () => {
//         localStorage.setItem("autoSeleccionado", JSON.stringify(auto));
//         console.log(`Auto ${vehiculos.patente} guardado en el localStorage`);
//       });

//       // Seleccionar el ícono de eliminar y añadir un evento para la solicitud de eliminación
//       const eliminarIcon = divAuto.querySelector(".eliminar-auto");
//       eliminarIcon.addEventListener("click", async (event) => {
//         event.stopPropagation(); // Evita que el click se propague al evento de la tarjeta

//         // Confirmar antes de eliminar
//         const confirmacion = confirm(
//           `¿Estás seguro de que quieres eliminar el vehículo con patente ${vehiculos.patente}?`
//         );
//         if (!confirmacion) return;

//         try {
//           const response = await fetch(
//             `https://back-gestion-p1.vercel.app/users/eliminarVehiculoUsuarioParticular?patente=${vehiculos.patente}`,
//             {
//               method: "DELETE",
//               headers: {
//                 "Content-Type": "application/json",
//               },
//             }
//           );

//           if (response.ok) {
//             console.log(
//               `Vehículo con patente ${vehiculos.patente} eliminado con éxito`
//             );

//             // Opcionalmente, eliminar la tarjeta del DOM
//             divAuto.remove();
//             window.location.reload();
//           } else {
//             const errorData = await response.json();
//             console.error("Error al eliminar el vehículo:", errorData);
//           }
//         } catch (error) {
//           console.error(
//             "Hubo un problema con la solicitud de eliminación:",
//             error
//           );
//         }
//       });

//       // Añadir la tarjeta a la sección
//       sectionCard.appendChild(divAuto);
//     });
//   } else {
//     sectionCard.innerHTML = "<p>No se encontraron vehículos con esa patente.</p>";
//   }
// });


document.getElementById("searchButton").addEventListener("click", function () {
  const inputValue = document.getElementById("patenteInput").value.toLowerCase();
  const vehiculos = JSON.parse(localStorage.getItem("autos")) || [];

  // Filtrar vehículos por patente
  const vehiculosFiltrados = vehiculos.filter((vehiculo) =>
    vehiculo.patente.toLowerCase().includes(inputValue)
  );
  console.log(vehiculosFiltrados);

  // Limpiar la sección de tarjetas
  const sectionCard = document.querySelector(".section-card .wrapper .notifications");
  sectionCard.innerHTML = "";

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

      // Guardar en localStorage cuando se haga clic en la tarjeta
      divAuto.addEventListener("click", () => {
        localStorage.setItem("autoSeleccionado", JSON.stringify(vehiculo));
        console.log(`Auto ${vehiculo.patente} guardado en el localStorage`);
      });

      // Seleccionar el ícono de eliminar y añadir un evento para la solicitud de eliminación
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
            // Eliminar la tarjeta del DOM
            divAuto.remove();
          } else {
            const errorData = await response.json();
            console.error("Error al eliminar el vehículo:", errorData);
          }
        } catch (error) {
          console.error("Hubo un problema con la solicitud de eliminación:", error);
        }
      });

      // Añadir la tarjeta a la sección
      sectionCard.appendChild(divAuto);
    });
  } else {
    sectionCard.innerHTML = "<p>No se encontraron vehículos con esa patente.</p>";
  }
});
