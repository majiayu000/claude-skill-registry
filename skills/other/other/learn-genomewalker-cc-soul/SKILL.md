---
name: learn
description: Learn from web sources, generate SKILL.md, and store key patterns in soul memory. Trigger keywords: learn, skill-gen, web-learn, documentation, tutorial.
execution: direct
aliases: [web-learn, skill-gen]
---

# Learn

```ssl
[learn] topic|url|repo→discover→fetch→synthesize→SKILL.md+soul

pipeline:
  1. recall: existing knowledge from soul
  2. classify: topic|url|github-repo|npm-pkg|pypi-pkg
  3. discover: WebSearch→candidate sources (if topic)
  4. fetch: API-first→WebFetch fallback→normalize
  5. synthesize: merge sources→SKILL.md with version pin
  6. persist: SKILL.md + triangulated patterns→soul memory

triangulation: promote to memory only if 2+ sources OR 1 canonical
provenance: source, version, retrieved_at, confidence
output: skills/<topic>/SKILL.md + [SOLUTION]/[GOTCHA]/[PATTERN] markers

--global: ~/.claude/skills/<topic>/SKILL.md
--url: skip discovery, fetch directly
--repo: API-first via gh CLI
```

## Usage

```
/learn <topic>                    # Search web, create project-local skill
/learn <topic> --global           # Save to ~/.claude/skills/
/learn <url>                      # Learn from specific URL
/learn <owner/repo>               # Learn from GitHub repository
/learn <topic> --depth shallow    # Quick overview only
/learn <topic> --depth deep       # Comprehensive with examples
```

## Process

### Stage 1: Recall Existing Knowledge

Before any web activity, check what the soul already knows.

```
chitta recall --query "<topic>" --limit 10
```

If soul has relevant memories (< 30 days old), ask:
```
Soul has N memories about <topic>. Refresh from web? (y/N)
```

### Stage 2: Classify Input

| Pattern | Type | Action |
|---------|------|--------|
| `https://...` or `http://...` | URL | Skip to Stage 4 (fetch) |
| `owner/repo` (no dots) | GitHub repo | API-first via `gh` CLI |
| `github.com/owner/repo` | GitHub URL | Extract owner/repo, use `gh` |
| `@scope/package` | npm package | `npm view` + registry API |
| Known PyPI name | PyPI package | `pip show` + PyPI JSON API |
| Everything else | Topic | WebSearch discovery |

### Stage 3: Discover Sources (Topic Mode)

Run targeted web searches:

```
WebSearch: "<topic> documentation guide"
WebSearch: "<topic> tutorial best practices"
WebSearch: "<topic> API reference examples"
```

Rank sources by quality:
1. **Canonical** (highest): Official docs, README, API reference
2. **Authoritative**: Tutorial sites, conference talks, RFCs
3. **Community**: Blog posts (needs triangulation)

Select top 3-5 sources with diversity.

### Stage 4: Fetch and Normalize

**API-first ingestion** (preferred):

For GitHub repos:
```bash
gh api repos/<owner>/<repo> --jq '{name, description, language, topics}'
gh api repos/<owner>/<repo>/readme --jq '.content' | base64 -d
gh api repos/<owner>/<repo>/releases/latest --jq '{tag_name, published_at}'
```

For npm packages:
```bash
npm view <package> name version description homepage --json
```

For PyPI packages:
```bash
pip show <package>
# Or: WebFetch "https://pypi.org/pypi/<package>/json"
```

**WebFetch for HTML** (fallback):

```
WebFetch(url, prompt="Extract: 1) What this does, 2) Key concepts,
3) Installation, 4) Core API with examples, 5) Gotchas, 6) Version info")
```

**JS-rendered docs**: WebFetch cannot execute JavaScript. If minimal content returned:
```
[GOTCHA] <url> appears JS-rendered, content may be incomplete.
Falling back to: GitHub README, API endpoints, or package registry.
```

### Stage 5: Synthesize SKILL.md

Generate SKILL.md with required sections:

```markdown
---
name: <topic>
description: <one-line description>
version: <detected version or "unknown">
retrieved_at: <YYYY-MM-DD>
sources:
  - <url1>
  - <url2>
---

# <Topic>

## Overview
What it is, what problem it solves, when to use it.

## Installation / Setup
Version-pinned commands (npm install x@1.2.3, pip install x==1.2.3).

## Core Concepts
Key abstractions, terminology, mental model.

## Usage Patterns
Code examples for common operations. At least 2 examples.

## API Quick Reference
Key functions/methods with signatures.

## Gotchas and Caveats
Non-obvious behavior. Common mistakes.

## Version Notes
Version this was written for. Breaking changes.
```

**Conflict handling**: If new sources contradict soul memories:
```
[DECISION] <topic>: Web says X, soul says Y. Adopting X because <reason>.
[GOTCHA] <topic>: Previous approach Z no longer recommended as of vN.
```

### Stage 6: Persist

**Write SKILL.md**:

```bash
# Default (project-local)
mkdir -p ./skills/<topic>/
# Write to ./skills/<topic>/SKILL.md

# With --global
mkdir -p ~/.claude/skills/<topic>/
# Write to ~/.claude/skills/<topic>/SKILL.md
```

**Store patterns in soul** (triangulation required):

Only promote patterns confirmed by 2+ sources or 1 canonical source:

```
chitta remember --content "[<topic>:sol] <pattern>"
chitta remember --content "[<topic>:gotcha] <gotcha>"
chitta remember --content "[<topic>:pat] <usage pattern>"
```

Emit markers for stop-hook:
```
[SOLUTION] <topic>: <key approach>
[GOTCHA] <topic>: <trap or caveat>
[PATTERN] <topic>: <recurring pattern>
```

## Quality Gate

| Check | Required | If Missing |
|-------|----------|------------|
| Frontmatter (name, description) | Yes | Add from synthesis |
| At least 1 code example | Yes | Fetch more examples |
| Gotchas section | Yes | Add "[none discovered]" |
| Version-pinned installs | Yes | Pin to latest |
| Sources in frontmatter | Yes | Add all URLs |
| retrieved_at date | Yes | Add current date |

## Output Format

```
## Learn: <Topic>

### Sources Consulted
1. [Official Docs](<url>) - canonical
2. [Tutorial](<url>) - authoritative

### Generated
SKILL.md written to: `<path>`
- Sections: N
- Code examples: N
- Version: <version>

### Stored to Soul
- [SOLUTION] N patterns
- [GOTCHA] N warnings
- Triangulation: N/M patterns confirmed by 2+ sources
```

## Examples

### Learn a Topic
```
/learn duckdb

[Recalling existing knowledge...]
Soul has 2 memories about duckdb.

[Discovering sources...]
1. https://duckdb.org/docs/ (canonical)
2. https://duckdb.org/docs/api/python (canonical)
3. https://motherduck.com/blog/duckdb-tutorial (authoritative)

[Synthesizing SKILL.md...]
SKILL.md written to: ./skills/duckdb/SKILL.md
- Sections: 7, Examples: 5, Version: 1.1.3

[SOLUTION] duckdb: in-memory OLAP, pandas integration via .df()
[GOTCHA] duckdb: default memory limit is 80% RAM
```

### Learn from GitHub
```
/learn duckdb/duckdb

[Fetching via GitHub API...]
  repos/duckdb/duckdb → metadata
  repos/duckdb/duckdb/readme → README
  repos/duckdb/duckdb/releases/latest → v1.1.3

SKILL.md written to: ./skills/duckdb/SKILL.md
```

### Learn from URL
```
/learn https://docs.pydantic.dev/latest/

[Fetching URL directly...]
[Supplementing with WebSearch for triangulation...]

SKILL.md written to: ./skills/pydantic/SKILL.md
```

### Learn Global
```
/learn fastapi --global

SKILL.md written to: ~/.claude/skills/fastapi/SKILL.md
Available across all projects.
```

## Error Handling

| Error | Recovery |
|-------|----------|
| WebSearch no results | Broader query, check spelling |
| WebFetch empty/JS-rendered | GitHub README, API, registry |
| All sources fail | Report, suggest manual URL |
| Recent SKILL.md exists | Ask before overwriting |
| GitHub rate limited | WebFetch fallback |

## Anti-Patterns

- Never generate from single blog post without triangulation
- Never store unverified patterns in soul
- Never omit discoverable version info
- Never use `latest` or unpinned versions in install commands
- Never skip recall stage
- Never announce "I found on the web" -- present knowledge naturally

## MCP Tools Used

| Tool | Stage | Purpose |
|------|-------|---------|
| `recall` | 1 | Check existing knowledge |
| `remember` | 6 | Store confirmed patterns |
| `learn_insight` | 6 | Promote cross-project patterns |
