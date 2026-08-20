---
name: ghm-self-install
description: >
  Install the PRD-Driven Context Engineering methodology into a fresh OR existing
  repository — the subscription-native alternative to forking the whole repo. Runs an
  interactive wizard that seeds the framework (.claude/ hooks, skills, agents, rules,
  scripts) without clobbering product content. Triggers on "install the methodology",
  "adopt this into my repo", "self-install", "set up PRD lifecycle here", "onboard
  existing project". Outputs an installed framework + a verification report.
disable-model-invocation: true
context: fork
execution_modes:
  default: standard
  supports: [quick, standard, deep]
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Self-Install

Install the methodology into a target repo from the **install manifest**, the way
Xantham's blueprint installs from markdown: the agent runtime *is* the installer, so
the whole thing runs inside your Claude Code subscription — no API key, no metered
calls, no service to stand up.

> **Two paths, one manifest.** This skill is the interactive path. `install.sh` is the
> deterministic CLI path. Both read `.claude/install-manifest.yaml`, so they can't drift.
> Prefer driving `install.sh` from this skill; fall back to manual copies only when the
> script isn't reachable.

## Consumes

- `.claude/install-manifest.yaml` — authoritative `framework` / `template_seed` /
  `never_touch` lists (the keystone; never hardcode file lists).
- `install.sh` — the deterministic installer this skill normally drives.
- Safety rules from `ghm-template-sync` Phase "Safety Rules" — never overwrite
  `MEMORY.md`, `SoT/*`, `PRD.md`, `README.md` content.

## Produces

- An installed framework in the target repo (no new SoT IDs — this skill *places* the
  engine, it doesn't author specs).
- A verification report (hooks emit valid JSON; `readiness.py` runs).

## Workflow

### Phase 1 — Preflight & mode detect
1. Confirm `git`, `python3`, `awk` are present; warn if the target isn't a git repo.
2. Detect mode: **greenfield** (no `.claude/`) vs **brownfield** (existing `.claude/`).
   Brownfield means *merge, never overwrite product*.
3. State the trade explicitly: this installs files only — it costs subscription tokens
   for the wizard turn, **zero API**.

### Phase 2 — Wizard questions
Ask only what changes the outcome (honor the execution mode's budget):
- **Target directory** (default: current repo).
- **Domain profile**: `product` (default) · `library` · `infrastructure` · `research`.
- **Subset** `[standard+]`: keep all 4 agents + all skills (default), or trim to a role
  subset. Quick mode skips this and installs everything.

### Phase 3 — Install (drive `install.sh`)
Run the deterministic installer so behavior matches the CLI path exactly:
```bash
bash install.sh --target <DIR> --profile <PROFILE>        # add --dry-run to preview
```
- Show the `--dry-run` plan first `[standard+]`, then execute.
- If a framework file shows **drift**, surface the diff and only re-run with `--force`
  after the user confirms (mirrors `ghm-template-sync` "show diff before destructive").
- Never write anything in the manifest's `never_touch` list.

### Phase 4 — Verify (trust-but-verify, the Xantham `verify-blueprint.sh` analog)
1. Run each `.claude/hooks/*.sh` in the target; assert valid JSON on stdout.
2. Run `python scripts/readiness.py run` — a non-zero exit on an empty scaffold is the
   **expected BLOCK gate** (no content yet), not a failure. Report the score.
3. Print next steps: customize `README.md` + `PRD.md`, then "Let's frame the problem".

## Anti-patterns

| Pattern | Fix |
|---------|-----|
| Hardcoding the file list in the skill | Read `.claude/install-manifest.yaml` |
| Overwriting a brownfield repo's `PRD.md`/`SoT` | Honor `never_touch`; seed templates once |
| Treating readiness BLOCK on a fresh scaffold as a bug | It's the gate working — report the score |
| Re-implementing copy logic instead of driving `install.sh` | One code path = no drift |
