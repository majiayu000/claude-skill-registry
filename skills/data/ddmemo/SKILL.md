---
name: ddmemo
description: Generate comprehensive investment memos for cyber•Fund investment committee decisions. Use when creating DD memos or investment analysis documents.
---

# DD Memo Skill

Generate comprehensive investment memos for cyber•Fund investment committee decisions.

## Capabilities

Transform research and analysis into structured investment memos following cyber•Fund's template and investment philosophy.

## Workflows

- `workflows/generate.md`: DD memo generation workflow

## Agents Used

- memo-analyst: Deep strategic analysis and scoring (Opus model for strategic depth)
- memo-writer: Template-driven memo writing (Sonnet for structure)

## Prerequisites

- Company research must exist in `~/CybosVault/private/deals/<company>/research/`
- Deal context in `~/CybosVault/private/deals/<company>/.cybos/context.md`

## Context Files

- `context/investment-philosophy.md`: Investment rubric and decision-making framework
- `context/MEMO_template.md`: Standard memo structure

## Output Location

- `~/CybosVault/private/deals/<company>/memo/memo.md` (overwrites previous version)

## Memo Components

A complete memo includes:
- Executive Summary & Investment Thesis
- Scoring Sheet (10 categories weighted)
- Product, Business Model, Technology sections
- Traction, Competition, GTM
- Team (Founders, Key Hires)
- Financials, Projections
- Investment Overview, Cap Table, Exit Analysis
- Risks & Mitigations
- IC Q&A preparation
- Clear recommendation

## Investment Philosophy

Applies cyber•Fund rubric:
- Path to $1B+ revenue (legendary outcomes)
- Defensible moat (data, network, hard tech)
- Clear business model (revenue > token speculation)
- Strong founders (energy, sales DNA, deep expertise)
- Market timing (why now?)
- Big Tech threat assessment (6-week rule)
- Reasonable valuation for stage

## Workflow Pattern

1. **GATHER**: Load all research and context
2. **ANALYZE**: Deep strategic analysis with memo-analyst (Opus)
3. **WRITE**: Template-driven memo with memo-writer (Sonnet)
4. **REVIEW**: Completeness and consistency check
5. **OUTPUT**: Save to deal memo folder
6. **LOG**: Record memo generation

## Success Criteria

- All template sections completed
- Investment rubric scores provided with rationale
- Clear recommendation (INVEST / PASS / MORE DILIGENCE)
- Risks identified with mitigations
- Exit scenarios modeled
- IC questions anticipated
