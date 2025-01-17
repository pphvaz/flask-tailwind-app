document.getElementById('adicionar_cliente').addEventListener('click', async (event) => {
    event.preventDefault();
    const form = document.getElementById('form-contato');
    const formData = new FormData(form);

    const allInputsValid = [...formData.values()].every(value => value.trim() !== '');

    if (!allInputsValid) {
        Swal.fire({
        title: 'Oops!',
        text: "Preencha todos os campos antes de submeter.",
        icon: 'warning',
        confirmButtonText: 'OK'
        });
        return;
    }

    try {
        // Send POST request with form data
        const response = await fetch('lead/cadastrar_lead', {
            method: 'POST',
            body: formData,
        });
        console.log(response)
        if (response.ok) {
            
            const responseData = await response.json();
            Swal.fire({
                title: 'Success!',
                text: responseData.message,
                icon: 'success',
                confirmButtonText: 'OK',
            });
            form.querySelectorAll('input, select');
            form.reset();

        } else {
            const errorData = await response.json();
            Swal.fire({title:"Error",text:errorData.Erro || "Aconteceu um erro",icon:'error', confirmButtonText:'Ok'});
        }
    } catch (error) {
        // Handle network or unexpected errors
        console.error('Erro ao enviar a solicitação:', error);
        Swal.fire({
            title: 'Error',
            text: 'Erro de conexão. Tente novamente mais tarde.',
            icon: 'error',
            confirmButtonText: 'OK',
        });
    }
});