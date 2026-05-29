---
name: neotex-init
description: Use when user runs /neotex-init to deeply scan a codebase and auto-generate organizational knowledge for neotex.
---

# Neotex Codebase Onboarding

Automatically scan a codebase and generate organizational knowledge for neotex. Uses parallel exploration and scoring to capture what matters.

## Prerequisites

```bash
ls .neotex/config.yaml 2>/dev/null || neotex init
```

---

## PHASE 1: MEASURE & SPAWN (Immediate)

### 1.1 Measure Project Scale

Run these commands to understand project size:

```bash
# Total files (excluding node_modules, .git, vendor)
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/vendor/*' | wc -l

# Directory depth distribution
find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*' | awk -F/ '{print NF-1}' | sort -n | uniq -c

# Files per directory (top 20)
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -20

# Detect languages
ls *.go go.mod 2>/dev/null && echo "GO"
ls package.json 2>/dev/null && echo "JS/TS"
ls *.py pyproject.toml setup.py 2>/dev/null && echo "PYTHON"
ls Cargo.toml 2>/dev/null && echo "RUST"
```

### 1.2 Spawn Background Agents (IMMEDIATELY)

**CRITICAL**: Fire these agents in parallel BEFORE doing anything else. Use Task tool with `run_in_background: true`.

**Base agents (always spawn):**

```
Agent 1: "Explore anti-patterns: Search for 'DO NOT', 'NEVER', 'ALWAYS', 'DEPRECATED', 'TODO', 'FIXME', 'HACK' in comments. Report forbidden patterns and technical debt."

Agent 2: "Explore entry points: Find main files, CLI entrypoints, API routes, event handlers. Report non-standard organization."

Agent 3: "Explore conventions: Sample 5-10 source files. Report naming patterns, error handling style, logging approach, test organization. Focus on DEVIATIONS from language defaults."
```

**Dynamic agents (spawn based on scale):**

| Condition | Extra Agents |
|-----------|--------------|
| >100 files | +1 agent: "Explore directory {X}: Document purpose, key files, patterns" |
| >10k lines | +1 agent: "Explore complexity hotspots: Find largest files, most imported modules" |
| Depth ≥4 | +1 agent: "Explore nested structure: Map deep directories, explain hierarchy" |
| Monorepo detected | +1 per package: "Explore package {X}: Purpose, dependencies, API surface" |
| Multiple languages | +1 per language: "Explore {LANG} code: Conventions, build, test patterns" |

---

## PHASE 2: STRUCTURE ANALYSIS (Main Session)

While agents explore, analyze structure yourself:

### 2.1 Read Key Files

```bash
# Identity
cat README.md 2>/dev/null | head -100
cat package.json go.mod Cargo.toml pyproject.toml 2>/dev/null | head -50

# Build/Dev
cat Makefile docker-compose.yaml .env.example 2>/dev/null

# CI/CD
cat .github/workflows/*.yml .gitlab-ci.yml 2>/dev/null | head -100
```

### 2.2 Score Directories

For each major directory, calculate a score:

| Factor | Weight | High Threshold |
|--------|--------|----------------|
| File count | 3x | >20 files |
| Subdirectory count | 2x | >5 subdirs |
| Code ratio (vs config) | 2x | >70% code |
| Has index/main file | 2x | Yes |
| Import frequency | 3x | >20 imports from other dirs |

**Decision thresholds:**
- Score >15 → Document as separate learning
- Score 8-15 → Document if distinct domain
- Score <8 → Skip (parent covers it)

---

## PHASE 3: COLLECT & GENERATE

### 3.1 Collect Background Results

Wait for all background agents to complete. Gather their findings.

### 3.2 Generate Learnings

For each discovery, save to neotex immediately (no prompts):

```bash
echo '{"type":"TYPE","title":"TITLE","body_md":"BODY"}' | neotex add --output
```

### Learning Templates

**Architecture Decision:**
```json
{
  "type": "decision",
  "title": "Uses {pattern} for {purpose}",
  "body_md": "## Context\n{What problem this solves}\n\n## Decision\n{What was chosen}\n\n## Consequences\n{Trade-offs, implications}"
}
```

**Code Guideline:**
```json
{
  "type": "guideline",
  "title": "{Action verb} {what} {how}",
  "body_md": "## Rule\n{The convention}\n\n## Rationale\n{Why this exists}\n\n## Examples\n```{lang}\n{good example}\n```\n\n## Anti-patterns\n```{lang}\n{bad example}\n```"
}
```

**Domain Learning:**
```json
{
  "type": "learning",
  "title": "{Entity/concept}: {key insight}",
  "body_md": "## Overview\n{What this is}\n\n## Key Files\n- `{path}`: {purpose}\n\n## Relationships\n{How it connects to other parts}"
}
```

**Command Snippet:**
```json
{
  "type": "snippet",
  "title": "{Action}: {command}",
  "body_md": "## Command\n```bash\n{command}\n```\n\n## When to Use\n{Context}\n\n## Notes\n{Gotchas, options}"
}
```

### Type Mapping

| Discovery Category | Type | Focus |
|-------------------|------|-------|
| Framework/stack choices | `decision` | Why chosen, trade-offs |
| Architecture patterns | `decision` | Layers, boundaries |
| Naming conventions | `guideline` | Deviations from standard only |
| Error handling | `guideline` | Project-specific patterns |
| Testing approach | `guideline` | Framework, style, mocking |
| Folder structure | `learning` | Non-obvious organization |
| Core entities | `learning` | Domain model |
| Build commands | `snippet` | Dev workflow |
| Anti-patterns | `guideline` | What NOT to do |

---

## PHASE 4: QUALITY GATES

Before saving each learning, verify:

1. **Not generic** - Would this apply to ANY project? Skip it.
2. **Not obvious** - Would a senior dev assume this? Skip it.
3. **Actionable** - Does it help someone DO something? Keep it.
4. **Specific** - Does it reference actual files/patterns? Keep it.

**Examples to SKIP:**
- "Use meaningful variable names"
- "Write tests for your code"
- "Handle errors appropriately"

**Examples to KEEP:**
- "Error responses use `api.Error(w, code, msg)` - never write JSON directly"
- "All repository methods take `ctx context.Context` as first param"
- "Tests use `testify/assert` not standard library"

---

## PHASE 5: SUMMARY REPORT

After all learnings saved, output:

```markdown
## Neotex Onboarding Complete

Scanned {FILE_COUNT} files across {DIR_COUNT} directories.
Spawned {AGENT_COUNT} exploration agents.
Generated {LEARNING_COUNT} learnings.

### Architecture & Decisions ({N})
| Title | Type |
|-------|------|
{list}

### Guidelines & Conventions ({N})
| Title | Type |
|-------|------|
{list}

### Domain & Structure ({N})
| Title | Type |
|-------|------|
{list}

### Commands & Snippets ({N})
| Title | Type |
|-------|------|
{list}

---

**Next steps:**
- `neotex search "<query>"` - Find specific knowledge
- `neotex pull` - Sync to local .neotex/index.json
- Review and delete any unwanted learnings via web UI
```

---

## ERROR HANDLING

- If `neotex add` fails → Log error, continue with others
- If background agent fails → Note in summary, continue
- If file unreadable → Skip silently
- If project too small (<10 files) → Generate minimal learnings, note in summary

---

## GUIDELINES

- **Deviations over defaults** - Only document what's different from standard practices
- **Specific over generic** - Reference actual files, actual patterns
- **Actionable over descriptive** - Help someone DO something
- **Parallel over sequential** - Spawn agents immediately, collect later
- **Score before documenting** - Don't document everything, document what matters
- **Never include secrets** - Skip any file with credentials, keys, tokens
