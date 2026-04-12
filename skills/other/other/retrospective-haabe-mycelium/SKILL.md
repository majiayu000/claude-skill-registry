---
name: retrospective
description: "Structured retrospective after completing a delivery increment or diamond. Captures learning for continuous improvement."
---

# Retrospective

Run after every completed delivery diamond or significant milestone. Source: Forsgren (learning culture).

## Format

### 1. What Went Well?
- Which patterns from patterns.md were reused successfully?
- What new approaches worked?
- Where did the theory gates catch a real problem?

### 2. What Didn't Go Well?
- What mistakes were made? (Add to corrections.md)
- Where did we skip a guardrail and regret it?
- What took longer than expected and why?

### 3. What Should Change?
- New corrections to add
- New patterns to capture
- Process improvements
- Guardrail adjustments

### 4. BVSSH Dimension Check
- **Better**: Did quality improve or degrade?
- **Value**: Did we deliver actual user value?
- **Sooner**: Was our flow efficient?
- **Safer**: Did we maintain security and trust?
- **Happier**: How is team satisfaction?

## Blameless Post-Mortem Format (SRE)

For incidents or significant failures, use the SRE blameless post-mortem:
1. **Timeline**: What happened, when, in what order
2. **Impact**: Who was affected, how severely, for how long
3. **Contributing factors**: What conditions led to this (NOT "who caused it")
4. **Root cause**: The systemic issue, not the human action
5. **Action items**: Specific, assigned, time-bound improvements
6. **What went well**: What prevented it from being worse

Rule: No blame. Focus on the system, not the person. *Source: Beyer et al. (SRE)*

## Refactoring Prompt

After delivery retrospective, always ask:
- "Are there refactoring opportunities? Duplicated logic (DRY)? Unnecessary complexity (KISS)?"
*Source: Beck (XP), Fowler (Refactoring)*

## Output
1. Update `.claude/memory/corrections.md` with new corrections
2. Update `.claude/memory/patterns.md` with new patterns
3. Update `.claude/memory/delivery-journal.md` with retrospective entry
4. Update canvas/bvssh-health.yml if dimensions changed
5. Log in decision-log.md
