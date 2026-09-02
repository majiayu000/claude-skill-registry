---
name: propose-issue
description: 'Use when the user asks to propose an issue, file or open a bug report, or turn a reported defect into a tracked issue. Grounds the defect in cited source, gates it, and files one issue. Don''t use for fixing the defect, triaging existing issues, or reviewing PRs.'
disable-model-invocation: true
---

# Propose issue

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A human explicitly asks to propose an issue, file or open a bug report, or turn a reported defect into a tracked issue. |
| Authority | Human-only. Preview the repository, proposed title, body, and consequence before using authenticated GitHub access; the explicit invocation authorizes creation of at most one issue in that previewed repository, and no other remote mutation. |
| Side effect | Create one GitHub issue with `gh` only after the evidence, duplicate, and six-criterion self-review gates all pass. |
| Done | Report the created issue URL, or abort and name the failing criterion; never report both. |

## Inputs

The reported symptom or suspected defect is required. An explicit target repository is optional; otherwise resolve the repository from the current checkout. Source files and history needed to investigate the report must be readable. Authenticated `gh` access is required only for tracker search and issue creation. Reproduction details, affected versions, and configurations are optional evidence and must not be invented when absent.

## Procedure

1. Resolve the target repository from the explicit target or the current checkout. Before any authenticated GitHub command, preview the resolved repository, the intended consequence of creating one public or repository-visible issue, and the fact that no other remote state will change. Stop if the repository cannot be resolved unambiguously. Done when: the repository is resolved and the consequence is previewed, or the run stops on ambiguity.
2. Locate the reported behavior in source opened during this run. Attach a `path:line` citation to every factual claim intended for the issue. Record a user-reported symptom that cannot be located only as an explicitly attributed, unconfirmed report; do not assert it as fact. Done when: every factual claim has a `path:line` citation and unlocatable symptoms are attributed as unconfirmed.
3. Separate mechanism from symptom. Name the causal mechanism supported by the cited source, determine the affected callers, versions, and configurations that the available evidence supports, and reproduce the defect. If reproduction is impossible, record the exact reason in one line rather than claiming a result. Done when: the causal mechanism is named, affected scope is determined, and reproduction is attempted or its impossibility is recorded.
4. Search all issue states before drafting with `gh issue list --repo <target> --state all --search "<mechanism and symptom terms>"`. Record either `no match` or the matching issue number. Treat the same mechanism as a duplicate even when wording differs; do not treat the same symptom caused by a different mechanism as a duplicate. If a matching issue exists, stop without creating anything and report its URL or number. Done when: the duplicate search is complete and no match is found, or a duplicate is reported.
5. Draft a title that states the defect rather than a proposed fix. Draft the body with exactly these headings in this order: `Summary`, `Reproduction`, `Evidence`, `Expected vs actual`, and `Scope`. Include only claims supported under steps 2 and 3. Done when: the title states the defect and the body has the five headings in order with only supported claims.
6. Preview the final target repository, title, complete body, and issue-creation consequence. Then mark each gate criterion explicitly as pass or fail: (1) every factual claim has a `path:line` citation read during this run; (2) the report is a defect rather than a preference or style opinion; (3) the supported mechanism is named rather than only the symptom; (4) the duplicate search ran and found no match; (5) the title states the defect rather than the fix; and (6) no claim relies on a file not opened during this run. Any failure stops filing. Done when: all six gate criteria are marked pass or fail, and any failure stops filing.
7. Only when all six criteria pass, run `gh issue create --repo <target> --title <title> --body <body>` once. Accept success only when the command confirms creation with an issue URL; do not retry a result that may have created the issue until the tracker has been checked for that exact title and body. Done when: the issue is created and confirmed with a URL, or an ambiguous result is checked before retry.

## Failure and recovery
- Unresolved target or unavailable source: make no remote change; return the draft material available, the missing input, and the criterion that cannot be established.
- Unsupported defect or failed reproduction: preserve unsupported observations as explicitly attributed, unconfirmed reports, make no remote change, and return the draft with the failed evidence or mechanism criterion.
- Duplicate found: make no remote change and return the matching issue instead of a new draft as though filing succeeded.
- Gate failure: make no remote change; return the draft, all six pass/fail marks, and every failing criterion.
- Tracker search failure: do not infer `no match`; make no remote change and return the command failure as a blocked duplicate criterion.
- Create failure with confirmed no issue created: make no further remote change and return the error with the retained final draft.
- Ambiguous create result: search the target for the exact title and body before any retry. If exactly one matching issue exists, report its URL; if none or more than one exists, do not retry and return a blocked result naming the ambiguity.

No failure path may claim completion. Partial evidence and drafts may be returned, but the terminal result remains an abort until the issue URL is confirmed.

## Output
Return exactly one terminal classification: - **Filed:** the target repository and confirmed issue URL. - **Aborted:** the target repository when known, the retained draft or duplicate match when available, and the specific failed or blocked criterion. Never return both classifications.
