const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn1 = document.querySelector("#sign-up-btn-p");
const sign_up_btn2 = document.querySelector("#sign-up-btn-e");
const sign_up_p = document.getElementById("form-particular");
const sign_up_e = document.getElementById("form-entidad");
const container = document.querySelector(".sec-container");

const nombreApellidoRegex = /^[A-Za-z]+$/;
const dniRegex = /^[0-9]{7,8}$/;
const cuilRegex = /^[0-9]{2}-[0-9]{7,8}-[0-9]$/;
const cuitRegex = /^[0-9]{2}-[0-9]{8}-[0-9]$/;
const mailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const contrasenaRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{7,}$/;

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
function registrarParticular() {
  // Evita que el formulario se envíe de manera tradicional
  const nombre = document.getElementById("nombre").value;
  const apellido = document.getElementById("apellido").value;
  const dni = document.getElementById("dni").value;
  const cuil = document.getElementById("cuil").value;
  const mail = document.getElementById("mail").value;
  const contrasena = document.getElementById("contrasena").value;

  // Aquí puedes enviar los datos a un servidor utilizando fetch o XMLHttpRequest
  // Ejemplo utilizando fetch:
  fetch("https://back-gestion-p1.vercel.app/users/registroUsuarioParticular", {
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
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      return response.json();
    })
    .then((data) => {
      alert("Formulario enviado exitosamente!");
      console.log(data);
      window.location.href = "../views/inicioSesion.html";
    })
    .catch((error) => {
      alert("Hubo un problema al enviar el formulario.");
      console.error(error);
    });

  //Logica de Registro Entidad
  // document
  //   .getElementById("form-entidad")
  //   .addEventListener("submit", function (event) {
  //     event.preventDefault(); // Evita que el formulario se envíe de manera tradicional
  //     const nombre = document.getElementById("nombre-entidad").value;
  //     const cuit = document.getElementById("cuit").value;
  //     const mail = document.getElementById("mail-entidad").value;
  //     const contrasena = document.getElementById("contrasena-entidad").value;

  //     // Aquí puedes enviar los datos a un servidor utilizando fetch o XMLHttpRequest
  //     // Ejemplo utilizando fetch:
  //     fetch(
  //       "https://back-gestion-p1.vercel.app/users/registroUsuarioOrganizacion",
  //       {
  //         // Reemplaza con la URL de tu servidor
  //         method: "POST",
  //         headers: {
  //           "Content-Type": "application/json",
  //         },
  //         body: JSON.stringify({
  //           razonSocial: nombre,
  //           email: mail,
  //           contraseña: contrasena,
  //           cuit: cuit,
  //         }),
  //       }
  //     )
  //       .then((response) => response.json())
  //       .then((data) => {
  //         alert("Formulario enviado exitosamente!");
  //         console.log(data);
  //       })
  //       .catch((error) => {
  //         alert("Hubo un problema al enviar el formulario.");
  //         console.error(error);
  //       });
  //   });
}

function registrarEntidad() {
  const nombre = document.getElementById("nombre-entidad").value;
  const cuit = document.getElementById("cuit").value;
  const mail = document.getElementById("mail-entidad").value;
  const contrasena = document.getElementById("contrasena-entidad").value;

  // Aquí puedes enviar los datos a un servidor utilizando fetch o XMLHttpRequest
  // Ejemplo utilizando fetch:
  fetch(
    "https://back-gestion-p1.vercel.app/users/registroUsuarioOrganizacion",
    {
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
    }
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      return response.json();
    })
    .then((data) => {
      alert("Formulario enviado exitosamente!");
      console.log(data);
      window.location.href = "../views/inicioSesion.html";
    })
    .catch((error) => {
      alert("Hubo un problema al enviar el formulario.");
      console.error(error);
    });
}
//Logica de inicion de sesion
/*document
  .getElementById("inicio-sesion-form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); 

    const mail = document.getElementById("mail-inicio-sesion").value;
    const password = document.getElementById("password-inicio-sesion").value;

    if (validateEmail(mail) && password.length > 0) {
      // Llama al servidor para verificar las credenciales
      fetch(
        `https://back-gestion-p1.vercel.app/users/verificarLogeoExitosoUsuarioParticular?email=${encodeURIComponent(
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
          if (data.esParticular == true) {
            // Redirigir al usuario si la autenticación es exitosa
            localStorage.setItem("usuario", JSON.stringify(data));
            window.location.href = "../views/inicio.html";
          } else {
            fetch(
              `https://back-gestion-p1.vercel.app/users/verificarLogeoExitosoUsuarioOrganizacion?email=${encodeURIComponent(
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
                if (data.esParticular == false) {
                  localStorage.setItem("usuario", JSON.stringify(data));
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
  });*/

function iniciarSesion() {
  const mail = document.getElementById("mail-inicio-sesion").value;
  const password = document.getElementById("password-inicio-sesion").value;
  fetch(
    `https://back-gestion-p1.vercel.app/users/verificarLogeoExitosoUsuarioParticular?email=${encodeURIComponent(
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
      if (data.esParticular == true) {
        // Redirigir al usuario si la autenticación es exitosa
        localStorage.setItem("usuario", JSON.stringify(data));
        window.location.href = "../views/inicio.html";
      } else {
        fetch(
          `https://back-gestion-p1.vercel.app/users/verificarLogeoExitosoUsuarioOrganizacion?email=${encodeURIComponent(
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
            if (data.esParticular == false) {
              localStorage.setItem("usuario", JSON.stringify(data));
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
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

// Función para mostrar errores usando id
function mostrarError(input, mensaje, feedbackId) {
  input.classList.add("is-invalid");
  input.classList.remove("is-valid");
  const errorElement = document.getElementById(feedbackId);
  errorElement.style.display = "block";
  errorElement.textContent = mensaje;
}

function mostrarExito(input, successId) {
  input.classList.remove("is-invalid");
  input.classList.add("is-valid");
  const successElement = document.getElementById(successId);
  successElement.style.display = "none";
}

function validarCampo(input, regex, mensaje, feedbackId) {
  if (!regex.test(input.value.trim())) {
    mostrarError(input, mensaje, feedbackId);
    return false;
  } else {
    mostrarExito(input, feedbackId);
    return true;
  }
}

function validarCuil() {
  const dni = document.getElementById("dni").value.trim();
  const cuil = document.getElementById("cuil");

  if (!cuilRegex.test(cuil.value.trim())) {
    mostrarError(
      cuil,
      "El CUIL debe tener el formato XX-XXXXXXX-X",
      "cuilFeedback"
    );
    return false;
  }

  const partesCuil = cuil.value.split("-");
  if (partesCuil[1] !== dni) {
    mostrarError(
      cuil,
      "El CUIL no coincide con el DNI ingresado",
      "cuilFeedback"
    );
    return false;
  } else {
    mostrarExito(cuil, "cuilFeedback");
    return true;
  }
}

function validarContrasena() {
  const contrasena = document.getElementById("contrasena");
  const valorContrasena = contrasena.value.trim();
  const tieneLetra = /[A-Za-z]/.test(valorContrasena);
  const tieneNumero = /\d/.test(valorContrasena);

  if (valorContrasena.length < 7) {
    mostrarError(
      contrasena,
      "La contraseña debe tener al menos 7 caracteres",
      "contrasenaFeedback"
    );
    return false;
  }

  if (!tieneLetra) {
    mostrarError(
      contrasena,
      "La contraseña debe contener al menos una letra",
      "contrasenaFeedback"
    );
    return false;
  }

  if (!tieneNumero) {
    mostrarError(
      contrasena,
      "La contraseña debe contener al menos un número",
      "contrasenaFeedback"
    );
    return false;
  }

  mostrarExito(contrasena, "contrasenaFeedback");
  return true;
}

function validarContrasenaEntidad() {
  const contrasena = document.getElementById("contrasena-entidad");
  const valorContrasena = contrasena.value.trim();
  const tieneLetra = /[A-Za-z]/.test(valorContrasena);
  const tieneNumero = /\d/.test(valorContrasena);

  if (valorContrasena.length < 7) {
    mostrarError(
      contrasena,
      "La contraseña debe tener al menos 7 caracteres",
      "contrasenaEntidadFeedback"
    );
    return false;
  }

  if (!tieneLetra) {
    mostrarError(
      contrasena,
      "La contraseña debe contener al menos una letra",
      "contrasenaEntidadFeedback"
    );
    return false;
  }

  if (!tieneNumero) {
    mostrarError(
      contrasena,
      "La contraseña debe contener al menos un número",
      "contrasenaEntidadFeedback"
    );
    return false;
  }

  mostrarExito(contrasena, "contrasenaEntidadFeedback");
  return true;
}

function validarContrasenaSesion() {
  const contrasena = document.getElementById("password-inicio-sesion");
  const valorContrasena = contrasena.value.trim();
  const tieneLetra = /[A-Za-z]/.test(valorContrasena);
  const tieneNumero = /\d/.test(valorContrasena);

  mostrarExito(contrasena, "passwordSesionFeedback");
  return true;
}

function validarFormularioParticular() {
  let isValid = true;

  const nombre = document.getElementById("nombre");
  const apellido = document.getElementById("apellido");
  const dni = document.getElementById("dni");
  const cuil = document.getElementById("cuil");
  const mail = document.getElementById("mail");
  const contrasena = document.getElementById("contrasena");

  isValid =
    validarCampo(
      nombre,
      nombreApellidoRegex,
      "El nombre solo puede contener letras",
      "nombreFeedback"
    ) && isValid;
  isValid =
    validarCampo(
      apellido,
      nombreApellidoRegex,
      "El apellido solo puede contener letras",
      "apellidoFeedback"
    ) && isValid;
  isValid =
    validarCampo(
      dni,
      dniRegex,
      "El DNI debe tener 7 u 8 dígitos",
      "dniFeedback"
    ) && isValid;
  isValid = validarCuil() && isValid;
  isValid =
    validarCampo(
      mail,
      mailRegex,
      "Por favor, ingresa un correo válido",
      "mailFeedback"
    ) && isValid;
  isValid = validarContrasena() && isValid;

  return isValid; // Devuelve el estado final de validación
}

function validarFormularioEntidad() {
  let isValid = true;

  const nombreEntidad = document.getElementById("nombre-entidad");
  const cuit = document.getElementById("cuit");
  const mailEntidad = document.getElementById("mail-entidad");
  const contrasenaEntidad = document.getElementById("contrasena-entidad");

  // Validar nombre de la entidad
  isValid =
    validarCampo(
      nombreEntidad,
      nombreApellidoRegex,
      "El nombre de la entidad solo puede contener letras",
      "nombreEntidadFeedback"
    ) && isValid;

  // Validar CUIT con la expresión regular específica
  isValid =
    validarCampo(
      cuit,
      cuitRegex,
      "El CUIT debe tener el formato XX-XXXXXXXX-X",
      "cuitFeedback"
    ) && isValid;

  // Validar email
  isValid =
    validarCampo(
      mailEntidad,
      mailRegex,
      "Por favor, ingresa un correo válido",
      "mailEntidadFeedback"
    ) && isValid;

  // Validar contraseña
  isValid =
    validarCampo(
      contrasenaEntidad,
      contrasenaRegex,
      "La contraseña debe tener al menos 7 caracteres",
      "contrasenaEntidadFeedback"
    ) && isValid;

  return isValid; // Devuelve el estado final de validación
}

document.querySelectorAll("input").forEach((input) => {
  input.addEventListener("input", function () {
    switch (input.id) {
      case "nombre":
        validarCampo(
          input,
          nombreApellidoRegex,
          "El nombre solo puede contener letras",
          "nombreFeedback"
        );
        break;
      case "apellido":
        validarCampo(
          input,
          nombreApellidoRegex,
          "El apellido solo puede contener letras",
          "apellidoFeedback"
        );
        break;
      case "dni":
        validarCampo(
          input,
          dniRegex,
          "El DNI debe tener 7 u 8 dígitos",
          "dniFeedback"
        );
        break;
      case "cuil":
        validarCuil();
        break;
      case "mail":
        validarCampo(
          input,
          mailRegex,
          "Por favor, ingresa un correo válido",
          "mailFeedback"
        );
        break;
      case "contrasena":
        validarContrasena();
        break;
      case "contrasena-entidad":
        validarContrasenaEntidad();
        break;
      case "nombre-entidad":
        validarCampo(
          input,
          nombreApellidoRegex,
          "El nombre de la entidad solo puede contener letras",
          "nombreEntidadFeedback"
        );
        break;
      case "cuit":
        validarCampo(
          input,
          cuitRegex,
          "El CUIT debe tener el formato XX-XXXXXXXX-X",
          "cuitFeedback"
        );
        break;
      case "mail-entidad":
        validarCampo(
          input,
          mailRegex,
          "Por favor, ingresa un correo válido",
          "mailEntidadFeedback"
        );
        break;
      case "mail-inicio-sesion":
        validarCampo(
          input,
          mailRegex,
          "Por favor, ingresa un correo válido",
          "mailEntidadFeedback"
        );
        break;
      case "password-inicio-sesion":
        validarContrasenaSesion();
        break;
    }
  });
});

document
  .getElementById("form-particular")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Previene el envío del formulario

    const esValidoParticular = validarFormularioParticular(); // Valida todo el formulario

    if (esValidoParticular) {
      registrarParticular();

      // Aquí puedes proceder con el envío del formulario o cualquier otra acción
    } else {
      alert("Por favor, corrige los errores antes de continuar");
    }
  });
document
  .getElementById("form-entidad")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Previene el envío del formulario

    const esValidoEntidad = validarFormularioEntidad();
    if (esValidoEntidad) {
      registrarEntidad();

      // Aquí puedes proceder con el envío del formulario o cualquier otra acción
    } else {
      alert("Por favor, corrige los errores antes de continuar");
    }
  });

function limpiarFormulario() {
  const inputs = document.querySelectorAll(
    "#form-particular input[type='text'], #form-particular input[type='email'], #form-particular input[type='password'], #form-entidad input[type='text'], #form-entidad input[type='email'], #form-entidad input[type='password'], #inicio-sesion-form input[type='text'], #inicio-sesion-form input[type='email'], #inicio-sesion-form input[type='password'"
  );

  // Limpiar todos los inputs (excepto el botón de registro)
  inputs.forEach((input) => {
    input.value = ""; // Limpiar el valor del input
    input.classList.remove("is-valid", "is-invalid"); // Remover las clases de validación
  });

  // Ocultar todos los mensajes de feedback
  const feedbacks = document.querySelectorAll(
    ".invalid-feedback, .valid-feedback"
  );
  feedbacks.forEach((feedback) => {
    feedback.style.display = "none"; // Ocultar los mensajes de error/exito
  });

  // Asegurar que el botón de registro no sea afectado
  const registrarseBtn = document.querySelector(".btn[value='Registrarse']");
  if (registrarseBtn) {
    registrarseBtn.style.display = "block"; // Asegurar que el botón esté visible
  }
}

document.getElementById("sign-in-btn").addEventListener("click", function () {
  limpiarFormulario();
});

document.getElementById("sign-up-btn-p").addEventListener("click", function () {
  limpiarFormulario();
});

document.getElementById("sign-up-btn-e").addEventListener("click", function () {
  limpiarFormulario();
});

// Validación de inicio de sesión
document
  .getElementById("inicio-sesion-form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Evita el envío del formulario

    const mail = document.getElementById("mail-inicio-sesion");
    const password = document.getElementById("password-inicio-sesion");

    let isValid = true;

    // Validar email
    if (!mailRegex.test(mail.value.trim())) {
      mostrarError(
        mail,
        "Por favor, ingresa un correo válido",
        "mailSesionFeedback"
      );
      isValid = false;
    } else {
      mostrarExito(mail, "mailSesionFeedback");
    }

    // Validar contraseña
    if (!contrasenaRegex.test(password.value.trim())) {
      mostrarError(
        password,
        "La contraseña es incorrecta",
        "passwordSesionFeedback"
      );
      isValid = false;
    } else {
      mostrarExito(password, "passwordSesionFeedback");
    }

    if (isValid) {
      // Si es válido, envía la solicitud de inicio de sesión
      iniciarSesion();
    }
  });
localStorage.clear();
