document.addEventListener("DOMContentLoaded", function () {
  const tipoContaSelect = document.getElementById("tipoConta");
  const camposCliente = document.getElementById("camposCliente");
  const camposProfissional = document.getElementById("camposProfissional");

  tipoContaSelect.addEventListener("change", function () {
    const tipo = this.value;
    camposCliente.style.display = tipo === "cliente" ? "block" : "none";
    camposProfissional.style.display = tipo === "profissional" ? "block" : "none";
  });

  // Esconde os campos inicialmente
  camposCliente.style.display = "none";
  camposProfissional.style.display = "none";
});
