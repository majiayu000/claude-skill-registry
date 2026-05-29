---
name: indicadores-sociais
description: Painel de indicadores sociais (IBGE/IPEA/MDS)
---

Consumo de APIs do IBGE, IPEA e SAGI/MDS para visualização de indicadores sociais por território.

## Contexto

- Dados sociais existem mas são inacessíveis para gestores locais e sociedade civil
- Censo 2022 trouxe dados atualizados após 12 anos
- IPEA, IBGE e MDS publicam indicadores mas em formatos técnicos
- Correlacionar cobertura de benefícios com bem-estar é essencial para políticas públicas

## Indicadores Disponíveis

### IBGE (Censo 2022 + Pesquisas)
| Indicador | API | Agregação |
|-----------|-----|-----------|
| População total | SIDRA tabela 4714 | Município |
| Renda domiciliar per capita | SIDRA tabela 6579 | Município |
| Taxa de analfabetismo | SIDRA tabela 3540 | Município |
| Domicílios com saneamento | SIDRA tabela 6445 | Município |
| Pirâmide etária | SIDRA tabela 9514 | Município |
| Tipo de moradia | SIDRA tabela 6373 | Município |

### IPEA
| Indicador | Código | Descrição |
|-----------|--------|-----------|
| IDH-M | IDHM | Índice de Desenvolvimento Humano Municipal |
| Gini | GINI | Coeficiente de desigualdade de renda |
| IVS | IVS | Índice de Vulnerabilidade Social |
| Taxa de pobreza | TXPOB | % da população abaixo da linha de pobreza |

### SAGI/MDS
| Indicador | Fonte | Descrição |
|-----------|-------|-----------|
| Famílias no CadÚnico | CECAD | Total por faixa de renda |
| Cobertura Bolsa Família | TabSocial | Famílias atendidas vs. elegíveis |
| Equipamentos SUAS | Censo SUAS | CRAS, CREAS por município |
| Taxa de atualização CadÚnico | CECAD | % cadastros em dia |

## APIs

### IBGE SIDRA
```python
# backend/app/services/indicadores/ibge.py
import httpx

class IBGEService:
    BASE_URL = "https://apisidra.ibge.gov.br/values"

    async def populacao_municipio(self, ibge: str) -> dict:
        """Busca população do Censo 2022."""
        url = f"{self.BASE_URL}/t/4714/n6/{ibge}/v/93/p/last"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        dados = response.json()
        return {
            "municipio_ibge": ibge,
            "populacao": int(dados[1]["V"]),
            "ano": dados[1]["D3N"],
        }

    async def renda_per_capita(self, ibge: str) -> dict:
        """Busca renda domiciliar per capita."""
        url = f"{self.BASE_URL}/t/6579/n6/{ibge}/v/all/p/last"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        dados = response.json()
        return {
            "municipio_ibge": ibge,
            "renda_per_capita": float(dados[1]["V"]),
            "ano": dados[1]["D3N"],
        }

    async def perfil_demografico(self, ibge: str) -> dict:
        """Busca perfil demográfico completo."""
        populacao = await self.populacao_municipio(ibge)
        renda = await self.renda_per_capita(ibge)
        return {**populacao, **renda}
```

### IPEA Data
```python
# backend/app/services/indicadores/ipea.py
class IPEAService:
    BASE_URL = "http://www.ipeadata.gov.br/api/odata4"

    async def idh_municipal(self, ibge: str) -> dict:
        """Busca IDH-M via API IPEA."""
        url = f"{self.BASE_URL}/ValoresSerie(SERCODIGO='ADH_IDHM')"
        params = {"$filter": f"TERCODIGO eq '{ibge}'", "$orderby": "VALDATA desc", "$top": 1}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        dados = response.json()["value"]
        if dados:
            return {
                "municipio_ibge": ibge,
                "idh_m": dados[0]["VALVALOR"],
                "ano": dados[0]["VALDATA"][:4],
            }
        return None

    async def indice_gini(self, ibge: str) -> dict:
        """Busca coeficiente de Gini."""
        url = f"{self.BASE_URL}/ValoresSerie(SERCODIGO='ADH_GINI')"
        params = {"$filter": f"TERCODIGO eq '{ibge}'", "$orderby": "VALDATA desc", "$top": 1}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        dados = response.json()["value"]
        if dados:
            return {
                "municipio_ibge": ibge,
                "gini": dados[0]["VALVALOR"],
                "ano": dados[0]["VALDATA"][:4],
                "interpretacao": interpretar_gini(dados[0]["VALVALOR"]),
            }
        return None
```

### Painel Consolidado
```python
# backend/app/services/indicadores/painel.py
async def painel_municipal(ibge: str) -> dict:
    """Painel consolidado de indicadores sociais do município."""
    ibge_svc = IBGEService()
    ipea_svc = IPEAService()

    # Buscar em paralelo
    populacao, renda, idh, gini, cobertura = await asyncio.gather(
        ibge_svc.populacao_municipio(ibge),
        ibge_svc.renda_per_capita(ibge),
        ipea_svc.idh_municipal(ibge),
        ipea_svc.indice_gini(ibge),
        calcular_cobertura_beneficios(ibge),
    )

    return {
        "municipio_ibge": ibge,
        "demografia": populacao,
        "renda": renda,
        "desenvolvimento": idh,
        "desigualdade": gini,
        "cobertura_social": cobertura,
        "comparativo_uf": await comparar_com_estado(ibge),
        "comparativo_brasil": await comparar_com_nacional(ibge),
    }

async def comparativo_municipios(lista_ibge: list[str]) -> list[dict]:
    """Compara indicadores entre municípios."""
    paineis = await asyncio.gather(*[painel_municipal(ibge) for ibge in lista_ibge])
    return sorted(paineis, key=lambda p: p.get("desenvolvimento", {}).get("idh_m", 0))
```

## Interpretações em Linguagem Simples
```python
def interpretar_gini(valor: float) -> str:
    if valor < 0.40:
        return "A renda é distribuída de forma razoável neste município."
    elif valor < 0.55:
        return "Existe desigualdade moderada de renda."
    else:
        return "A desigualdade de renda é alta neste município."

def interpretar_idh(valor: float) -> str:
    if valor >= 0.800:
        return "Desenvolvimento humano muito alto."
    elif valor >= 0.700:
        return "Desenvolvimento humano alto."
    elif valor >= 0.550:
        return "Desenvolvimento humano médio."
    else:
        return "Desenvolvimento humano baixo. Atenção especial necessária."
```

## Arquivos Relacionados
- `backend/app/services/indicadores/ibge.py` - Serviço IBGE
- `backend/app/services/indicadores/ipea.py` - Serviço IPEA
- `backend/app/services/indicadores/painel.py` - Painel consolidado
- `backend/app/routers/admin.py` - Endpoints admin (dashboard)
- `backend/app/models/municipality.py` - Dados municipais

## Referências
- API SIDRA IBGE: https://apisidra.ibge.gov.br/
- API IBGE Localidades: https://servicodados.ibge.gov.br/api/docs
- IPEA Data: http://www.ipeadata.gov.br/
- Atlas do Desenvolvimento Humano: http://www.atlasbrasil.org.br/
- CECAD/SAGI: https://cecad.cidadania.gov.br/
