---
name: vulnerabilidade-preditiva
description: Score de risco social e recomendações proativas
---

Score de risco social para sugestão proativa de benefícios e prevenção de perda de direitos.

## Contexto

- Prevenção é mais eficaz que remediação
- Famílias perdem benefícios por cadastro vencido sem saber
- Muitos não conhecem benefícios que têm direito
- IA pode identificar padrões de vulnerabilidade a partir do perfil

## Score de Vulnerabilidade

### Dimensões do Score (0 a 100)
```
Score = soma ponderada de fatores

Dimensão          | Peso | Indicadores
-------------------|------|----------------------------------
Renda              | 30%  | Renda per capita, fonte de renda, estabilidade
Composição familiar| 20%  | Crianças <6, gestantes, idosos, PCD
Moradia            | 15%  | Tipo, posse, saneamento, localização
Trabalho           | 15%  | Formal/informal, desemprego, subemprego
Proteção social    | 10%  | Benefícios ativos, CadÚnico atualizado
Território         | 10%  | IDH-M, cobertura SUAS, zona rural/urbana
```

### Faixas de Risco
```
0-25:  BAIXO      → Monitoramento periódico
26-50: MODERADO   → Verificar novos benefícios elegíveis
51-75: ALTO       → Ação preventiva (alertas, orientação)
76-100: CRÍTICO   → Encaminhamento urgente para CRAS/CREAS
```

## Implementação

### Cálculo do Score
```python
# backend/app/services/score_vulnerabilidade.py
from dataclasses import dataclass

@dataclass
class PerfilFamiliar:
    renda_per_capita: float
    membros_familia: int
    criancas_0_6: int
    gestantes: int
    idosos_60_mais: int
    pessoas_com_deficiencia: int
    tipo_moradia: str       # propria, alugada, cedida, ocupacao, rua
    trabalho_formal: bool
    desempregados: int
    beneficios_ativos: list[str]
    cadunico_atualizado: bool
    meses_desde_atualizacao: int
    municipio_ibge: str
    zona: str               # urbana, rural

def calcular_score(perfil: PerfilFamiliar, dados_territorio: dict) -> dict:
    score = 0
    fatores = []

    # --- RENDA (0-30 pontos) ---
    if perfil.renda_per_capita == 0:
        score += 30
        fatores.append("Sem renda declarada")
    elif perfil.renda_per_capita <= 105:
        score += 25
        fatores.append("Extrema pobreza (até R$105/pessoa)")
    elif perfil.renda_per_capita <= 218:
        score += 20
        fatores.append("Pobreza (até R$218/pessoa)")
    elif perfil.renda_per_capita <= 660:
        score += 10
        fatores.append("Baixa renda (até R$660/pessoa)")

    # --- COMPOSIÇÃO FAMILIAR (0-20 pontos) ---
    if perfil.criancas_0_6 > 0:
        score += min(perfil.criancas_0_6 * 3, 8)
        fatores.append(f"{perfil.criancas_0_6} criança(s) pequena(s)")
    if perfil.gestantes > 0:
        score += 5
        fatores.append("Gestante na família")
    if perfil.idosos_60_mais > 0:
        score += 4
        fatores.append("Idoso(s) na família")
    if perfil.pessoas_com_deficiencia > 0:
        score += 5
        fatores.append("Pessoa(s) com deficiência")

    # --- MORADIA (0-15 pontos) ---
    moradia_scores = {
        "rua": 15, "ocupacao": 12, "cedida": 8,
        "alugada": 5, "propria": 0,
    }
    score += moradia_scores.get(perfil.tipo_moradia, 5)

    # --- TRABALHO (0-15 pontos) ---
    if not perfil.trabalho_formal:
        score += 8
        fatores.append("Sem trabalho formal")
    if perfil.desempregados > 0:
        score += min(perfil.desempregados * 4, 15)
        fatores.append(f"{perfil.desempregados} desempregado(s)")

    # --- PROTEÇÃO SOCIAL (0-10 pontos) ---
    if not perfil.cadunico_atualizado:
        score += 5
        fatores.append("CadÚnico desatualizado")
    if perfil.meses_desde_atualizacao >= 20:
        score += 5
        fatores.append("CadÚnico próximo de vencer")

    # --- TERRITÓRIO (0-10 pontos) ---
    idh_m = dados_territorio.get("idh_m", 0.7)
    if idh_m < 0.55:
        score += 10
        fatores.append("Município com IDH muito baixo")
    elif idh_m < 0.65:
        score += 6
    if perfil.zona == "rural":
        score += 3
        fatores.append("Zona rural")

    # Limitar a 100
    score = min(score, 100)

    return {
        "score": score,
        "faixa": classificar_faixa(score),
        "fatores": fatores,
        "recomendacoes": gerar_recomendacoes(perfil, score),
    }
```

### Recomendações Proativas
```python
def gerar_recomendacoes(perfil: PerfilFamiliar, score: int) -> list[dict]:
    """Gera recomendações baseadas no perfil e score."""
    recomendacoes = []

    # Benefícios não acessados
    if perfil.renda_per_capita <= 218 and "bolsa_familia" not in perfil.beneficios_ativos:
        recomendacoes.append({
            "tipo": "beneficio_nao_acessado",
            "beneficio": "Bolsa Família",
            "mensagem": "Você pode ter direito ao Bolsa Família. Procure o CRAS.",
            "prioridade": "alta",
        })

    if perfil.idosos_60_mais > 0 and perfil.renda_per_capita <= 353:
        if "bpc_idoso" not in perfil.beneficios_ativos:
            recomendacoes.append({
                "tipo": "beneficio_nao_acessado",
                "beneficio": "BPC Idoso",
                "mensagem": "O idoso da família pode ter direito ao BPC (1 salário mínimo/mês).",
                "prioridade": "alta",
            })

    # CadÚnico vencendo
    if perfil.meses_desde_atualizacao >= 20:
        recomendacoes.append({
            "tipo": "alerta_cadastro",
            "mensagem": f"Seu CadÚnico vence em {24 - perfil.meses_desde_atualizacao} meses. Atualize no CRAS.",
            "prioridade": "alta" if perfil.meses_desde_atualizacao >= 22 else "media",
        })

    # Tarifa social
    if perfil.renda_per_capita <= 660 and "tarifa_social" not in perfil.beneficios_ativos:
        recomendacoes.append({
            "tipo": "beneficio_nao_acessado",
            "beneficio": "Tarifa Social de Energia",
            "mensagem": "Você pode ter desconto na conta de luz. Peça na sua distribuidora.",
            "prioridade": "media",
        })

    return sorted(recomendacoes, key=lambda r: {"alta": 0, "media": 1, "baixa": 2}[r["prioridade"]])
```

## Uso no Agente
```python
# Após consulta de benefícios, calcular score e sugerir
async def pos_consulta(cpf: str, session: Session):
    perfil = await construir_perfil(cpf)
    resultado = calcular_score(perfil, await dados_territorio(perfil.municipio_ibge))

    if resultado["recomendacoes"]:
        mensagem = "Encontrei algumas coisas que podem te ajudar:\n\n"
        for rec in resultado["recomendacoes"]:
            mensagem += f"• {rec['mensagem']}\n"
        await session.send(mensagem)
```

## Privacidade e Ética
- Score NUNCA é compartilhado com terceiros
- Dados usados apenas para recomendar benefícios
- Cidadão pode optar por não receber recomendações
- Score não é usado para negar serviços (apenas para ampliar acesso)
- Sem discriminação algorítmica: todas as faixas recebem sugestões

## Arquivos Relacionados
- `backend/app/services/score_vulnerabilidade.py` - Cálculo do score
- `backend/app/services/recomendacoes.py` - Motor de recomendações
- `backend/app/services/eligibility_service.py` - Serviço de elegibilidade
- `backend/app/models/municipality.py` - Dados territoriais

## Referências
- Escala Brasileira de Insegurança Alimentar (EBIA): IBGE
- Índice de Vulnerabilidade Social (IVS): IPEA
- IDH-M: Atlas do Desenvolvimento Humano (PNUD)
