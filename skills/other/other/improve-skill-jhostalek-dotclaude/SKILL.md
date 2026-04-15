---
name: improve-skill
description: Use when the user asks to improve, compare, audit, or identify gaps in an existing skill.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, Task, WebFetch, WebSearch
argument-hint: <skill-name>
---

skill_name = $ARGUMENTS

If no argument, ask.

## Finding the Skill

Search in order: `~/.claude/skills/{skill_name}/SKILL.md` → `~/.claude/skills/{skill_name}/*.md` → `.rulesync/skills/{skill_name}/SKILL.md`. Read completely, including referenced files.

## Philosophy

The goal is often making a skill *shorter*, not longer — cutting bloat is as valuable as adding techniques. Subtraction requires independent judgment formed *before* seeing what competitors do. Research without a prior assessment just produces parroting.

## Self-Assessment

Form hypotheses before external research. Assess two dimensions:

### Capability Gaps & Contradictions

What the skill likely should do but doesn't. Where it contradicts its own philosophy.

### Agent-Execution Quality

Evaluate the skill as a *prompt for an executing agent*, not a document for a human. This is the higher-value analysis — most skills have acceptable coverage but poor prompt engineering.

| Check | What to look for |
|-------|-----------------|
| **Why-motivation** | Unmotivated directives (MUST/NEVER/ALWAYS without reasoning) get dropped by agents under pressure. Count them. |
| **Adaptive scaling** | Does workflow adjust to task complexity? A 2-file task shouldn't trigger the same pipeline as a 50-file task. |
| **Progressive disclosure** | Skills over ~300 lines of core workflow suffer attention dilution. Are details in reference files loaded on demand? |
| **Failure mode awareness** | "You'll be tempted to skip this because..." outperforms "MUST complete this step." Does the skill anticipate agent failure modes? |
| **Escape hatches** | Can the agent skip phases that don't apply? |
| **Constraint density** | Above ~5 unmotivated constraints per 100 lines = attention dilution risk. |
| **Tone** | Explanatory ("because X, do Y") > directive ("NEVER do X"). Explanatory tone lets the agent reason about edge cases. |
| **File references** | `!path/to/file.md` (inline injection) > plain paths (requires extra read). |
| **Phantom constraints** | Instructions the model would follow anyway. If no competitor bothers instructing it, the model handles it without being told. |

Write down all hypotheses. Research will validate or invalidate them.

## Competitive Research

Spawn **three research teammates in parallel**. For each: read the prompt file from `${CLAUDE_SKILL_DIR}/agents/<name>.md`, pass its full content as the teammate's prompt, prepend the skill summary and your hypotheses for context.

| Teammate | File | Purpose |
|----------|------|---------|
| System Prompts Analyzer | `agents/system-prompts.md` | Compare against other AI coding tools' system prompts |
| Ecosystem Scanner | `agents/ecosystem.md` | Search open skills registry for similar skills |
| Vendor Docs Researcher | `agents/vendor-docs.md` | Search vendor docs and best practices |

## Synthesis & Report

After all teammates complete, look for: which hypotheses research validated, insights that emerge from *combining* sources, and what to cut — apply the **phantom constraint test**: if no competitor instructs it and the model would do it anyway, flag for removal.

Present as a single consolidated report:

**1. Executive summary** (2-3 sentences) — ahead, behind, or on par? Over-engineered, under-engineered, or right-sized?

**2. Agent-execution quality assessment:**

| Check | Current State | Recommendation | Priority |
|-------|--------------|----------------|----------|

**3. Gap analysis:**

| Category | Have | Missing | Could Cut | Priority | Sources |
|----------|------|---------|-----------|----------|---------|

**4. Recommended removals** — concrete sections to delete, with rationale.

**5. Recommended additions** — highest-impact first, with concrete text. Severity: CRITICAL (most competitors have it, significantly impacts quality) → HIGH → MEDIUM → LOW.

**6. Net effect** — will the skill get longer, shorter, or stay the same? Aim for shorter-or-same.

**7. Unique strengths** to preserve.

**8. Anti-patterns** — techniques from competitors to explicitly NOT adopt, with reasoning.

**STOP.** Wait for user approval before modifying anything.

## Implementation (After Approval)

Apply removals before additions — models default to additive changes; subtract first to prevent the skill from growing. Convert plain file paths to `!path/to/file.md` inline injection where appropriate. Report net line count change — a negative number is a good sign.

When rewriting, apply the `/prompt` skill's design principles.
