# Refactoring Decision Tree for DRY Violations

Use this tree when generating recommendations for detected DRY violations.

## Level 1: WHERE Is the Duplication?

| Duplication Location | Recommended Pattern | Example |
|---|---|---|
| Same file | Extract local function/method | Private helper within the class |
| Same module/domain | Module-level utility file | `users/utils/validation.ts` |
| Cross-module (3+ consumers) | Shared module in `shared/` or `utils/` | `references/validators/email.ts` |
| Cross-layer (controller + service) | Middleware / Decorator / Interceptor | `middleware/auth.ts` applied at router level |

## Level 2: WHAT Type of Logic Is Duplicated?

| Logic Type | Pattern | When to Use | Recommendation Template |
|---|---|---|---|
| **Pure transformation** (no side effects) | Utility function | Stateless input→output (format date, parse URL, sanitize string) | "Extract to `{domain}/utils/{name}.ts`" |
| **Validation rules** | Shared validator module | Email, password, phone, URL checks across entry points | "Extract to `references/validators/{type}.ts`" |
| **DB access patterns** | Base Repository / Repository method | Same query in 2+ services | "Create `{entity}Repository.{method}()`, callers use repository" |
| **Error handling** | Middleware / Decorator | try-catch wrapping same operations in multiple handlers | "Create error-handling middleware, remove try-catch from handlers" |
| **Constants / messages** | Constants file | Same string/number in 3+ places | "Create `constants/{category}.ts`, import everywhere" |
| **Object construction** | Factory / Builder | Complex object creation with 5+ fields, conditional defaults | "Create `{Entity}Factory.create()` with defaults" |
| **Behavioral variation** | Strategy pattern | Same interface, different behavior per context (payment methods, notification channels) | "Define `{Name}Strategy` interface, implement per variant" |
| **Template with hooks** | Template Method / Base class | Same sequence of steps, different individual steps (CRUD controllers, report generators) | "Create `Base{Name}` with abstract hook methods" |
| **Mapping / transformation** | Mapper class or function | Entity→DTO, DTO→Entity, API response shaping | "Create `{Entity}Mapper.toDto()` / `.toEntity()`" |
| **Middleware / decorator chain** | Named middleware group or router-level middleware | Same auth+validate+rateLimit stack on 5+ routes | "Create `{name}Middleware` group, apply at router level" |
| **Type definitions** | Shared type or base interface | Same fields in 2+ interfaces/types | "Create `Base{Entity}` type in `references/types/`, extend where needed" |

## Decision Factors

When multiple patterns could apply, use these factors:

| Factor | Utility Function | Shared Service (DI) | Base Class | Strategy |
|---|---|---|---|---|
| **State needed?** | No | Yes (has dependencies) | Maybe | No |
| **# consumers** | Any (2+) | 3+ across domains | 3+ subclasses | 2+ variants |
| **Changes often?** | Rarely | Sometimes | Rarely | Often (add new) |
| **Has dependencies?** | No (pure) | Yes (DB, APIs, etc.) | Maybe | No |
| **Domain boundary** | Within or cross-domain | Cross-domain | Within domain | Within domain |

## Quick Reference: DRY Type → Default Pattern

| DRY Type | Default Recommendation |
|---|---|
| 1.1 Identical code | Extract function → decide location by Level 1 |
| 1.2 Validation | Shared validator module |
| 1.3 Error messages | Constants file (`errors.ts`) |
| 1.4 Similar patterns | Extract common logic → decide pattern by Level 2 |
| 1.5 SQL queries | Repository method |
| 1.6 Test setup | Test helpers (`tests/helpers/`) |
| 1.7 API responses | DTO/Response class |
| 1.8 Middleware chains | Named middleware group |
| 1.9 Type definitions | Shared base type/interface |
| 1.10 Mapping logic | Mapper class/function |

---
**Version:** 1.0.0
**Last Updated:** 2026-02-08
