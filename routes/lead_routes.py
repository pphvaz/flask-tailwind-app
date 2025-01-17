from flask import Blueprint, request, jsonify
from services.email_service import enviar_emails
import threading

lead_bp = Blueprint('lead', __name__)


@lead_bp.route('/cadastrar_lead', methods=['POST'])
def register_lead():
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

    response = enviar_emails(nome, telefone, email, patrimonio, aporte_mensal, False)
    
    return jsonify({"message": "Solicitação recebida com sucesso!"}), 200