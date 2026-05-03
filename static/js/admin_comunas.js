document.addEventListener("DOMContentLoaded", function () {
    const regionSelect = document.getElementById("id_region");
    const comunaSelect = document.getElementById("id_comuna");

    if (!regionSelect || !comunaSelect) {
        return;
    }

    const comunasPorRegion = {
        "RM": [
            ["Santiago", "Santiago"],
            ["Providencia", "Providencia"],
            ["Maipú", "Maipú"],
            ["Puente Alto", "Puente Alto"],
            ["La Florida", "La Florida"],
            ["Las Condes", "Las Condes"]
        ],
        "V": [
            ["Valparaíso", "Valparaíso"],
            ["Viña del Mar", "Viña del Mar"],
            ["Quilpué", "Quilpué"],
            ["Villa Alemana", "Villa Alemana"]
        ],
        "VI": [
            ["Rancagua", "Rancagua"],
            ["Machalí", "Machalí"],
            ["San Fernando", "San Fernando"]
        ],
        "VII": [
            ["Talca", "Talca"],
            ["Curicó", "Curicó"],
            ["Linares", "Linares"]
        ],
        "VIII": [
            ["Concepción", "Concepción"],
            ["Talcahuano", "Talcahuano"],
            ["Los Ángeles", "Los Ángeles"]
        ],
        "IX": [
            ["Temuco", "Temuco"],
            ["Padre Las Casas", "Padre Las Casas"],
            ["Villarrica", "Villarrica"]
        ]
    };

    function actualizarComunas() {
        const regionSeleccionada = regionSelect.value;
        const comunas = comunasPorRegion[regionSeleccionada] || [];

        comunaSelect.innerHTML = "";

        const opcionInicial = document.createElement("option");
        opcionInicial.value = "";
        opcionInicial.textContent = "Seleccione una comuna";
        comunaSelect.appendChild(opcionInicial);

        comunas.forEach(function (comuna) {
            const option = document.createElement("option");
            option.value = comuna[0];
            option.textContent = comuna[1];
            comunaSelect.appendChild(option);
        });
    }

    regionSelect.addEventListener("change", actualizarComunas);
    actualizarComunas();
});