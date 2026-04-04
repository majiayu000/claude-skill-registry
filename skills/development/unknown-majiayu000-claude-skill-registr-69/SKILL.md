---
name: plan
description: Generate plan.md and tasks.md for PLANNING increment using Architect Agent
---

# /sw:plan - Generate Implementation Plan

**⚠️ FOR EXISTING INCREMENTS ONLY - NOT for creating new increments!**

**When to use `/sw:plan`:**
- You already have `spec.md` created
- Increment status is PLANNING or ACTIVE
- You need to generate/regenerate `plan.md` and `tasks.md`

**When NOT to use `/sw:plan`:**
- Creating a brand new increment from scratch → Use `/sw:increment` instead
- No `spec.md` exists yet → Use `/sw:increment` instead

---

Generate `plan.md` and `tasks.md` for an increment using Architect Agent and test-aware-planner.

## Usage

```bash
/sw:plan                      # Auto-detect PLANNING increment
/sw:plan 0039                 # Explicit increment ID
/sw:plan --force              # Overwrite existing plan/tasks
/sw:plan 0039 --verbose       # Verbose output
```

## What It Does

1. **Auto-detect increment** (if not specified):
   - Prefers PLANNING status
   - Falls back to single ACTIVE increment

2. **Validate pre-conditions**:
   - spec.md exists and is not empty
   - Increment is not COMPLETED/ABANDONED
   - plan.md/tasks.md don't exist (unless --force)

   **Error Handling:**
   ```typescript
   import { ERROR_MESSAGES, formatError } from './src/utils/error-formatter.js';

   // If spec.md not found
   if (!specExists) {
     formatError(ERROR_MESSAGES.SPEC_NOT_FOUND(incrementId));
     return;
   }

   // If increment not found
   if (!incrementExists) {
     formatError(ERROR_MESSAGES.INCREMENT_NOT_FOUND(incrementId));
     return;
   }

   // If user tries to use /sw:plan for NEW increments
   if (userIsCreatingNew) {
     formatError(ERROR_MESSAGES.WRONG_COMMAND_FOR_NEW_INCREMENT());
     return;
   }
   ```

3. **Generate plan.md** (via Architect Agent):
   - Technical approach
   - Architecture design
   - Dependencies
   - Risk assessment

4. **Generate tasks.md** (via test-aware-planner):
   - Checkable task list
   - Embedded test plans (BDD format)
   - Coverage targets

5. **Update metadata**:
   - PLANNING → ACTIVE transition (tasks.md now exists)
   - Update lastUpdated timestamp

## Options

- `--force`: Overwrite existing plan.md/tasks.md
- `--preserve-task-status`: Keep existing task completion status (requires --force)
- `--verbose`: Show detailed execution information

## Examples

**Auto-detect and plan**:
```bash
/sw:plan
# ✅ Auto-detected increment: 0039-ultra-smart-next-command
# ✅ Generated plan.md (2.5K)
# ✅ Generated tasks.md (4.2K, 15 tasks)
# ✅ Transitioned PLANNING → ACTIVE
```

**Force regenerate**:
```bash
/sw:plan 0039 --force
# ⚠️  Overwriting existing plan.md
# ⚠️  Overwriting existing tasks.md
# ✅ Generated plan.md (2.8K)
# ✅ Generated tasks.md (5.1K, 18 tasks)
```

**Multiple PLANNING increments**:
```bash
/sw:plan
# ❌ Multiple increments in PLANNING status found:
#    - 0040-feature-a
#    - 0041-feature-b
# Please specify: /sw:plan 0040
```

## Self-Awareness Check

**🎯 OPTIONAL**: Detect if planning for SpecWeave framework increment.

Before generating plan.md, check repository context:

```typescript
import { detectSpecWeaveRepository } from './src/utils/repository-detector.js';

const repoInfo = detectSpecWeaveRepository(process.cwd());

if (repoInfo.isSpecWeaveRepo) {
  console.log('ℹ️  Planning for SpecWeave framework increment');
  console.log('');
  console.log('   💡 Framework Planning Considerations:');
  console.log('      • Design for backward compatibility');
  console.log('      • Consider impact on existing user projects');
  console.log('      • Plan for migration guides if breaking');
  console.log('      • Document new patterns in CLAUDE.md');
  console.log('      • Add ADR for significant architectural changes');
  console.log('');
}
```

**Why This Helps**:
Planning for framework features requires different considerations than user apps:
- Backward compatibility is critical
- Changes affect ALL SpecWeave users
- Architecture decisions need ADRs
- Workflow changes need CLAUDE.md updates

---

## Workflow Integration

**Typical workflow**:
```bash
# 1. Create increment (generates spec.md)
/sw:increment "Add user authentication"
# Status: BACKLOG → PLANNING (spec.md created)

# 2. Edit spec.md (add requirements, ACs)
# ... edit spec.md ...

# 3. Generate plan and tasks
/sw:plan
# Status: PLANNING → ACTIVE (tasks.md created)

# 4. Execute tasks
/sw:do
```

## Error Handling

**spec.md not found**:
```bash
❌ spec.md not found in increment '0039-ultra-smart-next-command'
💡 Create spec.md first using `/sw:increment` or manually
```

**plan.md already exists**:
```bash
❌ plan.md already exists in increment '0039'
💡 Use --force to overwrite existing plan.md
```

**Increment closed**:
```bash
❌ Cannot generate plan for COMPLETED increment
💡 Reopen increment with `/sw:reopen` first
```

## Architecture

**Components**:
- `IncrementDetector`: Auto-detect or validate increment
- `PlanValidator`: Validate pre-conditions
- `ArchitectAgentInvoker`: Generate plan.md via Architect Agent
- `TaskGeneratorInvoker`: Generate tasks.md via test-aware-planner
- `PlanCommandOrchestrator`: Coordinate execution pipeline

**State transitions**:
- PLANNING → ACTIVE (when tasks.md created)
- ACTIVE → ACTIVE (regenerate plan/tasks)
- BACKLOG → (no change - spec.md already exists)

## Related Commands

- `/sw:increment` - Create new increment (generates spec.md)
- `/sw:do` - Execute tasks from tasks.md
- `/sw:validate` - Validate increment structure
- `/sw:sync-docs` - Sync spec changes to living docs

## Notes

- **Auto-transition**: Creating tasks.md automatically transitions PLANNING → ACTIVE
- **Force mode**: Use with caution - overwrites existing work
- **Preserve status**: Use `--preserve-task-status` to keep completion checkmarks when regenerating
- **Architect Agent**: Requires ~10-30 seconds for plan generation
- **Test coverage**: tasks.md includes embedded test plans for each task

---

**Part of**: Increment 0039 (Ultra-Smart Next Command)
**Status**: Phase 1 - Foundation (US-007)
