document.getElementById("tipoConta").addEventListener("change", function () {
    const tipo = this.value;
    document.getElementById("camposCliente").style.display = tipo === "cliente" ? "block" : "none";
    document.getElementById("camposProfissional").style.display = tipo === "profissional" ? "block" : "none";
});

// Esconde os campos inicialmente
document.getElementById("camposCliente").style.display = "none";
document.getElementById("camposProfissional").style.display = "none";