---
name: ic-migrate
description: Migrate old IC10 code to work with current Stationeers version. Use when user has legacy IC10 scripts that don't work due to game updates or breaking changes.
---

# IC10 Code Migration

Update old IC10 code to work with current Stationeers game version, handling breaking changes and deprecated features.

## Workflow

### 1. Analysis Phase
Use Task tool to spawn:
- `code-analyzer` - Understand current code structure

### 2. Migration Phase
Use Task tool to spawn:
- `code-migrator` - Apply version-specific transformations

### 3. Validation Phase
Use Task tool to spawn:
- `code-validator` - Verify migrated code passes validation

## Version Detection

The migrator will detect which version the code was written for based on patterns:

| Indicator | Detected Version | Breaking Changes |
|-----------|-------------------|------------------|
| No tier handling for trading | Pre-Dec 2022 | Trading Update III |
| Old stack ops (no peek/poke) | Pre-Mar 2025 | "Big Changes Coming" |
| No TraderInstruction enum | Pre-Mar 2025 | Trading enhancement |
| Modern patterns present | Current | None |

## Common Migration Scenarios

### Trading Scripts (Pre-Dec 2022)

**Problem**: Old trading scripts don't handle tier system (Close/Medium/Far dishes)

**Symptoms**:
- Script tries to trade but doesn't work
- No dish tier detection
- Missing InterrogationProgress checks

**Migration**:
1. Add tier constants (TIER_CLOSE, TIER_MEDIUM, TIER_FAR)
2. Add dish tier detection logic
3. Add interrogation progress checks before trading
4. Update trading flow for 3-tier system

### Stack Operations (Pre-Mar 2025)

**Problem**: Old code uses only push/pop, missing peek/poke

**Symptoms**:
- Stack operations limited
- Can't read stack without popping
- Inefficient stack management

**Migration**:
1. Add peek operation for non-destructive reads
2. Add poke operation for targeted writes
3. Optimize stack usage patterns

### Batch Operations (Outdated Hashes)

**Problem**: Prefab hashes may have changed in game updates

**Symptoms**:
- Batch operations don't affect devices
- Errors like "device not found"

**Migration**:
1. Verify hashes against `knowledge/hashes/device-hashes.md`
2. Update all `lb`/`sb` operations with current hashes
3. Test in-game to verify

## Instructions

When user requests code migration:

1. **Identify the code's approximate age**
   - Ask: "When was this code written?"
   - Analyze code patterns for version indicators
   - Note which breaking changes likely apply

2. **Launch code-migrator** with:
   - The old IC10 code
   - Detected version
   - Target version (current game)

3. **Review migration report**
   - Check which breaking changes were applied
   - Verify transformations make sense
   - Note any features requiring in-game testing

4. **Present migrated code**
   - Show before/after comparisons for key sections
   - Highlight breaking changes addressed
   - Explain migration strategy

5. **Provide testing recommendations**
   - List features that need in-game verification
   - Suggest test scenarios
   - Note any remaining uncertainties

## Example Triggers

- "Update this old script"
- "This code doesn't work anymore"
- "Migrate from pre-2022 version"
- "Trading script broken after update"
- "Update for current Stationeers version"
- "Fix deprecated features"

## Output Format

After migration completes, respond with:

```markdown
## Migration Report: [Script Name]

### Version Detection
**Original Version**: Pre-Dec 2022 (no tier handling)
**Target Version**: Current (Dec 2025)
**Breaking Changes Applied**: 3 (Trading tiers, InterrogationProgress, Stack ops)

### Transformations

| Change | Lines | Status |
|---------|-------|--------|
| Added tier detection | 12 | ✅ |
| Added interrogation handling | 8 | ✅ |
| Updated stack operations | 5 | ✅ |

### Migrated Code

```ic10
[Full migrated code with migration comments]
```

### In-Game Testing Required

⚠️ **Features to verify in-game:**

1. **Dish tier detection** - Verify Close/Medium/Far dish logic
2. **InterrogationProgress** - Test interrogation timing works
3. **Peek/poke operations** - Confirm stack operations work

### Testing Checklist

- [ ] Load migrated code into IC Housing
- [ ] Test with Close/Medium/Far dishes
- [ ] Verify trading completes successfully
- [ ] Check stack operations work as expected
- [ ] Verify no CPU overrun errors
```

## Notes

- Migration is based on documented breaking changes
- Some features require in-game verification
- Original code intent is preserved
- Modern best practices are applied during migration
- Line count constraints are maintained

## Related Skills

- `ic-debug` - For fixing specific bugs in migrated code
- `ic-test` - For verifying migrated code logic
- `ic-validate` - For checking migrated code constraints
