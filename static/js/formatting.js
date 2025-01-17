function formatarTelefone(input) {
    let valor = input.value.replace(/\D/g, "");
    if (valor.length >= 3) {
        valor = valor
            .replace(/^(\d{2})(\d)/, "($1) $2")
            .replace(/(\d{5})(\d)/, "$1-$2");
    }
    input.value = valor;
}

document.getElementById("telefone-input").addEventListener("input", function () {
    formatarTelefone(this);
});