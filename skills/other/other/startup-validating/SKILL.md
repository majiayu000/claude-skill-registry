---
name: startup-validating
description: >
  Orchestrate a 6-stage startup idea validation pipeline with decision gates, confidence scoring,
  and composable domain presets. Use when user runs /startup-validate command, wants to validate
  a startup idea, mentions "startup validation", "idea validation", "market validation",
  "feasibility analysis", or "go-to-market plan".
argument-hint: "\"<idea>\" | @<file> [--preset <name>]... [--fast] [--deep] [--from <N>] [--stage <N>] [--name <slug>]"
allowed-tools: Read, Write, Glob, Grep, Agent, AskUserQuestion
---

# Startup Validation Pipeline

Orchestrate a 6-stage startup validation pipeline. Each stage is executed by a dedicated agent, produces a confidence-scored markdown report, and presents a decision gate.

## Pipeline Stages

| # | Stage | Agent | Decision Gate |
|---|-------|-------|--------------|
| 1 | Problem & Market Validation | `market-validator` | Is this a real problem worth solving? |
| 2 | Feasibility Analysis | `feasibility-analyst` | Can this be built legally and operationally? |
| 3 | Product & Solution Design | `product-designer` | Can we design a differentiated product? |
| 4 | Business Model & Strategy | `business-strategist` | Can this become profitable and defensible? |
| 5 | Go-to-Market & Growth | `growth-strategist` | Can we acquire users sustainably? |
| 6 | Execution Roadmap | `execution-planner` | Can we build and launch realistically? |

## Arguments

Parse from `$ARGUMENTS`:

| Flag | Effect |
|------|--------|
| `"<idea>"` | The startup idea to validate (required — or use `@file`) |
| `@<file>` | Provide idea description or research brief from a file |
| `--preset <name>` | Load preset from `presets/` dir (composable) |
| `--fast` | Skip decision gates, run all stages autonomously |
| `--deep` | Spawn parallel sub-agents per stage + critic synthesis |
| `--from <N>` | Resume from stage N (reads prior reports from disk) |
| `--stage <N>` | Run only stage N in isolation |
| `--name <slug>` | Override auto-generated run slug |

## Orchestration

See [WORKFLOW.md](WORKFLOW.md) for the complete orchestration protocol including:
- Slug generation and output directory setup
- Preset loading and composition
- Stage execution (standard and deep modes)
- Decision gate interaction
- Summary scorecard generation

## Output

Reports are saved to `startup-validation/{slug}/` in the current project:

```
startup-validation/{slug}/
├── idea.md
├── pipeline-state.json          ← created on PAUSE, consumed on resume
├── stage-1-market-validation.md
├── stage-2-feasibility.md
├── stage-3-product-design.md
├── stage-4-business-model.md
├── stage-5-go-to-market.md
├── stage-6-execution-roadmap.md
└── summary.md
```

## Examples

See [EXAMPLES.md](EXAMPLES.md) for usage examples.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.
