---
name: project-planner-alceupassos-cepainfo
description: Especialista em arquitetura de software, planejamento e orquestração
  para o projeto Analises.
---

# Project Planner Skill

Especialista em arquitetura de software, planejamento e orquestração para o projeto Analises.

## Metodologia

1. Decomposição em componentes
2. Definir dependências entre partes
3. Sequenciar execução (o que primeiro)
4. Identificar riscos e mitigações
5. Criar checklists verificáveis

## Arquitetura Analises

Frontend: Next.js + shadcn/ui
Backend: Supabase + API Routes
IA: Claude, Gemini, GPT via MCP
Database: PostgreSQL (Supabase) + MSSQL (SUPRA)

## MCP Servers a Configurar

1. Power BI MCP
   * ExecuteDAXQuery
   * GetModelSchema
2. Supabase MCP
   * ReadData, WriteData
   * ListTables, Subscribe
3. AI Orchestrator
   * RouteToModel(prompt, model\_id)
   * ParallelQuery(prompts\[], models\[])

## Sequência de Implementação

1. Setup Next.js + tema dark
2. Configurar Supabase (tabelas)
3. Implementar conexão MSSQL
4. Criar layout base + sidebar
5. Importador .pbix
6. Matriz DRE
7. Gráficos dinâmicos
8. Chat CEPALAB.IA
9. Orquestração MCP
10. Testes e validação
