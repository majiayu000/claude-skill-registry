---
name: perspective-validation
description: Create a Perspective Validation Checklist (PVC) report for a change, workflow, schema, or policy. Use when performing socio-technical review, governance review, operational readiness review, or when a PR touches schemas/hooks/skills/tools and needs a PVC report.
argument-hint: "[target] [risk_tier] [domain]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Write, Edit, Bash, Git
context: fork
agent: general-purpose
---

## Intent

Produce a **PVC report** (Perspective Validation Checklist) that scores the target against key non-type failure modes (human factors, governance, economics, adversarial security, loop stability, data governance, and legitimacy) with concrete evidence references and remediation actions.

**Success criteria:**
- A valid PVC report is written to `docs/reviews/pvc/` and passes `python skills/perspective-validation/scripts/validate_pvc.py`
- Each non-N/A score is justified with at least one evidence reference
- Any FAIL/PARTIAL includes a concrete remediation action (P0/P1/P2)

**References:**
- `CHECKLIST.md`
- `pvc_report_template.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `target` | Yes | string | What to review (file/dir path, workflow name, or PR/change description) |
| `risk_tier` | No | enum | `low \| medium \| high` (defaults to `medium` if unclear) |
| `domain` | No | string | Domain context (e.g., `general`, `manufacturing`, `healthcare`) |
| `deployment` | No | string | Deployment context (e.g., `local-dev`, `customer-facing`, `safety-critical`) |

## Procedure

1) **Scope the review**: Confirm `target`, `domain`, `deployment`, and `risk_tier`
   - If the target is a PR or branch diff, identify changed files and whether they touch critical paths (`schemas/`, `hooks/`, `skills/`, `grounded_agency/`, `tools/`, `spec/`)

2) **Collect evidence**: Read the minimum set of files needed to justify scores
   - Prefer evidence anchors as `file:path#Lline` (or `file:path:line` if needed)
   - When reviewing a change set, include at least one evidence item for “what changed” and “what it affects”

3) **Score the checklist**: For each PVC test ID (HF-101 … ECO-901), assign one of:
   - PASS: explicitly satisfied with evidence
   - PARTIAL: acknowledged but missing enforcement/measurement/runbook detail
   - FAIL: absent
   - N/A: not applicable to this target (include a brief reason in `assumptions` or in an action note)

4) **Write the report**: Create a new file in `docs/reviews/pvc/` named:
   - `YYYY-MM-DD_<short-slug>.pvc.yaml`
   - Start from `pvc_report_template.yaml`, then fill it in completely

5) **Validate**: Run `python skills/perspective-validation/scripts/validate_pvc.py`
   - If it fails, fix the report until it passes

6) **Summarize actions**: Provide the top remediation actions (P0 first), with crisp “what to change” and “where it lives” guidance

## Output Contract

Return a structured object:

```yaml
pvc_report_path: string  # Path under docs/reviews/pvc/
target: string
context:
  domain: string
  deployment: string
  risk_tier: low | medium | high
scorecard:
  HF-101: PASS | PARTIAL | FAIL | N/A
  HF-102: PASS | PARTIAL | FAIL | N/A
  HF-103: PASS | PARTIAL | FAIL | N/A
  ORG-201: PASS | PARTIAL | FAIL | N/A
  GOV-202: PASS | PARTIAL | FAIL | N/A
  ECON-301: PASS | PARTIAL | FAIL | N/A
  ECON-302: PASS | PARTIAL | FAIL | N/A
  SEC-401: PASS | PARTIAL | FAIL | N/A
  SEC-402: PASS | PARTIAL | FAIL | N/A
  CTRL-501: PASS | PARTIAL | FAIL | N/A
  ASSUR-601: PASS | PARTIAL | FAIL | N/A
  ASSUR-602: PASS | PARTIAL | FAIL | N/A
  DG-701: PASS | PARTIAL | FAIL | N/A
  ETH-801: PASS | PARTIAL | FAIL | N/A
  ECO-901: PASS | PARTIAL | FAIL | N/A
actions:
  - id: string
    priority: P0 | P1 | P2
    fix: string
    artifact: doc | workflow | policy | hook | test | benchmark | code
    owner: string
confidence: number  # 0.0-1.0
evidence_anchors: array[string]
assumptions: array[string]
```

## Example

### Example: Review a workflow DSL change

**Input:**
```yaml
target: "schemas/workflow_catalog.yaml (new gates + recovery semantics)"
risk_tier: medium
domain: general
deployment: customer-facing
```

**Output:**
```yaml
pvc_report_path: "docs/reviews/pvc/2026-01-29_workflow-catalog-gates.pvc.yaml"
target: "schemas/workflow_catalog.yaml (new gates + recovery semantics)"
context:
  domain: "general"
  deployment: "customer-facing"
  risk_tier: "medium"
scorecard:
  HF-101: PARTIAL
  HF-102: FAIL
  HF-103: PARTIAL
  ORG-201: FAIL
  GOV-202: FAIL
  ECON-301: FAIL
  ECON-302: N/A
  SEC-401: PARTIAL
  SEC-402: PARTIAL
  CTRL-501: PASS
  ASSUR-601: PARTIAL
  ASSUR-602: FAIL
  DG-701: FAIL
  ETH-801: N/A
  ECO-901: PASS
actions:
  - id: "DOC-001"
    priority: P0
    fix: "Add an operator-facing incident view schema and a minimal tabletop exercise for this workflow family."
    artifact: doc
    owner: "maintainers"
confidence: 0.7
evidence_anchors:
  - "file:schemas/workflow_catalog.yaml#L1"
assumptions:
  - "No runtime UI exists; report assumes log-based incident response."
```

## Safety Constraints

- This skill is intended to be **read-mostly**.
- Only write under `docs/reviews/pvc/` unless the user explicitly asks for additional changes.
- Do not include secrets/PII in evidence excerpts; prefer references/hashes over raw content.

