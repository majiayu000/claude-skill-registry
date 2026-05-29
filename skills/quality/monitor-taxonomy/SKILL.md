---
name: monitor-taxonomy
description: >
  Three-tier cascade taxonomy quality monitor. Assesses whether bridge_attributes
  and collection_tags on memory documents are CORRECT (not just present).
  Uses T0 heuristic → T1.5 classifier/GPT → T2 Brandon teacher cascade.
  Accumulates training labels for autonomous quality assessment.
triggers:
  - monitor taxonomy
  - taxonomy quality
  - check taxonomy quality
  - taxonomy cascade
  - bridge attribute quality
  - run taxonomy monitor
allowed-tools: Bash
metadata:
  short-description: Three-tier cascade taxonomy quality monitor

provides:
  - monitor-taxonomy
composes: [, task-monitor]
---

# Monitor Taxonomy

Taxonomy quality monitor that assesses correctness of bridge_attributes and
collection_tags on memory documents via a three-tier cascade.

**Key distinction from monitor-memory**: monitor-memory checks coverage/method/drift.
monitor-taxonomy checks **correctness** via cascade validation.

## Continuous Operation (Non-Negotiable)

This skill is **always-on**. It:
- Runs on its configured schedule indefinitely — it NEVER stops unless explicitly halted by the user
- The agent MUST NOT stop and wait for the human to ask for status or remember to check
- If a cycle fails, diagnose the failure, attempt auto-repair, and continue
- Only escalate to the human if genuinely blocked after exhausting /dogpile research
- Gracefully handles restarts and maintains state across cycles
- Is designed for multi-day/week/month autonomous operation

**Anti-pattern**: Reporting status and waiting for the human to ask "what next?" is UNACCEPTABLE. The agent must proactively fix issues and continue the monitoring loop.

## Architecture

```
Document with bridge_attributes
         │
    ┌────▼────┐
    │  Tier 0  │  Heuristic: vocabulary validation, null check,
    │ (instant) │  text-bridge coherence (keyword overlap score)
    └────┬────┘
         │ confidence < 0.80
    ┌────▼─────┐
    │ Tier 1.5  │  Trained classifier (after 50+ labels)
    │ (~200ms)  │  OR small GPT (after /create-gpt training)
    └────┬─────┘
         │ confidence < 0.85 ("maybe" zone)
    ┌────▼────┐
    │  Tier 2  │  Brandon (scillm persona) — authoritative teacher
    │ (~3s)    │  Full semantic assessment → training_labels.jsonl
    └────┬────┘
         │
    Grade: CORRECT / MISTAGGED / MISSING / HALLUCINATED
    Action: keep / re-extract / remove / flag
```

## Commands

```bash
# Run all probes
./run.sh check --json

# Run a specific tier
./run.sh check --tier 0 --autofix --json

# Run a single probe
./run.sh check --probe null-bridge-gc --json

# Dashboard
./run.sh dashboard

# Status (labels, shadow, classifier)
./run.sh status

# Register nightly schedule
./run.sh register-nightly

# Help
./run.sh help
```

## Probes

### Tier 0 — Heuristic Quality (instant, deterministic)

| ID  | Probe                   | Auto-Fix |
|-----|-------------------------|----------|
| P01 | null-bridge-gc          | Yes      |
| P02 | vocabulary-violation    | Yes      |
| P03 | text-bridge-coherence   | No       |
| P04 | collection-tag-violation| Yes      |
| P05 | stale-taxonomy          | No       |

### Tier 1.5 — Classifier/GPT Quality (after training)

| ID  | Probe                     | Auto-Fix |
|-----|---------------------------|----------|
| P10 | classifier-quality-check  | No       |
| P11 | shadow-agreement          | No       |
| P12 | confidence-distribution   | No       |

### Tier 2 — Brandon Teacher + Training

| ID  | Probe              | Auto-Fix |
|-----|--------------------|----------|
| P20 | teacher-validate   | No       |
| P21 | label-accumulation | No       |
| P22 | shadow-tracking    | No       |
| P23 | retrain-trigger    | Yes      |

## Nightly Schedule

```
03:00  monitor-taxonomy T0: Heuristic quality (P01-P05) + auto-fix
03:15  monitor-taxonomy T1.5: Classifier quality (P10-P12) — skips if no model
03:30  monitor-taxonomy T2: Brandon teacher (P20-P23) — validates flagged docs
```

Runs BEFORE monitor-memory at 05:00. Taxonomy fixes applied before coverage measured.

## Environment Variables

| Variable                       | Default                        | Description              |
|-------------------------------|--------------------------------|--------------------------|
| `ARANGO_URL`                   | `http://127.0.0.1:8529`      | ArangoDB endpoint        |
| `ARANGO_DB`                    | `memory`                       | Database name            |
| `MONITOR_TAXONOMY_STATE_DIR`   | `~/.pi/monitor-taxonomy`      | State directory          |
| `TAXONOMY_RETRAIN_THRESHOLD`   | `50`                           | Labels to trigger retrain|
| `TAXONOMY_SAMPLE_SIZE`         | `100`                          | Nightly sample size      |
| `TAXONOMY_COHERENCE_THRESHOLD` | `0.20`                         | Min keyword overlap      |
| `TAXONOMY_STALE_DAYS`          | `90`                           | Days before stale        |
