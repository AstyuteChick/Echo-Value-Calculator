
import pytest
from evc_app import evc_app

@pytest.fixture
def app():
    evc_app.config.update({"TESTING": True})
    yield evc_app

@pytest.fixture
def client(app): return app.test_client()

@pytest.fixture
def valid_request_payload(): return {"char": "Suisui", "team": "Default", "totEr": 260, "ssr": [0.0]*13}

def test_calc_echo_success(client, valid_request_payload):
    response=client.post("/calcEcho", json=valid_request_payload)
    assert response.status_code==200
    assert response.get_json()=={"score": "0.0", "tier": "Not Applicable"}
    assert response.content_type=="application/json" #not sure
