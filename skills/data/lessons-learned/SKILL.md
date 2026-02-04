---
name: lessons-learned
description: Use when capturing discoveries after phase completion, before shipping, or when reflecting on completed work to extract reusable patterns
---

<!-- TOKEN BUDGET: 150 lines / ~450 tokens -->

# Lessons Learned

## Overview

The lessons-learned system captures discoveries, patterns, and pitfalls found during implementation and feeds them back into project memory. Lessons are stored in `.shipyard/LESSONS.md` and optionally surfaced in `CLAUDE.md` so future agents benefit from past experience.

## When to Use

- After phase completion during `/shipyard:ship` (Step 3a)
- When reflecting on completed work to extract reusable knowledge
- When a build summary contains notable discoveries worth preserving

## LESSONS.md Format

Store lessons in `.shipyard/LESSONS.md` using this exact structure:

```markdown
# Shipyard Lessons Learned

## [YYYY-MM-DD] Phase N: {Phase Name}

### What Went Well
- {Bullet point}

### Surprises / Discoveries
- {Pattern discovered}

### Pitfalls to Avoid
- {Anti-pattern encountered}

### Process Improvements
- {Workflow enhancement}

---
```

New entries are prepended after the `# Shipyard Lessons Learned` heading so the most recent phase appears first. Each phase gets its own dated section with all four subsections.

## Structured Prompts

Present these four questions to the user during lesson capture:

1. **What went well in this phase?** -- Patterns, tools, or approaches that worked effectively.
2. **What surprised you or what did you learn?** -- Unexpected behaviors, new techniques, or revised assumptions.
3. **What should future work avoid?** -- Anti-patterns, dead ends, or approaches that caused problems.
4. **Any process improvements discovered?** -- Workflow changes, tooling suggestions, or efficiency gains.

Pre-populate suggested answers from build artifacts before asking (see Pre-Population below).

## Pre-Population

Before presenting prompts, extract candidate lessons from completed build summaries:

1. Read all `SUMMARY-*.md` files in `.shipyard/phases/{N}/results/`.
2. Extract entries from **"Issues Encountered"** sections -- these often contain workarounds and edge cases.
3. Extract entries from **"Decisions Made"** sections -- these capture rationale worth preserving.
4. Present extracted items as pre-populated suggestions the user can accept, edit, or discard.

This reduces friction and ensures discoveries documented during building are not lost.

## Memory Enrichment

If the `shipyard:memory` skill is available and memory is enabled:

1. Search memory for the milestone's date range and project path.
2. Use Haiku to extract insights about:
   - Debugging struggles and resolutions
   - Rejected approaches and why they failed
   - Key decisions and their rationale
3. Add memory-derived insights to candidates (marked separately from summary-derived).

Memory captures implicit knowledge from conversation context that may not appear in formal SUMMARY.md files.

## CLAUDE.md Integration

After the user approves lessons, optionally append a summary to the project's `CLAUDE.md`:

1. **Check for CLAUDE.md** -- If no `CLAUDE.md` exists in the project root, skip this step entirely.
2. **Find existing section** -- Look for a `## Lessons Learned` heading in `CLAUDE.md`.
3. **Append if exists** -- Add new bullet points under the existing `## Lessons Learned` section.
4. **Create if missing** -- If `CLAUDE.md` exists but has no `## Lessons Learned` section, append the section at the end of the file.
5. **Format for CLAUDE.md** -- Use concise single-line bullets. Omit phase dates; focus on actionable guidance:
   ```markdown
   ## Lessons Learned
   - Bash `set -e` interacts poorly with pipelines -- use explicit error checks after pipes
   - jq `.field // "default"` prevents null propagation in optional config values
   ```

## Quality Standards

Lessons must be **specific, actionable, and reusable**. Apply these filters:

**Good lessons** (specific, transferable):
- "Bash `set -e` interacts poorly with pipelines -- use explicit error checks after pipes"
- "jq `.field // \"default\"` prevents null propagation in optional config values"
- "bats-core `run` captures exit code but swallows stderr -- use `2>&1` to capture both"

**Bad lessons** (too vague or too specific):
- "Tests are important" -- too generic, not actionable
- "Fixed a bug on line 47" -- too specific, not transferable
- "Code should be clean" -- vague platitude
- "Changed variable name from x to y" -- implementation detail, not a lesson

**Anti-Patterns to reject:**
- Lessons that duplicate existing entries in LESSONS.md
- Lessons that reference specific line numbers or ephemeral file locations
- Lessons that are generic truisms rather than discovered knowledge
- Lessons longer than two sentences -- split or summarize

## Integration

**Referenced by:** `commands/ship.md` Step 3a for post-phase lesson capture.

**Pairs with:** `shipyard:shipyard-verification` for validating lesson quality before persisting.
