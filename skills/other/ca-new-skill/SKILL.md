---
name: ca-new-skill
description: "Author a new codeArbiter skill: prove the gap is real, get the spec approved, then write it."
argument-hint: "<verb-noun skill name>"
---

# /ca-new-skill — author a skill

The only permitted entry to creating a skill. Nothing is written until the gap is proven uncovered — skills are not created speculatively. Name the skill in verb-noun form (`"dependency-review"`), not as a description (`"the thing that checks packages"`).

## Flow

Routes to the `skill-author` skill, which owns the work end to end through its five gated phases — gap
evidence, scope, authoring, self-review against the v2 house style, and routing integration (the
`INDEX.md` + routing-table entry that makes the new skill reachable). The phase definitions live in the
skill; this command does not restate them. Nothing is authored until an existing skill or agent is
proven not to cover the need; nothing ships until the new skill carries gated phases, hard rules, and
its routing entry.

## Routes to

`skill-author` (`<plugin-root>/routines/skill-author/SKILL.md`) — all five phases.

## When NOT to use

- A one-time action → `/ca-feature` or a command definition.
- An existing skill nearly covers it → extend that skill via `/ca-feature`.
- "Do we even need a skill here?" → `/ca-btw`.

## Hard gate

MUST prove the gap is real in Phase 1 before writing any skill content. MUST get user approval on the
spec before authoring. MUST NOT create a skill that duplicates an existing skill's purpose — surface
the overlap instead. Skill files live only under `<plugin-root>/routines/<name>/`.
