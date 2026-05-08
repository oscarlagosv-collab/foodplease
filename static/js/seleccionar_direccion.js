document.addEventListener("DOMContentLoaded", function () {

    const direccionInput = document.getElementById("direccionInput");
    const comunaInput = document.getElementById("comunaInput");
    const regionInput = document.getElementById("regionInput");
    const sugerencias = document.getElementById("sugerenciasDireccion");
    const confirmarBtn = document.getElementById("confirmarDireccion");

    let direccionSeleccionada = false;

    // BUSCAR DIRECCIONES
    direccionInput.addEventListener("input", async function () {

        const query = direccionInput.value.trim();

        direccionSeleccionada = false;

        if (query.length < 3) {
            sugerencias.innerHTML = "";
            return;
        }

        try {

            const response = await fetch(
                `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&countrycodes=cl&addressdetails=1&limit=5`
            );

            const data = await response.json();

            sugerencias.innerHTML = "";

            data.forEach(lugar => {

                const item = document.createElement("div");

                item.classList.add("item-sugerencia");

                item.textContent = lugar.display_name;

                item.addEventListener("click", function () {

                    direccionInput.value = lugar.display_name;

                    // COMUNA
                    comunaInput.value =
                        lugar.address.city ||
                        lugar.address.town ||
                        lugar.address.village ||
                        lugar.address.suburb ||
                        "";

                    // REGIÓN
                    regionInput.value =
                        lugar.address.state ||
                        "";

                    sugerencias.innerHTML = "";

                    direccionSeleccionada = true;
                });

                sugerencias.appendChild(item);
            });

        } catch (error) {
            console.error(error);
        }
    });

    // CONFIRMAR DIRECCIÓN
    confirmarBtn.addEventListener("click", function () {

        const direccion = direccionInput.value.trim();
        const comuna = comunaInput.value.trim();
        const region = regionInput.value.trim();

        if (
            !direccion ||
            !comuna ||
            !region ||
            !direccionSeleccionada
        ) {
            alert("Debes seleccionar una dirección válida.");
            return;
        }

        // Guardar datos
        localStorage.setItem("direccionCliente", direccion);
        localStorage.setItem("comunaCliente", comuna);
        localStorage.setItem("regionCliente", region);
        localStorage.removeItem("modoVitrina");

        // Redireccionar
        window.location.href =
            `/principal/?comuna=${encodeURIComponent(comuna)}`;
    });
});