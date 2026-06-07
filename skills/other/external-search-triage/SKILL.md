---
name: external-search-triage
description: |-
  Use when deciding whether external research is needed and turning cited findings into repo actions.
  Triggers:
practices:
- pragmatic-programmer
hexagonal_role: supporting
consumes:
- repo-context
- task-question
- external-source-candidates
produces:
- search-triage-note
- citation-log
- grounded-next-actions
context_rel: []
skill_api_version: 1
user-invocable: false
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: library
  stability: stable
  dependencies: []
output_contract: "A concise triage note that records the search question, query choices, cited sources, confidence, and grounded repository next actions."
---

# External Search Triage - ground repository decisions with cited sources

Use this skill when repository work depends on facts that may live outside the
checkout: current library behavior, API documentation, standards, advisories,
release notes, issue discussions, or ecosystem conventions. The goal is not to
collect links. The goal is to decide what evidence is needed, gather the
smallest useful set of sources, cite the facts that matter, and convert those
facts into concrete next actions in the repo.

## Critical Constraints

- Search because a decision needs evidence, not because the topic is vaguely
  interesting.
- Prefer primary sources: official docs, specs, source repositories, release
  notes, changelogs, issue threads, security advisories, and package registries.
- Keep repository evidence in charge. External sources explain dependencies and
  context; local code, tests, and generated artifacts define what this repo does.
- Capture the source, date, version, and exact claim being used. A bare URL is
  not a citation.
- Separate facts, inferences, and proposed actions. Do not let a blog post
  become an implementation plan without a repo-specific reason.

## When To Search

Use targeted web/search queries when at least one of these is true:

- The answer depends on current external behavior: package versions, API
  signatures, platform limits, security guidance, pricing, policies, or release
  status.
- The repo references an external tool, service, standard, or dependency and the
  local documentation may be stale.
- A failing test, build error, or runtime symptom mentions an external project,
  error code, protocol, or dependency version.
- You need a citation for a design decision, review finding, user-facing doc, or
  risk assessment.
- Multiple plausible fixes exist and external compatibility facts decide which
  fix is least risky.

Skip search when the repository already contains authoritative evidence for the
question, the work is a local refactor with no external contract, or the request
explicitly asks for local-only analysis.

## Frame The Search

Before searching, write a one-line frame:

```
Question: <fact needed>
Decision it affects: <repo action or review conclusion>
Freshness needed: <current / version-specific / historical>
Repo anchors: <file, symbol, command, error, dependency, or version>
Stop condition: <what evidence is enough>
```

If the decision it affects is unclear, inspect the repo first. Searching before
you know the local decision usually produces generic evidence.

## Query Strategy

Start narrow and widen only if needed:

1. Query the exact repo anchor: dependency name plus version, error code, API
   symbol, command flag, config key, or protocol name.
2. Add intent terms: migration, deprecation, breaking change, security advisory,
   compatibility, example, or release notes.
3. Bias toward primary domains with targeted queries, such as an official docs
   domain, a source repository, a package registry, a standards body, or a
   vendor advisory page.
4. Add date or version terms when freshness matters.
5. If results conflict, search for the source of the conflict: release notes,
   merged pull requests, issue closure comments, or documentation history.

Avoid broad queries like "best way to fix build" or "how does this library
work". They bury the fact you need under unrelated examples.

## Source Triage

For each candidate source, decide whether it is usable before reading deeply:

- Authority: Is it primary, maintained by the project, or directly tied to the
  service or standard?
- Match: Does it cover the version, platform, language, and workflow used by the
  repo?
- Freshness: Does the date or release line match the question?
- Specificity: Does it state the fact needed, or only discuss a related concept?
- Reproducibility: Can the claim be checked against a command, test, schema, or
  code path in the repo?

Reject sources that are stale, anonymous, content-farm summaries, unrelated to
the repo's version, or only useful as background.

## Citation Capture

Record citations while researching, not afterward. Use this compact shape:

```
| Claim | Source | URL | Date accessed | Version/date covered | Confidence |
| --- | --- | --- | --- | --- | --- |
| <fact used> | <title or project page> | <link> | <YYYY-MM-DD> | <version/date> | high/medium/low |
```

For each citation, include only the claim that affects the repo decision. Quote
short fragments only when exact wording matters; otherwise paraphrase and link.
If you infer something from a source, label it as an inference.

## Turn Findings Into Actions

End the triage by mapping evidence to work:

```
Finding: <cited fact>
Repo impact: <file, behavior, command, dependency, or doc affected>
Action: <change, test, doc update, review comment, or no-op>
Confidence: <high/medium/low and why>
Follow-up: <remaining uncertainty or validation command>
```

Prefer actions that can be validated locally: add or update a test, pin or bump a
dependency, adjust docs to match current behavior, change a command, or open a
small issue with the cited evidence. If the evidence only changes confidence,
say that and avoid inventing a code change.

## Output Shape

When reporting results, keep it short and source-backed:

1. Search frame: the question, decision, and stop condition.
2. Queries used: only the queries that found useful evidence.
3. Citations: claim, source, URL, date accessed, version/date covered,
   confidence.
4. Grounded next actions: repo impact, action, validation, and any remaining
   uncertainty.

## Quality Rubric

A triage pass is complete only if:

- Every external claim used for a repo decision has a citation.
- Citations include enough context to judge authority, freshness, and version
  match.
- Conflicting sources are either resolved or called out with their impact.
- Next actions name concrete repo files, commands, tests, docs, or issue follow
  ups.
- The result distinguishes verified facts from inferences and assumptions.
