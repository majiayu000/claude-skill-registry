---
name: bootstrap-template-evaluation
description: Fastest route to a deployed live evaluation using a pre-built Truesight template. Use when the user wants a quick start without building judgment configs from scratch.
---

# Bootstrap Template Evaluation

Use this skill when a pre-built template likely covers the target use case.

## Interactive Q&A protocol (mandatory)

<HARD-GATE>
BEFORE the first scoping question, search for a structured question tool (e.g., `AskUserQuestion` or similar interactive widget) and load it. Use that tool for EVERY scoping question. Fall back to plain-text lettered options ONLY if no such tool exists in the environment.
</HARD-GATE>

If template choice is ambiguous, ask one question at a time using the structured question tool (loaded per the HARD-GATE above).

Example question structure:

```
Which template family best matches your goal?
A) AI writing detection
B) Code quality
C) Unsure, list all templates first
```

Rules:
- Ask one question per message.
- Use the structured question tool for every question. Structure each with a short header, 2-4 options with labels and descriptions, and place the recommended option first. Do not add "(Recommended)" or similar annotations to option labels.
- Ask one follow-up only when needed.

## Workflow

1. Discover templates:
   - Call `list_templates`.
2. Select template:
   - Match use case to template `slug`.
3. Provision private dataset:
   - Call `provision_template(slug)`.
4. Deploy live evaluation:
   - Call `create_and_deploy_evaluation(dataset_id)`.
   - Capture `api_key` immediately because it is returned only once.
5. Verify:
   - Run `run_eval` with representative inputs.
6. Return deployment artifacts:
   - `dataset_id`
   - `live_evaluation_id`
   - verification result

## Guardrails

- If no template fits, hand off to `create-evaluation`.
- Do not skip verification after deployment.

## Scopes reference

- `list_templates` requires `datasets:read`
- `provision_template` requires `datasets:write`
- `create_and_deploy_evaluation` requires `evaluations:write`, `live-evaluations:write`
- `run_eval` requires `live-evaluations:execute`
