---
name: learn
description: Extract learnings from current conversation and add to project's CLAUDE.md.
---

# Learn

Extract learnings from the current conversation and add them to the project's CLAUDE.md.

## Steps

1. **Review current conversation for friction moments:**
   - Commands/approaches that failed before finding the right way
   - Non-obvious solutions or workarounds discovered
   - If nothing notable was learned: report "No new learnings to capture." and STOP.

2. **Resolve project CLAUDE.md:**
   - If active session exists: read Working Dir from `_overview.md`, use `[Working Dir]/CLAUDE.md`
   - Otherwise: use `git rev-parse --show-toplevel` to find repo root, use `[repo root]/CLAUDE.md`
   - If CLAUDE.md doesn't exist: create it

3. **Append learnings:**
   - Find or create `## Learnings` section in CLAUDE.md
   - Add one line per learning, format: `- When [situation], [do this / don't do that]`
   - **Generalize as much as possible.** Never reference specific files, variables, or code locations. Extract only generic techniques, rules, and patterns that apply broadly across projects and sessions.
   - Keep it terse — one line, no paragraphs
   - Don't duplicate entries already present

4. **Commit:**
   - `cd [repo root] && git add CLAUDE.md && git commit -m "docs: add learnings"`

5. **Report:**
   - List the learnings added
   - Or: "No new learnings to capture."
