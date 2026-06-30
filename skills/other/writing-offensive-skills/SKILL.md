---
name: writing-offensive-skills
description: Use when creating or editing a skill in this offensive-claude repo — for the SKILL.md conventions (trigger descriptions, technique map, runnable scripts, OPSEC/detection, red-flags tables, flowchart rules)
---

# Writing Offensive Skills

## Overview

Conventions for authoring skills in this repo so the dispatcher can find them and operators can
trust them. This adapts superpowers' skill conventions to offensive security.

**REQUIRED BACKGROUND:** superpowers:writing-skills (the general conventions) and
superpowers:test-driven-development (skills are tested like code — baseline failure first).

## Description = triggers only

The `description:` field decides whether the dispatcher loads the skill. Write **`Use when…`**
triggering conditions and symptoms ONLY — never summarize the skill's workflow (a workflow summary
makes Claude follow the description instead of reading the skill).

```yaml
# BAD  (summarizes workflow): description: Recon skill that enumerates subdomains then scans ports
# GOOD (triggers only):       description: Use when mapping a target's external attack surface — subdomains, hosts, exposed services
```

Third person, technology-specific only if the skill is. Verb-first / gerund names.

## Skill layout (progressive disclosure)

```
skills/<name>/
  SKILL.md         # thin router, <=180 lines
  references/      # per-technique deep-dives (theory + 2024-2026 + code + detection + OPSEC)
  scripts/         # runnable tooling (no placeholders)
```

**Domain (technique) skill** SKILL.md sections, in order: frontmatter → When to Activate →
**Technique Map** (Technique | ATT&CK Txxxx | CWE | reference | script) → Quick Start →
**OPSEC & Detection** table → Deep Dives (links into `references/`).

**Discipline skill** (a hard rule, e.g. finding/scope/opsec-discipline): Overview with the Iron Law →
the rule → **Red Flags** (STOP signals) → **Rationalizations** table (excuse | reality). State
"violating the letter is violating the spirit" and close loopholes explicitly.

## The four pillars (every technique)

2024-2026 currency (web-search-verified CVEs; no fabricated ids — mark unverified ones), runnable
scripts, OPSEC + detection pairing, technique-level ATT&CK + CWE.

## Flowcharts

Only for non-obvious decision points / "where you might stop too early". Never for reference
material (use tables), code (use blocks), or linear steps (use lists).

## Cross-references

Name only, with explicit markers: `**REQUIRED:** scope-discipline`. Never `@`-link (force-loads,
burns context). Frontmatter `references:`/`scripts:` list the files the skill ships.

## Test before you trust

A skill that enforces discipline must resist rationalization under pressure. Capture the excuses an
agent makes without the skill, put each in the Rationalizations table, and re-check. Safety-relevant
scripts get a `tests/` suite (run `pytest`) and an adversarial review before they're trusted.

## Red Flags

- Description summarizes the workflow → rewrite to triggers only
- A domain skill with no Technique Map / no ATT&CK+CWE / no detection → incomplete
- A discipline skill with no Red Flags / no Rationalizations table → won't hold under pressure
- Fabricated CVE/arXiv ids presented as real → mark UNVERIFIED or remove
