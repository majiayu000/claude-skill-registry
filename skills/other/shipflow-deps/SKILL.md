---
name: shipflow-deps
description: Deep dependency audit — vulnerabilities, outdated packages, unused deps, license compliance, type definitions, configuration health
disable-model-invocation: true
argument-hint: ["global"] (omit for current project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -120 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Package.json: !`cat package.json 2>/dev/null | head -80 || echo "no package.json"`
- Dependencies: !`cat package.json 2>/dev/null | grep -E '"(dependencies|devDependencies)"' -A 100 | head -80 || pip list 2>/dev/null | head -40 || echo "unknown"`
- Lockfile: !`ls -1 package-lock.json yarn.lock pnpm-lock.yaml requirements.txt Pipfile.lock 2>/dev/null | head -3 || echo "none"`
- Node/Python version: !`node -v 2>/dev/null; python3 --version 2>/dev/null; cat .nvmrc .python-version .node-version 2>/dev/null || echo "not pinned"`
- Security config: !`ls -1 .github/dependabot.yml renovate.json .npmrc 2>/dev/null || echo "none"`
- Project structure: !`find . -maxdepth 2 -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.astro" -o -name "*.vue" -o -name "*.py" -o -name "*.sh" \) 2>/dev/null | grep -v node_modules | grep -v .git | grep -v dist | sort | head -40`

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: audit dependencies across ALL projects.
- **`$ARGUMENTS` is empty** → PROJECT MODE: full dependency audit of the current project.
- **No FILE MODE** — dependencies are project-scoped, not file-scoped.

---

## GLOBAL MODE

Audit dependencies across ALL projects in the workspace.

1. Read `/home/claude/shipflow_data/PROJECTS.md` — check the **Domain Applicability** table. Identify projects with ✓ in the Deps column. BuildFlowz (Bash) has no package manager → skip.

2. Use **AskUserQuestion** to let the user choose:
   - Question: "Which projects should I audit for dependency health?"
   - `multiSelect: true`
   - One option per applicable project: label = project name, description = stack from PROJECTS.md
   - All projects with package managers pre-listed

3. Use the **Task tool** to launch one agent per **selected** project — ALL IN A SINGLE MESSAGE (parallel). Each agent: `subagent_type: "general-purpose"`.

   Agent prompt must include:
   - `cd [path]` then read `CLAUDE.md` for project context
   - The complete **PROJECT MODE** section from this skill (all 8 phases)
   - The **Tracking** section from this skill

4. After all agents return, compile a **cross-project dependency report**:

   ```
   GLOBAL DEPENDENCY AUDIT — [date]
   ═══════════════════════════════════════
   PROJECT SCORES
     [project]    [A/B/C/D]  —  summary
     ...
   CROSS-PROJECT PATTERNS
     [Shared vulnerabilities, duplicate libraries across projects, version inconsistencies]
   ALL ISSUES BY SEVERITY
     🔴 [project] — description
     🟠 [project] — description
     🟡 [project] — description
   Total: X critical, Y high, Z medium across N projects
   ═══════════════════════════════════════
   ```

5. Update `/home/claude/shipflow_data/AUDIT_LOG.md` (one row per project, Deps column) and `/home/claude/shipflow_data/TASKS.md` (each project's `### Audit: Deps` subsection).

6. Ask: **"Which projects should I fix?"** — list projects with scores. Fix only approved projects, one at a time.

---

## PROJECT MODE

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `requirements.txt`, no `src/` dir, no `lib.sh`) BUT contains multiple project subdirectories — you are at the **workspace root**, not inside a project.

Use **AskUserQuestion**:
- Question: "You're at the workspace root. Which project(s) should I audit for dependency health?"
- `multiSelect: true`
- Options:
  - **All projects** — "Run dependency audit across every project with a package manager" (Recommended)
  - One option per project from `/home/claude/shipflow_data/PROJECTS.md`: label = project name, description = stack

Then proceed to **GLOBAL MODE** with the selected projects.

### PHASE 1: VULNERABILITY SCAN

Run the appropriate security audit tool:

**Node.js**: `npm audit` / `yarn audit` / `pnpm audit` (match the lockfile)
**Python**: `pip-audit` if available, or `safety check`, or `pip install pip-audit && pip-audit`

For each vulnerability found:
- [ ] CVE ID and severity (critical/high/medium/low)
- [ ] Affected package and version range
- [ ] Fix available? (patch version, or requires major upgrade)
- [ ] Transitive or direct dependency?

**Supply chain checks**:
- [ ] Lockfile committed to git (`git ls-files --error-unmatch [lockfile]`)
- [ ] No unusual registry URLs in `.npmrc` or lockfile
- [ ] No `postinstall` scripts in dependencies doing suspicious things (`grep -r postinstall node_modules/*/package.json | head -20`)
- [ ] Provenance/integrity checksums present in lockfile

---

### PHASE 2: OUTDATED PACKAGES

Run the appropriate outdated check:

**Node.js**: `npm outdated` / `yarn outdated` / `pnpm outdated`
**Python**: `pip list --outdated`

Classify each outdated package:
- **Patch** (1.2.3 → 1.2.4) — safe to update, bug fixes only
- **Minor** (1.2.3 → 1.3.0) — usually safe, new features
- **Major** (1.2.3 → 2.0.0) — breaking changes, needs migration

Additional checks:
- [ ] Deprecation timeline — is the package abandoned? (no commits >2 years)
- [ ] Replacement recommendations for deprecated packages
- [ ] Framework version alignment (e.g., all React ecosystem on same major)

---

### PHASE 3: UNUSED & DUPLICATE

Cross-reference installed dependencies with actual usage:

- [ ] Search for each dependency name in source files (imports/requires)
- [ ] Flag packages in `dependencies` that should be in `devDependencies` (test frameworks, build tools, linters, type packages used only in dev)
- [ ] Flag packages in `devDependencies` that should be in `dependencies` (imported by production code)
- [ ] Detect functional duplicates — multiple libraries doing the same job:
  - HTTP clients (axios + fetch + got + node-fetch)
  - Date libraries (moment + dayjs + date-fns + luxon)
  - Validation (zod + yup + joi + valibot)
  - CSS-in-JS (styled-components + emotion + stitches)
  - State management (redux + zustand + jotai + recoil)

---

### PHASE 4: LICENSE COMPLIANCE

List all dependency licenses:

**Node.js**: `npx license-checker --summary 2>/dev/null || npx license-checker-rspack --summary 2>/dev/null` or parse from `node_modules/*/package.json`
**Python**: `pip-licenses 2>/dev/null` or parse from package metadata

- [ ] Flag copyleft licenses (GPL, AGPL, LGPL) — may be incompatible with commercial use
- [ ] Flag unknown or missing licenses
- [ ] Flag SSPL (Server Side Public License) — restrictive for SaaS
- [ ] Ensure project's own license is declared

---

### PHASE 5: TYPE DEFINITIONS (TypeScript only)

Skip this phase for Python or Bash projects.

- [ ] Check `@types/*` coverage — for every untyped JS dependency, is there a corresponding `@types/` package?
- [ ] Version alignment — `@types/react` version should match `react` version range
- [ ] Inline types preferred — packages shipping their own `.d.ts` don't need `@types/`
- [ ] No `@types/` packages for dependencies that already include types (wasted install)

---

### PHASE 6: CONFIGURATION HEALTH

- [ ] Runtime version pinned: `.nvmrc`, `.node-version`, or `engines` field in package.json
- [ ] Package manager version pinned: `packageManager` field in package.json, or `corepack enable`
- [ ] Security automation configured: `dependabot.yml` or `renovate.json` for auto-updates
- [ ] If dependabot/renovate exists: check it covers all package ecosystems (npm, pip, github-actions, docker)
- [ ] `.npmrc` settings appropriate (no `ignore-scripts=false`, proper registry)
- [ ] `overrides` / `resolutions` documented with reason (why is each override needed?)

---

### PHASE 7: FIX

Apply fixes in priority order. **Ask before each category** using AskUserQuestion.

1. **Critical CVEs** — apply patch-level fixes for critical/high vulnerabilities
2. **Unused dependencies** — remove them (`npm uninstall` / `pip uninstall`)
3. **Misplaced dependencies** — move between deps ↔ devDeps
4. **Missing type definitions** — install `@types/*` for untyped packages
5. **Configuration gaps** — add `.nvmrc`, `engines`, etc.
6. **Patch/minor updates** — update safe packages (patch first, then minor)

**NEVER auto-upgrade major versions.** For major version upgrades, recommend `/shipflow-migrate` instead.

---

### PHASE 8: REPORT

```
DEPENDENCY AUDIT: [project name] — [stack detected]
═══════════════════════════════════════════════════

Vulnerabilities              [A/B/C/D]
  Critical CVEs                [count]
  High CVEs                    [count]
  Supply chain risks           [count]

Currency                     [A/B/C/D]
  Patch outdated               [count]
  Minor outdated               [count]
  Major outdated               [count]
  Abandoned (>2yr)             [count]

Hygiene                      [A/B/C/D]
  Unused deps                  [count]
  Misplaced deps               [count]
  Duplicate functionality      [count]

License                      [A/B/C/D]
  Copyleft detected            [count]
  Unknown license              [count]

Configuration                [A/B/C/D]
  Runtime pinned               [yes/no]
  Package mgr pinned           [yes/no]
  Auto-update configured       [yes/no]
  Lockfile committed           [yes/no]
═══════════════════════════════════════════════════
OVERALL                      [A/B/C/D]

Fixed: X issues | Remaining: Y (major upgrades → /shipflow-migrate)
```

---

## Tracking (all modes)

After generating the report and applying fixes:

### Log the audit

Append a row to two files:

1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`**: append a row filling the Deps column, `—` for other domains.
2. **Project-local `./AUDIT_LOG.md`**: same but without the Project column.

Create either file if missing, using the table header from the master `/shipflow-audit` skill format.

### Update TASKS.md

1. **Local TASKS.md** (project root): add/replace a `### Audit: Deps` subsection with critical (🔴), high (🟠), and medium (🟡) issues.
2. **Master `/home/claude/shipflow_data/TASKS.md`**: find the project's section, add/replace a `### Audit: Deps` subsection with the same tasks.

---

## Important

- BuildFlowz (Bash/Shell) has no package manager — Deps = `—` in PROJECTS.md. Skip it.
- SocialFlowz is empty — skip it.
- Never auto-upgrade major versions. Always recommend `/shipflow-migrate` for breaking changes.
- For monorepos (tubeflow), audit all workspace package.json files.
- For Python projects, check both `requirements.txt` and `pyproject.toml`.
- If `npm audit` / `pip-audit` is not available, install it first or use alternative tools.
