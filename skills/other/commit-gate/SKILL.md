---
name: commit-gate
description: The only path to a commit. Routed to when the user invokes /commit or otherwise instructs codeArbiter to persist staged changes. Nine gated phases — permission, branch, classification, verification (test/lint/secrets), behavioral proof, diff review, selective stage, message, commit. Nothing reaches version control without clearing every gate; "it looks good" is not authorization.
---

# commit-gate

The only permitted path to a commit. Bypassing it is a hard-rule violation. Routed to when the user invokes `/commit` or any equivalent instruction to persist staged changes.

## Pre-flight

Read these, or STOP and surface the gap — never guess a command:

- `${CLAUDE_PROJECT_DIR}/.codearbiter/tech-stack.md` — test, lint, and secrets-scan invocations. Stop if missing; do not guess.
- A git repository must be present and `git status` available.
- The `tdd` skill must have cleared all six phases for any new or modified feature code in the staged set. If `tdd` is incomplete, STOP and surface the gap.

## Phase 1 — Permission · gate: BLOCK

Confirm the user explicitly authorized this commit. Speculative commits are prohibited.

Explicit instructions: "commit", "commit this", "go ahead and commit", "create the commit". Ambiguous signals — "looks good", "that should work" — are NOT authorization. Record the instruction text for the report.

Gate: explicit user authorization is on record. Inferred or assumed permission does not pass.

## Phase 2 — Branch · gate: BLOCK

Run `git branch --show-current`. If the branch is `main`, `master`, or any protected branch, STOP and instruct the user to create a feature branch. Record the branch name for the report.

Gate: the working branch is not protected.

## Phase 3 — Classification · gate: BLOCK

Read the staged set (`git diff --cached --name-only` and `--stat`). Classify the change into a commit type:

- `feat` — new capability or behavior
- `fix` — corrects a defect
- `test` — tests only
- `refactor` — restructures without behavior change
- `docs` — documentation only
- `chore` — build, tooling, dependency updates
- `ci` — pipeline changes

Derive the scope from the staged paths. If the staged set spans more than one type, split it — stage and commit each type separately.

Flag any staged **database migration** (per `_hooklib.is_migration_path`) here — it carries a mandatory migration-review routing in Phase 4 (the H-14 gate), independent of the commit type.

Gate: the staged set is type-homogeneous with a single type and scope.

## Phase 4 — Verification · gate: BLOCK

Read the test, lint, and secrets-scan commands from `tech-stack.md`. Then:

- Run the test command. ALL tests green. Any failure blocks.
- Run lint, and the type-check if the project is statically typed. Zero errors.
- Run the secrets scan on ALL staged files, regardless of commit type. Any finding blocks.
- **Security gates (mandatory routing):** if the staged diff touches crypto/TLS or secret patterns, route it through `crypto-compliance` and/or `secret-handling` (`${CLAUDE_PLUGIN_ROOT}/skills/`) — they scan against `security-controls.md` and, on pass, record the diff-bound marker `.codearbiter/.markers/security-gate-passed` (via `hooks/security-pass.py`). This is not optional: the PreToolUse commit hook **H-09b/H-10b blocks the commit** until that gate pass is recorded AND covers every sensitive line being committed.
- **Migration gate (mandatory routing):** if the staged set contains a database migration (Phase 3 flags it; the detection rule is `_hooklib.is_migration_path` — default migration globs, extendable/narrowable via a `migration-paths` block in `security-controls.md`), dispatch the `migration-reviewer` agent (`${CLAUDE_PLUGIN_ROOT}/agents/migration-reviewer.md`). **On a genuine PASS only**, record the content-bound marker `.codearbiter/.markers/migration-gate-passed` by running `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/migration-pass.py" || python "${CLAUDE_PLUGIN_ROOT}/hooks/migration-pass.py"`. This is not optional: the PreToolUse commit hook **H-14 blocks the commit** until the pass is recorded AND covers every migration file being committed (by content digest, no freshness window — an edit to a reviewed migration re-blocks). This closes the bare-`/commit` / small-lane gap from issue #77. On a BLOCK, do not record the pass.
- **CI/deploy review (mandatory routing, no marker gate):** if the staged set touches a CI/CD workflow (`_hooklib.is_ci_path` — defaults extendable via a `ci-paths` block in `security-controls.md`) or a deployment/IaC manifest (`_hooklib.is_deploy_path` — `deploy-paths` block), dispatch the `security-reviewer` agent (`${CLAUDE_PLUGIN_ROOT}/agents/security-reviewer.md`). This is the enforcement point the advisory `post-write-edit` reminders **H-15/H-16** point to, and it closes the bare-`/commit` / small-lane gap for CI/deploy (the `/review`, `/pr`, `/checkpoint`, and sprint lanes already dispatch it). Unlike crypto/secret/migration there is **no commit-block marker** — a CI workflow runs only once merged and IaC bites only on apply, so a BLOCK-level finding halts the commit via Phase 6 review, but routine CI/deploy edits are not gated per-commit. Act on the findings by severity; do not record a marker.

Record each result (PASS / BLOCK) for the report.

Gate: test, lint, secrets scan, and (when crypto/secret is touched) the security gate all PASS. Any failure halts the commit until fixed and re-run.

## Phase 5 — Behavioral proof · gate: BLOCK

Apply the shared fresh-run discipline in `${CLAUDE_PLUGIN_ROOT}/includes/fresh-verification.md`, with
**the spec's acceptance criterion** as the target — prove the behavior against the spec, not against a
self-report.

- Identify the proving command or observable: the acceptance criterion from `${CLAUDE_PROJECT_DIR}/.codearbiter/specs/<slug>.md` (or the task's verification in the plan). If none exists, derive the smallest command that exercises the claimed behavior.
- Run it fresh in this phase, read its output and exit code, and confirm the observed behavior matches the spec's acceptance criteria. A mismatch, or an unverifiable claim, blocks.

**Stakes:** a behavioral-proof mismatch means the change does not do what the spec claims — state what would ship broken if this passed ("the retry path never fires; a transient error would hang the caller"), not just "proof mismatch." That gap is exactly what a green-looking suite hides.

Gate: the change is proven to do what it claimed by fresh evidence — command output and exit code read in this phase. A self-reported "it works" does not pass.

## Phase 5.5 — Provenance auto-heal (conditional)

Compute the heal worklist from the staged set via `_provenancelib.heal_worklist(staged_paths, provenance, current_hashes)` — the subset of staged paths that are `drift_trigger:true` provenance entries whose recorded hash has diverged or is absent. **Empty worklist → skip this phase entirely; most commits pay nothing** (cost guarantee: ordinary commits touching no provenance source do zero re-scout work).

Non-empty worklist → run an **incremental re-scout scoped to those paths only** (not the full repo). For each path, re-examine whether the claims in the backing doc still hold:

- **Claim still holds → silently re-baseline.** Call `_provenancelib.rebaseline` to update the stored hash in `.codearbiter/.provenance/<doc>.json` and stage that file by explicit path so the re-baselined record rides THIS commit (ADR-0008 ride-along pattern — nothing is surfaced to the user). After staging, re-run the secrets scan from `tech-stack.md` over the newly-staged path(s) — any file staged after Phase 4 must still pass the automated secrets scan before the commit proceeds.
- **Claim changed → route to the existing Phase 6 diff-review.** The doc or code-map edit required to reflect the changed claim is proposed in diff review — the user reviews it as part of the normal diff; nothing is silently rewritten.

## Phase 6 — Diff review · gate: BLOCK

Read the complete staged diff (`git diff --cached`). Flag as blocking:

- Unexpected files — not discussed in the session.
- Credentials, tokens, API keys, or any secret — belt-and-suspenders to Phase 4.
- Incomplete changes — TODO markers, placeholder values, dead commented-out code, partial stubs.
- Tests disabled or skipped that were not intentionally disabled.
- Scope creep — changes outside the agreed feature or fix boundary.

**Board-edit exemption (ADR-0008):** an edit to `open-tasks.md` where `_taskboardlib.classify_board_diff(old, new)` returns a clean transition (done-flip `[~]`→`[x]`, start-flip `[ ]`→`[~]` with its optional minted dotted ID, or a single queued-add `[ ]`) is **expected and RETAINED** — it is not scope creep and MUST NOT be unstaged. Any other `open-tasks.md` change — a reworded or deleted entry, or an arbitrary content edit — does not classify as a transition and still flags as scope creep.

**Provenance re-baseline exemption (ADR-0008):** a `.codearbiter/.provenance/<doc>.json` file written by the Phase 5.5 auto-heal re-baseline is likewise **expected and RETAINED** — it is not scope creep and MUST NOT be unstaged. A heal-proposed doc or code-map edit (the claim-changed path from Phase 5.5) appears in the diff for normal review; treat it as any other finding. This exemption waives the scope-creep flag only; the secrets check is not waived — the automated re-scan in Phase 5.5 covers the provenance file.

On any blocking finding, unstage the affected files, surface the finding, and STOP. An out-of-scope change that should not be lost gets an inline `[NEEDS-TRIAGE]` marker before it is set aside.

**Stakes:** name what the finding would have cost if committed — a leaked credential is live the moment it lands and must be rotated; a scope-creep file ships untested behavior the review waved through. State that consequence on a credential or scope finding, not just "out of scope."

Gate: the diff is clean — zero blocking findings.

## Phase 7 — Selective stage · gate: BLOCK

**First, run the follow-up harvest — before staging anything.** Run the follow-up harvest (`${CLAUDE_PLUGIN_ROOT}/includes/harvest.md`) over any Phase 6 `[NEEDS-TRIAGE]` set-asides — promote discovered follow-ups to `open-tasks.md` (work) or `open-questions.md` (decision) via the existing harvest procedure. Running this before the commit means raised board tasks are staged and ride the work commit in the same payload.

**Atomicity rule:** a raised task riding the work commit is a **contingent default** — if the PR/branch is abandoned, the board additions are abandoned with it (self-correcting, ADR-0008). A follow-up that **must survive** PR abandonment is filed as a **GitHub issue**, not the board.

Then selectively stage: if files were unstaged in Phase 6, re-stage only the clean files by explicit path: `git add path/to/file`. When a clean task-board transition was retained by the Phase 6 board-edit exemption, include `open-tasks.md` in the selective stage by explicit path (`git add open-tasks.md`) alongside the work files, so the flip rides the same commit. Include any `open-tasks.md` additions produced by the harvest step in the same explicit-path stage. When Phase 5.5 produced a re-baselined provenance record, include the affected `.codearbiter/.provenance/<doc>.json` file(s) by explicit path in the same selective stage so the re-baselined record rides the work commit. Re-run `git diff --cached --name-only` and confirm the staged list matches the intended set exactly — no extra files. Unstage any extra and report the discrepancy.

Gate: the staged set contains exactly the intended files. MUST NOT use `git add -A`, `git add .`, or any wildcard.

## Phase 8 — Message · gate: BLOCK

Compose a Conventional Commits message:

- Subject: `<type>(<scope>): <imperative summary>`, MUST NOT exceed 72 characters.
- Blank line, then a body explaining WHY — not a restatement of what changed.
- For `feat` and `fix`, add a `CHANGELOG:` footer summarizing the user-visible impact.
- If the commit closes an issue or references a decision, add the footer (`Closes #NN`, `Ref: ADR-NNNN`).
- No content-free subjects — "fix bug", "update code", "changes" do not pass.

Gate: subject ≤ 72 chars, a body is present, and any `feat`/`fix` carries a `CHANGELOG:` footer.

## Phase 9 — Commit · gate: BLOCK

Commit with the approved message via `-m` or heredoc with proper quoting — never an interactive editor. Capture the resulting SHA.

If a pre-commit hook fails: read its output in full, fix the issue, re-stage by explicit path (Phase 7 rules apply), and create a NEW commit. MUST NOT `--amend` after a hook failure.

After a successful commit, run `git status` to confirm the tree is clean. Deliver the report: SHA, branch, explicit file list, gate results (test / lint / secrets), and the message used.

Gate: the commit lands and `git status` is clean. Unexpected uncommitted changes after the commit block closure — report the discrepancy.

## Hard rules

- MUST NOT commit without explicit user authorization. "It looks good" is not permission.
- MUST NOT commit to `main`, `master`, or any protected branch.
- MUST NOT run `git add -A`, `git add .`, or any wildcard staging.
- MUST NOT commit while any test is failing, any lint error stands, or any secret is present.
- MUST NOT accept a self-reported "it works" — prove the behavior against the spec with a fresh command run (Phase 5) before committing.
- MUST NOT skip, disable, or work around any automated gate.
- MUST NOT commit a staged database migration without a recorded migration-review pass — the H-14 hook blocks it until `migration-reviewer` passes and `hooks/migration-pass.py` records the content-bound marker.
- MUST NOT `--amend` after a pre-commit hook failure — create a new commit.
- MUST NOT guess the test, lint, or secrets-scan command — read `tech-stack.md` or STOP.
- MUST NOT silently rewrite a doc's claims — a claim-change edit proposed by Phase 5.5 goes through diff review (Phase 6), never through the silent re-baseline path. The re-baseline path is strictly for claims that still hold; the Phase 5.5 re-baseline MUST ride the work commit (staged by explicit path in Phase 7).
- MUST, **at Phase 7 before staging**, run the follow-up harvest (`${CLAUDE_PLUGIN_ROOT}/includes/harvest.md`) over any Phase 6 `[NEEDS-TRIAGE]` set-aside — promote to `open-tasks.md` (work) or `open-questions.md` (decision) so raised tasks ride the work commit. A follow-up that must survive PR abandonment is filed as a GitHub issue, not the board.
