---
name: deprecate-and-migrate
description: Plan and execute deprecation and migration of old systems, APIs, or features. Use when removing old code, migrating users to a new implementation, or deciding whether to maintain or sunset something.
---

# Deprecation and Migration

## Overview

Code is a liability. Every line carries ongoing cost: tests, documentation, security patches, dependency bumps, and the attention of anyone who edits nearby. The asset is the functionality; the code is the bill. Deprecation removes code that no longer earns its cost. Migration moves consumers from the old path to the new one without breaking them.

Building is the easy half. Removal is the half most teams skip. This skill covers removal.

## When to Use

- Replacing an old system, API, or library with a new one
- Sunsetting a feature that's no longer needed
- Consolidating duplicate implementations
- Removing dead code that nobody owns but everybody depends on
- Planning the lifecycle of a new system (deprecation planning starts at design time)
- Deciding whether to maintain a legacy system or invest in migration

## Core Principles

### Code Is a Liability

Every line costs maintenance: tests, docs, security patches, dependency updates, and cognitive load on nearby work. Functionality is what users buy; the code is what you pay. When the same functionality fits in less code, less state, or a cleaner interface, retire the old code.

### Hyrum's Law Makes Removal Hard

Past a certain consumer count, every observable behavior gets depended on, including bugs, timing quirks, and undocumented side effects. Deprecation therefore needs active migration, not an announcement. A consumer cannot "just switch" while it relies on behavior the replacement does not reproduce.

### Deprecation Planning Starts at Design Time

When building something new, ask how it gets removed in three years. Clean interfaces, feature flags, and a small surface keep a system removable. Leaked implementation details make it permanent.

## The Deprecation Decision

Answer these before deprecating anything:

```
1. Does this system still provide unique value?
   → If yes, maintain it. If no, proceed.

2. How many users/consumers depend on it?
   → Quantify the migration scope.

3. Does a replacement exist?
   → If no, build the replacement first. Don't deprecate without an alternative.

4. What's the migration cost for each consumer?
   → If trivially automated, do it. If manual and high-effort, weigh against maintenance cost.

5. What's the ongoing maintenance cost of NOT deprecating?
   → Security risk, engineer time, opportunity cost of complexity.
```

## Compulsory vs Advisory Deprecation

| Type | When to Use | Mechanism |
|------|-------------|-----------|
| **Advisory** | Migration is optional, old system is stable | Warnings, documentation, nudges. Users migrate on their own timeline. |
| **Compulsory** | Old system has security issues, blocks progress, or maintenance cost is unsustainable | Hard deadline. Old system will be removed by date X. Provide migration tooling. |

**Default to advisory.** Compulsory is justified only when maintenance cost or risk forces the issue, and it obligates you to ship migration tooling, documentation, and support. A deadline alone is not a migration.

## The Migration Process

### Step 1: Build the Replacement

No deprecation without a working alternative. The replacement must:

- Cover all critical use cases of the old system
- Have documentation and a migration guide
- Be proven in production, not argued to be theoretically better

### Step 2: Announce and Document

```markdown
## Deprecation Notice: OldService

**Status:** Deprecated as of 2025-03-01
**Replacement:** NewService (see migration guide below)
**Removal date:** Advisory; no hard deadline yet
**Reason:** OldService requires manual scaling and lacks observability.
            NewService handles both automatically.

### Migration Guide
1. Swap the old client dependency for the new one — e.g. `old-service` → `new-service`
   as the import in a TypeScript/JS project, the package path in a Go import, or the
   module in a Python `import`.
2. Update configuration (see examples below).
3. Run the migration verification check shipped with the replacement.
```

### Step 3: Migrate Incrementally

Migrate consumers one at a time, not all at once. For each consumer:

```
1. Identify all touchpoints with the deprecated system
2. Update to use the replacement
3. Verify behavior matches (tests, integration checks)
4. Remove references to the old system
5. Confirm no regressions
```

**The Churn Rule:** If you own the infrastructure being deprecated, you own migrating its users — or you ship backward-compatible updates that require no migration. Announcing a deprecation and leaving users to figure it out is not allowed.

### Step 4: Remove the Old System

Only after all consumers have migrated:

```
1. Verify zero active usage (metrics, logs, dependency analysis)
2. Remove the code
3. Remove associated tests, documentation, and configuration
4. Remove the deprecation notices
5. Celebrate — removing code is an achievement
```

## Migration Patterns

### Strangler Pattern

Run old and new in parallel. Route traffic incrementally from old to new. When the old system handles 0% of traffic, remove it.

```
Phase 1: New system handles 0%, old handles 100%
Phase 2: New system handles 10% (canary)
Phase 3: New system handles 50%
Phase 4: New system handles 100%, old system idle
Phase 5: Remove old system
```

### Adapter Pattern

Wrap the new implementation behind the old interface. Consumers keep calling the old API while the backend moves to the replacement.

```typescript
// Old interface, new implementation underneath
class LegacyTaskService implements OldTaskAPI {
  constructor(private readonly next: NewTaskService) {}

  getTask(id: number): OldTask {
    return this.toOldFormat(this.next.findById(String(id)));
  }
}
```

```python
# Old interface, new implementation underneath
class LegacyTaskService(OldTaskAPI):
    def __init__(self, nxt: NewTaskService) -> None:
        self._next = nxt

    def get_task(self, task_id: int) -> OldTask:
        return to_old_format(self._next.find_by_id(str(task_id)))
```

### Feature Flag Migration

Flip consumers from old to new one cohort at a time, gated by a flag.

```go
func TaskServiceFor(userID string) TaskService {
    if flags.Enabled("new-task-service", userID) {
        return NewTaskService()
    }
    return LegacyTaskService()
}
```

```typescript
function taskServiceFor(userId: string): TaskService {
  return flags.isEnabled("new-task-service", { userId })
    ? new NewTaskService()
    : new LegacyTaskService();
}
```

## Zombie Code

Zombie code is code that nobody owns but everybody depends on. It is unmaintained, has no owner, and accumulates security vulnerabilities and compatibility rot. Signs:

- No commits in 6+ months but active consumers exist
- No assigned maintainer or team
- Failing tests that nobody fixes
- Dependencies with known vulnerabilities that nobody updates
- Documentation that references systems that no longer exist

**Response:** Assign an owner and maintain it properly, or deprecate it with a concrete migration plan. Zombie code does not stay in limbo. It gets investment or it gets removed.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It still works, why remove it?" | Working code that nobody maintains accumulates security debt and complexity. The maintenance cost grows silently. |
| "Someone might need it later" | If it's needed later, rebuild it. Keeping unused code "just in case" costs more than rebuilding. |
| "The migration is too expensive" | Compare migration cost to two or three years of maintenance cost. Migration is usually cheaper long-term. |
| "We'll deprecate it after we finish the new system" | Deprecation planning starts at design time. By the time the new system ships, you'll have new priorities. Plan now. |
| "Users will migrate on their own" | They won't. Provide tooling, documentation, and incentives, or do the migration yourself (the Churn Rule). |
| "We can maintain both systems indefinitely" | Two systems doing the same job is double the maintenance, testing, documentation, and onboarding cost. |

## Red Flags

- Deprecated systems with no replacement available
- Deprecation announcements with no migration tooling or documentation
- "Soft" deprecation that's been advisory for years with no progress
- Zombie code with no owner and active consumers
- New features added to a deprecated system (invest in the replacement instead)
- Deprecation without measuring current usage
- Removing code without verifying zero active consumers

## Verification

After completing a deprecation:

- [ ] Replacement is production-proven and covers all critical use cases
- [ ] Migration guide exists with concrete steps and examples
- [ ] All active consumers have been migrated (verified by metrics/logs)
- [ ] Old code, tests, documentation, and configuration are fully removed
- [ ] No references to the deprecated system remain in the codebase
- [ ] Deprecation notices are removed (they served their purpose)
