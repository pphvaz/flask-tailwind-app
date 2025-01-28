import os
import json
from datetime import datetime, timedelta
from services.bcb_service import busca_bcb

DATA_FILE_PATH = 'data/financial_data.json'
DATA_SOURCES = {
    'cdi': '4392',
    'selic': '1178',
    'poupanca': '196',
    'tr': '226'
}

class FinancialData:
    def __init__(self):
        self.data = {}
        self.load_data_from_file()

    def update(self, results):
        self.data.update(results)
        self.data['last_update'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    def get(self, key):
        return self.data.get(key, None)

    def load_data_from_file(self):
        if os.path.exists(DATA_FILE_PATH):
            if os.stat(DATA_FILE_PATH).st_size > 0:
                try:
                    with open(DATA_FILE_PATH, 'r') as f:
                        self.data = json.load(f)
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    print(f"Error reading financial data from file: {e}")
                    fetch_and_calculate_averages()
            else:
                print("Data file is empty. Fetching new data.")
                fetch_and_calculate_averages()
        else:
            print("Data file does not exist. Fetching new data.")
            fetch_and_calculate_averages()


def fetch_and_calculate_averages():
    hoje = datetime.today()
    um_ano_atras = hoje - timedelta(days=365)

    inicio = um_ano_atras.strftime('%d/%m/%Y')
    fim = hoje.strftime('%d/%m/%Y')

    results = {}
    for key, code in DATA_SOURCES.items():
        data = busca_bcb(code, inicio, fim)
        if isinstance(data, list):
            values = [float(item['valor']) for item in data if 'valor' in item]
            avg = sum(values) / len(values) if values else 0
            results[key] = avg
        else:
            results[key] = None

    financial_data = {
        'com assessor': results.get('cdi') + 2,
        'cdi': results.get('cdi'),
        'poupanca': results.get('poupanca') * 12,
        'last_update': hoje.strftime('%d/%m/%Y %H:%M:%S')
    }

    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
    with open(DATA_FILE_PATH, 'w') as f:
        json.dump(financial_data, f)


def validate_financial_data():
    print("Validating.....")
    if os.path.exists(DATA_FILE_PATH) and os.stat(DATA_FILE_PATH).st_size > 0:
        try:
            with open(DATA_FILE_PATH, 'r') as f:
                financial_data = json.load(f)

            last_update = datetime.strptime(financial_data['last_update'], '%d/%m/%Y %H:%M:%S')
            today = datetime.today()
            delta_days = (today - last_update).days

            if delta_days > 7 or any(value is None or value == 0 for value in financial_data.values()):
                print("Data is outdated or contains invalid values. Fetching new data.")
                fetch_and_calculate_averages()
            else:
                print("Financial data is up-to-date.")

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error reading financial data: {e}. Fetching new data.")
            fetch_and_calculate_averages()
    else:
        print("No previous data found or the data file is empty. Fetching new data.")
        fetch_and_calculate_averages()
