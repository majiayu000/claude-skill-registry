---
name: precommit
description: Format, validate checkstyle, and run tests before committing — in the correct order
argument-hint: [module]
allowed-tools: Bash(./mvnw *)
---

## Pre-commit Check: Format → Validate → Test

Run this before every commit to catch format and checkstyle issues early.

`$ARGUMENTS` is an optional module name (e.g. `jhelm-core`). If omitted, runs against all modules.

---

### Step 1: Auto-format

**Single module:**
```bash
./mvnw spring-javaformat:apply -pl $ARGUMENTS
```

**All modules:**
```bash
./mvnw spring-javaformat:apply
```

---

### Step 2: Validate (checkstyle)

**Single module:**
```bash
./mvnw validate -pl $ARGUMENTS 2>&1 | grep -E "^\[ERROR\]|violations"
```

**All modules:**
```bash
./mvnw validate 2>&1 | grep -E "^\[ERROR\]|violations"
```

If violations remain after auto-format, invoke the `/checkstyle` skill to fix them manually. Do **not** proceed to Step 3 until `validate` passes cleanly.

---

### Step 3: Run tests

**Single module:**
```bash
./mvnw test -pl $ARGUMENTS 2>&1 | tail -20
```

**All modules (full build):**
```bash
./mvnw install 2>&1 | tail -20
```

---

### Outcome

Report a summary:

| Step | Result |
|------|--------|
| Format | Applied / Already clean |
| Checkstyle | 0 violations / N violations (list them) |
| Tests | X passed, 0 failures / list failures |

If everything is green, the working tree is ready to commit.
If anything fails, fix it before committing.
