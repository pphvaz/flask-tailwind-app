from flask import Blueprint, request, jsonify
from services.email_service import enviar_emails
import os
import requests

recaptcha_secret = os.getenv('RECAPTCHA_SECRET_KEY')
recaptcha__test_secret = os.getenv('RECAPTCHA_TEST_SECRET_KEY')

lead_bp = Blueprint('lead', __name__)

@lead_bp.route('/cadastrar_lead', methods=['POST'])
def register_lead():
    recaptcha_token = request.form.get('recaptcha_token')
    if not recaptcha_token:
        return jsonify({'error': 'reCAPTCHA token ausente'}), 400
    response = validarRecaptcha(recaptcha_token)

    if not response.get('success'):
        return jsonify({'error': 'Falha na verificação do reCAPTCHA'}), 400

    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    patrimonio = request.form.get('patrimonio')
    aporte_mensal = request.form.get('mensal')
        
    if not all([nome, telefone, email, patrimonio, aporte_mensal]):
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    try:
        patrimonio = float(patrimonio)
        aporte_mensal = float(aporte_mensal)
    except ValueError:
        return jsonify({"error": "Patrimônio e aporte mensal devem ser valores numéricos."}), 400

    # response = enviar_emails(nome, telefone, email, patrimonio, aporte_mensal, False)
    
    return jsonify({"message": "Solicitação recebida com sucesso!"}), 200

def validarRecaptcha(recaptcha_token):
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': recaptcha__test_secret,
        'response': recaptcha_token
    }
    try:
        response = requests.post(recaptcha_url, data=payload)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao comunicar com o reCAPTCHA: {e}")
        return {'success': False}