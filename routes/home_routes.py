from flask import Blueprint, render_template, json

home_bp = Blueprint('home', __name__)

DATA_FILE_PATH = 'data/financial_data.json'

with open(DATA_FILE_PATH, 'r') as f:
                financial_data = json.load(f)

@home_bp.route('/')
def index():
    print(financial_data)
    return render_template(
           'index.html', 
            taxa_selic = round(financial_data['selic'],2),
            taxa_cdi = financial_data['cdi'],
            poupanca = round(financial_data['poupanca'],2),
            atualizacao = financial_data['last_update']
        )

@home_bp.route('/cookies')
def cookies():
    return render_template('cookies.html')

@home_bp.route('/privacidade')
def privacidade():
    return render_template('privacidade.html')