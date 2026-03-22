---
name: dev-docs-review
description: Review all project documentation for staleness — READMEs, skills, plans, CLAUDE.md, project structure trees
argument-hint: "[--fix] [--lesson <track>/<NN>] [--pr <number>]"
disable-model-invocation: false
---

Sweep every documentation file in the repo for staleness, inaccuracy, and gaps.
This catches stale project structure trees, completed plan items that should be
removed, missing READMEs, skill docs referencing deleted files, and lesson lists
that are behind the actual lesson count.

**When to use this skill:**

- After a batch of lessons or features lands on main
- After a major refactor that moved files or directories
- Periodically (monthly) to keep docs honest
- Before tagging a release or milestone

The user optionally provides:

- `--fix` — auto-fix issues where possible (update trees, prune plans, add
  missing READMEs). Without this flag, report findings only.
- `--lesson <track>/<NN>` — review only docs relevant to a specific lesson
  (e.g. `--lesson gpu/37`). See "Lesson-scoped review" below.
- `--pr <number>` — review only the documentation files changed in a pull
  request (e.g. `--pr 199`). See "PR-scoped review" below.

## Lesson-scoped review (`--lesson`)

When `--lesson <track>/<NN>` is provided, skip the full parallel sweep and
instead run a single focused agent that checks only the documentation touched
by that lesson. This is fast and useful right after creating or updating a
lesson.

**Resolve the lesson** from the argument:

- `<track>` is `gpu`, `math`, `ui`, `engine`, `assets`, `physics`, or `audio`
- `<NN>` is the lesson number (zero-padded or not)
- Find the actual directory: glob `lessons/<track>/<NN>-*` to get the full
  slug (e.g. `gpu/37` → `lessons/gpu/37-3d-picking/`)
- If no directory matches, report an error and exit

**Files to review:**

| File | What to check |
|------|---------------|
| `lessons/<track>/README.md` | Lesson listed in the track's lesson table (GPU track uses screenshot gallery table) |
| `lessons/<track>/<NN>-*/README.md` | Lesson README exists, links are valid, diagrams referenced exist in `assets/` |
| `scripts/forge_diagrams/README.md` | Diagram count and lesson count for the track are accurate |
| `scripts/forge_diagrams/<track>/lesson_<NN>.py` | Diagram module exists if lesson has diagrams |
| `.claude/skills/*/SKILL.md` | Find the skill created for this lesson (search for the lesson name or number), verify its path references are valid |
| `PLAN.md` (root) | Lesson is not still listed as a TODO if it exists and is complete |

**Checks per file:**

1. **Track `README.md`** (`lessons/<track>/README.md`):
   - The lesson is listed in the track's lesson table. For the GPU track,
     this is a screenshot gallery table (thumbnail + name + description).
     For other tracks, it is a markdown table.
   - If missing, add the lesson entry in the correct format for that track.
   - **Skills list (GPU track):** The GPU README has an "Available skills"
     bullet list. If the lesson has a matching skill in `.claude/skills/`,
     verify it appears in this list. If missing, add it.

2. **Lesson `README.md`** (`lessons/<track>/<NN>-*/README.md`):
   - Exists. If missing, report (don't auto-generate — lesson READMEs are
     substantive).
   - All `assets/*.png` references point to files that exist.
   - All internal links (e.g. to other lessons, common/ headers) are valid.

3. **Diagram infrastructure:**
   - If `scripts/forge_diagrams/<track>/lesson_<NN>.py` exists, verify it is
     re-exported in `scripts/forge_diagrams/<track>/__init__.py` (the track
     package `__init__.py` surfaces modules to the `__main__.py` registry).
   - Check that `scripts/forge_diagrams/README.md` counts are still accurate
     (total diagrams, per-track lesson counts).

4. **Lesson skill:**
   - Search `.claude/skills/*/SKILL.md` for references to the lesson number
     or slug. The matching skill is the one created alongside the lesson (e.g.
     `forge-stencil-testing` for lesson 34).
   - Verify all path references in that skill doc are valid.

5. **Root `PLAN.md`:**
   - If the lesson directory exists and is complete (has `main.c` + README),
     it should not appear as an unchecked TODO in the plan.

**Report format (lesson-scoped):**

```text
Lesson Documentation Review: <track>/<NN>-<slug>
═══════════════════════════════════════════════════

Root README:              ✓ ok | X issues (Y fixed)
Track README:             ✓ ok | X issues (Y fixed)
Lesson README:            ✓ ok | X issues (Y fixed)
Diagram infrastructure:   ✓ ok | X issues (Y fixed)
Lesson skill:             ✓ ok | X issues (Y fixed)
Root PLAN.md:             ✓ ok | X issues (Y fixed)

Details:
────────────────────────────────────────────
[Findings, if any]
```

## PR-scoped review (`--pr`)

When `--pr <number>` is provided, review only the documentation files changed
in that pull request. This is useful after a PR lands to verify that all the
docs it touched are consistent.

**Get the changed files:**

```bash
gh pr diff <number> --name-only
```

**Filter to documentation files** — keep only files matching:

- `*.md` (READMEs, PLANs, lesson docs)
- `.claude/skills/*/SKILL.md` (skill docs)
- `CLAUDE.md`
- `scripts/forge_diagrams/README.md`

Discard non-documentation files (`.c`, `.h`, `.py`, `.hlsl`, etc.).

**For each documentation file changed in the PR, check:**

1. **README.md files** (root, track, lesson, scripts, etc.):
   - Project structure trees (in CLAUDE.md, scripts/) match the filesystem
   - Track READMEs list all existing lesson directories for that track
   - Internal links are valid
   - Diagram counts are accurate (for `scripts/forge_diagrams/README.md`)
   - Note: the root README is intentionally minimal — no structure trees,
     no full lesson lists, no skills tables. Do not add them back.

2. **SKILL.md files:**
   - File path references point to files that exist
   - Cross-references name skills that exist
   - Lesson references match actual directories
   - Code examples use current import paths and function names

3. **PLAN.md:**
   - Completed items (lessons that exist, merged PRs) are removed or marked done
   - Lesson numbers and names match actual directories

4. **CLAUDE.md:**
   - Project structure tree matches filesystem
   - Cross-references are valid

**Report format (PR-scoped):**

```text
PR Documentation Review: #<number> — <title>
═══════════════════════════════════════════════

Files reviewed: N documentation files changed in PR

<file-path>:          ✓ ok | X issues (Y fixed)
<file-path>:          ✓ ok | X issues (Y fixed)
...

Details:
────────────────────────────────────────────
[Findings, if any]
```

## Full review (no `--lesson` or `--pr` flag)

When no `--lesson` flag is given, run the full parallel sweep described below.

## Team structure

This review runs as **parallel agents** — each agent owns one review area and
works independently. Launch all agents at once, then collect results.

### Agent 1: Project structure trees and root README

**Goal:** Verify every project structure tree matches the actual filesystem,
and verify the root README library lists are current.

1. **Find all structure trees** — search for `├──` or `└──` in:
   - `CLAUDE.md`
   - `scripts/README.md`
   - `scripts/forge_diagrams/README.md`
   - Any other `README.md` that contains a tree
   - Note: the root `README.md` is intentionally minimal and does NOT contain
     a structure tree or full lesson lists — do not add them back.

2. **For each tree**, extract the listed paths and compare against the real
   filesystem:
   - **Missing entries** — directories or files that exist but are not in the
     tree (e.g. a new `common/` module, a new lesson, a new track)
   - **Stale entries** — paths listed in the tree that no longer exist
   - **Wrong descriptions** — comments that don't match the directory contents

3. **Root README library list** — the root `README.md` has a "What you'll get"
   section that lists shared libraries as inline links like
   `[math](common/math/)`. Verify this list matches the actual `common/*/`
   directories that have a README (i.e. are real library modules, not empty
   or placeholder dirs). Flag any `common/` library that exists and is
   documented but is missing from the root README's library list.
   Note: the root README is intentionally minimal — no structure trees,
   no full lesson lists, no skills tables. Do not add them back.

4. **Lesson lists** — verify each track's own README lists all lessons for
   that track. The GPU track (`lessons/gpu/README.md`) uses a screenshot
   gallery table (thumbnail + name + description). Other tracks use markdown
   tables. Check that every `lessons/<track>/NN-*` directory has a row.

5. **Skills lists** — the GPU track README (`lessons/gpu/README.md`) has a
   "Available skills" bullet list mapping each lesson to its Claude Code skill.
   Verify that every lesson with a matching skill in `.claude/skills/` has an
   entry in this list. Cross-reference by globbing `.claude/skills/*/SKILL.md`
   for skills that reference a GPU lesson.

6. **Report** each finding with file, line number, and what's wrong.

7. **If `--fix`:** Edit the trees to match reality. Add missing entries, remove
   stale ones, fix descriptions. Add missing libraries to the root README
   lists. Do not rewrite working trees — only patch the diffs.

### Agent 2: PLAN.md and lesson PLANs

**Goal:** Remove completed items and verify remaining items are current.

1. **Root `PLAN.md`** — read the roadmap:
   - Items that reference merged PRs or lessons that exist → mark as completed
     or remove
   - Items referencing features that have landed → remove or move to a "done"
     section
   - Verify lesson numbers and names match actual directories
   - Check for duplicate or contradictory items

2. **Lesson `PLAN.md` files** — glob `lessons/**/PLAN.md`:
   - If the lesson is complete (has `main.c`, README, assets), the PLAN.md
     may still contain stale task assignments, agent decompositions, or TODOs
     that were completed. These are fine to keep as historical records — do
     NOT delete lesson PLANs.
   - But check for references to files/paths that have moved (e.g. old
     diagram file paths)

3. **Report** each finding.

4. **If `--fix`:** Update the root PLAN.md. Leave lesson PLANs as-is (they
   serve as historical records of how the lesson was built).

### Agents 3a–3d: Skill documentation (batched)

**Goal:** Verify all skill SKILL.md files reference correct paths and patterns.

**CRITICAL: Context limit batching.** There are 60+ skills. A single agent
reading all of them will hit context limits and fail. Split skill verification
into **batches of ~10 skills per agent**. Launch all batch agents in parallel.

**How to batch:**

1. Glob all skill directories: `ls -d .claude/skills/*/`
2. Sort alphabetically and split into groups of 10
3. Launch one agent per group, giving it the explicit list of 10 skill paths

Each batch agent does the same work:

1. **For each skill in its batch**, read the SKILL.md and check:
   - **File path references** — every path mentioned should exist in the repo.
     Flag paths to deleted or moved files.
   - **Cross-references** — references to other skills (e.g. "use
     `/dev-create-diagram`") should name skills that actually exist.
   - **Lesson references** — lesson numbers and names should match actual
     directories (e.g. "based on Lesson 28" should link to a real lesson).
   - **Naming convention** — every skill directory and `name:` field must use
     the correct prefix. Lesson skills (any track) use `forge-` (e.g.
     `forge-stencil-testing`, `forge-bloom`), development/workflow skills use
     `dev-` (e.g. `dev-create-pr`, `dev-gpu-lesson`). Flag any skill
     whose directory name lacks the expected prefix. Check that the `name:`
     field in the YAML frontmatter matches the directory name exactly.

2. **Work efficiently** — scan for path references, verify against the
   filesystem, move on. Don't read every line in detail — focus on paths
   and cross-refs.

3. **Report** each finding with skill name and issue. Report "No issues" if
   the batch is clean.

4. **If `--fix`:** Update path references and `name:` fields. Rename skill
   directories to match the naming convention (`git mv` the directory). Update
   all references to the old directory name across the repo (lesson READMEs,
   track READMEs, other SKILL.md cross-references). Do NOT rewrite skill
   logic or workflows — only fix factual inaccuracies and naming.

### Agent 4: README coverage

**Goal:** Find directories that would benefit from a README but don't have one.

1. **Scan directories** that should have READMEs:
   - `common/*/` — every library module should have a README
   - `lessons/*/` — every track should have a README
   - `lessons/*/*/` — every lesson should have a README
   - `pipeline/` — should have a README
   - `docs/` — `building.md` (build guide) and any other docs
   - `tests/` — could benefit from a README
   - `tools/` — each tool directory
   - `scripts/` and subdirectories
   - `.claude/skills/` — a top-level README explaining the skill system

2. **For directories that have READMEs**, quick-check:
   - Does the README mention all major files in the directory?
   - Is the description still accurate? (e.g. does it mention features that
     were added since the README was written?)
   - Are internal links still valid?

3. **Report** directories missing READMEs, and READMEs that appear stale.

4. **If `--fix`:** Write READMEs for directories that need them. Keep them
   short — a one-paragraph description, a file listing, and usage examples
   where applicable. Do NOT write READMEs for trivial directories (build/,
   `__pycache__/`, etc.).

### Agent 5: CLAUDE.md consistency

**Goal:** Verify CLAUDE.md is accurate and complete.

1. **Code conventions** — spot-check 3-5 recent lessons to verify the
   documented conventions (naming, error handling, line endings) match actual
   practice. Flag conventions that are documented but not followed, or
   practices that are followed but not documented.

2. **Testing section** — verify the documented test commands work:
   - `cmake --build build --target test_gltf`
   - `ctest --test-dir build`
   - `uv run pytest tests/pipeline/`
   - Check for new test targets that should be documented

3. **Shader compilation** — verify the documented commands match the actual
   script arguments.

4. **Dependencies** — verify the listed dependencies are current. Check for
   new dependencies that should be listed.

5. **Cross-references** — all lesson references, library references, and skill
   references should be valid.

6. **Report** each finding.

7. **If `--fix`:** Update CLAUDE.md sections that are factually wrong. Do NOT
   add new conventions or change the tone — only fix inaccuracies.

## Collecting results

After all agents complete, combine their findings into a single report:

```text
Documentation Review Summary
═══════════════════════════════════════════

Project Structure Trees + Root README:  X issues found
Plans:                                 X issues found
Skill Documentation:                   X issues found
README Coverage:                       X issues found
CLAUDE.md Consistency:                  X issues found

Total:                          X issues found (Y auto-fixed)

Details:
────────────────────────────────────────────
[Full findings from each agent, grouped by area]
```

If `--fix` was specified, show what was changed. If not, show what would need
to change.

## What this skill does NOT do

- Does not review lesson content quality (use `/dev-final-pass` for that)
- Does not check code correctness (use tests and linters)
- Does not review diagram accuracy (use `/dev-review-diagrams`)
- Does not check markdown formatting (use `/dev-markdown-lint`)
- Does not modify skill logic or workflows — only fixes factual references
