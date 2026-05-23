---
name: spike-testing
description: |
  Hypothesis-driven debugging methodology for TMNL.
  Progressive isolation (simple → complex), H1/H2/H3/H4 tagging,
  and Effect-native spike patterns.
triggers:
  - "spike"
  - "hypothesis"
  - "H1.*H2"
  - "diagnose"
  - "debug.*isolation"
  - "progressive.*test"
  - "debug.*integration"
---

# Spike Testing Patterns

## 🚨 MANDATORY DISCIPLINE

**This is not optional.** When debugging integration issues, you MUST create a spike.

### Self-Prompt Triggers

If you encounter ANY of these signals, STOP and run `bun spike init <issue-name>`:

```
❌ VIOLATION: Attempting to debug without spike
   Signal: "Works in X but fails in Y"

   REQUIRED ACTION:
   1. bun spike init <descriptive-name>
   2. Edit config with hypotheses
   3. bun spike new --config <file>
   4. Implement H1-H4 progressive tests
   5. Run spike, analyze output
   6. Extract fix to production
```

### Mandatory Spike Signals

| Signal | Response | Self-Prompt |
|--------|----------|-------------|
| "Binding expected X, actual Y" | `bun spike init binding-mismatch` | "STOP. Create spike before debugging." |
| "Works locally, fails in CI" | `bun spike init env-difference` | "STOP. Isolate environment variables." |
| "Tests pass alone, fail together" | `bun spike init state-pollution` | "STOP. Identify shared state." |
| "Schema error: missing _tag" | `bun spike init encoding-issue` | "STOP. Trace encoding layers." |
| "undefined is not a function" | `bun spike init type-mismatch` | "STOP. Validate type flow." |
| 3+ failed attempts at same bug | `bun spike init persistent-issue` | "STOP. Progressive isolation required." |

### Enforcement Protocol

When you see an integration error:

1. **DO NOT** add console.logs to existing code
2. **DO NOT** guess at the fix
3. **DO NOT** modify production code without spike evidence
4. **DO** run `bun spike init <issue>` immediately
5. **DO** define falsifiable hypotheses
6. **DO** test each layer in isolation

### Config-Driven Spikes (Preferred)

For any non-trivial debugging:

```bash
# 1. Generate structured config
bun spike init datetime-binding

# 2. Edit spike-datetime-binding.config.json
#    - Add specific hypotheses
#    - Define acceptance criteria
#    - Link related files

# 3. Generate spike from config
bun spike new --config spike-datetime-binding.config.json

# 4. Run and analyze
bun spike run scripts/spike-datetime-binding.ts --verbose
```

### Violation Detection

If you find yourself:
- Adding `console.log` to debug → **VIOLATION** → Create spike instead
- Trying random fixes → **VIOLATION** → Define hypotheses first
- Debugging for >10 minutes → **VIOLATION** → Progressive isolation required
- Modifying code without evidence → **VIOLATION** → Run spike first

---

## What is a Spike?

A **spike** is a time-boxed, throwaway investigation designed to answer a specific technical question or prove/disprove a hypothesis. Unlike production code, spikes are:

- **Isolated** — Self-contained files with minimal dependencies
- **Ephemeral** — Can be deleted after learning is extracted
- **Verbose** — Heavy logging to expose internal state
- **Progressive** — Builds incrementally from simple to complex

## When to Spike

| Signal | Spike Action |
|--------|--------------|
| "Works in PostgreSQL, fails in SQLite" | Type/binding constraints |
| "Tests pass individually, fail together" | Shared state pollution |
| "Schema error: missing _tag" | Encoding layer inspection |
| Documentation unclear | Empirical observation |
| Integration bug with no obvious cause | Progressive isolation |

## CLI Commands

```bash
# List all spike files
bun spike list

# List with custom pattern
bun spike list -p "scripts/diagnose-*.ts"

# Execute a spike
bun spike run scripts/spike-jsonl-buffering.ts

# Execute with verbose output
bun spike run scripts/spike-jsonl-buffering.ts --verbose

# Generate simple spike template
bun spike new jsonl-buffering

# Generate with topic description (options before args)
bun spike new -t "JSONL chunk handling" jsonl-buffering

# Generate config template (PREFERRED for non-trivial issues)
bun spike init datetime-binding

# Generate spike from config
bun spike new --config spike-datetime-binding.config.json
```

### Config Schema (Effect Schema)

The config file uses Effect Schema validation:

```json
{
  "$schema": "./spike-config.schema.json",
  "metadata": {
    "name": "datetime-binding",
    "topic": "DateTime SQLite Binding Investigation",
    "author": "Val",
    "date": "2026-01-16",
    "issueRef": "beads-123",
    "relatedFiles": ["src/lib/ams/v2/models/Session.ts"],
    "expectedOutcome": "Identify correct DateTime encoding for SQLite"
  },
  "paths": {
    "outputDir": "scripts",
    "outputFilename": "spike-datetime-binding.ts"
  },
  "hypotheses": [
    {
      "id": "H1",
      "description": "Schema DateTime encoding",
      "claim": "DateTimeFromDate encodes to ISO string",
      "acceptanceCriteria": ["typeof encoded === 'string'", "ISO format matches"]
    },
    {
      "id": "H2",
      "description": "Model layer",
      "claim": "Model.DateTimeInsert encodes correctly",
      "acceptanceCriteria": ["No Date object in encoded output"]
    }
  ]
}
```

## Spike Structure (Progressive Isolation)

### Pattern: H1 → H2 → H3 → H4

Start with the smallest possible reproduction, then add layers until the bug manifests.

```typescript
// H1: Schema alone (no DB)
async function h1_schema_encoding() {
  console.log("H1: Schema Encoding")
  console.log("Hypothesis: Schema encodes DateTime to ISO string")

  const program = Effect.gen(function* () {
    const encoded = yield* Schema.encode(MySchema)(value)
    console.log(`Encoded: ${JSON.stringify(encoded)} (type: ${typeof encoded})`)
    return typeof encoded === "string" ? "PASS" : "FAIL"
  })

  return Effect.runPromise(program)
}

// H2: Schema + Model (no DB)
async function h2_model_encoding() {
  console.log("H2: Model Encoding")
  console.log("Hypothesis: Model.insert encodes DateTime correctly")

  const program = Effect.gen(function* () {
    const payload = MyModel.insert.make({ ... })
    const encoded = yield* Schema.encode(MyModel.insert)(payload)
    console.log(`Insert encoded: ${JSON.stringify(encoded)}`)
    return encoded.createdAt instanceof Date ? "FAIL" : "PASS"
  })

  return Effect.runPromise(program)
}

// H3: Schema + Model + Repository
async function h3_repo_insert() {
  console.log("H3: Repository Insert")
  console.log("Hypothesis: Repository insert accepts encoded payload")

  const program = Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient
    const repo = yield* Model.makeRepository(MyModel, { ... })
    const result = yield* repo.insert(payload)
    console.log(`Insert result: ${JSON.stringify(result)}`)
    return result ? "PASS" : "FAIL"
  }).pipe(Effect.provide(TestLayer))

  return Effect.runPromise(program)
}

// H4: Full integration with Layer
async function h4_full_integration() {
  console.log("H4: Full Integration")
  console.log("Hypothesis: Full stack insert → findById works")

  const program = Effect.gen(function* () {
    // Full stack test
    const inserted = yield* service.insert(payload)
    const found = yield* service.findById(inserted.id)
    return Option.isSome(found) ? "PASS" : "FAIL"
  }).pipe(Effect.provide(FullLayer))

  return Effect.runPromise(program)
}
```

### Pattern: Hypothesis Tagging

Name tests by hypothesis, not by number:

```typescript
// ❌ BAD - What does this test?
const test1 = () => { ... }
const test2 = () => { ... }

// ✅ GOOD - Clear hypothesis
const h1_optionFromNullOr_encodes_to_string_null = () => { ... }
const h2_fieldOption_jsonFromString_produces_wrong_encoding = () => { ... }
const h3_custom_transform_with_optionFromSelf_produces_correct_encoding = () => { ... }
```

## Spike Output Requirements

A spike must produce:

1. **Console output** showing actual values and types at each stage
2. **Pass/Fail conclusion** for each hypothesis
3. **Root cause identification** when bug is found
4. **Canonical fix** that can be extracted to production code

### Example Output Analysis

```
=== H1: Schema.OptionFromNullOr(parseJson) ===
Option.none() encodes to: "null" (type: string)     <-- BUG: string "null", not null

=== H2: Model.FieldOption(JsonFromString) ===
Option.none() encodes to: "null" (type: string)     <-- CONFIRMS: Same bug in Model

=== H3: Custom NullableJsonFromString ===
Option.none() encodes to: null (type: object)       <-- CORRECT: actual null
Option.some({foo:"bar"}) encodes to: "{\"foo\":\"bar\"}" (type: string)

=== H4: Full SQLite Integration ===
Insert successful! Result: {"id":"test-1","jsonField":{"_id":"Option","_tag":"None"}}

============================================================
SUMMARY
============================================================
  ❌ H1
  ❌ H2
  ✅ H3
  ✅ H4

❌ Some hypotheses failed

ROOT CAUSE: Schema.Option vs Schema.OptionFromSelf encoding difference
FIX: Use OptionFromSelf in custom transform for SQLite compatibility
```

## Spike Ethos

### 1. Don't Trust Documentation Alone

```
WRONG: "The docs say it should work, so the bug must be elsewhere"
RIGHT: "Let me observe what actually happens with a spike"
```

### 2. Isolate Before You Integrate

```
WRONG: Add console.logs to 500-line integration test
RIGHT: Extract minimal reproduction to spike file
```

### 3. Observe, Don't Assume

```
WRONG: "I think the issue is X, let me write code assuming X"
RIGHT: "I think the issue is X. Let me write code that exposes whether X is true"
```

### 4. Name the Hypothesis

Every test in a spike should answer a specific question:

```
WRONG: test1, test2, test3
RIGHT:
- h1_schema_encodes_datetime_to_iso
- h2_model_insert_preserves_type
- h3_sqlite_binding_accepts_string
```

### 5. Preserve the Learning

After the spike reveals the fix:

1. Extract the fix to production code
2. Write documentation (like `.edin/` files)
3. Keep the spike file as a reference (or delete if trivial)
4. Create a test that would have caught the bug

## Canonical Sources

### Methodology
- `.edin/SPIKE_METHODOLOGY.md` — Full methodology documentation

### Example Spikes
- `scripts/diagnose-generative-container.ts` — H1-H4 pattern example

### Related Skills
- `/bdd-hypothesis-validation` — Hypothesis UI patterns for testbeds
- `/effect-schema-mastery` — Schema encoding patterns

## File Naming Convention

```
scripts/spike-{topic}.ts           # General spikes
scripts/diagnose-{issue}.ts        # Diagnostic spikes for specific issues
src/lib/{domain}/spikes/spike-{N}-{description}.ts  # Domain-specific spikes
```

Examples:
- `spike-nullable-json.ts` — JSON encoding investigation
- `diagnose-generative-container.ts` — GenerativeContainer state issue
- `spike-datetime-sqlite.ts` — DateTime + SQLite binding spike

## Spike Lifecycle

```
Problem Detected
     │
     ▼
Create Spike File (bun spike new <name>)
     │
     ▼
Progressive Tests (H1 → H2 → H3 → H4)
     │
     ▼
Observe Output (don't assume)
     │
     ▼
Identify Root Cause
     │
     ▼
Extract Fix to Production
     │
     ▼
Record Learning (bun spike learn)
     │
     ▼
Decide: Keep or Delete Spike
```

---

## Autopoietic Workflows (Self-Healing System)

The spike system learns from past debugging sessions to improve future suggestions.

### After Fixing a Bug with a Spike

```bash
# 1. Run your spike (if not already done)
bun spike run scripts/spike-datetime-binding.ts --verbose

# 2. Record the learning with the fix description
bun spike learn scripts/spike-datetime-binding.ts \
  --fix "Use DateTimeInsert for SQLite (not DateTimeInsertFromDate)"

# 3. Check pattern statistics
bun spike stats
```

### When Encountering a New Error

```bash
# 1. Get hypothesis suggestions based on error message
bun spike suggest "SQLITE_CONSTRAINT: NOT NULL constraint failed"

# 2. Generate spike from suggestions
bun spike init datetime-fix
bun spike new --config spike-datetime-fix.config.json

# 3. Implement and run the spike
# ... fill in test logic ...
bun spike run scripts/spike-datetime-fix.ts --verbose

# 4. After resolution, record learning
bun spike learn scripts/spike-datetime-fix.ts --fix "Use string encoding for DateTime"
```

### Periodic Pattern Evolution

```bash
# Review pattern statistics
bun spike stats

# Evolve patterns based on success rates
bun spike stats --evolve
```

### Self-Prompt Integration

When you see these signals, the autopoietic system can help:

| Signal | Action |
|--------|--------|
| Error message with no obvious cause | `bun spike suggest "<error>"` |
| Spike completed successfully | `bun spike learn <file> --fix "..."` |
| Multiple similar spikes | `bun spike stats --evolve` |
| Starting new investigation | `bun spike suggest` to check past patterns |

### Pattern Store

Patterns are stored in `.claude/cache/spike-patterns.json` with:

- **Error signatures** - Regex patterns that trigger suggestions
- **Hypothesis templates** - Pre-built H1-H4 structures
- **Success/failure counts** - Track what works
- **Recorded fixes** - Past solutions for reference

### Memory Integration

When `--fix` is provided to `learn`, the system also stores the learning to the opc memory system for broader recall across sessions.

### Autopoietic Feedback Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    FEEDBACK LOOP                            │
│                                                             │
│  Error encountered → bun spike suggest → Pattern matched    │
│       │                                         │           │
│       ▼                                         ▼           │
│  Create spike ←─────── Use hypothesis template ←┘           │
│       │                                                     │
│       ▼                                                     │
│  Run spike → Fix found → bun spike learn                    │
│                              │                              │
│                              ▼                              │
│               Pattern updated → Better suggestions          │
│                              │                              │
│                              └──────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```
