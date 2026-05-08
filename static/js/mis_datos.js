document.addEventListener("DOMContentLoaded", function () {
    const btnModificar = document.getElementById("btnModificarDatos");
    const btnGuardar = document.getElementById("btnGuardarDatos");
    const form = document.getElementById("formMisDatos");

    const btnEliminar = document.getElementById("btnEliminarUsuario");
    const modalEliminar = document.getElementById("modalEliminarUsuario");
    const btnCancelar = document.getElementById("btnCancelarEliminar");

    if (btnModificar) {
        btnModificar.addEventListener("click", function () {
            const inputs = form.querySelectorAll("input");

            inputs.forEach(input => {
                input.removeAttribute("readonly");
            });

            const passwordInput = form.querySelector('input[name="password"]');
            passwordInput.value = "";
            passwordInput.placeholder = "Nueva contraseña";

            btnModificar.style.display = "none";
            btnGuardar.style.display = "inline-block";
        });
    }

    if (btnEliminar) {
        btnEliminar.addEventListener("click", function () {
            modalEliminar.style.display = "flex";
        });
    }

    if (btnCancelar) {
        btnCancelar.addEventListener("click", function () {
            modalEliminar.style.display = "none";
        });
    }
});