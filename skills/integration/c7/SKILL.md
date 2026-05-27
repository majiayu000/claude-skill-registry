---
name: c7
description: "Fetches up-to-date library documentation from Context7 and saves to /tmp/context7/. Use when needing current API docs, code examples, library references, SDK documentation, or checking latest library versions. Triggers: context7, c7, library docs, fetch docs, current documentation, api reference."
allowed-tools:
  - Bash(scripts/c7.sh:*)
  - AskUserQuestion
---

# c7 - Context7 Documentation Fetcher

Fetch-only skill. Does NOT read docs into context.

## Usage

### Fetch documentation

```bash
scripts/c7.sh <library-name> "<query>"
```

Example:
```bash
scripts/c7.sh nextjs "app router middleware"
```

### List cached docs

```bash
scripts/c7.sh --list
```

### Force re-fetch (bypass cache)

```bash
scripts/c7.sh --force <library-name> "<query>"
```

## Workflow

1. Run `scripts/c7.sh <library> "<query>"`
2. Handle output:
   - `CACHED: <path> (Xh old)` → Use AskUserQuestion: "Documentation for X is already cached (Y hours old). Use cached version or fetch fresh?"
     - If re-fetch → run with `--force`
     - If use cached → inform user of location, done
   - Success (path printed) → inform user: "Documentation saved to <path>"
   - `NOT_FOUND:` → Use AskUserQuestion: "Library not found in Context7. How should I proceed?" with options like retry with different name, skip, etc.
   - `RATE_LIMITED:` → inform user rate limit hit, stop
   - `API_ERROR:` → inform user of error, stop

3. Done. Do NOT read the file into context.

## Exit Codes

| Code | Output | Action |
|------|--------|--------|
| 0 | filepath | Success - report location |
| 0 | CACHED: path | Ask user: use cache or re-fetch? |
| 1 | NOT_FOUND: | Ask user for alternatives |
| 2 | RATE_LIMITED: | Inform user, stop |
| 3 | API_ERROR: | Inform user, stop |
| 4 | FUZZY_MATCH: | Ask user: "Context7 matched X instead of Y. Use this or try different name?" |
