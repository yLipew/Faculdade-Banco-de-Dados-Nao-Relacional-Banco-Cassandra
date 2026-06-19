"""
Leitor de dados de sensores armazenados no Astra DB (Cassandra) via API REST.

Configuração:
    Defina as credenciais como variáveis de ambiente antes de rodar:

        export ASTRA_DB_ID="011475e8-2c3b-42bc-9728-62ccb8ebd5b2"
        export ASTRA_DB_REGION="us-east-2"
        export ASTRA_TOKEN="sua_chave_aqui"

    (No Windows/PowerShell: $env:ASTRA_TOKEN="sua_chave_aqui")
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import requests

sys.stdout.reconfigure(encoding="utf-8")


@dataclass
class AstraConfig:
    db_id: str
    region: str
    token: str
    keyspace: str = "default_keyspace"
    table: str = "leituras_sensor"

    @property
    def url(self) -> str:
        return (
            f"https://{self.db_id}-{self.region}.apps.astra.datastax.com"
            f"/api/rest/v2/keyspaces/{self.keyspace}/{self.table}/rows"
        )

    @classmethod
    def from_env(cls) -> "AstraConfig":
        try:
            return cls(
                db_id=os.environ["ASTRA_DB_ID"],
                region=os.environ["ASTRA_DB_REGION"],
                token=os.environ["ASTRA_TOKEN"],
                keyspace=os.environ.get("ASTRA_KEYSPACE", "default_keyspace"),
                table=os.environ.get("ASTRA_TABLE", "leituras_sensor"),
            )
        except KeyError as e:
            raise SystemExit(
                f"❌ Variável de ambiente faltando: {e}. "
                "Configure ASTRA_DB_ID, ASTRA_DB_REGION e ASTRA_TOKEN."
            )


def buscar_leituras(config: AstraConfig) -> list[dict]:
    """Busca as leituras de sensores no Astra DB e retorna a lista de registros."""
    headers = {
        "X-Cassandra-Token": config.token,
        "Accept": "application/json",
    }

    try:
        resposta = requests.get(config.url, headers=headers, timeout=10)
        resposta.raise_for_status()
    except requests.exceptions.Timeout:
        raise SystemExit("❌ Tempo de conexão esgotado. Verifique sua internet ou o status do Astra DB.")
    except requests.exceptions.HTTPError:
        raise SystemExit(f"❌ Falha na conexão. Erro {resposta.status_code}: {resposta.text}")
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"❌ Erro de conexão: {e}")

    return resposta.json().get("data", [])


def exibir_leituras(leituras: list[dict]) -> None:
    """Exibe as leituras formatadas no terminal."""
    if not leituras:
        print("⚠️ Nenhuma leitura encontrada.")
        return

    print(f"✅ Conexão bem-sucedida! {len(leituras)} leitura(s) recuperada(s) da nuvem:\n")
    for leitura in leituras:
        sensor = leitura.get("sensor_id")
        data_leitura = leitura.get("data_leitura")
        temp = leitura.get("temperatura")
        status = leitura.get("status")
        print(f"Data: {data_leitura} | Sensor: {sensor} | Temp: {temp}°C | Status: {status}")


def main() -> None:
    config = AstraConfig.from_env()
    print("Conectando à API do Cassandra (Astra DB)...\n")
    leituras = buscar_leituras(config)
    exibir_leituras(leituras)


if __name__ == "__main__":
    main()