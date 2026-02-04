---
name: bio-workflow-methods-docwriter
description: Generate reproducible bioinformatics/data-science Methods + run documentation from workflow run artifacts (Nextflow/Snakemake/CWL), including a top-of-doc workflow summary, exact executed commands, tool versions, parameters, QC, and outputs.
---

# Bio Workflow Methods Docwriter

Create **publication-ready Methods + internal run documentation** for a *specific executed* bioinformatics or data science workflow run.

## When to use
Use this Skill when you need to document:
- **exact workflow flow + steps that actually ran**
- **tool + reference versions** (and/or container image digests)
- **key parameters + QC gates**
- **outputs and how to reproduce the run**

## Hard rules (reliability)
- **Never invent** commands, tool versions, reference versions, or dataset accessions.
- If an item is missing from evidence, write **`NOT CAPTURED`** and add a **“How to capture next time”** note.
- Prefer **verbatim command scripts** from the workflow engine (e.g., Nextflow `.command.sh`) over paraphrases.
- Keep user data private: redact tokens, credentials, and PHI.

## Inputs (evidence package)
Ask for (or locate) an *evidence package* folder containing:
- Workflow engine artifacts (Nextflow/Snakemake/CWL)
- Pipeline config + params
- Software version artifacts (e.g., nf-core `software_versions.yml`, conda env export, container digest)
- Run logs + QC reports

See: `reference/evidence-checklist.md`

## Output artifacts (always produce all 3)
1. **Workflow Summary** (top of doc): 5–12 lines, plain language + step bullets.
2. **Methods & Run Documentation** (`METHODS.md`): detailed, step-by-step.
3. **Machine-readable Run Manifest** (`run_manifest.yaml`): exact run metadata & steps (validate).

Schema + validator:
- Schema: `schemas/run-manifest.schema.json`
- Validate: `python scripts/validate_run_manifest.py run_manifest.yaml`

Optional structured literature record (only if asked):
- `PaperSummary` record using `schemas/bio-paper-schema.yaml`

## Workflow
Copy this checklist into your working notes and check off as you go:

- [ ] 1) Inventory evidence files (log what you have / what is missing)
- [ ] 2) Build `run_manifest.yaml` from evidence (no guessing)
- [ ] 3) Validate manifest (fix schema errors)
- [ ] 4) Draft `METHODS.md` (summary first, then detailed steps)
- [ ] 5) Run quality gates (versions, parameters, QC, outputs, reproducibility command)

### Quality gates (must pass)
- Every major step has: purpose • inputs • outputs • command (or NOT CAPTURED) • tool+version (or NOT CAPTURED)
- Reproduction section includes: pinned pipeline revision • container/conda info • full run command • params/config paths
- “Workflow Summary” appears at the very top

## Quick examples (triggers)
- “Write the Methods section for this Nextflow run directory, include exact commands and versions.”
- “Document this Snakemake pipeline run with a workflow summary at the top and a reproducibility appendix.”
- “Summarize this paper’s protocol into the PaperSummary schema.”

