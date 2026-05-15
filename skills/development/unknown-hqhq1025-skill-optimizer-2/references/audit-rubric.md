# Audit Rubric

Use this rubric before personalizing an existing skill, especially when the user says it undertriggers, overtriggers, feels noisy, is too long, conflicts with other skills, or might be worth deleting.

## Data Sources

Use the same evidence surfaces as `skill-miner`: active sessions, archived sessions, rollout summaries, exported transcripts, installed skill files, and project-local agent instructions.

Keep raw transcripts local unless the user asks for verbatim evidence. Prefer sanitized examples in reports.

## Audit Dimensions

| Dimension | What To Check |
| --- | --- |
| Trigger fit | Does the description match real user phrasing and likely retrieval terms? |
| Undertrigger | User asked for the capability but the skill was not used or not followed. |
| Overtrigger | Skill appears to fire for neighboring tasks where it adds friction. |
| User reaction | After skill use, did the user accept, correct, reject, interrupt, or switch topics? |
| Workflow completion | Did the agent complete the skill's stated steps or stop midway? |
| Static quality | Frontmatter, description, word count, structure, progressive disclosure, and clarity. |
| Cross-skill conflicts | Trigger overlap, duplicated workflows, or contradictory instructions. |
| Environment consistency | Referenced files, paths, commands, tools, hosts, and install paths exist or are documented. |
| Token economics | Large rarely used skills should be compressed, split, or moved into references/scripts. |

## Static Quality Checklist

- Frontmatter contains only safe cross-agent fields unless platform-specific metadata is intentionally isolated.
- `name` is lowercase hyphen-case.
- `description` starts with `Use when` and describes trigger conditions, not the workflow.
- Strongest trigger terms appear early in the description.
- `SKILL.md` is concise; long examples, rubrics, scripts, and data belong in bundled resources.
- YAML is quoted when punctuation could break parsing.
- Critical safety rules appear near the top of the skill body.
- Avoid narrative postmortems such as “in one session we found”.
- Avoid excessive MUST/NEVER emphasis; use concrete rules and rationale.

## Research-Backed Heuristics

- Treat undertriggering as a compounding risk: skills that are not retrieved cannot gather feedback or improve through use.
- Prefer retrieved, narrow, relevant context over stuffing many long skills into every prompt.
- Front-load trigger and safety details because long-context models can miss information buried in the middle.
- Require evidence for workflow completion; durable skills should encode practices that have been validated, not merely imagined.
- Review community or downloaded skills for provenance, permissions, and environment assumptions before trusting them.
- Distinguish agent-native behavior from portable `SKILL.md` behavior before calling a skill broken.

## Report Format

```markdown
# Skill Audit Report
Scope: <skills audited>
Evidence: <sources scanned, date range, limitations>

## Overview
| Skill | Trigger Fit | Usage Evidence | Static | Conflicts | Token | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |

## P0 Fixes
1. ...

## P1 Improvements
1. ...

## P2 Optimizations
1. ...

## Per-Skill Notes
### <skill-name>
- Evidence:
- Diagnosis:
- Suggested edits:
- Validation prompts:
```

## Recommendation Labels

- `keep`: healthy or strategically useful.
- `personalize`: valuable but needs local paths, phrasing, or workflow defaults.
- `generalize`: reusable but too personal for publication.
- `split`: one skill contains multiple unrelated workflows.
- `compress`: skill is too large for its value or should move details to references/scripts.
- `remove`: no evidence of need, obsolete, or unsafe.
