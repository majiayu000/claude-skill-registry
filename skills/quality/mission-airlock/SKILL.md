---
name: mission-airlock
description: "Run test and lint validation gate. Use after implementation to verify code quality."
---

# /mission-airlock - Validation Gate

Run tests, lint, and type checking before task completion.

---

## Instructions

### Step 1: Detect Project Type

Check for these files in project root:

| File | Type |
|------|------|
| `package.json` | Node.js |
| `Cargo.toml` | Rust |
| `pyproject.toml` or `setup.py` | Python |
| `go.mod` | Go |
| `Makefile` | Make |
| `build.gradle` | Gradle |
| `pom.xml` | Maven |

### Step 2: Run Tests

| Type | Command |
|------|---------|
| Node.js | `npm test` (if "test" script exists in package.json) |
| Rust | `cargo test` |
| Python | `pytest` or `python -m unittest discover` |
| Go | `go test ./...` |
| Make | `make test` (if target exists) |
| Gradle | `./gradlew test` |
| Maven | `mvn test` |

### Step 3: Run Lint

| Type | Command |
|------|---------|
| Node.js | `npm run lint` or `npx eslint .` or `npx biome check .` |
| Rust | `cargo clippy -- -D warnings` |
| Python | `ruff check .` or `flake8 .` |
| Go | `golangci-lint run` or `go vet ./...` |
| Make | `make lint` (if target exists) |
| Gradle | `./gradlew spotlessCheck` or `./gradlew checkstyleMain` |
| Maven | `mvn checkstyle:check` (if configured) |

### Step 4: Run Type Check (if applicable)

| Type | Command |
|------|---------|
| Node.js | `npx tsc --noEmit` (if tsconfig.json exists) |
| Python | `mypy .` (if configured) |

### Step 5: Report Result

- All pass → `=== RESULT: PASS ===`
- Any fail → `=== RESULT: FAIL ===`

---

## Pod Integration

**On PASS:** Proceed to `bd close <task_id>`.

**On FAIL:** Create blocking bug:

```bash
bd create -t bug --title="Airlock: [summary]" --priority=1
bd comments <bug-id> --add "[CONTEXT] Task: <task-id>, Failure: <type>, Output: <error>"
bd dep add <task-id> <bug-id>
bd sync
```

---

## Bug Severity

| Failure | Severity | Blocks? |
|---------|----------|---------|
| Tests fail | blocker (P1) | Yes |
| Build fail | critical (P0) | Yes + halt Ralph |
| Lint/Type fail | warning (P2) | No |
