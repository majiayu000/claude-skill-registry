---
name: monitor-legislacao
description: Monitor de mudanças legislativas
---

Monitoramento automatizado de mudanças legislativas que afetam benefícios sociais catalogados.

## Contexto

- Regras de benefícios mudam frequentemente (decretos, portarias, medidas provisórias)
- Novo CadÚnico em março/2025 mudou regras de vários programas
- Catálogo de 229+ benefícios precisa estar sempre atualizado
- Cidadão precisa saber o que mudou em linguagem simples

## Fontes Monitoradas

### Fontes Primárias
| Fonte | URL | Tipo | Frequência |
|-------|-----|------|-----------|
| Diário Oficial da União | https://www.in.gov.br | Leis, decretos, portarias | Diária |
| Planalto | https://www.planalto.gov.br/legislacao | Leis federais | Quando publica |
| LeXML | https://www.lexml.gov.br | Busca legislativa | Diária |
| MDS | https://www.gov.br/mds | Normas de assistência social | Semanal |
| INSS | https://www.gov.br/inss | Normas previdenciárias | Semanal |

### Fontes Secundárias
| Fonte | URL | Tipo |
|-------|-----|------|
| Câmara dos Deputados API | https://dadosabertos.camara.leg.br/api/v2 | Projetos de lei |
| Senado API | https://legis.senado.leg.br/dadosabertos | Tramitação |
| SAGI/MDS | https://aplicacoes.mds.gov.br/sagi | Relatórios sociais |

## Pipeline de Monitoramento

### 1. Coleta (Scraping / API)
```python
# backend/app/jobs/monitor_legislacao.py
import httpx
from bs4 import BeautifulSoup

PALAVRAS_CHAVE = [
    "bolsa família", "bpc", "loas", "cadúnico", "cadastro único",
    "tarifa social", "farmácia popular", "auxílio gás", "seguro defeso",
    "benefício", "assistência social", "renda", "transferência",
    "garantia-safra", "pis", "pasep", "fgts", "salário mínimo",
]

async def coletar_dou(data: date) -> list[dict]:
    """Coleta publicações do Diário Oficial da União por data."""
    url = f"https://www.in.gov.br/leiturajornal?data={data.strftime('%d-%m-%Y')}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    publicacoes = []
    for item in soup.select(".resultados-item"):
        titulo = item.select_one(".titulo").text.strip()
        resumo = item.select_one(".resumo").text.strip()

        # Filtrar por relevância
        texto = f"{titulo} {resumo}".lower()
        if any(palavra in texto for palavra in PALAVRAS_CHAVE):
            publicacoes.append({
                "titulo": titulo,
                "resumo": resumo,
                "url": item.select_one("a")["href"],
                "data": data.isoformat(),
                "secao": item.select_one(".secao").text.strip(),
            })
    return publicacoes

async def coletar_projetos_lei() -> list[dict]:
    """Busca projetos de lei em tramitação via API da Câmara."""
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
    params = {
        "siglaTipo": "PL,PLP,MPV,PEC",
        "keywords": "benefício social,assistência social,cadastro único",
        "tramitacaoSenado": "false",
        "ordem": "DESC",
        "ordenarPor": "id",
        "itens": 20,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    return response.json().get("dados", [])
```

### 2. Análise de Impacto
```python
# backend/app/services/analise_legislativa.py
from backend.app.agent.agent import TaNaMaoAgent

async def analisar_impacto(publicacao: dict) -> dict:
    """Usa IA para analisar impacto de mudança legislativa nos benefícios."""
    prompt = f"""
    Analise esta publicação do Diário Oficial e responda:

    Título: {publicacao['titulo']}
    Resumo: {publicacao['resumo']}

    1. Quais benefícios do Tá na Mão são afetados?
    2. O que mudou? (antes → depois)
    3. Quem é afetado?
    4. Quando entra em vigor?
    5. Resumo em linguagem simples (5ª série)

    Responda em JSON.
    """
    analise = await agent.analyze(prompt)
    return {
        "publicacao": publicacao,
        "beneficios_afetados": analise["beneficios_afetados"],
        "mudanca": analise["mudanca"],
        "publico_afetado": analise["publico_afetado"],
        "vigencia": analise["vigencia"],
        "resumo_simples": analise["resumo_simples"],
        "severidade": analise["severidade"],  # alta, media, baixa
    }
```

### 3. Atualização do Catálogo
```python
async def atualizar_catalogo(analise: dict) -> list[str]:
    """Sugere atualizações no catálogo de benefícios."""
    alteracoes = []
    for beneficio_id in analise["beneficios_afetados"]:
        alteracoes.append({
            "beneficio_id": beneficio_id,
            "campo": analise["mudanca"]["campo"],
            "valor_anterior": analise["mudanca"]["antes"],
            "valor_novo": analise["mudanca"]["depois"],
            "fonte": analise["publicacao"]["url"],
            "vigencia": analise["vigencia"],
            "status": "pendente_revisao",  # humano valida antes de aplicar
        })
    return alteracoes
```

### 4. Notificação
```python
async def notificar_mudanca(analise: dict):
    """Envia notificação sobre mudança legislativa."""
    if analise["severidade"] == "alta":
        # Notificar equipe imediatamente
        await enviar_alerta_equipe(analise)
        # Publicar no feed do app
        await publicar_feed_atualizacoes(analise)
    elif analise["severidade"] == "media":
        # Adicionar à fila de revisão
        await adicionar_fila_revisao(analise)
```

## Job Agendado
```python
# backend/app/jobs/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# Executar diariamente às 7h (após publicação do DOU)
@scheduler.scheduled_job('cron', hour=7, minute=0)
async def job_monitor_legislacao():
    hoje = date.today()
    publicacoes = await coletar_dou(hoje)

    for pub in publicacoes:
        analise = await analisar_impacto(pub)
        if analise["beneficios_afetados"]:
            await atualizar_catalogo(analise)
            await notificar_mudanca(analise)

# Projetos de lei: semanal (sexta-feira)
@scheduler.scheduled_job('cron', day_of_week='fri', hour=18)
async def job_monitor_projetos_lei():
    projetos = await coletar_projetos_lei()
    for projeto in projetos:
        analise = await analisar_impacto(projeto)
        if analise["beneficios_afetados"]:
            await registrar_projeto_relevante(projeto, analise)
```

## Template de Alerta (Linguagem Simples)
```markdown
## O que mudou?
{{resumo_simples}}

## Quem é afetado?
{{publico_afetado}}

## O que fazer?
{{acao_recomendada}}

## Quando começa a valer?
{{vigencia}}

Fonte: {{url_publicacao}}
```

## Arquivos Relacionados
- `backend/app/jobs/monitor_legislacao.py` - Job de monitoramento
- `backend/app/services/analise_legislativa.py` - Análise com IA
- `backend/app/models/atualizacao_legislativa.py` - Modelo de dados
- `frontend/src/data/benefits/` - Catálogo de benefícios

## Checklist
- [ ] Scraper do DOU funcionando
- [ ] API da Câmara integrada
- [ ] Análise de impacto com IA
- [ ] Fila de revisão humana
- [ ] Notificação à equipe
- [ ] Feed de atualizações no app
- [ ] Testes com publicações reais
