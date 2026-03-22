---
name: review-config-registry
description: Audit config registry for dead keys, no-op configs, stale descriptions, and organizational opportunities
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit `src/shared/config_registry.ahk` for dead weight, behavioral no-ops, stale metadata, and organizational drift. The config registry is user-facing — every key maps to a line in someone's `config.ini`. Findings are surfaced for human review, not auto-fixed.

## Scope

- `src/shared/config_registry.ahk` — the single source of truth for all config definitions
- All source files that consume config values via `cfg.KeyName`

## Phase 1 — Dead Keys (Mechanical, High Confidence)

A dead key exists in the registry but has zero effect on the application.

### Method

For every key in the registry:
1. Use `query_config.ps1 -Usage <keyName>` to find all consumer files
2. If zero consumers outside of `config_registry.ahk`, `config_loader.ahk`, and editor files — the key is dead

**Classification:**
- **Dead** — zero consumers. The key does nothing. Safe to remove (with config migration note).
- **Test-only** — consumed only in test files. Possibly dead in production, or possibly a test-specific override. Flag for review.
- **Editor-only** — consumed only by the config editor UI. May be used for display logic but has no production effect.

### Edge cases
- Keys consumed via dynamic access (`cfg.%varName%`) won't show in static grep. Check for dynamic access patterns before declaring a key dead.
- Array section keys use `{N}` templates (e.g., `Shader{N}_ShaderName`). The consumer will reference `cfg.Shader1_ShaderName` etc. — search for expanded names.

## Phase 2 — Behavioral No-Ops (Medium Confidence, High Value)

A no-op key is consumed in source code, but the code behaves identically regardless of the key's value. Grep finds it. The config is still useless.

### Method

For each config key (prioritize booleans and enums — they're the most common no-ops):

1. Find all usage sites via `query_config.ps1 -Usage <keyName>`
2. For each usage site, read the surrounding code context (the function or block containing `cfg.KeyName`)
3. Assess whether the key's value actually influences behavior:

**Patterns that indicate a no-op:**
- `if (cfg.Flag)` where the body is empty, commented out, or effectively identical to the else branch
- `if (cfg.Flag)` with no else, where the guarded code was moved/deleted but the condition shell remains
- A numeric config multiplied into a value that's subsequently overwritten or never used
- A string config compared against values, but all comparison branches execute the same logic
- A config value assigned to a variable that's never read after assignment
- A config consumed only inside a diagnostic log guard (the config controls logging but nothing else — may be intentional, flag for review)

**Patterns that are NOT no-ops (don't flag these):**
- Config consumed in a ternary or conditional that feeds into a DllCall, ComCall, or GUI property
- Config consumed as a parameter to a function that branches on it internally (trace one level deep)
- Config consumed in the paint path or shader pipeline where the visual effect differs

### Classification
- **No-op** — the key demonstrably has no behavioral effect. Include the code snippet showing why.
- **Suspected no-op** — the key is consumed but the usage looks vestigial. Include context for human review.
- **Active** — the key meaningfully influences behavior. No action needed.

## Phase 3 — Metadata Accuracy (Mechanical, Medium Confidence)

### Descriptions
For each key, check the `d` (description) field against actual behavior:
- Does the description reference functions, features, or behaviors that no longer exist?
- Does the description say "controls X" when the key now controls Y (feature was refactored)?
- For enum-style keys: does the description list all valid values? Are there values listed that the code doesn't handle?

### Bounds
For numeric keys with `min`/`max`:
- Is the `default` within the `min`/`max` range?
- Does the code actually clamp to these bounds, or does it accept values outside them?
- Are the bounds reasonable? (e.g., a millisecond timer with `max: 1000000` — technically valid, practically useless)

### Types
- Does the `t` (type) field match how the key is actually used? A key typed as `int` but compared as a string, or typed as `bool` but used as a numeric threshold.

## Phase 4 — Organizational Review (Subjective, Lower Priority)

This phase surfaces clustering opportunities. All findings are suggestions — the human decides if reorganization is worth the config.ini migration cost.

### Method

1. Group all keys by their INI section (`s` field)
2. For each section, note the key count and conceptual coherence
3. Look for:

**Scattered related keys:**
Keys that relate to the same feature but live in different sections. Signal: similar name prefixes, consumed by the same functions, or controlling different aspects of one visual/behavioral feature.

Example pattern: "inner shadow" keys split across `[GUI]` and `[Performance]` when they could be a coherent group.

**Oversized sections:**
Sections with 40+ keys where natural sub-groupings exist. Not a problem per se, but worth surfacing.

**Naming inconsistencies:**
Keys whose name prefix doesn't match their section. A key named `GUI_FooBar` in the `[Store]` section, or a key that was moved between sections but kept its old prefix.

**Orphaned sections:**
Sections with only 1-2 keys that could reasonably merge into a parent section.

### Output format for this phase

Don't just list problems — sketch the potential reorganization so the human can evaluate it as a whole:

```
Suggestion: Shadow settings consolidation
Currently:
  [GUI] GUI_UseInnerShadow, GUI_InnerShadowAlpha, GUI_InnerShadowDepthPx
  [Performance] Perf_ShadowQuality
Proposed:
  [GUI.Shadow] UseInnerShadow, Alpha, DepthPx, Quality
Impact: Would require config.ini migration for 4 keys
```

## Explore Strategy

Split by registry section for Phase 1-3 (parallel):
- **Agent 1**: `[AltTab]`, `[Launcher]`, `[Setup]`, `[Tools]`, `[IPC]` sections
- **Agent 2**: `[GUI]` section (largest — may need the full agent)
- **Agent 3**: `[Store]`, `[Performance]`, `[Capture]` sections
- **Agent 4**: `[Shader.*]`, `[MouseEffect]`, `[BackgroundImage]` sections
- **Agent 5**: `[Theme]`, `[Diagnostics]`, `[Komorebi]` sections

Each agent runs Phase 1 (dead keys), Phase 2 (no-ops), and Phase 3 (metadata) for its sections.

Phase 4 (organizational review) runs after, since it needs the full picture across all sections.

## Output Format

### Dead Keys

| Key | Section | Consumers | Status | Notes |
|-----|---------|-----------|--------|-------|
| `Store_FooBar` | Store | 0 | Dead | No references outside registry/loader |
| `GUI_OldFlag` | GUI | 1 (test only) | Test-only | Only in `test_unit_config.ahk` |

### Behavioral No-Ops

| Key | Section | Usage Sites | Why It's a No-Op | Code Evidence |
|-----|---------|-------------|------------------|---------------|
| `GUI_SomeFlag` | GUI | `gui_paint.ahk:142` | `if` body is empty after refactor | `if (cfg.GUI_SomeFlag) { }` |
| `Store_Mode` | Store | `gui_data.ahk:88` | Both branches execute identical logic | Both call `_Refresh()` with same args |

### Metadata Issues

| Key | Field | Issue | Current | Should Be |
|-----|-------|-------|---------|-----------|
| `GUI_FooMs` | `d` | References deleted function | "Delay for `_GUI_OldFunc()`" | "Delay for overlay show" |
| `Perf_Bar` | `min/max` | Default outside bounds | default=0, min=1 | Either default=1 or min=0 |

### Organizational Suggestions

Group by suggestion, not by individual key. Include migration impact.

```
Suggestion: [descriptive name]
Currently: [where keys live now]
Proposed: [where they could live]
Keys affected: N
Migration impact: [brief — breaking change to config.ini, needs migration in config_loader]
```

Order all tables: dead keys first (easy wins), no-ops second (highest value — invisible waste), metadata third, organizational last.

Ignore any existing plans — create a fresh one.
