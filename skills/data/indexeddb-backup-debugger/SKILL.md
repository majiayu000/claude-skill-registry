---
name: indexeddb-backup-debugger
description: Debug IndexedDB backup synchronization issues in Vue.js/Pinia applications by analyzing database state, tracing data flow, and identifying sync problems between UI, store, and backup systems.
---

# IndexedDB Backup Debugger

Debug IndexedDB backup synchronization issues in Vue.js/Pinia applications by systematically analyzing database state, tracing data flow, and identifying synchronization problems between UI components, Pinia stores, IndexedDB, and backup systems.

## When to Use This Skill

Use this skill when:
- Backup system reports different task counts than actual UI data
- IndexedDB data appears stale or out of sync with Pinia store
- Backup system is not capturing current user data
- Data consistency issues between application layers
- Hebrew/Unicode content not properly preserved through backup cycles
- Real-time data synchronization problems in Vue.js applications

## Core Debugging Workflows

### Workflow 1: Database State Analysis
Execute database analysis to identify state inconsistencies:

1. Run `scripts/analyze-database.js` to dump all IndexedDB databases
2. Compare task counts across Pinia store, IndexedDB, and backup system
3. Identify which database version contains stale data
4. Verify Hebrew content preservation across all storage layers

The analysis reveals:
- Multiple IndexedDB database versions (flow-state v1, v2, v3)
- Data inconsistencies between storage layers
- Stale data sources being read by backup system
- Unicode handling issues in backup/restore cycles

### Workflow 2: Real-time Sync Monitoring
Monitor data flow and synchronization timing:

1. Use `assets/debug-templates/sync-monitor.html` for real-time monitoring
2. Track Pinia store mutations vs IndexedDB writes
3. Verify backup system reads current data, not cached state
4. Detect async timing issues and race conditions

Monitor for:
- Pinia store changes not persisting to IndexedDB
- Backup system reading from stale data sources
- Async timing conflicts between store updates and backup creation
- Data races in multi-tab scenarios

### Workflow 3: Data Consistency Verification
Systematic verification of data integrity:

1. Execute `scripts/trace-data-flow.js` to trace data path
2. Compare UI → Pinia → IndexedDB → Backup pipeline
3. Test Hebrew content preservation through entire flow
4. Verify backup/restore cycles with actual user data

Verify consistency across:
- UI task count vs Pinia store count
- Pinia store count vs IndexedDB count
- IndexedDB count vs backup system count
- Hebrew Unicode integrity through all layers

## Key Debugging Tools

### Database Analysis Script
`scripts/analyze-database.js` provides comprehensive database inspection:

```bash
# Analyze all IndexedDB databases and versions
node scripts/analyze-database.js

# Output includes:
# - Database versions and schemas
# - Task counts per database
# - Data consistency checks
# - Hebrew content verification
```

### Data Flow Tracer
`scripts/trace-data-flow.js` tracks data movement:

```bash
# Trace complete data flow pipeline
node scripts/trace-data-flow.js

# Identifies:
# - Data synchronization breaks
# - Stale data sources
# - Async timing issues
# - Unicode handling problems
```

### Real-time Monitor
`assets/debug-templates/sync-monitor.html` provides live monitoring:
- Real-time Pinia store observation
- IndexedDB change tracking
- Backup system data source verification
- Live synchronization status display

## Common Issues and Solutions

### Issue: Backup System Reading Stale Data
**Problem**: Backup system reports old task counts (e.g., 22 tasks) while UI shows current data (e.g., 4 tasks)

**Debug Steps**:
1. Run database analysis to identify multiple database versions
2. Check which version backup system is reading from
3. Verify Pinia store ↔ IndexedDB synchronization
4. Test manual backup creation timing

**Solution**: Ensure backup system reads from latest IndexedDB version and waits for Pinia → IndexedDB sync completion.

### Issue: Hebrew Content Loss
**Problem**: Hebrew characters corrupted or lost during backup/restore

**Debug Steps**:
1. Test Unicode preservation through JSON serialization
2. Verify IndexedDB stores UTF-8 correctly
3. Check backup system string handling
4. Test restore process with actual Hebrew content

**Solution**: Implement proper Unicode handling and verify UTF-8 encoding throughout pipeline.

### Issue: Async Timing Conflicts
**Problem**: Pinia store updates not reflected in backups due to timing

**Debug Steps**:
1. Monitor Pinia store mutation timing
2. Track IndexedDB write completion
3. Verify backup system waits for data persistence
4. Test rapid state changes

**Solution**: Implement proper async coordination between Pinia updates, IndexedDB writes, and backup creation.

## Implementation Guidelines

### Database Analysis Script Requirements:
- Support multiple IndexedDB database versions
- Compare task counts across storage layers
- Verify Hebrew Unicode content preservation
- Identify data source inconsistencies

### Data Flow Tracing Requirements:
- Track UI → Pinia → IndexedDB → Backup pipeline
- Detect synchronization breakpoints
- Monitor async operation timing
- Verify Unicode handling at each stage

### Real-time Monitoring Requirements:
- Live Pinia store observation
- IndexedDB change detection
- Backup system data source verification
- Visual sync status indicators

## Expected Outcomes

Using this skill will identify:
- Exact point where backup data diverges from actual user data
- Which IndexedDB database version contains current vs stale data
- Pinia store synchronization timing issues
- Hebrew content preservation problems in backup pipeline
- Root cause of data consistency issues between application layers

The systematic approach provided by this skill enables precise diagnosis and resolution of IndexedDB backup synchronization problems in Vue.js applications.

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
