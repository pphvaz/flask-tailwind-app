from utils import email_utils, convert_currency
from flask import jsonify, json
from datetime import datetime
import os
import requests

BULK_STATUS_FILE = "data/bulk_status.json"

# Common Email Configurations
from_mail = "MS_SmgJH7@trial-pxkjn41vze64z781.mlsender.net"
from_name = "Assessoria Daniel Salum"
email_assessor = "pedrohvs.alves1@gmail.com"

def enviar_emails(nome, telefone, email, patrimonio, aporte_mensal, reenvio):
    # Create bulk email list
    mail_list = []

    cliente = {
        "nome":nome,
        "telefone":telefone,
        "email":email,
        "patrimonio":patrimonio,
        "aporte_mensal":aporte_mensal
    }
    
    # Configure assessor email
    assessor_email = configurar_email(
        recipient={"name": "Daniel Salum", "email": email_assessor},
        subject=f"Boas notícias: Novo lead, {nome}",
        text_content=create_text_assessor(nome, telefone, email, patrimonio, aporte_mensal),
        html_content=create_html_assessor(nome, telefone, email, patrimonio, aporte_mensal)
    )
    mail_list.append(assessor_email)
    
    # Configure client email
    client_email = configurar_email(
        recipient={"name": nome, "email": email},
        subject=f"Olá, {nome}! Sua solicitação foi recebida com sucesso",
        text_content=create_text_cliente(nome),
        html_content=create_html_cliente(nome)
    )
    mail_list.append(client_email)
    
    response = email_utils.enviar_lista_emails(mail_list)

    if not reenvio:
        status, json_str = response.split("\n")  

        if int(status) == 202:
            bulk_email_id = json.loads(json_str)['bulk_email_id']
            salvar_bulk_status(bulk_email_id, mail_list, "processando",cliente)
        else:
            salvar_bulk_status(response, mail_list, "falha_no_envio",cliente)

    return response
    
def salvar_bulk_status(bulk_email_id, mail_list, status,cliente):
    bulk_data = []
    data = {
        "bulk_email_id":bulk_email_id,
        "emails":mail_list,
        "status":status,
        "datahora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cliente": cliente,
        "tentativas":1
    }
    try:
        with open(BULK_STATUS_FILE, "r") as f:
            if f.read(1):
                f.seek(0)
                bulk_data = json.load(f)
                print("NÃO ESTÁ VAZIO")
            else:
                print("ELSE ZERANDO...")
                bulk_data = []
    except (FileNotFoundError):
        print("EXCEPT ZERANDO...")
        bulk_data = []
    
    bulk_data.append(data)
    with open(BULK_STATUS_FILE, "w") as f:
        json.dump(bulk_data, f, indent=4)

def verificar_bulk_status():
    print("VERIFICANDO LISTA DE EMAILS \n")
    try:
        with open(BULK_STATUS_FILE, "r") as f:
            bulk_data = json.load(f)
    except (FileNotFoundError):
        return
    headers = {
        "Authorization": f"Bearer {os.getenv('MAILERSEND_API_KEY')}",
        "Content-Type": "application/json"
    }
    for entry in bulk_data[:]:
        if entry["status"] != "completed" and entry["bulk_email_id"]:
            url = f"https://api.mailersend.com/v1/bulk-email/{entry['bulk_email_id']}"
            response = requests.get(url, headers=headers)
            print("Pesquisando...\n")
            if response.status_code == 200:
                response_data = response.json()
                if response_data['data']['state'] == "completed":
                    print("removing....")
                    bulk_data.remove(entry)

                else:
                    print("REENVIANDO EMAIL ENCONTRADO...")
                    email_utils.enviar_lista_emails(entry['emails'])
            else:
                print("REENVIANDO EMAIL NÃO ENCONTRADO...\n")
                # Criar nova solicitação de email...
                enviar_emails(entry['cliente']['nome'], entry['cliente']['telefone'], entry['cliente']['email'], entry['cliente']['patrimonio'], entry['cliente']['aporte_mensal'], True)
            entry['tentativas'] = entry['tentativas'] + 1
        else:
            print("EMAIL JÁ ENVIADO...")
            bulk_data.remove(entry)
    with open(BULK_STATUS_FILE, "w") as f:
        print(f"SALVANDO JSON.DUMP COM OS DADOS: {len(bulk_data)} emails.")
        json.dump(bulk_data, f, indent=4)

def configurar_email(recipient, subject, text_content, html_content):
    """BULK_STATUS_FILE
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
