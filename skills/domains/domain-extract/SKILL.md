---
name: domain-extract
description: Extract domain knowledge from existing project sources and generate domain rules. Also handles vault sync and domain listing.
context: fork
---

# Domain Extract

Analyze existing project sources to propose domain knowledge rules for approval.

## Dispatch

Based on $ARGUMENTS after "domain":
- `domain extract` → Step 1-5 (full extraction)
- `domain list` → Step 6 (list only)
- `domain sync-vault` → Step 7 (vault sync only)

---

## Step 1: Gather sources

Read these project sources (skip any that don't exist):

1. **CLAUDE.md** — sections below `<!-- forge:custom -->` (user-written content)
2. **Auto-memory** — resolve the project's memory directory:
   - Compute project path hash: the memory lives in `~/.claude/projects/-<path-with-dashes>/memory/`
   - Read MEMORY.md index, then read each linked memory file
   - Filter: keep only entries with business/domain content (not purely technical)
3. **CLAUDE_ERRORS.md** — read all entries. Flag errors where the root cause is "Claude didn't know X about the business"
4. **Agent memory** — read `.claude/agent-memory/implementer/*.md` and `.claude/agent-memory/architect/*.md`
   - Filter: keep domain-relevant learnings (business logic, API behavior, deployment procedures)
5. **Existing rules** — read all `.claude/rules/*.md`. Identify files that mix domain + technical content
6. **Git log** — run `git log --oneline -50` to identify domain-related commits (keywords: fix, deploy, API, auth, config)

## Step 2: Classify findings

For each piece of domain knowledge found, classify:

- **Category**: deploy, api-integration, business-logic, data-model, auth-flow, external-service, workflow
- **Source**: which file(s) it came from
- **Confidence**: high (explicit in CLAUDE.md/rules), medium (in memory/errors), low (inferred from git)
- **Overlap**: does it duplicate existing `.claude/rules/domain/*.md` content?

Discard:
- Pure technical patterns (import order, test fixtures, lint rules)
- Already covered by existing domain rules
- One-time fixes that won't recur

## Step 3: Generate proposals

Group findings by category. For each group, propose a domain rule file:

```
═══ DOMAIN EXTRACT ═══
Project: {{project_name}}
Sources analyzed: {{count}}
Existing domain rules: {{count in .claude/rules/domain/}}

── PROPOSED DOMAIN RULES ──

{{number}}. {{filename}}.md (from: {{sources}})
   globs: {{suggested glob patterns}}
   Content preview:
     "{{3-5 line summary of what the rule will contain}}"
   → Create? (y/n/edit)
```

Also propose a Role section if CLAUDE.md doesn't have `## Role` yet:

```
── ROLE SECTION ──
Detected role from project context:
  "{{proposed role description}}"
  → Add to CLAUDE.md ## Role? (y/n/edit)
```

And a Domain section if CLAUDE.md doesn't have `## Domain` yet:

```
── DOMAIN SECTION ──
Detected domain context:
  "{{proposed domain summary}}"
  → Add to CLAUDE.md ## Domain? (y/n/edit)
```

## Step 4: Wait for user approval

STOP and WAIT for the user to respond to each proposal (y/n/edit).

If the user says "edit", ask what to change and regenerate that specific proposal.
If the user says "all", approve all proposals.

## Step 5: Create approved files

For each approved domain rule:

1. Create `.claude/rules/domain/` directory if not exists
2. Write the file with frontmatter:
   ```yaml
   ---
   globs: "{{patterns}}"
   description: "{{one-line description}}"
   domain: {{category}}
   last_verified: {{today YYYY-MM-DD}}
   ---
   ```
3. Content: imperative mood, concise facts, <40 lines per file
4. All content in English (Claude-consumed content rule)

For approved Role/Domain sections:
1. Read current CLAUDE.md
2. If `## Role` marker exists, replace content. If not, add section before `## Arquitectura`
3. If `## Domain` marker exists, replace content. If not, add section after `## Role`

Show summary:
```
═══ DOMAIN EXTRACT — DONE ═══
Created: {{N}} domain rules in .claude/rules/domain/
Updated: CLAUDE.md (Role: ✓/✗, Domain: ✓/✗)
Total domain knowledge: {{N}} files
```

---

## Step 6: Domain list (for `/forge domain list`)

List all files in `.claude/rules/domain/` with metadata:

```
═══ DOMAIN RULES ═══
File              Domain    Globs                          Last Verified   Status
─────────────────────────────────────────────────────────────────────────────────
ratios.md         trading   **/*ratio*,**/*price*          2026-03-15      ⚠ stale (>90d)
deploy-vps.md     infra     **/*deploy*,docker-compose*    2026-03-25      ✓ current
jira-api.md       jira      **/*jira*,**/*issue*           2026-03-20      ✓ current
```

Status rules:
- `✓ current` — last_verified within 90 days
- `⚠ stale` — last_verified older than 90 days
- `✗ no date` — missing last_verified field

If no `.claude/rules/domain/` exists: "No domain rules found. Run `/forge domain extract` to generate from existing sources."

---

## Step 7: Vault sync (for `/forge domain sync-vault`)

For each file in `.claude/rules/domain/` that has `domain_source: vault://...` in frontmatter:

1. Resolve path: replace `vault://` with `~/vault/`
2. Read the vault note at that path
3. Compare key facts in the vault note vs the domain rule
4. If differences found:
   ```
   ══ VAULT SYNC ══
   File: ratios.md
   Source: vault://decisions/ratio-engine.md
   
   Changes detected:
     + New: "ONs use factor 0.001 for sub-peso bonds"
     ~ Changed: exit ratio now uses mid-price, not ask
   
   → Update domain rule? (y/n/edit)
   ```
5. If approved: update the domain rule content, set `last_verified` to today
6. If vault note not found: warn and skip

If no files have `domain_source`: "No vault-linked domain rules found. Add `domain_source: vault://path` to a domain rule frontmatter to enable sync."

---

## Constraints

- NEVER auto-create files without user approval — always show proposals first
- Domain rules go in `.claude/rules/domain/`, never in `.claude/rules/` root
- All generated content must be in English (Claude-consumed)
- Keep each domain rule file under 40 lines
- Frontmatter fields: globs (required), description (required), domain (required), last_verified (required), domain_source (optional)
- If a project has no meaningful domain knowledge in its sources, say so honestly — don't generate empty placeholder files
