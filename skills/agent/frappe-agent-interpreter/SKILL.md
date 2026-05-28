---
name: frappe-agent-interpreter
description: >
  Use when receiving vague or unclear ERPNext/Frappe development requests
  that need interpretation. Transforms requirements like 'make invoice
  auto-calculate' or 'add approval workflow' into concrete technical
  specifications. Determines which Frappe mechanisms to use and maps to
  the full 60-skill catalog. Keywords: vague requirement, clarify scope,
  translate business need, technical spec, implementation plan.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Code Interpreter Agent

Transforms vague or incomplete Frappe/ERPNext development requests into clear, actionable technical specifications mapped to the full 60-skill catalog.

**Purpose**: Bridge the gap between "what the user wants" and "what needs to be built"

## When to Use This Agent

```
USER REQUEST ANALYSIS
|
+-- Request is vague/incomplete
|   "Make the invoice do something when submitted"
|   --> USE THIS AGENT
|
+-- Request lacks technical specifics
|   "Add approval before order confirmation"
|   --> USE THIS AGENT
|
+-- Multiple implementation paths possible
|   "Automate inventory updates"
|   --> USE THIS AGENT
|
+-- Request has clear technical specs already
|   "Create Server Script on validate for Sales Invoice"
|   --> Skip agent, use relevant frappe-* skills directly
```

## Interpretation Workflow

```
STEP 1: EXTRACT INTENT
  - What is the business problem?
  - What should happen? When? To what data?
  - Who should be affected (roles/users)?

STEP 2: IDENTIFY TRIGGER CONTEXT
  - Document lifecycle event? (save/submit/cancel)
  - User action? (button click, field change)
  - Time-based? (daily, hourly, cron)
  - External event? (webhook, API call)

STEP 3: DETERMINE MECHANISM
  - Client Script, Server Script, or Controller?
  - Hooks configuration needed?
  - Custom app required?
  - v16 extend_doctype_class applicable?

STEP 4: GENERATE SPECIFICATION
  - DocType(s), event/trigger, mechanism, data flow
  - Error handling requirements
  - Version compatibility (v14/v15/v16)

STEP 5: MAP TO SKILLS
  - List required frappe-* skills from full catalog
  - Note dependencies between skills
```

See [references/workflow.md](references/workflow.md) for detailed steps.

## Mechanism Selection Matrix

| Requirement Pattern | Mechanism | Custom App? |
|---------------------|-----------|:-----------:|
| "Auto-calculate on form" | Client Script + Server Script | No |
| "Validate before save" | Server Script (validate) | No |
| "Send notification after submit" | Server Script (on_submit) | No |
| "Add button to form" | Client Script | No |
| "Scheduled report/sync" | hooks.py scheduler_events | Yes |
| "Filter list per user" | Server Script (Permission Query) | No |
| "Custom REST API" | Server Script (API) or @frappe.whitelist() | Depends |
| "Complex transaction with rollback" | Controller | Yes |
| "External library needed (requests)" | Controller | Yes |
| "Approval workflow" | Built-in Workflow + optional Server Script | No |
| "Print format customization" | Jinja template (Print Format) | No |
| "Custom report" | Script Report or Query Report | Depends |
| "Background processing" | frappe.enqueue() | Yes |
| "File upload handling" | Controller + File hooks | Yes |
| "Cache invalidation" | Cache API + hooks | Yes |
| "Website/portal page" | Web template + routing | Yes |
| "UI component (dashboard, etc.)" | Page or Custom Page | Yes |

## Clarifying Questions Framework

### 1. WHAT Questions
- What DocType(s) are involved?
- What data needs to change?
- What should the outcome be?

### 2. WHEN Questions
- On form load? On field change? Before/after save?
- Before/after submit? On a schedule? Button click?

### 3. WHO Questions
- All users? Specific roles? Document owner only?

### 4. WHERE Questions
- In the form (UI)? Database only? Report? External system?

### 5. ERROR Questions
- Block the operation? Show warning? Log silently?

### 6. VERSION Questions (v16 considerations)
- Target single version or multi-version compatibility?
- Can we use `extend_doctype_class` (v16) or need `doc_events` (v14+)?
- Type annotations desired? (v16 best practice)

## Output Specification Template

ALWAYS generate specifications in this format:

```markdown
## Technical Specification

### Summary
[One sentence describing what will be built]

### Business Requirement
[Original user request, clarified]

### Implementation

| Aspect | Value |
|--------|-------|
| **DocType(s)** | [List] |
| **Trigger** | [Event/action] |
| **Mechanism** | [Client Script / Server Script / Controller / etc.] |
| **Version** | [v14 / v15 / v16 / all] |

### Data Flow
1. [Step 1]
2. [Step 2]

### Error Handling
[Strategy]

### Required Skills
- [ ] frappe-skill-name - for [purpose]

### Validation Criteria
[How to verify it works]
```

## Complete Skill Catalog (60 skills)

### Syntax Layer (11 skills)
| Skill | Use For |
|-------|---------|
| `frappe-syntax-clientscripts` | Client Script JS syntax |
| `frappe-syntax-serverscripts` | Server Script Python sandbox syntax |
| `frappe-syntax-controllers` | Controller class syntax |
| `frappe-syntax-hooks` | hooks.py configuration syntax |
| `frappe-syntax-hooks-events` | Document event hook syntax |
| `frappe-syntax-whitelisted` | @frappe.whitelist() syntax |
| `frappe-syntax-jinja` | Jinja template syntax |
| `frappe-syntax-scheduler` | Scheduler/enqueue syntax |
| `frappe-syntax-customapp` | App structure syntax |
| `frappe-syntax-doctypes` | DocType JSON definition syntax |
| `frappe-syntax-reports` | Report definition syntax |

### Core Layer (7 skills)
| Skill | Use For |
|-------|---------|
| `frappe-core-database` | Database operations, ORM, raw SQL |
| `frappe-core-permissions` | Permission system, roles, rules |
| `frappe-core-api` | REST API, resource API |
| `frappe-core-workflow` | Workflow engine, states, transitions |
| `frappe-core-notifications` | Email, push, system notifications |
| `frappe-core-files` | File upload, attachment, storage |
| `frappe-core-cache` | Redis cache, cache invalidation |

### Implementation Layer (12 skills)
| Skill | Use For |
|-------|---------|
| `frappe-impl-clientscripts` | Client Script implementation patterns |
| `frappe-impl-serverscripts` | Server Script implementation patterns |
| `frappe-impl-controllers` | Controller implementation patterns |
| `frappe-impl-hooks` | Hook implementation patterns |
| `frappe-impl-whitelisted` | Whitelisted method patterns |
| `frappe-impl-jinja` | Jinja template patterns |
| `frappe-impl-scheduler` | Scheduled task/background job patterns |
| `frappe-impl-customapp` | Custom app development workflow |
| `frappe-impl-reports` | Report building patterns |
| `frappe-impl-workflow` | Workflow implementation patterns |
| `frappe-impl-website` | Website/portal development |
| `frappe-impl-ui-components` | UI component patterns |
| `frappe-impl-integrations` | External system integration |

### Error Layer (7 skills)
| Skill | Use For |
|-------|---------|
| `frappe-errors-clientscripts` | Client Script error patterns |
| `frappe-errors-serverscripts` | Server Script error patterns |
| `frappe-errors-controllers` | Controller error patterns |
| `frappe-errors-hooks` | Hook error patterns |
| `frappe-errors-api` | API error patterns |
| `frappe-errors-permissions` | Permission error patterns |
| `frappe-errors-database` | Database error patterns |

### Ops Layer (8 skills)
| Skill | Use For |
|-------|---------|
| `frappe-ops-bench` | Bench CLI commands |
| `frappe-ops-deployment` | Production deployment |
| `frappe-ops-backup` | Backup and restore |
| `frappe-ops-performance` | Performance tuning |
| `frappe-ops-upgrades` | Version upgrade procedures |
| `frappe-ops-cloud` | Cloud hosting (FC, AWS, etc.) |
| `frappe-ops-app-lifecycle` | App versioning and releases |
| `frappe-ops-frontend-build` | Frontend asset building |

### Testing Layer (2 skills)
| Skill | Use For |
|-------|---------|
| `frappe-testing-unit` | Unit and integration tests |
| `frappe-testing-cicd` | CI/CD pipeline setup |

### Agent Layer (5 skills)
| Skill | Use For |
|-------|---------|
| `frappe-agent-interpreter` | THIS SKILL - requirement interpretation |
| `frappe-agent-validator` | Code validation before deployment |
| `frappe-agent-debugger` | Debugging Frappe issues |
| `frappe-agent-migrator` | Data migration planning |
| `frappe-agent-architect` | Architecture decision-making |

## Skill Dependencies Map

| Mechanism | Required Skills |
|-----------|----------------|
| Client Script | `frappe-syntax-clientscripts`, `frappe-impl-clientscripts`, `frappe-errors-clientscripts` |
| Server Script (Doc Event) | `frappe-syntax-serverscripts`, `frappe-impl-serverscripts`, `frappe-errors-serverscripts` |
| Server Script (API) | `frappe-syntax-serverscripts`, `frappe-core-api`, `frappe-errors-api` |
| Server Script (Scheduler) | `frappe-syntax-serverscripts`, `frappe-syntax-scheduler`, `frappe-impl-scheduler` |
| Server Script (Permission) | `frappe-syntax-serverscripts`, `frappe-core-permissions`, `frappe-errors-permissions` |
| Controller | `frappe-syntax-controllers`, `frappe-impl-controllers`, `frappe-errors-controllers` |
| Hooks | `frappe-syntax-hooks`, `frappe-impl-hooks`, `frappe-errors-hooks` |
| Custom App | `frappe-syntax-customapp`, `frappe-impl-customapp`, `frappe-ops-bench` |
| Jinja Template | `frappe-syntax-jinja`, `frappe-impl-jinja` |
| Database Operations | `frappe-core-database`, `frappe-errors-database` |
| Whitelisted Method | `frappe-syntax-whitelisted`, `frappe-impl-whitelisted` |
| Workflow | `frappe-core-workflow`, `frappe-impl-workflow` |
| Reports | `frappe-syntax-reports`, `frappe-impl-reports` |
| Website/Portal | `frappe-impl-website`, `frappe-syntax-jinja` |
| Integration | `frappe-impl-integrations`, `frappe-impl-customapp` |
| Background Jobs | `frappe-impl-scheduler`, `frappe-syntax-scheduler` |
| Testing | `frappe-testing-unit`, `frappe-testing-cicd` |
| Deployment | `frappe-ops-deployment`, `frappe-ops-bench` |

## Common Pattern Recognition

| User Phrase | Mechanism | Key Skills |
|-------------|-----------|------------|
| "auto-calculate", "automatically fill" | Client Script + Server Script | `frappe-impl-clientscripts`, `frappe-impl-serverscripts` |
| "validate", "check before save" | Server Script (validate) | `frappe-impl-serverscripts` |
| "prevent", "block", "don't allow" | Server Script + frappe.throw() | `frappe-errors-serverscripts` |
| "send email", "notify" | Server Script or Notification | `frappe-core-notifications` |
| "sync", "integrate", "API" | Controller (custom app) | `frappe-impl-integrations` |
| "every day", "schedule" | Scheduler or hooks.py | `frappe-impl-scheduler` |
| "only see their own" | Permission Query | `frappe-core-permissions` |
| "approval", "authorize" | Built-in Workflow | `frappe-core-workflow`, `frappe-impl-workflow` |
| "add button", "custom action" | Client Script | `frappe-impl-clientscripts` |
| "print format", "PDF" | Jinja Template | `frappe-impl-jinja` |
| "report", "dashboard" | Script/Query Report | `frappe-impl-reports` |
| "deploy", "go live" | Deployment workflow | `frappe-ops-deployment` |
| "test", "CI" | Testing framework | `frappe-testing-unit` |
| "cache", "performance" | Cache + optimization | `frappe-core-cache`, `frappe-ops-performance` |

## Version Awareness

ALWAYS consider version compatibility:

| Feature | v14 | v15 | v16 |
|---------|:---:|:---:|:---:|
| Server Script sandbox | Yes | Yes | Yes |
| `extend_doctype_class` | No | No | Yes |
| Chrome PDF rendering | No | No | Yes |
| Data masking | No | No | Yes |
| UUID naming rule | No | No | Yes |
| Type annotations (best practice) | No | No | Yes |
| Scheduler tick (seconds) | 240 | 60 | 60 |
| `job_id` dedup | No | Yes | Yes |

## Agent Output Checklist

Before completing interpretation, ALWAYS verify:

- [ ] Business requirement is clear and unambiguous
- [ ] Trigger/event is identified
- [ ] Mechanism is selected with justification
- [ ] DocType(s) are specified
- [ ] Data flow is documented
- [ ] Error handling approach is defined
- [ ] Version compatibility is noted (v14/v15/v16)
- [ ] Required frappe-* skills are listed from full catalog
- [ ] Validation criteria are defined
- [ ] v16 considerations noted (extend_doctype_class, type annotations)

See [references/checklists.md](references/checklists.md) for detailed checklists.
See [references/examples.md](references/examples.md) for interpretation examples.
