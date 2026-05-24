---
description:
  Conduct market, domain, or technical research with verified sources. Phase 1
  Analysis
user-invocable: true
disable-model-invocation: true
---

# Research Workflow

**Goal:** Conduct comprehensive research across multiple domains using current
web data and verified sources.

**Agent:** Analyst (Mary) **Phase:** 1 - Analysis

---

## Workflow Architecture

This uses **routing-based discovery** with micro-file architecture. Each
research type has its own step folder.

## Initialization

Check for project config at `bmad/config.yaml`. Load project settings.

**Requires:** Web search capability.

## Research Tracks

- **Market Research:** `./market-steps/step-01-init.md`
- **Domain Research:** `./domain-steps/step-01-init.md`
- **Technical Research:** `./technical-steps/step-01-init.md`

Begin by asking the user what they want to research, then route to the
appropriate track.

## Output

Research document with citations at:
`planning-artifacts/research/{type}-{topic}-research-{date}.md`
