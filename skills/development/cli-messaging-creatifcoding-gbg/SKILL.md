---
name: cli-messaging
description: Agent-guiding error messages and output formatting for Effect CLI. Covers Data.TaggedError patterns, recovery suggestions, and structured output.
model_invoked: true
triggers:
  - "error messages"
  - "agent guidance"
  - "CLI output"
  - "TaggedError"
  - "error formatting"
  - "recovery options"
---

# CLI Messaging Patterns

Agent-guiding error messages and output formatting for Effect CLI applications.

## Philosophy

> **Errors should guide the next action, not just report failure.**

Every error message should answer:
1. **What happened?** — Clear description
2. **Why?** — Context about the cause
3. **What now?** — Recovery options

---

## Agent-Guiding Errors

### Pattern: TaggedError with Guidance

```typescript
import { Data, Effect } from "effect"

export class SessionNotFoundError extends Data.TaggedError("SessionNotFoundError")<{
  readonly id: string
  readonly suggestion: string
}> {
  override get message() {
    return `[SESSION_NOT_FOUND] Session '${this.id}' does not exist.

AGENT GUIDANCE: ${this.suggestion}

RECOVERY OPTIONS:
  1. List available sessions: rs list
  2. Search by topic: rs search "<keyword>"
  3. Create new session: rs create "<topic>"
`
  }
}
```

### Pattern: Validation Error with Fix

```typescript
export class InvalidInputError extends Data.TaggedError("InvalidInputError")<{
  readonly field: string
  readonly value: string
  readonly expected: string
  readonly examples: string[]
}> {
  override get message() {
    return `[INVALID_INPUT] Invalid value for '${this.field}': "${this.value}"

EXPECTED: ${this.expected}

VALID EXAMPLES:
${this.examples.map((e) => `  - ${e}`).join("\n")}

FIX: Provide a value matching the expected format.
`
  }
}
```

### Pattern: Permission/State Error

```typescript
export class OperationNotAllowedError extends Data.TaggedError("OperationNotAllowedError")<{
  readonly operation: string
  readonly reason: string
  readonly currentState: string
  readonly requiredState: string
}> {
  override get message() {
    return `[OPERATION_NOT_ALLOWED] Cannot ${this.operation}.

REASON: ${this.reason}
CURRENT STATE: ${this.currentState}
REQUIRED STATE: ${this.requiredState}

RECOVERY:
  1. Check current status: rs show <id>
  2. Update status if needed: rs update <id> --status=${this.requiredState}
  3. Then retry the operation
`
  }
}
```

### Pattern: Dependency Error

```typescript
export class DependencyError extends Data.TaggedError("DependencyError")<{
  readonly dependency: string
  readonly installCommand: string
}> {
  override get message() {
    return `[MISSING_DEPENDENCY] Required dependency '${this.dependency}' not found.

INSTALL:
  ${this.installCommand}

After installing, retry your command.
`
  }
}
```

---

## Error Codes Convention

Use bracketed codes for machine-parseable errors:

| Code Pattern | Meaning |
|--------------|---------|
| `[NOT_FOUND]` | Resource doesn't exist |
| `[INVALID_INPUT]` | Bad user input |
| `[CONFLICT]` | State conflict |
| `[PERMISSION]` | Not allowed |
| `[DEPENDENCY]` | Missing requirement |
| `[NETWORK]` | Connection issue |
| `[INTERNAL]` | Bug/unexpected |

### Example Error Code Usage

```typescript
export class ConflictError extends Data.TaggedError("ConflictError")<{
  readonly resource: string
  readonly conflictWith: string
}> {
  override get message() {
    return `[CONFLICT] ${this.resource} conflicts with ${this.conflictWith}.

RESOLUTION OPTIONS:
  1. Use --force to overwrite
  2. Rename the resource
  3. Delete the conflicting resource first
`
  }
}
```

---

## Structured Output

### Pattern: Table Formatting

```typescript
const formatTable = <T extends Record<string, unknown>>(
  items: T[],
  columns: Array<{ key: keyof T; header: string; width?: number }>
): string => {
  if (items.length === 0) {
    return "No items found."
  }

  // Calculate widths
  const widths = columns.map((col) => {
    const maxContent = Math.max(
      col.header.length,
      ...items.map((item) => String(item[col.key] ?? "").length)
    )
    return col.width ?? Math.min(maxContent, 40)
  })

  // Header
  const header = columns
    .map((col, i) => col.header.padEnd(widths[i]))
    .join("  ")

  const separator = widths.map((w) => "─".repeat(w)).join("──")

  // Rows
  const rows = items.map((item) =>
    columns
      .map((col, i) => {
        const val = String(item[col.key] ?? "")
        return val.length > widths[i]
          ? val.slice(0, widths[i] - 1) + "…"
          : val.padEnd(widths[i])
      })
      .join("  ")
  )

  return [header, separator, ...rows].join("\n")
}

// Usage
const sessions = yield* repo.list()
yield* Console.log(
  formatTable(sessions, [
    { key: "id", header: "ID", width: 8 },
    { key: "topic", header: "TOPIC", width: 30 },
    { key: "status", header: "STATUS", width: 10 },
    { key: "updated_at", header: "UPDATED", width: 20 },
  ])
)
```

### Pattern: JSON Output Mode

```typescript
const formatOption = Options.boolean("json").pipe(
  Options.withAlias("j"),
  Options.withDefault(false),
  Options.withDescription("Output as JSON")
)

const listCommand = Command.make(
  "list",
  { json: formatOption },
  ({ json }) =>
    Effect.gen(function* () {
      const sessions = yield* repo.list()

      if (json) {
        yield* Console.log(JSON.stringify(sessions, null, 2))
      } else {
        yield* Console.log(formatTable(sessions, TABLE_COLUMNS))
      }
    })
)
```

### Pattern: Verbose Mode

```typescript
const verboseOption = Options.boolean("verbose").pipe(
  Options.withAlias("v"),
  Options.withDefault(false)
)

const showCommand = Command.make(
  "show",
  { id: Args.text({ name: "id" }), verbose: verboseOption },
  ({ id, verbose }) =>
    Effect.gen(function* () {
      const session = yield* repo.get(id)

      if (verbose) {
        yield* Console.log("=== Session Details ===")
        yield* Console.log(`ID:         ${session.id}`)
        yield* Console.log(`Topic:      ${session.topic}`)
        yield* Console.log(`Status:     ${session.status}`)
        yield* Console.log(`Created:    ${session.created_at}`)
        yield* Console.log(`Updated:    ${session.updated_at}`)
        yield* Console.log("")
        yield* Console.log("=== Sources ===")
        for (const source of session.sources) {
          yield* Console.log(`  [${source.type}] ${source.url}`)
        }
      } else {
        yield* Console.log(JSON.stringify(session, null, 2))
      }
    })
)
```

---

## Success Messages

### Pattern: Action Confirmation

```typescript
const createCommand = Command.make(
  "create",
  { topic: Args.text({ name: "topic" }) },
  ({ topic }) =>
    Effect.gen(function* () {
      const id = yield* repo.create(topic)

      yield* Console.log(`
[SUCCESS] Session created.

  ID:    ${id}
  Topic: ${topic}

NEXT STEPS:
  - Add sources: rs add-source ${id} --type deepwiki --url "..."
  - View details: rs show ${id}
  - Start working: rs update ${id} --status=in_progress
`)
    })
)
```

### Pattern: Dry Run Mode

```typescript
const dryRunOption = Options.boolean("dry-run").pipe(
  Options.withDefault(false),
  Options.withDescription("Show what would happen without making changes")
)

const deleteCommand = Command.make(
  "delete",
  { id: Args.text({ name: "id" }), dryRun: dryRunOption },
  ({ id, dryRun }) =>
    Effect.gen(function* () {
      const session = yield* repo.get(id)

      if (dryRun) {
        yield* Console.log(`
[DRY RUN] Would delete:

  ID:    ${session.id}
  Topic: ${session.topic}
  Sources: ${session.sources?.length ?? 0}

Run without --dry-run to execute.
`)
        return
      }

      yield* repo.delete(id)
      yield* Console.log(`[SUCCESS] Deleted session '${id}'.`)
    })
)
```

---

## Progress Indicators

### Pattern: Simple Progress

```typescript
const importCommand = Command.make(
  "import",
  { file: Args.text({ name: "file" }) },
  ({ file }) =>
    Effect.gen(function* () {
      yield* Console.log(`Importing from ${file}...`)

      const items = yield* parseFile(file)
      let count = 0

      for (const item of items) {
        yield* repo.create(item)
        count++
        if (count % 10 === 0) {
          yield* Console.log(`  Processed ${count}/${items.length}...`)
        }
      }

      yield* Console.log(`
[SUCCESS] Import complete.

  Total imported: ${count}
  Source file:    ${file}
`)
    })
)
```

### Pattern: Spinner (with Effect)

```typescript
import { Effect, Schedule } from "effect"

const withSpinner = <A, E>(
  message: string,
  effect: Effect.Effect<A, E>
): Effect.Effect<A, E> => {
  const frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
  let frameIndex = 0

  const spinner = Effect.gen(function* () {
    process.stdout.write(`\r${frames[frameIndex]} ${message}`)
    frameIndex = (frameIndex + 1) % frames.length
  }).pipe(
    Effect.repeat(Schedule.spaced("80 millis")),
    Effect.fork
  )

  return Effect.gen(function* () {
    const fiber = yield* spinner
    const result = yield* effect
    yield* fiber.interrupt
    process.stdout.write(`\r✓ ${message}\n`)
    return result
  })
}

// Usage
yield* withSpinner("Loading data...", repo.list())
```

---

## Error Handling Pattern

### Centralized Error Handler

```typescript
const handleError = (e: unknown): Effect.Effect<void> => {
  // Known tagged errors - already formatted
  if (
    e instanceof SessionNotFoundError ||
    e instanceof InvalidInputError ||
    e instanceof OperationNotAllowedError
  ) {
    return Console.error(e.message)
  }

  // SQL errors
  if (e instanceof Error && e.message.includes("SQLITE")) {
    return Console.error(`
[DATABASE_ERROR] Database operation failed.

DETAILS: ${e.message}

RECOVERY:
  1. Check database file exists: ls ~/.myapp/
  2. Verify permissions: ls -la ~/.myapp/data.db
  3. Try reinitializing: rm ~/.myapp/data.db && myapp init
`)
  }

  // Unknown errors
  const msg = e instanceof Error ? e.message : String(e)
  return Console.error(`
[INTERNAL_ERROR] An unexpected error occurred.

DETAILS: ${msg}

Please report this issue with the above details.
`)
}

// Apply to program
pipe(
  program,
  Effect.catchAll(handleError),
  Effect.provide(AppLayer),
  NodeRuntime.runMain
)
```

---

## Help Text Patterns

### Command Help

```typescript
const mainCommand = Command.make("mycli", {}, () =>
  Console.log(`
mycli v1.0.0 - Research Session Manager

USAGE:
  mycli <command> [options]

COMMANDS:
  list              List all sessions
  show <id>         Show session details
  create <topic>    Create new session
  update <id>       Update session
  delete <id>       Delete session
  search <query>    Search sessions

GLOBAL OPTIONS:
  --json, -j        Output as JSON
  --verbose, -v     Verbose output
  --help, -h        Show help
  --version, -V     Show version

EXAMPLES:
  mycli create "Effect-TS patterns"
  mycli list --json
  mycli show abc123 --verbose
  mycli search "authentication"

AGENT USAGE:
  For automated usage, always use --json for parseable output.
  Error codes in brackets (e.g., [NOT_FOUND]) are machine-readable.
`)
)
```

---

## Anti-Patterns

### DON'T: Generic error messages

```typescript
// WRONG - No guidance
throw new Error("Session not found")

// CORRECT - Agent-guiding
yield* Effect.fail(
  new SessionNotFoundError({
    id,
    suggestion: "The session may have been deleted. Use 'list' to see available sessions.",
  })
)
```

### DON'T: Swallow errors silently

```typescript
// WRONG - Silent failure
const result = yield* effect.pipe(Effect.catchAll(() => Effect.succeed(null)))
if (result) { ... }

// CORRECT - Report the issue
const result = yield* effect.pipe(
  Effect.catchTag("NotFoundError", (e) =>
    Effect.gen(function* () {
      yield* Console.error(e.message)
      return null
    })
  )
)
```

### DON'T: Inconsistent output formats

```typescript
// WRONG - Mixing formats
console.log("Found:", sessions.length)
console.log(JSON.stringify(sessions))

// CORRECT - Consistent format
yield* Console.log(JSON.stringify({ count: sessions.length, sessions }, null, 2))
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `cli/core` | Command definition |
| `cli/persistence` | Storage patterns |
| `cli/services` | Service composition |
| `cli/config` | Configuration patterns |

---

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `Data.TaggedError` | Typed, catchable errors |
| `[ERROR_CODE]` | Machine-parseable prefix |
| `RECOVERY OPTIONS` | Guide next actions |
| `--json` flag | Structured output mode |
| `--verbose` flag | Detailed human output |
| `--dry-run` flag | Preview without executing |
| Centralized handler | Consistent error formatting |
