---
name: paper-review-lite-codex
description: Run a cross-model adversarial pre-submission audit from Codex. Use when a user explicitly requests the heavier paper-review-lite-codex workflow, independent Codex and Claude review passes, or cross-model verification of a manuscript. Apply the paper-review-lite protocol, cross-check findings against the manuscript, and retain only evidence-grounded issues.
---

# Paper review lite: Codex lead, cross-model audit

Run Codex as the lead and use Claude Code's non-interactive CLI as the independent model family. This is the Codex-side equivalent of the Claude skill with the same name; the direction of delegation is reversed.

Read [`../paper-review-lite/SKILL.md`](../paper-review-lite/SKILL.md) completely before starting. It defines the review dimensions, severity rubric, evidence requirements, and final report format. If the sibling skill is unavailable, stop and tell the user to install it; do not reconstruct a partial protocol from memory.

## Preflight

1. Confirm that the user explicitly requested `$paper-review-lite-codex` or a cross-model audit. Otherwise use `$paper-review-lite`.
2. Locate the manuscript, supplement, bibliography, figures, preregistration, and replication archive.
3. Check `command -v claude` and run a harmless authentication/status check supported by the installed CLI. Do not print credentials.
4. Explain that `claude -p` is an external model call that may consume separate credits. Obtain confirmation before the first call unless the user already explicitly authorized Claude or cross-model execution.
5. If Claude is unavailable or authorization is declined, offer the fallback in “Reduced-diversity mode.”

Claude Code documents `claude -p` as its non-interactive interface. Use `--output-format text`, `--no-session-persistence`, and read-only tools for review calls. See [Run Claude Code programmatically](https://code.claude.com/docs/en/headless).

## Orient once

Follow `$paper-review-lite` Phase 1. Read the manuscript before spawning reviewers. Record actual absolute paths, design family, source format, target journal, and missing inputs. Create:

```text
.review-tmp/
├── codex/
├── claude/
└── cross-check/
```

Treat this directory as disposable workflow state. Preserve it only if the user asks.

## Phase 1: independent Red Teams

### Codex cohort

Run the nine `$paper-review-lite` review dimensions in parallel batches that respect the runtime's agent limit. Each subagent receives only:

- the relevant dimension block from `$paper-review-lite`;
- the manuscript and related absolute paths;
- the common severity and quote requirements; and
- its assigned output path under `.review-tmp/codex/`.

Keep agents blind to one another. Require direct manuscript evidence for every critical or recommended issue.

### Claude cohort

Run three independent Claude CLI calls concurrently when safe:

1. argument, claims, and numerical consistency;
2. references, DOI status, writing, figures, and tables;
3. methods, CONSORT/preregistration where applicable, and replication readiness.

Construct each prompt from the matching dimension blocks in `$paper-review-lite`; do not paraphrase away requirements. Tell Claude to read the named files, print structured Markdown only, and never edit them. Redirect stdout to the assigned file under `.review-tmp/claude/`.

Use this command shape, substituting absolute paths and a complete prompt file:

```bash
claude -p \
  --output-format text \
  --no-session-persistence \
  --allowedTools "Read" \
  "$(< /absolute/path/to/prompt.txt)" \
  > /absolute/path/to/.review-tmp/claude/review-N.md
```

Do not use `--bare` unless API-key authentication is configured explicitly; bare mode skips normal OAuth and keychain discovery. Never pass secrets in the prompt or command line.

Validate every output file. A non-zero exit, empty file, or refusal is a failed reviewer, not evidence that the manuscript passed.

## Phase 2: blind cross-check

After both cohorts finish, launch four verification passes:

- two Codex subagents verify Claude's content/methods and technical findings;
- two Claude CLI calls verify Codex's corresponding findings.

For each critical or recommended issue, require this sequence:

1. Find the quoted span at the cited location. If absent, mark `QUOTE FAILED` and drop it.
2. Check whether the manuscript already answers the concern elsewhere. If yes, mark `REFUTED` or `DOWNGRADE` with the contradicting location.
3. Check the issue on its merits. Mark `CONFIRMED`, `REFUTED`, or `DOWNGRADE`.
4. Do not add new issues during cross-checking.

Cross-checkers read the manuscript plus the other cohort's files, never their own cohort's findings.

## Phase 3: adjudicate

Apply these rules in order:

- **Mutual and confirmed:** retain at the stronger justified severity; label `Mutual (Codex + Claude)`.
- **Single-cohort and cross-confirmed:** retain; label the originating cohort and confirmation.
- **Single-cohort and cross-refuted:** drop unless the lead rereads the source and records specific contrary evidence. If retained, demote one tier.
- **Quote failed:** drop.
- **Reviewer failed:** record reduced coverage; never convert missing output into a pass.

Deduplicate by underlying issue, not wording. Then follow `$paper-review-lite` Phase 4 to write the recommendation, editor's note, severity-ranked issues, strengths, readiness checklist, and “What Still Needs Your Input.” Add a `Confidence` column to critical and recommended findings.

## Reduced-diversity mode

If Claude cannot run, ask whether to continue with two blind Codex cohorts. If approved:

- give each cohort fresh context and identical specifications;
- keep cohorts blind until cross-checking;
- label the report `same-model independent review`, never `cross-model`; and
- state that agreement is weaker evidence because model-family blind spots are shared.

If the user declines, run ordinary `$paper-review-lite` or stop as requested.

## Completion checks

- Every retained critical or recommended issue has a verified quote and location.
- Both directions of cross-check completed, or reduced coverage is explicit.
- Failed/empty reviewer outputs are disclosed.
- No agent edited the manuscript.
- The final report is self-contained and does not expose scratch prompts or agent chatter.
- `.review-tmp/` is removed after delivery unless the user asked to keep it.
