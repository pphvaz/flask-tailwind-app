document.addEventListener("DOMContentLoaded", function() { 
    const recaptchaWidgetId = grecaptcha.render('recaptcha-container', {
        'sitekey': '6LfzgbwqAAAAALd7Bl362HUQ6G9jzEujHoeR52Jw',
        'theme': 'light',
    });


    document.getElementById('adicionar_cliente').addEventListener('click', async (event) => {
    event.preventDefault();
    console.log(grecaptcha);
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

    const recaptchaResponse = grecaptcha.getResponse(recaptchaWidgetId);

    if (!recaptchaResponse) {
        Swal.fire({
            title: 'Oops!',
            text: 'Falha ao verificar o reCAPTCHA. Por favor, tente novamente.',
            icon: 'warning',
            confirmButtonText: 'OK',
        });
        return;
    }
    console.log(recaptchaResponse);
    formData.append('recatcha_token', recaptchaResponse);

    try { 
        const response = await fetch('lead/cadastrar_lead', {
            method: 'POST',
            body: formData,
        });
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

});