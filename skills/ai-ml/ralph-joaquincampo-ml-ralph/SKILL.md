---
name: ralph
description: "Convert an ML PRD into prd.json for ML-Ralph. Use when you have an ML PRD and need prd.json. Triggers on: convert this prd, turn this into ml-ralph format, create prd.json from this, ralph json."
---

# ML-Ralph PRD Converter

Converts ML PRDs into the `prd.json` format used by ML-Ralph.

---

## The Job

Take a PRD (markdown or text) and convert it to `prd.json` in the ML-Ralph directory.

---

## Output Format

```json
{
  "project": "[Project Name]",
  "branchName": "ml-ralph/[feature-name-kebab-case]",
  "description": "[Short description]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [role], I want [outcome] so that [benefit].",
      "type": "discovery | experiment | evaluation | implementation | ops",
      "hypothesis": "[Optional hypothesis]",
      "evidenceRequired": "[Required evidence to log]",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2",
        "Ruff check passes",
        "Ruff format passes",
        "Mypy passes",
        "Pytest passes (if tests exist)",
        "Evidence logged in progress.jsonl"
      ],
      "priority": 1,
      "passes": false,
      "notes": "",
      "supersededBy": "",
      "risk": ""
    }
  ]
}
```

---

## Story Size: The Number One Rule

Each story must be completable in **one iteration**. If you cannot describe the change in 2-3 sentences, split it.

---

## Story Ordering: Dependencies First

Order stories so earlier ones unlock later ones:
1. Discovery/evaluation scaffolding
2. Baseline experiments
3. Improvements and analysis
4. Operationalization

---

## Acceptance Criteria Rules

- Criteria must be verifiable.
- **Always include** Ruff/Mypy/Pytest checks and evidence logging.
- For experiment stories, include the specific metric and logging requirement, including W&B run URL/ID.

---

## Conversion Rules

1. Each user story becomes one JSON entry
2. IDs sequential: US-001, US-002, ...
3. `priority` orders execution
4. `passes: false` for all
5. `supersededBy` empty string for all
6. `branchName` must start with `ml-ralph/`

---

## Dynamic Backlog Note

ML-Ralph refines `prd.json` every iteration based on evidence. This is expected and part of the loop. Do not attempt to “lock” the backlog.
