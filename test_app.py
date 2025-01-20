import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import app
from typing import Generator

@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    """
    Create a test client to simulate requests to the app.
    """
    app.config['TESTING'] = True
    yield app.test_client()


def test_simulate_investments(client):
    # Test valid POST request to /simular-investimento
    response = client.post('/financial/simular-investimento', data={
        'inicial': 1000,
        'mensal': 200,
        'juros': 5,
        'tipo_juros': 'ano',
        'tempo': 5,
        'tipo_tempo': 'anos'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)  # Check if the response is a list

def test_simulate_investments_invalid(client):
    # Test POST request with invalid data
    response = client.post('/financial/simular-investimento', data={
        'inicial': -1000,  # Invalid value
        'mensal': 200,
        'juros': 5,
        'tipo_juros': 'ano',
        'tempo': 5,
        'tipo_tempo': 'anos'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'Erro' in data  # Check if an error message is present


def test_index(client):
    # Test GET request to index
    response = client.get('/')
    assert response.status_code == 200
    assert b"Selic" in response.data  # Check if the Selic data appears on the page

def test_cookies(client):
    # Test GET request to /cookies
    response = client.get('/cookies')
    assert response.status_code == 200
    assert b"Cookies" in response.data  # Check if "Cookies" is mentioned in the page

def test_privacidade(client):
    # Test GET request to /privacidade
    response = client.get('/privacidade')
    assert response.status_code == 200
    assert b"Privacidade" in response.data  # Check if "Privacidade" is mentioned in the page


def test_register_lead_valid(client, mocker):
    # Mock the email sending to avoid actual sending during tests
    mocker.patch('services.email_service.enviar_emails', return_value='202')
    
    response = client.post('/lead/cadastrar_lead', data={
        'recatcha_token': 'valid-token',
        'nome': 'John Doe',
        'telefone': '123456789',
        'email': 'john@example.com',
        'patrimonio': 50000,
        'mensal': 1000
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'Solicitação recebida com sucesso' in data['message']

def test_register_lead_invalid_recaptcha(client):
    # Test POST with invalid reCAPTCHA
    response = client.post('/lead/cadastrar_lead', data={
        'recatcha_token': '',
        'nome': 'John Doe',
        'telefone': '123456789',
        'email': 'john@example.com',
        'patrimonio': 50000,
        'mensal': 1000
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'reCAPTCHA token ausente' in data['error']

def test_register_lead_missing_fields(client):
    # Test POST with missing fields
    response = client.post('/lead/cadastrar_lead', data={
        'recatcha_token': 'valid-token',
        'nome': '',
        'telefone': '123456789',
        'email': 'john@example.com',
        'patrimonio': 50000,
        'mensal': 1000
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'Todos os campos são obrigatórios' in data['error']