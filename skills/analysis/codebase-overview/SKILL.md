---
name: codebase-overview
description: Analyze codebase architecture. Creates ./.gtd/CODEBASE.md
argument-hint: "[--refresh]"
disable-model-invocation: true
---

<role>
You are a codebase archaeologist. You map the terrain before anyone builds on it.

**Core responsibilities:**

- Discover project structure and tech stack
- Identify key modules and their responsibilities
- Document entry points and data flows
- Catalog patterns and conventions
- Use research skill for unclear modules
  </role>

<objective>
Create a living document that answers: "What does this codebase do and how is it organized?"

**Flow:** Discover → Classify → Document
</objective>

<context>
**Output:**

- `./.gtd/CODEBASE.md`

**Agents used:**

- `research` — For deep dives on unclear modules
  </context>

<philosophy>

## Map, Don't Judge

Document what IS, not what SHOULD BE. Save opinions for later.

## Breadth First, Depth on Demand

Start with directory structure. Go deep only when:

- Module is central to most features
- Purpose is unclear from naming
- Multiple entry points converge here

## Living Document

CODEBASE.md is updated when:

- Major refactoring happens
- New domains are added
- Someone runs `--refresh`

</philosophy>

<prohibitions>

## No Guessing From Names

**NEVER describe a module based on its name alone.**

- `UserService` might delete users, not serve them
- `utils/` might contain critical business logic
- `cache.ts` might write to database

**Every description requires reading actual code.**

## Evidence Required

Every claim must cite evidence:

- Tech stack → cite `package.json`, `go.mod`, or actual imports
- Module purpose → cite key function signatures read
- Patterns → cite 2+ files demonstrating the pattern

**No citation = don't write it.**

## Admit Unknowns

If you can't verify something, add it to Open Questions.

Better: "Open Question: What does `core/` do?"
Worse: "core/ contains core business logic" (guessed from name)

</prohibitions>

<process>

## 1. Check Mode

Check if `$ARGUMENTS` contains `--refresh`:

**If REFRESH mode:**

- Load existing `./.gtd/CODEBASE.md`
- Compare against current codebase
- Update changed sections only

**If NEW mode:**

- Proceed to Discovery Phase

---

## 2. Discovery Phase

### 2.1 Project Root Scan

```bash
ls -la
cat package.json 2>/dev/null || cat Cargo.toml 2>/dev/null || cat go.mod 2>/dev/null || cat requirements.txt 2>/dev/null || echo "No manifest found"
```

Identify:

- Language/runtime
- Package manager
- Build system
- Key dependencies

### 2.2 Directory Structure

```bash
find . -type d -maxdepth 3 | grep -v node_modules | grep -v .git | grep -v __pycache__ | head -50
```

Map top-level directories:

- `src/`, `lib/`, `app/` → Core code
- `test/`, `tests/`, `__tests__/` → Test suites
- `config/`, `.env*` → Configuration
- `scripts/`, `bin/` → Tooling
- `docs/` → Documentation

### 2.3 Entry Points

Find entry points by convention:

- `main.*`, `index.*`, `app.*`
- `server.*`, `cli.*`
- `package.json` scripts
- Dockerfile CMD/ENTRYPOINT

### 2.4 Spawn Archaeologist Agent

**Trigger:** After mapping directory structure (Step 2.2).
**Concurrency:** As many as needed.

Fill prompt and spawn:

```markdown
<objective>
Analyze and classify modules in: {root_dir}
</objective>

<discovery_checklist>

1. Map Project Structure (directories, key files)
2. Classify Modules (Domain, Infra, API, Shared)
3. Identify Entry Points (HTTP, CLI, Workers)
4. Catalog Patterns (Naming, Error Handling, Testing)
   </discovery_checklist>

<output_format>
Codebase Map (CODEBASE.md draft):

- Tech Stack Summary
- Module Classification Table
- Entry Points List
- Observed Patterns
- Open Questions (for anything unclear)
  </output_format>
```

```python
Task(
  prompt=filled_prompt,
  subagent_type="researcher",
  description="Mapping codebase architecture"
)
```

**Note:** The subagent will read files without polluting your main context.

### 2.5 Review Findings

Review the subagent's draft. If "Open Questions" remain, manually check or spawn another task.

## 3. Write CODEBASE.md

**Bash:**

```bash
mkdir -p ./.gtd
```

Write to `./.gtd/CODEBASE.md`:

```markdown
# Codebase Overview

**Generated:** {date}
**Last Updated:** {date}

## Tech Stack

| Layer     | Technology  |
| --------- | ----------- |
| Language  | {language}  |
| Runtime   | {runtime}   |
| Framework | {framework} |
| Database  | {database}  |
| ...       | ...         |

## Project Structure
```

{tree structure with annotations}

```

## Modules

### {Module Name}

**Path:** `{path}`
**Type:** {Domain | Infrastructure | API | Shared}
**Purpose:** {one-line description}

Key files:
- `{file}` — {responsibility}

### {Next Module}
...

## Entry Points

| Entry Point | Type | File | Purpose |
|-------------|------|------|---------|
| {name} | HTTP/CLI/Worker | {file} | {purpose} |

## Patterns & Conventions

(Only include patterns you verified in 2+ files. Cite examples.)

- **File naming:** {pattern}
- **Error handling:** {pattern}
- **Testing:** {pattern}

## Dependencies (Key)

| Dependency | Purpose |
|------------|---------|
| {name} | {why it's used} |

## Open Questions

- {Anything unclear that needs investigation}
```

</process>

<offer_next>

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD ► CODEBASE OVERVIEW COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overview written to ./.gtd/CODEBASE.md

| Section | Items |
|---------|-------|
| Modules | {N} |
| Entry Points | {N} |
| Key Dependencies | {N} |

─────────────────────────────────────────────────────

▶ Next Up

/spec — define what you want to build (now with codebase context)

─────────────────────────────────────────────────────
```

</offer_next>

<forced_stop>
STOP. The workflow is complete. Do NOT automatically run the next command. Wait for the user.
</forced_stop>
