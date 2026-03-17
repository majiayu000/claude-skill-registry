---
name: growth-kr-reporting
description: Use when preparing Growth KR reports that require orchestrating mapped analytics scripts, parallel subagent analysis, strict source traceability, and a final report that answers mandatory KR questions.
---

# Growth KR Reporting

## Overview
This skill is an orchestration workflow for Growth KR analysis. It selects scripts from a metrics registry, delegates analysis to subagents, consolidates markdown outputs, and enforces evidence-first reporting.

Primary metrics map path:
- `/Users/ivanfarias/clawd/scripts/metrics_map.json`

## When to Use
- Weekly or monthly Growth KR updates requiring multiple data sources
- KR reporting that needs channel/country/funnel decomposition
- Any report that must be reproducible, sourced, and auditable
- Cases where one analyst flow is too broad and needs parallel decomposition

Do not use when:
- The request is qualitative brainstorming without quantitative claims
- The metrics map is unavailable and no substitute mapping is provided

## Non-Negotiable Rules
1. Never calculate with natural-language reasoning.
   All derived metrics must come from script outputs.
2. Never publish numbers without provenance.
   Every numeric claim must map to an artifact and source location.
3. Never assume missing data.
   Either spawn a fetch subagent or ask the user objective missing-data questions.
4. Never set `On track` or `Off track` without explicit target and cycle window.
5. Never claim causality from descriptive data alone.
   Label unsupported causal statements as hypotheses.
6. Final output is mandatory: always produce one consolidated markdown report.

## Absolute Enforcement (Non-Overridable)
1. If numeric output is requested, script execution is mandatory.
2. If asked to skip scripts or "do quick math", refuse numeric output and provide only commands + missing inputs.
3. This enforcement overrides speed/format preferences.

## Hard Stop Conditions
If any condition below is true, block final analysis and ask for remediation:
- Metrics map file unreadable: `/Users/ivanfarias/clawd/scripts/metrics_map.json`
- No mapped scripts for one or more requested KRs
- Selector returned KR in `fallback_krs` (query fallback without exact KR mapping)
- Missing target/cycle window for any KR status call
- No executable command path for selected script

## Required Inputs (Ask If Missing)
- KR ids and formal metric definitions
- Reporting window (`start_date`, `end_date`)
- KR targets + cycle dates (`cycle_start`, `cycle_end`)
- Comparison baseline (previous week/month)
- Decision context (what decisions this report must support)

## Mandatory KR Scope (Vender o Metodo)
Always cover these KRs when requested for this report family:
- `KR T2.1 | MRR de Iniciadas`
- `KR O2.1.1 | Signups App AD5`
- `KR O2.1.2 | MRR Novos Web`
- `KR O2.1.2.1 | Signups Web ICP/AD5`
- `KR O2.1.2.2 | ARPA Web`

## Question and Metric Contract (Must Be Answered)

### KR T2.1 | MRR de Iniciadas
Associated metrics:
- `MRR de Assinaturas Iniciadas`
- `MRR App`, `MRR Web`
- channel decomposition when available

Questions:
- What is the current value and trajectory vs cycle expectation?
- Is current pace enough to hit target by deadline?
- Which components (App/Web/channel) explain movement?

### KR O2.1.1 | Signups App AD5 (Paid Media AD5)
Associated metrics (mandatory):
- `signups`
- `installs`
- `cost`
- `clicks`
- `impressions`
- campaign/ad-group/country cuts when available

Questions:
- What is current signup level and weekly trajectory vs target pace?
- Which campaign/ad group/country segments are materially driving movement?
- How are `cost` and `installs` evolving relative to signup movement?
- Are leading funnel signals aligned with expected signup outcome?

### KR O2.1.2 | MRR Novos Web
Associated metrics:
- `MRR total`
- `MRR de Assinaturas Iniciadas`
- `MRR de Novas Assinaturas`
- `Net MRR Variation`
- platform and channel decomposition

Questions:
- Is MRR Novos Web improving, stagnating, or regressing?
- Which components materially explain the trajectory?
- Is current variance noise or structural shift?

### KR O2.1.2.1 | Signups Web ICP/AD5
Associated metrics:
- `Assinaturas/Signups Iniciadas Web`
- `Reativacoes`
- `Novas Assinaturas`
- channel and country decomposition

Questions:
- What changed since last update and what drives current level?
- Which channels/segments contribute most to variance?
- Are leading indicators aligned with end-of-cycle expectation?

### KR O2.1.2.2 | ARPA Web
Associated metrics:
- `ARPA`
- `ARPA Novas Web`, `ARPA Novas App`
- `ARPA Reativacoes`, `ARPA Assinaturas Existentes`
- channel and country decomposition

Questions:
- Is ARPA Web improving, stagnating, or regressing?
- Which mix components explain ARPA movement?
- Is performance within expected variance or structural shift?

## Orchestrator Workflow

### Phase 1: Intake and Run Setup
1. Capture requested KRs and reporting window.
2. Create `run_id` (`YYYYMMDD-HHMMSS`) for artifacts.
3. Prepare output root:
   - `docs/analytics/runs/<run_id>/`

### Phase 2: Script Discovery From Metrics Map
Run selector script:

```bash
python3 .codex/skills/growth-kr-reporting/scripts/select_metric_scripts.py \
  --metrics-map /Users/ivanfarias/clawd/scripts/metrics_map.json \
  --kr T2.1 \
  --kr O2.1.1 \
  --kr O2.1.2 \
  --kr O2.1.2.1 \
  --kr O2.1.2.2 \
  --out docs/analytics/runs/<run_id>/script_plan.json
```

Selection policy:
- Priority 1: exact KR usage match in map
- Priority 2: associated-metric coverage bundle for the KR
- Priority 3: decomposition scripts (`by channel`, `by country`, `campaign`, `ad group`) for `Detalhes`

If `script_plan.json` returns `missing_krs`, `fallback_krs`, or `coverage_gaps`:
- spawn fetch/map-gap subagent for fetchable gaps
- ask user for missing external inputs when not fetchable

### Phase 3: Parallel Subagent Fan-Out
Spawn independent subagents per analysis block:
- `KR-level core trajectory`
- `Channel decomposition`
- `Country/geography decomposition` (if relevant)
- `Campaign/ad group decomposition` (if relevant)
- `Leading indicators / funnel progression`

Each subagent must:
1. Execute mapped scripts (or report exact execution blocker).
2. Produce one markdown report at:
   - `docs/analytics/runs/<run_id>/subagents/<slug>.md`
3. Include sections:
   - `Scope`
   - `Scripts Executed`
   - `Computed Claims`
   - `Insights`
   - `Open Gaps`
   - `Sources`

### Phase 4: Missing-Data Loop
If any subagent reports `Open Gaps`:
1. Classify each gap:
   - `fetchable` (can be solved with another mapped script)
   - `external_input` (needs user answer)
2. For `fetchable`, spawn additional fetch subagent and rerun affected analysis subagent.
3. For `external_input`, ask user concise, blocking questions.

### Phase 5: Consolidation (Mandatory Final Report)
After all required subagent reports are complete:
1. Merge findings into final markdown:
   - `docs/analytics/runs/<run_id>/final-analysis.md`
2. For each KR output exactly:
   - `Update`
   - `Status`
   - `Atualizacoes`
     - `Resumo`
     - `Pontos Criticos / Decisoes`
     - `Detalhes`
3. Explicitly answer the KR question contract in the relevant sections.
4. Add final `Sources` section linking each claim to subagent artifact + raw output.

## Subagent Contract
Use this instruction template for each subagent:

```text
You are an analytics subagent in orchestrated mode.
Follow growth-kr-reporting rules strictly.
- Use mapped scripts only.
- No mental calculations.
- Cite sources for every numeric claim.
- If data is missing, report in Open Gaps with exact missing field.
Write output to: docs/analytics/runs/<run_id>/subagents/<slug>.md
```

## Refusal Template
Use when blocked:

```text
Nao posso concluir esta analise sem executar scripts mapeados e validar fontes.
Para continuar, preciso executar:
<command>
Ou confirmar os parametros faltantes:
<missing_inputs>
```

## Compliance Checklist (Before Final Response)
- [ ] `metrics_map.json` loaded successfully
- [ ] `script_plan.json` generated
- [ ] No unresolved `missing_krs`
- [ ] No unresolved `fallback_krs`
- [ ] `coverage_gaps` resolved or escalated to user
- [ ] Subagent markdown files generated
- [ ] Numeric claims sourced to artifacts
- [ ] Status logic tied to target + cycle window
- [ ] Final markdown generated at `docs/analytics/runs/<run_id>/final-analysis.md`
- [ ] KR question contract answered for all required KRs

## Quick Reference
| Item | Rule |
|---|---|
| Script mapping | Must come from `metrics_map.json` |
| Associated metrics | Must satisfy KR bundle before consolidation |
| Delegation | Parallel by analysis block |
| Gaps | Fetch via subagent or ask user |
| Consolidation | Single final markdown report |
| Output root | `docs/analytics/runs/<run_id>/` |

## Common Mistakes
- Selecting scripts by memory instead of reading `metrics_map.json`
- Missing associated metrics for KR (`O2.1.1` without `signups/installs/cost`)
- Running scripts but skipping subagent markdown artifacts
- Consolidating before resolving open gaps
- Calling status without target/cycle context
- Providing recommendations not backed by measured drivers
