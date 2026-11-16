import os
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)


@app.get("/saude")
def saude():
    return {"status": "ok"}


@app.get("/soma")
def soma():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    resultado = a + b
    caminho = os.environ.get("HISTORICO")
    if caminho:
        with Path(caminho).open("a", encoding="utf-8") as f:
            f.write(f"{a} + {b} = {resultado}\n")
    return {"a": a, "b": b, "resultado": resultado}


@app.get("/historico")
def historico():
    caminho = os.environ.get("HISTORICO")
    if not caminho or not Path(caminho).exists():
        return []
    return Path(caminho).read_text(encoding="utf-8").splitlines()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)