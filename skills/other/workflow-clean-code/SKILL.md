---
name: clean-code
description: Comprehensive clean code workflow that analyzes codebase, recommends best practices, and applies clean code principles for React, Next.js, and modern tooling.
argument-hint: "[-a] [-e] [-s] [-r <id>] <feature/file>"
---

<objective>
Fast, systematic clean code improvements using parallel agents.
</objective>

<quick_start>
**Basic usage (analyze and apply clean code principles):**
```bash
/clean-code auth feature
```

**Auto mode (skip confirmations):**
```bash
/clean-code -a dashboard
```

**With save (output to `.claude/output/clean-code/`):**
```bash
/clean-code -s -a refactor api
```

**What it does:**
1. Scans codebase for issues (React, Next.js, Zustand, TanStack Query)
2. Loads relevant best practices docs
3. Applies clean code improvements
4. Verifies with build and tests
5. Commits changes
</quick_start>

<parameters>

| Flag | Description |
|------|-------------|
| `-a` | Auto mode: skip confirmations |
| `-e` | Economy mode: no subagents, direct tools only |
| `-s` | Save mode: output to `.claude/output/clean-code/` |
| `-r` | Resume mode: continue from previous task |
| `--react` | Force load React 19 patterns |
| `--nextjs` | Force load Next.js 15/16 patterns |
| `--zustand` | Force load Zustand v5 patterns |
| `--query` | Force load TanStack Query v5 patterns |

<examples>
```bash
/clean-code auth feature          # Basic
/clean-code -a dashboard          # Auto mode
/clean-code -e -a fix types       # Economy + auto
/clean-code -s refactor api       # Save outputs
/clean-code -r auth-feature       # Resume
/clean-code --nextjs --query data # Force docs
```
</examples>

</parameters>

<workflow>
```
SCAN → APPLY → VERIFY
  │       │       │
  │       │       └─ Build, test, commit
  │       └─ Load docs, recommend, apply
  └─ Parse flags, detect tech, find issues
```
</workflow>

<state_variables>

| Variable | Type | Description |
|----------|------|-------------|
| `{task_description}` | string | What to analyze |
| `{task_id}` | string | Kebab-case identifier |
| `{auto_mode}` | boolean | Skip confirmations |
| `{economy_mode}` | boolean | No subagents |
| `{save_mode}` | boolean | Save outputs |
| `{detected_tech}` | object | Technologies found |
| `{issues}` | array | Issues found |

</state_variables>

<reference_files>

| File | When Loaded |
|------|-------------|
| `references/general-clean-code.md` | Always |
| `references/react-clean-code.md` | React detected / `--react` |
| `references/nextjs-clean-code.md` | Next.js detected / `--nextjs` |
| `references/zustand-best-practices.md` | Zustand detected / `--zustand` |
| `references/tanstack-query-best-practices.md` | No data fetching / `--query` |

</reference_files>

<entry_point>

Load `steps/step-01-scan.md`

</entry_point>

<step_files>

| Step | File | Purpose |
|------|------|---------|
| 01 | `step-01-scan.md` | Init + analyze |
| 02 | `step-02-apply.md` | Load docs + apply |
| 03 | `step-03-verify.md` | Build + commit |

</step_files>

<execution_rules>
- Load one step at a time
- Use parallel agents in step-01 (unless economy mode)
- Always run build before completing
- Follow patterns from reference files exactly
</execution_rules>

<success_criteria>
- Technologies correctly detected (React, Next.js, Zustand, TanStack Query)
- Issues identified and documented
- Relevant reference docs loaded
- Clean code improvements applied
- Build passes without errors
- Tests pass (if tests exist)
- Changes committed with clear message
- No hacks or shortcuts used
</success_criteria>
