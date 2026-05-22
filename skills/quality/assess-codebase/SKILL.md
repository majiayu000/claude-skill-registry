---
name: assess-codebase
description: Assess a codebase for patterns, anti-patterns, and quality opportunities; use when asked to generate coding rules, standards, or quality guidelines.
---

# Assess Codebase

## Overview

Run a multi-agent assessment using CLI subagents and synthesize code quality rules.

## Inputs

- Focus area or directories (optional)
- File patterns (optional)

## Workflow

1. Identify scope and primary languages using `rg --files -g` and recent git activity.
2. Run three CLI subagents (Gemini Flash, Codex, Claude Haiku) using the commands below.
3. Collect outputs, dedupe, and group by patterns, anti-patterns, and opportunities.
4. Draft rules and guidelines with short examples.
5. Save results to `CLAUDE.md` or `AGENTS.md` if requested.

## Subagent Commands

### Gemini Flash (patterns)

```bash
CLOUDSDK_CORE_PROJECT="" GOOGLE_CLOUD_PROJECT="" GCLOUD_PROJECT="" GEMINI_API_KEY=${GEMINI_API_KEY} \
  gemini -m gemini-3-flash-preview -o text "Assess this codebase for patterns in naming, imports, structure, and consistency. Return a structured list with file paths."
```

### Codex (anti-patterns)

```bash
codex exec -m gpt-5.2 -s read-only -c model_reasoning_effort="medium" --skip-git-repo-check \
  "Assess this codebase for anti-patterns (deep nesting, dense one-liners, inconsistent error handling, duplication). Return a structured list with file paths."
```

### Claude Haiku (opportunities)

```bash
claude --model haiku -p "Assess this codebase for clarity, consistency, maintainability, testing, and docs opportunities. Return a structured list with file paths."
```

## Output

- Patterns list
- Anti-patterns list
- Proposed rules and guidelines with priorities
