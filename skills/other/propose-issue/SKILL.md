---
name: propose-issue
description: 'Turn a symptom into a source-grounded GitHub issue: find the evidence, analyse cause versus symptom, draft the issue, pass a self-review gate, then file it. Use when the user says "propose an issue", "file an issue for this", "open a bug report", or hands you a defect to turn into a tracked issue.'
metadata:
  short-description: 'Evidence-grounded GitHub issue: analyse, self-review, file'
---

# propose-issue

A filed issue is a claim someone else will act on. The cost of a wrong one is not the issue, it is the hour the maintainer spends disproving it. So the work is not writing: it is grounding the symptom in source, naming the mechanism behind it, and passing a gate strict enough to stand in for a human reviewer.

Run the sections in order. Filing is reachable only through the gate.

## Evidence

Locate the defect in real source before describing it. Open the files; do not reason from memory or from the user's paraphrase.

Every factual claim destined for the issue body carries a `path:line` citation read during this run. A symptom the user reported but you could not locate in source is recorded as unconfirmed and stays unconfirmed in the draft. Never assert it.

**Completion criterion:** every claim destined for the issue body has a `path:line` citation, or is explicitly marked unconfirmed.

## Analysis

Separate cause from symptom. State the mechanism, not the surface: "the loop reuses the buffer across iterations" is a mechanism, "output is garbled" is a surface.

Determine blast radius: which callers, which versions, which configurations. Then reproduce the defect, or state exactly why reproduction is not possible.

**Completion criterion:** the issue names one mechanism with its evidence, and reproduction is either demonstrated or its absence explained in one line.

## Duplicate check

Before drafting, search the tracker:

```bash
gh issue list --repo <target> --state all --search "<key terms>"
```

An existing issue covering the same mechanism aborts filing. Report the match instead. Same symptom under a different mechanism is not a duplicate.

**Completion criterion:** the search was run and its result recorded, either "no match" or the matched issue number.

## Draft

The issue body uses exactly these headings, in this order:

- `Summary`
- `Reproduction`
- `Evidence`
- `Expected vs actual`
- `Scope`

The title states the defect, never the proposed fix. "Buffer reused across loop iterations" is a title; "Add per-iteration buffer allocation" is a patch description wearing a title's clothes.

## Self-review gate [LOAD-BEARING]

This gate replaces user approval, so it is the load-bearing section of the skill. Mark each of the six explicitly. All six must pass.

1. Every factual claim carries a `path:line` citation read this run.
2. The reported thing is a defect, not a preference or a style opinion.
3. The mechanism is named, not just the symptom.
4. The duplicate search ran and returned no match.
5. The title states the defect, not the fix.
6. No claim rests on a file that was not opened this run.

Any single failure means do not file. Emit the draft and name the failing criterion.

**Completion criterion:** all six explicitly marked pass, or the filing is aborted with the failing criterion named.

## File

Reachable only when the gate passes fully.

```bash
gh issue create --repo <target> --title <title> --body <body>
```

The target repo defaults to the current checkout, resolved via `gh repo view --json nameWithOwner`. An explicit target overrides it.

**Completion criterion:** the issue URL is reported, or the abort reason from the gate is reported. Never both.
