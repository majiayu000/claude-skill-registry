<!-- SOURCE-OF-TRUTH: shared/references/output_normalization.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Output Normalization

<!-- SCOPE: Shared reference for normalizing, deduplicating, and grouping CLI output before presenting to agent or truncating. -->

## 1. Message Normalization Rules

Replace runtime-specific values with placeholders to enable grouping of identical errors. Apply in listed order.

| Pattern | Replacement | Regex |
|---------|-------------|-------|
| UUID | `<UUID>` | `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` |
| ISO timestamp | `<TS>` | `\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}` |
| US timestamp | `<TS>` | `\d{2}-\d{2}-\d{4}\s\d{2}:\d{2}:\d{2}` |
| IP address | `<IP>` | `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?` |
| Path ID segment | `/<ID>` | `/[0-9a-f]{8,}` |
| Large number | `<N>` | `\b\d{3,}\b` |
| Trace ID | `trace_id=<TRACE>` | `trace_id=[0-9a-fA-F]{1,8}` |

## 2. Deduplication Protocol

After normalization, group identical lines:

```
1. Normalize all output lines per §1 rules
2. Group identical normalized lines
3. For each group with count > 1:
   - Keep ONE representative line
   - Append suffix: "(x{count})"
4. Sort groups by count descending (most frequent first)
```

**Example:**
```
# Before (6 lines):
Error connecting to 192.168.1.10:5432 - timeout after 30000ms
Error connecting to 192.168.1.11:5432 - timeout after 30001ms
Error connecting to 192.168.1.12:5432 - timeout after 29998ms
ImportError: No module named 'foo.bar'
ImportError: No module named 'foo.baz'
AssertionError: expected 42, got 0

# After normalization + dedup (3 lines):
Error connecting to <IP> - timeout after <N>ms  (x3)
ImportError: No module named 'foo.bar'  (x2)
AssertionError: expected <N>, got <N>  (x1)
```

## 3. Error Grouping Categories

When processing test/build output, classify errors into categories for structured reporting:

| Category | Detection Patterns | Example |
|----------|-------------------|---------|
| **Import/Module** | `ImportError`, `ModuleNotFoundError`, `Cannot find module`, `unresolved import` | Missing dependency, wrong path |
| **Assertion** | `AssertionError`, `assert`, `expected.*got`, `toBe`, `toEqual` | Test expectation mismatch |
| **Timeout** | `timeout`, `ETIMEDOUT`, `deadline exceeded`, `timed out after` | Slow operation, missing mock |
| **Type** | `TypeError`, `type mismatch`, `cannot assign`, `TS\d{4}` | Wrong type, missing cast |
| **Connection** | `ECONNREFUSED`, `ECONNRESET`, `connection failed`, `socket hang up` | Service not running |
| **Permission** | `EACCES`, `PermissionError`, `403`, `Access denied` | Missing permissions |
| **Runtime** | All other exceptions/errors | Catch-all |

**Reporting format:**
```
FAIL: 8 tests (3 Import/Module in auth/, 3 Assertion in payment/, 2 Timeout in e2e/)
```

## 4. Smart Truncation

When output must be truncated (e.g., "last 50 lines"), apply this pipeline BEFORE truncating:

```
Raw output
  → §1 Normalize (replace runtime values)
  → §2 Deduplicate (group identical, add counts)
  → §3 Group by category (optional, for test/build output)
  → Truncate to N lines
```

This produces more informative truncated output than raw tail.

## Usage in SKILL.md

Reference this file instead of implementing normalization inline:

```markdown
**MANDATORY READ:** Load `references/output_normalization.md`
```

Then apply the relevant sections per use case:
- **Test output:** §1 + §2 + §3 + §4
- **Build output:** §1 + §2 + §4
- **Suspicion dedup:** §1 + §2 (normalize descriptions, group duplicates)
- **Log analysis:** §1 (normalization rules, canonical source)

---
**Version:** 1.0.0
**Last Updated:** 2026-03-15
