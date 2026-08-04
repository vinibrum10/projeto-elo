"""Cria o schema staging e a view de veiculos tratados."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

SQL_VIEW = """
CREATE SCHEMA IF NOT EXISTS staging;

CREATE OR REPLACE VIEW staging.veiculos AS
SELECT
    payload->>'id'                          AS veiculo_id,
    payload->>'license_plate'               AS placa,
    payload->>'brand'                       AS marca,
    payload->>'model'                       AS modelo,
    NULLIF(payload->>'year', '')::int       AS ano,
    payload->>'fuel'                        AS combustivel,
    payload->>'size'                        AS porte,
    payload->>'alias'                       AS apelido,
    payload->>'last_driver_name'            AS ultimo_motorista,
    NULLIF(payload->>'speed_limit_in_kmh', '')::numeric AS limite_velocidade,
    extraido_em
FROM raw.cobli_vehicles
WHERE payload->>'brand' IS NOT NULL
  AND payload->>'brand' <> 'OBD'
  AND extraido_em = (SELECT MAX(extraido_em) FROM raw.cobli_vehicles);
"""


def get_engine():
    usuario = os.getenv("POSTGRES_USER")
    senha = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    porta = os.getenv("POSTGRES_PORT")
    banco = os.getenv("POSTGRES_DB")
    url = f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}"
    return create_engine(url)


def main():
    engine = get_engine()

    with engine.begin() as conexao:
        conexao.execute(text(SQL_VIEW))
    print("View staging.veiculos criada.")

    with engine.connect() as conexao:
        total = conexao.execute(
            text("SELECT COUNT(*) FROM staging.veiculos")
        ).scalar()
    print(f"Veiculos validos na staging: {total}")


if __name__ == "__main__":
    main()