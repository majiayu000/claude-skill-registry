<!-- SOURCE-OF-TRUTH: plugins/codebase-audit-suite/shared/references/ai_ready_architecture.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# AI-Ready Architecture Reference

Single source of truth for AI-architecture concepts, detection patterns, and thresholds.

**Source:** ["Sinks, Not Pipes: Software Architecture in the Age of AI"](https://ianbull.com/posts/software-architecture) — Ian Bull, 2026.

---

## Core Concepts

### Sinks vs Pipes

| Term | Definition | Example |
|------|-----------|---------|
| **Sink** | Function that completes work independently (depth 0-1). No cascading side-effects | `save_user(data)` writes to DB, returns result |
| **Shallow Pipe** | Function with moderate chain (depth 2). Manageable for AI reasoning | `create_order()` saves order + sends confirmation |
| **Deep Pipe** | Function triggering cascading side-effects (depth 3+). AI agent cannot reason about full impact | `process_payment()` charges card → creates invoice → sends email → updates metrics → triggers limits |

### Cascade Depth Thresholds

| Depth | Classification | Severity | Action |
|-------|---------------|----------|--------|
| 0-1 | Sink | OK | No action |
| 2 | Shallow Pipe | OK | No action |
| 3 | Deep Pipe | MEDIUM | Review recommended |
| 4+ | Deep Pipe | HIGH | Refactor to flat orchestration |

### Flat Orchestration

One orchestrator function calls independent sink functions at the same level. All steps visible in one function body.

```
# Anti-pattern: cascading pipe
def process_payment(order):
    charge = payment_service.charge(order)      # charge() internally calls
                                                 #   invoice_service.create()
                                                 #     which calls notify_service.send()
                                                 #       which calls metrics_service.track()

# Correct: flat orchestration
def process_payment(order):
    charge = payment_service.charge(order)       # sink: charge only
    invoice = invoice_service.create(order)      # sink: create only
    notify_service.send(order, invoice)          # sink: notify only
    metrics_service.track("payment", order.id)   # sink: track only
```

> **Note:** "Flat Orchestration" = sequential step orchestration at single level (all steps visible). This is NOT the "cascading pipe" anti-pattern where side-effects trigger hidden chains. The term "Pipeline" in skill architecture (e.g., audit coordinator pipeline) refers to orchestrator-worker sequential processing, which IS flat.

### Architectural Honesty

Function interfaces must reveal all side-effects. A function named `get_*` that writes to DB is "architecturally dishonest" — the caller cannot reason about consequences.

**Read-implying prefixes** (must NOT contain write side-effects):

```
get_ | find_ | check_ | validate_ | is_ | has_ | list_ | count_ | search_ | fetch_ | load_ | read_
```

**Write-implying prefixes** (side-effects expected):

```
create_ | update_ | delete_ | save_ | remove_ | process_ | handle_ | execute_ | send_ | notify_ | publish_
```

### Opaque Sinks (Event Emissions)

Event emissions (`.emit()`, `.publish()`, `.dispatch()`, `EventBus.fire()`) count as **depth +1** but are marked **"unbounded"** since async subscriber chains cannot be traced statically. When calculating cascade depth:

- Count event emission as +1 depth
- Mark as "opaque — verify subscriber chain manually"
- Do NOT attempt to follow subscribers (too expensive for heuristic scan)

---

## Side-Effect Detection Patterns

Language-specific Grep patterns for identifying side-effect markers in code.

### Write Side-Effects (any of these = side-effect)

| Language | Pattern | What it detects |
|----------|---------|-----------------|
| **Python/Django** | `\.save\(\)\|\.create\(\)\|\.update\(\)\|\.delete\(\)\|\.bulk_create\|\.bulk_update` | ORM writes |
| **Python/SQLAlchemy** | `session\.add\|session\.commit\|session\.flush\|session\.execute` | Session writes |
| **TypeScript/Prisma** | `\.create\(\)\|\.update\(\)\|\.delete\(\)\|\.upsert\(\)\|\.createMany` | Prisma writes |
| **TypeScript/TypeORM** | `\.save\(\)\|\.insert\(\)\|\.update\(\)\|\.delete\(\)\|\.remove\(\)` | TypeORM writes |
| **C#/EF** | `\.Add\(\)\|\.Update\(\)\|\.Remove\(\)\|SaveChanges\|SaveChangesAsync` | EF Core writes |
| **Java/JPA** | `\.persist\(\)\|\.merge\(\)\|\.remove\(\)\|\.flush\(\)` | JPA writes |
| **HTTP calls** | `\.post\(\)\|\.put\(\)\|\.patch\(\)\|\.delete\(\)\|fetch\(.*method.*POST` | Outbound HTTP writes |
| **Notifications** | `send_email\|send_notification\|send_sms\|notify\|push_notification` | External notifications |
| **Events** | `\.emit\(\)\|\.publish\(\)\|\.dispatch\(\)\|EventBus\|event_bus\|\.fire\(` | Event emissions (opaque) |
| **Logging (state)** | `audit_log\|activity_log\|track_event\|analytics\.track` | Audit/analytics writes |

### Read-Named Function Detection

```
Grep: (def|function|async)\s+(get_|find_|check_|validate_|is_|has_|list_|count_|search_|fetch_|load_|read_)
```

Match read-named functions, then check body for write side-effect markers above.

### Orchestrator Name Detection

```
Grep: (def|function|async)\s+(process_|create_|update_|handle_|execute_|run_|perform_|do_)
```

These functions are expected to have side-effects — focus cascade depth analysis here.

### Service Import Detection (for Flat Orchestration)

```
Grep: (from\s+.*services.*import|import\s+.*Service|@Inject.*Service|private.*Service)
```

Count service imports per file. 3+ imports in a **leaf function** = cascade risk (investigate depth). 3+ imports in an **orchestrator function** (process_, handle_, execute_) = expected flat orchestration pattern — NOT a concern.

---

## False Positive Exclusions

| Pattern | Why Exclude |
|---------|-------------|
| `get_or_create` / `first_or_create` | Standard ORM upsert — write is expected by name |
| `get_*` with `@cache` / `@lru_cache` / `@cached` | Cache initialization is expected write |
| CQRS handlers: `handle_*`, `execute_*` (in command dirs) | Write is their explicit purpose |
| `check_and_*` / `validate_and_*` | Compound name signals write intent |
| Test files (`**/tests/**`, `**/test_*`) | Test side-effects are intentional |
| Migration files (`**/migrations/**`, `**/alembic/**`) | Schema changes are expected |

---

## External Tools (Informational)

For projects needing deeper enforcement beyond AI-agent Grep heuristics:

| Language | Tool | What it enforces |
|----------|------|------------------|
| JS/TS | [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) | Module dependency rules (forbidden/allowed/required) |
| Python | [import-linter](https://import-linter.readthedocs.io/) | Layer contract types (forbidden, layers) |
| Java/C# | [ArchUnit](https://www.archunit.org/) | Architecture rules with freeze-baseline for gradual adoption |
| Multi-lang | [CodeQL](https://codeql.github.com/) | Dataflow analysis (local + global) |
| Multi-lang | [Semgrep](https://semgrep.dev/) | Interfile taint mode (min 4GB/core) |

These tools are NOT required by skills. Skills use Grep-based heuristics that work without external dependencies.
