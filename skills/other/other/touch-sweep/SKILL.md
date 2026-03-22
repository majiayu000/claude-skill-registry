---
name: touch-sweep
description: Finds every file and location affected by a GitHub issue change. Use when scoping an issue, finding blast radius, or answering "what does this touch". Trigger phrases - /touch-sweep, "find all affected files", "scope this issue", "what does this touch", "blast radius".
argument-hint: "#N [--dry-run]"
disable-model-invocation: true
context: fork
---

# touch-sweep

You are a blast-radius analyst for the Fenrir Ledger codebase. Your job is to take a GitHub issue, understand what it asks for, then systematically search every corner of the repository to produce a complete, actionable inventory of affected files. No fluff. No guesses. Every line must be verifiable.

## Arguments

Parse `$ARGUMENTS` to extract:
- **Issue number**: required, e.g. `#123` or `123`
- **--dry-run flag**: optional, if present print findings to console instead of updating the issue

## Workflow

Follow these steps exactly, in order.

### Step 1 — Read the issue

```bash
gh issue view <N> --json title,body,labels,number
```

Parse the issue to understand:
- What is being changed (rename, refactor, feature, bug fix, removal, migration, etc.)
- Key search terms to grep for
- The type of change determines your search strategy:
  - **Rename**: search for old name everywhere
  - **Removal**: search for all usages of the thing being removed
  - **Feature**: search for integration points
  - **Refactor**: search for all references to the module/function/pattern
  - **Migration**: search for old patterns that need updating

### Step 2 — Build search strategy

Based on the issue analysis, determine:
- **Primary search terms**: exact strings to grep for (e.g. `development/frontend`, `monitor-ui`, a function name)
- **Secondary search terms**: contextual or partial matches (e.g. `cd frontend`, regex patterns)
- **Exclusion patterns**: things to NOT match (e.g. for a "monitor" rename, exclude unrelated "monitoring" infra references)
- **File pattern filters**: relevant file extensions or path patterns

Write out your search strategy before executing it so the reasoning is clear.

### Step 3 — Systematic search

Search ALL of the following areas. Use absolute paths. For each area, report file paths and match counts. Skip areas with zero matches in the final report, but you MUST search all of them.

1. **Terraform** — `infrastructure/*.tf` and `infrastructure/**/*.tf`
2. **K8s / Helm** — `infrastructure/k8s/` manifests, deployments, services, ingress, configmaps
3. **GitHub Actions** — `.github/workflows/*.yml`
4. **Dockerfiles** — `**/Dockerfile*`, `**/docker-compose*`
5. **App source code** — `development/` source files (`.ts`, `.tsx`, `.js`, `.jsx`, `.css`)
6. **Tests** — test files, playwright configs, vitest configs
7. **Justfiles** — `**/justfile`, `**/Justfile`, `**/*.just`
8. **Package configs** — `**/package.json`, `**/tsconfig*.json`, `pnpm-workspace.yaml`, `turbo.json`
9. **CLAUDE.md and agent config** — `**/CLAUDE.md`, `.claude/agents/*.md`
10. **Skills and templates** — `.claude/skills/**/*`
11. **Scripts** — `**/*.sh`, `**/*.mjs`, standalone scripts
12. **Documentation** — `**/*.md` in `product/`, `ux/`, `security/`, `quality/`, `designs/`, `memory/`
13. **Monitoring and alerting** — `monitoring.tf`, uptime checks, alerting configs
14. **DNS / Ingress / SSL** — ingress resources, managed certs, DNS records in tf
15. **Environment and secrets** — `.env*` files, k8s secrets/configmaps references
16. **Symlinks** — check for symlinks pointing to affected paths

For each match found, record:
- Absolute file path
- Number of matches in that file
- Brief description of what is affected in that file
- Flag if it needs careful handling (not a simple find-replace, has logic dependencies, etc.)

### Step 4 — Compile findings

Organize results into a structured report grouped by area. Calculate:
- Total file count across all areas
- Per-area file list with line references
- Any external dependencies that need manual action (GCP console, DNS registrar, OAuth configs, etc.)
- Suggested order of operations if relevant (e.g. "rename directory first, then update all references")

**Area summary table:** Build a concise summary table showing each affected area, file count, and risk level at a glance. This goes at the top of the report before the detailed file listings.

**Risk assessment:** For each affected area, assign a risk level based on:

| Risk | Criteria |
|------|----------|
| `HIGH` | Changes to auth, API routes, database schema, secrets, CI/CD pipelines, infrastructure (Terraform/K8s). Breaking these can cause outages, data loss, or security issues. |
| `MEDIUM` | Changes to shared types/interfaces, package configs, build configs, test infrastructure, agent templates. Breaking these can cause build failures or cascading test failures. |
| `LOW` | Changes to documentation, skills, wireframes, cosmetic UI, comments. Breaking these has no runtime impact. |

Also assess **overall risk** based on:
- Number of high-risk areas affected
- Whether changes span multiple apps (cross-app impact)
- Whether external/manual steps are required
- Total blast radius (file count)

### Step 5 — Post sweep as a comment (or print if --dry-run)

Do NOT modify the issue body, labels, or assignees. The original issue description stays untouched.

Post the sweep results as a **comment** on the issue using `gh issue comment <N> --body-file <tempfile>`.
If `--dry-run` was passed, print the comment body to console instead.

Construct the following markdown comment body:

```
## Touch Sweep — Blast Radius Analysis

## Summary

| Area | Files | Risk |
|------|------:|------|
| <Area 1> | N | HIGH/MEDIUM/LOW |
| <Area 2> | N | HIGH/MEDIUM/LOW |
| ... | ... | ... |
| **Total** | **N** | **<overall risk>** |

## Risk Assessment

**Overall risk: HIGH/MEDIUM/LOW**

- <1-2 sentence explanation of the biggest risk factor>
- <Any cross-app or external dependency concerns>
- <Mitigation notes if applicable, e.g. "all changes are find-replace safe">

## Affected Areas

### <Area Name> (N files) — <RISK>
- `<absolute/path/to/file>` (N matches) — <what references the search term and why it matters>

... (one section per area that has matches, skip empty areas)

### External / Manual Steps
- <anything that cannot be done via code change, e.g. "Update GCP OAuth redirect URIs">

(omit this section if there are no external steps)

## Execution Plan
1. <Ordered steps for the agent to follow>
2. ...

## Acceptance Criteria
- [ ] Zero references to `<old name/pattern>` remain in repo (verified via grep)
- [ ] tsc passes
- [ ] Build passes
- [ ] Vitest passes
- [ ] <area-specific criteria>

## Stats
- **Total files affected:** N
- **Areas affected:** N
- **Sweep performed:** <current date>

---
Generated with [Claude Code](https://claude.com/claude-code) `/touch-sweep`
```

### Step 6 — Cross-app impact check (Odin's Spear)

After compiling findings, check whether the issue changes behaviour in the Ledger app
(`development/ledger/`) that could affect Odin's Spear (`development/odins-spear/`).

Odin's Spear is the admin tool that manages Ledger data. Changes to any of the following
in the Ledger are likely to require a follow-up issue for Odin's Spear:

- **API routes** (`development/ledger/src/app/api/`) — Spear calls these endpoints
- **Firestore schema / collection names** — Spear reads/writes the same collections
- **Auth / session handling** (`@/lib/auth/`) — Spear uses the same auth system
- **Shared types or interfaces** — tier names, card status values, user models
- **Environment variables** consumed by both apps
- **URL routes** that Spear links to or redirects to

**How to check:**
1. From the issue's affected files, identify any Ledger API routes, Firestore paths,
   shared types, or auth changes.
2. Grep `development/odins-spear/` for references to those same routes, types, or paths.
3. If matches are found, there is cross-app impact.

**If cross-app impact is detected**, use `AskUserQuestion` to recommend filing a follow-up:

```
Question: "This change affects Ledger behaviour that Odin's Spear depends on (<brief reason>). File a follow-up issue for Odin's Spear?"
Options:
  - "Yes, file it" — after the sweep completes, invoke /file-issue with the Spear-specific scope
  - "No, skip" — continue without filing
```

If the user says yes, file the follow-up issue via `/file-issue` with:
- Title referencing the parent issue: "Update Odin's Spear for #<N> — <short description>"
- Label: `enhancement`
- Body noting which Spear files need updating and why

**If no cross-app impact**, skip this step silently — do not mention Odin's Spear.

### Step 7 — Report back

Output a summary to the caller:

```
Swept #<N> — "<title>"
Risk: HIGH/MEDIUM/LOW | <X> files across <Y> areas

| Area | Files | Risk |
|------|------:|------|
| ... summary table ... |

Comment posted: https://github.com/declanshanaghy/fenrir-ledger/issues/<N>
```

If `--dry-run`, replace "Comment posted" with "Dry run — comment NOT posted".

## Rules

- NEVER add fluff or generic advice. Every line in the output must be actionable and verifiable.
- NEVER miss an area. The whole point of this skill is completeness. Search all 16 areas.
- Group results by area, not by file. This makes the report scannable.
- Skip areas with zero matches — do not include empty sections in the final report.
- Include external/manual steps that cannot be automated (DNS changes, OAuth console updates, etc.).
- The execution plan must be ordered logically (e.g. rename directory before updating references).
- Always include a grep verification step in acceptance criteria.
- **NEVER modify the issue body.** Sweep results go in a comment, not the issue description.
- Preserve any existing labels on the issue. Do not modify them.
- The `--dry-run` output format must be identical to the comment body format so the user can preview.
- Use absolute file paths in all output.
- Write the comment body to a temp file and use `gh issue comment <N> --body-file <tempfile>` to avoid quoting issues.
