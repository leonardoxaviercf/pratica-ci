from app import app


def test_saude():
    cliente = app.test_client()
    resposta = cliente.get("/saude")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"status": "ok"}


def test_soma():
    cliente = app.test_client()
    resposta = cliente.get("/soma?a=2&b=3")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"a": 2.0, "b": 3.0, "resultado": 5.0}


def test_historico_sem_variavel(monkeypatch):
    monkeypatch.delenv("HISTORICO", raising=False)
    cliente = app.test_client()
    cliente.get("/soma?a=2&b=3")
    resposta = cliente.get("/historico")
    assert resposta.get_json() == []


def test_historico_com_variavel(monkeypatch, tmp_path):
    arquivo = tmp_path / "historico.log"
    monkeypatch.setenv("HISTORICO", str(arquivo))
    cliente = app.test_client()
    cliente.get("/soma?a=2&b=3")
    resposta = cliente.get("/historico")
    assert resposta.get_json() == ["2.0 + 3.0 = 5.0"]