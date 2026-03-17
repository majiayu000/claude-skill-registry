---
name: quality-verify-integration
description: Verifies components are integrated into the system, not just created. Detects orphaned code (exists but never imported). Use BEFORE marking features complete, moving ADRs to completed/, or claiming integration work done. Enforces Creation-Connection-Verification (CCV) principle.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Verify Integration

## Purpose

Prevent "done but not integrated" failures where:
- Code exists ✓
- Unit tests pass ✓
- Quality gates pass ✓
- **But code is never called at runtime** ✗

## When to Use

**MANDATORY before:**
- Moving ADR to `3_completed/`
- Marking todo tasks complete for integration work
- Claiming a feature is "done" or "working"
- Creating a PR for integration changes

## The CCV Principle

```
COMPLETE = CREATION + CONNECTION + VERIFICATION
```

| Phase | What It Proves | Required Evidence |
|-------|----------------|-------------------|
| **CREATION** | Artifact exists | File, tests, types |
| **CONNECTION** | Wired into system | Import, registration |
| **VERIFICATION** | Works at runtime | Logs, output |

**Missing any phase = NOT complete**

## The Four Questions Test

Before "done", answer ALL FOUR:

1. **How do I trigger this?** (entry point)
2. **What connects it to the system?** (import/registration)
3. **What proves it runs?** (logs/traces)
4. **What shows it works?** (outcome)

Cannot answer all four? → **NOT COMPLETE**

## Quick Verification

### Step 1: Check for Orphaned Modules

```bash
# Run orphan detection script
./scripts/verify_integration.sh

# Or manual check for specific module
grep -r "from.*module_name import\|import.*module_name" src/ --include="*.py" | grep -v test
```

**If no matches → Module NOT integrated**

### Step 2: Verify Call-Sites

```bash
# Check if function/class is actually called
grep -r "function_name\|ClassName" src/ --include="*.py" | grep -v "^def \|^class " | grep -v test
```

**If no matches → Code never called**

### Step 3: Check Context-Specific Integration

**LangGraph Nodes:**
```bash
grep -n "from.*nodes import\|add_node.*name" src/temet_run/coordination/graph/builder.py
```

**DI Services:**
```bash
grep -n "providers.Singleton\|providers.Factory" src/temet_run/container.py
```

**CLI Commands:**
```bash
grep -n "add_command\|@app.command" src/temet_run/cli/app.py
```

### Step 4: Demand Runtime Proof

Require one of:
- Integration test output showing component exists
- Logs from execution showing code ran
- State inspection showing fields populated

## Connection Patterns

See [references/connection-patterns.md](references/connection-patterns.md) for:
- LangGraph node integration
- Dependency Injection patterns
- CLI command registration
- API endpoint wiring
- Configuration loading

## Verification Report Template

```markdown
## Integration Verification: [Feature Name]

### CCV Status

**CREATION:** ✅ / ❌
- Files: [list]
- Tests: [count] passing
- Types: mypy passes

**CONNECTION:** ✅ / ❌
- Import location: [file:line]
- Registration: [how wired]
- Entry point: [how triggered]

**VERIFICATION:** ✅ / ❌
- Integration test: [pass/fail]
- Runtime logs: [attached/missing]
- Expected outcome: [observed/not observed]

### Four Questions

1. Trigger: [answer or UNANSWERED]
2. Connection: [answer or UNANSWERED]
3. Execution proof: [answer or UNANSWERED]
4. Outcome proof: [answer or UNANSWERED]

### Verdict

**APPROVED ✅** — All phases complete, evidence attached
OR
**BLOCKED ❌** — Missing: [list what's missing]
```

## Supporting Files

- [references/connection-patterns.md](references/connection-patterns.md) - Integration patterns by artifact type

## Success Criteria

- [ ] No orphaned modules (verify_integration.sh passes)
- [ ] All imports verified with grep
- [ ] All call-sites verified
- [ ] Context-specific checks passed
- [ ] Four Questions answered
- [ ] Runtime proof attached
