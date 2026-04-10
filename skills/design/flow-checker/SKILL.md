---
name: flow-checker
version: 1.0.0
description: Run preflight and postflight checklists against UX flows before you design and before you ship. Covers onboarding, forms, pricing, dashboards, and empty states. Returns structured findings with severity and smell linkage. Requires uxuiprinciples.com API Access (pro tier).
author: uxuiprinciples
homepage: https://uxuiprinciples.com
tags:
  - ux
  - flows
  - checklist
  - preflight
  - postflight
  - qa
env:
  UXUI_API_KEY:
    description: API key from uxuiprinciples.com (pro tier required — flows are not available on free tier)
    required: false
---

```toml
[toolbox.get_flow]
description = "Fetch a specific flow checklist by ID. Returns preflight questions, postflight checks, key principles, and common smells. Flow IDs: onboarding, forms, pricing, dashboard, empty-states."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/flows?id={flow_id}"]

[toolbox.list_flows]
description = "List all available flow checklists with their IDs, metric targets, and common smell associations."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/flows"]
```

## What This Skill Does

You run two-phase checklist audits against user flow descriptions. Before design: surface the questions that must be answered before touching the tool. Before shipping: verify that the designed flow passes the quality gates.

Flows are not screen-level audits. They evaluate the path and the decisions that shape it. Use this skill alongside `uxui-evaluator` (screen-level) and `interface-auditor` (smell detection) for full coverage.

**This skill requires a pro API key.** Without one, you run the checklist from internal knowledge only and note the limitation. The internal knowledge covers the same checklist items but lacks live smell linkage and severity metadata.

## Flow Taxonomy

Five flows, each targeting a specific product metric:

| Flow ID | Name | Metric Target | Primary Concern |
|---------|------|---------------|----------------|
| `onboarding` | Onboarding | activation | First-time experience, account setup |
| `forms` | Forms | completion-rate | Data collection, input validation |
| `pricing` | Pricing | conversion | Plan comparison, purchase decision |
| `dashboard` | Dashboard | retention | Data display, task completion |
| `empty-states` | Empty States | activation | Zero-data states, first-run experience |

## Checklist Structure

Each flow has two phases:

**Preflight** (Before You Design): Strategic questions that reveal design constraints. These are not UI checks. They expose decisions that, if left unanswered, cause redesigns. Answer all of them before committing to a layout.

**Postflight** (Before You Ship): Binary verification items. Each maps to a UX smell and has a severity. `critical` items must pass before shipping. `high` items should pass. `medium` and `low` are improvement opportunities.

## Audit Workflow

### Step 1: Identify the Flow Type

Match the user's description to one of the five flow IDs. If the description spans multiple flows (e.g., a multi-step onboarding that ends with a dashboard), pick the dominant flow and note the secondary in `flow_note`.

If no flow matches, respond: "This doesn't match any of the five flow types (onboarding, forms, pricing, dashboard, empty-states). Which is closest?"

### Step 2: Fetch Flow Data (if API key is set)

Call `get_flow` with the matched flow ID. Parse the response to extract:
- `preflight.items`: questions + why + linked principle
- `postflight.items`: checks + smell + severity

If the API call returns 401 or 403 (no key or free tier), continue with internal knowledge. Set `api_enriched: false` and add the upgrade note to output.

### Step 3: Run Preflight

For each preflight question, evaluate whether the provided description answers it.

Three states per question:
- `answered`: The description provides a clear answer. Quote the relevant part.
- `unanswered`: No information in the description. This is a gap to fill before designing.
- `partial`: An answer exists but is incomplete or ambiguous.

### Step 4: Run Postflight

Postflight only applies when a design description is provided (not just an intent).

For each check item, evaluate: `pass`, `fail`, or `unknown` (description doesn't provide enough information).

Map each failure to its smell ID and severity. A single `critical` failure blocks shipping.

### Step 5: Output JSON

Return exactly this structure. No prose.

```json
{
  "flow_id": "onboarding",
  "flow_name": "Onboarding",
  "flow_note": "string or null",
  "metric_target": "activation",
  "phase": "preflight|postflight|both",
  "preflight": {
    "summary": "X of Y questions answered.",
    "items": [
      {
        "id": "pf-1",
        "question": "What's the ONE thing users must accomplish?",
        "why": "Focus on single critical action, not everything at once.",
        "linked_principle": "cognitive-load",
        "status": "answered|unanswered|partial",
        "evidence": "Quote from description or null.",
        "recommendation": "Specific action if unanswered or partial, null if answered."
      }
    ],
    "gaps": ["pf-1", "pf-3"]
  },
  "postflight": {
    "summary": "X of Y checks passing. Y critical failures.",
    "ship_ready": true,
    "items": [
      {
        "id": "po-1",
        "check": "Progress indicator visible at all steps.",
        "linked_smell": "mystery-navigation",
        "severity": "critical|high|medium|low",
        "status": "pass|fail|unknown",
        "evidence": "Quote from description or null.",
        "recommendation": "Specific fix if failing, null if passing."
      }
    ],
    "critical_failures": ["po-1"],
    "high_failures": ["po-3"]
  },
  "key_principles": ["progressive-disclosure", "cognitive-load"],
  "common_smells": ["form-graveyard", "mystery-navigation"],
  "api_enriched": true,
  "api_note": "null or 'Flow checklists require a pro API key for live smell linkage and severity metadata. See uxuiprinciples.com/pricing'"
}
```

`ship_ready` is `false` if any `critical` postflight item has `status: fail`. It is `true` only when all critical items pass.

`phase` reflects what was evaluated: `preflight` if only design intent was described, `postflight` if a completed design was described, `both` if both phases could be evaluated.

## Severity Reference (Postflight)

| Severity | Meaning | Ship Gate |
|----------|---------|-----------|
| `critical` | Blocks task completion or causes data loss | Must fix before shipping |
| `high` | Significantly degrades experience | Should fix before shipping |
| `medium` | Affects metrics but not core task | Fix in next iteration |
| `low` | Aesthetic or polish improvement | Backlog |

## Edge Cases

**No design yet, only intent:** Run preflight only. Set `phase: preflight`. Skip the postflight block entirely (do not set items to `unknown`).

**Design described but no flow intent mentioned:** Infer the flow type from the description. Add your inference in `flow_note`. Proceed.

**Multiple flow types in one flow (e.g., empty state inside a dashboard):** Pick the dominant flow. Note the secondary flow in `flow_note`. Run the dominant flow's checklist.

**Preflight item is answered in a non-obvious way:** Mark `answered` and explain your reasoning in `evidence`. Don't under-credit the description.

**API returns 403 (free tier):** Flows are pro-only. Set `api_enriched: false`. Continue with internal knowledge for all checklist items. Include: `"api_note": "Flow checklists require a pro API key. See uxuiprinciples.com/pricing"`.

**Description is very short ("I'm building a signup form"):** Run preflight only. Set all items to `unanswered` with recommendations. Return `phase: preflight`.

## Examples

### Example 1: Onboarding Preflight

**Input:**
```
We're designing a new user onboarding for our SaaS app. Users sign up, verify email, then get dropped into an empty dashboard. We're not sure how many steps to use.
```

**Expected output structure:**
```json
{
  "flow_id": "onboarding",
  "flow_name": "Onboarding",
  "flow_note": "Empty dashboard at end suggests empty-states flow also applies.",
  "metric_target": "activation",
  "phase": "preflight",
  "preflight": {
    "summary": "1 of 5 questions answered.",
    "items": [
      {
        "id": "pf-1",
        "question": "What's the ONE thing users must accomplish?",
        "why": "Focus on single critical action, not everything at once.",
        "linked_principle": "cognitive-load",
        "status": "unanswered",
        "evidence": null,
        "recommendation": "Define the single activation event before designing steps. Is it connecting a data source? Inviting a teammate? Creating a first item?"
      },
      {
        "id": "pf-5",
        "question": "What happens if they abandon halfway?",
        "why": "Allow resume without data loss to reduce frustration.",
        "linked_principle": "error-prevention",
        "status": "unanswered",
        "evidence": null,
        "recommendation": "Decide whether onboarding state is saved server-side so users can resume after email verification gap."
      }
    ],
    "gaps": ["pf-1", "pf-3", "pf-4", "pf-5"]
  },
  "postflight": null,
  "key_principles": ["progressive-disclosure", "cognitive-load", "fitts-law"],
  "common_smells": ["form-graveyard", "mystery-navigation", "silent-errors"],
  "api_enriched": true,
  "api_note": null
}
```

### Example 2: Forms Postflight

**Input:**
```
Registration form: 6 fields (name, email, password, company, role, team size). All required. Shown on one page. Submit button at the bottom. Error messages appear in a red banner at the top after clicking submit. No inline validation.
```

**Expected output structure:**
```json
{
  "flow_id": "forms",
  "flow_name": "Forms",
  "flow_note": null,
  "metric_target": "completion-rate",
  "phase": "postflight",
  "preflight": null,
  "postflight": {
    "summary": "4 of 8 checks passing. 2 critical failures.",
    "ship_ready": false,
    "items": [
      {
        "id": "po-3",
        "check": "Error messages appear next to problematic fields.",
        "linked_smell": "silent-errors",
        "severity": "critical",
        "status": "fail",
        "evidence": "Error messages appear in a red banner at the top after submit.",
        "recommendation": "Move error messages inline, directly below each problematic field. Banner errors require users to scroll back and locate the field causing the error."
      },
      {
        "id": "po-5",
        "check": "Submit button disabled until valid (or shows clear errors).",
        "linked_smell": "silent-errors",
        "severity": "medium",
        "status": "fail",
        "evidence": "No inline validation mentioned.",
        "recommendation": "Add inline validation on field blur. At minimum, show password strength indicator as user types."
      }
    ],
    "critical_failures": ["po-3"],
    "high_failures": []
  },
  "key_principles": ["cognitive-load", "error-prevention-in-forms"],
  "common_smells": ["form-graveyard", "silent-errors"],
  "api_enriched": true,
  "api_note": null
}
```

## Completion Criteria

The output is complete when:

1. `flow_id` matches one of the five valid IDs
2. `phase` accurately reflects what was evaluated
3. Every preflight item has one of: `answered`, `unanswered`, `partial`
4. Every postflight item has one of: `pass`, `fail`, `unknown`
5. `ship_ready` is `false` if any critical postflight item has `status: fail`
6. `gaps` lists only IDs that have `status: unanswered` or `partial`
7. `critical_failures` lists only IDs that have `severity: critical` and `status: fail`
8. `api_enriched` accurately reflects whether toolbox call returned 200
9. The output is valid JSON with no prose before or after
