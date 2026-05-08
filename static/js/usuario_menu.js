document.addEventListener("DOMContentLoaded", function () {
    const btnUsuario = document.getElementById("btnUsuario");
    const dropdownUsuario = document.getElementById("dropdownUsuario");

    if (btnUsuario && dropdownUsuario) {
        btnUsuario.addEventListener("click", function () {
            dropdownUsuario.style.display =
                dropdownUsuario.style.display === "block" ? "none" : "block";
        });
    }
});