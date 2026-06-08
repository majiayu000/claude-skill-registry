---
name: research-software
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  Research software tools via source code, GitHub, web. Use when creating skills,
  learning new tools, finding undocumented features, or bleeding-edge patterns.
practices:
- pragmatic-programmer
---
# research-software — Software Research

> **Rules:** Latest STABLE tag (not main). Filter to 2025-2026. Code > Docs. Skip Stack Overflow.

## Output First

Every research produces this structure:

```markdown
## [Tool] vX.Y.Z (YYYY-MM-DD)

**Repo:** github.com/org/repo @ abc123

### Commands
| Task | Command | Notes |
|------|---------|-------|

### Config
| Option | Default | Notes |
|--------|---------|-------|

### Env Vars
| Variable | Purpose |
|----------|---------|

### Gotchas
- [problem]: [fix]. Source: [PR/issue/code]

### Sources
- Code: [file:line]
- PRs: #123, #456
- Posts: [url]
```

---

## THE PROMPT

```
Research [TOOL] for [PURPOSE].
Clone to /tmp, checkout latest stable tag.
Spawn Explore agent on source. Find: CLI, config, hidden flags, env vars.
Parallel: GitHub PRs/issues, web search "[tool] 2025".
Output: skill-ready markdown.
```

---

## Pipeline

```bash
# 0. Detect context (if in a project)
# Check package.json, Cargo.toml, pyproject.toml for existing versions

# 1. Clone + stable tag
git clone --depth 1 https://github.com/[org]/[repo] /tmp/[repo]-research
cd /tmp/[repo]-research && git fetch --tags && git checkout $(git describe --tags --abbrev=0)

# 2. Spawn Explore agent (parallel with step 3-4)
# → "Find all CLI commands, config options, hidden flags, env vars in /tmp/[repo]-research"

# 3. GitHub activity
gh pr list -R [org]/[repo] --state merged --limit 30 --json title,mergedAt
gh issue list -R [org]/[repo] --label question --limit 20

# 4. Web search
# → "[tool] 2025" "[tool] 2026" "[tool] tutorial"

# 5. Synthesize → Output structure above

# 6. Cleanup
rm -rf /tmp/[repo]-research
```

---

## Checklist

- [ ] **Detect context:** Check package.json/Cargo.toml/pyproject.toml for versions
- [ ] **Clone repo** to /tmp, checkout latest stable tag
- [ ] **Explore agent:** CLI commands, config schema, hidden flags, env vars
- [ ] **GitHub:** Recent merged PRs, issues tagged "question"/"documentation"
- [ ] **Web search:** "[tool] 2025", "[tool] 2026", skip pre-2025
- [ ] **Synthesize:** Commands table, config table, gotchas, patterns
- [ ] **Cite sources:** repo@commit, PR numbers, blog URLs
- [ ] **Clean up:** `rm -rf /tmp/[repo]-research`

---

## Source Priority

```
1. Source code (actual behavior)
2. Recent PRs (features being added)
3. GitHub issues (real problems)
4. Blog posts 2025-2026 (practical patterns)
5. Official docs (baseline, often outdated)
```

**Skip:** Stack Overflow, anything pre-2025, basic tutorials

---

## Top Mistakes

| Mistake | Fix |
|---------|-----|
| Using beta/canary | Checkout latest stable TAG, not main |
| Old content (pre-2025) | Always add year to search queries |
| Trusting docs over code | Code wins: check actual defaults in source |
| Missing env vars | Search `process.env`, `std::env`, `os.environ` |
| Forgetting cleanup | `rm -rf /tmp/[repo]-research` when done |

---

## Key Searches

```bash
# Hidden/experimental flags
rg "hidden|experimental|unstable" /tmp/[repo]-research

# Environment variables by language
rg "process\.env\." /tmp/[repo]-research --type ts    # TypeScript
rg "std::env::" /tmp/[repo]-research --type rust      # Rust
rg "os\.environ" /tmp/[repo]-research --type py       # Python
rg "os\.Getenv" /tmp/[repo]-research --type go        # Go

# Recent changes
git log --oneline --since="2025-06-01" | head -30
```

---

## Done When

- [ ] Have version number from stable tag
- [ ] Commands table has 5+ entries
- [ ] Config table covers main options
- [ ] Gotchas section has 3+ real issues from GitHub/code
- [ ] All sources cited with links

---

## Decision Tree

```
What are you researching?
│
├─ CLI tool (wrangler, cargo, bun)
│  Focus: src/cli/, commands, flags, env vars
│
├─ Library/Framework (React, Next.js)
│  Focus: packages/*/src/, exported APIs, deprecations
│
├─ Runtime (Bun, Deno, Node)
│  Focus: built-ins, runtime flags, compat layers
│
└─ Database/Service (D1, R2, Postgres)
   Focus: query syntax, config, limits, gotchas
```

### Key Searches by Type

| Type | Where to look | Key searches |
|------|---------------|--------------|
| CLI | `src/cli/`, `bin/` | `hidden.*true`, `#[arg(`, `process.env` |
| Library | `packages/*/src/`, `index.ts` | `export `, `deprecated`, `experimental` |
| Runtime | `src/`, built-ins | `flag`, `--`, `compat` |
| Database | queries, limits | `limit`, `max`, `error` |

**Deep strategies:** [STRATEGIES.md](references/STRATEGIES.md)

---

## Subagent: Code Investigator

```
Investigate /tmp/[repo]-research for [TOOL].
Find: CLI commands, config options, hidden/experimental flags, env vars.
Check git log --oneline -30 for recent changes.
Output as markdown tables.
```
Use model: `sonnet` (balance of speed + depth)

---

## Subagent: Web Researcher

```
Search "[TOOL] 2025" and "[TOOL] 2026".
Find 5-10 recent tutorials, blog posts, announcements.
Extract: patterns, gotchas, tips.
Skip: Stack Overflow, anything pre-2025, basic tutorials.
```
Use model: `haiku` (fast, web-focused)

---

## References

| Need | File |
|------|------|
| Output templates by tool type | [OUTPUT-TEMPLATES.md](references/OUTPUT-TEMPLATES.md) |
| Example research sessions | [EXAMPLES.md](references/EXAMPLES.md) |
| Tool-specific deep strategies | [STRATEGIES.md](references/STRATEGIES.md) |
