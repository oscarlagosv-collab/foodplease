function abrirUbicacion() {
    document.getElementById("modalUbicacion").style.display = "block";
}

function cerrarUbicacion() {
    document.getElementById("modalUbicacion").style.display = "none";
}

function buscarDireccion() {
    let direccion = document.getElementById("direccion").value;
    let sugerencias = document.getElementById("sugerencias");

    if (direccion.length < 3) {
        sugerencias.innerHTML = "";
        return;
    }

    sugerencias.innerHTML = `
        <p>📍 ${direccion}, Santiago</p>
        <p>📍 ${direccion}, Providencia</p>
        <p>📍 ${direccion}, Maipú</p>
    `;
}

function usarLocalizacionActual() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            let latitud = position.coords.latitude;
            let longitud = position.coords.longitude;

            document.getElementById("resultadoUbicacion").innerHTML =
                "Ubicación detectada: Lat " + latitud + ", Lon " + longitud;
        });
    } else {
        alert("Tu navegador no permite geolocalización.");
    }
}