---
name: blueprint-discovery
description: Discovery phase for blueprint workflow - interview triggers, acceptance criteria, and feature classification
---

# Blueprint Discovery

Handles Steps 1-5 of the blueprint workflow: Idea Refinement, Research Decision Signals, Interview decision, Acceptance Criteria gathering, and Feature Classification.

## Input

```yaml
feature_description: string  # Raw feature description from user
```

## 1. Idea Refinement

Quick clarification before deep discovery. Catches misunderstandings early with 1-3 targeted questions.

**Trigger when:**
- `feature_description` < 100 characters
- Contains uncertainty: "maybe", "probably", "something like", "I think", "not sure"
- Missing core elements: no clear action verb OR no clear subject

**Skip when:**
- Description is detailed (> 200 characters with clear intent)
- User says "proceed" or "skip refinement"
- Bug fix with reproduction steps

**If triggered:**

```
AskUserQuestion:
  question: "Quick check - what's the primary goal?"
  header: "Goal"
  options:
    - label: "Add new capability"
      description: "Feature that doesn't exist yet"
    - label: "Fix broken behavior"
      description: "Something that should work but doesn't"
    - label: "Improve existing feature"
      description: "Enhancement to current functionality"
    - label: "Refactor/cleanup"
      description: "Better code without behavior change"
```

**Follow-up (if answer reveals gaps):**

```
If goal == "Add new capability":
  AskUserQuestion:
    question: "Who will use this and when?"
    header: "Context"
    options:
      - label: "End users in the app"
      - label: "Admins/internal team"
      - label: "Developers/API consumers"
      - label: "Automated systems"

If goal == "Fix broken behavior":
  AskUserQuestion:
    question: "How does it fail?"
    header: "Symptom"
    options:
      - label: "Error/crash"
      - label: "Wrong output"
      - label: "Missing data"
      - label: "Performance issue"
```

**Max 3 questions total.** After refinement:

```
refined_description = original + goal + context/symptom (if asked)
```

**Output skip offer:**
> "Got it: {refined_description}. Ready to proceed, or clarify further?"

## 2. Research Decision Signals

During refinement, gather signals to inform the research decision in blueprint-research.

**Infer from conversation:**

| Signal | How to Detect |
|--------|---------------|
| `user_familiarity` | Points to existing code examples? Knows where files live? → `high` |
| `user_intent` | "Quick fix", "ship today" → `speed` / "want it right", "research first" → `thoroughness` |
| `topic_risk` | Keywords: auth, payment, stripe, security, encrypt, API key, webhook → `high` |
| `uncertainty_level` | "Not sure how", "what's the best way", exploring options → `high` |

**If signals unclear, quick probe:**

```
AskUserQuestion:
  question: "What matters more for this task?"
  header: "Priority"
  options:
    - label: "Get it done fast"
      description: "Good enough solution, ship quickly"
    - label: "Get it done right"
      description: "Research best practices first"
```

**Store signals for research phase.**

## 3. Interview Decision

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

## 4. Acceptance Criteria

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

## 5. Feature Classification

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
  refined_description: string  # Original + refinement context
  refinement_skipped: boolean
  interview_conducted: boolean
  interview_output: string | null  # If interview was run
  acceptance_criteria:
    - criterion: string
      verification: string
  feature_type: "ui" | "devops" | "api" | "data" | "general"
  design_system_path: string | null  # For UI features
  # Research decision signals (for blueprint-research)
  user_familiarity: high | medium | low
  user_intent: speed | thoroughness
  topic_risk: high | medium | low
  uncertainty_level: high | medium | low
  ready_for_research: boolean
```
