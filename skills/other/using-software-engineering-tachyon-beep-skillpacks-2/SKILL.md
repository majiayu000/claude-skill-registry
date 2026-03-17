---
name: using-software-engineering
description: Use when facing complex engineering challenges that require systematic methodology - horrible bugs, safe refactoring, code review, production incidents, technical debt decisions, or building confidence in unfamiliar codebases
---

# Software Engineering Foundations

Universal methodology for professional software engineering practice. Language-agnostic foundations that apply regardless of tech stack.

## Core Principle

**Engineering excellence is methodology, not heroics.** Systematic approaches beat clever improvisation. These skills encode battle-tested processes for situations where "just figure it out" leads to wasted time and missed root causes.

## When to Use

Load this skill when:
- Facing a bug that resists simple fixes
- Need to refactor safely without breaking things
- Reviewing code (yours or others')
- Production is on fire
- Deciding what technical debt to address
- Taking ownership of code you don't fully understand

**Don't use for**: Language-specific issues (use language packs), algorithm design (use CS fundamentals), infrastructure/deployment (use DevOps packs).

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are in the SAME DIRECTORY as this SKILL.md.

When this skill is loaded from:
  `skills/using-software-engineering/SKILL.md`

Reference sheets like `complex-debugging.md` are at:
  `skills/using-software-engineering/complex-debugging.md`

NOT at:
  `skills/complex-debugging.md` (WRONG PATH)

---

## Routing by Situation

### Horrible Bugs

**Symptoms**:
- Bug resists simple fixes
- "I've tried everything"
- Intermittent failures
- Works on my machine
- Can't reproduce reliably
- Multi-system interactions
- Heisenbugs (changes when observed)
- Race conditions suspected

**Route to**: [complex-debugging.md](complex-debugging.md)

**Why**: Systematic debugging methodology using scientific method. Adapted for Claude's strengths (fast codebase reading, pattern recognition) and limitations (no interactive debuggers).

**Integration**: For domain-specific bugs, use this methodology THEN hand off to specialists:
- PyTorch issues → `yzmir-pytorch-engineering` (debug-oom, debug-nan)
- RL training → `yzmir-deep-rl` (rl-debugging)
- Simulation chaos → `bravos-simulation-tactics` (debugging-simulation-chaos)
- ML production → `yzmir-ml-production` (production-debugging-techniques)

---

### Safe Code Transformation

**Symptoms**:
- "This code needs cleanup"
- Large refactoring needed
- Scared to change working code
- Technical debt paydown
- Architecture migration
- "How do I change this without breaking it?"

**Route to**: [systematic-refactoring.md](systematic-refactoring.md)

**Why**: Safe, incremental transformation methodology. Preserves behavior while improving structure.

**Pairs with**: [technical-debt-triage.md](technical-debt-triage.md) to decide WHAT to refactor, this skill for HOW.

---

### Code Review

**Symptoms**:
- Reviewing someone's PR
- Want feedback on your code
- "Is this code good?"
- Pre-merge quality check
- Teaching through review
- Review feels overwhelming

**Route to**: [code-review-methodology.md](code-review-methodology.md)

**Why**: Systematic review process - what to look for, in what order, how to give actionable feedback.

**Pairs with**: [codebase-confidence-building.md](codebase-confidence-building.md) when reviewing unfamiliar code areas.

---

### Production Fire

**Symptoms**:
- Production is down
- Users are affected NOW
- Incident in progress
- Need to triage quickly
- Postmortem needed
- "Everything is broken"

**Route to**: [incident-response.md](incident-response.md)

**Why**: Fire-fighting methodology - contain, diagnose, fix, learn. Keeps you calm under pressure.

**Note**: Use DURING incidents for process. Use [complex-debugging.md](complex-debugging.md) for the debugging portion.

---

### Technical Debt Decisions

**Symptoms**:
- "Should we fix this?"
- Prioritizing cleanup work
- Debt is slowing us down
- Sprint planning for maintenance
- "Everything needs fixing"
- Justifying refactoring to stakeholders

**Route to**: [technical-debt-triage.md](technical-debt-triage.md)

**Why**: Systematic identification, categorization, and prioritization. When to pay down vs. live with debt.

**Pairs with**:
- [systematic-refactoring.md](systematic-refactoring.md) for HOW to fix
- [codebase-confidence-building.md](codebase-confidence-building.md) to understand debt in unfamiliar areas

---

### Building Codebase Confidence

**Symptoms**:
- "I own this but don't fully understand it"
- New to a codebase
- Taking over from someone
- ~70% confidence, need more
- "Where do I even start?"
- Undocumented system

**Route to**: [codebase-confidence-building.md](codebase-confidence-building.md)

**Why**: Systematic exploration to internalize a system you'll maintain. Different from archaeology (analysis) - this is about building working mental models.

**Pairs with**:
- [technical-debt-triage.md](technical-debt-triage.md) - confidence reveals debt
- [code-review-methodology.md](code-review-methodology.md) - review helps you learn

**Related but different**: `axiom-system-archaeologist` is for architecture ANALYSIS. This skill is for INTERNALIZATION of systems you'll maintain long-term.

---

## Cross-Cutting Scenarios

### Taking Over a Codebase

1. [codebase-confidence-building.md](codebase-confidence-building.md) - Build mental model
2. [technical-debt-triage.md](technical-debt-triage.md) - Identify what needs fixing
3. [systematic-refactoring.md](systematic-refactoring.md) - Execute improvements

### Inherited Bug in Unfamiliar Code

1. [codebase-confidence-building.md](codebase-confidence-building.md) - Understand relevant subsystem
2. [complex-debugging.md](complex-debugging.md) - Apply debugging methodology

### Major Refactoring Project

1. [technical-debt-triage.md](technical-debt-triage.md) - Prioritize what to fix
2. [systematic-refactoring.md](systematic-refactoring.md) - Safe transformation process
3. [code-review-methodology.md](code-review-methodology.md) - Validate changes

### Production Incident with Unknown Root Cause

1. [incident-response.md](incident-response.md) - Contain and triage
2. [complex-debugging.md](complex-debugging.md) - Find root cause
3. [incident-response.md](incident-response.md) - Postmortem

---

## Ambiguous Queries - Ask First

When situation unclear, ASK ONE clarifying question:

**"Help me with this code"**
→ Ask: "What's the goal? Debug a bug? Review quality? Refactor safely? Understand it?"

**"This is a mess"**
→ Ask: "Do you need to debug something broken, or clean up working-but-ugly code?"

**"Fix this"**
→ Ask: "Is it broken (debugging) or just ugly (refactoring)?"

**Never guess. Ask once, route accurately.**

---

## Common Routing Mistakes

| Symptom | Wrong | Correct | Why |
|---------|-------|---------|-----|
| "Code needs cleanup" | complex-debugging | systematic-refactoring | Not broken, needs transformation |
| "Bug in code I don't know" | complex-debugging only | confidence-building THEN debugging | Understand before debugging |
| "Production down" | complex-debugging | incident-response THEN debugging | Contain first |
| "Should we fix this debt?" | systematic-refactoring | technical-debt-triage | Decide WHAT before HOW |
| "Review this PR" | complex-debugging | code-review-methodology | Review ≠ debugging |

---

## Reference Sheet Catalog

| Sheet | Purpose |
|-------|---------|
| [complex-debugging.md](complex-debugging.md) | Scientific method for horrible bugs |
| [systematic-refactoring.md](systematic-refactoring.md) | Safe incremental code transformation |
| [code-review-methodology.md](code-review-methodology.md) | How to review systematically |
| [incident-response.md](incident-response.md) | Production fire methodology |
| [technical-debt-triage.md](technical-debt-triage.md) | Identify, prioritize, decide |
| [codebase-confidence-building.md](codebase-confidence-building.md) | Internalize systems you maintain |

---

## Cross-Plugin Integration

This plugin provides **methodology**. Other plugins provide **domain expertise**. Use together:

| This Plugin | Pairs With | For |
|-------------|------------|-----|
| complex-debugging | `yzmir-pytorch-engineering` | ML debugging (OOM, NaN) |
| complex-debugging | `yzmir-deep-rl:rl-debugging` | RL training issues |
| complex-debugging | `ordis-quality-engineering` | Flaky tests, observability |
| complex-debugging | `yzmir-systems-thinking` | Systemic/feedback loop bugs |
| incident-response | `ordis-quality-engineering` | Chaos engineering, load testing |
| technical-debt-triage | `axiom-system-architect` | Architecture-level debt |
| technical-debt-triage | `ordis-quality-engineering` | Quality metrics, static analysis |
| codebase-confidence-building | `axiom-system-archaeologist` | Formal architecture analysis |

**Pattern**: Use this plugin's methodology to structure your approach, then hand off to domain specialists for specific technical guidance.

---

## Claude-Specific Adaptations

All reference sheets are adapted for Claude's unique position:

**Claude's Strengths** (lean into these):
- Fast codebase reading - can scan entire codebases quickly
- Pattern recognition - spot similar bugs across files
- Exhaustive search - check every occurrence of a pattern
- No fatigue - systematic processes don't tire Claude out
- Memory within session - track hypotheses and experiments

**Claude's Limitations** (work around these):
- No interactive debuggers (gdb, pdb step-through)
- Can't observe runtime state directly
- Must ask user for information Claude can't get (logs, user actions, production state)

**When to ask the user**: Sooner rather than later, but ONLY if you can't get the information yourself. Check logs, code, git history, tests first.
