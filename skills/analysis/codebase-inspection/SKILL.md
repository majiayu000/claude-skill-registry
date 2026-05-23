---
name: "Codebase Inspection Protocol"
description: "Mandatory inspection before writing any Rails code. Use when: (1) Starting ANY implementation task, (2) Making architectural decisions, (3) Suggesting patterns or conventions, (4) Creating new files/classes. Core rule: Never plan without file path citations. Trigger keywords: analyze, inspect, patterns, conventions, codebase, discover, structure, dependencies, existing, before"
version: 1.1.0
---

# Codebase Inspection Protocol

**Core Rule**: "Inspect before you suggest" — No planning decisions without codebase inspection. Every recommendation must cite observed file paths.

## Inspection Decision Tree

```
What are you doing?
│
├─ Creating a new file
│   └─ Inspect: Target directory + similar existing files
│
├─ Implementing a pattern (service, component, job)
│   └─ Inspect: Existing implementations of same pattern
│
├─ Modifying existing code
│   └─ Inspect: All usages + method visibility
│
├─ Making architectural decision
│   └─ Inspect: Project structure + Gemfile + existing patterns
│
└─ Starting fresh on a project
    └─ Run FULL inspection (all sections below)
```

---

## Quick Inspection Commands

### Project Structure
```bash
tree app -L 2 -I 'assets|javascript' 2>/dev/null || find app -type d -maxdepth 2
head -60 Gemfile | grep -v '^#' | grep -v '^$'
```

### Pattern Discovery
```bash
# Services
ls app/services/*/ 2>/dev/null
head -30 $(find app/services -name '*.rb' | head -1)

# Components
ls app/components/*/ 2>/dev/null
head -40 $(find app/components -name '*_component.rb' | head -1)

# Jobs
ls app/jobs/ 2>/dev/null
head -30 $(find app/jobs -name '*.rb' | head -1)
```

### Naming Conventions
```bash
# Class/module patterns in services
grep -r 'module\|class' app/services/ --include='*.rb' | head -20
```

### Method Visibility (Critical!)
```bash
# Find method and check if after private/protected
awk '/class/,/private/' app/path/to/file.rb | grep 'def '
```

---

## NEVER Do This

**NEVER** suggest a directory structure without checking it exists:
```
# WRONG: "Let's create app/services/payments/..."
# (Never verified if app/services/ exists or follows different pattern)

# RIGHT: First run: ls app/services/*/ 2>/dev/null
# Then cite: "Following existing pattern in app/services/orders/"
```

**NEVER** recommend a pattern without finding an existing example:
```
# WRONG: "Use the Service Object pattern with .call"
# (Project might use .perform, .execute, or different pattern entirely)

# RIGHT: "Matching TasksManager::Create pattern from app/services/tasks_manager/create.rb"
```

**NEVER** assume gem availability:
```
# WRONG: "Use Sidekiq for this background job"
# (Gemfile might have delayed_job, resque, or good_job instead)

# RIGHT: Check Gemfile first, cite: "Using Sidekiq (Gemfile line 42)"
```

**NEVER** invent naming conventions:
```
# WRONG: "Call it PaymentProcessor" (when project uses PaymentService pattern)
# RIGHT: "Following *Service naming from app/services/order_service.rb"
```

---

## Inspection Output Template

After inspection, document findings before planning:

```markdown
## Inspection Findings

### Structure Observed
- Services: `app/services/{domain}/` (namespaced)
- Components: `app/components/{namespace}/` (separate templates)
- Evidence: [file path]

### Pattern in Use
- Service signature: `.call(params)` returns Result object
- Evidence: `app/services/orders/create.rb:15`

### Conventions
- Naming: `{Domain}::{Action}` (e.g., `Orders::Create`)
- Evidence: [file paths showing pattern]

### Dependencies
- Background: Sidekiq (Gemfile:42)
- Components: ViewComponent 3.x (Gemfile:28)
```

---

## When Inspection Fails

```markdown
**Inspection Limitation:**
- Unable to access: [path]
- Proceeding with assumption: [assumption]
- Risk: [what could go wrong]
- Mitigation: [how to verify later]
```

---

## Citation Requirements

Every recommendation must cite:
- **Existing patterns**: Reference specific `file:line`
- **Similar to X**: Show the actual file
- **Gem dependencies**: Quote the Gemfile line
- **Conventions**: Show example from codebase

No citations = No recommendation. Return to inspection.
