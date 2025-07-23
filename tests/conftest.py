import sys
import os

import pytest 
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app


@pytest.fixture(scope='module')
def client():
    '''
    Fixture que fornece um cliente de teste para a aplicação FastAPI.
    Este cliente pode fazer requisições HTTP para as rotas do app.
    '''

    with TestClient(app) as c:
        yield c