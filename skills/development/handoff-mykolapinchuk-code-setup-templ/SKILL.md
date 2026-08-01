---
name: handoff-mykolapinchuk-code-setup-templ
description: 'Prepare handoff: update HANDOFF/REPO_MAP, rotate logs, update .gitignore
  if needed, and create a safe handoff git commit.'
---

---
name: handoff
description: Prepare handoff: update HANDOFF/REPO_MAP, rotate logs, update .gitignore if needed, and create a safe handoff git commit.
---

This is the repo-local handoff skill. It intentionally avoids hyphens in the skill name so it can be invoked as `$handoff`.

When invoked, do this in order.

A) Documentation and state (must do)
1) Update `HANDOFF.md`:
   - Fill/refresh every section.
   - Include concrete evidence: file paths, artifact paths, and (if a commit is created) the commit hash.
   - If anything is broken/uncertain, list it under "Known issues / current breakage" with a minimal repro command if possible.

2) Update `REPO_MAP.md` only if needed:
   - new important file/dir/entrypoint created
   - important file moved/renamed
   - canonical commands/entrypoints changed
   - focus area ("hot paths") changed

3) Ensure `.gitignore` is updated so that:
   - large datasets and bulky artifacts are ignored
   - secret-like files are ignored (e.g., `.env`, `*.pem`, `*.key`)
   - If unsure what to ignore, stop and report rather than guessing.

4) Ensure README "For agents" section still points to the right files.

B) Log rotation (must do)
1) Determine next log filename:
   - `agent_logs/YYYY-MM-DD_agentNN.md`, where NN is 01, 02, ... chosen as the next unused number for today.
2) Move `agent_logs/current.md` -> that filename.
3) Append a one-line entry to `agent_logs/INDEX.md`:
   - `- YYYY-MM-DD_agentNN.md — <short summary> (optional: commit <hash>)`
4) Create a fresh `agent_logs/current.md` using the standard template.

C) Safe handoff commit (must do, unless safety checks fail)
Constraints:
- You may commit to the current branch (e.g., `dev`) for checkpoints and handoff.
- You must NOT run: `git push`, `git commit --amend`, `git rebase`, `git reset --hard`, `git clean -fdx`, or modify git remotes.

Before committing, always run and show output:
- `git status`
- `git diff --stat`

Safety checks:
1) Secrets check (blockers):
   - Never stage/commit: `.env`, `*.pem`, `*.key`, `id_rsa`, `id_ed25519`, credentials files, or anything that looks like a key/token.
   - If unsure, stop and report.

2) Large file check (blockers):
   - Never commit large datasets or large artifacts unless explicitly instructed.
   - If there are newly added files, check sizes and stop/report if any look like dataset/artifact payloads.

Staging approach:
- Prefer staging only source/docs/config files.
- Do not stage data or bulky artifact directories.
- If the diff includes suspicious paths, stop and report.

Commit message:
- `handoff: <short description> [<agent number>]`

After committing:
- Show `git status` again.
- Ensure either:
  - status is clean, OR
  - list the remaining uncommitted files and the reason in `HANDOFF.md`.

D) Final reporting (must do)
- Print:
  - what you updated (`HANDOFF.md`, `REPO_MAP.md`, `.gitignore` if changed)
  - log filename created
  - commit hash (if committed) or explicit reason why commit was not created
