---
name: use-skill-create
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

**Writing skills IS Test-Driven Development applied to process documentation.**

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand autonome:use-tdd before using this skill.

# What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

# When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)
- Mechanical constraints (automate with regex/validation)

# The Iron Law (Same as TDD)

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

Write skill before testing? Delete it. Start over.

# RED-GREEN-REFACTOR for Skills

## RED: Write Failing Test (Baseline)

Run pressure scenario with subagent WITHOUT the skill. Document exact behavior:
- What choices did they make?
- What rationalizations did they use (verbatim)?
- Which pressures triggered violations?

## GREEN: Write Minimal Skill

Write skill that addresses those specific rationalizations.

Run same scenarios WITH skill. Agent should now comply.

## REFACTOR: Close Loopholes

Agent found new rationalization? Add explicit counter. Re-test until bulletproof.

# SKILL.md Structure

**Frontmatter (YAML):**
- Only two fields: `name` and `description`
- Max 1024 characters total
- `name`: Letters, numbers, hyphens only
- `description`: Third-person, "Use when..." format
  - **CRITICAL:** Describe ONLY triggering conditions
  - **NEVER summarize the skill's process or workflow**
  - Keep under 500 characters

**Why no workflow in description:** Testing revealed that when descriptions summarize workflow, Claude may follow the description instead of reading the full skill content. Descriptions should only answer "Should I read this skill right now?"

**Body sections:**
```markdown
# Skill Name

Core principle in 1-2 sentences.

# When to Use

Bullet list with SYMPTOMS and use cases
When NOT to use

# The Process / Pattern

Clear, numbered steps or comparison

# Red Flags

What indicates you're about to violate

# Common Rationalizations

Table of excuses vs. reality
```

# Key Principles

**Token Efficiency:**
- Target <200 words for frequently-loaded skills
- Move details to tool help
- Use cross-references (don't repeat)
- Compress examples
- Eliminate redundancy

**Claude Search Optimization (CSO):**
- Keywords: Error messages, symptoms, synonyms, tools
- Descriptive naming: Verb-first, active voice
- No workflow summaries in description

**Bulletproofing Against Rationalization:**
- Close every loophole explicitly
- Address "Spirit vs Letter" arguments
- Build rationalization table from testing
- Create red flags list

# Testing Skill Types

**Discipline-Enforcing Skills (TDD, verification):**
- Test with pressure scenarios
- Multiple combined pressures (time + sunk cost + exhaustion)
- Identify rationalizations, add explicit counters

**Technique Skills (how-to guides):**
- Application scenarios
- Variation scenarios
- Missing information tests

**Pattern Skills (mental models):**
- Recognition scenarios
- Application scenarios
- Counter-examples

# Skill Creation Checklist

**RED Phase:**
- [ ] Create pressure scenarios (3+ combined pressures)
- [ ] Run WITHOUT skill - document baseline verbatim
- [ ] Identify patterns in rationalizations

**GREEN Phase:**
- [ ] Name uses only letters, numbers, hyphens
- [ ] Description starts with "Use when..." (no workflow)
- [ ] Keywords throughout for search
- [ ] Address specific baseline failures
- [ ] Run scenarios WITH skill - verify compliance

**REFACTOR Phase:**
- [ ] Identify NEW rationalizations
- [ ] Add explicit counters
- [ ] Build rationalization table
- [ ] Create red flags list
- [ ] Re-test until bulletproof

**Deployment:**
- [ ] Commit skill to git

# The Bottom Line

**Creating skills IS TDD for process documentation.**

Same Iron Law: No skill without failing test first.
Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes).

If you follow TDD for code, follow it for skills.
