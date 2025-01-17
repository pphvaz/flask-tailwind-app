from flask import Blueprint, request, jsonify, json
from services.financial_service import calcular_juros_compostos
from models import financial_data

financial_bp = Blueprint('financial', __name__)

DATA_FILE_PATH = 'data/financial_data.json'

with open(DATA_FILE_PATH, 'r') as f:
    financial_data = json.load(f)

@financial_bp.route('/simular-investimento', methods=['POST'])
def simulate_investments():
    try:
        print("Simulação solicitada.")
        inicial = float(request.form.get("inicial", 0))
        aporte_mensal = float(request.form.get("mensal", 0))
        taxa_de_juros = float(request.form.get("juros", 0))
        tipo_juros = request.form.get("tipo_juros")
        tempo = int(request.form.get("tempo"))
        tipo_tempo = request.form.get("tipo_tempo")

        # Validar inputs
        if inicial < 0 or aporte_mensal < 0 or taxa_de_juros < 0 or tempo <= 0:
            return jsonify({"Erro":"Valores inválidos."})
        
        # Converter taxa de juros mensais - se necessário
        taxa_juros_mensal = mensalizar_juros_anuais(taxa_de_juros) if tipo_juros == 'ano' else taxa_de_juros / 100

        # Converter anos para meses - se necessário
        meses = tempo * 12 if tipo_tempo == 'anos' else tempo

        juros_simulado = nome_para_referencia_solicitada(tipo_juros,taxa_de_juros)

        listaValoresSimulados = []
        listaValoresSimulados.append(calcular_juros_compostos(juros_simulado, inicial, aporte_mensal, taxa_juros_mensal, meses))

        for referencia, taxa in financial_data.items():
            if not isinstance(taxa, (int, float)):
                continue
            resultado = calcular_juros_compostos(referencia, inicial, aporte_mensal, mensalizar_juros_anuais(taxa), meses)
            listaValoresSimulados.append(resultado)
            
        return jsonify(listaValoresSimulados), 200
    except ValueError:
        print(e)
        return jsonify({"Erro":"Campos preenchidos para a simulação estão inválidos."}), 400
    except Exception as e:
        print(e)
        return jsonify({"Erro":"Não foi possível completar a solicitação"}), 500
    
def mensalizar_juros_anuais(juros):
    return (1 + juros / 100) ** (1 / 12) - 1

def nome_para_referencia_solicitada(tipo_juros, taxa_juros):
    nome_juros_abreviado = 'a.a.' if tipo_juros == 'ano' else 'a.m.'
    return f"{round(taxa_juros,2)}% {nome_juros_abreviado}"