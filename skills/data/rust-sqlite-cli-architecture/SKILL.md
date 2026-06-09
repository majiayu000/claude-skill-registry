---
name: rust-sqlite-cli-architecture
description: |-
  Use when designing Rust CLIs backed by SQLite with migrations, transactions, tests, and data safety.
  Triggers:
practices:
- pragmatic-programmer
- devsecops-cdlc
- testable-architecture
hexagonal_role: supporting
consumes:
- product-requirements
- command-map
- data-model
- operational-constraints
produces:
- architecture-plan
- migration-plan
- transaction-policy
- test-strategy
context_rel: []
skill_api_version: 1
user-invocable: false
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: judgment
  stability: stable
  external_dependencies:
  - Rust toolchain
  - SQLite
output_contract: "A Rust SQLite CLI architecture plan covering command boundaries, schema ownership, migrations, transaction policy, tests, backups, recovery, and data-safety checks."
---

# Rust SQLite CLI Architecture

Use this skill when designing or reviewing a Rust command-line application that
stores durable local state in SQLite. The output is an implementation-ready
architecture plan, not a pile of generic database advice. It should identify
where data lives, how schema changes land, which commands own transactions, how
tests prove safety, and how users recover when something goes wrong.

## Critical Constraints

- Treat the database as user data, not an internal cache, unless the product
  explicitly says it can be deleted without loss.
- Pick one canonical database location and make overrides explicit through a
  flag, environment variable, or config value.
- Never run destructive schema changes without a tested backup and rollback
  path.
- Every mutating command needs an explicit transaction boundary.
- Migrations are source-controlled, ordered, repeatable, and tested from older
  fixtures.
- User-facing errors must explain the next action without exposing raw SQL as
  the main message.
- Recovery commands must exist before the tool is used for important data.

## When SQLite Fits

SQLite is a strong fit when the CLI needs local durable state, offline operation,
fast startup, simple deployment, and one-machine ownership. Examples include
task stores, local indexes, audit logs, sync queues, caches that must survive
restart, and portable project databases.

Choose another storage design when the product requires heavy multi-writer
concurrency across machines, central policy enforcement, server-side audit, or
very large binary payloads. A CLI can still use SQLite as a local queue or cache
in those systems, but the architecture should name the server of record.

## Inputs To Collect

Before designing modules or tables, gather these facts:

- Primary commands and which ones read, mutate, import, export, sync, or delete.
- Data ownership: per user, per workspace, per repository, or per explicit file.
- Portability needs: copyable database file, project-relative database, or
  platform data directory.
- Durability expectations: cache, rebuildable index, or authoritative user data.
- Concurrency expectations: one process, shell pipelines, background daemon,
  scheduled runs, or multiple terminals.
- Upgrade expectations: how old an installed database might be in the field.
- Privacy and backup expectations for sensitive or irreplaceable data.

## Architecture Procedure

1. Define the storage contract.
   State the default path, override mechanism, file permissions, and whether the
   database is authoritative. Do not hide important data under an ambiguous temp
   or cache path.

2. Draw the command-to-data map.
   For each command, list the tables it reads and writes, whether it needs a
   transaction, and what invariant must hold after it exits.

3. Choose module boundaries.
   Keep CLI parsing, domain decisions, database access, migrations, and output
   rendering separate enough that transaction tests can call the domain layer
   without scraping terminal text.

4. Design the schema for operations.
   Model stable entities as tables with primary keys, foreign keys, and indexes
   that match command queries. Use JSON columns only for opaque payloads or
   bounded extension fields, not for data that commands must filter or join.

5. Define connection setup.
   Open one connection per command unless the product has a daemon mode. Apply
   required connection settings consistently, including foreign-key enforcement,
   busy timeout, and any journal-mode decision.

6. Write the migration policy.
   Decide whether normal command startup applies pending migrations or whether
   users run an explicit upgrade command. For authoritative data, prefer a
   preflight check, backup, migration, integrity check, and clear failure path.

7. Specify transaction boundaries.
   Every mutating command begins a transaction after validation and commits only
   after all database invariants are satisfied. Render output after commit so a
   successful message cannot precede a rolled-back write.

8. Plan operational commands.
   Include commands or documented workflows for `doctor`, `backup`, `restore`,
   `export`, `import`, `schema-version`, and optional compaction.

9. Build the test matrix.
   Cover fresh database creation, migration from prior fixtures, transaction
   rollback, command integration, concurrent-process behavior, backup/restore,
   import validation, and corruption diagnosis.

## Recommended File Shape

Adapt names to the repository, but preserve the separation of responsibilities:

```text
src/
  main.rs              # process entry point and error-to-exit mapping
  cli.rs               # argument parsing and command enum
  commands/            # command handlers, one file per workflow
  domain/              # validation and state-transition rules
  db/
    mod.rs             # connection factory and common database errors
    migrations/        # ordered migration files or embedded migration sources
    schema.rs          # schema-version checks and migration runner
    repo_*.rs          # small query modules grouped by aggregate or workflow
tests/
  cli/                 # black-box command tests
  fixtures/db-v*.sqlite
```

The key rule is direction: commands may call domain and database modules; the
database layer should not know about terminal formatting, color, progress bars,
or command-line flags.

## Data Location Rules

- Per-user tools should default to a platform data directory and print the path
  in diagnostic commands.
- Per-project tools should prefer an explicit project metadata directory or a
  user-selected path checked into the project policy.
- Support `--database <path>` or an equivalent override for tests, recovery, and
  advanced operation.
- Refuse to create parent directories with broad permissions for sensitive
  state.
- Document sidecar files if the journal mode creates them, because backup and
  cleanup procedures must include them or checkpoint first.

## Schema Rules

- Enable foreign-key enforcement for every connection.
- Use stable integer or text primary keys; do not rely on row order.
- Store timestamps in one format and name the clock source used by commands.
- Add indexes for the queries on the command map, not for speculative future
  reports.
- Keep schema metadata in the database, including current migration version and
  application identity.
- Keep destructive changes explicit: copy-table migrations are safer than
  in-place mutation when data matters.
- Make uniqueness constraints carry product meaning, then translate violations
  into user-facing conflict messages.

## Migration Policy

A migration plan must answer:

- How pending migrations are detected.
- Whether a backup is created before migration.
- How integrity is checked before and after migration.
- Which migrations are reversible, and which require restore from backup.
- How the tool behaves when the executable is older than the database schema.
- How fixture databases are generated and kept for compatibility tests.

For important user data, the safe default is:

1. Open the database.
2. Check application identity and schema version.
3. Run an integrity check.
4. Create or require a backup.
5. Apply pending migrations inside the narrowest safe transaction scope.
6. Run post-migration integrity and invariant checks.
7. Report the new schema version and backup location.

## Transaction Policy

Use one explicit transaction per mutating command. Start it after input
validation and connection setup. Commit after database invariants pass. Roll
back on any error. Commands that perform read-modify-write decisions should
acquire the write intent early enough to avoid stale decisions under concurrent
processes.

External side effects need special care:

- If the command writes files and the database, define which side is
  authoritative and how cleanup works after failure.
- If the command sends network requests, prefer an outbox table or idempotent
  operation key so retry does not duplicate user-visible effects.
- If output streams a report, collect database state first, commit if needed,
  then render.

## Testing Plan

Build tests around behavior, not driver internals:

- Fresh-start test: no database exists, the first read and first write behave as
  documented.
- Migration fixture test: every supported older fixture opens, migrates, and
  preserves expected rows.
- Transaction rollback test: inject a failure after partial work and verify no
  partial state remains.
- Command integration test: run the compiled binary against a temp database and
  assert output plus database state.
- Concurrency test: run two processes against the same database for commands
  that users might execute in parallel.
- Backup/restore test: create data, back it up, restore it elsewhere, and run
  `doctor`.
- Import test: malformed input fails before mutation; valid input is atomic.
- Destructive command test: dry-run output matches the rows affected by the real
  command.

Prefer temp directories and per-test database paths. Tests should not touch a
developer's real data directory.

## Operational Safety

Add a `doctor` path that checks database path, application identity, schema
version, integrity, foreign-key consistency, journal leftovers, and writability.
The command should return a nonzero exit code on unsafe state and include the
next command a user can run.

Add backup and export behavior before destructive workflows. A backup preserves
the native database for restore; an export gives users an inspectable format for
portability. They solve different problems and should not be treated as
interchangeable.

For delete, reset, prune, and migration commands:

- Provide dry-run output with row counts or item identifiers.
- Require an explicit confirmation flag for non-interactive use.
- Create or require a backup when data is not rebuildable.
- Log enough context for support without leaking secrets.
- Make interruption behavior clear and tested.

## Design Review Checklist

- The architecture names the database location and override mechanism.
- Each command has a declared read/write set and transaction policy.
- Migrations are ordered, source-controlled, and tested from fixtures.
- The executable handles newer database schemas safely.
- Backup, restore, export, and doctor paths are present for important data.
- Tests use isolated database paths and prove rollback behavior.
- Destructive operations have dry-run and confirmation behavior.
- Error messages map database failures to user actions.
- The final design distinguishes rebuildable caches from authoritative data.

## Output Specification

Return a concise architecture packet with these sections:

1. Storage contract.
2. Command-to-data map.
3. Module layout.
4. Schema and migration policy.
5. Transaction policy.
6. Testing plan.
7. Operational safety plan.
8. Open risks and decisions.

If implementing code, include only the smallest scaffold needed to prove the
architecture: connection setup, migration runner, one read command, one mutating
command, and tests for migration plus rollback.

## Quality Rubric

The design passes when a reviewer can answer:

- Where is user data stored, and how can a test or operator override it?
- What happens if a command fails halfway through a write?
- What happens when an old database meets a new executable?
- What happens when a new database meets an old executable?
- How does a user back up, inspect, restore, and diagnose the database?
- Which tests prove those answers instead of assuming them?
