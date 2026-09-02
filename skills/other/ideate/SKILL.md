---
name: ideate
description: 'Use when a human asks to brainstorm, asks what to build, requests ideas for a divergent subject, or invokes /ideate. Produces a grounded ideation artifact committed locally with adjudicated survivors and a reason for every rejection.'
---

# Ideate

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A human says "let's brainstorm", asks "what should we build" or "any ideas for", or invokes `/ideate` on a divergent subject. |
| Authority | Read the repository and write only the named local ideation artifact files. Stage and commit only files written by this run. All delegated exploration, generation, critique, and review is read-only. No source modification, no remote mutation, no push. |
| Side effect | Writes `docs/ideation/<slug>.md`; with `format:html`, also writes `docs/ideation/<slug>.html`. Stages and commits only files written by this run. |
| Done | The canonical Markdown records grounded survivors and a reason for every rejected candidate; every candidate cites its basis; one Reviewer has adjudicated the complete pool; each output has been read back; only the run's outputs are in one staged-scope commit; the result ends at intent clarification rather than planning or implementation. |

## Inputs

The human must supply an identifiable divergent subject, either as ordinary text or after `/ideate`. An optional leading `format:html` requests a self-contained HTML view in addition to the mandatory Markdown. The operating repository is the grounding corpus. If the root contains `STRATEGY.md`, use it as optional strategic context; its absence is not an error. Derive `<slug>` by lowercasing the subject, replacing each run of non-alphanumeric characters with one hyphen, and trimming leading and trailing hyphens; reject an empty result.

## Procedure

1. Parse the optional format flag and subject. Reject unsupported flags, an empty subject, an empty derived slug, or a target that would escape `docs/ideation/`. Before any write, fix the exact output set as the Markdown path and, only when requested, the matching HTML path. If either target already exists, stop with `blocked: target-exists` rather than overwrite it. Done when: the output set is fixed and no target exists.
2. Ground the subject before generating ideas. Read the smallest relevant repository surfaces and `STRATEGY.md` when present. Record architecture, existing patterns, constraints, and strategic context with `file:line` citations. For a single known concern, use one read-only explorer; for multiple or uncertain concerns, use three in parallel; for a cross-module or architectural subject, use five in parallel. If the evidence does not identify the subject, stop with `blocked: subject-unidentified` and request clarification without writing or staging anything. Done when: the grounding summary is recorded with citations, or the subject is reported as unidentified.
3. Build distinct generation assignments by crossing repository-relevant topic axes with different frames such as user value, workflow, architecture, reliability, leverage, and constraint removal. Launch every read-only generator in one parallel dispatch, supplying the same grounding summary but a different axis-frame assignment. Require roughly six to eight concise candidates from each generator and require every candidate to include an idea, rationale, and `file:line` basis. Allow `external:<source>` only when that source was actually inspected. Drop ungrounded candidates and record that rejection rather than inventing a citation. Done when: all generators have returned or failed, and ungrounded candidates are dropped with recorded rejections.
4. Give the complete raw pool to one read-only critic. Treat every candidate as rejected unless it clears all four tests: its cited basis supports it, it is feasible in this repository, it is not a restatement of another survivor, and it would change a meaningful decision. Require `survive` or `reject` plus a one-line reason for every candidate; no candidate may disappear silently. Done when: every candidate has a critic verdict and reason.
5. Give the grounding summary, full raw pool, and all critic verdicts to one read-only Reviewer. Require the Reviewer to audit completeness, consistency, accuracy, and scope, then return the sole authoritative survivor set and rejection reasons. Apply that adjudication without rescuing a rejection or re-litigating a survivor. If any candidate lacks a final verdict and reason, stop with `non-converged: incomplete-adjudication` before writing. Done when: the Reviewer has returned the authoritative survivor set and rejection reasons for every candidate.
6. Assemble `docs/ideation/<slug>.md` with, in order: the subject; grounding context and citations; topic axes and generation frames; survivors, each with rationale and evidence; rejected candidates, each with its rejection reason and evidence; and a next step that asks the human to clarify intent among the survivors. Do not plan or implement a survivor. Done when: the Markdown skeleton is assembled.
7. Create the parent directory if needed, write only the fixed Markdown target, and read it back. Verify that every adjudicated candidate appears exactly once as surviving or rejected, every survivor has rationale and evidence, every rejection has a reason and evidence, and the next step is intent clarification. A failed check blocks staging. Done when: the Markdown is written, read back, and verified.
8. If `format:html` was supplied, render one self-contained HTML file from the verified Markdown without adding or removing substantive content. Write only the fixed HTML target, read it back, and verify heading, survivor, rejection, rationale, citation, and next-step parity with the Markdown. The Markdown remains canonical. On parity failure, stop with `non-converged: html-parity`. Done when: the HTML is written, read back, and parity-verified, or the format flag was not supplied.
9. Show the exact output set, then stage only those paths by explicit path. Never stage all changes and never alter pre-existing unrelated index entries. Inspect the staged paths and stop with `blocked: staging-scope` unless they exactly equal this run's output set. Create one local commit containing exactly that staged set. Verify the commit path set equals the output set. Do not publish or push. Done when: the commit is created and verified, and the result ends at intent clarification.

## Failure and recovery

- `blocked: subject-unidentified`: the repository evidence does not identify the divergent subject. Request clarification. No files written or staged.
- `blocked: target-exists`: the output Markdown or HTML path already exists. Do not overwrite. Report the conflicting path.
- `non-converged: incomplete-adjudication`: a candidate lacks a final Reviewer verdict and reason. Stop before writing. Report the incomplete candidate.
- `blocked: staging-scope`: the staged paths do not exactly equal this run's output set. Unstage only the explicit paths and report the mismatch.
- `non-converged: html-parity`: the HTML view does not match the Markdown on heading, survivor, rejection, rationale, citation, or next-step content. Stop and report the parity failure.
- Write or read-back failure: report the exact files created and do not stage them. Recovery is to delete only those newly created files after preserving any requested diagnostic output.
- Before the first write, failure leaves the repository and index unchanged. After a partial write, report the exact files created and do not stage them. After staging failure, unstage only this run's explicit paths. If commit creation or commit-path verification fails, stop without publishing or pushing and report the exact local state.

## Output

On success, return the canonical `docs/ideation/<slug>.md`, optional parity-checked `docs/ideation/<slug>.html`, the exact committed path list and local commit identifier, counts of raw candidates, survivors, and rejections, and an intent-clarification prompt based only on the Reviewer's survivors. On failure, return the terminal blocked or non-converged classification, the failed gate, any partial files, and the precise rollback action.
