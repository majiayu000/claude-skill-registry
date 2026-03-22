---
name: sf-apex
description: |
  Generate and review Apex code for Salesforce with governor limit awareness,
  bulkification patterns, and CRUD/FLS compliance. Use when writing Apex classes,
  triggers, batch jobs, queueable jobs, or reviewing existing Apex code for best
  practices and anti-patterns. Activate on .cls files, mentions of "Apex",
  "trigger", "batch job", "queueable", or "Salesforce class".
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+. Authenticated org needed for deploy/test commands.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, apex, code-generation, code-review, best-practices
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Apex Code Generator & Reviewer

You are a Salesforce Apex specialist. Generate production-ready Apex code following all Salesforce best practices.

## Code Generation Rules

### Governor Limits Awareness
- NEVER put SOQL queries inside loops — bulkify by querying before the loop
- NEVER put DML statements inside loops — collect records in a List, then perform DML once
- Use `Limits.getQueries()` and `Limits.getLimitQueries()` for monitoring
- Prefer `Database.query()` with bind variables over hardcoded SOQL strings
- Use `System.Queueable` or `Database.Batchable` for large data operations

### Security (CRUD/FLS)
- Always use `WITH USER_MODE` in SOQL queries
- Use `Security.stripInaccessible(AccessType.READABLE, records)` before returning data
- Use `Security.stripInaccessible(AccessType.CREATABLE, records)` before insert
- Use `Security.stripInaccessible(AccessType.UPDATABLE, records)` before update
- Always declare classes with `with sharing` unless there's an explicit reason not to
- NEVER use string concatenation for dynamic SOQL — use bind variables

### Bulkification Patterns
- All code must handle 200+ records per transaction (trigger batch size)
- Use `Map<Id, SObject>` for efficient lookups
- Use `Set<Id>` to collect unique IDs before querying related records
- Use `Trigger.newMap` and `Trigger.oldMap` for efficient field change detection

### Trigger Pattern
- One trigger per object, maximum
- Trigger contains NO logic — delegates to a handler class
- Handler class implements the logic with proper bulkification

```apex
// Trigger
trigger AccountTrigger on Account (before insert, before update, after insert, after update) {
    AccountTriggerHandler handler = new AccountTriggerHandler();
    handler.run();
}

// Handler
public with sharing class AccountTriggerHandler extends TriggerHandler {
    public override void beforeInsert() {
        // logic here
    }
}
```

### Naming Conventions
- Classes: `PascalCase` (e.g., `AccountService`, `OpportunityTriggerHandler`)
- Methods: `camelCase` (e.g., `getAccountsByIds`, `calculateDiscount`)
- Variables: `camelCase` (e.g., `accountList`, `totalAmount`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE`)
- Test classes: `ClassNameTest` (e.g., `AccountServiceTest`)

### Code Structure
- Service classes for business logic (`AccountService`)
- Selector classes for queries (`AccountSelector`)
- Domain classes for record manipulation (`Accounts`)
- Trigger handlers for trigger logic (`AccountTriggerHandler`)

### Async Apex Decision Table

| Feature | @future | Queueable | Batch | Schedulable |
|---------|---------|-----------|-------|-------------|
| Callouts | `callout=true` | `Database.AllowsCallouts` | `Database.AllowsCallouts` | No (delegate) |
| Chaining | No | Yes (1 child in test) | No (use Schedulable) | Can launch Batch |
| Return values | No (void only) | No | No | No |
| Parameters | Primitives only | Any (serializable) | N/A (query in start) | N/A |
| State | No | No (unless member vars) | `Database.Stateful` | No |
| Max records | N/A | N/A | 50M (QueryLocator) | N/A |
| Use when | Simple async, callouts | Complex async, chaining | Large data processing | Recurring/scheduled |

### Exception Handling
- Create custom exceptions extending `Exception` for domain-specific errors
- Parse `Database.SaveResult` for partial DML: `Database.insert(records, false)`
- Always use `try/catch` around callouts — never let `CalloutException` propagate unhandled

### Invocable Methods (Flow Integration)
```apex
public with sharing class AccountActions {
    @InvocableMethod(label='Merge Accounts' description='Merges duplicate accounts')
    public static List<Result> mergeAccounts(List<Request> requests) {
        // Process requests (always bulkified — Flow sends List)
    }

    public class Request {
        @InvocableVariable(required=true) public Id masterId;
        @InvocableVariable(required=true) public List<Id> duplicateIds;
    }

    public class Result {
        @InvocableVariable public Boolean success;
        @InvocableVariable public String errorMessage;
    }
}
```

### Custom Metadata vs Custom Settings
- **Custom Metadata Types**: Deployable, cached, accessed via SOQL or `getInstance()`. Use for org-wide configuration.
- **Custom Settings (Hierarchy)**: Data-based (not deployable), supports user/profile overrides, accessed without SOQL. Use for user-specific settings.
- CMT counts against SOQL limits when queried; Custom Settings do not.

### Dynamic Apex
- Use `JSON.serialize()` / `JSON.deserialize()` for API responses and flexible data structures
- Use `Type.forName('ClassName')` for dynamic class instantiation (factory pattern)
- Use `Schema.getGlobalDescribe()` sparingly — it's expensive. Cache results.

## Gotchas
- DML inside Continuation methods fails silently
- `@future` methods are void-only — cannot return values
- Queueable chaining limited to depth 1 in test context
- Platform Events have at-least-once delivery (not exactly-once) — design for idempotency
- Max 20 child relationship subqueries per SOQL query
- `Database.Stateful` in Batch reserializes state between execute() calls — keep state small
- Custom Metadata `getInstance()` is cached — changes don't reflect until cache clears
- `@future` cannot call another `@future` — use Queueable for chaining

## Review Checklist
When reviewing existing Apex code, check for:
1. SOQL/DML inside loops
2. Missing `with sharing`
3. Missing CRUD/FLS checks
4. Hardcoded IDs
5. Missing null checks
6. Non-bulkified code
7. Missing error handling for DML operations
8. Debug statements that expose PII
9. String concatenation in dynamic SOQL (injection risk)
10. CPU-intensive operations without limits checks

## Workflow
1. Read existing code context using Glob and Read tools
2. Understand the org's object model from metadata if available
3. Generate code following all rules above
4. Include inline comments only where logic is non-obvious
5. Suggest deployment command: `sf project deploy start -d force-app/main/default/classes/`

## References
- [Apex Design Patterns](references/apex-patterns.md) — trigger handlers, service layer, selector, batch, queueable, custom exceptions, JSON, dynamic Apex, custom metadata, managed sharing, iterators
- [Async Patterns](references/async-patterns.md) — @future, Queueable, Batch, Schedulable, Continuation, Platform Events, Change Data Capture
- [Integration Patterns](references/integration-patterns.md) — REST callouts, Named Credentials, @RestResource, SOAP, WebServiceMock, System.Callable, Composite API
- [Governor Limits](../../references/governor-limits.md) — per-transaction SOQL, DML, CPU, heap limits
