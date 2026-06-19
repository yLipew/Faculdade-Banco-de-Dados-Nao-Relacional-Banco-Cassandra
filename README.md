# 🗄️ Atividade Prática — Apache Cassandra com Astra DB (REST API)

> **Disciplina:** Banco de Dados NoSQL  
> **Curso:** Análise e Desenvolvimento de Sistemas — FATESG  
> **Semestre:** 2º Semestre · 2026/1  

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cassandra](https://img.shields.io/badge/Apache%20Cassandra-1287B1?style=for-the-badge&logo=apache-cassandra&logoColor=white)
![DataStax](https://img.shields.io/badge/DataStax%20Astra-FF6F00?style=for-the-badge&logo=datastax&logoColor=white)
![AWS](https://img.shields.io/badge/AWS%20us--east--2-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![REST API](https://img.shields.io/badge/REST%20API-Stargate-6DB33F?style=for-the-badge&logo=fastapi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)

---

## 📌 Sobre o Projeto

Este projeto demonstra a integração entre **Python** e o **Apache Cassandra** hospedado na nuvem via **DataStax Astra DB**, utilizando a **API REST (Stargate)**. O cenário simulado é um sistema de leitura de sensores IoT, onde dados de temperatura, umidade e status são armazenados e consultados remotamente.

---

## 🧱 Arquitetura

```
┌─────────────────────┐        REST API (HTTPS)       ┌──────────────────────────┐
│   Script Python     │ ─────────────────────────────▶ │   DataStax Astra DB      │
│  (leitura de dados) │ ◀─────────────────────────────  │   (Apache Cassandra)     │
└─────────────────────┘        JSON Response           └──────────────────────────┘
                                                              │
                                                     Keyspace: default_keyspace
                                                     Tabela: leituras_sensor
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão / Plano | Função |
|---|---|---|
| Python | 3.13+ | Linguagem principal |
| `requests` | latest | Requisições HTTP à API REST |
| DataStax Astra DB | Free Tier | Banco Cassandra gerenciado na nuvem |
| Stargate REST API | v2 | Interface HTTP para o Cassandra |
| AWS | us-east-2 | Região do datacenter |

---

## 🗃️ Modelagem da Tabela

Criada via **CQL Console** no painel do Astra DB:

```sql
CREATE TABLE IF NOT EXISTS leituras_sensor (
    sensor_id   text,
    data_leitura date,
    horario      timestamp,
    temperatura  decimal,
    umidade      decimal,
    status       text,
    PRIMARY KEY ((sensor_id, data_leitura), horario)
) WITH CLUSTERING ORDER BY (horario DESC);
```

### Dados inseridos para teste

```sql
INSERT INTO leituras_sensor (sensor_id, data_leitura, horario, temperatura, umidade, status)
VALUES ('sensor-001', '2026-05-22', '2026-05-22 10:30:00', 25.4, 60.2, 'OK');

INSERT INTO leituras_sensor (sensor_id, data_leitura, horario, temperatura, umidade, status)
VALUES ('sensor-001', '2026-05-22', '2026-05-22 10:35:00', 25.7, 61.0, 'OK');

INSERT INTO leituras_sensor (sensor_id, data_leitura, horario, temperatura, umidade, status)
VALUES ('sensor-002', '2026-05-22', '2026-05-22 10:30:00', 28.1, 58.5, 'ALERTA');
```

---

## 📁 Estrutura do Projeto

```
RAG-avancado_Cassandra-API/
├── .venv/                          # Ambiente virtual Python
└── Atividade_API-Cassandra/
    ├── API_Cassandra.py            # Script principal (versão inicial)
    ├── Atividade-Cassandra.py      # Script refatorado com boas práticas
    ├── Tutorial-Cassandra.docx     # Tutorial da atividade
    └── Tutorial-Cassandra.pdf      # Tutorial em PDF
```

---

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/RAG-avancado_Cassandra-API.git
cd RAG-avancado_Cassandra-API
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install requests
```

### 4. Configure as variáveis de ambiente

**Linux/macOS:**
```bash
export ASTRA_DB_ID="011475e8-2c3b-42bc-9728-62ccb8ebd5b2"
export ASTRA_DB_REGION="us-east-2"
export ASTRA_TOKEN="sua_chave_aqui"
```

**Windows (PowerShell):**
```powershell
$env:ASTRA_DB_ID="011475e8-2c3b-42bc-9728-62ccb8ebd5b2"
$env:ASTRA_DB_REGION="us-east-2"
$env:ASTRA_TOKEN="sua_chave_aqui"
```

> ⚠️ **Nunca** versione o `ASTRA_TOKEN` diretamente no código. Utilize sempre variáveis de ambiente ou um arquivo `.env` listado no `.gitignore`.

---

## ▶️ Execução

```bash
python Atividade-Cassandra.py
```

### Saída esperada no terminal

```
Conectando à API do Cassandra (Astra DB)...

✅ Conexão bem-sucedida! 3 leitura(s) recuperada(s) da nuvem:

Data: 2026-05-22 | Sensor: sensor-001 | Temp: 25.7°C | Status: OK
Data: 2026-05-22 | Sensor: sensor-001 | Temp: 25.4°C | Status: OK
Data: 2026-05-22 | Sensor: sensor-002 | Temp: 28.1°C | Status: ALERTA
```

---

## 🔍 Como Funciona

O script segue o fluxo abaixo:

1. **Carrega credenciais** das variáveis de ambiente via `AstraConfig.from_env()`
2. **Monta a URL REST** do endpoint Stargate do Astra DB
3. **Realiza requisição `GET`** com o token de autenticação no header `X-Cassandra-Token`
4. **Parseia o JSON** retornado e exibe cada leitura formatada no terminal
5. **Trata erros** de timeout, HTTP e conexão com mensagens claras

```python
# Endpoint utilizado
https://{ASTRA_DB_ID}-{ASTRA_DB_REGION}.apps.astra.datastax.com
    /api/rest/v2/keyspaces/{KEYSPACE}/{TABLE}/rows
```

---

## 📊 Métricas no Painel Astra DB

O banco **tutorial-cassandra** rodou na região **AWS us-east-2** com latência média abaixo de **5ms** durante os testes, com throughput de **2 requests** no período de monitoramento de 10 minutos.

---

## 🧠 Conceitos Aprendidos

- ✅ Modelagem de dados orientada a consultas no Cassandra (partition key + clustering key)
- ✅ Uso da API REST Stargate para acessar Cassandra sem driver nativo
- ✅ Autenticação via Application Token no Astra DB
- ✅ Boas práticas Python: `dataclasses`, separação de responsabilidades, tratamento de erros
- ✅ Gerenciamento seguro de credenciais com variáveis de ambiente

---

## 📝 .gitignore recomendado

```
.venv/
__pycache__/
*.pyc
.env
*.env
```

---

## 📄 Licença

Projeto acadêmico desenvolvido para fins educacionais — FATESG · 2026.
