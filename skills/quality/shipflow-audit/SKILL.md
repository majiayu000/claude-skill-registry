---
name: shipflow-audit
description: Master audit — launches all 8 domain audits (code, design, copy, seo, gtm, translate, deps, perf) in parallel agents. Works on a single file or the full project.
disable-model-invocation: true
argument-hint: [file-path | "global"] (omit for full project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -50 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Project structure: !`find src -maxdepth 2 -type d 2>/dev/null | grep -v node_modules | head -20 || echo "no src dir"`
- i18n present: !`find src -path "*/i18n/*" -o -path "*/locales/*" 2>/dev/null | head -3 || echo "no i18n"`
- Package.json scripts: !`cat package.json 2>/dev/null | grep -E '^\s+"(dev|build|lint|typecheck|check)"' || echo "no package.json"`

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: full audit of ALL projects across ALL applicable domains.
- **`$ARGUMENTS` is a file path** → FILE MODE: audit that single file across all domains.
- **`$ARGUMENTS` is empty** → PROJECT MODE: full audit of the entire project.

---

## GLOBAL MODE

Full audit of ALL projects across ALL applicable domains — the most comprehensive audit.

### Step 1: Build the audit plan

Read `/home/claude/shipflow_data/PROJECTS.md`. Use the **Domain Applicability** table to determine which domains apply to each project.

### Step 2: Let the user choose

Use **AskUserQuestion** with TWO questions in a single call:

- **Q1** — "Which projects should I audit?"
  - `multiSelect: true`
  - One option per project: label = project name, description = stack from PROJECTS.md
  - All projects pre-listed

- **Q2** — "Which domains should I run?"
  - `multiSelect: true`
  - Options: Code, Design, Copy, SEO, GTM, Translate, Deps, Perf
  - Description for each: one-line summary of what it checks

Only launch (project × domain) pairs where: user selected the project AND user selected the domain AND the domain applies to that project per PROJECTS.md.

### Step 3: Read domain checklists

Read each selected domain skill to get their PROJECT MODE checklists:
- `/home/claude/dotfiles/claude/skills/shipflow-audit-code/SKILL.md`
- `/home/claude/dotfiles/claude/skills/shipflow-audit-design/SKILL.md`
- `/home/claude/dotfiles/claude/skills/shipflow-audit-copy/SKILL.md`
- `/home/claude/dotfiles/claude/skills/shipflow-audit-seo/SKILL.md`
- `/home/claude/dotfiles/claude/skills/shipflow-audit-gtm/SKILL.md`
- `/home/claude/dotfiles/claude/skills/shipflow-audit-translate/SKILL.md`
- `/home/claude/dotfiles/claude/skills/shipflow-deps/SKILL.md`
- `/home/claude/dotfiles/claude/skills/shipflow-perf/SKILL.md`

### Step 4: Launch ALL agents

Use the **Task tool** to launch one agent per **(project × domain)** pair — ALL IN A SINGLE MESSAGE for maximum parallelism.

Example: if 9 projects need Design audit and 5 need GTM, that's 14 agents for those two domains. Launch everything at once.

Each agent: `subagent_type: "general-purpose"`. Each agent prompt MUST include:
1. `cd [project-path]` then read the project's `CLAUDE.md`
2. The complete **PROJECT MODE** section from the corresponding domain skill
3. The **Tracking** section from that domain skill
4. Rule: **read-only analysis** — no code fixes, only update AUDIT_LOG.md and TASKS.md

### Step 5: Cross-project master report

Once all agents complete:

```
══════════════════════════════════════════════════════
GLOBAL MASTER AUDIT — [date]
══════════════════════════════════════════════════════

PROJECT × DOMAIN MATRIX
              Code  Design  Copy  SEO  GTM  Trans  Deps  Perf  Overall
my-robots      [B]    —      —     —    —     —    [A]   [B]    [B]
tubeflow       [A]   [B]    [B]   [C]  [B]   —    [B]   [B]    [B]
GoCharbon      [B]   [A]    [B]   [B]  [C]   —    [A]   [A]    [B]
...

──────────────────────────────────────────────────────
CROSS-PROJECT PATTERNS
  [Systemic issues across multiple projects]

ALL ISSUES BY SEVERITY
  🔴 [project] [domain] file:line — description
  🟠 [project] [domain] file:line — description
  🟡 [project] [domain] file:line — description

Total: X critical, Y high, Z medium
       across N projects and M domain audits (up to 8 domains)
══════════════════════════════════════════════════════
```

### Step 6: Update global tracking

1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`** — one row per project with all domain scores.
2. **Master `/home/claude/shipflow_data/TASKS.md`** — update each project's audit subsections.

### Step 7: Ask about fixes

> **Global audit complete across N projects. X critical, Y high, Z medium issues total. Which projects should I fix?**

List projects ranked by overall score (worst first). Fix approved projects one at a time, domain by domain.

---

## Your task

You are the **audit orchestrator**. You do NOT perform the audits yourself. You launch **parallel agents** and then consolidate results.

### Step 0: Workspace root detection

If the current directory has no project markers (no `package.json`, no `requirements.txt`, no `src/` dir, no `lib.sh`) BUT contains multiple project subdirectories — you are at the **workspace root**, not inside a project.

Use **AskUserQuestion**:
- Question: "You're at the workspace root. Which project(s) should I audit?"
- `multiSelect: true`
- Options:
  - **All projects** — "Run global audit across every project" (Recommended)
  - One option per project from `/home/claude/shipflow_data/PROJECTS.md`: label = project name, description = stack

Then proceed to **GLOBAL MODE** with the selected projects (or all if "All projects" was chosen).

### Step 1: Determine scope and applicable domains

Detect which domains apply to this project:

- **Code** — always applicable
- **Design** — if the project has a UI (web or mobile)
- **Copy** — if the project has user-facing content
- **SEO** — if it's a web project with public pages
- **GTM** — only if commercial intent (pricing, signup, analytics)
- **Translate** — only if multiple locales (i18n files, locale dirs, bilingual content)
- **Deps** — always applicable (except projects with no package manager, e.g., BuildFlowz)
- **Perf** — always applicable

Then use **AskUserQuestion** to let the user confirm:
- Question: "Which domains should I audit for this project?"
- `multiSelect: true`
- List all 8 domains as options. For each: label = domain name, description = what it checks
- Mark inapplicable domains with "(not detected)" in the description so the user can still opt in

Only launch agents for selected domains.

### Step 2: Launch parallel agents

Use the **Task tool** to launch one agent per domain, ALL IN A SINGLE MESSAGE (parallel execution). Each agent should be `subagent_type: "general-purpose"`.

For each agent, provide this prompt structure:

```
You are performing a [DOMAIN] audit of [scope: file path OR full project] in the project at [current directory].

[Paste the FULL audit checklist for that domain from the corresponding skill — PAGE MODE section if file argument given, PROJECT MODE section if no argument]

Project CLAUDE.md context:
[Include the CLAUDE.md content from this skill's context]

IMPORTANT:
- Do NOT fix anything. This is a READ-ONLY analysis pass.
- Score every category A/B/C/D.
- For each issue found, note: file path, line number, what's wrong, severity (critical/high/medium/low), and your proposed fix.
- End with the full report table as specified in the checklist.
```

**Critical rules for agent prompts:**
- Copy the FULL checklist from the corresponding audit skill — don't summarize or skip sections.
- Agents must NOT edit files — analysis only. Fixes happen in Step 4.
- Include the project CLAUDE.md so agents understand project conventions.

### Step 3: Consolidate reports

Once all agents return, compile a **master report**:

```
══════════════════════════════════════════════════════
MASTER AUDIT: [project name or file name]
══════════════════════════════════════════════════════

DOMAIN SCORES
  Code           [A/B/C/D]  —  one-line summary
  Design         [A/B/C/D]  —  one-line summary
  Copy           [A/B/C/D]  —  one-line summary
  SEO            [A/B/C/D]  —  one-line summary
  GTM            [A/B/C/D]  —  one-line summary  (or "skipped — [reason]")
  Translate      [A/B/C/D]  —  one-line summary  (or "skipped — [reason]")
  Deps           [A/B/C/D]  —  one-line summary  (or "skipped — no package manager")
  Perf           [A/B/C/D]  —  one-line summary

OVERALL          [A/B/C/D]

──────────────────────────────────────────────────────
CRITICAL ISSUES (fix immediately)
  1. [domain] file:line — description
  2. ...

HIGH ISSUES (fix soon)
  1. [domain] file:line — description
  2. ...

MEDIUM ISSUES (improve when possible)
  1. [domain] file:line — description
  2. ...
──────────────────────────────────────────────────────
Total issues: X critical, Y high, Z medium
══════════════════════════════════════════════════════
```

Then print each domain's full detailed report below the master summary.

### Step 4: Log the audit

Update **two** audit logs. Never delete previous rows — this is the history.

**1. Global `/home/claude/shipflow_data/AUDIT_LOG.md`** — cross-project dashboard:

```markdown
# Audit Log

> Quick view of all audit runs across all projects. See project-local `AUDIT_LOG.md` for details.

| Date       | Project          | Scope        | Code | Design | Copy | SEO | GTM | Translate | Deps | Perf | Overall | Issues     |
|------------|------------------|--------------|------|--------|------|-----|-----|-----------|------|------|---------|------------|
| 2026-02-21 | plaisirsurprise  | full project | B    | C      | B    | D   | B   | C         | B    | B    | C       | 3/8/12     |
| 2026-02-21 | GoCharbon        | full project | A    | B      | B    | C   | —   | B         | A    | A    | B       | 0/3/7      |
| 2026-03-05 | plaisirsurprise  | index.astro  | A    | B      | B    | B   | B   | B         | —    | B    | B       | 0/2/4      |
```

**2. Project-local `./AUDIT_LOG.md`** — same format but only for this project (no Project column):

```markdown
# Audit Log — [project name]

| Date       | Scope        | Code | Design | Copy | SEO | GTM | Translate | Deps | Perf | Overall | Issues     |
|------------|--------------|------|--------|------|-----|-----|-----------|------|------|---------|------------|
| 2026-02-21 | full project | B    | C      | B    | D   | B   | C         | B    | B    | C       | 3/8/12     |
```

- Issues column format: `critical/high/medium`.
- Use `—` for skipped domains.
- Append a new row per run. This is an append-only log.

### Step 5: Update TASKS.md

Add audit findings as tasks. Two files to update:

**1. Project-local TASKS.md** (e.g., `./TASKS.md` in the current project):
- Create it if it doesn't exist.
- Add an `## Audit Findings` section (or update it if it already exists — replace old findings with fresh ones).
- List all issues (critical, high, and medium) as tasks:

```markdown
## Audit Findings
> Last audit: 2026-02-21 — Overall: [C]

| Pri | Task | Domain | Status |
|-----|------|--------|--------|
| 🔴 | Fix XSS in user comment rendering (src/components/Comments.tsx:42) | Code | 📋 todo |
| 🔴 | Add missing meta descriptions on 8 pages | SEO | 📋 todo |
| 🟠 | Standardize button styles across 12 components | Design | 📋 todo |
| 🟠 | Rewrite homepage headline — benefit-driven | Copy | 📋 todo |
| 🟡 | Add alt text to 5 decorative images | SEO | 📋 todo |
| 🟡 | French typographic spaces before colons | Translate | 📋 todo |
```

- Use 🔴 for critical, 🟠 for high, 🟡 for medium.
- If a previous `## Audit Findings` section exists, replace it entirely with fresh findings (don't accumulate stale issues).

**2. Master `/home/claude/shipflow_data/TASKS.md`**:
- Find the section for the current project.
- Add or update an `### Audit` subsection with a summary line and all issues as tasks.
- Update the Dashboard table's "Top Priority" column if audit found critical issues (they take precedence).

### Step 6: Apply fixes

After presenting the consolidated report and updating tracking files, ask the user:

> **Found X critical, Y high, Z medium issues. How do you want to proceed?**
> 1. Fix all (critical + high + medium)
> 2. Fix critical and high only
> 3. Fix critical only
> 4. Don't fix anything — just keep the report

Then apply fixes sequentially (NOT in parallel — fixes may touch the same files). Priority order:
1. Critical security issues
2. Critical bugs
3. High severity across all domains
4. Medium severity across all domains

When fixing, group changes by file to avoid conflicts. If two domains flag the same file, apply all fixes to that file at once.

### Important

- The value of this skill is PARALLELISM. Always launch agents in a single message so they run concurrently. Never run them one by one.
- Keep agent prompts self-contained — each agent should work independently without needing context from other agents.
- If a domain agent fails or times out, report it and continue with the others.
- Don't re-audit what agents already audited. Trust their analysis, consolidate, and fix.
- For FILE MODE: some domain checklists may partially apply (e.g., GTM checks don't make sense for a utility function). Agents should skip irrelevant checks and note "N/A" in their report.
