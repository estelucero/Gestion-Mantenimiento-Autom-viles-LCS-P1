document.getElementById("searchButton").addEventListener("click", function() {
    const inputValue = document.getElementById("patenteInput").value.toLowerCase();
    const vehiculos = JSON.parse(localStorage.getItem("autos")) || [];
    
    // Filtrar vehículos por patente
    const vehiculosFiltrados = vehiculos.filter(vehiculo => 
        vehiculo.patente.toLowerCase().includes(inputValue)
    );

    // Limpiar la sección de tarjetas
    const sectionCard = document.querySelector(".section-card .wrapper .notifications");
    sectionCard.innerHTML = "";

    if (vehiculosFiltrados.length > 0) {
        vehiculosFiltrados.forEach(vehiculo => {
            // Crear la tarjeta del vehículo
            const vehicleCard = `
                <div class="single-box">
                    <div class="box-avatar-text">
                        <div class="avatar">
                            <img src="../assets/imagenes/coche-default.png" alt="imagen-vehiculo"/>
                        </div>
                        <div class="box-text">
                            <div class="text-patente">
                                <p class="patente-p">${vehiculo.patente}</p>
                            </div>
                            <div class="text-flex">
                                Marca: <p>${vehiculo.marca}</p>
                            </div>
                            <div class="text-flex">
                                Modelo: <p>${vehiculo.modelo}</p>
                            </div>
                            <div class="text-flex">
                                Año de Fabricación: <p>${vehiculo.fechaFabricacion}</p>
                            </div>
                        </div>
                    </div>
                    <div class="box-img">
                        <a href="../views/auto.html"><img src="../assets/logos/edit-solid-24.png" alt="editar"/></a>
                        <img src="../assets/logos/eliminar.png" alt="eliminar"/>
                    </div>
                </div>
            `;
            sectionCard.innerHTML += vehicleCard;
        });
    } else {
        sectionCard.innerHTML = "<p>No se encontraron vehículos con esa patente.</p>";
    }
});
