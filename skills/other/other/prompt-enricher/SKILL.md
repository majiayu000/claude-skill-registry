---
name: prompt-enricher
description: Phase 0.2 — Enriches the raw user prompt with discovered constraints, ambiguities, likely edge cases, and suggested scope boundaries. Runs after context-gatherer, before idea-explorer questions. Generates enriched-prompt.md in the state directory.
---

# Prompt Enricher

Runs **automatically as Phase 0.2**, after context-gatherer and before `idea-explorer` questions.
Purpose: transform the raw user prompt into a grounded, constraint-aware brief that prevents the spec from ignoring known realities of the codebase.

## Entry conditions

- `context.md` must exist in `.claude/feature-state/{slug}/` (run context-gatherer first)
- Generates `enriched-prompt.md` and saves to `.claude/feature-state/{slug}/`
- Load if already exists (resume flow)

## Step 1: Detect constraints from codebase

Read `context.md` and extract constraints relevant to the feature:

- **Architectural constraints**: What patterns must be followed? (e.g., "All API routes use verifyAuthRequest")
- **Data constraints**: What data model rules exist? (e.g., "soft delete only, never hard delete")
- **Infrastructure constraints**: What infrastructure is confirmed vs. uncertain? (e.g., "Stripe webhook is not configured in production")
- **Dependency constraints**: What libraries are already in use that shape the approach?

## Step 2: Identify ambiguities

From the prompt + context, list decisions that have multiple valid interpretations:

Examples:
- "Use the existing checkout flow or create a new direct-connect mechanism?"
- "Should connection be pending/approved or immediate?"
- "Is this feature for trainers or students or both?"
- "Real-time list updates or on-load only?"

## Step 3: Suggest likely edge cases by feature type

Auto-detect the feature type from the prompt and inject standard edge cases:

| Feature type detected | Auto-suggested edge cases |
|----------------------|--------------------------|
| Connection/relationship | What if already connected? What if connection is rejected? |
| Auth/permissions | What if token expired? What if user not found? Rate limit? |
| List/query | Empty result? Pagination? Combined filters? Sort order? |
| Form/input | Required vs optional fields? XSS/injection? Max length? |
| External integration | Timeout? Partial failure? Idempotency? |
| Delete/remove | Soft delete? Orphaned references? Permission check? |
| Notification | What if FCM token missing? Duplicate notification? |
| Payment | Idempotency? Webhook replay? Network failure mid-transaction? |

## Step 4: Suggest scope boundaries

Based on the prompt and the project's "Out of Scope" section in PROJECT.md:

- **In scope** (inferred from prompt + context)
- **Likely out of scope** (YAGNI — things often requested but not essential)
- **Deferred** (good ideas for a future iteration)

## Step 5: Generate enriched-prompt.md

Save to `.claude/feature-state/{slug}/enriched-prompt.md`:

```markdown
## Enriched Prompt

### Original Prompt
Allow personal trainers to connect with students after checkout

### Discovered Constraints
- All API routes must call verifyAuthRequest() before any operation (PROJECT.md)
- Firestore: soft delete only — status: 'archived', never hard delete
- Stripe webhook (handleCheckoutComplete) already creates trainer-student links
- FCM token not guaranteed — push notifications are optional

### Ambiguities to Resolve
- Should this create a NEW connection mechanism or extend the existing checkout flow?
- Is the connection immediate or does it require mutual acceptance?
- Should trainers see ALL their students or only active ones?
- Should students be notified when a trainer connects?

### Likely Edge Cases
- Trainer tries to connect with a student already connected → already-connected state
- Student belongs to multiple trainers → one-to-many or one-to-one relationship?
- Trainer with no students → empty state in CMS list
- Connection made, then Stripe payment reversed → what happens to the link?
- Real-time list update vs. stale view when trainer is on the CMS page

### Suggested Scope Boundaries
**In scope:**
- Trainer can see their connected students in /cms/students
- Student appears after successful checkout (existing mechanism)
- trainerId persisted on student Firestore document
- Student list loads on trainer CMS page

**Likely out of scope (YAGNI):**
- Student can view which trainer they're connected to (separate feature)
- Real-time listener for connection status (polling is sufficient for v1)
- Trainer can disconnect a student (follow-up feature)

**Deferred:**
- Push notification when connection is made (requires FCM token guarantee)
- Multiple trainers per student
```

## Step 6: Inject into idea-explorer context

This file is made available to `idea-explorer` as its starting brief.
When the enriched prompt exists, the first question from `idea-explorer` must reference it:

```
Based on what I found in the codebase, here's what we're working with:

[Summary of enriched-prompt.md key sections]

My first question: [first question anchored in the ambiguities above]
```

## Edge case injection by feature type detection

Feature type is detected from keywords in the prompt:

| Keywords | Detected type |
|----------|--------------|
| connect, link, assign, bind, invite, follow | connection/relationship |
| login, auth, token, session, password, verify | auth/permissions |
| list, search, filter, query, paginate, find, show all | list/query |
| create, add, submit, form, input, register | form/input |
| stripe, payment, subscription, checkout, invoice | payment |
| delete, remove, archive, deactivate | delete/remove |
| notify, notification, push, email, alert | notification |
| webhook, API, external, integration, sync | external integration |

Multiple types can be detected for a single feature.
