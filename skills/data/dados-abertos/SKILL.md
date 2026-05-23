---
name: dados-abertos
description: Pipeline de dados abertos governamentais
---

Consumo automatizado de datasets abertos para manter o catálogo de benefícios atualizado.

## Contexto

- Portal da Transparência (CGU) publica dados mensais de todos os programas federais
- dados.gov.br tem datasets estruturados de benefícios
- R$441 bilhões/ano em programas sociais
- 40+ programas federais usam CadÚnico
- Catálogo de 229+ benefícios precisa de atualização contínua

## Fontes de Dados Abertos

### Federais
| Fonte | URL | Dados | Formato | Frequência |
|-------|-----|-------|---------|-----------|
| Portal da Transparência | portaldatransparencia.gov.br | Bolsa Família, BPC, Auxílio Gás, Seguro Defeso | CSV | Mensal |
| dados.gov.br | dados.gov.br | Benefícios concedidos, CadÚnico agregado | CSV/JSON | Variável |
| SAGI/MDS | aplicacoes.mds.gov.br/sagi | Relatórios sociais, painéis | API/CSV | Mensal |
| OpenDataSUS | opendatasus.saude.gov.br | Farmácia Popular, Dignidade Menstrual | CSV | Mensal |
| ANEEL | dados.aneel.gov.br | Tarifa Social de Energia | CSV | Mensal |
| IBGE | api.ibge.gov.br | População, PIB, indicadores | API JSON | Anual |
| IPEA | ipeadata.gov.br | Indicadores sociais, Gini, IDH | API | Variável |
| FNDE | dados.fnde.gov.br | PNAE (merenda escolar) | OData | Mensal |

### APIs Estruturadas
```python
APIS_DADOS_ABERTOS = {
    "ibge_localidades": {
        "url": "https://servicodados.ibge.gov.br/api/v1/localidades",
        "endpoints": [
            "/estados",
            "/municipios",
            "/distritos",
        ],
        "formato": "json",
    },
    "ibge_indicadores": {
        "url": "https://servicodados.ibge.gov.br/api/v3/agregados",
        "endpoints": [
            "/4714/periodos/-6/variaveis/93?localidades=N1[all]",  # População
            "/5938/periodos/-6/variaveis/37?localidades=N6[all]",  # PIB municipal
        ],
        "formato": "json",
    },
    "sagi_cecad": {
        "url": "https://cecad.cidadania.gov.br/api",
        "endpoints": [
            "/dashboard/uf",
            "/dashboard/municipio/{ibge}",
        ],
        "formato": "json",
        "auth": "token",
    },
    "transparencia": {
        "url": "https://api.portaldatransparencia.gov.br/api-de-dados",
        "endpoints": [
            "/bolsa-familia-disponivel-por-municipio",
            "/bpc-por-municipio",
            "/auxilio-emergencial-por-municipio",
        ],
        "formato": "json",
        "auth": "api_key",
        "rate_limit": "30/min",
    },
}
```

## Pipeline ETL

### 1. Extração
```python
# backend/app/jobs/dados_abertos/extrator.py
import httpx
import csv
import io

class ExtratorDadosAbertos:
    async def extrair_transparencia_bolsa_familia(self, mes: int, ano: int) -> list[dict]:
        """Extrai dados de Bolsa Família do Portal da Transparência."""
        url = f"https://portaldatransparencia.gov.br/download-de-dados/bolsa-familia-pagamentos/{ano}{mes:02d}"
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.get(url)

        # CSV com encoding latin-1 (padrão governo)
        content = response.content.decode('latin-1')
        reader = csv.DictReader(io.StringIO(content), delimiter=';')
        return [row for row in reader]

    async def extrair_ibge_populacao(self) -> list[dict]:
        """Extrai população por município via API IBGE."""
        url = "https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/-1/variaveis/93"
        params = {"localidades": "N6[all]"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        return response.json()

    async def extrair_sagi_cadunico(self, ibge: str) -> dict:
        """Extrai dados CadÚnico por município via SAGI."""
        url = f"https://cecad.cidadania.gov.br/api/dashboard/municipio/{ibge}"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {settings.SAGI_TOKEN}"}
            )
        return response.json()
```

### 2. Transformação
```python
# backend/app/jobs/dados_abertos/transformador.py
class TransformadorDados:
    def transformar_bolsa_familia(self, dados_brutos: list[dict]) -> list[dict]:
        """Transforma dados brutos do CSV em formato padronizado."""
        agregado = {}
        for row in dados_brutos:
            ibge = row["CÓDIGO MUNICÍPIO IBGE"]
            if ibge not in agregado:
                agregado[ibge] = {
                    "municipio_ibge": ibge,
                    "programa": "bolsa_familia",
                    "total_beneficiarios": 0,
                    "valor_total": 0,
                }
            agregado[ibge]["total_beneficiarios"] += 1
            valor = float(row["VALOR PARCELA"].replace(",", "."))
            agregado[ibge]["valor_total"] += valor

        return list(agregado.values())

    def validar_dados(self, dados: list[dict], schema: str) -> tuple[list, list]:
        """Valida dados transformados contra schema esperado."""
        validos = []
        invalidos = []
        for item in dados:
            try:
                validado = SCHEMAS[schema].model_validate(item)
                validos.append(validado)
            except ValidationError as e:
                invalidos.append({"item": item, "erros": str(e)})
        return validos, invalidos
```

### 3. Carga
```python
# backend/app/jobs/dados_abertos/carregador.py
class CarregadorDados:
    async def carregar_beneficiarios(self, dados: list[dict]):
        """Carrega dados transformados no banco."""
        async with get_session() as session:
            for item in dados:
                stmt = insert(BeneficiaryData).values(**item).on_conflict_do_update(
                    index_elements=["municipio_ibge", "programa", "referencia"],
                    set_={
                        "total_beneficiarios": item["total_beneficiarios"],
                        "valor_total": item["valor_total"],
                        "atualizado_em": datetime.utcnow(),
                    }
                )
                await session.execute(stmt)
            await session.commit()
```

### 4. Orquestração
```python
# backend/app/jobs/dados_abertos/orquestrador.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

JOBS_DADOS_ABERTOS = [
    {"nome": "bolsa_familia", "cron": "0 3 5 * *",    "descricao": "Dia 5 de cada mês às 3h"},
    {"nome": "bpc",           "cron": "0 3 6 * *",    "descricao": "Dia 6 de cada mês às 3h"},
    {"nome": "farmacia",      "cron": "0 4 7 * *",    "descricao": "Dia 7 de cada mês às 4h"},
    {"nome": "tsee",          "cron": "0 4 8 * *",    "descricao": "Dia 8 de cada mês às 4h"},
    {"nome": "populacao",     "cron": "0 5 1 1,7 *",  "descricao": "Jan e Jul, dia 1 às 5h"},
    {"nome": "indicadores",   "cron": "0 5 1 1 *",    "descricao": "Janeiro, dia 1 às 5h"},
]

async def executar_pipeline(nome: str):
    """Executa pipeline completo: extrair → transformar → validar → carregar."""
    extrator = ExtratorDadosAbertos()
    transformador = TransformadorDados()
    carregador = CarregadorDados()

    # Extrair
    dados_brutos = await getattr(extrator, f"extrair_{nome}")()

    # Transformar
    dados = getattr(transformador, f"transformar_{nome}")(dados_brutos)

    # Validar
    validos, invalidos = transformador.validar_dados(dados, nome)
    if invalidos:
        await alertar_dados_invalidos(nome, invalidos)

    # Carregar
    await carregador.carregar_beneficiarios(validos)

    return {"processados": len(validos), "invalidos": len(invalidos)}
```

## Monitoramento
```python
# Alertas de qualidade de dados
ALERTAS = {
    "dados_ausentes": "Fonte {fonte} não retornou dados para {mes}/{ano}",
    "queda_brusca": "Beneficiários de {programa} caíram {pct}% vs. mês anterior",
    "aumento_brusco": "Valor total de {programa} subiu {pct}% vs. mês anterior",
    "fonte_indisponivel": "API {fonte} retornou erro {status_code}",
}
```

## Arquivos Relacionados
- `backend/app/jobs/dados_abertos/` - Pipeline ETL
- `backend/app/jobs/ingest/` - Jobs de ingestão existentes
- `backend/app/models/beneficiary_data.py` - Modelo de dados
- `backend/docs/DATA_SOURCES.md` - Documentação de fontes

## Comandos
```bash
# Executar pipeline manualmente
python -m backend.app.jobs.dados_abertos.orquestrador --job=bolsa_familia --mes=1 --ano=2026

# Verificar última atualização
python -m backend.app.jobs.dados_abertos.status

# Validar dados sem carregar (dry-run)
python -m backend.app.jobs.dados_abertos.orquestrador --job=bpc --dry-run
```

## Referências
- Portal da Transparência: https://portaldatransparencia.gov.br/download-de-dados
- dados.gov.br: https://dados.gov.br/
- API IBGE: https://servicodados.ibge.gov.br/api/docs
- SAGI/MDS: https://aplicacoes.mds.gov.br/sagi/
- API Portal da Transparência: https://api.portaldatransparencia.gov.br/swagger-ui/index.html
