# Validate Pipeline Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Orchestrate validation steps before closing a bead, aggregating results and enforcing gates.

## When to Activate

Use this skill when:
- beads-loop step 5 VERIFY COMPLETION
- Before bd close
- Run validation
- Check acceptance criteria
- About to close a bead

## Core Principles

### 1. Validation Before Closure

Beads cannot close until validation passes (or hybrid gates are explicitly overridden).

*Prevents incomplete or broken work from being marked complete.*

### 2. Hard Gates vs Hybrid Gates

Some validations (tests) cannot be overridden; others (fixture validation) allow agent override with justification.

*Test failures indicate broken code. Fixture issues may have valid reasons (new fixture not yet created, intentional deviation).*

### 3. Structured Output

All validation steps produce JSON conforming to the validation interface.

*Enables programmatic aggregation, reporting, and decision-making.*

### 4. Fail Fast With Context

When validation fails, provide actionable error information with file/line references.

*Agents and humans need to quickly understand what failed and where.*

---

## Workflow

### Phase 1: Load Configuration

Find and parse validation configuration.

1. Look for .beads/validation.yaml in project root
2. If not found, use sensible defaults (cargo test, clippy if Rust project)
3. Parse step definitions including blocking mode

**Outputs:** List of validation steps to execute, Blocking mode for each step (hard, hybrid, false)

### Phase 2: Execute Steps

Run each validation step in sequence.

1. For each step in configured order
2. Execute the step command
3. Capture JSON output from stdout
4. Parse return code (0=passed, 1=failed, 2=warning, 3=skipped)
5. Collect result into aggregate report
6. If hard gate fails, stop immediately

**Outputs:** Array of step results, Early exit if hard gate failed

### Phase 3: Aggregate Results

Combine step results into overall pass/fail decision.

1. Count passed, failed, warning, skipped
2. Identify blocking failures (hard gates that failed)
3. Identify hybrid failures (require justification to proceed)
4. Calculate overall status

**Outputs:** Aggregate result summary, List of failures requiring attention, List of warnings (advisory)

### Phase 4: Report and Gate

Output results and determine if bead can close.

1. Display human-readable summary
2. Output structured JSON report
3. If hard gate failed - block bead closure, provide fix guidance
4. If hybrid gate failed - prompt for override justification
5. If only warnings - allow closure with logged warnings
6. If all passed - allow closure

**Outputs:** Final verdict (can_close boolean), Required actions if blocked, Override justification if hybrid gate overridden

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Default Rust Validation** | Project has Cargo.toml and no explicit config | Run in order: 1. cargo test (hard gate), 2. cargo clippy --all-targets (warning), 3. cargo fmt --check (warning) | Standard Rust quality checks with sensible defaults |
| **Fixture Validation** | Project has tests/fixtures/ directory | Run fixture validation step (hybrid gate) | Fixtures must stay current but agent can override with justification |
| **Custom Steps** | .beads/validation.yaml exists | Execute steps as configured in order | Projects may have specific validation needs |
| **Override Documentation** | Agent overrides a hybrid gate | Document in bead notes: What validation failed, Why override is acceptable, What follow-up is needed (if any) | Overrides must be justified and tracked |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Skipping Validation** | Broken or incomplete work marked complete, breaks downstream beads | Always run validation before bd close |
| **Overriding Hard Gates** | Broken code gets committed, trust in system erodes | Fix the tests or the code until tests pass |
| **Silent Warnings** | Technical debt accumulates untracked | Log warnings in bead notes, file follow-up tasks for significant warnings |
| **Unstructured Output** | Pipeline cannot aggregate or report properly | Ensure all steps output valid JSON per validation-interface.md |

---

## Configuration Reference

### `.beads/validation.yaml` Format

```yaml
version: 1
steps:
  - name: cargo-test
    command: cargo test --no-fail-fast -- --nocapture
    blocking: hard    # No override possible
    
  - name: cargo-clippy
    command: cargo clippy --all-targets -- -D warnings
    blocking: false   # Advisory only (warning)
    
  - name: fixture-validate
    command: beadsmith validate fixtures
    blocking: hybrid  # Agent can override with justification
    
  - name: cargo-fmt
    command: cargo fmt --check
    blocking: false   # Advisory only
```

### Blocking Modes

| Mode | Behavior | Override |
|------|----------|----------|
| `hard` | Failure blocks bead closure | Never allowed |
| `hybrid` | Failure requires justification | Agent provides reason in notes |
| `false` | Advisory warning only | Not needed |

---

## Default Configuration

When no `.beads/validation.yaml` exists, the pipeline uses project-detection:

### Rust Projects (Cargo.toml exists)

```yaml
steps:
  - name: cargo-test
    command: cargo test
    blocking: hard
    
  - name: cargo-clippy
    command: cargo clippy --all-targets
    blocking: false
```

### Node.js Projects (package.json exists)

```yaml
steps:
  - name: npm-test
    command: npm test
    blocking: hard
    
  - name: npm-lint
    command: npm run lint
    blocking: false
```

---

## Quality Checklist

Before completing validation:

- [ ] Validation config found or defaults determined
- [ ] All configured steps executed in order
- [ ] Hard gates passed (no failures)
- [ ] Hybrid gate failures justified if overridden
- [ ] Warnings logged for visibility
- [ ] Structured report generated
- [ ] Bead notes updated with any overrides

---

## Examples

### All Validation Passes

```
1. Run cargo test -> 0 (passed)
2. Run clippy -> 2 (warning, 3 lints)
3. Run fmt --check -> 0 (passed)
4. Aggregate: 2 passed, 0 failed, 1 warning
5. Log: "Validation passed with 3 clippy warnings"
6. Allow bead closure
```

### Hard Gate Failure (Tests Fail)

```
1. Run cargo test -> 1 (failed)
   Output: {"step":"cargo-test","status":"failed","errors":[...]}
2. Stop immediately (hard gate)
3. Report: "Validation blocked: 2 test failures"
4. Display error details with file/line references
5. Block bead closure
6. Agent must fix tests and re-run validation
```

### Hybrid Gate Override

```
1. Run cargo test -> 0 (passed)
2. Run fixture validate -> 1 (failed, 1 missing fixture)
3. Agent analyzes: fixture for new feature, will be created in follow-up bead
4. Agent provides justification: "New fixture, tracked in beadsmith-e12.5"
5. Log override in bead notes
6. Allow bead closure with documented override
```

---

## Integration with beads-loop

The validation pipeline integrates at step 5 (VERIFY COMPLETION) of beads-loop:

```
LOOP:
  ...
  4. EXECUTE THE BEAD
     Implement per acceptance criteria
     
  5. VERIFY COMPLETION
     Run: /validate-pipeline   <-- This skill
     If blocked -> Fix issues, GOTO step 5
     If warnings -> Log to notes
     If passed -> Continue to step 6
     
  6. CLOSE THE BEAD
     Run: bd close <id> -r "Completed: <summary>"
  ...
```

---

## References

- [docs/validation-interface.md](../docs/validation-interface.md) - Validation step interface spec
- [commands/beads-loop.md](../commands/beads-loop.md) - Step 5 VERIFY COMPLETION
- beadsmith-e12.2 - Design validation step interface (completed)
