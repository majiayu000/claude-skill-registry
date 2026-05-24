---
name: paper-review-lite-codex
description: Cross-model adversarial pre-submission audit. Claude and Codex independently apply the paper-review-lite specification, then each cross-checks the other's findings; surviving issues are annotated by confidence.
argument-hint: "[path to paper or describe manuscript to review]"
context: fork  # Claude Code: run skill in a forked subagent context (isolated from conversation history). See https://code.claude.com/docs/en/skills#frontmatter-reference
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
---

# Paper Pre-Submission Review (Lite, Cross-Model Adversarial)

This is the cross-model sibling of [`paper-review-lite`](../paper-review-lite/SKILL.md), itself the in-session, Claude-Code-native counterpart to [`presubmit`](https://github.com/scdenney/presubmit) (our port of the [reviewer2](https://github.com/isitcredible/reviewer2) adversarial peer-review pipeline). The heritage carries over wholesale. Sub-agents adopt a Critical-Reviewer posture, every finding is grounded in a verbatim quote, and a verification cascade filters hallucinations before they reach the final report.

The new mechanic is cross-model adversarial verification. Two reviewers — Claude (the orchestrator) and Codex (GPT-5.4, called through `codex:codex-rescue`) — independently apply the same `paper-review-lite` specification to the same paper. Each then plays Blue Team to the other's Red Team. Two different model families have different blind spots, so:

- **Mutual catches** (both teams flag the issue, both cross-checks confirm) are high-confidence.
- **Asymmetric catches** (one team flags, the other's cross-checker confirms against the paper) survive at standard confidence and often surface real but easy-to-miss problems.
- **Asymmetric refutations** (one team flags, the other's cross-checker refutes against the paper) are dropped by default. The orchestrator can override by re-reading the manuscript directly, but the burden is on the override.
- **Quote-failed** findings (the cross-checker cannot find the cited verbatim span) are dropped as hallucinations.

This is the heavier sibling. Roughly 22 model calls total (9 Claude Red Team, 9 Codex Red Team, 4 cross-model Blue Team) plus orientation and synthesis by the orchestrator. Reach for it before submission when you want maximum adversarial pressure and a second model family's blind spots. For the heaviest standalone deliverable — Red Team personas (Breaker, Butcher, Shredder, Collector, Void), math audits, code-replication checks, resumable, cost-tracked — use [`presubmit`](https://github.com/scdenney/presubmit).

## Instructions

### 1. Orientation (orchestrator, before any review agent launches)

Run the orientation step from `paper-review-lite` § 1 verbatim. Read the paper yourself to determine source format (LaTeX, Pandoc, Word), SI location, figure paths, replication archive, bibliography format, and design family. Use this to write specific review prompts that name actual file paths and section names. Generic prompts produce shallow reviews from both model families.

For experimental manuscripts, also invoke `methods-reporting` in audit mode and fold its 45-item checklist into Agents 6 and 7 on both teams. For conjoint, list-experiment, topic-modeling, LLM-classification, or VLM-OCR manuscripts, invoke the matching sibling skill and fold its checklist into Agent 9 on both teams.

### 2. Orchestration contract

Create this scratch layout in the paper's working directory.

```
.review-tmp/
├── claude/
│   ├── agent-1-content.md
│   ├── agent-2-numbers.md
│   ├── agent-3-references.md
│   ├── agent-4-dois.md
│   ├── agent-5-writing.md
│   ├── agent-6-consort.md
│   ├── agent-7-prereg.md
│   ├── agent-8-figures.md
│   └── agent-9-archive.md
├── codex/
│   ├── agent-1-content.md   (same dimensions, Codex output)
│   ├── ...
│   └── agent-9-archive.md
└── cross-check/
    ├── claude-checks-codex-content.md     (covers Codex agents 1, 2, 6, 7)
    ├── claude-checks-codex-technical.md   (covers Codex agents 3, 4, 5, 8, 9)
    ├── codex-checks-claude-content.md
    └── codex-checks-claude-technical.md
```

Both teams write independently to their own subdirectory. Cross-checkers read the *other* team's subdirectory. Use absolute paths when spawning Codex sub-agents. The `codex:codex-rescue` runtime inherits the parent working directory, but explicit paths remove ambiguity when the paper lives outside the current CWD.

### 3. Phase 2 — Dual independent Red Team (18 parallel calls)

Launch all 18 review calls in a single message.

- **9 Claude sub-agents** via the `Agent` tool (default `subagent_type`). Use the agent prompts from `paper-review-lite` § 2 (Agents 1–9) verbatim, but redirect output to `.review-tmp/claude/agent-N-*.md` instead of the original `.review-tmp/agent-N-*.md`.
- **9 Codex sub-agents** via the `Agent` tool with `subagent_type: codex:codex-rescue`. Use the Codex Phase 2 template below, one call per dimension. Output to `.review-tmp/codex/agent-N-*.md`.

Both teams apply the same dimension definitions, the same Critical-Reviewer posture, and the same severity rubric (`[CRITICAL]`, `[RECOMMENDED]`, `[MINOR]`) from `paper-review-lite` § 2. The point of running two model families on one specification is to compare independent applications of one standard, not to give them different jobs. Neither team sees the other's findings during Phase 2.

Agents 6 (CONSORT) and 7 (pre-registration) are required for experimental manuscripts and marked `NA` for non-experimental ones on both teams.

### 4. Phase 3 — Cross-model adversarial verification (4 parallel calls)

Each model verifies the other's findings. Cross-checkers do not add new findings; that was Phase 2's job. They verify, refute, or downgrade.

**Claude cross-checks Codex (2 sub-agents via `Agent`).**

- Sub-agent A reads `.review-tmp/codex/agent-{1,2,6,7}-*.md` and the manuscript. Writes `.review-tmp/cross-check/claude-checks-codex-content.md`.
- Sub-agent B reads `.review-tmp/codex/agent-{3,4,5,8,9}-*.md` plus the manuscript, bibliography, and archive. Writes `.review-tmp/cross-check/claude-checks-codex-technical.md`.

For each Codex `[CRITICAL]` or `[RECOMMENDED]` finding, the cross-checker verifies the cited verbatim quote appears at the cited location, verifies the issue against the actual paper, flags any Codex finding that Claude also flagged independently in `.review-tmp/claude/` (mutual catch — note for synthesis), and steel-mans the paper. When the paper anticipates or partially addresses the concern, note it for severity downgrade.

**Codex cross-checks Claude (2 sub-agents via `Agent` with `subagent_type: codex:codex-rescue`).**

- Sub-agent C reads `.review-tmp/claude/agent-{1,2,6,7}-*.md`. Writes `.review-tmp/cross-check/codex-checks-claude-content.md`.
- Sub-agent D reads `.review-tmp/claude/agent-{3,4,5,8,9}-*.md`. Writes `.review-tmp/cross-check/codex-checks-claude-technical.md`.

Use the Codex Phase 3 template below. Same verification protocol.

### 5. Phase 4 — Adjudication and synthesis (orchestrator, direct)

Build the consolidated Pre-Submit Report by adjudicating across teams.

- **Mutual.** Both teams flagged it; both cross-checkers confirmed. Mark `[CRITICAL ✓✓]` or `[RECOMMENDED ✓✓]`. Highest-confidence findings.
- **Asymmetric, cross-confirmed.** One team flagged; the other team's cross-checker confirmed against the paper. Retain at original severity. Mark `[CRITICAL ✓]` or `[RECOMMENDED ✓]`. These often surface real but easy-to-miss problems.
- **Asymmetric, cross-refuted.** One team flagged; the other team's cross-checker refuted against the paper. Default action is to drop. The orchestrator can override by re-reading the manuscript directly, in which case retain at one tier below original severity with the note "single-team finding, cross-refuted, retained after orchestrator re-read at <file:line>".
- **Quote-failed.** The cross-checker could not find the cited verbatim span. Drop as hallucination on the finder's side.

Apply the synthesis rules from `paper-review-lite` § 4 in order. Deduplicate within-team first (multiple agents on the same team flagging the same underlying issue). Then deduplicate across-team (a mutual catch is one entry, not two). Then demote self-conceded critiques (any finding whose own description includes language conceding the point). Then write a single-line Recommendation at the top of the report. Then write the Editor's Note (3–6 paragraph prose memo). Then the issue lists. Then the journal-readiness checklist. Then "What Still Needs Your Input".

The Critical Issues and Recommended Changes tables get one extra column compared to the original `paper-review-lite` report.

```
| Severity | Confidence                                      | Location | Issue | Fix |
|----------|-------------------------------------------------|----------|-------|-----|
| CRITICAL | Mutual (Claude + Codex)                         | …        | …     | …   |
| CRITICAL | Asymmetric: Codex only, confirmed by Claude     | …        | …     | …   |
| CRITICAL | Asymmetric: Claude only, cross-refuted, retained after orchestrator re-read | … | … | … |
```

Everything else in the report follows the `paper-review-lite` § 4 format exactly. Top-line Recommendation, then Editor's Note, then Critical / Recommended / Minor lists, then Strengths, then Journal-Readiness Checklist, then What Still Needs Your Input.

## Codex Phase 2 template (one per dimension, 9 total)

Spawn `codex:codex-rescue` with the prompt below. Substitute `DIMENSION_INSTRUCTIONS` with the verbatim text of the corresponding agent from `paper-review-lite` § 2 (the full text of Agent 1, Agent 2, …, Agent 9 — do not paraphrase). Substitute `PAPER_PATH` with the absolute manuscript path and `OUTPUT_PATH` with the absolute path to the Codex agent's output file under `.review-tmp/codex/`.

```xml
<task>
You are a Critical Reviewer auditing the manuscript at PAPER_PATH for the dimension below.

Posture (required): adversarial but fair. Find every place the argument is weaker than the paper presents it to be. Attack the argument or the data, not the authors. Framing like "fraudulent" or "incompetent" is out of scope. "The claim on line X is not supported by the evidence on line Y" is in scope.

Dimension:

DIMENSION_INSTRUCTIONS

Write your findings to OUTPUT_PATH. Do not write to any other file.

A second model (Claude) is independently performing the same review on the same paper for the same dimension. You will not see its findings. After both passes complete, each model's findings will be verified by the other. Findings without a verbatim quote will be dropped as hallucinations during cross-check.
</task>

<output_format>
Structured list, not prose. For each issue:
- Severity: [CRITICAL] / [RECOMMENDED] / [MINOR]
- Location: file path and line number, or section name
- Issue: one sentence describing the problem
- Fix: one sentence describing what to do
- Quote: a verbatim span (≤ 2 sentences) from the manuscript that supports the finding. REQUIRED for every [CRITICAL] and [RECOMMENDED] finding. Optional for [MINOR].

Severity rubric (apply consistently):
- [CRITICAL] — blocks submission. Wrong numbers, broken references, missing ethics or data-availability statement when required, silent pre-registration deviation, anonymization failure, unreproducible main result.
- [RECOMMENDED] — will draw reviewer complaint. Unsupported claim, missing robustness check, undefined threshold, missing limitation, insufficient figure caption, undocumented exclusion.
- [MINOR] — polish. Style, typography, citation format, wording consistency.
</output_format>

<action_safety>
Scope. Read PAPER_PATH and any files it references (bibliography, archive, SI). Write only to OUTPUT_PATH. Do not edit the manuscript or any other file.
</action_safety>

<default_follow_through_policy>
Apply the dimension end-to-end without stopping for confirmation.
If the finding is unambiguous, record it.
If the finding requires author knowledge to confirm (embargo status, IRB number), record it as [RECOMMENDED] with the caveat "requires author confirmation".
Do not ask clarifying questions mid-run.
</default_follow_through_policy>
```

## Codex Phase 3 template (cross-check Claude's findings)

Used for sub-agents C and D in Phase 3. Substitute `PAPER_PATH`, `INPUT_FILES` (a comma-separated list of `.review-tmp/claude/agent-N-*.md` paths the cross-checker should read), and `OUTPUT_PATH`.

```xml
<task>
You are a verification cross-checker. Another model (Claude) has produced findings about the manuscript at PAPER_PATH. Your job is to verify each finding against the actual manuscript.

Read the findings file(s) at INPUT_FILES. For each [CRITICAL] or [RECOMMENDED] finding, output one verdict entry.

1. QUOTE CHECK. Does the cited verbatim quote appear at the cited location in PAPER_PATH? If not, verdict is "QUOTE FAILED — drop as hallucination".
2. ISSUE CHECK. Does the issue itself hold up against the actual paper text? If the issue does not exist, is already addressed elsewhere in the paper, or is a misreading, verdict is "REFUTED" with a one-sentence explanation citing the paper line that refutes it.
3. STEEL-MAN. If the issue is real, note whether the paper anticipates or partially addresses the concern. If it does, verdict is "CONFIRMED, downgrade one severity tier — partially addressed at <file:line>".
4. OTHERWISE. Verdict is "CONFIRMED".

Do not add new findings of your own. You are verifying, not reviewing.

Write your verdicts to OUTPUT_PATH.
</task>

<inputs>
Findings to verify: INPUT_FILES
Manuscript: PAPER_PATH
</inputs>

<output_format>
For each finding in the input files, one entry.
- Source finding: <Claude agent N, severity, location>
- Quote check: PASS / FAIL
- Issue check: CONFIRMED / REFUTED / DOWNGRADE
- Evidence: one sentence citing the paper line that supports the verdict.
- Original severity vs. recommended severity (if downgrade)
</output_format>

<action_safety>
Read PAPER_PATH and the files listed in INPUT_FILES. Write only to OUTPUT_PATH. Do not edit the manuscript or the input files.
</action_safety>

<default_follow_through_policy>
Process every finding in the input files end-to-end. Do not ask clarifying questions mid-run.
</default_follow_through_policy>
```

## Quality Checks

- [ ] Orientation completed by the orchestrator before any review agent launches. Paper structure, SI location, archive location, and design family identified.
- [ ] For experimental manuscripts, `methods-reporting` invoked in audit mode and its 45-item checklist folded into Agents 6 and 7 on both teams.
- [ ] For domain-specific manuscripts (conjoint, list-experiment, topic-modeling, text-classification, VLM-OCR), the relevant sibling skill is invoked and its checklist folded into Agent 9 on both teams.
- [ ] Three subdirectories created under `.review-tmp/`. `claude/`, `codex/`, `cross-check/`.
- [ ] All 18 Phase 2 calls (9 Claude + 9 Codex) launched in a single parallel message.
- [ ] Both teams use the same dimension prompts and severity rubric from `paper-review-lite` § 2. No model gets a different job.
- [ ] Codex sub-agents called via `Agent` with `subagent_type: codex:codex-rescue` and absolute paths in the prompt.
- [ ] Agents 6 and 7 marked `NA` on both teams for non-experimental or non-preregistered manuscripts.
- [ ] All 4 Phase 3 cross-check calls launched in a single parallel message after all 18 Phase 2 output files exist.
- [ ] Phase 3 cross-checkers do not add new findings. Verify, refute, or downgrade only.
- [ ] Adjudication produces one entry per underlying issue. Across-team deduplication done after within-team deduplication.
- [ ] Quote-failed findings dropped as hallucinations on the finder's side.
- [ ] Asymmetric, cross-refuted findings dropped by default. Retention requires an explicit orchestrator re-read of the manuscript and a note on the entry.
- [ ] Final report annotates each retained Critical / Recommended issue with confidence. Mutual, Asymmetric-confirmed, or Asymmetric-after-adjudication.
- [ ] Synthesis applies `paper-review-lite` § 4 rules. Single-line Recommendation at top, Editor's Note (3–6 paragraphs) before issue lists, Strengths section present, journal-readiness checklist filled, "What Still Needs Your Input" populated with author-knowledge items.
- [ ] Every retained issue cites file path and line number, or section name.
- [ ] Report distinguishes objective errors from subjective suggestions.

## When to reach for this skill vs. siblings

| Skill | Adversarial depth | Cost | When |
|-------|-------------------|------|------|
| `paper-review-lite` | Single-model, 11 agents, in-session verification cascade | Lightest | Fast in-flow review during writing |
| `paper-review-lite-codex` (this) | Cross-model, 18 agents plus 4 cross-checks, dual verification cascade | ~2× the calls of `paper-review-lite` | Before submission, when you want maximum pressure and a second model family's blind spots |
| [`presubmit`](https://github.com/scdenney/presubmit) | ~30 stages, dedicated Red Team personas, Blue Team defence, math and code-replication audits, resumable, cost-tracked | Heaviest, separate Anthropic API key | The review is the deliverable. Co-author feedback, pre-print critique, final pre-submission pass. |
