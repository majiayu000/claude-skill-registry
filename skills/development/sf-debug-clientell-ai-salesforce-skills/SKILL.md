---
name: sf-debug
description: |
  Debug and troubleshoot Salesforce applications using debug logs, governor limit
  monitoring, error diagnosis, and performance profiling. Use when analyzing debug
  logs, diagnosing governor limit violations, interpreting stack traces, resolving
  common Salesforce errors, or profiling Apex performance. Activate on .log files,
  mentions of "debug", "governor limit", "error", "exception", "troubleshoot",
  "stack trace", or "performance issue".
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+. Authenticated org needed for log retrieval and trace flag commands.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, debug, troubleshooting, governor-limits, error-diagnosis, performance
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Salesforce Debug & Troubleshooting Specialist

You are a Salesforce debugging expert. Diagnose issues from debug logs, governor limit violations, exceptions, and performance bottlenecks. Provide root-cause analysis and actionable fixes.

## 1. Debug Log Analysis

### Log Levels (from most to least verbose)

| Level | Use Case |
|-------|----------|
| FINEST | Full trace — variable values, internal framework calls |
| FINER | Detailed flow — method entries/exits with parameters |
| FINE | Key decision points and loop iterations |
| DEBUG | General diagnostic information |
| INFO | High-level transaction milestones |
| WARN | Recoverable issues that may indicate problems |
| ERROR | Failures requiring immediate attention |

### Log Categories

| Category | What It Captures |
|----------|-----------------|
| `Apex_code` | Apex execution, System.debug() output, variable assignments |
| `Apex_profiling` | Cumulative resource usage — SOQL, DML, CPU, heap |
| `Database` | SOQL queries, DML operations, query plans, row counts |
| `System` | System methods, platform events, formula evaluations |
| `Validation` | Validation rules, workflow field updates |
| `Workflow` | Workflow rules, process builder, flow executions |
| `Callout` | HTTP callouts, SOAP calls, external service responses |
| `Visualforce` | VF page rendering, view state, controller actions |
| `NBA` | Next Best Action strategy execution |

### Reading Debug Logs — Key Line Prefixes

```
EXECUTION_STARTED / EXECUTION_FINISHED — transaction boundaries
CODE_UNIT_STARTED / CODE_UNIT_FINISHED — trigger, class, or method execution
SOQL_EXECUTE_BEGIN / SOQL_EXECUTE_END — query with row count
DML_BEGIN / DML_END — DML operation with row count
EXCEPTION_THROWN — exception type and message
FATAL_ERROR — unrecoverable error with stack trace
HEAP_ALLOCATE — heap memory allocation
LIMIT_USAGE_FOR_NS — governor limit summary per namespace
CUMULATIVE_LIMIT_USAGE — end-of-transaction limit summary
USER_DEBUG — System.debug() output
VARIABLE_SCOPE_BEGIN / VARIABLE_ASSIGNMENT — variable tracking (FINEST)
METHOD_ENTRY / METHOD_EXIT — method call tracking (FINER+)
FLOW_START_INTERVIEWS — flow/process builder execution
VALIDATION_RULE — validation rule evaluation
CALLOUT_REQUEST / CALLOUT_RESPONSE — external HTTP calls
```

### Log Structure

A debug log follows this sequence:
1. `EXECUTION_STARTED` — transaction begins
2. `CODE_UNIT_STARTED` — trigger or entry point fires
3. Before-trigger logic (validation, field updates)
4. DML execution and after-trigger logic
5. Workflow rules, process builder, flows
6. Re-evaluation of before/after triggers if workflow causes field updates
7. Commit or rollback
8. `CUMULATIVE_LIMIT_USAGE` — final governor limit summary
9. `EXECUTION_FINISHED` — transaction ends

## 2. Governor Limit Monitoring

### Limits Class Methods — Check Before Hitting Walls

```apex
// SOQL
System.debug('SOQL queries: ' + Limits.getQueries() + ' / ' + Limits.getLimitQueries());

// DML
System.debug('DML statements: ' + Limits.getDmlStatements() + ' / ' + Limits.getLimitDmlStatements());
System.debug('DML rows: ' + Limits.getDmlRows() + ' / ' + Limits.getLimitDmlRows());

// CPU
System.debug('CPU time (ms): ' + Limits.getCpuTime() + ' / ' + Limits.getLimitCpuTime());

// Heap
System.debug('Heap size (bytes): ' + Limits.getHeapSize() + ' / ' + Limits.getLimitHeapSize());

// Query rows
System.debug('Query rows: ' + Limits.getQueryRows() + ' / ' + Limits.getLimitQueryRows());

// Callouts
System.debug('Callouts: ' + Limits.getCallouts() + ' / ' + Limits.getLimitCallouts());

// Future calls
System.debug('Future calls: ' + Limits.getFutureCalls() + ' / ' + Limits.getLimitFutureCalls());

// Queueable jobs
System.debug('Queueable jobs: ' + Limits.getQueueableJobs() + ' / ' + Limits.getLimitQueueableJobs());
```

### When to Check Limits

- **Before expensive operations** — query or DML in a loop you cannot refactor immediately
- **After processing batches** — at the end of each batch in `Database.Batchable.execute()`
- **In utility/service classes** — log limits at entry and exit for profiling
- **In catch blocks** — when a LimitException might be approaching
- **Never in tight loops** — `Limits.*()` calls themselves consume CPU

### Sync vs Async Limits

| Resource | Synchronous | Asynchronous (Batch/Future/Queueable) |
|----------|------------|---------------------------------------|
| SOQL queries | 100 | 200 |
| DML statements | 150 | 150 |
| CPU time | 10,000 ms | 60,000 ms |
| Heap size | 6 MB | 12 MB |
| Query rows | 50,000 | 50,000 |
| Callouts | 100 | 100 |
| DML rows | 10,000 | 10,000 |

## 3. Common Error Diagnosis

| Error | Likely Cause | Fix Direction |
|-------|-------------|---------------|
| `UNABLE_TO_LOCK_ROW` | Concurrent updates on same record or parent record in master-detail | Retry with `FOR UPDATE`, reduce batch scope, use async processing, avoid updating parent records unnecessarily |
| `ENTITY_IS_DELETED` | DML on a record that was deleted earlier in the same transaction or by another user | Check `isDeleted` before DML, handle concurrency with try/catch, verify trigger order |
| `FIELD_CUSTOM_VALIDATION_EXCEPTION` | Validation rule failure | Check validation rules on the object, ensure field values meet all criteria, use `Database.insert(records, false)` for partial success |
| `INSUFFICIENT_ACCESS_ON_CROSS_REFERENCE_ENTITY` | Missing access to a related record (lookup/master-detail parent, owner, queue) | Verify sharing rules, check OWD, ensure running user has access to related records, use `without sharing` only with explicit justification |
| `MIXED_DML_OPERATION` | DML on setup object (User, Group) and non-setup object in same transaction | Move one DML to `@future`, use `System.runAs()` in tests, separate into different transactions |
| `System.LimitException: Too many SOQL queries` | More than 100 SOQL queries in synchronous transaction | Move queries out of loops, use collections and Maps for lookups, use SOQL for-loops for large datasets |
| `System.LimitException: Too many DML statements` | More than 150 DML statements in transaction | Collect records into Lists, perform bulk DML outside loops |
| `System.CalloutException` | HTTP callout failure — timeout, invalid endpoint, certificate issue | Check Named Credential config, verify endpoint URL, handle timeout with retry, check remote site settings |
| `System.NullPointerException` | Accessing method/property on a null reference | Add null checks before access, use safe navigation operator `?.`, verify SOQL returns results before accessing |
| `System.QueryException: List has no rows` | `[SELECT ... LIMIT 1]` returned no rows assigned to single sObject variable | Use `List<SObject>` and check `.isEmpty()`, or wrap in try/catch |
| `System.QueryException: List has more than 1 row` | Query assigned to single variable returned multiple rows | Add `LIMIT 1` or use `List<SObject>`, investigate data — duplicates may indicate a data quality issue |
| `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` | Trigger recursion or cascading trigger failure | Implement static recursion guard, check trigger handler framework for re-entrancy protection |
| `System.AsyncException` | Too many async jobs enqueued, or chaining limit hit | Check `Limits.getQueueableJobs()`, use `Finalizer` for batch chaining, limit enqueue to 1 per Queueable |
| `System.SerializationException` | Unserializable object in Queueable or Platform Event | Remove transient references, avoid SObject types with relationship fields in serialized state |
| `STRING_TOO_LONG` | Field value exceeds maximum length | Validate or truncate with `.abbreviate(maxLength)` before DML |

### Error Diagnosis Workflow

1. **Read the full error message** — Salesforce errors follow `STATUS_CODE: message` format
2. **Find the originating line** — look for `Class.MethodName: line X, column Y` in stack trace
3. **Identify the trigger context** — is this before/after insert/update? Check `CODE_UNIT_STARTED`
4. **Check for cascading failures** — one trigger failure can cause `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` in a parent trigger
5. **Reproduce with minimal data** — use Execute Anonymous or a focused test method

## 4. Debug Log CLI Commands

### Tail Logs in Real Time
```bash
# Stream logs as they are generated (colored output)
sf apex tail log --target-org myOrg --color

# Tail with specific log level
sf apex tail log --target-org myOrg --debug-level MyDebugLevel
```

### List and Retrieve Logs
```bash
# List recent debug logs
sf apex log list --target-org myOrg --json

# Get a specific log by ID
sf apex log get --log-id 07Lxxxxxxxxxxxxxxx --target-org myOrg

# Get the most recent log
sf apex log get --number 1 --target-org myOrg

# Get logs and save to file for analysis
sf apex log get --log-id 07Lxxxxxxxxxxxxxxx --target-org myOrg > debug.log
```

### Run Apex with Debug Output
```bash
# Execute anonymous Apex and capture output
sf apex run --target-org myOrg --file scripts/debug-script.apex

# Run inline Apex for quick debugging
echo "System.debug(Limits.getQueries());" | sf apex run --target-org myOrg
```

### Delete Old Logs
```bash
# Clean up old logs to free storage
sf apex log list --target-org myOrg --json | \
  sf data delete bulk --sobject ApexLog --file -
```

## 5. Checkpoint & Developer Console Debugging

### Execute Anonymous Debugging

Use Execute Anonymous for targeted investigation:

```apex
// Reproduce an issue with specific data
Account testAcc = [SELECT Id, Name, Industry FROM Account WHERE Id = '001xxxxxxxxxxxx'];
System.debug('Account state: ' + JSON.serializePretty(testAcc));

// Test a specific method in isolation
MyService service = new MyService();
try {
    service.processRecord(testAcc);
    System.debug('SUCCESS: Method completed without error');
} catch (Exception e) {
    System.debug('FAILED: ' + e.getTypeName() + ' - ' + e.getMessage());
    System.debug('Stack trace: ' + e.getStackTraceString());
}

// Check governor limits after operation
System.debug('Post-execution SOQL: ' + Limits.getQueries());
System.debug('Post-execution DML: ' + Limits.getDmlStatements());
System.debug('Post-execution CPU: ' + Limits.getCpuTime() + 'ms');
```

### Checkpoints (Developer Console)

- Set checkpoints on specific lines in Developer Console
- Checkpoints capture heap state, local variables, and static variables at that execution point
- Maximum 5 checkpoints active at a time
- Checkpoints expire after 30 minutes
- Results appear in the Checkpoint Inspector tab
- Use checkpoints when System.debug() is insufficient — they capture the full object graph

### SOQL Query Debugging in Developer Console

```
Query Editor → Execute SOQL/SOSL directly
Logs tab → Filter by "DATABASE" events to see query performance
Query Plan tool → Use Tooling API: /services/data/vXX.0/query?explain=SELECT ...
```

## 6. Performance Profiling

### Identifying CPU Bottlenecks

Look for these patterns in debug logs:
- `METHOD_ENTRY` / `METHOD_EXIT` — calculate time between pairs
- High `CUMULATIVE_LIMIT_USAGE` CPU time relative to the operation size
- `HEAP_ALLOCATE` in large amounts inside loops

### Common Performance Anti-Patterns

| Anti-Pattern | Log Signal | Fix |
|-------------|-----------|-----|
| SOQL in loop | Repeated `SOQL_EXECUTE_BEGIN` in same code unit | Query before loop, use Map for lookups |
| DML in loop | Repeated `DML_BEGIN` in same code unit | Collect into List, DML once after loop |
| Large heap allocation | `HEAP_ALLOCATE` with large byte counts in loops | Use SOQL for-loop, process in batches |
| Expensive describe calls | Repeated `Schema.getGlobalDescribe()` | Cache in static variable |
| String concatenation in loop | Rising heap, CPU time | Use `String.join()` or `List<String>` |
| Unfiltered SOQL | `SOQL_EXECUTE_END` with high row count | Add WHERE filters, use selective indexed fields |
| Nested loops over collections | High CPU, no SOQL/DML signal | Use Map-based lookups, reduce O(n^2) to O(n) |

### CPU Time Profiling Pattern

```apex
Long startCpu = Limits.getCpuTime();
// ... operation under test ...
Long endCpu = Limits.getCpuTime();
System.debug('CPU consumed: ' + (endCpu - startCpu) + 'ms for operation X');
```

### Heap Profiling Pattern

```apex
Integer heapBefore = Limits.getHeapSize();
// ... operation under test ...
Integer heapAfter = Limits.getHeapSize();
System.debug('Heap delta: ' + (heapAfter - heapBefore) + ' bytes for operation X');
```

## 7. Trace Flags

### Setting Up Trace Flags via CLI

```bash
# Create a debug level first
sf data create record --sobject DebugLevel --target-org myOrg \
  --values "DeveloperName='DetailedDebug' MasterLabel='Detailed Debug' \
  ApexCode='FINE' ApexProfiling='FINEST' Database='FINE' System='DEBUG' \
  Validation='INFO' Workflow='INFO' Callout='INFO' Visualforce='INFO'"

# Query the debug level ID
sf data query --query "SELECT Id FROM DebugLevel WHERE DeveloperName='DetailedDebug'" \
  --target-org myOrg --json

# Create a trace flag for a specific user (lasts up to 24 hours)
sf data create record --sobject TraceFlag --target-org myOrg \
  --values "TracedEntityId='005xxxxxxxxxxxx' DebugLevelId='7dlxxxxxxxxxxxx' \
  LogType='USER_DEBUG' StartDate='2026-03-20T00:00:00.000Z' \
  ExpirationDate='2026-03-20T23:59:59.000Z'"
```

### Trace Flag Types

| LogType | Traces |
|---------|--------|
| `USER_DEBUG` | All transactions by a specific user |
| `CLASS_TRACING` | Executions involving a specific Apex class |
| `DEVELOPER_LOG` | Current Developer Console session |

### Trace Flag via Setup UI

1. Setup > Debug Logs > New
2. Select traced entity (User, Apex Class, Apex Trigger)
3. Set start/end time (max 24 hours)
4. Select debug level
5. Save — logs will be captured until expiration or 20 logs generated (whichever first)

## 8. Gotchas

### Debug Log Truncation
- Debug logs are truncated at **20 MB** — large transactions will lose the beginning of the log
- The log shows `*** Skipped N bytes of detailed log` when truncated
- To avoid: reduce log levels on categories you do not need, set non-essential categories to NONE or ERROR
- Truncated logs still include `CUMULATIVE_LIMIT_USAGE` at the end

### Log Retention
- Debug logs are retained for only **24 hours** (or until 20 logs accumulate per trace flag)
- Download critical logs immediately for post-mortem analysis
- Use `sf apex log get` to save logs to local files before they expire

### Trace Flag Expiry
- Trace flags have a maximum duration of **24 hours**
- They silently stop capturing logs after expiration — no warning
- Re-create trace flags before reproducing intermittent issues
- Maximum 250 MB of debug logs per org (oldest are purged first)

### Performance Impact of Debugging
- `System.debug()` statements consume CPU time even in production
- Writing to the debug log adds overhead — high log levels slow execution
- Log levels at FINEST can **double** CPU time for complex transactions
- Remove or guard debug statements before deploying to production:
  ```apex
  // Use a custom setting or custom metadata to gate debug output
  if (DebugSettings__c.getInstance().EnableDetailedLogging__c) {
      System.debug(LoggingLevel.FINE, 'Detailed: ' + JSON.serialize(records));
  }
  ```

### System.debug() in Production
- Debug statements are **not** captured unless a trace flag is active on the running user
- They still consume CPU time regardless of whether a trace flag is set
- Never use `System.debug()` with sensitive data (PII, credentials, tokens)
- Prefer custom logging frameworks (Platform Events + Big Objects) for production observability

### Other Traps
- `System.debug()` calls `toString()` on the argument — this can throw NullPointerException if the object graph has null references
- Aggregate queries (`COUNT()`, `SUM()`) consume 1 query row per aggregate result
- `Database.setSavepoint()` and `Database.rollback()` count as DML statements
- Trigger.new is read-only in after triggers — modifying it throws a runtime error
- Tests with `@isTest(SeeAllData=true)` can pass in dev but fail in CI due to data differences

## 9. Debugging Workflow

### Step-by-Step Process

1. **Reproduce the issue**
   - Identify the exact user action, API call, or automated process that fails
   - Note the timestamp window and the user experiencing the issue

2. **Set up trace flags**
   ```bash
   # Ensure trace flag is active for the user
   sf apex tail log --target-org myOrg --color
   ```

3. **Trigger the issue and capture the log**
   - Reproduce via UI, API, or Execute Anonymous
   - Save the log immediately: `sf apex log get --number 1 --target-org myOrg > issue.log`

4. **Scan for errors first**
   - Search for `EXCEPTION_THROWN`, `FATAL_ERROR`, and `LIMIT_USAGE` in the log
   - If truncated, focus on `CUMULATIVE_LIMIT_USAGE` at the end

5. **Trace the execution path**
   - Find `CODE_UNIT_STARTED` to identify which triggers/classes executed
   - Track the order: before triggers, DML, after triggers, workflows, process builder, flows

6. **Check governor limits**
   - Look at `LIMIT_USAGE_FOR_NS` — are any limits above 70%?
   - Cross-reference SOQL count with the number of `SOQL_EXECUTE_BEGIN` events

7. **Identify the root cause**
   - Is it a data issue? (missing record, null field)
   - Is it a logic issue? (wrong condition, missing bulkification)
   - Is it a limits issue? (SOQL in loop, DML in loop)
   - Is it a concurrency issue? (record locking, race condition)
   - Is it a configuration issue? (validation rule, sharing rule, permission)

8. **Fix and verify**
   - Apply the smallest correct fix
   - Re-run with trace flag active to confirm the issue is resolved
   - Check that governor limits improved (not just that the error went away)

### Quick Diagnosis Commands

```bash
# Search for errors in a saved log
grep -E "EXCEPTION_THROWN|FATAL_ERROR|LIMIT_USAGE" debug.log

# Count SOQL queries in log (look for loops)
grep -c "SOQL_EXECUTE_BEGIN" debug.log

# Count DML operations in log
grep -c "DML_BEGIN" debug.log

# Find slow queries (queries returning many rows)
grep "SOQL_EXECUTE_END" debug.log | grep -E "Rows:[0-9]{3,}"
```

## 10. Cross-Skill Integration

| Need | Delegate to | Reason |
|------|-------------|--------|
| Fix Apex code | [sf-apex](../sf-apex/SKILL.md) | Code change generation and review |
| Write/run tests | [sf-testing](../sf-testing/SKILL.md) | Test execution, coverage, assertions |
| Deploy fix | [sf-deploy](../sf-deploy/SKILL.md) | Deployment orchestration |
| Data investigation | [sf-data](../sf-data/SKILL.md) | Query and inspect org data |
| Security audit | [sf-security](../sf-security/SKILL.md) | CRUD/FLS and sharing review |

## References
- [Debug Reference](references/debug-reference.md) -- Limits class methods, log parsing patterns, Execute Anonymous patterns, error handling, performance profiling, Tooling API trace flags
- [Governor Limits](../../references/governor-limits.md) -- per-transaction SOQL, DML, CPU, heap limits
