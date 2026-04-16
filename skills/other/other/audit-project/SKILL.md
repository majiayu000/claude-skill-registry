---
name: audit-project
description: Audits the Claude Code configuration of a project against the dotforge template. Generates a report with score and gaps.
context: fork
---

# Audit Project

Run a full audit of the Claude Code configuration for the current project.

## Step 1: Detect stack

Use detection rules from `$DOTFORGE_DIR/stacks/detect.md`.

## Step 1b: Detect project tier

Auto-detect project tier based on signals:
- **simple** (<5K LOC, 1 stack, no CI config): recommended items are relaxed (items 8-10 don't penalize)
- **standard** (5K-50K LOC, 1-2 stacks): default behavior
- **complex** (>50K LOC, 3+ stacks, monorepo indicators like `packages/` or `apps/`): recommended items 8-10 become semi-obligatory (each worth 0-2 instead of 0-1)

Detection signals:
1. LOC: count non-empty lines in source files (`find . -name '*.py' -o -name '*.ts' -o -name '*.js' -o -name '*.go' -o -name '*.java' -o -name '*.swift' | xargs wc -l`)
2. Stack count: number of stacks detected in step 1
3. CI: presence of `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`
4. Monorepo: presence of `packages/`, `apps/`, `lerna.json`, `pnpm-workspace.yaml`, `turbo.json`

Save tier in registry entry.

## Step 1c: Config coherence check

Before scoring, validate internal coherence. Run `$DOTFORGE_DIR/tests/test-config.sh <project-dir>` or perform equivalent checks inline:

1. Hooks referenced in settings.json exist and are executable
2. Rules have valid `globs:` or `paths:` frontmatter (with `alwaysApply: false` for lazy loading)
3. Rule globs match at least 1 real file in the project
4. settings.json is valid JSON with deny list covering .env, *.key, *.pem
5. CLAUDE.md has minimum required sections (stack, build/test, architecture)
6. No contradictory allow+deny patterns in settings.json
7. No prompt injection patterns in rules or CLAUDE.md

If coherence check finds critical failures (missing hooks, invalid JSON), report them in a `── COHERENCE ──` section BEFORE the score. These are configuration bugs, not gaps.

## Step 2: Load checklist

Read `$DOTFORGE_DIR/audit/checklist.md` for evaluation criteria.
Read `$DOTFORGE_DIR/audit/scoring.md` for weights and caps.

## Step 3: Evaluate

For each checklist item, verify existence **and quality**:

### Obligatory (0-10 points)
1. **CLAUDE.md** — Does it exist? Verify it has key sections:
   - Stack/technologies mentioned explicitly
   - At least 1 exact build/test command
   - Project structure or architecture
   - Do NOT count only lines — a 50-line boilerplate file is score 1
2. **settings.json** — Does it exist in `.claude/`? Does it have explicit permissions? Does it have a deny list?
3. **Rules** — Is there at least 1 rule in `.claude/rules/`? Does it have frontmatter with `globs:` or `paths:`?
4. **Hook block-destructive** — Verify:
   - Does `.claude/hooks/block-destructive.sh` exist?
   - Is it executable? (`test -x` or check permissions)
   - Is it referenced in `.claude/settings.json` under hooks?
5. **Build/test commands** — Are they in CLAUDE.md? Do they match the detected stack?

### Recommended (0-7 bonus points)
6. **CLAUDE_ERRORS.md** — Does it exist with table format with Type column?
7. **Hook lint** — Does it exist? Is it executable? (verify `chmod +x`)
8. **Custom commands** — Are there files in `.claude/commands/`?
9. **Memory** — Are there project memory files?
10. **Agents** — Is there `.claude/agents/` + `agents.md` rule in rules?
11. **.gitignore** — Does it protect .env, *.key, *.pem, credentials?
12. **Prompt injection scan** — Are rules/CLAUDE.md free of suspicious patterns?

**Tier adjustments:**
- `simple`: items 8-10 score 0 don't penalize (treated as N/A)
- `complex`: items 8-10 become semi-obligatory (each 0-2 instead of 0-1)

## Step 4: Calculate score

Use weights from `$DOTFORGE_DIR/audit/scoring.md`:
1. `score_obligatory = sum(items 1-5)` — maximum 10
2. `score_recommended = sum(items 6-12)` — maximum 7
3. `score_total = score_obligatory * 0.7 + score_recommended * (3.0 / 7)` — max 7.0 + 3.0 = 10.0
4. Apply tier adjustments before calculating (see Step 1b)
4. `score_normalized = min(score_total, 10)`

**Security cap:** If item 2 (settings.json) or item 4 (block-destructive) is 0, maximum score = 6.0.

## Step 5: Generate report

Format:
```
═══ AUDIT dotforge: {{project}} ═══
Date: {{YYYY-MM-DD}}
Detected stack: {{stacks}}
Tier: {{simple|standard|complex}}
dotforge version: {{version from last bootstrap/sync if detectable}}
Score: {{X.X}}/10 {{level}}

── OBLIGATORY ──
{{✅|⚠️|❌}} CLAUDE.md ({{0-2}}) — {{detail: which sections exist/missing}}
{{✅|⚠️|❌}} settings.json ({{0-2}}) — {{detail: deny list yes/no, permissions}}
{{✅|⚠️|❌}} Rules ({{0-2}}) — {{detail: N rules, globs yes/no}}
{{✅|⚠️|❌}} Hook block-destructive ({{0-2}}) — {{detail: executable yes/no, wired yes/no}}
{{✅|⚠️|❌}} Build/test commands ({{0-2}}) — {{detail: which ones and whether they match the stack}}

── RECOMMENDED ──
{{✅|⚠️}} CLAUDE_ERRORS.md — {{detail}}
{{✅|⚠️}} Hook lint — {{detail: executable yes/no}}
{{✅|⚠️}} Custom commands — {{detail: N commands}}
{{✅|⚠️}} Memory — {{detail}}
{{✅|⚠️}} Agents — {{detail}}
{{✅|⚠️}} .gitignore — {{detail}}
{{✅|⚠️}} Prompt injection scan — {{detail}}

── DOMAIN KNOWLEDGE ──
Role defined:     {{✓ if ## Role exists in CLAUDE.md with content | ✗ otherwise}}
Domain rules:     {{N files in .claude/rules/domain/ | "none"}}
Stale (>90 days): {{N files with last_verified older than 90 days | "none"}}
Coverage:         {{list glob patterns from domain rules → cross-reference with git log --name-only -30 to estimate % of recent edits covered}}

Note: Domain knowledge is informational only — does not affect the audit score.
If no domain rules exist and the project has business logic, suggest: /forge domain extract

── CRITICAL GAPS ──
1. {{what is missing}} → {{recommended action}}
2. ...

── NEXT STEP ──
Run `/forge sync` to apply the dotforge template and close the gaps.
```

## Step 6: Cross-project error promotion

If the project has `CLAUDE_ERRORS.md`, scan it for recurring patterns:
1. Read `CLAUDE_ERRORS.md` and group errors by Area column
2. If any Area has 3+ entries with similar root causes, it's a candidate for promotion
3. Check `$DOTFORGE_DIR/practices/inbox/` and `active/` for existing practices covering that pattern
4. If no existing practice covers it, create a new practice in `practices/inbox/` using the capture format:
   - `source_type: cross-project`
   - `tags: [error-promotion, <area>]`
   - Description: the recurring pattern and derived rule
5. Report promotions in the audit output under `── ERROR PATTERNS ──`

This closes the Memory → Learning synergy: recurring project errors feed the practices pipeline.

## Step 7: Audit gaps as practices

For each obligatory item scored 0 or 1, and each recommended item scored 0:
1. Check if a practice already exists in `practices/inbox/` or `active/` for that gap
2. If not, create a practice in `practices/inbox/`:
   - `source_type: audit-gap`
   - `tags: [audit-gap, <item-name>]`
   - Description: what's missing and recommended fix
3. Only create practices for gaps that reflect a template/stack issue (not project-specific misconfigurations)
4. Report in audit output under `── CAPTURED GAPS ──`

This closes the Audit → Learning synergy: detected gaps feed back into the practices pipeline.

## Step 8: Update registry

If `$DOTFORGE_DIR/registry/projects.yml` exists, update the project entry:
- `score:` with the calculated score
- `last_audit:` with the current date
- `dotforge_version:` with the VERSION version if the project was bootstrapped
- `last_sync:` preserve the existing value (do not modify here)
- `notes:` brief summary of the audit
- `history:` append a new entry `{date: YYYY-MM-DD, score: X.X, version: <dotforge_version>}`. Never overwrite previous entries — this enables score trending over time.
