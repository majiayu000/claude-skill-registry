---
name: web-research
description: Search the web, fetch documentation, navigate sites, analyze competitors
---
# Skill: Web Research

## Quando Usar
Quando o usuario pedir para pesquisar, buscar informacoes, ler paginas web, ou navegar sites.

## Ferramentas
- **WebSearch**: Busca no Google/Bing
- **WebFetch**: Le conteudo de URL especifica
- **Playwright MCP**: Navega sites interativos, tira screenshots, preenche formularios

## Estrategia
1. Para perguntas factuais: WebSearch primeiro
2. Para URLs especificas: WebFetch direto
3. Para sites que precisam interacao: Playwright
4. Para documentacao de libs: Context7 MCP (`resolve-library-id` + `query-docs`)

## Regras
- Cite fontes quando apresentar informacoes
- Prefira fontes oficiais e recentes
- Para comparacao de concorrentes: seja objetivo e factual
