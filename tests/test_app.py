
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
    assert response.content_type=="application/json"

def test_calc_echo_malformed_json(client):
    response = client.post("/calcEcho", data="{'char': 'Suisui',", content_type="application/json")
    assert response.status_code==400
    assert response.get_json()["code"]=="invalid_json"
    assert response.is_json

def test_json_invalid_contract(client, valid_request_payload):
    valid_request_payload["char"]=123
    response=client.post("/calcEcho", json=valid_request_payload)
    assert response.status_code==400
    assert response.get_json()["code"]=="invalid_request"
    assert response.is_json

def test_main_internal_error(client, valid_request_payload, monkeypatch):
    def fake_main(*args, **kwargs): raise RuntimeError("internal_crash")
    monkeypatch.setattr("evc_app.main", fake_main)
    response=client.post("/calcEcho", json=valid_request_payload)
    assert response.status_code==500
    assert response.get_json()["code"]=="internal_error"
    

