from uuid import uuid4
from fastapi.testclient import TestClient

email_test = f'teste_{uuid4()}@email.com'
password_test = f'teste_{uuid4()}'

def test_create_account(client: TestClient):

    user_data = {
        'name': 'Teste do Teste',
        'email': email_test,
        'password': password_test,
    }

    response = client.post('/api/v1/auth/create-account', json=user_data)

    assert response.status_code == 201 

    response_data = response.json()

    assert 'data' in response_data
    user_in_response = response_data['data']

    assert 'id' in user_in_response
    assert 'name' in user_in_response
    assert 'email' in user_in_response
    assert 'active' in user_in_response
    assert 'admin' in user_in_response

    assert user_in_response['email'] == email_test
    assert user_in_response['name'] == 'Teste do Teste'
    assert user_in_response['active'] is True
    assert user_in_response['admin'] is False

    assert 'password' not in user_in_response 
    assert 'password' not in response_data

def test_login(client: TestClient):
    user_data = {
        'email': email_test,
        'password': password_test
    }

    response = client.post('/api/v1/auth/login', json=user_data)
    assert response.status_code == 200

    response_data = response.json()
    assert 'access_token' in response_data
    assert 'refresh_token' in response_data
    assert 'token_type' in response_data
    assert response_data['token_type'] == 'Bearer'