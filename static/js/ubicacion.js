document.addEventListener("DOMContentLoaded", function () {
    const comuna = localStorage.getItem("comunaCliente");
    const direccion = localStorage.getItem("direccionCliente");
    const region = localStorage.getItem("regionCliente");
    const modoVitrina = localStorage.getItem("modoVitrina");

    const btnComuna = document.getElementById("btnComunaCliente");
    const menuComuna = document.getElementById("menuComuna");
    const direccionActual = document.getElementById("direccionActual");
    const cambiarDireccion = document.getElementById("cambiarDireccion");

    if (!btnComuna) return;

    // CASO 1: Cliente ingresó dirección
    if (comuna && direccion && region) {
        btnComuna.textContent = `📍 ${comuna}`;

        if (direccionActual) {
            direccionActual.textContent = `${direccion}, ${comuna}, ${region}`;
        }

        btnComuna.addEventListener("click", function () {
            if (menuComuna) {
                menuComuna.style.display =
                    menuComuna.style.display === "block" ? "none" : "block";
            }
        });
    }

    // CASO 2: Cliente entró como vitrina
    else if (modoVitrina === "true") {
        btnComuna.textContent = "👀 Vitrineando";

        btnComuna.addEventListener("click", function () {
            localStorage.removeItem("modoVitrina");
            window.location.href = "/";
        });
    }

    // CASO 3: No hay datos
    else {
        btnComuna.textContent = "📍 Dirección";

        btnComuna.addEventListener("click", function () {
            window.location.href = "/";
        });
    }

    if (cambiarDireccion) {
        cambiarDireccion.addEventListener("click", function () {
            localStorage.removeItem("direccionCliente");
            localStorage.removeItem("comunaCliente");
            localStorage.removeItem("regionCliente");
            localStorage.removeItem("modoVitrina");

            window.location.href = "/";
        });
    }
});