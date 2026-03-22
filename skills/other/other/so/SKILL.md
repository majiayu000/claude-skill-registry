---
name: so
description: Analyze and improve existing skills against best practices. This skill should be used when asked to optimize, review, audit, or improve a skill's structure, triggers, clarity, or token efficiency. Evaluates 7 dimensions with scoring and optionally researches domain-specific patterns via EXA MCP.
argument-hint: [skill-name] | list
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Task, mcp__exa__get_code_context_exa, mcp__exa__web_search_exa
---

# Skill Optimizer

Analyze existing skills against best practices and apply targeted improvements.

Complements `/skill-creator` (creates new skills) — this skill *improves* existing ones.

## Usage

- `/so [skill-name]` - Analyze a specific skill (e.g., `/so hookify`)
- `/so [path]` - Analyze skill at path (e.g., `/so .claude/skills/hookify`)
- `/so list` - Show all skills with summary stats, then pick one to analyze

Parse `$ARGUMENTS` to determine the target skill.

---

## GATE 0: Resolve Target Skill

### If `$ARGUMENTS` == "list":

1. Glob for `.claude/skills/*/SKILL.md`
2. For each file, extract only the YAML frontmatter (read first 20 lines to get `name` and `description`)
3. Present summary table:

| # | Skill | Description (first 80 chars) |
|---|-------|------------------------------|

4. AskUserQuestion: "Which skill to analyze?" with top skills as options

### If `$ARGUMENTS` is a skill name:

Resolve to `.claude/skills/$ARGUMENTS/SKILL.md`. Verify file exists.

### If `$ARGUMENTS` is a path:

Use the path directly. Verify SKILL.md exists at that location.

### If `$ARGUMENTS` is empty:

AskUserQuestion: "Which skill to analyze? Enter the skill name (e.g., hookify, ct, sr)."

---

## GATE 1: Read & Analyze

### Step 1: Inventory

1. Read the target SKILL.md completely
2. Glob for bundled resources:
   - `[skill-dir]/scripts/*`
   - `[skill-dir]/references/*`
   - `[skill-dir]/assets/*`
   - Any other files in the skill directory
3. Read key reference files if present (to check for orphaned links and content quality)

### Step 2: Score 7 Dimensions

Read [references/evaluation-rubric.md](references/evaluation-rubric.md) for detailed criteria.

Score each dimension 0-10:

| # | Dimension | Focus |
|---|-----------|-------|
| 1 | Frontmatter Quality | name, description, triggers, argument-hint, allowed-tools |
| 2 | Structure & Organization | sections, flow, GATE/STEP patterns, length |
| 3 | Instruction Clarity | imperative voice, actionable steps, error handling, examples |
| 4 | Token Efficiency | word count, progressive disclosure, redundancy |
| 5 | Trigger Precision | specific phrases, breadth, conflicts with other skills |
| 6 | Composability | delegation, related skills, AskUserQuestion usage |
| 7 | Bundled Resources | scripts/references/assets categorization, orphans |

Mark dimension 7 as N/A if the skill genuinely has no need for bundled resources.

### Step 3: Present Report

Format:

```
## Skill Analysis: [skill-name]

**Overall Score: X.X/10** ([rating])

### Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| ... | .../10 | ... |

### Strengths (top 3)
1. ...

### Issues (top 3, prioritized)
1. [CRITICAL/HIGH/MEDIUM] ...
```

**STOP** — present the report and wait for user response before proceeding.

---

## GATE 2: Research (optional)

Scan the SKILL.md content for mentions of:
- Frameworks/libraries (React Native, NestJS, Prisma, Expo, etc.)
- External APIs (Linear, GitHub, OpenAI, Supabase, etc.)
- CLI tools (gh, npm, docker, railway, etc.)
- Domain methodologies (DDD, TDD, Clean Architecture, etc.)

### If references found:

Present the **exact list of detected keywords** to the user first:

AskUserQuestion: "Detected references to: [keyword1, keyword2, keyword3]. Research latest best practices for these? This will query EXA (external search)."

Options:
- "Yes, research all" - query EXA for each keyword
- "Select which to research" - let user pick specific keywords
- "Skip research" - proceed to recommendations

### If user approves:

For each approved keyword:
1. `get_code_context_exa` with query: "[keyword] best practices patterns 2026"
2. Compare findings with skill content
3. Flag discrepancies or outdated patterns
4. Add research findings to the report

### If no external references detected or user skips:

Proceed directly to GATE 3.

---

## GATE 3: Recommendations & Apply

### Step 1: Generate Recommendations

Based on the analysis (and research if done), create prioritized list:

- **CRITICAL** — Blocking issues: missing/broken frontmatter, broken resource references, security issues
- **HIGH** — Significant improvements: vague triggers, missing error handling, >5k words without progressive disclosure
- **MEDIUM** — Polish: voice inconsistency, structure optimization, better examples

Each recommendation includes:
- What to change (specific section/line)
- Why (brief rationale)
- Proposed fix (concrete text or restructuring)

### Step 2: User Selection

AskUserQuestion (multiSelect): "Which improvements to apply?"

List all CRITICAL and HIGH recommendations as options. MEDIUM items listed but marked as optional.

### Step 3: Apply Changes

For each selected improvement:
1. Show the proposed change (old vs new)
2. Apply using Edit tool
3. Confirm each change

### Step 4: Summary

After all changes applied:
1. List all modifications made
2. Show updated scores for affected dimensions
3. Suggest re-running `/so [skill-name]` after testing to verify improvements

---

## Conflict Detection

When evaluating Trigger Precision (dimension 5), check for conflicts:

1. Glob for all `.claude/skills/*/SKILL.md`
2. Extract descriptions from other skills
3. Compare trigger phrases with the analyzed skill
4. Flag overlapping triggers that could cause mis-activation

Report format:
```
Potential trigger conflicts:
- [skill-a] and [skill-b]: both trigger on "create project"
```

---

## Quick Reference: Priority Rules

1. Frontmatter issues are always CRITICAL (skill won't load correctly)
2. Token efficiency >5k words is HIGH (degrades performance)
3. Missing error handling is HIGH for workflow skills, MEDIUM for reference skills
4. Voice inconsistency is always MEDIUM (cosmetic but important)
5. Bundled resource issues are HIGH if files are orphaned, MEDIUM if just mis-categorized
