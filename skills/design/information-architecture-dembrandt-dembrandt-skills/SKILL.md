---
name: information-architecture
description: In large applications, information architecture determines whether users can find, understand, and act on data. Naming matters. The UI should mirror the data model and signal how data can be transformed. Dangerous or irreversible changes always require a confirm dialog. Use when designing navigation, naming entities, structuring large feature sets, or modelling data-driven UI.
metadata:
  priority: 9
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "ui/**"
    - "app/**"
    - "pages/**"
  promptSignals:
    phrases:
      - "information architecture"
      - "navigation structure"
      - "naming"
      - "mental model"
      - "data model"
      - "entity"
      - "confirm dialog"
      - "destructive action"
      - "large application"
      - "ia"
retrieval:
  aliases:
    - information architecture
    - IA
    - naming
    - mental model
    - data model UI
    - navigation structure
    - confirm dialog
    - destructive action
  intents:
    - structure a large application
    - name entities clearly
    - design navigation for complex product
    - model the UI around data
    - add confirm dialog for dangerous action
    - build user mental model
  examples:
    - how should I structure navigation for this app
    - what should I call this entity
    - add a confirm dialog before deleting
    - design the data model for this UI
    - make this large app easier to navigate
---

# Information Architecture

In small products, users find their way by exploring. In large applications — multi-module SaaS, ERPs, analytics platforms, marketplaces — exploration breaks down. The structure itself must do the navigational work. Information architecture is the design of that structure: what exists, what it is called, and how it relates to everything else.

Good IA is invisible. Users find what they need without thinking about the structure. Bad IA forces users to hold a map in their head.

---

## Naming is Design

The names given to entities, sections, and actions are one of the most consequential design decisions in a large application. Bad names create cognitive friction on every visit.

**Principles:**

- **Use the user's vocabulary, not the engineer's.** If users call it a "job", do not call it a `task_assignment`. If they call it a "client", do not surface `contact_entity`.
- **Be specific.** "Settings" is vague. "Account settings", "Workspace settings", "Notification preferences" tell the user exactly where they are.
- **Be consistent.** If it is called "Project" in the sidebar, it must be called "Project" in the breadcrumb, the page title, the confirmation dialog, and the API error message.
- **Distinguish similar things.** If the product has both "Users" and "Members", the distinction must be meaningful and consistently communicated.
- **Name actions by their effect.** "Archive" not "Hide". "Publish" not "Save to live". "Transfer ownership" not "Change user".

**Naming audit questions:**
- Would a new user understand this term without training?
- Is this name used consistently across every surface it appears?
- Does this name describe what the thing *does*, not how it is stored?

---

## Mental Model Follows Data Model

The UI should be a direct, legible expression of the underlying data model. Users build a mental model of the product by interacting with it — that mental model should match how the data actually works.

**Match entities to screens.** Each major data entity (Project, Invoice, User, Product) typically deserves its own list view and detail view. Do not collapse distinct entities into one screen because it seems simpler — users will be confused when one action affects something they did not see.

**Expose relationships.** If a Project contains Tasks, and Tasks belong to Users, the UI hierarchy should reflect this:

```
Projects
  └── Project: Website Redesign
        └── Tasks
              └── Task: Fix header  [Assigned to: Maria]
```

Breadcrumbs, parent labels, and contextual references ("3 tasks in this project") reinforce the data relationships visually.

**Show transformation paths.** The UI should make it clear how data moves through the system. A draft becomes published. An invoice moves from pending to paid. A user is promoted to admin. These state transitions should be visible:

- Status labels that show current state and available transitions
- Action buttons labelled with the transformation: "Publish", "Mark as paid", "Promote to admin"
- Timeline or history showing past transitions

**Signal the scope of actions.** Before a user commits to an action, they must understand what it will affect:

```
"Archive this project?"
This will also archive 47 tasks and remove it from all dashboards. 
Team members will lose access immediately.
[Cancel]  [Archive project]
```

---

## Confirm Dialogs for Dangerous Actions

Any action that is irreversible, affects a wide scope, or causes data loss requires explicit confirmation before execution. The confirm dialog is not a courtesy — it is a contract with the user.

**When a confirm dialog is required:**

| Action type | Example | Dialog required |
|---|---|---|
| Permanent deletion | Delete project, remove user | Always |
| Bulk destruction | Delete all items in a filter | Always |
| Irreversible state change | Publish, Submit, Send | Yes if no undo |
| Wide-scope change | Transfer ownership, change billing plan | Always |
| Account-level action | Cancel subscription, delete account | Always |
| Permission escalation | Grant admin access | Yes |

**Confirm dialog anatomy:**

```
[Title: specific, not generic]
"Delete project: Website Redesign?"

[Body: scope and consequences]
"This will permanently delete:
• 47 tasks
• 3 milestones
• All associated files

This cannot be undone."

[Secondary action]  [Destructive primary action]
    [Cancel]              [Delete project]
```

**Rules:**
- Title names the specific entity — "Delete project: Website Redesign?" not "Are you sure?"
- Body states exactly what will be affected and whether it can be undone
- The destructive action is labelled with the action, not "OK" or "Yes"
- The destructive action is visually distinct: red fill, or positioned on the right
- Cancel is always available and is the default focus (keyboard enter should not trigger deletion)
- For the highest-risk actions (account deletion, irreversible bulk operations), require the user to type the entity name to confirm

**What not to use a confirm dialog for:**
- Saving or updating (autosave + undo is better)
- Navigation away from unsaved changes (use an unsaved changes warning banner instead)
- Low-stakes reversible actions (archiving with an unarchive option)

---

## Navigation Structure in Large Applications

IA manifests most visibly in navigation. As products grow, navigation must scale with them.

**Flat is fast, deep is findable.** Aim for no more than 3 levels of hierarchy in primary navigation. If the product requires more, introduce grouping and search rather than more levels.

**Group by user goal, not by product feature.** Users navigate to accomplish tasks. Group navigation items around what users want to do, not around how the backend is organised.

```
Bad:  Settings → Integrations → Webhooks → Event types
Good: Developer → Webhooks
```

**Progressive disclosure for power users.** Show the most-used sections in primary navigation. Secondary features live in settings, secondary nav, or are reached via search. Do not surface every feature at the top level.

**Global search as escape hatch.** In large applications, search reduces the navigation burden. Users who know what they want should never have to navigate through 4 levels to find it.

**Logo as Home.** The product logo should always be an interactive link leading back to the primary landing page or dashboard. This is a universal user expectation — a "reset button" for navigation.

**Global Header Consistency.** In applications with deep hierarchy, keep the primary header and top-level navigation consistent across all views. Changing the global navigation based on the user's current depth disorients them and removes their easy path back to other content.

**Persistent context.** In deeply nested views, the user must always be able to answer: where am I, what does this belong to, and how do I get back?
- **Shallow hierarchy (1–2 layers):** Use a simple "← Back to [Parent]" link. Breadcrumbs (Home > Parent > Current) often add unnecessary visual noise for simple structures.
- **Deep hierarchy (3+ layers):** Use breadcrumbs to provide a clear map of the user's location and an easy path to any parent level.

Use parent labels and contextual headers to reinforce the current location.

---

## Review Checklist

- [ ] Are entity names derived from user vocabulary, not system terminology?
- [ ] Is the same name used consistently across every surface (nav, breadcrumb, dialog, error)?
- [ ] Does the UI hierarchy reflect the data model hierarchy?
- [ ] Are data state transitions (draft → published, pending → paid) clearly visible and labelled?
- [ ] Does every action communicate its scope before the user commits?
- [ ] Do all irreversible or wide-scope actions have a confirm dialog?
- [ ] Does the confirm dialog name the specific entity and list consequences?
- [ ] Is the destructive action in the confirm dialog labelled with the action, not "OK"?
- [ ] Is Cancel the default focus in confirm dialogs?
- [ ] Is primary navigation grouped by user goal, not product feature?
- [ ] Is global search available for products with more than 3 navigation levels?
- [ ] Does the product logo link back to the landing page or primary dashboard?
- [ ] Is the primary header and global navigation consistent across all views, regardless of depth?
- [ ] Are back links used for shallow hierarchies (1–2 layers) and breadcrumbs for deep hierarchies (3+ layers)?
