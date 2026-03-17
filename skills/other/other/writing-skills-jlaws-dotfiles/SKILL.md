---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Writing Skills

**Writing skills IS Test-Driven Development applied to process documentation.**

**Personal skills live in agent-specific directories (`~/.claude/skills` for Claude Code, `~/.codex/skills` for Codex)**

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

## When to Create a Skill

**Create when:** Technique wasn't intuitively obvious, reusable across projects, pattern applies broadly, others would benefit.

**Don't create for:** One-off solutions, standard well-documented practices, project-specific conventions (use CLAUDE.md), mechanically enforceable constraints (automate instead).

## Skill Types

- **Technique**: Concrete method with steps (condition-based-waiting)
- **Pattern**: Way of thinking about problems (flatten-with-flags)
- **Reference**: API docs, syntax guides, tool documentation

## Directory Structure

```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```

Separate files for: heavy reference (100+ lines), reusable tools. Keep everything else inline.

## SKILL.md Structure

**Frontmatter:** Only `name` (letters/numbers/hyphens) and `description` (max 1024 chars, third-person, starts with "Use when...")

**CRITICAL:** Description = triggering conditions ONLY. Never summarize the skill's workflow in description. Testing showed Claude follows description shortcuts instead of reading skill body.

```yaml
# BAD: Summarizes workflow
description: Use when executing plans - dispatches subagent per task with code review between tasks

# GOOD: Just triggers
description: Use when executing implementation plans with independent tasks in the current session
```

**Body structure:**
```markdown
# Skill Name
## Overview (1-2 sentences, core principle)
## When to Use (flowchart IF decision non-obvious, bullets with symptoms)
## Core Pattern (before/after code)
## Quick Reference (table/bullets)
## Common Mistakes (what goes wrong + fixes)
```

## Claude Search Optimization (CSO)

- Use concrete triggers/symptoms in description, not language-specific symptoms
- Include keywords Claude would search: error messages, symptoms, tool names
- Name by what you DO: `condition-based-waiting` not `async-test-helpers`
- Gerunds work well: `creating-skills`, `debugging-with-logs`

**Token Efficiency:**
- Getting-started workflows: <150 words
- Frequently-loaded skills: <200 words
- Other skills: <500 words
- Move details to `--help`, use cross-references, compress examples

**Cross-References:** Use `**REQUIRED SUB-SKILL:** Use superpowers:skill-name`. Never use `@` links (force-loads, burns context).

## Flowchart Usage

Use ONLY for: non-obvious decisions, process loops, "when to use A vs B".
Never for: reference material, code examples, linear instructions.

## The Iron Law (Same as TDD)

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Applies to new skills AND edits. Write skill before testing? Delete it. Start over. No exceptions.

## RED-GREEN-REFACTOR for Skills

**RED:** Run pressure scenario WITHOUT skill. Document exact failures and rationalizations.

**GREEN:** Write minimal skill addressing those specific failures. Re-test with skill.

**REFACTOR:** Agent found new rationalization? Add explicit counter. Re-test until bulletproof.

## Testing Skills With Subagents

Run scenarios without skill (RED), write skill addressing failures (GREEN), close loopholes (REFACTOR).

### RED Phase: Baseline Testing

Run pressure scenario WITHOUT skill. Document exact failures.

**Process:**
- [ ] Create pressure scenarios (3+ combined pressures)
- [ ] Run WITHOUT skill
- [ ] Document choices and rationalizations verbatim
- [ ] Identify patterns

### Pressure Types

| Pressure | Example |
|----------|---------|
| Time | Emergency, deadline, deploy window |
| Sunk cost | Hours of work, "waste" to delete |
| Authority | Senior says skip it |
| Exhaustion | End of day, want to go home |
| Pragmatic | "Being pragmatic vs dogmatic" |

**Best tests combine 3+ pressures.**

### Key Elements
1. Concrete A/B/C choices (not open-ended)
2. Real constraints (specific times, consequences)
3. Real file paths
4. Make agent act ("What do you do?" not "What should you do?")

### REFACTOR Phase: Close Loopholes

Capture new rationalizations verbatim. For each, add:
1. **Explicit negation** in rules
2. **Rationalization table** entry
3. **Red flag** entry
4. **Updated description** with violation symptoms

Re-test after each refactor. Continue until no new rationalizations.

### Meta-Testing

After agent chooses wrong: "You read the skill and chose wrong. How could it be clearer?"

Three responses:
1. "Skill WAS clear, I chose to ignore" -> Need stronger foundational principle
2. "Skill should have said X" -> Add their suggestion
3. "I didn't see section Y" -> Make it more prominent

## Persuasion Principles for Skill Design

LLMs respond to the same persuasion principles as humans. Meincke et al. (2025) tested 7 principles with N=28,000 AI conversations. Persuasion techniques doubled compliance rates (33% -> 72%, p < .001).

### Effective Principles

- **Authority**: Imperative language ("YOU MUST", "Never", "Always"), non-negotiable framing. For discipline-enforcing skills.
- **Commitment**: Require announcements, force explicit choices. For ensuring skills are followed.
- **Scarcity**: Time-bound requirements ("Before proceeding"), sequential dependencies. For immediate verification.
- **Social Proof**: Universal patterns ("Every time", "Always"), failure modes. For documenting universal practices.
- **Unity**: Collaborative language ("our codebase", "we're colleagues"). For collaborative workflows.
- **Reciprocity & Liking**: Use sparingly or avoid.

| Skill Type | Use | Avoid |
|------------|-----|-------|
| Discipline-enforcing | Authority + Commitment + Social Proof | Liking, Reciprocity |
| Guidance/technique | Moderate Authority + Unity | Heavy authority |
| Collaborative | Unity + Commitment | Authority, Liking |
| Reference | Clarity only | All persuasion |

## Anthropic Best Practices

### Core Principles
- **Concise is key**: Only add what Claude doesn't already know. Challenge each piece: "Does Claude need this?"
- **Degrees of freedom**: High (text instructions) for multiple valid approaches; Medium (pseudocode) for preferred patterns; Low (exact scripts) for fragile operations

### Anti-Patterns
- Offering too many library options (provide a default with escape hatch)
- Assuming packages installed (list dependencies)
- Deeply nested references (keep one level deep)
- Time-sensitive information (use "old patterns" section)

### Evaluation-Driven Development
1. Run Claude on tasks without Skill, document failures
2. Create 3+ evaluation scenarios
3. Establish baseline performance
4. Write minimal instructions to pass evaluations
5. Iterate: evaluate, compare baseline, refine

## Skill Creation Checklist

**RED Phase:**
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run WITHOUT skill - document baseline failures verbatim
- [ ] Identify rationalization patterns

**GREEN Phase:**
- [ ] YAML frontmatter: name (letters/numbers/hyphens), description (Use when..., third-person)
- [ ] Address specific baseline failures
- [ ] Keywords throughout for search
- [ ] One excellent code example (not multi-language)
- [ ] Run WITH skill - verify compliance

**REFACTOR Phase:**
- [ ] Add counters for new rationalizations
- [ ] Build rationalization table and red flags list
- [ ] Re-test until bulletproof

**Deployment:**
- [ ] Commit and push
