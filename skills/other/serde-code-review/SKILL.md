---
name: serde-code-review
description: Reviews serde serialization code for derive patterns, enum representations, custom implementations, and common serialization bugs. Use when reviewing Rust code that uses serde, serde_json, toml, or any serde-based serialization format. Covers attribute macros, field renaming, and format-specific pitfalls.
---

# Serde Code Review

## Review Workflow

1. **Check Cargo.toml** — Note serde features (`derive`, `rc`), format crates (`serde_json`, `toml`, `bincode`, etc.), and Rust edition (2024 has breaking changes affecting serde code)
2. **Check derive usage** — Verify `Serialize` and `Deserialize` are derived appropriately
3. **Check enum representations** — Enum tagging affects wire format compatibility and readability
4. **Check field attributes** — Renaming, defaults, skipping affect API contracts
5. **Check edition 2024 compatibility** — Reserved `gen` keyword, RPIT lifetime capture changes, `never_type_fallback`
6. **Verify round-trip correctness** — Serialized data must deserialize back to the same value

## Gates (before reporting findings)

Run **in order**. Do not write a finding until the step that applies has passed.

1. **Serde context on disk** — **Pass when:** You have read the relevant `Cargo.toml` (crate or workspace root) and can state Rust `edition`, `serde` / `serde_derive` features if non-default (`derive`, `rc`), and which format crates apply (`serde_json`, `toml`, `bincode`, etc.) for the code under review. **Then** apply edition-specific checklist items (e.g. `gen`, RPIT/`never_type_fallback`) only when that file supports them.

2. **Per-finding evidence** — **Pass when:** Each issue cites `[FILE:LINE]` from the **current** tree for the `struct`/`enum`, `Serialize`/`Deserialize` impl, or attribute block in question (not from memory, docs-only, or another branch).

3. **Category check vs protocol** — **Pass when:** For the finding type (derive attrs, enum tagging, `flatten`, custom impl, sqlx + serde alignment), you ran the matching checks from `beagle-rust:review-verification-protocol` (e.g. full type definition + serde attrs before “wrong representation”; confirmed edition in `Cargo.toml` before edition-2024-only findings). **Then** add the finding.

4. **Output shape** — **Pass when:** The report lines match **Output Format** below (severity + description).

## Output Format

Report findings as:

```text
[FILE:LINE] ISSUE_TITLE
Severity: Critical | Major | Minor | Informational
Description of the issue and why it matters.
```

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Derive patterns, attribute macros, field configuration | [references/derive-patterns.md](references/derive-patterns.md) |
| Custom Serialize/Deserialize, format-specific issues | [references/custom-serialization.md](references/custom-serialization.md) |

## Review Checklist

### Derive Usage
- [ ] `#[derive(Serialize, Deserialize)]` on types that cross serialization boundaries
- [ ] `#[derive(Debug)]` alongside serde derives (debugging serialization issues)
- [ ] Feature-gated derives when serde is optional: `#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]`
- [ ] Prefer `#[expect(unused)]` over `#[allow(unused)]` for serde-only fields (self-cleaning lint suppression, stable since 1.81)

### Enum Representation
- [ ] Enum tagging is explicit (not relying on serde's default externally-tagged format when another is intended)
- [ ] Tag names are stable and won't collide with field names
- [ ] `#[serde(rename_all = "...")]` used consistently across the API

### Field Configuration
- [ ] `#[serde(skip_serializing_if = "Option::is_none")]` for optional fields (clean JSON output)
- [ ] `#[serde(default)]` for fields that should have fallback values during deserialization
- [ ] `#[serde(rename = "...")]` when Rust field names differ from wire format
- [ ] `#[serde(flatten)]` used judiciously (can cause key collisions)
- [ ] No `#[serde(deny_unknown_fields)]` on types that need forward compatibility
- [ ] No fields or variants named `gen` — reserved keyword in edition 2024 (use `r#gen` or rename)

### Database Integration (sqlx)
- [ ] `#[derive(sqlx::Type)]` enums use consistent representation with serde
- [ ] Enum variant casing matches between serde (`rename_all`) and sqlx (`rename_all`)

### Edition 2024 Compatibility
- [ ] No fields or enum variants named `gen` (reserved keyword — use `r#gen` with `#[serde(rename = "gen")]` or choose a different name)
- [ ] Custom `Serialize`/`Deserialize` impls returning `impl Trait` account for RPIT lifetime capture changes (all in-scope lifetimes captured by default; use `+ use<'a>` for precise control)
- [ ] Deserialization error paths handle `never_type_fallback` — `!` falls back to `!` instead of `()`, which affects match exhaustiveness on `Result<T, !>` patterns

### Correctness
- [ ] Round-trip tests exist for complex types (serialize → deserialize → assert_eq)
- [ ] `PartialEq` derived for types with round-trip tests
- [ ] No lossy conversions (e.g., `f64` → `i64` in JSON numbers)
- [ ] `Decimal` used for money/precision-sensitive values, not `f64`

## Severity Calibration

### Critical
- Enum representation mismatch between serializer and deserializer (data loss)
- Missing `#[serde(rename)]` causing API-breaking field name changes
- `#[serde(flatten)]` causing silent key collisions
- Lossy numeric conversions (`f64` precision loss for monetary values)

### Major
- Inconsistent `rename_all` across related types (confusing API)
- Missing `skip_serializing_if` causing null/empty noise in output
- `deny_unknown_fields` on types consumed by evolving APIs (breaks forward compatibility)
- Missing round-trip tests for complex enum representations
- Field or variant named `gen` without `r#gen` escape (edition 2024 compile failure)

### Minor
- Unnecessary `#[serde(default)]` on required fields
- Using string representation for enums when numeric would be more efficient
- Verbose custom implementations where derive + attributes suffice
- Using `#[allow(unused)]` instead of `#[expect(unused)]` for serde-only fields (prefer self-cleaning lint suppression)

### Informational
- Suggestions to switch enum representation for cleaner wire format
- Suggestions to add `#[non_exhaustive]` alongside serde for forward compatibility

## Valid Patterns (Do NOT Flag)

- **Externally tagged enums** — serde's default, valid for many use cases
- **`#[serde(untagged)]` enums** — Valid when discriminated by structure, not by tag
- **`serde_json::Value` for dynamic data** — Appropriate for truly schema-less fields
- **`#[serde(skip)]` on computed fields** — Correct for derived/cached values
- **`#[serde(with = "...")]` for custom formats** — Standard for dates, UUIDs, etc.
- **`r#gen` with `#[serde(rename = "gen")]`** — Correct edition 2024 workaround for `gen` fields in wire formats
- **`+ use<'a>` on custom serializer return types** — Precise RPIT lifetime capture (edition 2024)

## Before Submitting Findings

Complete **Gates (before reporting findings)** above; gate 3 incorporates `beagle-rust:review-verification-protocol` for serde-related issue types.
