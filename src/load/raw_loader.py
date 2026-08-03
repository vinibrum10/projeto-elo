"""Carrega arquivos JSON da pasta raw para o schema raw do PostgreSQL."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

RAW_DIR = Path("data/raw")


def get_engine():
    usuario = os.getenv("POSTGRES_USER")
    senha = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    porta = os.getenv("POSTGRES_PORT")
    banco = os.getenv("POSTGRES_DB")
    url = f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}"
    return create_engine(url)


def preparar_schema(engine):
    with engine.begin() as conexao:
        conexao.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
        conexao.execute(text("""
            CREATE TABLE IF NOT EXISTS raw.cobli_vehicles (
                id            SERIAL PRIMARY KEY,
                extraido_em   TIMESTAMPTZ NOT NULL,
                arquivo       TEXT NOT NULL,
                payload       JSONB NOT NULL,
                carregado_em  TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """))
    print("Schema e tabela prontos.")


def carregar_arquivo(engine, caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        conteudo = json.load(arquivo)

    veiculos = conteudo["data"]
    carimbo = caminho.stem.replace("vehicles_", "")
    extraido_em = datetime.strptime(carimbo, "%Y%m%dT%H%M%SZ").replace(
        tzinfo=timezone.utc
    )

    with engine.begin() as conexao:
        for veiculo in veiculos:
            conexao.execute(
                text("""
                    INSERT INTO raw.cobli_vehicles (extraido_em, arquivo, payload)
                    VALUES (:extraido_em, :arquivo, :payload)
                """),
                {
                    "extraido_em": extraido_em,
                    "arquivo": caminho.name,
                    "payload": json.dumps(veiculo),
                },
            )

    print(f"{len(veiculos)} veiculos carregados de {caminho.name}")


def main():
    engine = get_engine()
    preparar_schema(engine)

    arquivos = sorted(RAW_DIR.glob("vehicles_*.json"))
    if not arquivos:
        print("Nenhum arquivo encontrado em data/raw/")
        return

    mais_recente = arquivos[-1]
    print(f"Carregando: {mais_recente.name}")
    carregar_arquivo(engine, mais_recente)


if __name__ == "__main__":
    main()