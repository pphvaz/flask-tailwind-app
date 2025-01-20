from utils import email_utils, convert_currency
from flask import jsonify, json
from datetime import datetime
import os
import requests
import logging

LISTA_EMAILS = "data/LISTA_EMAILS.json"

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Common Email Configurations
from_mail = os.getenv('MAILERSEND_USER')
from_name = "Assessoria Daniel Salum"
email_assessor = "pedrohvs.alves1@gmail.com"

def ler_lista_emails():
    """Função para ler a lista de emails do arquivo."""
    try:
        with open(LISTA_EMAILS, "r") as f:
            if os.stat(LISTA_EMAILS).st_size > 0:
                return json.load(f)
            else:
                logger.info("Arquivo vazio, inicializando lista.")
                return []
    except FileNotFoundError:
        logger.warning("Arquivo não encontrado, criando uma nova lista.")
        return []

def salvar_lista_emails(bulk_email_id, mail_list, status_text, status_code, cliente, message):
    """Função para salvar a lista de emails no arquivo."""
    logger.info("Salvando lista de emails...")
    lista_emails = ler_lista_emails()
    
    # Preparar dados para salvar
    data = {
        "bulk_email_id": bulk_email_id,
        "emails": mail_list,
        "status": status_text,
        "status_code": status_code,
        "datahora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cliente": cliente,
        "tentativas": 1,
        "message": message
    }
    
    lista_emails.append(data)
    
    with open(LISTA_EMAILS, "w") as f:
        json.dump(lista_emails, f, indent=4)
    logger.info(f"{len(lista_emails)} emails salvos.")

def enviar_emails(nome, telefone, email, patrimonio, aporte_mensal, reenvio):
    """Função para enviar os e-mails para cliente e assessor."""
    # Create bulk email list
    mail_list = []

    cliente = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "patrimonio": patrimonio,
        "aporte_mensal": aporte_mensal
    }

    # Configure emails
    try:
        # Assessor email
        assessor_email = configurar_email(
            recipient={"name": "Daniel Salum", "email": email_assessor},
            subject=f"Boas notícias: Novo lead, {nome}",
            text_content=create_text_assessor(nome, telefone, email, patrimonio, aporte_mensal),
            html_content=create_html_assessor(nome, telefone, email, patrimonio, aporte_mensal)
        )
        mail_list.append(assessor_email)

        # Client email
        client_email = configurar_email(
            recipient={"name": nome, "email": email},
            subject=f"Olá, {nome}! Sua solicitação foi recebida com sucesso",
            text_content=create_text_cliente(nome),
            html_content=create_html_cliente(nome)
        )
        mail_list.append(client_email)

        # Enviar e-mails
        response = email_utils.enviar_lista_emails(mail_list)

        status_code = response.status_code
        message = response.json().get('message', 'Sem mensagem')

        if not reenvio:
            if response.status_code == 202:
                # salvar o e-mail na lista para verificar se o status é completed.
                bulk_email_id = response.json().get('bulk_email_id')
                salvar_lista_emails(bulk_email_id, mail_list, "processando", status_code, cliente, message)
            else:
                salvar_lista_emails(None, mail_list, "falha_no_envio", status_code, cliente, message)
        else:
            return response

    except Exception as e:
        logger.error(f"Erro ao enviar e-mails: {str(e)}")


def verificar_lista_emails():
    """Função para verificar a lista de emails e processá-los."""
    logger.info("Verificando lista de emails...")
    lista_emails = ler_lista_emails()
    
    if not lista_emails:
        logger.info("Nenhum email na lista para processar.")
        return

    headers = {
        "Authorization": f"Bearer {os.getenv('MAILERSEND_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    for entry in lista_emails[:]:
        if entry["status"] not in ["completed"]:
            processar_email(entry, headers, lista_emails)
        else:
            logger.info(f"Email com bulk_email_id {entry['bulk_email_id']} já enviado ou com falha.")

    # Salvar lista atualizada
    with open(LISTA_EMAILS, "w") as f:
        logger.info(f"Salvando {len(lista_emails)} emails restantes.")
        json.dump(lista_emails, f, indent=4)

def processar_email(entry, headers, lista_emails):
    """Função para processar cada email individualmente."""
    url = f"https://api.mailersend.com/v1/bulk-email/{entry['bulk_email_id']}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['data']['state'] == "completed":
            logger.info(f"Email {entry['bulk_email_id']} concluído, removendo da lista.")
            lista_emails.remove(entry)
        else:
            logger.info("Email ainda não concluído, reenviando...")
            email_utils.enviar_lista_emails(entry['emails'])
    else:
        logger.warning(f"Falha ao verificar email {entry['bulk_email_id']}. Status: {response.status_code}.")
        # Criar nova solicitação de email em caso de falha
        response = enviar_emails(entry['cliente']['nome'], entry['cliente']['telefone'], entry['cliente']['email'], entry['cliente']['patrimonio'], entry['cliente']['aporte_mensal'], True)
        print(response)
        if response.status_code == 202:
            logger.info("Email reenviado com sucesso.\n")
            entry['bulk_email_id'] = response.json().get('bulk_email_id')
            entry['status'] = "processando"
    
    entry['tentativas'] += 1

def configurar_email(recipient, subject, text_content, html_content):
    """LISTA_EMAILS
    Configures an individual email object.
    """
    return {
        "from": {
            "email": from_mail,
            "name": from_name
        },
        "to": [recipient],
        "subject": subject,
        "text": text_content,
        "html": html_content,
    }

def create_text_assessor(nome, telefone, email, patrimonio, aporte_mensal):
    """
    Creates the plaintext content for the assessor email.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    patrimonio_formatted = convert_currency.converter_moeda(patrimonio)
    aporte_mensal_formatted = convert_currency.converter_moeda(aporte_mensal)
    
    return f"""
    Boas notícias: Novo lead, {nome}

    Nome: {nome}
    Telefone: {telefone}
    Email: {email}
    Patrimônio: {patrimonio_formatted}
    Aporte Mensal: {aporte_mensal_formatted}

    Data e Hora do Envio: {timestamp}
    """

def create_html_assessor(nome, telefone, email, patrimonio, aporte_mensal):
    """
    Creates the HTML content for the assessor email.
    """
    with open('./templates/email/novo_lead.html', 'r', encoding='utf-8') as template_file:
        html_template = template_file.read()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    patrimonio_formatted = convert_currency.converter_moeda(patrimonio)
    aporte_mensal_formatted = convert_currency.converter_moeda(aporte_mensal)
    
    return html_template.format(
        nome=nome,
        telefone=telefone,
        email=email,
        patrimonio=patrimonio_formatted,
        aporte_mensal=aporte_mensal_formatted,
        timestamp=timestamp
    )

def create_text_cliente(nome):
    """
    Creates the plaintext content for the client email.
    """
    return f"""
    Olá {nome},

    Obrigado por entrar em contato conosco! Recebemos suas informações e um dos nossos assessores entrará em contato com você o mais rápido possível para entender melhor suas necessidades e ajudá-lo.

    Estamos à disposição para ajudar no que for necessário.

    Atenciosamente,  
    Equipe de Atendimento
    """

def create_html_cliente(nome):
    """
    Creates the HTML content for the client email.
    """
    with open('./templates/email/boas_vindas.html', 'r', encoding='utf-8') as template_file:
        html_template = template_file.read()
    
    return html_template.format(nome=nome)
