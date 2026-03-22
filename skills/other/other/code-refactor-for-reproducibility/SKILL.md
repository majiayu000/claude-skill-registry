---
name: code-refactor-for-reproducibility
description: Transforms research code into publication-ready, reproducible workflows. Adds documentation, implements error handling, creates environment specifications, and ensures computational reproducibility for scientific publications.
license: MIT
skill-author: AIPOCH
---
# Research Code Reproducibility Refactoring Tool

Refactor research code for publication by adding documentation, parameterizing hardcoded values, pinning dependencies, and validating deterministic outputs.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- Refactoring analysis scripts for publication or sharing with collaborators
- Adding documentation and error handling to existing research code
- Creating reproducible computational workflows with pinned environments
- Preparing code for journal submission or data repository deposit

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback template:** If `scripts/main.py` fails or inputs are missing, report: (a) which step failed, (b) what partial output is still valid, (c) the manual equivalent command or reasoning path.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--input` | string | Yes | Source code file or directory to refactor |
| `--output` | string | Yes | Output directory for refactored code |
| `--language` | string | No | Language hint: `python` or `r` (default: auto-detect) |
| `--template` | string | No | Journal template: `nature`, `science`, `elife` |
| `--project-name` | string | No | Project name for README and environment files |

## Usage

```text
python scripts/main.py --input analysis.py --output refactored/ --language python
python scripts/main.py --input src/ --output pub_ready/ --template nature --project-name my-study
```

## Refactoring Steps

**Step 1 — Analyze:** Identify reproducibility issues (missing docstrings, hardcoded paths, missing seeds, bare `except:`, unpinned imports, magic numbers).

**Step 2 — Refactor:** Apply docstrings, parameterize paths via `argparse`, set random seeds (`SEED = 42`), add structured error handling with `logging`.

**Step 3 — Environment:** Generate `requirements.txt` via `pipreqs` or `environment.yml` with pinned versions. Verify clean install in a fresh venv.

**Step 4 — Validate:** Run pipeline twice, diff outputs, confirm checksums match pre-refactor baseline. Run `pytest tests/ -v`.

→ Full patterns and templates: [references/guide.md](references/guide.md)

## Output Requirements

Every response must make these explicit:

- Objective and deliverable
- Inputs used and assumptions introduced
- Workflow or decision path taken
- Core result or artifact
- Constraints, risks, caveats
- Unresolved items and next-step checks

## Input Validation

This skill accepts: research code files (Python/R scripts, notebooks, analysis pipelines) submitted for reproducibility improvement.

If the request does not involve refactoring existing research code — for example, asking to write new code from scratch, debug unrelated software, or perform statistical analysis — do not proceed. Instead respond:

> "`code-refactor-for-reproducibility` is designed to improve reproducibility of existing research code. Your request appears to be outside this scope. Please provide source code files to refactor, or use a more appropriate skill for your task."

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks
