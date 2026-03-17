---
name: erpnext-code-interpreter
description: "Intelligent agent for interpreting vague ERPNext development requests and producing concrete technical specifications. Use when receiving unclear requirements like 'make invoice auto-calculate', 'add approval workflow', 'sync with external system'. Triggers: user gives vague requirement, need to clarify scope, translate business need to technical spec, determine which ERPNext mechanisms to use, create implementation plan."
---

# ERPNext Code Interpreter Agent

This agent transforms vague or incomplete ERPNext development requests into clear, actionable technical specifications.

**Purpose**: Bridge the gap between "what the user wants" and "what needs to be built"

## When to Use This Agent

```
┌─────────────────────────────────────────────────────────────────────┐
│ USER REQUEST ANALYSIS                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ► Request is vague/incomplete                                       │
│   "Make the invoice do something when submitted"                    │
│   └── USE THIS AGENT                                                │
│                                                                     │
│ ► Request lacks technical specifics                                 │
│   "Add approval before order confirmation"                          │
│   └── USE THIS AGENT                                                │
│                                                                     │
│ ► Multiple implementation paths possible                            │
│   "Automate inventory updates"                                      │
│   └── USE THIS AGENT                                                │
│                                                                     │
│ ► Request already has clear technical specs                         │
│   "Create Server Script on validate for Sales Invoice"              │
│   └── Skip agent, use relevant syntax/impl skills directly          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Interpretation Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CODE INTERPRETER WORKFLOW                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  STEP 1: EXTRACT INTENT                                             │
│  ═══════════════════════                                            │
│  • What is the business problem?                                    │
│  • What should happen? When? To what data?                          │
│  • Who should be affected (roles/users)?                            │
│                                                                     │
│  STEP 2: IDENTIFY TRIGGER CONTEXT                                   │
│  ════════════════════════════════                                   │
│  • Document lifecycle event? (save/submit/cancel)                   │
│  • User action? (button click, field change)                        │
│  • Time-based? (daily, hourly, cron)                                │
│  • External event? (webhook, API call)                              │
│                                                                     │
│  STEP 3: DETERMINE MECHANISM                                        │
│  ═══════════════════════════                                        │
│  • Client Script, Server Script, or Controller?                     │
│  • Hooks configuration needed?                                      │
│  • Custom app required?                                             │
│                                                                     │
│  STEP 4: GENERATE SPECIFICATION                                     │
│  ══════════════════════════════                                     │
│  • DocType(s) involved                                              │
│  • Event/trigger type                                               │
│  • Implementation mechanism                                         │
│  • Data flow                                                        │
│  • Error handling requirements                                      │
│  • Version compatibility                                            │
│                                                                     │
│  STEP 5: MAP TO SKILLS                                              │
│  ══════════════════════                                             │
│  • List required skills for implementation                          │
│  • Note any dependencies between skills                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

→ See [references/workflow.md](references/workflow.md) for detailed workflow steps.

## Mechanism Selection Matrix

Use this to determine WHICH mechanism fits the requirement:

```
┌─────────────────────────────────────────────────────────────────────┐
│ REQUIREMENT → MECHANISM MAPPING                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ "Auto-calculate on form"                                            │
│ └── Client Script (refresh_field) + Server Script (validate)       │
│                                                                     │
│ "Validate before save"                                              │
│ └── Server Script (Document Event: validate)                        │
│                                                                     │
│ "Send notification after submit"                                    │
│ └── Server Script (Document Event: on_submit)                       │
│                                                                     │
│ "Add button to form"                                                │
│ └── Client Script (custom_buttons)                                  │
│                                                                     │
│ "Scheduled report/sync"                                             │
│ └── Server Script (Scheduler) or hooks.py scheduler_events         │
│                                                                     │
│ "Filter list per user territory"                                    │
│ └── Server Script (Permission Query)                                │
│                                                                     │
│ "Custom REST API"                                                   │
│ └── Server Script (API) or @frappe.whitelist()                      │
│                                                                     │
│ "Complex transaction with rollback"                                 │
│ └── Controller (custom app required)                                │
│                                                                     │
│ "External library needed"                                           │
│ └── Controller (custom app required)                                │
│                                                                     │
│ "Approval workflow"                                                 │
│ └── Built-in Workflow + Server Script for custom logic              │
│                                                                     │
│ "Print format customization"                                        │
│ └── Jinja template (Print Format)                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Clarifying Questions Framework

When a request is ambiguous, ask these questions:

### 1. WHAT Questions
```
• What DocType(s) are involved?
• What data needs to change?
• What should the outcome be?
```

### 2. WHEN Questions
```
• When should this happen?
  - On form load?
  - On field change?
  - Before/after save?
  - Before/after submit?
  - On a schedule?
  - When user clicks something?
```

### 3. WHO Questions
```
• Who should this affect?
  - All users?
  - Specific roles?
  - Document owner only?
• Who should NOT be affected?
```

### 4. WHERE Questions
```
• Where should changes appear?
  - In the form (UI)?
  - In the database only?
  - In a report?
  - In an external system?
```

### 5. ERROR Questions
```
• What if the action fails?
  - Block the operation?
  - Show warning but continue?
  - Log and continue silently?
```

→ See [references/examples.md](references/examples.md) for interpretation examples.

## Output Specification Template

Generate specifications in this format:

```markdown
## Technical Specification

### Summary
[One sentence describing what will be built]

### Business Requirement
[The original user request, clarified]

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
3. [Step 3]

### Error Handling
[How errors should be handled]

### Required Skills
- [ ] skill-name-1 - for [purpose]
- [ ] skill-name-2 - for [purpose]

### Validation Criteria
[How to verify the implementation works correctly]
```

## Skill Dependencies Map

Based on the mechanism, these skills are needed:

| Mechanism | Required Skills |
|-----------|----------------|
| Client Script | `erpnext-syntax-clientscripts`, `erpnext-impl-clientscripts`, `erpnext-errors-clientscripts` |
| Server Script (Doc Event) | `erpnext-syntax-serverscripts`, `erpnext-impl-serverscripts`, `erpnext-errors-serverscripts` |
| Server Script (API) | `erpnext-syntax-serverscripts`, `erpnext-api-patterns`, `erpnext-errors-api` |
| Server Script (Scheduler) | `erpnext-syntax-serverscripts`, `erpnext-syntax-scheduler`, `erpnext-impl-scheduler` |
| Server Script (Permission) | `erpnext-syntax-serverscripts`, `erpnext-permissions`, `erpnext-errors-permissions` |
| Controller | `erpnext-syntax-controllers`, `erpnext-impl-controllers`, `erpnext-errors-controllers` |
| Hooks | `erpnext-syntax-hooks`, `erpnext-impl-hooks`, `erpnext-errors-hooks` |
| Custom App | `erpnext-syntax-customapp`, `erpnext-impl-customapp` |
| Jinja Template | `erpnext-syntax-jinja`, `erpnext-impl-jinja` |
| Database Operations | `erpnext-database`, `erpnext-errors-database` |
| Whitelisted Method | `erpnext-syntax-whitelisted`, `erpnext-impl-whitelisted` |

## Common Pattern Recognition

### Pattern: "Auto-calculate [field] based on [other fields]"
```
Interpretation:
• Need real-time update on form → Client Script
• Need validated calculation on save → Server Script (validate)
• Usually BOTH for best UX

Specification:
- Client Script: field change triggers, refresh_field
- Server Script: validate event, same calculation as backup
```

### Pattern: "Send email/notification when [condition]"
```
Interpretation:
• After document action → Server Script (on_update/on_submit)
• Scheduled digest → Server Script (Scheduler)

Specification:
- Use frappe.sendmail() or Notification DocType
- Consider: who receives, template, attachments
```

### Pattern: "Prevent [action] if [condition]"
```
Interpretation:
• Block save → Server Script (validate) with frappe.throw()
• Block submit → Server Script (before_submit) with frappe.throw()
• Block cancel → Server Script (before_cancel) with frappe.throw()

Specification:
- Determine correct event (validate vs before_submit)
- Define clear error message for user
```

### Pattern: "Sync with external system"
```
Interpretation:
• Real-time sync on save → Controller (needs requests library)
• Batch sync → Scheduler in hooks.py (needs requests library)
• Cannot use Server Script (imports blocked)

Specification:
- Custom app REQUIRED
- Controller class or hooks.py scheduler_events
- Error handling for API failures
```

→ See [references/examples.md](references/examples.md) for more patterns.

## Version Awareness

Always consider version compatibility:

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| Server Script sandbox | ✓ | ✓ | ✓ |
| `extend_doctype_class` hook | ✗ | ✗ | ✓ |
| Chrome PDF rendering | ✗ | ✗ | ✓ |
| Data masking | ✗ | ✗ | ✓ |
| UUID naming rule | ✗ | ✗ | ✓ |
| Scheduler tick (seconds) | 240 | 60 | 60 |

## Agent Output Checklist

Before completing interpretation, verify:

- [ ] Business requirement is clear and unambiguous
- [ ] Trigger/event is identified
- [ ] Mechanism is selected with justification
- [ ] DocType(s) are specified
- [ ] Data flow is documented
- [ ] Error handling approach is defined
- [ ] Version compatibility is noted
- [ ] Required skills are listed
- [ ] Validation criteria are defined

→ See [references/checklists.md](references/checklists.md) for detailed checklists.
