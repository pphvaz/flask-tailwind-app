from flask import jsonify
import os
from mailersend import emails

api_key = os.getenv('MAILERSEND_API_KEY')
MAILERSEND_USER=os.getenv('MAILERSEND_USER')

def enviar_lista_emails(mail_list):
    print(mail_list[0]['from'])
    if not api_key:
        raise ValueError("API key not found in environment variables")
    mailer = emails.NewEmail(api_key)
    print("Enviando e-mail agora..")
    return mailer.send_bulk(mail_list)