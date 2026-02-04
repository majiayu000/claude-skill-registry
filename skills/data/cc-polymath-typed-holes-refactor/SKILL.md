---
name: typed-holes-refactor
description: Refactor codebases using Design by Typed Holes methodology - iterative, test-driven refactoring with formal hole resolution, constraint propagation, and continuous validation. Use when refactoring existing code, optimizing architecture, or consolidating technical debt through systematic hole-driven development.
---

# Typed Holes Refactoring

Systematically refactor codebases using the Design by Typed Holes meta-framework: treat architectural unknowns as typed holes, resolve them iteratively with test-driven validation, and propagate constraints through dependency graphs.

## Core Workflow

### Phase 0: Hole Discovery & Setup

**1. Create safe working branch:**

```bash
git checkout -b refactor/typed-holes-v1
# CRITICAL: Never work in main, never touch .beads/ in main
```

**2. Analyze current state and identify holes:**

```bash
python scripts/discover_holes.py
# Creates REFACTOR_IR.md with hole catalog
```

The Refactor IR documents:
- **Current State Holes**: What's unknown about the current system?
- **Refactor Holes**: What needs resolution to reach the ideal state?
- **Constraints**: What must be preserved/improved/maintained?
- **Dependencies**: Which holes block which others?

**3. Write baseline characterization tests:**

Create `tests/characterization/` to capture exact current behavior:

```python
# tests/characterization/test_current_behavior.py
def test_api_contracts():
    """All public APIs must behave identically post-refactor"""
    for endpoint in discover_public_apis():
        old_result = run_current(endpoint, test_inputs)
        save_baseline(endpoint, old_result)

def test_performance_baselines():
    """Record current performance - don't regress"""
    baselines = measure_all_operations()
    save_json("baselines.json", baselines)
```

Run tests on main branch - they should all pass. These are your safety net.

### Phase 1-N: Iterative Hole Resolution

For each hole (in dependency order):

**1. Select next ready hole:**

```bash
python scripts/next_hole.py
# Shows holes whose dependencies are resolved
```

**2. Write validation tests FIRST (test-driven):**

```python
# tests/refactor/test_h{N}_resolution.py
def test_h{N}_resolved():
    """Define what 'resolved correctly' means"""
    # This should FAIL initially
    assert desired_state_achieved()

def test_h{N}_equivalence():
    """Ensure no behavioral regressions"""
    old_behavior = load_baseline()
    new_behavior = run_refactored()
    assert old_behavior == new_behavior
```

**3. Implement resolution:**

- Refactor code to make tests pass
- Keep characterization tests passing
- Commit incrementally with clear messages

**4. Validate resolution:**

```bash
python scripts/validate_resolution.py H{N}
# Checks: tests pass, constraints satisfied, main untouched
```

**5. Propagate constraints:**

```bash
python scripts/propagate.py H{N}
# Updates dependent holes based on resolution
```

**6. Document and commit:**

```bash
git add .
git commit -m "Resolve H{N}: {description}

- Tests: tests/refactor/test_h{N}_*.py pass
- Constraints: {constraints satisfied}
- Propagates to: {dependent holes}"
```

### Phase Final: Reporting

**Generate comprehensive delta report:**

```bash
python scripts/generate_report.py > REFACTOR_REPORT.md
```

Report includes:
- Hole resolution summary with validation evidence
- Metrics delta (LOC, complexity, coverage, performance)
- Behavioral analysis (intentional changes documented)
- Constraint validation (all satisfied)
- Risk assessment and migration guide

## Key Principles

### 1. Test-Driven Everything

- Write validation criteria BEFORE implementing
- Tests define "correct resolution"
- Characterization tests are sacred - never let them fail

### 2. Hole-Driven Progress

- Resolve holes in dependency order
- Each resolution propagates constraints
- Track everything formally in Refactor IR

### 3. Continuous Validation

Every commit must validate:
- ✅ Characterization tests pass (behavior preserved)
- ✅ Resolution tests pass (hole resolved correctly)
- ✅ Constraints satisfied
- ✅ Main branch untouched
- ✅ `.beads/` intact in main

### 4. Safe by Construction

- Work only in refactor branch
- Main is read-only reference
- Beads are untouchable historical artifacts

### 5. Formal Completeness

Design complete when:
- All holes resolved and validated
- All constraints satisfied
- All phase gates passed
- Metrics improved or maintained

## Hole Quality Framework

### SMART Criteria for Good Holes

Every hole must be:

- **Specific**: Clear, bounded question with concrete answer
  - ✓ Good: "How should error handling work in the API layer?"
  - ✗ Bad: "How to improve the code?"

- **Measurable**: Has testable validation criteria
  - ✓ Good: "Reduce duplication from 60% to <15%"
  - ✗ Bad: "Make code better"

- **Achievable**: Can be resolved with available information
  - ✓ Good: "Extract parsing logic to separate module"
  - ✗ Bad: "Predict all future requirements"

- **Relevant**: Blocks meaningful progress on refactoring
  - ✓ Good: "Define core interface (blocks 5 other holes)"
  - ✗ Bad: "Decide variable naming convention"

- **Typed**: Clear type/structure for resolution
  - ✓ Good: `interface Architecture = { layers: Layer[], rules: Rule[] }`
  - ✗ Bad: "Some kind of structure?"

### Hole Estimation Framework

Size holes using these categories:

| Size | Duration | Characteristics | Examples |
|------|----------|-----------------|----------|
| **Nano** | 1-2 hours | Simple, mechanical changes | Rename files, update imports |
| **Small** | 4-8 hours | Single module refactor | Extract class, consolidate functions |
| **Medium** | 1-3 days | Cross-module changes | Define interfaces, reorganize packages |
| **Large** | 4-7 days | Architecture changes | Layer extraction, pattern implementation |
| **Epic** | >7 days | **SPLIT THIS HOLE** | Too large, break into smaller holes |

**Estimation Red Flags**:
- More than 3 dependencies → Likely Medium+
- Unclear validation → Add time for discovery
- New patterns/tools → Add learning overhead

### Hole Splitting Guidelines

**Split a hole when**:
1. Estimate exceeds 7 days
2. More than 5 dependencies
3. Validation criteria unclear
4. Multiple distinct concerns mixed

**Splitting strategy**:
```
Epic hole: "Refactor entire authentication system"
→ Split into:
  R10_auth_interface: Define new auth interface (Medium)
  R11_token_handling: Implement JWT tokens (Small)
  R12_session_management: Refactor sessions (Medium)
  R13_auth_middleware: Update middleware (Small)
  R14_auth_testing: Comprehensive test suite (Medium)
```

**After splitting**:
- Update dependencies in REFACTOR_IR.md
- Run `python scripts/propagate.py` to update graph
- Re-sync with beads: `python scripts/holes_to_beads.py`

## Common Hole Types

### Architecture Holes

```python
"?R1_target_architecture": "What should the ideal structure be?"
"?R2_module_boundaries": "How should modules be organized?"
"?R3_abstraction_layers": "What layers/interfaces are needed?"
```

**Validation:** Architecture tests, dependency analysis, layer violation checks

### Implementation Holes

```python
"?R4_consolidation_targets": "What code should merge?"
"?R5_extraction_targets": "What code should split out?"
"?R6_elimination_targets": "What code should be removed?"
```

**Validation:** Duplication detection, equivalence tests, dead code analysis

### Quality Holes

```python
"?R7_test_strategy": "How to validate equivalence?"
"?R8_migration_path": "How to safely transition?"
"?R9_rollback_mechanism": "How to undo if needed?"
```

**Validation:** Test coverage metrics, migration dry-runs, rollback tests

See [HOLE_TYPES.md](references/HOLE_TYPES.md) for complete catalog.

## Constraint Propagation Rules

### Rule 1: Interface Resolution → Type Constraints

```
When: Interface hole resolved with concrete types
Then: Propagate type requirements to all consumers

Example:
  Resolve R6: NodeInterface = BaseNode with async run()
  Propagates to:
    → R4: Parallel execution must handle async
    → R5: Error recovery must handle async exceptions
```

### Rule 2: Implementation → Performance Constraints

```
When: Implementation resolved with resource usage
Then: Propagate limits to dependent holes

Example:
  Resolve R4: Parallelization with max_concurrent=3
  Propagates to:
    → R8: Rate limit = provider_limit / 3
    → R7: Memory budget = 3 * single_operation_memory
```

### Rule 3: Validation → Test Requirements

```
When: Validation resolved with test requirements
Then: Propagate data needs upstream

Example:
  Resolve R9: Testing needs 50 examples
  Propagates to:
    → R7: Metrics must support batch evaluation
    → R8: Test data collection strategy needed
```

See [CONSTRAINT_RULES.md](references/CONSTRAINT_RULES.md) for complete propagation rules.

## Success Indicators

### Weekly Progress

- 2-4 holes resolved
- All tests passing
- Constraints satisfied
- Measurable improvements

### Red Flags (Stop & Reassess)

- ❌ Characterization tests fail
- ❌ Hole can't be resolved within constraints
- ❌ Constraints contradict each other
- ❌ No progress for 3+ days
- ❌ Main branch accidentally modified

## Validation Gates

| Gate | Criteria | Check |
|------|----------|-------|
| Gate 1: Discovery Complete | All holes cataloged, dependencies mapped | `python scripts/check_discovery.py` |
| Gate 2: Foundation Holes | Core interfaces resolved, tests pass | `python scripts/check_foundation.py` |
| Gate 3: Implementation | All refactor holes resolved, metrics improved | `python scripts/check_implementation.py` |
| Gate 4: Production Ready | Migration tested, rollback verified | `python scripts/check_production.py` |

## Claude-Assisted Workflow

This skill is designed for effective Claude/LLM collaboration. Here's how to divide work:

### Phase 0: Discovery

**Claude's Role**:
- Run `discover_holes.py` to analyze codebase
- Suggest holes based on code analysis
- Generate initial REFACTOR_IR.md structure
- Write characterization tests to capture current behavior
- Set up test infrastructure

**Your Role**:
- Confirm holes are well-scoped
- Prioritize which holes to tackle first
- Review and approve REFACTOR_IR.md
- Define critical constraints

### Phase 1-N: Hole Resolution

**Claude's Role**:
- Write resolution tests (TDD) BEFORE implementation
- Implement hole resolution to make tests pass
- Run validation scripts: `validate_resolution.py`, `check_foundation.py`
- Update REFACTOR_IR.md with resolution details
- Propagate constraints: `python scripts/propagate.py H{N}`
- Generate commit messages documenting changes

**Your Role**:
- Make architecture decisions (which pattern, which approach)
- Assess risk and determine constraint priorities
- Review code changes for correctness
- Approve merge to main when complete

### Phase Final: Reporting

**Claude's Role**:
- Generate comprehensive REFACTOR_REPORT.md
- Document all metrics deltas
- List all validation evidence
- Create migration guides
- Prepare PR description

**Your Role**:
- Final review of report accuracy
- Approve for production deployment
- Conduct post-refactor retrospective

### Effective Prompting Patterns

**Starting a session**:
```
"I need to refactor [description]. Use typed-holes-refactor skill.
Start with discovery phase."
```

**Resolving a hole**:
```
"Resolve H3 (target_architecture). Write tests first, then implement.
Use [specific pattern/approach]."
```

**Checking progress**:
```
"Run check_completeness.py and show me the dashboard.
What's ready to work on next?"
```

**Generating visualizations**:
```
"Generate dependency graph showing bottlenecks and critical path.
Use visualize_graph.py with --analyze."
```

### Claude's Limitations

**Claude CANNOT**:
- Make subjective architecture decisions (you must decide)
- Determine business-critical constraints (you must specify)
- Run tests that require external services (mock or you run them)
- Merge to main (you must approve and merge)

**Claude CAN**:
- Analyze code and suggest holes
- Write comprehensive test suites
- Implement resolutions within your constraints
- Generate reports and documentation
- Track progress across sessions (via beads + REFACTOR_IR.md)

### Multi-Session Continuity

**At session start**:
```
"Continue typed-holes refactoring. Import beads state and
show current status from REFACTOR_IR.md."
```

**Claude will**:
- Read REFACTOR_IR.md to understand current state
- Check which holes are resolved
- Identify next ready holes
- Resume where previous session left off

**You should**:
- Keep REFACTOR_IR.md and .beads/ committed to git
- Export beads state at session end: `bd export -o .beads/issues.jsonl`
- Use /context before starting to ensure Claude has full context

## Beads Integration

**Why beads + typed holes?**
- Beads tracks issues across sessions (prevents lost work)
- Holes track refactoring-specific state (dependencies, constraints)
- Together: Complete continuity for long-running refactors

### Setup

```bash
# Install beads (once)
go install github.com/steveyegge/beads/cmd/bd@latest

# After running discover_holes.py
python scripts/holes_to_beads.py

# Check what's ready
bd ready --json
```

### Workflow Integration

**During hole resolution**:
```bash
# Start work on a hole
bd update bd-5 --status in_progress --json

# Implement resolution
# ... write tests, implement code ...

# Validate resolution
python scripts/validate_resolution.py H3

# Close bead
bd close bd-5 --reason "Resolved H3: target_architecture" --json

# Export state
bd export -o .beads/issues.jsonl
git add .beads/issues.jsonl REFACTOR_IR.md
git commit -m "Resolve H3: Define target architecture"
```

**Syncing holes ↔ beads**:
```bash
# After updating REFACTOR_IR.md manually
python scripts/holes_to_beads.py  # Sync changes to beads

# After resolving holes
python scripts/holes_to_beads.py  # Update bead statuses
```

**Cross-session continuity**:
```bash
# Session start
bd import -i .beads/issues.jsonl
bd ready --json  # Shows ready holes
python scripts/check_completeness.py  # Shows overall progress

# Session end
bd export -o .beads/issues.jsonl
git add .beads/issues.jsonl
git commit -m "Session checkpoint: 3 holes resolved"
```

**Bead advantages**:
- Tracks work across days/weeks
- Shows dependency graph: `bd deps bd-5`
- Prevents context loss
- Integrates with overall project management

## Scripts Reference

All scripts are in `scripts/`:

- `discover_holes.py` - Analyze codebase and generate REFACTOR_IR.md
- `next_hole.py` - Show next resolvable holes based on dependencies
- `validate_resolution.py` - Check if hole resolution satisfies constraints
- `propagate.py` - Update dependent holes after resolution
- `generate_report.py` - Create comprehensive delta report
- `check_discovery.py` - Validate Phase 0 completeness (Gate 1)
- `check_foundation.py` - Validate Phase 1 completeness (Gate 2)
- `check_implementation.py` - Validate Phase 2 completeness (Gate 3)
- `check_production.py` - Validate Phase 3 readiness (Gate 4)
- `check_completeness.py` - Overall progress dashboard
- `visualize_graph.py` - Generate hole dependency visualization
- `holes_to_beads.py` - Sync holes with beads issues

Run any script with `--help` for detailed usage.

## Meta-Consistency

This skill uses its own principles:

| Typed Holes Principle | Application to Refactoring |
|-----------------------|----------------------------|
| Typed Holes | Architectural unknowns cataloged with types |
| Constraint Propagation | Design constraints flow through dependency graph |
| Iterative Refinement | Hole-by-hole resolution cycles |
| Test-Driven Validation | Tests define correctness |
| Formal Completeness | Gates verify design completeness |

**We use the system to refactor the system.**

## Advanced Topics

For complex scenarios, see:

- [HOLE_TYPES.md](references/HOLE_TYPES.md) - Detailed hole taxonomy
- [CONSTRAINT_RULES.md](references/CONSTRAINT_RULES.md) - Complete propagation rules
- [VALIDATION_PATTERNS.md](references/VALIDATION_PATTERNS.md) - Test patterns for different hole types
- [EXAMPLES.md](references/EXAMPLES.md) - Complete worked examples

## Quick Start Example

```bash
# 1. Setup
git checkout -b refactor/typed-holes-v1
python scripts/discover_holes.py

# 2. Write baseline tests
# Create tests/characterization/test_*.py

# 3. Resolve first hole
python scripts/next_hole.py  # Shows H1 is ready
# Write tests/refactor/test_h1_*.py (fails initially)
# Refactor code until tests pass
python scripts/validate_resolution.py H1
python scripts/propagate.py H1
git commit -m "Resolve H1: ..."

# 4. Repeat for each hole
# ...

# 5. Generate report
python scripts/generate_report.py > REFACTOR_REPORT.md
```

## Troubleshooting

### Characterization tests fail

**Symptom**: Tests that captured baseline behavior now fail

**Resolution**:
1. Revert changes: `git diff` to see what changed
2. Investigate: What behavior changed and why?
3. Decision tree:
   - **Intentional change**: Update baselines with documentation
     ```python
     # Update baseline with reason
     save_baseline("v2_api", new_behavior,
                   reason="Switched to async implementation")
     ```
   - **Unintentional regression**: Fix the code, tests must pass

**Prevention**: Run characterization tests before AND after each hole resolution.

### Hole can't be resolved

**Symptom**: Stuck on a hole for >3 days, unclear how to proceed

**Resolution**:
1. **Check dependencies**: Are they actually resolved?
   ```bash
   python scripts/visualize_graph.py --analyze
   # Look for unresolved dependencies
   ```

2. **Review constraints**: Are they contradictory?
   - Example: C1 "preserve all behavior" + C5 "change API contract" → Contradictory
   - **Fix**: Renegotiate constraints with stakeholders

3. **Split the hole**: If hole is too large
   ```bash
   # Original: R4_consolidate_all (Epic, 10+ days)
   # Split into:
   R4a_consolidate_parsers (Medium, 2 days)
   R4b_consolidate_validators (Small, 1 day)
   R4c_consolidate_handlers (Medium, 2 days)
   ```

4. **Check for circular dependencies**:
   ```bash
   python scripts/visualize_graph.py
   # Look for cycles: R4 → R5 → R6 → R4
   ```
   - **Fix**: Break cycle by introducing intermediate hole or redefining dependencies

**Escalation**: If still stuck after 5 days, consider alternative refactoring approach.

### Contradictory Constraints

**Symptom**: Cannot satisfy all constraints simultaneously

**Example**:
- C1: "Preserve exact current behavior" (backward compatibility)
- C5: "Reduce response time by 50%" (performance improvement)
- Current behavior includes slow, synchronous operations

**Resolution Framework**:

1. **Identify the conflict**:
   ```markdown
   C1 requires: Keep synchronous operations
   C5 requires: Switch to async operations
   → Contradiction: Can't be both sync and async
   ```

2. **Negotiate priorities**:
   | Option | C1 | C5 | Tradeoff |
   |--------|----|----|----------|
   | A: Keep sync | ✓ | ✗ | No performance gain |
   | B: Switch to async | ✗ | ✓ | Breaking change |
   | C: Add async, deprecate sync | ⚠️ | ✓ | Migration burden |

3. **Choose resolution strategy**:
   - **Relax constraint**: Change C1 to "Preserve behavior where possible"
   - **Add migration period**: C implemented over 2 releases
   - **Split into phases**: Phase 1 (C1), Phase 2 (C5)

4. **Document decision**:
   ```markdown
   ## Constraint Resolution: C1 vs C5

   **Decision**: Relax C1 to allow async migration
   **Rationale**: Performance critical for user experience
   **Migration**: 3-month deprecation period for sync API
   **Approved by**: [Stakeholder], [Date]
   ```

### Circular Dependencies

**Symptom**: `visualize_graph.py` shows cycles

**Example**:
```
R4 (consolidate parsers) → depends on R6 (define interface)
R6 (define interface) → depends on R4 (needs parser examples)
```

**Resolution strategies**:

1. **Introduce intermediate hole**:
   ```
   H0_parser_analysis: Analyze existing parsers (no dependencies)
   R6_interface: Define interface using H0 analysis
   R4_consolidate: Implement using R6 interface
   ```

2. **Redefine dependencies**:
   - Maybe R4 doesn't actually need R6
   - Or R6 only needs partial R4 (split R4)

3. **Accept iterative refinement**:
   ```
   R6_interface_v1: Initial interface (simple)
   R4_consolidate: Implement with v1 interface
   R6_interface_v2: Refine based on R4 learnings
   ```

**Prevention**: Define architecture holes before implementation holes.

### No Progress for 3+ Days

**Symptom**: Feeling stuck, no commits, uncertain how to proceed

**Resolution checklist**:

- [ ] **Review REFACTOR_IR.md**: Are holes well-defined (SMART criteria)?
  - If not: Rewrite holes to be more specific

- [ ] **Check hole size**: Is current hole >7 days estimate?
  - If yes: Split into smaller holes

- [ ] **Run dashboard**: `python scripts/check_completeness.py`
  - Are you working on a blocked hole?
  - Switch to a ready hole instead

- [ ] **Visualize dependencies**: `python scripts/visualize_graph.py --analyze`
  - Identify bottlenecks
  - Look for parallel work opportunities

- [ ] **Review constraints**: Are they achievable?
  - Renegotiate if necessary

- [ ] **Seek external review**:
  - Share REFACTOR_IR.md with colleague
  - Get feedback on approach

- [ ] **Consider alternative**: Maybe this refactor isn't feasible
  - Document why
  - Propose different approach

**Reset protocol**: If still stuck, revert to last working state and try different approach.

### Estimation Failures

**Symptom**: Hole taking 3x longer than estimated

**Analysis**:
1. **Why did estimate fail?**
   - Underestimated complexity
   - Unforeseen dependencies
   - Unclear requirements
   - Technical issues (tool problems, infrastructure)

2. **Immediate actions**:
   - Update REFACTOR_IR.md with revised estimate
   - If >7 days, split the hole
   - Update beads: `bd update bd-5 --note "Revised estimate: 5 days (was 2)"`

3. **Future improvements**:
   - Use actual times to calibrate future estimates
   - Add buffer for discovery (20% overhead)
   - Note uncertainty in IR: "Estimate: 2-4 days (high uncertainty)"

**Learning**: Track actual vs estimated time in REFACTOR_REPORT.md for future reference.

---

**Begin with Phase 0: Discovery. Always work in a branch. Test first, refactor second.**
