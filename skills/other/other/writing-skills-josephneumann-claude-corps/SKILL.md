---
name: writing-skills
description: "Use when writing a new SKILL.md, revising an existing skill's instructions, or converting a repeated workflow into a reusable skill."
allowed-tools: Read, Bash, Glob, Grep, Edit, Write
---

# Skill Authoring Guide

## Structure

From CSO (Claude Search Optimization) research:

- **Description**: Contains ONLY triggering conditions ("Use when..."). Never workflow summaries. If the description tells the agent what the skill does internally, the agent will shortcut the full skill content.
- **Word count targets**: <200 for frequently-invoked, <500 for standard, <800 max. Verify with `wc -w` before finalizing.
- **Cross-reference, don't duplicate**: Reference other skills inline with context-specific takeaways (e.g., `**Verification discipline** (from /verify): <what to do here>`). Never copy full content between skills — summarize the relevant point and cite the source.
- **For discipline skills**: Include an anti-rationalization table (excuse/reality pairs from observed failures), an Iron Law (one-line absolute rule), and a Red Flags list (thoughts that signal rationalization).

## Tone

Skills are persuasive documents. They must sound authoritative and human, not like AI slop.

**Avoid**:
- Significance inflation: "crucial", "pivotal", "vital", "key" (just state the rule)
- Promotional language: "groundbreaking", "powerful", "seamless"
- Sycophantic tone: "Great!", "Of course!", "Certainly!"
- Filler: "In order to", "It is important to note that"
- Excessive hedging: "could potentially", "might possibly"
- Copula avoidance: "serves as", "stands as" (just use "is")
- Em dash overuse, emoji decoration, bold-header lists

**Do**:
- Vary sentence length. Short for rules. Longer for context.
- Have a voice. Don't write like a press release.
- Be specific. "Run tests before claiming completion" beats "ensure verification"

## Persuasion Principles

LLMs respond to the same persuasion techniques as humans (Meincke et al., 2025):

- **Authority**: Imperative language for rules ("YOU MUST", "NEVER", "ALWAYS")
- **Commitment**: Required announcements, explicit choices, checkboxes
- **Social Proof**: Universal framing ("Every time", "Always", "No exceptions")

These techniques doubled compliance rates in studies. Use them deliberately in discipline-enforcing skills.

## Checklist Before Finalizing

1. `wc -w` — within target?
2. Description — triggering conditions only?
3. No duplication — cross-references instead?
4. Anti-rationalization table — built from observed failures, not hypothesized?
5. Read it aloud — does it sound human?

*Informed by obra/superpowers writing-skills skill and persuasion-principles reference*
