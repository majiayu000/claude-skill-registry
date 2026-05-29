---
name: impacto-esg
description: Relatórios de impacto social (ESG/ODS)
---

Geração de métricas anonimizadas de impacto social para parceiros, investidores e municípios.

## Contexto

- 95% dos brasileiros priorizam empresas com práticas ESG
- Movimento Tech 2030 (iFood, Mercado Livre) promove inclusão via tech
- Plataformas de impacto social geram dados valiosos para ESG
- Municípios precisam prestar contas sobre efetividade dos programas

## Métricas de Impacto

### Métricas Primárias (Coletadas pela Plataforma)
```python
METRICAS_IMPACTO = {
    "acesso": {
        "cidadaos_atendidos": "Número de cidadãos que usaram a plataforma",
        "consultas_realizadas": "Total de consultas de benefícios",
        "beneficios_descobertos": "Benefícios que o cidadão não sabia que tinha direito",
        "encaminhamentos_cras": "Cidadãos encaminhados ao CRAS",
        "checklists_gerados": "Documentações geradas para benefícios",
    },
    "financeiro": {
        "valor_beneficios_conectados": "Valor total de benefícios que cidadãos passaram a acessar",
        "valor_dinheiro_esquecido": "PIS/PASEP/FGTS/SVR recuperados",
        "economia_transporte": "Economia por não precisar ir ao CRAS desnecessariamente",
    },
    "inclusao": {
        "primeiro_acesso_digital": "Cidadãos usando plataforma digital pela primeira vez",
        "atendimentos_whatsapp": "Interações pelo canal mais inclusivo",
        "atendimentos_acompanhante": "Uso do modo acompanhante digital",
        "atendimentos_voz": "Interações por comando de voz",
    },
    "eficiencia": {
        "tempo_medio_consulta": "Tempo para cidadão descobrir seus benefícios",
        "reducao_fila_cras": "Estimativa de atendimentos evitados por pré-triagem digital",
        "taxa_sucesso_encaminhamento": "% de encaminhamentos que resultaram em benefício",
    },
}
```

### Alinhamento com ODS (Objetivos de Desenvolvimento Sustentável)
```
ODS 1  - Erradicação da Pobreza
  → Cidadãos conectados a transferência de renda
  → Valor de benefícios acessados

ODS 2  - Fome Zero
  → Famílias conectadas ao PAA e PNAE
  → Encaminhamentos para cestas básicas

ODS 10 - Redução das Desigualdades
  → Cobertura em municípios de baixo IDH
  → Inclusão digital de populações vulneráveis

ODS 11 - Cidades Sustentáveis
  → Mapeamento de equipamentos sociais
  → Participação em orçamento participativo

ODS 16 - Instituições Fortes
  → Transparência sobre cobertura de programas
  → Dados para gestão pública baseada em evidências
```

## Geração de Relatórios

### Relatório Mensal de Impacto
```python
# backend/app/services/relatorio_impacto.py
async def gerar_relatorio_mensal(mes: int, ano: int, escopo: str = "nacional") -> dict:
    """Gera relatório de impacto social do período."""
    metricas = await coletar_metricas(mes, ano, escopo)

    return {
        "periodo": f"{mes:02d}/{ano}",
        "escopo": escopo,
        "resumo_executivo": {
            "cidadaos_atendidos": metricas["acesso"]["cidadaos_atendidos"],
            "valor_social_gerado": metricas["financeiro"]["valor_beneficios_conectados"],
            "beneficios_descobertos": metricas["acesso"]["beneficios_descobertos"],
        },
        "detalhamento": metricas,
        "ods_impactados": calcular_impacto_ods(metricas),
        "comparativo_anterior": await comparar_periodo_anterior(mes, ano, escopo),
        "anonimizacao": "Todos os dados são agregados e anonimizados (LGPD)",
    }
```

### Dashboard para Municípios
```python
async def gerar_dashboard_municipal(municipio_ibge: str) -> dict:
    """Dashboard de impacto para gestores municipais."""
    return {
        "populacao_cadastrada": await contar_populacao_cadunico(municipio_ibge),
        "cobertura_programas": await calcular_cobertura(municipio_ibge),
        "lacunas_acesso": await identificar_lacunas(municipio_ibge),
        "tendencias": await calcular_tendencias(municipio_ibge, meses=6),
        "benchmark": await comparar_com_similares(municipio_ibge),
    }

async def identificar_lacunas(municipio_ibge: str) -> list[dict]:
    """Identifica famílias elegíveis que não acessam benefícios."""
    cobertura = await calcular_cobertura(municipio_ibge)
    lacunas = []
    for programa, dados in cobertura.items():
        if dados["taxa_cobertura"] < 0.8:  # menos de 80% de cobertura
            lacunas.append({
                "programa": programa,
                "elegíveis_estimados": dados["elegiveis"],
                "atendidos": dados["atendidos"],
                "lacuna": dados["elegiveis"] - dados["atendidos"],
                "taxa_cobertura": f"{dados['taxa_cobertura']*100:.1f}%",
            })
    return sorted(lacunas, key=lambda x: x["lacuna"], reverse=True)
```

### Relatório para Parceiros/Investidores
```python
async def gerar_relatorio_parceiro(parceiro_id: str, periodo: str) -> dict:
    """Relatório formatado para parceiro ESG."""
    return {
        "parceiro": parceiro_id,
        "periodo": periodo,
        "impacto_direto": {
            "vidas_impactadas": 0,
            "valor_social_gerado_brl": 0,
            "municipios_alcancados": 0,
        },
        "ods_contribuicao": [],
        "historias_anonimizadas": await buscar_historias_sucesso(anonimizar=True),
        "metodologia": "Dados agregados e anonimizados conforme LGPD. "
                       "Métricas auditáveis via pipeline de dados abertos.",
        "selo": "Impacto Social Verificado - Tá na Mão",
    }
```

## Anonimização (LGPD)
```python
# Regras de anonimização para relatórios
REGRAS_ANONIMIZACAO = {
    "cpf": "NUNCA incluir, nem hasheado",
    "nome": "NUNCA incluir",
    "endereco": "Agregar por município (mínimo)",
    "renda": "Agregar por faixa (extrema pobreza, pobreza, baixa renda)",
    "beneficios": "Contar por programa, nunca por pessoa",
    "minimo_grupo": 10,  # mínimo 10 pessoas por agregação para evitar reidentificação
}
```

## Export de Relatórios
```python
# Formatos disponíveis
FORMATOS_EXPORT = {
    "json": "API endpoint para integração",
    "pdf": "Relatório formatado para apresentações",
    "xlsx": "Planilha para análise (usar skill xlsx)",
    "csv": "Dados tabulares para BI tools",
}
```

## Arquivos Relacionados
- `backend/app/services/relatorio_impacto.py` - Geração de relatórios
- `backend/app/routers/admin.py` - Endpoints administrativos
- `backend/app/services/anonimizacao.py` - Regras de anonimização
- `.claude/skills/xlsx.md` - Geração de planilhas Excel

## Referências
- ODS Brasil: https://odsbrasil.gov.br/
- GRI Standards: https://www.globalreporting.org/standards/
- Movimento Tech 2030: https://movimentotech2030.com.br/
- GIFE (Investimento Social Privado): https://gife.org.br/
