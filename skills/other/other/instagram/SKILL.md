---
name: instagram
description: Integracao completa com Instagram via Graph API. Publicacao, analytics, comentarios, DMs, hashtags, agendamento, templates e gestao de contas Business/Creator.
risk: critical
source: community
date_added: '2026-03-06'
author: renat
tags:
- social-media
- instagram
- graph-api
- content
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Skill: Instagram Integration

## Overview

Integracao completa com Instagram via Graph API. Publicacao, analytics, comentarios, DMs, hashtags, agendamento, templates e gestao de contas Business/Creator.

## When to Use This Skill

- When the user mentions "instagram" or related topics
- When the user mentions "ig" or related topics
- When the user mentions "post instagram" or related topics
- When the user mentions "publicar instagram" or related topics
- When the user mentions "reels instagram" or related topics
- When the user mentions "stories instagram" or related topics

## Do Not Use This Skill When

- The task is unrelated to instagram
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Controle completo da conta Instagram via Graph API. Publicação, comunidade, analytics,
DMs, hashtags, templates e dashboard — tudo gerido com governança (rate limits, audit log,
confirmações antes de ações públicas).

## Resumo Rápido

| Área | Scripts | O que faz |
|------|---------|-----------|
| **Setup** | `account_setup.py`, `auth.py` | Configurar conta, OAuth, token |
| **Publicação** | `publish.py`, `schedule.py` | Publicar foto/vídeo/reel/story/carrossel, agendar |
| **Comunidade** | `comments.py`, `messages.py` | Comentários, DMs, menções |
| **Analytics** | `insights.py`, `analyze.py` | Métricas, melhores horários, top posts |
| **Hashtags** | `hashtags.py` | Pesquisa e tracking |
| **Inteligência** | `templates.py`, `analyze.py` | Templates de conteúdo, tendências |
| **Infra** | `export.py`, `serve_api.py`, `run_all.py` | Exportar, dashboard, sync |
| **Leitura** | `profile.py`, `media.py` | Perfil, listar mídia |

## Localização

```
C:\Users\renat\skills\instagram\
├── SKILL.md
├── scripts/
│   ├── requirements.txt
│   │  # ── CORE ──
│   ├── config.py                     # Paths, constantes, specs de mídia
│   ├── db.py                         # SQLite: accounts, posts, comments, insights
│   ├── auth.py                       # OAuth 2.0, token storage/refresh
│   ├── api_client.py                 # Instagram Graph API wrapper + retry
│   ├── governance.py                 # Rate limits, audit log, confirmações
│   │  # ── FEATURES ──
│   ├── account_setup.py              # Detecção conta, migração, verificação
│   ├── publish.py                    # Publicar + upload local via Imgur
│   ├── schedule.py                   # Orquestrador: approved → published
│   ├── comments.py                   # Ler/responder/deletar comentários
│   ├── messages.py                   # DMs (enviar/receber/listar)
│   ├── insights.py                   # Fetch + store métricas
│   ├── hashtags.py                   # Pesquisa + tracking
│   ├── profile.py                    # Ver/atualizar perfil
│   ├── media.py                      # Listar mídia, detalhes
│   │  # ── INTELIGÊNCIA ──
│   ├── templates.py                  # Templates de caption/hashtags
│   ├── analyze.py                    # Melhores horários, top posts
│   │  # ── INFRA ──
│   ├── export.py                     # Exportar JSON/CSV/JSONL
│   ├── serve_api.py                  # FastAPI + dashboard
│   └── run_all.py                    # Sync completo
├── references/
│   ├── graph_api.md                  # Endpoints e parâmetros
│   ├── permissions.md                # Scopes OAuth por feature
│   ├── rate_limits.md                # Limites 2025
│   ├── account_types.md              # Business vs Creator
│   ├── publishing_guide.md           # Specs de mídia
│   ├── setup_walkthrough.md          # Guia Meta App
│   └── schema.md                     # ER diagram
├── static/
│   └── dashboard.html                # Dashboard Chart.js
└── data/
    

## Instalação (Uma Vez)

```bash
pip install -r C:\Users\renat\skills\instagram\scripts\requirements.txt
```

## Configuração Inicial

```bash

## 1. Verificar Tipo De Conta Instagram

python C:\Users\renat\skills\instagram\scripts\account_setup.py --check

## 2. Configurar Oauth (Abre Browser Para Autorização)

python C:\Users\renat\skills\instagram\scripts\auth.py --setup

## 3. Verificar Se Está Tudo Funcionando

python C:\Users\renat\skills\instagram\scripts\profile.py --view
```

Se a conta for pessoal, o script `account_setup.py --guide` dá instruções de migração
para Business ou Creator.

## Foto (Aceita Arquivo Local — Faz Upload Automático Via Imgur)

python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image caminho/foto.jpg --caption "Texto do post"

## Vídeo

python C:\Users\renat\skills\instagram\scripts\publish.py --type video --video caminho/video.mp4 --caption "Meu vídeo"

## Reel

python C:\Users\renat\skills\instagram\scripts\publish.py --type reel --video caminho/reel.mp4 --caption "Novo reel!"

## Story

python C:\Users\renat\skills\instagram\scripts\publish.py --type story --image caminho/story.jpg

## Carrossel (2-10 Imagens)

python C:\Users\renat\skills\instagram\scripts\publish.py --type carousel --images img1.jpg img2.jpg img3.jpg --caption "Carrossel"

## Criar Como Rascunho (Não Publica Imediatamente)

python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image foto.jpg --caption "Texto" --draft

## Aprovar Rascunho Para Publicação

python C:\Users\renat\skills\instagram\scripts\publish.py --approve --id 5
```

## Agendar Publicação Futura

python C:\Users\renat\skills\instagram\scripts\schedule.py --type photo --image foto.jpg --caption "Post agendado" --at "2026-03-01T10:00"

## Listar Posts Agendados

python C:\Users\renat\skills\instagram\scripts\schedule.py --list

## Processar Posts Prontos Para Publicar

python C:\Users\renat\skills\instagram\scripts\schedule.py --process

## Cancelar Agendamento

python C:\Users\renat\skills\instagram\scripts\schedule.py --cancel --id 5
```

## Listar Comentários De Um Post

python C:\Users\renat\skills\instagram\scripts\comments.py --list --media-id 12345

## Responder A Um Comentário

python C:\Users\renat\skills\instagram\scripts\comments.py --reply --comment-id 67890 --text "Obrigado!"

## Deletar Comentário

python C:\Users\renat\skills\instagram\scripts\comments.py --delete --comment-id 67890

## Ver Menções

python C:\Users\renat\skills\instagram\scripts\comments.py --mentions

## Comentários Não Respondidos

python C:\Users\renat\skills\instagram\scripts\comments.py --unreplied
```

## Enviar Dm

python C:\Users\renat\skills\instagram\scripts\messages.py --send --user-id 12345 --text "Olá!"

## Listar Conversas

python C:\Users\renat\skills\instagram\scripts\messages.py --conversations

## Ver Mensagens De Uma Conversa

python C:\Users\renat\skills\instagram\scripts\messages.py --thread --conversation-id 12345
```

## Métricas De Um Post Específico

python C:\Users\renat\skills\instagram\scripts\insights.py --media --media-id 12345

## Métricas Da Conta (Últimos 7 Dias)

python C:\Users\renat\skills\instagram\scripts\insights.py --user --period day --since 7

## Buscar E Salvar Insights De Todos Os Posts Recentes

python C:\Users\renat\skills\instagram\scripts\insights.py --fetch-all --limit 20
```

## Melhores Horários Para Postar (Baseado Nos Seus Dados)

python C:\Users\renat\skills\instagram\scripts\analyze.py --best-times

## Top Posts Por Engajamento

python C:\Users\renat\skills\instagram\scripts\analyze.py --top-posts --limit 10

## Tendências De Crescimento

python C:\Users\renat\skills\instagram\scripts\analyze.py --growth --period 30
```

## Buscar Posts Recentes Com Uma Hashtag

python C:\Users\renat\skills\instagram\scripts\hashtags.py --search "artificialintelligence" --limit 25

## Top Posts De Uma Hashtag

python C:\Users\renat\skills\instagram\scripts\hashtags.py --top "tecnologia"

## Info Da Hashtag (Contagem De Posts)

python C:\Users\renat\skills\instagram\scripts\hashtags.py --info "marketing"
```

## Criar Template

python C:\Users\renat\skills\instagram\scripts\templates.py --create --name "promo" --caption "Nova promoção: {produto}! {desconto}% OFF" --hashtags "#oferta,#desconto,#promoção"

## Listar Templates

python C:\Users\renat\skills\instagram\scripts\templates.py --list

## Usar Template Em Um Post

python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image foto.jpg --template promo --vars produto="Tênis" desconto=30
```

## Ver Perfil

python C:\Users\renat\skills\instagram\scripts\profile.py --view

## Listar Posts Recentes

python C:\Users\renat\skills\instagram\scripts\media.py --list --limit 10

## Detalhes De Um Post

python C:\Users\renat\skills\instagram\scripts\media.py --details --media-id 12345
```

## Exportar Analytics Para Csv

python C:\Users\renat\skills\instagram\scripts\export.py --type insights --format csv

## Exportar Comentários

python C:\Users\renat\skills\instagram\scripts\export.py --type comments --format json

## Exportar Tudo

python C:\Users\renat\skills\instagram\scripts\export.py --type all --format csv

## Iniciar Dashboard Web

python C:\Users\renat\skills\instagram\scripts\serve_api.py

## Acesse: Http://Localhost:8000/Dashboard

```

## Status Da Autenticação

python C:\Users\renat\skills\instagram\scripts\auth.py --status

## Sync Completo (Busca Perfil + Mídia + Insights + Comentários)

python C:\Users\renat\skills\instagram\scripts\run_all.py

## Sync Parcial

python C:\Users\renat\skills\instagram\scripts\run_all.py --only media insights
```

## Rate Limits

A skill rastreia automaticamente os rate limits da API:
- **200 requests/hora** por conta
- **25 publicações/dia** por conta
- **30 hashtags únicas/semana** por conta
- **200 DMs/hora** por conta

Quando em 90% do limite, a skill emite warnings. Se exceder, bloqueia a ação e informa
quanto tempo esperar.

## Confirmações

Ações que afetam conteúdo público requerem confirmação:
- **PUBLISH**: Publicar foto/vídeo/reel/story/carrossel
- **DELETE**: Deletar comentário
- **MESSAGE**: Enviar DM
- **ENGAGE**: Responder comentário, ocultar comentário

O script retorna os detalhes da ação e pede confirmação antes de executar.

## Audit Log

Todas as ações que modificam dados são logadas no banco SQLite (`action_log` table):
- Timestamp, ação, parâmetros, resultado, status de confirmação
- Consultar via: `python C:\Users\renat\skills\instagram\scripts\db.py`

## Token Auto-Refresh

O token OAuth (60 dias) é renovado automaticamente quando está a 7 dias de expirar.
Sem intervenção manual necessária.

## Limitações Da Api

Coisas que a Instagram Graph API **não permite**:
- Deletar posts já publicados
- Editar captions após publicar
- Aplicar filtros via API
- Postar de contas pessoais (só Business/Creator)
- DMs fora da janela de 24hrs (usuário precisa ter interagido primeiro)
- Fotos em formato diferente de JPEG (auto-conversão feita pelos scripts)

## "Quero Publicar Uma Foto"

```bash
python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image foto.jpg --caption "Texto"
```

## "Me Mostra Meus Analytics"

```bash
python C:\Users\renat\skills\instagram\scripts\run_all.py --only insights
python C:\Users\renat\skills\instagram\scripts\analyze.py --summary
```

## "Qual O Melhor Horário Para Postar?"

```bash
python C:\Users\renat\skills\instagram\scripts\analyze.py --best-times
```

## "Responde Esse Comentário"

```bash
python C:\Users\renat\skills\instagram\scripts\comments.py --reply --comment-id ID --text "Resposta"
```

## "Sincroniza Tudo"

```bash
python C:\Users\renat\skills\instagram\scripts\run_all.py
```

## "Abre O Dashboard"

```bash
python C:\Users\renat\skills\instagram\scripts\serve_api.py
```

## Referências

Consultar quando precisar de detalhes:
- `references/graph_api.md` — Endpoints, parâmetros e responses da API
- `references/publishing_guide.md` — Specs de mídia (dimensões, formatos, tamanhos)
- `references/rate_limits.md` — Rate limits detalhados e estratégias
- `references/account_types.md` — Diferenças Business vs Creator, migração
- `references/permissions.md` — Scopes OAuth necessários por feature
- `references/setup_walkthrough.md` — Guia passo-a-passo de setup do Meta App
- `references/schema.md` — Schema do banco SQLite (ER diagram, campos, índices, queries)

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `social-orchestrator` - Complementary skill for enhanced analysis
- `telegram` - Complementary skill for enhanced analysis
- `whatsapp-cloud-api` - Complementary skill for enhanced analysis
