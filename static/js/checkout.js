document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("direccionCheckout");
    const sugerencias = document.getElementById("sugerenciasCheckout");
    const comuna = document.getElementById("comunaCheckout");
    const region = document.getElementById("regionCheckout");

    let temporizador = null;

    input.addEventListener("input", function () {
        clearTimeout(temporizador);

        const texto = input.value.trim();

        sugerencias.innerHTML = "";
        comuna.value = "";
        region.value = "";

        if (texto.length < 4) return;

        temporizador = setTimeout(() => {
            buscarDireccion(texto);
        }, 700);
    });

    async function buscarDireccion(texto) {
        const url = `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&countrycodes=cl&limit=5&q=${encodeURIComponent(texto)}`;

        try {
            const respuesta = await fetch(url);
            const datos = await respuesta.json();

            sugerencias.innerHTML = "";

            datos.forEach(item => {
                const opcion = document.createElement("div");
                opcion.classList.add("opcion-direccion");
                opcion.textContent = item.display_name;

                opcion.addEventListener("click", function () {
                    input.value = item.display_name;

                    const address = item.address || {};

                    comuna.value =
                        address.city ||
                        address.town ||
                        address.village ||
                        address.municipality ||
                        address.county ||
                        "";

                    region.value =
                        address.state ||
                        address.region ||
                        "";

                    sugerencias.innerHTML = "";
                });

                sugerencias.appendChild(opcion);
            });

        } catch (error) {
            console.error("Error buscando dirección:", error);
        }
    }
});