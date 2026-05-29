---
name: painel-gestor
description: Dashboard para gestores municipais
---

Painel analítico para secretarias de assistência social com métricas de cobertura, lacunas e planejamento.

## Contexto

- Rede GOV.BR expandiu de 160 para 2.000+ municípios
- Gestores locais precisam de dados acionáveis para planejamento
- Cobertura de benefícios varia enormemente entre municípios
- Prestação de contas é obrigatória (Tribunal de Contas, MDS)

## Público-Alvo

```
├── Secretário(a) de Assistência Social
├── Coordenador(a) do CRAS / CREAS
├── Gestor(a) do CadÚnico
├── Prefeito(a) / Vice
└── Conselho Municipal de Assistência Social
```

## Módulos do Dashboard

### 1. Visão Geral do Município
```python
# backend/app/services/dashboard_gestor.py
async def visao_geral(municipio_ibge: str) -> dict:
    """Dados de visão geral para o dashboard do gestor."""
    return {
        "populacao": await ibge.populacao(municipio_ibge),
        "familias_cadunico": await sagi.familias_cadunico(municipio_ibge),
        "cobertura_cadunico_pct": 0,  # calculado
        "beneficios_ativos": {
            "bolsa_familia": {"familias": 0, "valor_mensal": 0},
            "bpc": {"beneficiarios": 0, "valor_mensal": 0},
            "tarifa_social": {"domicilios": 0},
            "farmacia_popular": {"atendimentos_mes": 0},
        },
        "equipamentos_suas": {
            "cras": await contar_equipamentos(municipio_ibge, "cras"),
            "creas": await contar_equipamentos(municipio_ibge, "creas"),
            "centro_pop": await contar_equipamentos(municipio_ibge, "centro_pop"),
        },
        "kpis": await calcular_kpis(municipio_ibge),
    }
```

### 2. Análise de Lacunas
```python
async def analise_lacunas(municipio_ibge: str) -> dict:
    """Identifica famílias elegíveis que NÃO acessam benefícios."""
    populacao = await ibge.populacao(municipio_ibge)
    renda = await ibge.distribuicao_renda(municipio_ibge)
    cobertura = await calcular_cobertura_por_programa(municipio_ibge)

    lacunas = []
    for programa, dados in cobertura.items():
        if dados["taxa_cobertura"] < 0.9:  # menos de 90%
            lacunas.append({
                "programa": programa,
                "elegiveis_estimados": dados["elegiveis"],
                "atendidos": dados["atendidos"],
                "nao_atendidos": dados["elegiveis"] - dados["atendidos"],
                "taxa_cobertura": dados["taxa_cobertura"],
                "valor_nao_acessado_mensal": dados["valor_medio"] * (dados["elegiveis"] - dados["atendidos"]),
                "acao_sugerida": sugerir_acao(programa, dados),
            })

    return {
        "lacunas": sorted(lacunas, key=lambda x: x["nao_atendidos"], reverse=True),
        "valor_total_nao_acessado": sum(l["valor_nao_acessado_mensal"] for l in lacunas),
        "recomendacoes": [
            "Realizar busca ativa nos bairros com menor cobertura",
            "Organizar mutirão de cadastramento no CadÚnico",
            "Parcerias com UBS e escolas para identificar famílias",
        ],
    }
```

### 3. Mapa de Calor de Vulnerabilidade
```python
async def mapa_vulnerabilidade(municipio_ibge: str) -> dict:
    """Gera dados para mapa de calor por setor censitário/bairro."""
    setores = await ibge.setores_censitarios(municipio_ibge)

    camadas = []
    for setor in setores:
        camadas.append({
            "setor_id": setor["id"],
            "geometria": setor["geometria"],
            "indicadores": {
                "renda_media": setor["renda_domiciliar_media"],
                "taxa_pobreza": setor["pct_abaixo_linha_pobreza"],
                "cobertura_bf": setor["pct_familias_bolsa_familia"],
                "saneamento": setor["pct_domicilios_saneamento"],
            },
            "score_vulnerabilidade": calcular_score_setor(setor),
        })

    return {
        "municipio_ibge": municipio_ibge,
        "camadas": camadas,
        "legenda": {
            "verde": "Baixa vulnerabilidade",
            "amarelo": "Vulnerabilidade moderada",
            "laranja": "Alta vulnerabilidade",
            "vermelho": "Vulnerabilidade crítica",
        },
    }
```

### 4. Tendências Temporais
```python
async def tendencias(municipio_ibge: str, meses: int = 12) -> dict:
    """Evolução dos indicadores ao longo do tempo."""
    series = {}
    for programa in ["bolsa_familia", "bpc", "tarifa_social"]:
        series[programa] = await buscar_serie_temporal(
            municipio_ibge, programa, meses
        )

    return {
        "series": series,
        "alertas": detectar_anomalias(series),  # quedas ou picos abruptos
    }
```

### 5. Benchmark com Municípios Similares
```python
async def benchmark(municipio_ibge: str) -> dict:
    """Compara com municípios de mesmo porte e região."""
    perfil = await ibge.perfil_municipio(municipio_ibge)
    similares = await buscar_municipios_similares(
        populacao_faixa=perfil["faixa_populacao"],
        uf=perfil["uf"],
        limit=10,
    )

    comparativo = []
    for similar in similares:
        comparativo.append({
            "municipio": similar["nome"],
            "ibge": similar["ibge"],
            "populacao": similar["populacao"],
            "cobertura_bf": similar["cobertura_bf"],
            "idh_m": similar["idh_m"],
            "equipamentos_suas_per_capita": similar["suas_per_capita"],
        })

    return {
        "municipio_referencia": municipio_ibge,
        "similares": comparativo,
        "posicao_ranking": calcular_posicao(municipio_ibge, comparativo),
    }
```

## API Endpoints
```python
# backend/app/routers/admin.py
@router.get("/admin/dashboard/{municipio_ibge}")
async def dashboard(municipio_ibge: str, token: str = Depends(auth_gestor)):
    return await visao_geral(municipio_ibge)

@router.get("/admin/lacunas/{municipio_ibge}")
async def lacunas(municipio_ibge: str, token: str = Depends(auth_gestor)):
    return await analise_lacunas(municipio_ibge)

@router.get("/admin/mapa/{municipio_ibge}")
async def mapa(municipio_ibge: str, token: str = Depends(auth_gestor)):
    return await mapa_vulnerabilidade(municipio_ibge)

@router.get("/admin/tendencias/{municipio_ibge}")
async def tendencias_endpoint(municipio_ibge: str, meses: int = 12):
    return await tendencias(municipio_ibge, meses)

@router.get("/admin/benchmark/{municipio_ibge}")
async def benchmark_endpoint(municipio_ibge: str):
    return await benchmark(municipio_ibge)

@router.get("/admin/relatorio/{municipio_ibge}")
async def relatorio_pdf(municipio_ibge: str, formato: str = "pdf"):
    return await gerar_relatorio_gestor(municipio_ibge, formato)
```

## Autenticação de Gestores
```python
# Gestores autenticam via Gov.br (nível Prata+)
# + verificação de vínculo com o município
async def auth_gestor(token: str) -> GestorAutenticado:
    user = await verificar_token_govbr(token)
    vinculo = await verificar_vinculo_municipal(user.cpf, municipio_ibge)
    if not vinculo:
        raise HTTPException(403, "Sem vínculo com este município")
    return GestorAutenticado(user=user, municipio=municipio_ibge, perfil=vinculo.perfil)
```

## Arquivos Relacionados
- `backend/app/services/dashboard_gestor.py` - Serviço principal
- `backend/app/routers/admin.py` - Endpoints (existente, expandir)
- `backend/app/services/indicadores/` - Serviços IBGE/IPEA
- `backend/app/models/municipality.py` - Dados municipais

## Referências
- MDS TabSocial: https://aplicacoes.mds.gov.br/sagi/tabsocial/
- IBGE Cidades: https://cidades.ibge.gov.br/
- Mapa SUAS: https://mapas.mds.gov.br/
