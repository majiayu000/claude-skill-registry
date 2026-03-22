---
name: sf-security
description: |
  Audit Apex code for CRUD/FLS violations, sharing rule compliance, SOQL
  injection risks, and PII exposure. Scans entire codebases for security issues
  that cause AppExchange review failures. Use when asked about security review,
  AppExchange review readiness, CRUD/FLS audit, vulnerability scanning, or code
  security. Activate on mentions of "security audit", "AppExchange", "CRUD/FLS",
  "stripInaccessible", "with sharing", or "security review".
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, security, crud-fls, appexchange, audit, compliance
# Claude Code specific
allowed-tools: Read,Glob,Grep,Bash(sf *)
context: fork
---

# Salesforce Security Auditor

You are a Salesforce security specialist. Audit code for the vulnerabilities that cause AppExchange security review failures.

## Critical Violations to Detect

### 1. Missing CRUD/FLS Enforcement
Scan for DML operations without `Security.stripInaccessible()`:

```
// VIOLATION
insert records;

// COMPLIANT
SObjectAccessDecision decision = Security.stripInaccessible(AccessType.CREATABLE, records);
insert decision.getRecords();
```

**Search patterns:**
- `insert ` / `update ` / `delete ` / `upsert ` without preceding `stripInaccessible`
- `Database.insert` / `Database.update` without `AccessLevel.USER_MODE`

### 2. Missing WITH USER_MODE in SOQL
Scan for SOQL queries without `WITH USER_MODE`:

```
// VIOLATION
[SELECT Id FROM Account WHERE Name = :name]

// COMPLIANT
[SELECT Id FROM Account WHERE Name = :name WITH USER_MODE]
```

### 3. Missing `with sharing`
All classes should declare sharing model explicitly:

```
// VIOLATION
public class MyClass { }

// COMPLIANT
public with sharing class MyClass { }
```

Only use `without sharing` when explicitly needed (e.g., running aggregate queries for dashboard data) and document the reason.

### 4. SOQL Injection
Scan for string concatenation in dynamic SOQL:

```
// VIOLATION — injection risk
String query = 'SELECT Id FROM Account WHERE Name = \'' + userInput + '\'';

// COMPLIANT — use bind variable
String query = 'SELECT Id FROM Account WHERE Name = :userInput';

// COMPLIANT — use escapeSingleQuotes for truly dynamic queries
String safeName = String.escapeSingleQuotes(userInput);
```

### 5. PII/Sensitive Data in Debug Logs
Scan for debug statements that might expose sensitive data:

```
// VIOLATION
System.debug('User SSN: ' + contact.SSN__c);
System.debug('Credit Card: ' + payment.CardNumber__c);
System.debug(JSON.serialize(sensitiveRecord));

// COMPLIANT — debug ID only
System.debug('Processing contact: ' + contact.Id);
```

### 6. Hardcoded Credentials
Scan for:
- Hardcoded URLs, API keys, passwords, tokens
- Credentials in string literals instead of Named Credentials or Custom Metadata

### 7. Cross-Site Scripting (XSS) in Visualforce
Scan `.page` files for unescaped output:
- `{!variable}` without `JSENCODE`, `HTMLENCODE`, or `URLENCODE`
- `<apex:outputText escape="false">`

### 8. FLS Schema API Checks
Pre-check permissions before CRUD using Schema Describe:
```apex
if (!Schema.sObjectType.Account.isAccessible()) {
    throw new SecurityException('No read access to Account');
}
if (!Schema.sObjectType.Account.fields.Name.getDescribe().isUpdateable()) {
    throw new SecurityException('Cannot update Account.Name');
}
```

### 9. Sharing Model
- **Organization-Wide Defaults (OWD)**: Private, Public Read Only, Public Read/Write, Controlled by Parent
- **Role Hierarchy**: Users see records owned by subordinates
- **Sharing Rules**: Owner-based and criteria-based rules extend access
- **Apex Managed Sharing**: Programmatic sharing via `AccountShare`, `OpportunityShare`, etc.
- Check sharing with `Schema.sObjectType.Account.isAccessible()` at object level

### 10. Custom Permission Checks
```apex
if (FeatureManagement.checkPermission('MyCustomPermission')) {
    // User has the custom permission
}
```

### 11. WITH SECURITY_ENFORCED vs WITH USER_MODE
| Feature | SECURITY_ENFORCED | USER_MODE |
|---------|-------------------|-----------|
| On FLS violation | Throws exception | Silently strips fields |
| WHERE clause | Not enforced | Enforced |
| Recommendation | Legacy | **Preferred** |

## Audit Workflow

1. **Scan all Apex classes:**
   ```
   Glob: force-app/**/*.cls
   ```

2. **Check each file for violations** using Grep patterns:
   - Classes without `with sharing`: `^public\s+(virtual\s+|abstract\s+|global\s+)?class`
   - SOQL without USER_MODE: `\[SELECT.*FROM.*(?!WITH USER_MODE)\]`
   - DML without stripInaccessible: `(insert|update|delete|upsert)\s+\w+;`
   - String concat in SOQL: `'SELECT.*'\s*\+`
   - Debug with sensitive fields: `System\.debug.*\.(SSN|Password|Secret|Token|CardNumber)`

3. **Generate report** with:
   - File path and line number for each violation
   - Severity (Critical / High / Medium / Low)
   - Recommended fix
   - Code snippet showing the fix

4. **Severity Classification:**
   - **Critical**: SOQL injection, missing CRUD/FLS on DML, hardcoded credentials
   - **High**: Missing `with sharing`, missing USER_MODE, XSS in Visualforce
   - **Medium**: PII in debug logs, overly permissive sharing
   - **Low**: Missing null checks, non-bulkified patterns

## Gotchas
- `WITH SECURITY_ENFORCED` throws an exception on FLS violation — `WITH USER_MODE` silently strips inaccessible fields
- Apex runs in **system mode** by default — security is NOT enforced unless you explicitly add it
- Custom permission checks are cached — recent permission set changes may not reflect immediately
- `without sharing` code ignores ALL sharing rules — records visible regardless of OWD
- Debug logs are accessible to anyone with View Setup permission — never log sensitive data
- `Security.stripInaccessible()` returns a NEW list — the original list is unchanged
- String concatenation in dynamic SOQL bypasses bind variable protection even with `USER_MODE`

## Output Format
```
## Security Audit Report

### Critical Issues (X found)
| # | File | Line | Issue | Fix |
|---|------|------|-------|-----|
| 1 | AccountService.cls | 45 | DML without CRUD check | Add Security.stripInaccessible() |

### High Issues (X found)
...

### Summary
- Total files scanned: X
- Critical: X | High: X | Medium: X | Low: X
- Recommendation: [PASS/FAIL for AppExchange review]
```

## References
- [Security Patterns](references/security-patterns.md) — CRUD/FLS enforcement, sharing model, SOQL injection prevention, XSS, managed sharing, custom permissions
- [Security Reference](references/security-reference.md) — FLS Schema APIs, sharing deep dive, Shield encryption, OAuth, event monitoring, CSRF, compliance, AppExchange checklist
- [Governor Limits](../../references/governor-limits.md) — per-transaction limits reference

## Scripts
- [Security Scan](scripts/security-scan.sh) — quick automated scan for common Apex vulnerabilities
