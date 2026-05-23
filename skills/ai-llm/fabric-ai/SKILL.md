---
name: fabric-ai
description: Guides pattern selection through decomposition, exploration, and diverse approach generation
---

# Fabric Orchestrator
--ultrathink --seq

## Core Mission
Explore patterns creatively → Generate 5-7+ deeply reasoned approaches per challenge

**Resources:** `references/pattern_descriptions.json` (228 patterns), `references/strategies.json` (9 strategies)

## Workflow

1. **Analyze** (--ultrathink --seq): Components, goals, dimensions, creative angles
2. **Ask** (AskUserQuestion): Objective, constraints, creativity level, expansion ideas
3. **Consult**: Read JSONs
4. **Generate**: 5-7+ approaches (unique angle, patterns, strategy, WHY, commands, trade-offs)
5. **Present** → **Execute** → **Iterate**

## Pattern Discovery
- Read **Resoureces**
- Explore MULTIPLE tag categories (ANALYSIS:97, WRITING:63, DEVELOPMENT:44, EXTRACT:39, BUSINESS:34, SECURITY:30, others)
- Consider unexpected combinations
- Think across dimensions

## Content Types

| Type | Flags |
|------|-------|
| YouTube | `-y <url> --transcript` |
| Web | `-u <url>` |
| Audio/Video | `--transcribe-file <path>` |

**Always add:** `--stream` (long), `--session` (multi-step), `-c` (clipboard), `-o` (save), `--strategy`

## Pipelines
```bash
fabric <input> -p <pattern> --session <name>
fabric -p <pattern> --strategy <strat> --session <name> -c
```

## Quality Checklist
- [ ] Read both JSONs
- [ ] Explored MULTIPLE tags
- [ ] Generated 5-7+ approaches
- [ ] Deep WHY reasoning
- [ ] Varied all dimensions
- [ ] Used --session for pipelines

## Commands
```bash
fabric -y <url> -p extract_wisdom --strategy cot --stream
fabric --listpatterns / --liststrategies / --listmodels
```
