from flask import jsonify
import os
from mailersend import emails

api_key = os.getenv('MAILERSEND_API_KEY')

def enviar_lista_emails(mail_list):
    if not api_key:
        raise ValueError("API key not found in environment variables")
    mailer = emails.NewEmail(api_key)
    return mailer.send_bulk(mail_list)