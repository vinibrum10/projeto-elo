"""Extrai a lista de veiculos da API da Cobli e salva o retorno bruto."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COBLI_API_KEY")
BASE_URL = "https://api.cobli.co"
ENDPOINT = "/public/v1/vehicles"

RAW_DIR = Path("data/raw")


def extrair_veiculos():
    if not API_KEY:
        raise RuntimeError("COBLI_API_KEY nao encontrada no .env")

    headers = {
        "cobli-api-key": API_KEY,
        "Accept": "application/json",
    }

    resposta = requests.get(BASE_URL + ENDPOINT, headers=headers, timeout=30)
    print(f"Status HTTP: {resposta.status_code}")
    resposta.raise_for_status()

    dados = resposta.json()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    carimbo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destino = RAW_DIR / f"vehicles_{carimbo}.json"

    with open(destino, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    print(f"Salvo em: {destino}")
    return dados


def inspecionar(dados):
    print(f"\nTipo do retorno: {type(dados).__name__}")

    if isinstance(dados, dict):
        print(f"Chaves de primeiro nivel: {list(dados.keys())}")
        for chave, valor in dados.items():
            if isinstance(valor, list) and valor:
                print(f"\n'{chave}' tem {len(valor)} itens.")
                print(f"Campos do primeiro item: {list(valor[0].keys())}")
                break
    elif isinstance(dados, list):
        print(f"Lista com {len(dados)} itens.")
        if dados:
            print(f"Campos do primeiro item: {list(dados[0].keys())}")


if __name__ == "__main__":
    resultado = extrair_veiculos()
    inspecionar(resultado)