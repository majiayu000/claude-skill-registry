---
name: generating-quarterly-charters
description: Use when planning a quarter and need to convert signals (truth base, VOC, KTLO) into 3-5 strategic charters with clear problem statements and success metrics.
---

# Generating Quarterly Charters

## Overview

Converts accumulated PM signals into a coherent quarterly plan. Produces 3-5 charters that define strategic bets with clear problems, target users, success metrics, and risks.

## When to Use

- Quarterly planning cycle starting
- Need to present roadmap to leadership
- Have accumulated insights and need to prioritize
- Want structured format for eng/design alignment

## Output Formats

By default, produces full charters. Use `--format` for audience-specific outputs:

| Format | Command | Audience | Content |
|--------|---------|----------|---------|
| `full` (default) | `generating-quarterly-charters` | Planning team | Complete charter with all sections |
| `exec` | `generating-quarterly-charters --format exec` | Executives | 1-page summary: problems, metrics, risks, timeline |
| `eng` | `generating-quarterly-charters --format eng` | Engineering | Scope, dependencies, technical constraints only |

### Exec Format (`--format exec`)

Produces a 1-page executive summary:

```markdown
# Q[X] [YYYY] Quarterly Plan - Executive Summary

## Strategic Bets
| Charter | Problem | Success Metric | Confidence |
|---------|---------|----------------|------------|
| [Name] | [1-line] | [KPI + target] | High/Med/Low |

## Key Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Top 3 risks across all charters] |

## Resource Asks
[Any leadership decisions or resources needed]

## Timeline
[High-level milestones only]
```

### Eng Format (`--format eng`)

Produces engineering-focused summary:

```markdown
# Q[X] [YYYY] Engineering Context

## Charter Scope Summary
| Charter | In Scope | Out of Scope | Dependencies |
|---------|----------|--------------|--------------|
| [Name] | [Bullet list] | [Bullet list] | [Teams/systems] |

## Cross-Charter Dependencies
[Shared dependencies, sequencing constraints]

## Technical Risks
| Risk | Charter | Mitigation |
|------|---------|------------|
| [Technical risks only] |

## Open Technical Questions
[Questions that need eng input]
```

## Core Pattern

**Step 1: Gather Upstream Outputs**

Read all available:
- `outputs/truth_base/truth-base.md` - Product understanding
- `outputs/insights/voc-synthesis-*.md` - Customer signals
- `outputs/ktlo/ktlo-triage-*.md` - Operational burden
- `outputs/insights/kb-gaps-*.md` - Documentation gaps

**If key inputs are missing or stale, report and ask user to refresh first.**

**Step 2: Synthesize Signals**

Extract from each source:
- **Truth base:** Current roadmap themes, constraints, open questions
- **VOC:** Top themes, opportunities, customer pain
- **KTLO:** Critical issues, patterns, tech debt
- **KB gaps:** User struggle points, AI opportunities

**Step 3: Identify Charter Candidates**

Look for convergence:
- Pain point mentioned in VOC + KTLO ticket cluster = strong signal
- Roadmap theme + customer evidence = validated bet
- Gap in truth base + customer complaints = opportunity

Aim for 5-7 candidates, then narrow to 3-5.

**Step 4: Draft Each Charter**

For each charter:

| Section | Content | Source Required |
|---------|---------|-----------------|
| Problem | Specific user pain | VOC/KTLO evidence |
| Target Users | Who feels this pain | Explicit segment |
| Success Metrics | How we'll know it worked | Measurable KPIs |
| Scope | What's in | Clear boundaries |
| Non-Scope | What's out | Explicit exclusions |
| Dependencies | What we need from others | Named teams/systems |
| Risks | What could go wrong | Mitigations |
| Why Now | Why this quarter | Business/strategic reason |

**Step 5: Generate Output**

Write to `outputs/roadmap/Qx-YYYY-charters.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: generating-quarterly-charters
sources:
  - outputs/truth_base/truth-base.md (modified: YYYY-MM-DD)
  - outputs/insights/voc-synthesis-*.md (modified: YYYY-MM-DD)
  - outputs/ktlo/ktlo-triage-*.md (modified: YYYY-MM-DD)
downstream:
  - outputs/delivery/prds/*.md
---

# Q[X] [YYYY] Charters

## Executive Summary
[3-5 sentences: What are we betting on this quarter? Why?]

## Charter Overview

| # | Charter | Problem | Target | Confidence |
|---|---------|---------|--------|------------|
| 1 | [Name] | [1-line problem] | [Segment] | High/Med/Low |
| 2 | [Name] | [1-line problem] | [Segment] | High/Med/Low |
| ... | ... | ... | ... | ... |

---

## Charter 1: [Name]

### Problem Statement
[2-3 sentences describing the user pain. Must cite evidence.]

**Evidence:**
- VOC: [N sources mention this]
- KTLO: [N tickets related]
- Quote: "[verbatim]" — [source]

### Target Users
| Segment | Description | Why Them |
|---------|-------------|----------|
| [Segment] | [Description] | [Reason] |

### Success Metrics
| Metric | Current | Target | How Measured |
|--------|---------|--------|--------------|
| [KPI] | [X or Unknown] | [Y] | [Method] |

### Scope
**In scope:**
- [Feature/capability 1]
- [Feature/capability 2]

**Out of scope:**
- [Explicitly excluded item]

### Dependencies
| Dependency | Team/System | Status |
|------------|-------------|--------|
| [What we need] | [Who owns it] | [Known/Unknown] |

### Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | High/Med/Low | [Action] |

### Why Now
[1-2 sentences: business context, competitive pressure, customer urgency]

---

## Charter 2: [Name]
[Same structure]

---

## What We're NOT Doing This Quarter
| Item | Reason |
|------|--------|
| [Deprioritized item] | [Why not now] |

## Open Questions for Leadership
1. [Decision needed]
2. [Resource question]

## Sources Used
- [file paths with dates]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Problem affects X users] | Evidence | [VOC/KTLO file] |
| [Metric baseline is Y] | Evidence/Unknown | [data source or "Need data"] |
```

**Step 6: Copy to History & Update Tracker**

- Copy to `history/generating-quarterly-charters/Qx-YYYY-charters-YYYY-MM-DD.md`
- Update `alerts/stale-outputs.md`

## Quick Reference

| Input | What It Provides |
|-------|------------------|
| Truth base | Context, constraints, themes |
| VOC | Customer pain, opportunities |
| KTLO | Operational reality, patterns |
| KB gaps | User struggles, AI opps |

## Common Mistakes

- **No evidence:** "Users want X" → Must cite VOC/KTLO source
- **Vague metrics:** "Improve satisfaction" → Specific: "NPS +10 points"
- **Too many charters:** 8 charters = no focus → Max 5
- **Missing scope:** "Build feature X" → What's in AND out
- **Ignoring risks:** "This will be easy" → Every charter has risks
- **Stale inputs:** Using 3-month-old VOC → Check source dates

## Verification Checklist

- [ ] All upstream outputs read (truth base, VOC, KTLO, KB)
- [ ] Source dates checked (not stale)
- [ ] 3-5 charters (not more)
- [ ] Every problem has VOC/KTLO evidence
- [ ] Success metrics are measurable
- [ ] Scope and non-scope explicit
- [ ] Dependencies named
- [ ] Risks documented with mitigations
- [ ] "What we're NOT doing" section included
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Problem exists] | Evidence | [VOC/KTLO citations] |
| [Target segment] | Evidence | [explicit in sources] |
| [Metric baseline] | Evidence/Unknown | [data or "Need to measure"] |
