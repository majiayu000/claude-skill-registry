---
name: ears-format
description: EARS format for defining system behavior in implementation plans (Phase 2). Used by how-planner agent to write how.md. Do NOT use for UX planning or Gherkin scenarios.
durability: encoded-preference
---

# EARS Format for Acceptance Criteria

EARS (Easy Approach to Requirements Syntax) provides patterns for writing clear, testable acceptance criteria.

## WHEN Pattern (Event-driven)

Use for user actions and triggered behaviors.

```
WHEN <trigger/condition>
THE SYSTEM SHALL <expected behavior>
```

**Example:**
```
WHEN user clicks the submit button
THE SYSTEM SHALL validate all form fields
```

## IF Pattern (Conditional)

Use for state-based conditions and logical branching.

```
IF <precondition/state>
THEN THE SYSTEM SHALL <response>
```

**Example:**
```
IF user is not authenticated
THEN THE SYSTEM SHALL redirect to login page
```

## WHILE Pattern (Continuous)

Use for ongoing behaviors and continuous conditions.

```
WHILE <ongoing condition>
THE SYSTEM SHALL <continuous behavior>
```

**Example:**
```
WHILE file upload is in progress
THE SYSTEM SHALL display progress indicator
```

## WHERE Pattern (Contextual)

Use for context-dependent and environmental conditions.

```
WHERE <context/environment>
THE SYSTEM SHALL <contextual behavior>
```

**Example:**
```
WHERE user has admin role
THE SYSTEM SHALL display admin controls
```

## Compound Pattern

Combine patterns for complex requirements.

```
WHEN <event> AND <additional condition>
THEN THE SYSTEM SHALL <response>
```

**Example:**
```
WHEN user submits form AND validation passes
THEN THE SYSTEM SHALL save data and show success message
```

## Pattern Selection Guide

| Pattern | Use When |
|---------|----------|
| **WHEN** | Event-driven behaviors, user actions |
| **IF** | State-based conditions, logical branching |
| **WHILE** | Continuous behaviors, ongoing conditions |
| **WHERE** | Context-dependent, environmental conditions |

## Phase 2 Role

EARS is used in `how.md` to specify system behavior per User Story, complementing Gherkin scenarios defined in `ux.md`.

- **ux.md** (Phase 1): Gherkin scenarios define user-facing behavior (Given/When/Then)
- **how.md** (Phase 2): EARS statements define system-level behavior (WHEN/THE SYSTEM SHALL)

EARS statements in how.md should be testable and map to implementation requirements that the Gherkin scenarios alone do not capture (e.g., performance constraints, error handling at system level, data validation rules).
