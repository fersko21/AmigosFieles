function validarForm2() {
    var form = document.getElementById("formulario");
    var inputs = form.querySelectorAll("input, select");
    var errorDiv = document.querySelector(".informeError");
    var error = false;
    var errorMessage = "";
  
    for (var i = 0; i < inputs.length; i++) {
      var input = inputs[i];
  
      // Validación de los inputs
      if (input.value.trim() === "") {
        error = true;
        errorMessage += "- El campo " + input.name + " no puede estar vacío.<br>";
      }
          // Validación de rut
if (input.name === "rut") {
    if (!/^(\d{1,3}(?:\.\d{1,3}){2}-[\dkK])$/.test(input.value.trim())) {
      error = true;
      errorMessage += "- El rut ingresado no es válido.<br>";
    }
  }
      
    }

  
    if (error) {
      errorDiv.innerHTML = errorMessage;
      event.preventDefault();
    }
  } 