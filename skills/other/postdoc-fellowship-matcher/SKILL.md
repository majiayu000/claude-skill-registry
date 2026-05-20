---
name: postdoc-fellowship-matcher
description: Filter and match postdoctoral fellowship opportunities based on applicant nationality, years since PhD, and research field from a curated database.
license: MIT
skill-author: AIPOCH
---
# Postdoc Fellowship Matcher

Filter postdoctoral fellowships based on applicant nationality, years since PhD, and research area.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- Use this skill when a postdoc applicant needs to identify eligible fellowships based on their nationality, career stage, and research field.
- Use this skill when comparing fellowship requirements and deadlines across multiple programs.
- Do not use this skill to draft fellowship applications, write personal statements, or guarantee eligibility determinations.

## Workflow

1. Confirm the applicant's nationality, years since PhD completion, and research field.
2. Validate that the request is for fellowship matching, not application writing or eligibility certification.
3. Filter the fellowship database against the provided criteria.
4. Return a ranked list of eligible fellowships with deadlines, requirements, and notes.
5. If inputs are incomplete, state which fields are missing and request only the minimum additional information.

## Usage

```text
python scripts/main.py --nationality US --years 1 --field "immunology"
python scripts/main.py --nationality CN --years 3 --field "structural biology" --name "Dr. Zhang"
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--nationality` | string | Yes | Applicant nationality (e.g., `US`, `CN`, `DE`) |
| `--years` | integer | Yes | Years since PhD completion |
| `--field` | string | Yes | Research field (e.g., `immunology`, `neuroscience`) |
| `--name` | string | No | Applicant name (for report header) |

## Fellowship Database

Includes: NIH F32 · NSF Postdoctoral Fellowships · HFSP Fellowship · EMBO Fellowship · Marie Curie Fellowships · Schmidt Science Fellows

→ Full fellowship details: [references/fellowships.md](references/fellowships.md)

## Field Input Normalization

The `--field` parameter accepts free-text research field names. Common aliases are normalized automatically:

| Input | Normalized To |
|-------|---------------|
| `structural bio` | `structural biology` |
| `cell bio` | `cell biology` |
| `neuro` | `neuroscience` |
| `immuno` | `immunology` |

If your field is not recognized, the skill will return the closest matches and ask you to confirm.

## Output

- Eligible fellowships list with match rationale
- Deadlines and key requirements per fellowship
- Notes on eligibility caveats and verification steps

## Scope Boundaries

- Fellowship data reflects the built-in database; verify current deadlines and requirements on official program websites before applying.
- This skill does not access live fellowship databases or real-time deadline updates.
- Eligibility output is a filter result, not a legal or official determination.

## Stress-Case Rules

For complex multi-constraint requests, always include these explicit blocks:

1. Assumptions
2. Filter Criteria Applied
3. Matched Fellowships
4. Caveats and Verification Steps
5. Next Checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate fellowship deadlines, eligibility rules, or success rate statistics.

## Input Validation

This skill accepts: applicant nationality, years since PhD, and research field for fellowship eligibility filtering.

If the request does not involve fellowship matching — for example, asking to write a fellowship application, provide career counseling, or access live grant databases — do not proceed with the workflow. Instead respond:
> "postdoc-fellowship-matcher is designed to filter fellowship opportunities based on applicant profile criteria. Your request appears to be outside this scope. For application writing support, consider using an academic writing skill or consulting your institution's postdoc office. Please provide nationality, years since PhD, and research field, or use a more appropriate tool."

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

If the request is simple, you may compress the structure, but still keep assumptions and limits explicit when they affect correctness.
