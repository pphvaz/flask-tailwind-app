import requests

def buscar_banco_central(api_url):
    response = requests.get(api_url)
    return response.json()