import requests
import time
from requests.exceptions import ReadTimeout

def busca_bcb(codigo, data_inicio, data_fim, retries=5, delay=5):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={data_inicio}&dataFinal={data_fim}'
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except ReadTimeout:
            print(f"ReadTimeout: Retrying {attempt + 1}/{retries}...")
            attempt += 1
            time.sleep(delay * (2 ** attempt))
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break
    return []