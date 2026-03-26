---
name: test-cases-generation
description: >
  Generates structured test case sets with multi-dimensional coverage from project
  code analysis or specification documents. This skill activates when the user asks
  to write test cases, generate tests, supplement tests, create test coverage, or
  improve test completeness. It auto-scans the project to extract testable units
  (APIs, functions, components, CLI commands, tool definitions), identifies coverage
  gaps, designs test cases across multiple dimensions (coverage depth, input types,
  interaction patterns), and produces a structured test case document with coverage
  matrix. Includes test strategy and methodology by default. Use --formal flag to
  add management sections (environment, roles, schedule, defect management).
instructions: >
  Generate structured test case sets by scanning the project to extract testable
  units, identifying coverage gaps, designing multi-dimensional test cases, and
  producing a coverage matrix. Follow the seven-step workflow defined in this skill,
  reference the template at references/template.md, and validate output against
  the checklist at references/checklist.md.
---

# Test Cases Generation Skill

## What Are Test Cases?

Test cases are structured specifications that define what to test, how to test it, and what the expected outcome should be. Unlike a test plan (which focuses on strategy, schedule, roles, and process), test cases are the actionable core — each one is detailed enough for an engineer to translate directly into test code.

This skill treats test case design as a distinct discipline from test planning and test implementation:

- **Test Planning** (strategy, process, roles) → optional, available via `--formal` flag
- **Test Design** (what cases, which dimensions, what coverage) → this skill's core output
- **Test Implementation** (writing code) → downstream, handled by `code-forge:tdd`

## Core Capabilities

### Auto-Scan and Extract

The skill can automatically scan a project to extract testable units without requiring the user to provide a specification document. It identifies:

- **REST API routes** — endpoints, methods, parameters, response codes
- **Functions and methods** — signatures, parameter types, return values, branch logic
- **React/Vue/Svelte components** — props, events, state transitions
- **CLI commands** — commands, subcommands, flags, arguments
- **AI tool definitions** — tool names, trigger conditions, parameters, combination patterns
- **Database models** — schemas, relationships, constraints
- **Event handlers** — event types, payloads, side effects
- **Middleware/interceptors** — conditions, transformations, error handling

### Multi-Dimensional Coverage

Every test case set is organized across dimensions. The skill provides built-in dimensions and can auto-detect project-specific dimensions.

#### Built-in Dimensions

**Coverage Depth** (always applied):

| Level | Name | Description | Minimum per testable unit |
|-------|------|-------------|--------------------------|
| L1 | Happy Path | Basic correct behavior with valid inputs | 1 case |
| L2 | Boundary & Error | Edge cases, invalid inputs, error handling | 2 cases |
| L3 | Negative | Scenarios that should NOT trigger behavior | 1 case |

**Test Category** (apply categories relevant to the project):

| Category | When to Include | Description |
|----------|----------------|-------------|
| Functional | Always | Correct behavior verification |
| Data Integrity | Project has database / persistent store | Constraints, transactions, cascades |
| Security | Project handles auth, user input, or sensitive data | Auth, injection, access control |
| Performance | Project has latency/throughput requirements | Response time, throughput, resource usage |

#### Auto-Detected Dimensions

The skill analyzes the project to discover additional dimensions. Examples:

| Project Type | Auto-Detected Dimension | Values |
|-------------|------------------------|--------|
| AI Tool Calling | Trigger Mode | Single tool / Combo tools |
| AI Tool Calling | Conversation Turns | Single turn / Multi-turn |
| REST API | Auth Context | Unauthenticated / User / Admin |
| Frontend Component | Device Context | Desktop / Mobile / Tablet |
| CLI Tool | Input Source | Args / Stdin / Config file |
| CLI Tool | Output Format | JSON / Table / Plain text |
| Event System | Delivery Mode | Sync / Async / Batch |
| Function Library | Input Type | Primitive / Object / Array / Null / Undefined |
| Data Pipeline | Data Volume | Empty / Small / Large / Malformed |
| SDK / Client | Connection State | Connected / Disconnected / Reconnecting |

Auto-detected dimensions are presented to the user for confirmation before generating cases.

### Combination Testing

When testable units interact with each other, the skill generates combination test cases:

1. **Identify interaction pairs** — which units call, depend on, or affect each other
2. **Generate combination matrix** — pairwise combinations of interacting units
3. **Design combination cases** — test the interaction, not just individual units
4. **Prioritize combinations** — rank by risk (high coupling = high priority)

## Seven-Step Workflow

### Step 1 — Determine Input Mode and Project Profile

This step answers two questions: **how** to find testable units (input mode) and **what kind** of project this is (project profile).

#### 1a. Input Mode

| User Provides | Mode | Behavior |
|--------------|------|----------|
| Specification document (`@docs/features/auth.md`) | **Spec Mode** | Parse spec, extract testable requirements |
| Code path (`@src/services/payment.ts`) | **Code Mode** | Analyze code, extract testable units |
| Nothing or just a name | **Scan Mode** | Full project scan, discover everything |

#### 1b. Project Profile Detection

Scan the project to determine its type. Check for framework signatures and unit type distribution:

| Signal | Project Profile |
|--------|----------------|
| HTTP framework detected (Express, FastAPI, Spring Boot, Gin, NestJS, Koa, Hono, etc.) AND route/endpoint units present | **Web API** |
| CLI framework detected (Click, Cobra, Commander, clap, argparse with subcommands, etc.) OR command/subcommand units present | **CLI Tool** |
| Frontend framework detected (React, Vue, Svelte, Angular, etc.) AND component units present | **Frontend App** |
| Tool/plugin definitions with trigger conditions, LLM framework detected (LangChain, Vercel AI SDK, etc.) | **AI Agent** |
| Pipeline/transform/ETL patterns, data processing frameworks (Airflow, Prefect, dbt, etc.) | **Data Pipeline** |
| Exported functions/classes as primary interface, no routes/commands/components, published as package | **Function Library** |
| Client/SDK methods with connection management, API wrapper patterns | **SDK / Client Library** |

**Detection method:**
1. Scan `package.json` dependencies, `pyproject.toml`, `Cargo.toml`, `go.mod`, `build.gradle` for framework signatures
2. Count extracted unit types: routes vs. functions vs. components vs. commands vs. tools
3. Check for database presence: ORM imports, migration files, DB config
4. Check for auth presence: auth middleware, JWT/OAuth imports, permission decorators

**Output**: Explicit project profile label with rationale, e.g.: "Project Profile: **Web API** (Express detected in package.json, 12 route handlers found, PostgreSQL via Prisma)"

### Step 2 — Deep Scan and Extract

Extraction must go beyond listing function signatures. For each testable unit, capture four layers:

| Layer | What to Extract | Why It Matters |
|-------|----------------|----------------|
| **Interface** | Public API surface — function signatures, type contracts, trait/interface boundaries, input/output types | Defines what CAN be tested from outside |
| **Logic** | Branch paths, error handling chains, state transitions, validation rules, business logic | Defines what SHOULD be tested (complexity = risk) |
| **Architecture** | Module structure, layer boundaries, dependency direction, separation of concerns | Defines test STRATEGY (unit vs integration vs E2E) |
| **Relationships** | Call graphs, data flow between units, event propagation, shared state, trait implementations | Defines COMBINATION tests (which units interact) |

#### 2a. Project Scan (all modes)

1. **Glob the project tree** to discover structure, source modules, and naming conventions.
2. **Read the README** to understand the project's purpose and architecture.
3. **Identify the tech stack** by scanning `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.
4. **Detect project frameworks** (not just test frameworks):
   - HTTP frameworks: Express, FastAPI, Spring Boot, Gin, NestJS, Koa, Hono, etc.
   - CLI frameworks: Click, Cobra, Commander, clap, argparse, etc.
   - Frontend frameworks: React, Vue, Svelte, Angular, etc.
   - AI frameworks: LangChain, Vercel AI SDK, AutoGen, etc.
   - Test frameworks: Jest, pytest, Go test, JUnit, Vitest, etc.

#### 2b. Language-Aware Deep Extraction

Use the language-specific strategy matching the project's tech stack. Each strategy defines how to find ALL testable units across the four layers.

##### Python

| Layer | How to Extract |
|-------|---------------|
| **Interface** | Read `__init__.py` for `__all__` or public imports. Scan all `.py` files for `def`/`class` without leading `_`. Record decorators (`@app.route`, `@click.command`, `@property`). Extract type hints from signatures. |
| **Logic** | Count `if/elif/else`, `try/except`, `match/case` branches per function. Identify `raise` statements (error paths). Find `assert` statements (invariants). Identify state machines (class with state-changing methods). |
| **Architecture** | Map `import` statements to build module dependency graph. Identify layers (routes → services → repositories). Detect circular imports. Identify Abstract Base Classes (ABC) that define contracts. |
| **Relationships** | Trace function calls across modules (A calls B). Identify shared state (module-level variables, singletons). Map signal/event dispatchers to handlers. Identify dependency injection patterns. |

##### TypeScript / JavaScript

| Layer | How to Extract |
|-------|---------------|
| **Interface** | Read `index.ts` for `export` statements. Follow `export * from './module'` re-exports. Scan for `export function`, `export class`, `export interface`, `export type`. Extract parameter types and return types. Record `@decorator()` patterns. |
| **Logic** | Count `if/else`, `switch/case`, ternary operators per function. Identify `throw` statements and `try/catch` chains. Find `Promise` rejection paths. Identify state management patterns (reducers, stores). Detect `async/await` error propagation. |
| **Architecture** | Map `import` statements to build dependency graph. Identify barrel exports (`index.ts` re-export chains). Detect layer patterns (controllers → services → repositories). Identify React component tree (parent → child props). |
| **Relationships** | Trace function/method calls across modules. Map event emitters to listeners (`on/emit`, `addEventListener`). Map React context providers to consumers. Identify callback chains and promise pipelines. Map API client calls to server endpoints. |

##### Go

| Layer | How to Extract |
|-------|---------------|
| **Interface** | Scan all `.go` files for capitalized identifiers (exported). Extract function signatures, method receivers, interface definitions. Record struct field visibility (capitalized = public). Identify interface satisfaction (implicit implementation). |
| **Logic** | Count `if/else`, `switch/case` branches. Trace `error` return values through call chains (Go's error propagation pattern). Identify `defer/panic/recover` paths. Find goroutine spawning (`go func()`) and channel operations. |
| **Architecture** | Map package imports to build dependency graph. Identify internal packages (`internal/`). Detect interface-based abstraction layers. Identify `cmd/` entry points vs. library packages. |
| **Relationships** | Trace function calls across packages. Map interface implementors (which structs satisfy which interfaces). Identify channel communication patterns between goroutines. Map middleware chains. |

##### Rust

**Rust requires the deepest extraction** due to its unique type system. Surface-level scanning of `lib.rs` is NOT sufficient.

| Layer | How to Extract |
|-------|---------------|
| **Interface** | **1. Follow the mod tree**: Read `src/lib.rs` → find all `mod` and `pub mod` declarations → recursively read each module file (`src/{mod_name}.rs` or `src/{mod_name}/mod.rs`). **2. Track re-exports**: Follow `pub use` chains to determine the final public API. `pub use submod::MyStruct` in `lib.rs` makes `MyStruct` part of the crate's public API even if defined deep in a submodule. **3. Extract pub items**: `pub fn`, `pub struct`, `pub enum`, `pub trait`, `pub type`, `pub const`, `pub static`. **4. Parse visibility modifiers**: Distinguish `pub` (fully public), `pub(crate)` (crate-internal), `pub(super)` (parent module only). Only `pub` items are part of the external API; `pub(crate)` items are testable but internal. **5. Extract generic constraints**: Record `where` clauses and trait bounds (e.g., `fn process<T: Handler + Send>(item: T)` → testable with any `T` implementing `Handler + Send`). |
| **Logic** | **1. Pattern matching exhaustiveness**: Identify `match` arms — Rust enforces exhaustive matching, each arm is a branch to test. **2. Result/Option chains**: Trace `?` operator propagation, `unwrap()` calls (panic risk), `map/and_then/unwrap_or` chains. **3. Error types**: Find `enum` error types and their variants — each variant is a testable error path. **4. Unsafe blocks**: Each `unsafe` block is a high-risk area needing focused testing. **5. Lifetime constraints**: Functions with complex lifetime bounds may have subtle edge cases around borrow validity. **6. Derive macros**: `#[derive(Serialize, Deserialize)]` generates testable serialization behavior. `#[derive(Clone, PartialEq)]` generates comparison behavior. |
| **Architecture** | **1. Crate structure**: Map `src/lib.rs` → modules → submodules to understand the module tree. **2. Dependency graph**: Read `Cargo.toml` for crate dependencies; read `use` statements for internal module dependencies. **3. Trait abstraction layers**: Identify trait definitions that serve as interfaces between layers (e.g., `trait Repository` defining the data access contract). **4. Feature flags**: Read `[features]` in `Cargo.toml` — conditional compilation means different code paths need different tests. **5. Workspace structure**: If `Cargo.toml` has `[workspace]`, scan member crates for cross-crate dependencies. |
| **Relationships** | **1. Trait implementations**: Find all `impl Trait for Struct` blocks — these define behavioral contracts that must be tested. **2. Method implementations**: Find all `impl Struct` blocks to discover methods. Methods may be spread across multiple files. **3. Generic type consumers**: Trace where generic functions are called with concrete types — each concrete instantiation may have different behavior. **4. Async task spawning**: Identify `tokio::spawn`, `async_std::task::spawn` — each spawned task is an interaction point. **5. Channel communication**: `mpsc::channel`, `oneshot::channel`, `broadcast` — data flow between components. **6. Trait object dispatch**: `Box<dyn Trait>`, `&dyn Trait` — dynamic dispatch points where different implementations may be used. |

##### Other Languages

For languages not listed above, apply the same four-layer extraction principle:
1. Find all public symbols (Interface)
2. Count branches and error paths (Logic)
3. Map module/package dependencies (Architecture)
4. Trace cross-module calls and shared state (Relationships)

#### 2c. Scan Existing Tests

1. Find test files matching patterns: `**/*.test.*`, `**/*.spec.*`, `**/__tests__/**`, `**/test_*`, `**/tests/**`, `tests/**`, `*_test.go`, `**/*_test.rs`
2. For each test file, identify which source units are being tested
3. Calculate: which units have tests, which don't, rough coverage assessment

#### 2d. Scan Verification

After extraction, verify completeness:

1. **File coverage**: Count source files scanned vs. total source files. If < 90% were scanned, investigate why (excluded patterns? binary files? generated code?)
2. **Unit count sanity check**: Compare number of extracted units against project size. Rough heuristic: a typical source file has 2-8 testable units. If a 50-file project yields only 20 units, something was missed.
3. **Module tree completeness** (Rust-specific): Verify every `mod` declaration in `lib.rs` has a corresponding scanned module file. Missing modules = missed API surface.
4. **Re-export tracking** (Rust/TS): Verify all `pub use` / `export * from` chains were followed to their source.

If verification reveals gaps, re-scan the missed areas before proceeding.

#### 2e. Produce Functional Inventory

The inventory must include all four layers per unit:

```
Unit: createUser
  Type: route (POST /api/users)
  File: src/routes/users.ts:42
  Interface: (name: string, email: string) → User | ValidationError
  Logic: 3 branches (valid → create, duplicate → conflict, invalid → 400)
  Architecture: Route layer → calls UserService.create → calls UserRepository.save
  Relationships: depends on UserService, UserRepository; triggers UserCreatedEvent
  Has Tests: Partial (happy path only)
  Coverage Status: L1 covered, L2/L3 missing
```

**Scan Mode**: Perform steps 2a-2e for the full project.

**Code Mode**: Perform steps 2a-2e scoped to specified files + their dependencies. Project profile from full project context.

**Spec Mode**: Read spec document → extract requirements → map to testable behaviors → infer layers from spec descriptions.

### Step 3 — Detect Dimensions

After extracting testable units, analyze the project to identify applicable dimensions:

1. **Apply built-in dimensions** — Coverage Depth (L1/L2/L3) is always on
2. **Detect project-specific dimensions** by analyzing:
   - Auth patterns → Auth Context dimension (anonymous/user/admin)
   - API patterns → HTTP Method dimension if relevant
   - Tool/plugin patterns → Trigger Mode, Combination patterns
   - Frontend patterns → Device/viewport dimensions
   - Event patterns → Delivery Mode dimension
3. **Present dimensions to user** for confirmation:
   - Show built-in dimensions (cannot disable L1/L2/L3)
   - Show detected dimensions with rationale
   - Allow user to add custom dimensions
   - Allow user to remove irrelevant detected dimensions

### Step 4 — Confirm Scope with User

Present the analysis results and ask the user to confirm:

1. **Functional Inventory Summary** — "{N} testable units found across {M} modules, {X} currently have tests, {Y} do not"
2. **Coverage Gaps** — list uncovered units, grouped by module
3. **Detected Dimensions** — show the dimension matrix
4. **Scope Question** — "Generate test cases for: (A) all uncovered units, (B) all units (including re-testing covered ones), (C) specific modules only?"
5. **Business Logic Gaps** — "Are there any business rules, edge cases, or domain-specific behaviors that I can't infer from the code? (e.g., 'orders over $1000 require manager approval')"

Wait for user responses before proceeding.

### Step 5 — Generate Test Cases

Using the confirmed scope, dimensions, and user context, generate the test case set by filling in the template at `references/template.md`.

#### Generation Rules

**Per testable unit, generate at minimum:**
- 1 × L1 (Happy Path) case
- 2 × L2 (Boundary & Error) cases — at least one boundary, one error
- 1 × L3 (Negative) case — something that should NOT happen

**For each auto-detected dimension, cross with coverage depth:**
- If Auth Context dimension has 3 values × L1/L2/L3 = up to 9 cases per unit (prioritize, don't generate all blindly)

**Combination test cases:**
- Identify units with interaction relationships (calls, imports, data flow)
- Generate pairwise combination cases for high-risk interaction pairs
- Each combination case specifies which units are involved and their interaction sequence

**I/O and external dependency test cases:**
- **Own dependencies** (database, file system, cache, message queue) → test for real, not mocked
- **External services** (third-party APIs, payment gateways) → mock/stub acceptable
- If project has a database, include Data Integrity cases: unique constraints, FK constraints, cascade, transaction rollback, concurrent updates
- If project has no database or external I/O, skip Data Integrity section and simplify Test Infra column

**Priority assignment:**
- P0: Core functionality, critical path, data integrity
- P1: Important edge cases, security, error handling
- P2: Nice-to-have, cosmetic, low-risk scenarios

### Step 6 — Build Coverage Matrix

After generating all test cases, construct the coverage matrix:

1. **Unit Coverage Matrix** — rows = testable units, columns = dimensions, cells = test case IDs
2. **Dimension Coverage Matrix** — rows = dimension values, columns = coverage depth (L1/L2/L3), cells = count
3. **Gap Analysis** — flag any cells with zero coverage
4. **Statistics** — total cases, breakdown by priority, breakdown by category, breakdown by depth

If upstream SRS/Tech Design documents exist, also build a **Requirements Traceability Matrix** mapping requirement IDs to test case IDs.

### Step 7 — Quality Check and Output

1. Validate against `references/checklist.md`
2. Fix any issues before finalizing
3. Write output to `docs/<feature-name>/test-cases.md`
4. Return: file path, summary, total TC count, coverage statistics

## Test Case Writing Standards

### ID Format

```
TC-<MODULE>-<NNN>
```

- **TC** — fixed prefix
- **MODULE** — 3-5 character uppercase code for feature area (AUTH, PAY, CART, TOOL, CLI)
- **NNN** — zero-padded three-digit sequence starting at 001

### Test Case Structure

Each test case must be implementation-ready. Fields:

- **TC ID** — unique identifier (TC-MODULE-NNN)
- **Title** — pattern: `[action] [condition] [expected outcome]`
- **Module** — feature area or component under test
- **Dimensions** — which dimension values this case covers (e.g., `L2, Auth:admin`)
- **Priority** — P0 / P1 / P2
- **Category** — Functional / Data Integrity / Security / Performance
- **Preconditions** — exact state before test runs (database records with specific field values, auth state, config flags). No vague descriptions.
- **Steps** — numbered steps with concrete test data. Use real values: `name: "John Doe"`, `email: "test@example.com"`. Never use placeholders like `[valid name]`.
- **Expected Result** — two parts: (1) Response/output (exact status code, body structure). (2) State After (for write operations, exact database/state verification).
- **Not Expected** — what should NOT happen (required for L3 cases, recommended for all)
- **Test Infra** — what infrastructure the test needs: Real DB / Temp dir / Mock external (with justification) / N/A
- **Automation** — automated / to-be-automated / manual

### Anti-Shortcut Rules

These shortcuts are strictly prohibited:

1. **No placeholders** — use concrete values, not `[valid email]`
2. **No mocking own dependencies** — test your own DB/file system/cache/queue for real; only mock external services you don't control
3. **No happy-path-only** — every unit needs L1 + L2 + L3 coverage (minimum 1+2+1 = 4 cases per unit)
4. **No vague expected results** — specify exact output (return value / status code / exit code / rendered content) AND state changes
5. **No missing L3 cases** — every testable unit needs at least one "should NOT happen" case
6. **No blind combination explosion** — prioritize combinations by risk, don't generate all permutations
7. **No forcing irrelevant sections** — if project has no DB, skip Data Integrity; if no auth, skip auth tests. Adapt to actual project profile
8. **No omitting coverage matrix** — the matrix is a required output, it proves completeness
9. **No HTTP-specific language for non-HTTP projects** — use exit codes for CLI, return values for libraries, rendered output for frontend. Match the project's interface

## Test Strategy Section (Default)

The default output includes a concise test strategy covering:

- **Test Pyramid** — distribution rationale with project-specific justification
- **Test Methods** — black-box, white-box, gray-box applicability
- **External Dependency Policy** — what to test for real vs. mock (DB, file system, external APIs)
- **Risk-Based Prioritization** — how P0/P1/P2 were assigned

This is NOT a full test plan — it's the methodology context needed to understand the test cases. Sections are adapted to the project type (e.g., Data Integrity is omitted for projects without a database).

## Formal Mode (`--formal`)

When `--formal` flag is provided, the output additionally includes:

- Document information and revision history
- Test environment specifications (hardware, software, network)
- Entry and exit criteria
- Test data management strategy
- Defect management process (severity classification, lifecycle, reporting template)
- Risk assessment (testing risks, product risks with reasoning)
- Test schedule (Gantt chart, milestones)
- Roles and responsibilities

These sections follow IEEE 829 structure for teams that need formal QA documentation.

## Reference Files

- **`references/template.md`** — output template with default and formal sections
- **`references/checklist.md`** — quality validation checklist

Always read both files before generating test cases.

## Output Location

The finished test cases document is written to:

```
docs/<feature-name>/test-cases.md
```

where `<feature-name>` is a lowercase, hyphen-separated slug. If the directory does not exist, create it. If a file already exists, confirm before overwriting.

## Downstream Integration

The output is designed to be consumed by `code-forge:tdd` in driven mode:

```
/code-forge:tdd @docs/<feature-name>/test-cases.md
```

This will iterate through the test cases and implement each one following the Red-Green-Refactor cycle.
