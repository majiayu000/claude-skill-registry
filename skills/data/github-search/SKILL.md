---
name: github-search
description: "Search GitHub for repos, code, and usage examples using gh CLI. Capabilities: repo discovery, code search, finding library usage patterns, issue/PR search. Actions: search, find, discover repos/code/examples. Keywords: gh, github, search repos, search code, find examples, how to use library, stars, language filter. Use when: finding repositories, searching code patterns, discovering how libraries are used, exploring open source."
allowed-tools: Bash, Read
---

# GitHub Search

## Quick Commands

| Goal | Command |
|------|---------|
| Search repos | `gh search repos "<query>" --limit 30` |
| Search code | `gh search code "<query>" --limit 30` |
| Search issues | `gh search issues "<query>" --limit 30` |
| Search PRs | `gh search prs "<query>" --limit 30` |

## Patterns

### Finding Repositories

**When you see:** User wants to find projects/repos by criteria
**Use:** `gh search repos`

```bash
# Basic search with stars
gh search repos "stars:>500 language:rust" --sort=stars --limit=50

# Multiple languages (OR logic)
gh search repos "language:rust language:go language:typescript"

# Exclude topics
gh search repos "stars:>1000 -topic:cryptocurrency -topic:blockchain"

# By topic
gh search repos "topic:cli topic:terminal stars:>100"

# Recently updated
gh search repos "language:python pushed:>2024-01-01"
```

**Output formats:**
```bash
--json name,url,description,stargazersCount  # JSON output
--web                                         # Open in browser
```

### Finding Code Examples

**When you see:** User wants to know how to use a library
**Use:** `gh search code`

```bash
# Find usage patterns
gh search code "from zod import" --limit=20
gh search code "import { z } from 'zod'" --limit=20

# In specific file types
gh search code "useQuery" extension:tsx --limit=30

# In specific paths
gh search code "tanstack/query" path:src/ extension:ts

# Exact phrase
gh search code '"createTRPCRouter"' extension:ts
```

**Pro tip:** Combine with repo filter for focused results:
```bash
gh search code "pattern" repo:owner/repo
```

### Finding Issues/Discussions

**When you see:** User looking for bug reports, feature requests, or discussions
**Use:** `gh search issues` or `gh search prs`

```bash
# Open issues with label
gh search issues "is:open label:bug repo:facebook/react"

# PRs by author
gh search prs "author:username is:merged"

# Issues mentioning error
gh search issues '"connection refused" language:go'
```

## Query Qualifiers Reference

### Repo Search
| Qualifier | Example | Description |
|-----------|---------|-------------|
| `stars:` | `stars:>1000`, `stars:100..500` | Star count |
| `forks:` | `forks:>100` | Fork count |
| `language:` | `language:rust` | Primary language |
| `topic:` | `topic:cli` | Repository topic |
| `-topic:` | `-topic:blockchain` | Exclude topic |
| `pushed:` | `pushed:>2024-01-01` | Last push date |
| `created:` | `created:>2023-01-01` | Creation date |
| `license:` | `license:mit` | License type |
| `archived:` | `archived:false` | Archive status |
| `is:` | `is:public`, `is:private` | Visibility |

### Code Search
| Qualifier | Example | Description |
|-----------|---------|-------------|
| `extension:` | `extension:ts` | File extension |
| `path:` | `path:src/` | File path |
| `repo:` | `repo:owner/name` | Specific repo |
| `language:` | `language:javascript` | Code language |
| `filename:` | `filename:package.json` | File name |

### Common Flags
| Flag | Description |
|------|-------------|
| `--limit N` | Number of results (max 1000) |
| `--sort X` | Sort by: stars, forks, updated, best-match |
| `--order X` | asc or desc |
| `--json FIELDS` | JSON output with specific fields |
| `--web` | Open results in browser |

## Common Use Cases

### "Find popular X repos"
```bash
gh search repos "language:X stars:>500" --sort=stars --limit=50
```

### "How do people use library Y"
```bash
gh search code "import Y" extension:ts --limit=30
gh search code "from Y import" extension:py --limit=30
```

### "Find repos like Z but exclude crypto"
```bash
gh search repos "topic:Z -topic:cryptocurrency -topic:blockchain -topic:web3"
```

### "Find recent active projects"
```bash
gh search repos "language:go pushed:>2024-06-01 stars:>100" --sort=updated
```

## Tips

1. **Quote the query** when it contains special chars: `gh search repos "stars:>500"`
2. **Multiple languages = OR**: `language:rust language:go` matches either
3. **Use `--json`** for scripting: `--json name,url,stargazersCount`
4. **Date ranges**: `pushed:2024-01-01..2024-06-01`
5. **Numeric ranges**: `stars:100..500`
