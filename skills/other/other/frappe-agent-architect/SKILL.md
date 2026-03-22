---
name: frappe-agent-architect
description: >
  Use when designing multi-app Frappe architectures, deciding whether to split functionality into separate apps, or implementing cross-app communication patterns.
  Prevents monolithic app sprawl, circular dependencies between apps, and broken override chains.
  Covers multi-app architecture decisions, app dependency management, cross-app hooks, override patterns, when to split vs extend, shared DocType strategies.
  Keywords: architecture, multi-app, app splitting, cross-app, dependencies, override, extend, monolith, modular.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Multi-App Architecture Agent

Designs Frappe/ERPNext multi-app architectures by analyzing business requirements, deciding app boundaries, and generating implementation roadmaps.

**Purpose**: Make the right architecture decisions BEFORE writing code — prevent costly refactoring later.

## When to Use This Agent

```
ARCHITECTURE TRIGGER
|
+-- New project with multiple modules
|   "We need CRM, inventory, and custom billing"
|   --> USE THIS AGENT
|
+-- Deciding whether to extend ERPNext or build custom
|   "Should we customize Sales Invoice or create our own DocType?"
|   --> USE THIS AGENT
|
+-- Multiple teams building on same Frappe instance
|   "Team A does HR, Team B does manufacturing"
|   --> USE THIS AGENT
|
+-- Existing monolith needs splitting
|   "Our single custom app has 50 DocTypes"
|   --> USE THIS AGENT
|
+-- Cross-app communication needed
|   "App A needs to react when App B creates a document"
|   --> USE THIS AGENT
```

## Architecture Workflow

```
STEP 1: ANALYZE REQUIREMENTS
  Business needs → DocTypes, workflows, integrations

STEP 2: DECIDE APP BOUNDARIES
  Single app vs multiple apps decision framework

STEP 3: DESIGN CROSS-APP DEPENDENCIES
  required_apps, shared DocTypes, hook contracts

STEP 4: DESIGN DATA MODEL
  DocTypes, relationships, naming conventions

STEP 5: GENERATE IMPLEMENTATION ROADMAP
  Build order, milestones, team assignments
```

See [references/workflow.md](references/workflow.md) for detailed steps.

## Step 1: Requirement Analysis Matrix

Map each business requirement to Frappe mechanisms:

| Requirement Type | Frappe Mechanism | Example |
|-----------------|-----------------|---------|
| Data storage | DocType | "Track customer contracts" |
| Business rules | Controller/Server Script | "Auto-calculate totals" |
| Approval flow | Workflow | "Manager must approve orders >10k" |
| Scheduled tasks | Scheduler/hooks.py | "Daily report email" |
| External sync | Integration/API | "Sync with Shopify" |
| Custom UI | Client Script/Page | "Dashboard for warehouse" |
| Reports | Script Report/Query Report | "Monthly sales by region" |
| Permissions | Role Permission | "Sales team sees own data only" |
| Print output | Print Format (Jinja) | "Custom invoice layout" |
| Portal access | Website/Portal | "Customer can view orders" |

## Step 2: App Boundary Decision Framework

### Single App — Use When

- Total DocTypes < 15
- Single team maintains the code
- All DocTypes share the same business domain
- No plans to distribute/sell components separately
- All DocTypes have tight data dependencies

### Multiple Apps — Use When

- Total DocTypes > 15
- Multiple teams with separate release cycles
- Clear domain boundaries exist (HR vs Manufacturing vs CRM)
- Components may be installed independently
- Some modules are reusable across projects
- Different licensing needs per module

### Decision Tree

```
HOW MANY DOCTYPES?
|
+-- < 15 total
|   +-- Single domain? --> SINGLE APP
|   +-- Multiple domains? --> Consider splitting
|
+-- 15-30 total
|   +-- Tight coupling between all? --> SINGLE APP (with modules)
|   +-- Clear domain boundaries? --> 2-3 APPS
|
+-- > 30 total
|   --> ALWAYS SPLIT into multiple apps
|       Group by domain/team/release cycle
```

See [references/decision-tree.md](references/decision-tree.md) for the complete decision framework.

## Step 3: Cross-App Dependency Patterns

### required_apps Declaration

ALWAYS declare dependencies explicitly in `hooks.py`:

```python
# myapp/hooks.py
required_apps = ["frappe", "erpnext"]  # NEVER omit frappe
```

### Dependency Rules

- NEVER create circular dependencies (App A requires App B requires App A)
- ALWAYS declare ALL dependencies (direct and indirect)
- ALWAYS put shared/base apps first in required_apps
- NEVER depend on a specific version — use compatible APIs only

### Dependency Diagram Pattern

```
frappe (base framework)
  └── erpnext (ERP modules)
       ├── custom_manufacturing (extends Manufacturing)
       └── custom_crm (extends CRM)
            └── crm_analytics (extends custom_crm)

RULE: Dependencies flow DOWN only. Never up, never sideways.
```

### Cross-App Communication Patterns

| Pattern | Mechanism | Use When |
|---------|-----------|----------|
| **Hook Events** | `doc_events` in hooks.py | App B reacts to App A's documents |
| **Shared DocType** | Link fields to other app's DocTypes | Apps share reference data |
| **API Call** | `frappe.call()` to whitelisted method | Loose coupling between apps |
| **Custom Fields** | `fixtures` with Custom Field | Extend another app's DocType without modifying it |
| **Override** | `extend_doctype_class` (v16) or `doc_events` | Modify another app's behavior |
| **Signals** | `frappe.publish_realtime()` | Real-time notifications between apps |

## Step 4: Data Model Design

### DocType Relationship Types

| Relationship | Implementation | Example |
|-------------|---------------|---------|
| One-to-Many | Child Table DocType | Invoice → Invoice Items |
| Many-to-One | Link field | Invoice → Customer |
| Many-to-Many | Link DocType (intermediary) | Student → Course (via Enrollment) |
| One-to-One | Link field + unique validation | Employee → User |
| Self-referential | Link to same DocType | Employee → Reports To (Employee) |

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| App name | lowercase, underscores | `custom_manufacturing` |
| DocType name | Title Case, spaces | `Production Order` |
| Field name | lowercase, underscores | `production_date` |
| Controller | snake_case filename | `production_order.py` |
| Module | Title Case | `Manufacturing` |

### Data Model Rules

- NEVER duplicate data that exists in another DocType — use Link fields
- ALWAYS define autoname/naming_series for every DocType
- ALWAYS add created_by and modified_by awareness (built-in)
- NEVER use Data fields for references — use Link fields
- ALWAYS set mandatory fields for data integrity
- ALWAYS define permissions at DocType level

## App Composition Patterns

### Pattern 1: Base + Vertical

```
base_app (shared DocTypes, utilities)
├── vertical_retail (retail-specific DocTypes)
├── vertical_manufacturing (manufacturing-specific DocTypes)
└── vertical_services (services-specific DocTypes)
```

**Use when**: Building industry-specific solutions on shared foundation.

### Pattern 2: Core + Extensions

```
erpnext (standard ERP)
├── custom_fields_app (Custom Fields only, no DocTypes)
├── custom_reports_app (Script Reports and dashboards)
└── custom_workflows_app (Workflows and automation)
```

**Use when**: Extending ERPNext without modifying core. Keeps upgrades clean.

### Pattern 3: Shared Utilities

```
frappe_utils (shared library: PDF generation, email templates, etc.)
├── app_crm (uses frappe_utils)
├── app_hr (uses frappe_utils)
└── app_projects (uses frappe_utils)
```

**Use when**: Multiple apps need the same utility functions.

### Pattern 4: Marketplace App

```
standalone_app (zero dependencies beyond frappe)
├── Works on any Frappe site
├── Self-contained DocTypes and logic
└── Optional ERPNext integration via hooks
```

**Use when**: Building for distribution/sale on Frappe marketplace.

## ERPNext Extension Patterns

### Custom Fields vs Custom DocTypes vs Override

| Approach | Use When | Pros | Cons |
|----------|----------|------|------|
| **Custom Fields** | Adding 1-10 fields to existing DocType | Survives upgrades, no code | Limited logic, UI clutter |
| **Custom DocType** | New business entity not in ERPNext | Full control, clean design | No built-in ERPNext logic |
| **Controller Override** | Modifying existing ERPNext behavior | Full Python access | Fragile on upgrades |
| **Server Script** | Simple validation/automation | No custom app needed | Sandbox limitations |
| **Client Script** | UI customization | No custom app needed | JS only, no server logic |

### Extension Decision Rules

- ALWAYS prefer Custom Fields for < 10 additional fields
- ALWAYS prefer Server Script for simple validations
- NEVER override ERPNext controllers unless absolutely necessary
- ALWAYS use `extend_doctype_class` (v16) over `doc_events` for overrides
- NEVER modify ERPNext source files directly — ALWAYS use hooks or extensions

## Common Architecture Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|-------------|-----------------|
| Circular app dependencies | Install/update breaks | Restructure dependency tree |
| One mega-app with 50+ DocTypes | Unmaintainable, slow tests | Split by domain into 3-5 apps |
| Duplicating ERPNext DocTypes | Data inconsistency, double maintenance | Extend with Custom Fields + hooks |
| No `required_apps` declaration | Silent failures on fresh install | ALWAYS declare all dependencies |
| Shared database tables between apps | Tight coupling, migration conflicts | Use Link fields and API calls |
| Modifying ERPNext source files | Lost on every upgrade | Use hooks, Custom Fields, extensions |
| No module organization within app | Files scattered, hard to navigate | Group DocTypes into modules |
| Hardcoded site/company names | Breaks on multi-site/multi-company | Use `frappe.defaults` and filters |

## Agent Output Format

ALWAYS produce architecture output in this format:

```markdown
## Architecture Design

### Requirements Summary
| # | Requirement | DocTypes | Mechanism |
|---|------------|----------|-----------|

### App Structure
[Diagram showing apps and dependencies]

### App Inventory
| App | Module(s) | DocTypes | Dependencies |
|-----|-----------|----------|-------------|

### Data Model
| DocType | App | Key Fields | Relationships |
|---------|-----|------------|---------------|

### Cross-App Communication
| Source App | Target App | Mechanism | Trigger |
|-----------|-----------|-----------|---------|

### ERPNext Extensions
| Extension Type | Target DocType | Purpose |
|---------------|---------------|---------|

### Implementation Roadmap
| Phase | App(s) | Deliverables | Dependencies |
|-------|--------|-------------|-------------|

### Risk Assessment
| Risk | Mitigation |
|------|-----------|

### Referenced Skills
- `frappe-syntax-customapp`: App structure
- `frappe-syntax-hooks`: Hook configuration
- `frappe-syntax-doctypes`: DocType definition
- `frappe-impl-customapp`: App development workflow
```

See [references/decision-tree.md](references/decision-tree.md) for complete decision frameworks.
See [references/examples.md](references/examples.md) for architecture design examples.
