---
name: wontfix
description: 'Use when the user wants to elicit refused directions, generalize them, and close matching tracker items as not planned. Don''t use for closing duplicates, spam, or items closed for other reasons (completed, obsolete).'
disable-model-invocation: true
---

# Wontfix

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to elicit refused directions, generalize and concretize them, and close matching tracker items as not planned. |
| Authority | Explicit human invocation only. Before any mutation the exact target set and its consequence are previewed and approved; the same approval gates the optional docs record. No credentials, paid actions, publishing, or deployment occur. |
| Side effect | Matching tracker items closed as not planned; optional refusal preserved in docs. |
| Done | Refused directions are documented and matching items are closed as not planned after user approval. |

## Inputs

Must be supplied by the user:

- The refused directions or designs, in the user's own words; rough phrasing is acceptable and is recorded verbatim.
- The GitHub repository in scope; the working repository is used when `gh repo view --json nameWithOwner` resolves it, otherwise an explicit `owner/repo` is required.
- Explicit approval of the exact closure set before any mutation.

Optional:

- A durable refusal record in the docs folder; without the request, no docs file is touched.
- Narrowing filters (labels, assignees, search terms) to bound enumeration.

## Procedure

1. Name the tracker in scope: run `gh repo view --json nameWithOwner`; on error, ask for `owner/repo` and rerun `gh repo view <owner>/<repo> --json nameWithOwner`. Done when: tracker is identified, or the step has stopped on failure with zero mutations.
2. Elicit refused directions: ask the user what will not be done. Record each statement verbatim. Never add, infer, or propose refusals the user did not state. Done when: all refused directions are recorded verbatim.
3. Generalize and concretize each verbatim refusal: the generalization is the refused class of work in one sentence; the concretization is the detectable matching signals (keywords, component or path names, label names, design choices). A refusal that resists either form is ambiguous. Done when: every refusal has a generalization and concretization, or is marked ambiguous.
4. Resolve every ambiguous refusal and confirm the completed refusal list with the user. The list is frozen only after this confirmation. Done when: refusal list is confirmed and frozen.
5. Enumerate the open tracker surface: `gh issue list --repo <owner>/<repo> --state open --json number,title,body,url,labels --limit 200` and `gh pr list --repo <owner>/<repo> --state open --json number,title,body,url,labels --limit 200`. When the returned count equals the limit, rerun with a higher `--limit` until the open set is fully covered. Done when: open issues and PRs are fully enumerated, or the step has stopped on enumeration failure with zero mutations.
6. Match items to refusals: an item joins the closure set only when its title, body, or labels match a concretized signal of some refusal. For borderline candidates read the full item with `gh issue view` or `gh pr view`, and include it only on an explicit signal match. Record kind, number, title, URL, matched refusal, and matched signal for every included item; list excluded borderline items as not matched. Done when: every open item is classified as matched or not matched.
7. Preview and gate: present the exact closure set (number, kind, title, URL, matched refusal) with the consequence — issues close with reason "not planned", pull requests close unmerged with the refusal as the closing comment, and the docs record plan when requested. Mutate only after the user explicitly approves this exact set; any later change to the set requires fresh approval. Done when: user explicitly approves the exact closure set, or the step waits for approval.
8. Close each approved item, one at a time, recording every result: issue — `gh issue close <number> --repo <owner>/<repo> --reason "not planned" --comment "<generalization>"`; pull request — `gh pr close <number> --repo <owner>/<repo> --comment "<generalization> (closed as not planned)"`. A failed close is recorded and does not block the remaining approved items; failed items are never silently skipped. Done when: every approved item is attempted with its result recorded.
9. Confirm every intended closure: `gh issue view <number> --repo <owner>/<repo> --json state,stateReason` must report `"state": "CLOSED"` with `"stateReason": "NOT_PLANNED"`, and `gh pr view <number> --repo <owner>/<repo> --json state` must report `"state": "CLOSED"`. An item still reporting open receives exactly one retry of its close command and one re-check; a second miss is reported as unconfirmed. Done when: every approved item is confirmed closed or reported as unconfirmed.
10. Write the optional docs record only when the user requested it and after the step 7 approval: append a dated section to `docs/refused-directions.md` (create the file when missing) listing each refusal verbatim, its generalization and concretization, and the closed item numbers with URLs. Rollback is deletion of the appended section; the rest of the file is untouched. Done when: docs record is written or skipped (not requested).
11. Report per Output. The done predicate holds only when every approved item is confirmed closed. Done when: report is emitted and done predicate is evaluated.

## Failure and recovery
- Tracker unreachable or unauthenticated: any failing `gh` command before step 8 stops the skill in a blocked state with the command and error reported verbatim; zero items mutated.
- Unresolvable repository: blocked until the user supplies `owner/repo`; never guessed.
- Ambiguous or unmatched refusal: returned to the user with the blocking question; matches are never guessed from inference. A refusal with zero matching items is a valid outcome, reported as such.
- Partial batch failure: already-confirmed closures stand because each was individually approved; remaining approved items are still attempted; unconfirmed and failed items are named exactly. Done is never claimed while any approved item is unconfirmed.
- Wrong item closed: recovery is an explicit reopen on user instruction only, `gh issue reopen` or `gh pr reopen`, recorded in the report.
- Docs write failure: closures are unaffected; report the filesystem error and the intended section content; never report a record that was not written.
- Errors are surfaced verbatim; the done predicate is never reported as holding when any approved item is unconfirmed.

## Output
A refusal ledger (every verbatim refusal with generalization, concretization, and matched items), a closure table (number, kind, title, URL, result per item: confirmed closed as not planned / confirmed closed / unconfirmed / failed with error text), the docs record path when written or "not requested", a terminal classification (done / partial / blocked), and borderline items intentionally left open.
