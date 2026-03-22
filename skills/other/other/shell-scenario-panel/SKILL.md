---
name: shell-scenario-panel
description: Shell methodology scenario planning with worldview elicitation, external scenario construction, actor-relative impact analysis, and rigorous documentation. Use when exploring futures, uncertainty, preparedness, positioning, or other decisions that benefit from multi-scenario reasoning.
---

# Shell Scenario Panel

Use this skill when working inside:

- `/Users/braydon/projects/experiments/ai-simulations/shell-scenario-panel`

This skill is intentionally thin. The repo is the source of truth.

## Canonical Files

Read only what you need, in this order:

1. `CODEX.md` or `CLAUDE.md` for runtime-specific behavior
2. `prompts/moderator.md` for the actual facilitation sequence
3. `.claude/config.json` for phase definitions and specialist rosters

Do not rely on older copied workflow descriptions when these files disagree.

## Startup

For Codex sessions:

```bash
.codex/session-start.sh
```

To resume:

```bash
.codex/session-start.sh --scenario SCENARIO-YYYY-NNN
```

To create a new scenario explicitly:

```bash
.codex/session-start.sh --new
```

To open monitoring mode:

```bash
.codex/session-start.sh --monitor SCENARIO-YYYY-NNN
```

For Claude sessions, use the equivalent `.claude/session-start.sh`.

## Expected Workflow

The current live workflow is:

0. Worldview elicitation
0a. Internal baseline
0b. Context enrichment
1. Focal question
2. Predetermined elements
3. Critical uncertainties
4. Scenario development
5. Early warning signals
6a. Impact analysis
6b. Strategy / response testing
7. Worldview integration

Important distinction:

- Phases 1-5 build the external frame.
- Phase 6a translates that frame into actor-relative impact.
- Phase 6b turns impact into preparedness, positioning, or response guidance.
- Phase 7 connects the work back to the user's worldview.

## User-Facing Behavior

When the user invokes this skill, expected facilitator behavior is:

- bootstrap the session automatically
- check `resources/` and offer to ingest materials
- elicit worldview before doing external analysis
- capture internal baseline before recommendations
- stop after scenarios and run impact translation before strategy
- use checkpoints after major synthesis steps
- never ask the user to run scripts manually

From the user perspective, they should mostly:

- describe the topic or decision
- answer Dr. Wells' questions
- validate syntheses at checkpoints
- refine the focal actor or response mode when impact work begins

## Impact Layer

Treat `impact_analysis.md` as mandatory between scenarios and `strategy_analysis.md`.

The impact layer is:

- actor-relative, not scenario-relative
- cross-domain, not business-only
- suitable for household, personal finance, education, company, customer, or mixed actor systems

Default impact cast:

- Marisol Vega (`ledger_keeper`)
- Darnell Brooks (`friction_mechanic`)
- Nadia Rahman (`dependency_cartographer`)
- Dr. Imani Clarke (`burden_cartographer`)
- Ethan Rowe (`optionality_conservator`)
- Priya Desai (`precedent_archivist`)
- Luis Ortega (`signal_mason`)
- Jamie O'Sullivan (`contrarian`)

Overlay packs currently implemented:

- `household_personal`
- `commercial_positioning`

Use `.claude/lib/select-impact-specialists.sh --list-overlays` to inspect them or pass overlay ids to resolve the combined cast.

## Research and Validation

- Use `pp -r --no-interactive "query" --output json` for web research when needed.
- Do not bypass transcript checks, metadata updates, or quality gates.
- Use `.claude/lib/file-paths.sh` and related validation helpers when prompts refer to enforced file outputs.

## Exports

If exports are needed:

```bash
.claude/export-deck-brief.sh SCENARIO-YYYY-NNN
```

Preview exports locally with:

```bash
.claude/lib/serve-exports.sh SCENARIO-YYYY-NNN
```
