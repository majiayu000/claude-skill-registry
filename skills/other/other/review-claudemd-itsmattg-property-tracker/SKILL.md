---
name: review-claudemd
description: Audit all CLAUDE.md files for dead references, bloat, and inconsistencies
user-invocable: true
disable-model-invocation: true
---

# /review-claudemd — CLAUDE.md Health Check

Scan all CLAUDE.md and rules files for issues that waste tokens or cause confusion.

## Checks

### 1. Dead File References
For every file path mentioned in CLAUDE.md files and `.claude/rules/*.md`:
- Verify the referenced file exists using Glob
- Flag any missing files as "dead reference"

### 2. Orphaned Skills/Agents
- List all directories in `.claude/skills/` and `.claude/agents/`
- Check each is referenced in root CLAUDE.md
- Flag unreferenced skills/agents

### 3. Token Bloat & Cache Analysis
For each CLAUDE.md file and `.claude/rules/*.md` file:
- Count bytes and approximate tokens (bytes / 4)
- Flag files over 2KB as "consider splitting or moving on-demand"
- Flag duplicate content between CLAUDE.md and rules/ files
- **Budget check:** Root CLAUDE.md should be under 6KB (~1500 tokens). It's a router, not a manual. If over budget, identify sections that are process documentation (things the model already knows) vs gotcha documentation (things the model would get wrong without). Move process docs to on-demand files.
- **Total context cost:** Sum all always-loaded files (CLAUDE.md + rules/*.md + MEMORY.md) and report total. Target: under 20KB (~5000 tokens) for always-loaded context.
- **Cache efficiency:** Check if any rules/ files are also available as on-demand skills (duplication wastes cache). Files that are only relevant for specific workflows (Ralph, deployment) should be in `.claude/contexts/` not `.claude/rules/`.

### 4. Consistency Checks
- All skills in CLAUDE.md `On-Demand Skills` table have matching `.claude/skills/<name>/SKILL.md`
- All agents in CLAUDE.md `Custom Agents` table have matching `.claude/agents/<name>.md`
- All rules in `Scoped Guidance` table have matching files
- Anti-patterns files referenced in `anti-patterns.md` index all exist

### 5. Deprecated API Mentions
Search all CLAUDE.md files for known deprecated patterns:
- `forwardRef` (React 19)
- `useContext` instead of `useUtils` (tRPC v11)
- `getServerSideProps` (App Router)
- `tailwind.config.ts` (Tailwind v4)
- `nonempty()` (Zod v4)

## Output

Present a report:
```
## CLAUDE.md Health Report

### Dead References (X found)
- CLAUDE.md:19 → `.claude/rules/model-routing.md` (MISSING)

### Orphaned Skills (X found)
- `.claude/skills/foo/` not in CLAUDE.md

### Token Usage
| File | ~Tokens | Status |
|------|---------|--------|

### Deprecated APIs (X found)
- src/components/CLAUDE.md:45 mentions `forwardRef`
```
