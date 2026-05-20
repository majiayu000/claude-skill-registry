---
name: meta-ads-advanced
description: Advanced Meta Ads 2026 strategies — Andromeda AI, account structure, Advantage+, CAPI/EMQ, creative testing, partnership ads, and updated benchmarks
---

# Skill: Meta Ads Advanced (2026)

## O Paradigma Creative-First (Meta Andromeda)

A mudança fundamental de 2025-2026: o **criativo é o novo targeting**.

**Meta Andromeda** é o sistema de IA que funciona como retrieval engine dos anúncios:
- Avalia seus criativos (visuals, temas, copy, hooks) e **encontra usuários compatíveis**
- Criativos com baixo engagement = CPMs mais caros (penalização automática)
- Copy e visual são sinais de targeting, não só de persuasão
- GEM (Generative Recommendation Model) melhora conversões em +5%

**Implicação prática**: Invista mais em criatividade e volume de criativos do que em segmentação manual.

---

## Estrutura de Conta Ideal (2 Campanhas)

Abandone estruturas complexas por funil/audiência. Use:

| Campanha | Budget | Objetivo |
|---|---|---|
| **Creative Testing** | 10-20% do total | Identificar winners |
| **Winning Ads (Scale)** | 80-90% do total | Escalar criativos provados |

**Regras:**
- Use **CBO** sempre — algoritmo aloca melhor que você
- Campanhas com budget > R$250/dia mostram **34% melhor CPA**
- Winners: consolide em **um único ad set com broad targeting**
- Ao escalar winner, use o **Post ID original** (preserva social proof + Estimated Action Rate)

**Anti-pattern**: Campanhas separadas por funil (TOF/MOF/BOF) fragmentam dados e prejudicam aprendizagem.

---

## Advantage+ Audience (Targeting por Sinais)

Só localização e idade mínima são restrições rígidas. O resto são **sugestões**.

### Métricas documentadas de melhoria
| Métrica | Ganho |
|---|---|
| Custo por venda de catálogo | -13% |
| Custo por conversão web | -7% |
| Custo por clique/lead | -28% |

### Ordem de qualidade dos sinais
1. CAPI + Pixel combinados (server-side com match rates altas)
2. Custom Audiences com valor de compra (não só lista de emails)
3. Lookalikes 1-3% como seed inicial
4. 10-15 interesses relevantes (sugestões, não filtros)

**Requisitos mínimos:**
- 50+ conversões/semana para estabilidade
- Audiences de 2M-10M+ usuários (abaixo de 500k = fadiga + custo elevado)

---

## CAPI — Implementação Avançada

### Event Match Quality (EMQ)
Score 0-10 de capacidade de atribuição. **EMQ > 8 = performance superior**.

| Parâmetro | Impacto |
|---|---|
| Email hash (SHA-256) | Alto |
| Phone hash | Alto |
| `fbclid` / `fbc` / `fbp` | Alto |
| External ID (seu user ID) | Alto |
| IP address | Médio |
| User agent | Médio |
| Nome/Sobrenome hash | Médio |

### Dual Tracking (obrigatório para $1k+/mês)
```
Pixel (browser) ────┐
                    ├──→ Meta (deduplica por event_id)
CAPI (server) ──────┘
```
- Envie **mesmo `event_id`** em ambos canais
- Meta deduplica automaticamente

### Erros críticos
- Enviar eventos sem `event_id` de deduplicação
- Over-sending eventos irrelevantes (dilui sinais)
- Não manter (mudanças de privacidade exigem manutenção contínua)

---

## Creative Testing Framework

### Framework de 3 Níveis
| Nível | O que testar | Budget |
|---|---|---|
| **Estratégico** | Propostas de valor | Baixo |
| **Formato** | Video vs. static vs. carousel vs. UGC | Médio |
| **Execução** | Scripts, designs, hooks 3s | Alto (só após validar acima) |

Nunca escale execuções sem validar o conceito estratégico primeiro.

### Rapid Iteration
- Teste 10-15 variações simultâneas com orçamentos menores
- Pause sem sinais promissores em **48-72h ou após R$250-500**
- Escale winners imediatamente
- Cadência mínima: **1 batch de novos criativos a cada 7 dias**

### Dynamic Creative (DCO)
Upload de múltiplos assets:
- Até 10 imagens/vídeos
- Até 5 headlines, 5 descrições, 5 CTAs

O algoritmo aloca mais para combinações vencedoras. Mínimo de 50 conversões/variação antes de concluir.

### Mínimos estatísticos
- A/B test isolado: 100+ conversões/variação
- Duração mínima: 2-4 semanas
- Budget de teste: máx. 20-25% do budget diário total

---

## Advantage+ Shopping/Sales Campaigns (ASC)

Em 2025, renomeado para **Advantage+ Sales Campaigns** (expandido para leads e app installs).

### Novidades 2025-2026
- Budget Flexibility: redistribui até **20%** entre ad sets automaticamente
- Audience preferences expandidas: suporta preferências básicas dentro de Advantage+
- Advanced Measurement: integrações Nielsen, Oracle para offline conversions

### Quando NÃO usar ASC
- Conta nova (mínimo: 1.000 conversões/mês para ótima performance)
- B2B com critérios firmográficos muito estritos
- Quando brand safety é restrição crítica

---

## Partnership Ads (Creator Content como Performance Ad)

### Performance vs. brand ads tradicionais
| Métrica | Resultado |
|---|---|
| CPA | **-19%** |
| CTR | **+13%** |
| Cost per purchase | -3.9% |
| Probabilidade de superar brand ads | 82% |

71% dos consumidores fazem compra dentro de dias após ver creator content.

**Por que funciona**: Andromeda favorece conteúdo nativo ao feed → mais engagement → CPM menor.

**Setup**: Meta Business Suite com permissão do creator. Você controla targeting e spend.

---

## Benchmarks 2026

| Métrica | Benchmark |
|---|---|
| CTR médio | 1.4% – 2.19% |
| CTR leads | 2.53% |
| CPM Facebook Feed | US$ 7.47 |
| CPM Instagram Feed | US$ 7.68 |
| CPM Instagram Stories | US$ 6.25 |
| ROAS D2C prospecting | 2–3x |
| ROAS retargeting | 6–10x |
| ROAS mediano Meta | 1.93x |

---

## Contexto dos Projetos

### NewsApp
- **Conta**: act_XXXXXXXXXXXX | Pixel: XXXXXXXXXXXX
- **Campanha ativa**: META_LEADS_Newsletter — OUTCOME_LEADS, R$15/dia
- **CAPI**: Implementado (`MetaConversionsService.php`) — fbc+fbp+external_id
- **CPL target**: < R$5

### MyApp (SaaS)
- **Conta**: act_XXXXXXXXXXXX
- **Budget**: R$30/dia
- **Funil**: Meta Ads → /cadastrar → trial 14d → 7 emails → paywall
- **CPL target**: < R$15

### Token Meta
- Expira periodicamente. Localizado em `/root/.bashrc` ($META_ADS_TOKEN)
- API Graph v22.0, cache 1h

---

## Prioridades de Implementação (por impacto)

1. **CAPI com EMQ > 8** — base de tudo
2. **Consolidar no modelo 2-campaign** — pare de fragmentar
3. **Creative-first thinking** — criativo é o novo targeting
4. **Advantage+ Audience + broad** — confie no algoritmo com dados de qualidade
5. **1 batch de criativos/semana** — evitar fadiga
6. **Testar Partnership Ads** — -19% CPA com autenticidade

---

## Roadmap Meta 2026

Tendência: até fim de 2026, fluxo pode ser **objetivo + budget + URL → Meta gera tudo via IA** (imagens, copy, headlines via GEM).

**Opportunity Score (0-100)**: use para identificar gargalos de configuração antes que virem problemas de custo.
