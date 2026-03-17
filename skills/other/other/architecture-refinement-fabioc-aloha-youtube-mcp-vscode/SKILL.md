---
name: "Architecture Refinement Skill"
description: "Meta-skill for maintaining and evolving Alex's cognitive architecture through deliberate documentation and pattern extraction."
---

# Architecture Refinement Skill

> Meta-skill for maintaining and evolving Alex's cognitive architecture through deliberate documentation and pattern extraction.

## Purpose

This skill enables Alex to:

- Recognize when a learning session produces architecture-worthy insights
- Document patterns in the appropriate .github/ location (skills, instructions, prompts)
- Update migration trackers and status tables
- Consolidate knowledge files following KISS/DRY principles

## When to Apply

Trigger this skill when:

- A session resolves a recurring problem (document the pattern)
- A skill file is migrated or consolidated (update trackers)
- A new workflow emerges (capture in appropriate .instructions.md)
- User feedback reveals a principle ("don't over-simplify")

## Core Patterns

### Pattern Recognition Checklist

Before session ends, ask:

| Question | If Yes → Action |
| -------- | --------------- |
| Did we solve a problem that could recur? | Document in relevant skill file |
| Did we learn something about Alex's architecture? | Update relevant .github/ documentation |
| Did a file get created/deleted/consolidated? | Update migration trackers |
| Did user correct AI behavior? | Add to skill's Anti-Patterns + document principle |
| Did the skill itself get improved during use? | Commit the refinement immediately |

### Documentation Location Guide

| What You Learned | Where to Document | Audience |
| ---------------- | ----------------- | -------- |
| Technical skill pattern | `.github/skills/{name}/SKILL.md` | Alex (AI) |
| Important concepts for user | `.github/skills/{name}/SKILL.md` | Human + AI |
| Process improvement | `.github/instructions/*.instructions.md` | Alex (AI) |
| Complex workflow | `.github/prompts/*.prompt.md` | Alex (AI) |
| Domain expertise | `.github/skills/{name}/SKILL.md` | Alex (AI) |

**Key Distinction**:

- `.github/skills/` = Operational reference during work (Alex + user)

### Consolidation Decision Tree

- **>50% overlap** with existing skill → Consolidate INTO it, update tracker as "Consolidated"
- **<50% overlap** → Create new skill, add to tracker as "Migrated"

### Pattern Extraction Template

When documenting a learned pattern:

```markdown
### [Pattern Name]

**Pattern**: [One-sentence description of what to do]

**Example**: [Concrete instance from the session]

**Why**:

- [Reason 1]
- [Reason 2]

**Anti-pattern**: [What NOT to do, if applicable]
```

## Quality Checks

Before committing documentation updates:

- [ ] Markdown lint-clean (blank lines around lists, proper headings)
- [ ] Tables have header separators
- [ ] No orphaned references to deleted files
- [ ] Migration trackers reflect current state
- [ ] Commit message follows conventional format

## Anti-Patterns

| Don't | Do Instead |
| ----- | ---------- |
| Document every minor fix | Only architecture-worthy insights |
| Create new file for each learning | Consolidate into existing structure |
| Wait until end of session | Document as patterns emerge |
| Over-document obvious things | Focus on non-obvious learnings |
| Skip human feedback | Capture corrective principles explicitly |

## User Coaching Learning Loop

User corrections = high-value learning.

**Protocol**: Acknowledge → Fix → Extract principle → Document in skill → Commit

| AI Tendency | User Correction | Extracted Principle |
| ----------- | --------------- | ------------------- |
| Over-centralize | "Don't dump in one file" | Distribute to appropriate locations |
| Over-simplify | "You lost context" | Preserve nuance when consolidating |
| Skip validation | "Did you check it?" | Always verify (lint, count chars) |
| Assume completion | "What about X?" | Follow through on all aspects |
| Add diagrams to skills | "KISS them goodbye" | Skills are for AI, not visual learners |

---

## Connection to Bootstrap Learning

Learn → Coach → Extract → Document → Consolidate

## Synapses

See [synapses.json](synapses.json) for connection mapping.
