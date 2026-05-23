---
name: localsetup-skill-sandbox-tester
description: "Test skills in an isolated sandbox before production. Run after vetting and normalization (not right after import). Creates a unique temp sandbox when the skill needs read/write; runs smoke checks; on failure uses localsetup-debug-pro to iterate until fixed; no writes to repo until user approves. Use when validating a skill after it is framework-compliant, testing a skill end-to-end, or ensuring it runs correctly on all supported platforms."
metadata:
  version: "1.0"
compatibility: "Python 3.10+ for any bundled tooling. Sandbox paths follow platform temp (Linux /tmp, macOS /tmp or $TMPDIR, Windows %TEMP%). Resolves skill paths per _localsetup/docs/PLATFORM_REGISTRY.md. Tooling must follow _localsetup/docs/TOOLING_POLICY.md and INPUT_HARDENING_STANDARD.md."
---

# Skill Sandbox Tester

**Purpose:** Validate skills in an isolated sandbox so bugs are found and fixed before promoting to production. Handles staging (unique sandbox dir, no collision), smoke runs, and ties into **localsetup-debug-pro** for the fix loop. Does not write to the repo until the user approves.

## When to use this skill

- User wants to "test this skill," "validate the skill after import," "run the skill in a sandbox," or "make sure the skill works before we use it."
- After a skill has been vetted and normalized (not right after import), user wants to run it safely in a sandbox and fix any issues before production.
- User wants to confirm a skill runs correctly on the current platform (Cursor, Claude Code, Codex, OpenClaw) without affecting the repo.

## How it actually works

**Testing:** The skill does not run a built-in test suite. You (the agent) choose a **smoke command** that should succeed if the skill is healthy: for example run the skill’s main script with `--help`, or a dry-run/list mode, or whatever the skill’s SKILL.md says to run to verify. The tooling (1) copies the skill into a unique temp directory (the sandbox), then (2) runs that one command with the sandbox as the current working directory. **Pass** = the command exits 0. **Fail** = non-zero exit or crash. So "test" here means: run the chosen command in an isolated copy and treat exit code as the result.

**Debugging:** When the smoke command fails, this skill does not implement the fix. You **load localsetup-debug-pro** and follow its 7-step protocol (reproduce, isolate, hypothesize, instrument, verify, fix, regression). The important rule: **all reproduction and edits happen in the sandbox copy only.** You run the failing command in the sandbox, inspect logs or add print/debugger, change code in the sandbox, then run the same smoke command again from the sandbox. Repeat until the smoke command exits 0. Only then do you summarize the changes and **ask the user** to approve copying those fixes from the sandbox into the real skill directory (e.g. `_localsetup/skills/<name>/`). No writes to the repo until the user says so.

**End-to-end flow:**

1. Create sandbox: copy the skill to a temp dir (e.g. via `create_sandbox.py`).
2. Run smoke: execute your chosen command in that dir (e.g. via `run_smoke.py`). Check exit code.
3. If exit 0: report "smoke passed"; done unless the user wants more checks.
4. If non-zero: load debug-pro, reproduce and fix **inside the sandbox**, re-run the same smoke command in the sandbox until it passes.
5. After it passes: summarize what you changed in the sandbox and ask the user to approve applying those changes to the real skill; only then copy back and (if needed) run deploy.

So the sandbox tester provides the **staging and run** (copy, run one command, interpret exit code); debug-pro provides the **how to fix** when that command fails. The agent ties them together by choosing the smoke command, running it, and on failure following debug-pro while keeping all edits in the sandbox.

## Design: use debug-pro in conjunction

This skill does **not** duplicate the debugging methodology. When a smoke run fails:

1. **Do not** write fixes back to the repo.
2. **Load and follow localsetup-debug-pro** for the 7-step protocol (Reproduce, Isolate, Hypothesize, Instrument, Verify, Fix, Regression Test) and for language-specific debugging (Python, Node, Swift, network, git bisect).
3. Apply fixes in the **sandbox copy** of the skill only; re-run smoke in the sandbox until it passes.
4. Only after smoke passes, present a summary and ask the user to approve writing changes back (e.g. from sandbox to `_localsetup/skills/<name>/` or the deployed path).

This keeps a single source of truth for debugging (debug-pro) and a clear separation: sandbox tester = staging + run + smoke + orchestration; debug-pro = how to fix failures.

## Supported platforms

Skill paths and context loaders are defined in _localsetup/docs/PLATFORM_REGISTRY.md. The sandbox tester works on all supported platforms:

| Platform | Skills path (canonical or deployed) |
|----------|-------------------------------------|
| Framework source | _localsetup/skills/localsetup-*/ |
| Cursor | .cursor/skills/localsetup-*/ |
| Claude Code | .claude/skills/localsetup-*/ |
| Codex | .agents/skills/localsetup-*/ |
| OpenClaw | skills/localsetup-*/ (repo root) |

Resolve the skill directory from the current context: if working in the framework repo, use `_localsetup/skills/<name>/`; if the user refers to a deployed path, use the platform's skills path from PLATFORM_REGISTRY. Test using the same platform the user is on so behavior matches production.

## Tooling

Python 3.10+ scripts under `scripts/` (per TOOLING_POLICY and INPUT_HARDENING_STANDARD). Run from repo root or from the skill directory; paths below are relative to the skill (e.g. `_localsetup/skills/localsetup-skill-sandbox-tester/` or deployed equivalent).

| Script | Purpose |
|--------|---------|
| `scripts/create_sandbox.py` | Create a unique temp directory with a full copy of the skill. Prints the skill copy path (use as `--sandbox-dir` for run_smoke). |
| `scripts/run_smoke.py` | Run a single command with cwd set to the sandbox (skill copy). Exit code matches the command; use for smoke checks (e.g. `--command "python scripts/pr_review.py --help"`). |

**Quick start (by name):**

```bash
SANDBOX=$(python3 _localsetup/skills/localsetup-skill-sandbox-tester/scripts/create_sandbox.py --skill-name localsetup-pr-reviewer)
python3 _localsetup/skills/localsetup-skill-sandbox-tester/scripts/run_smoke.py --sandbox-dir "$SANDBOX" --command "python scripts/pr_review.py --help"
```

**By path:**

```bash
SANDBOX=$(python3 _localsetup/skills/localsetup-skill-sandbox-tester/scripts/create_sandbox.py --skill-path _localsetup/skills/localsetup-pr-reviewer)
python3 _localsetup/skills/localsetup-skill-sandbox-tester/scripts/run_smoke.py --sandbox-dir "$SANDBOX" --command "python scripts/pr_review.py --help"
```

Smoke passes if the command exits 0. On non-zero, use localsetup-debug-pro in the sandbox; do not write to the repo until the user approves.

## Workflow (agent steps)

### 1. Identify skill and sandbox need

- **Input:** Skill name (e.g. `localsetup-pr-reviewer`) or path. Resolve to the skill directory per platform (see above).
- **Read/write need:** If the skill has no scripts or side effects (e.g. doc-only), you can run a lightweight check (e.g. parse SKILL.md, check frontmatter). If the skill has `scripts/` or clearly writes output (state files, reports), treat it as needing a sandbox.
- **Sandbox only when needed:** Create an isolated environment only when the skill will read/write; otherwise a quick validation may suffice without a full sandbox.

### 2. Create unique sandbox (when needed)

- **Location:** Use platform-appropriate temp: Linux `/tmp`; macOS `/tmp` or `$TMPDIR`; Windows `%TEMP%` or `%TMP%`. See localsetup-safety-and-backup for temp file policy.
- **Naming:** Unique dir to avoid collision, e.g. `skill-sandbox-<skill-name>-<timestamp>` or `mktemp -d` (Bash) / `tempfile.mkdtemp` (Python). Example: `/tmp/skill-sandbox-localsetup-pr-reviewer-20260220-120000`.
- **Contents:** Copy the skill directory into the sandbox (do not symlink into the repo, so all writes stay in the sandbox). Optionally set env (e.g. `PR_REVIEW_STATE`, `PR_REVIEW_OUTDIR`) to point inside the sandbox so any state or reports go there.
- **Cleanup:** Remove the sandbox when the test session is done, or leave it for inspection when the user wants to debug; document the path.

### 3. Run smoke

- **Entrypoints:** Run the skill's main entrypoints (e.g. from SKILL.md "Quick Start" or "Usage"): run scripts with minimal safe arguments (e.g. `--help`, or a dry-run/list mode if the skill has one). Prefer invoking the framework tooling (Python scripts) from the sandbox copy so behavior matches production.
- **Smoke criteria:** Exit code 0 for success paths; no writes outside the sandbox; expected stdout/stderr shape (e.g. no tracebacks, or expected error message for known failure cases). If the skill documents "run X to verify," run that.
- **Platform:** Run in the same environment the user is on (same OS, same interpreter) so results are valid for that platform.

### 4. On success

- Report that the skill passed smoke and is ready for production use. Optionally suggest one more check (e.g. run one real scenario with user approval). Do not write to the repo unless the user asks to promote or commit.

### 5. On failure (debug loop)

- **Do not write to the repo.** All fixes happen in the sandbox copy.
- **Load localsetup-debug-pro** and follow its 7-step protocol and language-specific commands. Reproduce in the sandbox, isolate, hypothesize, instrument, verify, fix in sandbox, then re-run smoke in the sandbox.
- **Iterate** until smoke passes. If the user wants to bring in other skills (e.g. localsetup-receiving-code-review for review of the fix), use them in the loop.
- **After smoke passes:** Summarize changes made in the sandbox. Ask the user to approve applying those changes to the real skill location (e.g. copy fixed files from sandbox to `_localsetup/skills/<name>/`). Only then write to the repo; then run deploy if needed so the platform gets the updated skill.

## Framework standards

- **Tooling:** Any script added to this skill (e.g. a Python helper to create sandbox and run smoke) must be Python 3.10+, per _localsetup/docs/TOOLING_POLICY.md. Shell/PowerShell only for minimal platform entrypoints if required.
- **Input hardening:** Any tool that takes paths, skill names, or env must follow _localsetup/docs/INPUT_HARDENING_STANDARD.md: sanitize input, validate paths and bounds, emit actionable stderr, no silent failure.
- **Documentation:** Keep this SKILL.md and any references in sync with PLATFORM_REGISTRY and the framework docs index.

## Related skills

| Skill | Role |
|-------|------|
| **localsetup-debug-pro** | Use when smoke fails: 7-step protocol and language-specific debugging. Fix in sandbox; do not duplicate its content here. |
| **localsetup-safety-and-backup** | Temp file policy (/tmp, mktemp, cleanup); use for sandbox location and cleanup. |
| **localsetup-skill-vetter** | Security check before normalization; run after import. |
| **localsetup-skill-normalizer** | Run after vetting. Brings the skill to framework compliance (doc/spec, platform-neutral, tooling). **Run sandbox tester only after normalization is done.** Running it sooner is unsafe: the skill may not comply yet and failures will be noisy and misleading. |
| **localsetup-skill-importer** | Brings the skill in; then vet and normalize. Do not run sandbox tester right after import. |
| **localsetup-skill-creator** | New skills can be tested with this skill after they are normalized and ready. |
| **localsetup-framework-compliance** | If changes are written back to the framework, follow checkpoints and testing after modifications. |

## Reference

- _localsetup/docs/PLATFORM_REGISTRY.md – Supported platforms and skills paths.
- _localsetup/docs/TOOLING_POLICY.md – Python-first tooling, runtime target.
- _localsetup/docs/INPUT_HARDENING_STANDARD.md – Mandatory input handling for any script.
- _localsetup/docs/SKILLS_AND_RULES.md – How skills are loaded and where they live per platform.
