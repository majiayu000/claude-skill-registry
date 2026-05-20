---
name: scout-repos
description: Fetch .claude/ configs from curated repos in sources.yml, compare against dotforge template, report novel patterns.
---

# Scout Repos

Review curated public repos for Claude Code configuration patterns worth adopting.

## Step 0: Discover tools

WebFetch and WebSearch are deferred tools — they may not be loaded yet.
Run `ToolSearch("WebFetch WebSearch")` to ensure both tools are available before proceeding.

## Step 1: Load sources

Read `$DOTFORGE_DIR/practices/sources.yml`. Build a list of repos with their focus areas.

## Step 2: Fetch each repo's config

For each source, use `gh` CLI to fetch their Claude Code configuration files:

```bash
# Fetch CLAUDE.md
gh api repos/{owner}/{repo}/contents/CLAUDE.md --jq '.content' | base64 -d 2>/dev/null

# Fetch .claude/ directory listing
gh api repos/{owner}/{repo}/contents/.claude --jq '.[].name' 2>/dev/null

# Fetch specific files
gh api repos/{owner}/{repo}/contents/.claude/settings.json --jq '.content' | base64 -d 2>/dev/null
gh api repos/{owner}/{repo}/contents/.claude/rules --jq '.[].name' 2>/dev/null
```

If `gh` fails (rate limit, private repo), try WebFetch on the raw GitHub URL:
```
https://raw.githubusercontent.com/{owner}/{repo}/main/CLAUDE.md
https://raw.githubusercontent.com/{owner}/{repo}/main/.claude/settings.json
```

If both fail, skip the repo and note it in the report.

## Step 3: Analyze patterns

For each repo's config, extract patterns in the source's `focus` areas:

### Hooks
- New hook event/matcher combinations not in dotforge
- Novel blocking logic (different from block-destructive or lint-on-save)
- Hook chaining patterns

### Settings
- Deny list entries we don't have
- Permission patterns (granular vs wildcard)
- Hook wiring approaches

### Rules
- Globs patterns we don't use
- Rule content structure (frontmatter fields, sections)
- Cross-file rule dependencies

### Agents
- Agent definitions with novel roles
- Memory policies different from ours
- Orchestration patterns

### Commands/Skills
- Custom commands we could generalize
- Skill structures with novel step patterns

## Step 4: Compare against dotforge

For each discovered pattern, classify:

- **Novel**: not in dotforge → high interest, describe what it does and where it would go
- **Variant**: similar approach but different implementation → medium interest, note tradeoffs
- **Superior**: does what dotforge does but better → high interest, describe improvement
- **Covered**: dotforge already has this → skip
- **Incompatible**: conflicts with dotforge philosophy (e.g., too complex, too opinionated) → skip with note

## Step 5: Report

```
═══ SCOUT REPOS ═══
Date: {{YYYY-MM-DD}}
Repos analyzed: {{N}}/{{total}}
Repos skipped: {{list of inaccessible repos}}

── NOVEL PATTERNS ──

{{repo}} (focus: {{areas}})
  🆕 {{pattern name}}
     What: {{description}}
     Where: {{file in their repo}}
     Impact on dotforge: {{which files would change}}
     Effort: {{low|medium|high}}

── SUPERIOR PATTERNS ──

{{repo}}
  ⬆️ {{pattern name}}
     Theirs: {{what they do}}
     Ours: {{what we do}}
     Why theirs is better: {{reason}}

── VARIANTS ──

{{repo}}
  🔀 {{pattern name}}
     Difference: {{what's different}}
     Tradeoff: {{why we might or might not adopt}}

── SUMMARY ──
Novel: {{N}} | Superior: {{N}} | Variants: {{N}} | Covered: {{N}}
Repos with most learnings: {{top 2-3 repos}}

── NEXT STEPS ──
For each novel/superior pattern:
  /forge capture "{{description from {{repo}}}}"
Then: /forge update to evaluate and incorporate.
```

## Constraints

- DO NOT modify any dotforge files. Report only.
- DO NOT clone repos locally. Use `gh api` or WebFetch for read-only access.
- Respect rate limits — fetch only files relevant to the source's `focus` areas.
- If a repo has no `.claude/` directory, check for `CLAUDE.md` only. Skip if neither exists.
- Maximum 10 repos per run to avoid rate limiting.
