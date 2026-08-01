---
name: plan-validate-execute-template
description: '[REPLACE] Plan changes, validate before execution, execute with verification.
  Use when [REPLACE with specific triggers].'
---

---
name: plan-validate-execute-template
description: [REPLACE] Plan changes, validate before execution, execute with verification. Use when [REPLACE with specific triggers].
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite
---

# Plan-Validate-Execute Template

## Purpose

This template demonstrates the Plan → Validate → Execute → Verify workflow for operations requiring approval gates and validation.

**Use this template when:**

- Changes are irreversible or high-risk
- User approval needed before execution
- Validation required before and after changes
- Rollback procedures necessary

## Workflow

### Phase 1: Plan

<plan>
1. Analyze current state
2. Define desired end state
3. Break down into atomic steps
4. Identify risks and dependencies
5. Create rollback plan
6. Present plan for approval
</plan>

### Phase 2: Validate Plan

<validate-plan>
1. Check preconditions
2. Verify dependencies exist
3. Test transformations on sample data
4. Confirm rollback procedure works
5. Get explicit user approval before proceeding
</validate-plan>

### Phase 3: Execute

<execute>
1. Create backup/checkpoint
2. Execute steps sequentially
3. Log each operation
4. Stop on first error
5. Provide progress updates
</execute>

### Phase 4: Verify

<verify>
1. Confirm all changes applied
2. Run validation tests
3. Check data integrity
4. Verify system functionality
5. Document completion
</verify>

<validate>
Run the following validation script:
`/scripts/validate-skill-output.sh {arguments}`
</validate>

## Progressive Disclosure

**Core workflow (this file):**

- Plan → Validate → Execute → Verify phases
- Approval gates and checkpoints

**Detailed guidance (references/):**

- references/migration-example.md - Complete database migration
- Rollback procedures and error handling

## Example Usage

```xml
<plan>
Migration Plan: Users table normalization
1. Create new addresses table
2. Migrate address data
3. Add foreign keys
4. Drop old columns
Estimated time: 5 minutes
Risk: Medium (data transformation)
Rollback: Restore from backup
</plan>

<validate-plan>
✓ Sample data transformation verified
✓ Foreign key constraints tested
✓ Rollback procedure confirmed
⚠️ Awaiting user approval to proceed
</validate-plan>

<execute>
[Step 1/4] Creating addresses table... ✓
[Step 2/4] Migrating 1,245 records... ✓
[Step 3/4] Adding foreign keys... ✓
[Step 4/4] Dropping old columns... ✓
</execute>

<verify>
✓ All 1,245 records migrated successfully
✓ Foreign key constraints valid
✓ No orphaned records
✓ Application tests passing
Migration complete!
</verify>
```

## See Also

- @references/migration-example.md - Full migration workflow
