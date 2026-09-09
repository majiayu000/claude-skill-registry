---
description: >-
  Reviews local changes, an open PR/MR, or a branch diff against the project's own coding
  guidelines through the review lenses — bugs, security, guidelines, architecture,
  simplification, plus test coverage and API contracts when relevant — inline on a small diff,
  in parallel agents on a larger one. Excludes style and linter-catchable issues. Read-only:
  applies fixes or posts PR/MR comments only on explicit approval. For an iterative auto-fix
  loop, use /optimus:deep review.
disable-model-invocation: true
argument-hint: "[--pr N | --branch | path]"
---

# Code Review

Analyze local git changes (or a PR/MR) against the project's coding guidelines through the review lenses in Step 5 — inline on a small diff, in parallel agents on a larger one. Out of scope: style concerns, subjective preferences, and anything a linter already catches.

## Step 1: Parse Arguments and Verify Prerequisites

- `--branch` → force the branch diff in Step 3, skipping the PR auto-route. No effect when local changes exist or an explicit PR is requested (`--pr N`, `#N`, or a PR URL).
- Everything else is natural-language scope/focus: paths, PR numbers, refs (e.g., "review src/auth", "review PR #42", "changes since main").

**Multi-repo**: if the current directory has no `.git/` directory, read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` and apply it. In a workspace, run Step 3's git commands inside each child repo, PR/MR mode requires the user to name a repo, and Step 4 loads each repo's docs independently; if changed files map to no child repo, ask which repo's context applies.

**Prerequisites**: if `.claude/CLAUDE.md` or `.claude/docs/coding-guidelines.md` is missing, recommend `/optimus:init` first. On the user's choice to continue, fall back to the bundled baseline: read `$CLAUDE_PLUGIN_ROOT/skills/init/templates/docs/coding-guidelines.md` and review against it plus general best practices for the detected stack — a shared, versioned anchor keeps findings reproducible where ad-hoc judgment would not. Note in the report that findings are generic, not project-specific.

## Step 2: Inline Harness Mode Detection

If your invocation prompt body contains `HARNESS_MODE_INLINE`, you are running inside the `/optimus:deep` orchestrator as a single iteration. Read `$CLAUDE_PLUGIN_ROOT/references/harness-mode.md` and follow it — that reference governs which of the steps below run, how scope and agent prompts are overridden, and how this run ends.

If `HARNESS_MODE_INLINE` is NOT present, continue with the standard interactive flow below.

## Step 3: Determine Review Scope

**Local changes (default)**: gather staged + unstaged + untracked via `git diff --cached`, `git diff`, and `git status --short`. If local changes exist, review them.

**No local changes → auto-route** (no user prompt):

1. Detect the platform per the **Platform Detection Algorithm** in `$CLAUDE_PLUGIN_ROOT/skills/pr/references/platform-detection.md`.
2. Check for an open PR/MR on the current branch: GitHub `gh pr view --json number,state,baseRefName` (use only when `state` is `"OPEN"`); GitLab `glab mr view --output json` (use `iid`/`target_branch` only when `state` is `"opened"`; a failed command means no MR — unless it looks like an auth or connectivity error, in which case tell the user before falling back). Platform unknown: try both, use the first confirmed open PR/MR.
3. Base = the PR/MR target branch; with no open PR/MR or no CLI, detect the default branch per `$CLAUDE_PLUGIN_ROOT/skills/pr/references/default-branch-detection.md`. If detection fails, ask the user for a base ref — never guess; if they have none, report there is nothing to review.
4. Run `git log --oneline origin/<base>..HEAD`; if commits exist, route (branch diffs use Branch/ref mode with `<ref>` = `origin/<base>`; for GitLab say "MR !N" instead of "PR #N"):
   - `--branch` set → branch diff.
   - Open PR/MR found AND HEAD fully pushed (`git rev-list origin/<current-branch>..HEAD` exits 0 with no output) → enter PR mode for that PR without re-prompting. Tell the user, in one line: *"Reviewing PR #N — using the PR description as author intent context. Pass `--branch` to review the branch diff instead."*
   - Open PR/MR found BUT HEAD has unpushed commits or pushed state cannot be determined → branch diff. Tell the user, in one line: *"Reviewing the branch diff — PR #N exists but HEAD is not fully pushed. Pass `--pr N` to review only the PR's pushed state."*
   - No open PR/MR (or CLI unavailable) → branch diff.

**Nothing at all** → inform the user there are no changes to review; suggest staging changes or specifying a PR.

### PR mode

Entered on explicit request or via the auto-route. Detect the platform per the **Platform Detection Algorithm** (including **Signal Conflict Resolution**) in `$CLAUDE_PLUGIN_ROOT/skills/pr/references/platform-detection.md`; if unknown, ask the user.

| | GitHub | GitLab |
|---|---|---|
| Metadata | `gh pr view <N> --json state,isDraft,title,body,baseRefName,headRefName,headRefOid` | `glab mr view <N> --output json` |
| `pr-description` fields | `title` + `body` | `title` + `description` |
| Diff | `gh pr diff <N>` | `glab mr diff <N>` |
| Head SHA field | `headRefOid` | `sha` |
| Checkout | `gh pr checkout <N>` | `glab mr checkout <N>` |

- Verify the CLI first (`gh --version` / `glab --version`); if unavailable → tell the user PR/MR review requires it and offer the branch diff instead.
- Store the metadata's title + body as `pr-description` for Steps 5–6 (author intent context).
- PR/MR closed or merged → warn and stop.
- **Head mismatch**: if the head SHA differs from `git rev-parse HEAD`, offer the checkout command before continuing — Step 5's agents and Step 6's validation read the local working tree, so a mismatched checkout silently reviews the wrong file content. If declined, proceed with a warning that finding validation and line context come from the local tree, not the PR head.

**Branch/ref mode**: `git diff <ref>...HEAD` for the diff; `git diff --name-only <ref>...HEAD` for the file list.

**Path filter**: when the user scopes to a path, filter the diff to it (`git diff -- <path>`, `git diff --cached -- <path>`).

### Scope summary

Present a brief `## Review Scope` summary before proceeding: mode (local changes / PR #N / branch diff since `<ref>`), files changed, lines +/-. In PR/MR mode, append one note whenever intent-vs-implementation checks will not run — either the captured `pr-description` body is empty, **or** it is non-empty but has no `## Intent` section (apply the **Detection rule** in `$CLAUDE_PLUGIN_ROOT/skills/pr/references/pr-template.md`, the same rule `/optimus:pr` writes against, so both halves of the handoff share one definition). Say which case applies: intent-vs-implementation checks are skipped; running `/optimus:pr` in the implementation conversation can add intent metadata. Without this note a rich hand-written description reads as fully reviewed while every agent silently skipped the check. This is a soft warning — the review proceeds either way.

**Large diff warning**: if more than 50 files or 3000 lines are changed, warn the user and suggest narrowing the scope (e.g., a specific path or directory).

## Step 4: Load Project Context

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` and load the constraint docs it lists, applying its **Monorepo Scoping Rule** (a subproject's own docs govern that subproject's files) and **Submodule Exclusion** (a `.git` *file* marks a submodule — exclude those directories from the review). In a multi-repo workspace, load each changed repo's `.claude/CLAUDE.md` and `.claude/docs/` independently and apply per-repo context to that repo's files. These docs define the review criteria — every guideline finding must be justified by what they establish; never impose external preferences.

Present a brief context summary (docs loaded, docs missing with fallback status, project type), then proceed immediately to Step 5 — do not wait for confirmation.

## Step 5: Multi-Lens Review

The table below is the list of lenses this review has to cover. How many contexts you cover them in is yours to size.

**On a small diff — roughly 3 files or fewer and under 150 changed lines — apply the lenses yourself in one pass.** Five subagents over a five-line change each re-read the project docs and the same diff to produce findings you would reach directly; read the agent prompt files for their criteria and work through them. Fan out when the diff is large enough that one context cannot hold it with the docs, when the lenses need to read genuinely different parts of the tree, or in harness mode where the iteration's context is fresh and disposable.

When you do fan out, launch every applicable agent as a `general-purpose` Agent tool call in a **single** message so they run in parallel — separate messages serialize them for no benefit. Each agent covers a lens the others do not, so dropping one leaves that category unreviewed; the conditional rules below are how the fan-out shrinks on a narrow diff.

| Agent | Role | Prompt file |
|-------|------|-------------|
| 1 — Bug Detector | Null access, off-by-one, races, resource leaks, type mismatches | `bug-detector.md` |
| 2 — Security & Logic | Injection, XSS, secrets, missing auth, security-relevant API violations | `security-reviewer.md` |
| 3 — Guideline Compliance | Explicit violations of project docs, each citing the rule it breaks | `guideline-reviewer.md` |
| 4 — Architecture & Boundaries | Layering and dependency direction, module responsibility, structural pattern drift, placement | `architecture-reviewer.md` |
| 5 — Code Simplifier | Unnecessary complexity, dead code, removal-only simplifications | `code-simplifier.md` |
| 6 — Test Guardian | Test coverage gaps, structural barriers to testability | `test-guardian.md` |
| 7 — Contracts Reviewer | Backward compatibility, type safety, versioning, encapsulation | `contracts-reviewer.md` |

Lenses 1–5 always apply, inline or by agent. Lens 6 (Agent 6) applies when test infrastructure is detected (`.claude/docs/testing.md` or a subproject `docs/testing.md` exists). Lens 7 (Agent 7) applies when any changed file matches a contract pattern — directory patterns: `api/`, `routes/`, `controllers/`, `endpoints/`, `handlers/`, `graphql/`, `proto/`, `grpc/`; file patterns: `*.dto.*`, `*.schema.*`, `*.contract.*`, `openapi.*`, `swagger.*`, `*.proto`, `*.graphql`, `*.gql`. No match → skip it entirely.

**Prompt assembly**: read the prompt files from `$CLAUDE_PLUGIN_ROOT/skills/code-review/agents/`, plus `agents/shared-constraints.md` for the shared quality bar and output format. Compose per "Prompt assembly at dispatch time" in `$CLAUDE_PLUGIN_ROOT/references/agent-architecture.md`. For Agent 3, replace the `<!-- dispatcher: ... -->` line in `guideline-reviewer.md` with the concrete doc paths resolved in Step 4 for this project's layout.

End every assembled prompt with the changed-file list (from Step 3, or `scope_files.current` in harness mode when pre-populated) followed by the diff hunks — at minimum the changed line ranges per file when the diff is too large to inline. Agents have no sanctioned way to compute the diff themselves; never send file paths alone. Findings are bounded by the Finding Cap in `$CLAUDE_PLUGIN_ROOT/references/shared-agent-constraints.md`.

### PR/MR context injection (PR/MR mode only)

If the `pr-description` body captured in Step 3 is non-empty, prepend the PR/MR Context Block from `$CLAUDE_PLUGIN_ROOT/references/context-injection-blocks.md` (template, truncation rule, guardrail language) to every agent prompt immediately before the file list. Under `HARNESS_MODE_INLINE` on iterations 2+, also prepend the Iteration Context Block from the same reference — it defines the ordering when both blocks apply.

Wait for all launched agents to complete before proceeding to Step 6. This applies to every mode, not just the PR/MR path above: an agent still running when Step 6 starts contributes no findings to validate and none to the report, and the review prints its verdict anyway.

## Step 6: Validate Findings

Read `$CLAUDE_PLUGIN_ROOT/references/finding-validation.md` and apply it to every finding — the context, intent, pre-existing, and runtime-assumption checks plus change-intent awareness from git history. One code-review addition:

- **Cross-agent corroboration** — two agents independently flagging the same location raises confidence, even when their categories differ.

### PR/MR description as intent signal

If a `pr-description` was captured, use it as an additional soft signal: an explicit explanation of *why* a flagged change was made, corroborated by git history → one confidence reduction; contradicted or unsupported by git history → trust the history (code over claims); silent about the finding → no adjustment. Never hard-filter a finding on the description alone.

**Confidence after validation**: High and Medium proceed to Step 7. A finding you could not confirm against the code is dropped — but count the drops and report the count in the Step 7 summary, so filtered recall stays visible instead of silent. An agent's Low label describes *its* evidence, not yours: if your own check confirms the issue, promote it rather than dropping it.

## Step 7: Consolidate and Present Findings

- **Dedupe**: same file + line range + category → keep the more detailed version. When two agents reached it independently, merge into one and note "confirmed by independent review".
- **Contradictions**: findings on the same code region recommending opposite directions (e.g., "add validation" vs. "simplify this validation") → keep the higher severity; on ties, keep the security/correctness finding — security requirements justify proportionate complexity.
- **Severity**: **Critical** — bugs, security vulnerabilities, runtime failures, Intent Mismatch contradicting a stated non-goal. **Warning** — guideline violations, missing error handling, coverage gaps on critical paths, backward-incompatible contract changes, Intent Mismatch on unsupported scope claims. **Suggestion** — quality improvements, minor drift, Intent Mismatch on partial matches.
- **Finding cap**: max **15 domain findings** in the report, prioritized by severity then confidence. `Intent Mismatch` findings surface on top of the 15 — up to 5, deduplicated across agents, sorted by severity, presented after the domain findings. If more issues exist, note the count and suggest a narrower scope or `/optimus:deep review`.

Open with a **Change Summary** — 2–4 factual sentences on what the changes accomplish — so the user can verify the review understood them.

### Output format

```
## Code Review

### Summary
- Scope: [local changes / PR #N / branch diff since X]
- Files reviewed: [N]
- Lines changed: +[A] / -[R]
- Findings: [N] (Critical: [N], Warning: [N], Suggestion: [N])
- Docs used: [list]
- Agents: [list of agents run]
- Verdict: CHANGES LOOK GOOD / ISSUES FOUND

### Change Summary
[2–4 sentences]

### Findings

**[N]. [Finding title]** (Critical/Warning/Suggestion — [Category])
- **File:** `file:line`
- **Category:** [Bug | Security | Guideline Violation | Code Quality | Test Coverage Gap | Contract Quality | Intent Mismatch]
- **Guideline:** [project rule, "General: ...", or for Intent Mismatch the literal "Intent (see Intent claim)"]
- **Intent claim:** [Intent Mismatch only — the quoted claim from `## Intent`]
- **Issue:** [concrete description]
- **Current:** [code snippet — max 5 lines]
- **Suggested:** [fix or recommendation — max 5 lines]

[Order: Critical → Warning → Suggestion, each sorted by file path. If none: "The changes follow project guidelines. No bugs, security issues, or guideline violations detected."]
```

In PR mode, include full-SHA code links:
- GitHub: `https://github.com/owner/repo/blob/[full-sha]/path#L[start]-L[end]`
- GitLab: extract the instance URL from `git remote get-url origin`, then `https://[gitlab-host]/owner/repo/-/blob/[full-sha]/path#L[start]-L[end]`

## Step 8: Offer Actions

Verdict **CHANGES LOOK GOOD** → skip this step entirely; go to the closing recommendation.

Verdict **ISSUES FOUND** → `AskUserQuestion` (header "Action", question "How would you like to proceed with the review findings?"):
- **Fix issues** — apply suggested fixes directly, then run tests to verify
- **Post comment** (PR/MR mode only) — post the review summary as a PR/MR comment
- **Skip** — keep the report as reference only

**Posting a comment**: write the review summary to a temp file in the current working directory: `TMPFILE=$(mktemp ./review-summary-XXXXXX.md)`. Always clean up after the posting attempt (whether it succeeds or fails): `rm -f "$TMPFILE"`. Use a relative path, not `/tmp` — on Windows, Git Bash's `/tmp` mount is unresolvable by the native `gh.exe`/`glab.exe`, which would silently submit an empty comment.

- GitHub: `gh pr comment <N> --body-file "$TMPFILE"`
- GitLab: `glab api -X POST "projects/:id/merge_requests/<N>/notes" -F body=@"$TMPFILE"` — avoids the shell metacharacter breakage `glab mr note --message "$(cat ...)"` would hit with code snippets in the summary

## Important

- Outside harness mode this skill is read-only: never modify files, commit, push, or post comments without explicit user approval, and approved fixes remain local modifications the user reviews with `git diff` before committing. Under `HARNESS_MODE_INLINE` the orchestrator holds that approval and Step 2's protocol governs instead.
- When changes are too broad for effective review, recommend narrowing scope.

Close by recommending the next step: issues fixed → `/optimus:commit`; clean or fixes skipped → `/optimus:pr` (skip when already reviewing a PR/MR) — either way, stay in this conversation so the implementation context is captured. For iterative auto-fix, run `/optimus:deep review` in a fresh conversation.
