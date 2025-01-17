from flask import jsonify
import os
from mailersend import emails

def enviar_email(recipients, subject, html_content, plaintext_content, reply_to):

    try:
        mail_from = {"name": "Assessoria Daniel Salum", "email": "MS_SmgJH7@trial-pxkjn41vze64z781.mlsender.net"}
        api_key = os.getenv('MAILERSEND_API_KEY')
        if not api_key:
            raise ValueError("API key not found in environment variables")
        print("Setting up MailerSend")
        mailer = emails.NewEmail(api_key)

        mail_body = {}
        print("Configuring mail body")
        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject(subject, mail_body)
        mailer.set_html_content(html_content, mail_body)
        mailer.set_plaintext_content(plaintext_content, mail_body)
        mailer.set_reply_to(reply_to, mail_body)

        return mailer.send(mail_body)

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    


def enviar_lista_emails(mail_list):
    api_key = os.getenv('MAILERSEND_API_KEY')
    if not api_key:
        raise ValueError("API key not found in environment variables")
    mailer = emails.NewEmail(api_key)
    print("Enviando e-mail agora..")
    return mailer.send_bulk(mail_list)

