---
name: blueprint-discovery
description: Discovery phase for blueprint workflow - interview triggers, acceptance criteria, and feature classification
---

# Blueprint Discovery

Handles Steps 1-3 of the blueprint workflow: Interview decision, Acceptance Criteria gathering, and Feature Classification.

## Input

```yaml
feature_description: string  # Raw feature description from user
```

## 1. Interview Decision

**Suggest interview when:**
- Feature description < 2 sentences
- Contains uncertainty words: "maybe", "probably", "something like", "not sure"
- Involves multiple stakeholders or systems
- User seems uncertain

**Skip interview for:**
- Bug fixes with clear reproduction steps
- Small, well-defined tasks (< 3 files likely)
- Features with existing specs/PRDs referenced

**If interview suggested:**
```
AskUserQuestion:
  question: "This feature could benefit from a requirements interview. Explore in depth first?"
  options:
    - "Yes, interview me first" → Invoke /majestic:interview with feature_description
    - "No, proceed to planning" → Continue
```

## 2. Acceptance Criteria

**MANDATORY: Ask what "done" means.**

AC describes feature behaviors only. Quality gates (tests, lint, review) handled by other agents.

```
AskUserQuestion:
  question: "What behavior must work for this feature to be done?"
  header: "Done when"
  multiSelect: true
  options:
    - label: "User can perform action"
      description: "Feature enables a specific user action"
    - label: "System responds correctly"
      description: "API/backend behaves as expected"
    - label: "UI displays properly"
      description: "Visual elements render correctly"
    - label: "Data is persisted"
      description: "Changes are saved to database"
```

**Good AC examples:**
- "Authenticated user can login and redirect to dashboard"
- "Form validates email format before submission"
- "API returns 404 for non-existent resources"

**Bad AC examples (handled elsewhere):**
- "Tests pass" → always-works-verifier
- "Code reviewed" → quality-gate
- "No lint errors" → slop-remover

**Capture verification method for each criterion:**

| Criterion | Verification |
|-----------|--------------|
| User can login | `curl -X POST /login` or manual |
| Form validates | `rspec spec/features/signup_spec.rb` |
| API returns 404 | `curl /api/nonexistent` |

## 3. Feature Classification

| Type | Detection Keywords | Action |
|------|-------------------|--------|
| **UI** | page, component, form, button, modal, design, view, template | Check design system |
| **DevOps** | terraform, ansible, infrastructure, cloud, docker, deploy, server | Delegate to devops-plan |
| **API** | endpoint, route, controller, request, response, REST, GraphQL | Standard flow |
| **Data** | migration, model, schema, database, query | Standard flow |

**UI Feature Flow:**
1. Read config: `/majestic:config design_system_path`
2. If empty, check: `docs/design/design-system.md`
3. If no design system: Suggest `/majestic:ux-brief` first

**DevOps Feature Flow:**
```
Skill(skill: "majestic-devops:devops-plan")
```

## Output

```yaml
discovery_result:
  interview_conducted: boolean
  interview_output: string | null  # If interview was run
  acceptance_criteria:
    - criterion: string
      verification: string
  feature_type: "ui" | "devops" | "api" | "data" | "general"
  design_system_path: string | null  # For UI features
  ready_for_research: boolean
```
