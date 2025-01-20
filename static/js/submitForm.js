document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-contato');
    const submitButton = document.getElementById('adicionar_cliente');
    const loadingMessage = document.createElement('div');
    loadingMessage.textContent = 'Submitting, please wait...';
    loadingMessage.style.display = 'none';
    submitButton.insertAdjacentElement('afterend', loadingMessage);

    submitButton.addEventListener('click', async (event) => {
        event.preventDefault();

        submitButton.disabled = true;
        loadingMessage.style.display = 'block';

        const formData = new FormData(form);
        const allInputsValid = [...formData.values()].every(value => value.trim() !== '');
        const recaptchaResponse = grecaptcha.getResponse();

        if (!allInputsValid || !recaptchaResponse) {
            Swal.fire({
                title: 'Oops!',
                text: !allInputsValid ? "Preencha todos os campos antes de submeter." : 'Falha ao verificar o reCAPTCHA. Tente novamente.',
                icon: 'warning',
                confirmButtonText: 'OK',
            });
            resetForm();
            return;
        }
        formData.append('recaptcha_token', recaptchaResponse);

        try {
            const response = await fetch('lead/cadastrar_lead', {
                method: 'POST',
                body: formData,
            });
            const responseData = await response.json();
            if (response.ok) {
                Swal.fire({
                    title: 'Success!',
                    text: responseData.message,
                    icon: 'success',
                    confirmButtonText: 'OK',
                });
                form.reset();
            } else {
                Swal.fire({
                    title: "Error",
                    text: responseData.Erro || "Aconteceu um erro",
                    icon: 'error',
                    confirmButtonText: 'Ok',
                });
                resetForm();
            }
        } catch (error) {
            Swal.fire({
                title: 'Error',
                text: 'Erro de conexão. Tente novamente mais tarde.',
                icon: 'error',
                confirmButtonText: 'OK',
            });
        } finally {
            resetForm();
        }
    });

    function resetForm() {
        grecaptcha.reset();
        submitButton.disabled = false;
        loadingMessage.style.display = 'none';
    }
});
