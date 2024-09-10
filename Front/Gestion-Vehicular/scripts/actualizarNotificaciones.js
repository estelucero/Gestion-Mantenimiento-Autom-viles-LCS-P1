async function gestionarRevisiones() {
  const urlPostGenerar =
    "https://back-gestion-p1.vercel.app/users/generarRevisionesVencidas";
  const urlPutVerificar =
    "https://back-gestion-p1.vercel.app/users/verificarYActualizarRevisionesAVencer";

  try {
    // Llamada al método POST para generar revisiones vencidas
    const responsePost = await fetch(urlPostGenerar, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        // Aquí puedes agregar el body si se requiere para el POST
      }),
    });

    if (!responsePost.ok) {
      throw new Error(`Error en POST: ${responsePost.statusText}`);
    }

    const dataPost = await responsePost.json();
    console.log("Revisiones vencidas generadas:", dataPost);

    // Llamada al método PUT para verificar y actualizar revisiones
    const responsePut = await fetch(urlPutVerificar, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        // Aquí puedes agregar el body si se requiere para el PUT
      }),
    });

    if (!responsePut.ok) {
      throw new Error(`Error en PUT: ${responsePut.statusText}`);
    }

    const dataPut = await responsePut.json();
    console.log("Revisiones a vencer verificadas y actualizadas:", dataPut);
  } catch (error) {
    console.error("Error gestionando revisiones:", error);
  }
}

gestionarRevisiones();
setInterval(() => {
  gestionarRevisiones();
}, 50000);
