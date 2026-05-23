---
name: project
description: Clone and track external repos. Use when user shares GitHub URL to study or develop, or says "search repos", "find repo", "where is [project]". Actions - learn (clone for study), incubate (clone for development), search/find (search repos), list (show tracked).
---

# project-manager

Track and manage external repos: Learn (study) | Incubate (develop)

## Golden Rule

**ghq owns the clone → ψ/ owns the symlink**

Never copy. Always symlink. One source of truth.

## When to Use

Invoke this skill when:
- User shares a GitHub URL and wants to study/clone it
- User mentions wanting to learn from a codebase
- User wants to start developing on an external repo
- Need to find where a previously cloned project lives

## Actions

### learn [url|slug]

Clone repo for **study** (read-only reference).

```bash
# 1. Clone via ghq
ghq get -u https://github.com/owner/repo

# 2. Create flat symlink (NOT nested!)
GHQ_ROOT=$(ghq root)
ln -sf "$GHQ_ROOT/github.com/owner/repo" ψ/learn/repo-name
```

**Output**: "✓ Linked [repo] to ψ/learn/repo-name"

### incubate [url|slug]

Clone repo for **active development**.

```bash
# Same flow, different target
ghq get -u https://github.com/owner/repo
GHQ_ROOT=$(ghq root)
ln -sf "$GHQ_ROOT/github.com/owner/repo" ψ/incubate/repo-name
```

**Output**: "✓ Linked [repo] to ψ/incubate/repo-name"

### find [query]

Search for project across all locations:

```bash
# Search ghq repos
ghq list | grep -i "query"

# Search learn/incubate symlinks
ls -la ψ/learn/ ψ/incubate/ 2>/dev/null | grep -i "query"
```

**Output**: List matches with their ghq paths

### list

Show all tracked projects:

```bash
echo "📚 Learn"
ls -la ψ/learn/ | grep "^l" | awk '{print "  " $NF " → " $11}'

echo "🌱 Incubate"
ls -la ψ/incubate/ | grep "^l" | awk '{print "  " $NF " → " $11}'

echo "🏠 External (ghq)"
ghq list | head -10
```

## Directory Structure

```
ψ/
├── learn/<slug>     → ~/Code/github.com/owner/repo  (symlink)
└── incubate/<slug>  → ~/Code/github.com/owner/repo  (symlink)

~/Code/               ← ghq root (source of truth)
└── github.com/owner/repo/  (actual clone)
```

## Health Check

When listing, verify symlinks are valid:

```bash
# Check for broken symlinks
find ψ/learn ψ/incubate -type l ! -exec test -e {} \; -print 2>/dev/null
```

If broken: `ghq get -u [url]` to restore source.

## Examples

```
# User shares URL
User: "I want to learn from https://github.com/SawyerHood/dev-browser"
→ ghq get -u https://github.com/SawyerHood/dev-browser
→ ln -sf ~/Code/github.com/SawyerHood/dev-browser ψ/learn/dev-browser

# User wants to develop
User: "I want to contribute to claude-mem"
→ ghq get -u https://github.com/thedotmack/claude-mem
→ ln -sf ~/Code/github.com/thedotmack/claude-mem ψ/incubate/claude-mem
```

## Anti-Patterns

| ❌ Wrong | ✅ Right |
|----------|----------|
| `git clone` directly to ψ/ | `ghq get` then symlink |
| Nested paths: `ψ/learn/repo/github.com/...` | Flat: `ψ/learn/repo-name` |
| Copy files | Symlink always |
| Manual clone outside ghq | Everything through ghq |

## Quick Reference

```bash
# Add to learn
ghq get -u URL && ln -sf "$(ghq root)/github.com/owner/repo" ψ/learn/name

# Add to incubate
ghq get -u URL && ln -sf "$(ghq root)/github.com/owner/repo" ψ/incubate/name

# Update source
ghq get -u URL

# Find repo
ghq list | grep name
```
