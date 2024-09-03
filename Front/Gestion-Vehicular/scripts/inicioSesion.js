const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn1 = document.querySelector("#sign-up-btn-p");
const sign_up_btn2 = document.querySelector("#sign-up-btn-e");
const sign_up_p = document.getElementById("form-particular");
const sign_up_e = document.getElementById("form-entidad");
const container = document.querySelector(".sec-container");

sign_up_btn1.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
  sign_up_e.style.display = "none";
});
sign_up_btn2.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
  sign_up_p.style.display = "none";
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
  sign_up_e.style.display = "flex";
  sign_up_p.style.display = "flex";
});

//Logica de Registro Particular
document
  .getElementById("form-particular")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera tradicional
    const nombre = document.getElementById("nombre").value;
    const apellido = document.getElementById("apellido").value;
    const dni = document.getElementById("dni").value;
    const cuil = document.getElementById("cuil").value;
    const mail = document.getElementById("mail").value;
    const contrasena = document.getElementById("contrasena").value;

    // Aquí puedes enviar los datos a un servidor utilizando fetch o XMLHttpRequest
    // Ejemplo utilizando fetch:
    fetch("http://192.168.1.37:9090/users/registroUsuarioParticular", {
      // Reemplaza con la URL de tu servidor
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nombre: nombre,
        apellido: apellido,
        dni: dni,
        email: mail,
        contraseña: contrasena,
        cuil: cuil,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Formulario enviado exitosamente!");
        console.log(data);
      })
      .catch((error) => {
        alert("Hubo un problema al enviar el formulario.");
        console.error(error);
      });
  });
//Logica de Registro Entidad
document
  .getElementById("form-entidad")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera tradicional
    const nombre = document.getElementById("nombre-entidad").value;
    const apellido = document.getElementById("apellido-entidad").value;
    const dni = document.getElementById("dni-entidad").value;
    const cuit = document.getElementById("cuit").value;
    const mail = document.getElementById("mail-entidad").value;
    const contrasena = document.getElementById("contrasena-entidad").value;

    // Aquí puedes enviar los datos a un servidor utilizando fetch o XMLHttpRequest
    // Ejemplo utilizando fetch:
    fetch("http://192.168.1.37:9090/users/registroUsuarioOrganizacion", {
      // Reemplaza con la URL de tu servidor
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        razonSocial: nombre,
        email: mail,
        contraseña: contrasena,
        cuit: cuit,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Formulario enviado exitosamente!");
        console.log(data);
      })
      .catch((error) => {
        alert("Hubo un problema al enviar el formulario.");
        console.error(error);
      });
  });
//Logica de inicion de sesion
document
  .getElementById("inicio-sesion-form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Evita el envío del formulario

    const mail = document.getElementById("mail-inicio-sesion").value;
    const password = document.getElementById("password-inicio-sesion").value;

    if (validateEmail(mail) && password.length > 0) {
      // Llama al servidor para verificar las credenciales
      fetch(
        `http://192.168.1.37:9090/users/verificarLogeoExitosoUsuarioParticular?email=${encodeURIComponent(
          mail
        )}&password=${encodeURIComponent(password)}`
      )
        .then((response) => {
          if (!response.ok) {
            throw new Error("Error en la solicitud: " + response.statusText);
          }
          return response.json(); // Asumiendo que el servidor responde con JSON
        })
        .then((data) => {
          if (data.response == true) {
            // Redirigir al usuario si la autenticación es exitosa
            window.location.href = "../views/inicio.html";
          } else {
            fetch(
              `http://192.168.1.37:9090/users/verificarLogeoExitosoUsuarioOrganizacion?email=${encodeURIComponent(
                mail
              )}&password=${encodeURIComponent(password)}`
            )
              .then((response) => {
                if (!response.ok) {
                  throw new Error(
                    "Error en la solicitud: " + response.statusText
                  );
                }
                return response.json(); // Asumiendo que el servidor responde con JSON
              })
              .then((data) => {
                if (data.response == true) {
                  // Redirigir al usuario si la autenticación es exitosa
                  window.location.href = "../views/inicio.html";
                } else {
                  alert("Email o Contraseña erronea");
                }
              })
              .catch((error) => {
                console.error("Error:", error);
                alert(
                  "Hubo un problema con la autenticación. Inténtalo nuevamente."
                );
              });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Hubo un problema con la autenticación. Inténtalo nuevamente.");
        });
    } else {
      alert("Por favor, ingresa un correo y contraseña válidos.");
    }
  });

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}
