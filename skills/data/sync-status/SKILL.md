---
name: sync-status
description: Detect and fix status desyncs between metadata.json and spec.md
---

# Sync Status - Desync Detection & Recovery

**CRITICAL**: Detects and fixes status desyncs between metadata.json and spec.md to maintain source-of-truth integrity.

## Overview

This command scans increments for status desyncs where metadata.json and spec.md have different status values. This violates CLAUDE.md Rule #7 (source-of-truth discipline) and causes:
- Status line showing wrong increment
- Commands operating on wrong data
- User confusion and broken trust

**Incident Reference**: 2025-11-20 - Silent failure in /sw:done caused increment 0047 to have metadata.json="completed" while spec.md="active", breaking status line.

## Usage

```bash
# Scan all increments for desyncs
/sw:sync-status

# Check specific increment
/sw:sync-status 0047

# Auto-fix all desyncs (non-interactive)
/sw:sync-status --fix

# Scan and show detailed report
/sw:sync-status --verbose
```

## Arguments

- `<increment-id>` - Optional. Specific increment to check (e.g., "0047", "0001-test")
- `--fix` - Auto-fix all desyncs without prompting
- `--verbose` - Show detailed report including healthy increments

---

## Workflow

### Mode 1: Scan All Increments (Default)

**When to use**: Regular maintenance, pre-commit checks, incident investigation

**Steps**:

1. **Scan all increments**:
   ```typescript
   import { DesyncDetector } from '../../../src/core/increment/desync-detector.js';

   const detector = new DesyncDetector();
   const report = await detector.scanAll();
   ```

2. **Display report**:
   ```typescript
   console.log(detector.formatReport(report));
   ```

3. **Example output** (desyncs found):
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   STATUS DESYNC DETECTION REPORT
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Total Scanned: 47 increments
   Healthy: 46
   Desyncs Found: 1 ⚠️
   Errors: 0

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   DESYNCS DETECTED (CRITICAL!)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ❌ 0047-us-task-linkage
      metadata.json: completed
      spec.md:       active

   Fix command: /sw:sync-status --fix

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

4. **If desyncs found, prompt user**:
   ```typescript
   if (report.totalDesyncs > 0) {
     const shouldFix = await promptUser(
       `Found ${report.totalDesyncs} desync(s). Fix them? (y/n): `
     );

     if (shouldFix) {
       // Fix all desyncs
       for (const desync of report.desyncs) {
         const fixed = await detector.fixDesync(desync.incrementId);
         if (fixed) {
           console.log(`✅ Fixed ${desync.incrementId}`);
         } else {
           console.error(`❌ Failed to fix ${desync.incrementId}`);
         }
       }

       console.log('');
       console.log('All desyncs fixed! Run /sw:sync-status to verify.');
     }
   }
   ```

5. **Example output** (no desyncs):
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   STATUS DESYNC DETECTION REPORT
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Total Scanned: 47 increments
   Healthy: 47
   Desyncs Found: 0 ⚠️
   Errors: 0

   ✅ All increments healthy - no desyncs detected!

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

### Mode 2: Check Specific Increment

**When to use**: Investigating specific increment, post-fix verification

**Steps**:

1. **Check increment**:
   ```typescript
   const detector = new DesyncDetector();
   const result = await detector.checkIncrement(incrementId);
   ```

2. **Display result**:
   ```typescript
   if (result.error) {
     console.error(`❌ Error checking ${incrementId}: ${result.error}`);
     process.exit(1);
   }

   if (result.hasDesync) {
     console.log('━'.repeat(80));
     console.log(`❌ DESYNC DETECTED: ${incrementId}`);
     console.log('━'.repeat(80));
     console.log('');
     console.log(`metadata.json: ${result.metadataStatus}`);
     console.log(`spec.md:       ${result.specStatus}`);
     console.log('');
     console.log('This violates source-of-truth discipline (CLAUDE.md Rule #7)');
     console.log('');
     console.log(`Fix: /sw:sync-status ${incrementId} --fix`);
     console.log('━'.repeat(80));
   } else {
     console.log(`✅ ${incrementId} - No desync detected`);
     console.log(`   Status: ${result.metadataStatus}`);
   }
   ```

3. **Example output** (desync found):
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ❌ DESYNC DETECTED: 0047-us-task-linkage
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   metadata.json: completed
   spec.md:       active

   This violates source-of-truth discipline (CLAUDE.md Rule #7)

   Fix: /sw:sync-status 0047 --fix
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

### Mode 3: Auto-Fix (Non-Interactive)

**When to use**: CI/CD pipelines, automated recovery, pre-commit hooks

**Steps**:

1. **Scan and fix**:
   ```typescript
   const detector = new DesyncDetector();
   const report = await detector.scanAll();

   if (report.totalDesyncs > 0) {
     console.log(`Found ${report.totalDesyncs} desync(s) - fixing...`);
     console.log('');

     for (const desync of report.desyncs) {
       const fixed = await detector.fixDesync(desync.incrementId);
       if (fixed) {
         console.log(`✅ Fixed ${desync.incrementId}: ${desync.specStatus} → ${desync.metadataStatus}`);
       } else {
         console.error(`❌ Failed to fix ${desync.incrementId}`);
       }
     }

     console.log('');
     console.log('✅ All desyncs fixed!');
   } else {
     console.log('✅ No desyncs found - all healthy');
   }
   ```

2. **Example output**:
   ```
   Found 1 desync(s) - fixing...

   ✅ Fixed 0047-us-task-linkage: active → completed

   ✅ All desyncs fixed!
   ```

---

## How Desyncs Are Fixed

**Fix Strategy**: metadata.json is considered the source of truth for status updates.

**Rationale**:
- metadata.json is updated atomically by CLI commands
- metadata.json is used for increment state management
- spec.md should mirror metadata.json for consistency

**Fix Process**:
1. Read current status from metadata.json
2. Read current status from spec.md
3. Update spec.md frontmatter to match metadata.json
4. Write spec.md atomically (temp file → rename)
5. Verify fix by re-checking

**What gets updated**:
- ✅ spec.md YAML frontmatter `status` field
- ❌ metadata.json (already correct)

**Example fix**:
```yaml
# Before (spec.md)
---
status: active
---

# After (spec.md)
---
status: completed
---
```

---

## Post-Fix Actions

After fixing desyncs, the following actions happen automatically:

1. **Status Line Cache Update**:
   ```bash
   # Automatically triggered by spec.md change
   bash plugins/specweave/hooks/lib/update-status-line.sh
   ```

2. **Git Status**:
   ```bash
   # spec.md will be modified - commit the fix
   git status
   git add .specweave/increments/*/spec.md
   git commit -m "fix: sync spec.md status with metadata.json"
   ```

3. **Verification**:
   ```bash
   # Verify no desyncs remain
   /sw:sync-status
   ```

---

## Error Handling

### Increment Not Found
```
❌ Error: Increment 0047-us-task-linkage not found

Check increment ID and try again.
```

### File Permission Error
```
❌ Failed to fix desync for 0047-us-task-linkage
Error: EACCES: permission denied, open '.specweave/increments/0047-us-task-linkage/spec.md'

Fix permissions:
  chmod u+w .specweave/increments/0047-us-task-linkage/spec.md
```

### YAML Parse Error
```
❌ Failed to fix desync for 0047-us-task-linkage
Error: Invalid YAML frontmatter in spec.md

Check YAML syntax:
  vim .specweave/increments/0047-us-task-linkage/spec.md
```

---

## Prevention

**To prevent future desyncs**:

1. ✅ **Atomic transaction pattern** in `metadata-manager.ts`
   - Updates spec.md FIRST, then metadata.json
   - If spec.md fails, metadata.json is never updated
   - No silent failures

2. ✅ **Desync detection** in `/sw:done`
   - Validates before closing increment
   - Blocks closure if desync detected

3. ✅ **Pre-commit hook validation**
   - Scans for desyncs before commit
   - Blocks commit if desyncs found
   - Auto-fix option available

4. ✅ **Comprehensive tests**
   - Unit tests for DesyncDetector
   - Integration tests for status updates
   - E2E tests for recovery scenarios

---

## Related Commands

- `/sw:done` - Close increment (includes desync validation)
- `/sw:validate` - Validate increment quality
- `/sw:status` - Show increment status overview

---

## Related Files

- `src/core/increment/desync-detector.ts` - Detection & fix logic
- `src/core/increment/metadata-manager.ts` - Atomic status updates
- `src/core/increment/spec-frontmatter-updater.ts` - spec.md updates
- `scripts/pre-commit-desync-check.sh` - Pre-commit validation

---

**Important**: This command is part of the incident response to the 2025-11-20 silent failure bug. It ensures source-of-truth discipline is maintained across the entire increment lifecycle.

**Best Practice**: Run `/sw:sync-status` regularly (weekly or before releases) to catch any desyncs early.
