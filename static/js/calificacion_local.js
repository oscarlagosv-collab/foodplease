document.addEventListener("DOMContentLoaded", function () {
    const contenedor = document.querySelector(".estrellas-interactivas");

    if (!contenedor) return;

    const estrellas = contenedor.querySelectorAll("span");
    const localId = contenedor.dataset.localId;
    let calificacionActual = parseInt(contenedor.dataset.calificacion || "0");

    function pintarEstrellas(valor) {
        estrellas.forEach(estrella => {
            const estrellaValor = parseInt(estrella.dataset.valor);

            if (estrellaValor <= valor) {
                estrella.classList.add("activa");
            } else {
                estrella.classList.remove("activa");
            }
        });
    }

    function getCSRFToken() {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith("csrftoken=")) {
                return cookie.substring("csrftoken=".length);
            }
        }

        return "";
    }

    pintarEstrellas(calificacionActual);

    estrellas.forEach(estrella => {
        estrella.addEventListener("mouseenter", function () {
            pintarEstrellas(parseInt(this.dataset.valor));
        });

        estrella.addEventListener("mouseleave", function () {
            pintarEstrellas(calificacionActual);
        });

        estrella.addEventListener("click", async function () {
            const valor = parseInt(this.dataset.valor);

            const formData = new FormData();
            formData.append("estrellas", valor);

            const response = await fetch(`/local/${localId}/calificar/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                },
                body: formData
            });

            const data = await response.json();

            if (data.ok) {
                calificacionActual = valor;
                pintarEstrellas(valor);

                document.getElementById("promedioLocal").textContent = data.promedio;
                document.getElementById("mensajeCalificacion").textContent = "Calificación guardada.";
            }
        });
    });
});