"""Extrai a lista de motoristas da API da Cobli e salva o retorno bruto."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COBLI_API_KEY")
BASE_URL = "https://api.cobli.co"
ENDPOINT = "/public/v1/drivers"

RAW_DIR = Path("data/raw")


def extrair_motoristas():
    if not API_KEY:
        raise RuntimeError("COBLI_API_KEY nao encontrada no .env")

    headers = {"cobli-api-key": API_KEY, "Accept": "application/json"}
    resposta = requests.get(BASE_URL + ENDPOINT, headers=headers, timeout=30)
    print(f"Status HTTP: {resposta.status_code}")
    resposta.raise_for_status()

    dados = resposta.json()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    carimbo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destino = RAW_DIR / f"drivers_{carimbo}.json"

    with open(destino, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    print(f"Salvo em: {destino}")
    return dados


def inspecionar(dados):
    print(f"\nChaves de primeiro nivel: {list(dados.keys())}")
    print(f"Paginacao: {dados.get('pagination')}")

    motoristas = dados.get("data", [])
    print(f"Total de motoristas: {len(motoristas)}")

    if motoristas:
        print("\nCampos disponiveis:")
        for campo in motoristas[0].keys():
            print(f"  - {campo}")


if __name__ == "__main__":
    resultado = extrair_motoristas()
    inspecionar(resultado)