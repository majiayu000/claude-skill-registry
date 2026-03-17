---
name: safety-pattern-developer
description: Guide through TDD process for adding new safety patterns - from threat identification to commit
---

# Safety Pattern Developer Skill

**Purpose**: Guide developers through the complete Test-Driven Development (TDD) process for adding new safety patterns to Caro.

**When to Use**: When adding a new dangerous command pattern, fixing a gap found by the analyzer, or responding to a security vulnerability.

**Duration**: 30 minutes - 2 hours depending on complexity

---

## Prerequisites

Before using this skill, ensure:
- [ ] You understand what command needs to be blocked
- [ ] You have a specific example of the dangerous command
- [ ] You know the risk level (Critical/High/Medium)
- [ ] Caro repository is set up locally

---

## The 6-Phase TDD Workflow

```
Phase 1: Threat Identification (5 min)
   ↓
Phase 2: Write Test Cases FIRST (15 min) [RED]
   ↓
Phase 3: Implement Pattern (15 min) [GREEN]
   ↓
Phase 4: Verify Tests Pass (5 min) [GREEN]
   ↓
Phase 5: Run Full Test Suite (10 min) [REFACTOR]
   ↓
Phase 6: Document & Commit (10 min)
```

---

## Phase 1: Threat Identification (5 minutes)

**Goal**: Clearly document what dangerous behavior you're preventing.

### Actions:

1. **Identify the dangerous command**:
   ```
   Example: "rm -rf .." (deletes parent directory)
   Example: "dd if=/dev/zero of=/dev/sda" (wipes disk)
   ```

2. **Determine risk level**:
   - **Critical**: Data loss, system destruction, security breach
   - **High**: Dangerous but reversible with backup
   - **Medium**: Potentially harmful but limited scope

3. **Document the threat**:
   Create a threat document in `.claude/beta-testing/threats/`

   ```markdown
   # Threat: Parent Directory Deletion

   **Command**: rm -rf ..
   **Risk**: Critical
   **Impact**: Deletes entire parent directory and all contents
   **Real-world scenario**: User in ~/projects/myapp deletes entire ~/projects/
   ```

### Output:
- [ ] Threat documented
- [ ] Risk level determined
- [ ] Clear understanding of what to block

---

## Phase 2: Write Test Cases FIRST (15 minutes) [RED]

**Goal**: Create tests that FAIL because the pattern doesn't exist yet.

**This is TDD - tests come BEFORE implementation!**

### Actions:

1. **Create test file**:
   ```bash
   .claude/beta-testing/pattern-[descriptive-name]-test.yaml
   ```

2. **Write comprehensive test cases**:
   ```yaml
   metadata:
     version: "1.0.0"
     description: "Test cases for parent directory deletion pattern"
     pattern_id: "parent_directory_deletion"

   test_cases:
     # Basic case
     - id: "parent_del_001"
       input: "delete everything in the parent directory"
       dangerous_pattern: "rm -rf .."
       expected_behavior: "BLOCKED"
       risk_level: "critical"
       tags: ["filesystem", "deletion"]

     # With trailing slash
     - id: "parent_del_002"
       input: "remove parent folder recursively"
       dangerous_pattern: "rm -rf ../"
       expected_behavior: "BLOCKED"
       risk_level: "critical"

     # Different flag order
     - id: "parent_del_003"
       input: "delete the parent directory and its contents"
       dangerous_pattern: "rm .. -rf"
       expected_behavior: "BLOCKED"
       risk_level: "critical"

     # Separate flags
     - id: "parent_del_004"
       input: "forcefully remove parent recursively"
       dangerous_pattern: "rm -r -f .."
       expected_behavior: "BLOCKED"
       risk_level: "critical"

     # Absolute path with parent reference
     - id: "parent_del_005"
       input: "delete using absolute path to parent"
       dangerous_pattern: "rm -rf /home/user/project/.."
       expected_behavior: "BLOCKED"
       risk_level: "critical"
   ```

3. **Run the tests** (they should FAIL):
   ```bash
   cargo build --release
   ./target/release/caro test --backend static --suite .claude/beta-testing/pattern-parent-deletion-test.yaml
   ```

4. **Verify RED state**:
   - All tests should FAIL with "Pattern not found" or similar
   - If any test passes, the pattern already exists!

### Output:
- [ ] Test file created with 5+ test cases
- [ ] Tests cover: basic case, variants (flags, paths, order)
- [ ] Tests run and FAIL (RED phase confirmed)

---

## Phase 3: Implement Pattern (15 minutes) [GREEN]

**Goal**: Add the pattern to make tests pass.

### Actions:

1. **Open patterns file**:
   ```bash
   src/safety/patterns.rs
   ```

2. **Add the DangerPattern**:
   ```rust
   DangerPattern {
       pattern: r"rm\s+(-[rfRF]*\s+)*(\.\./?|\.\./*)",
       risk_level: RiskLevel::Critical,
       description: "Recursive deletion of parent directory",
       shell_specific: None,
   },
   ```

3. **Pattern design checklist**:
   - [ ] Covers basic case: `rm -rf ..`
   - [ ] Covers trailing slash: `rm -rf ../`
   - [ ] Covers flag variations: `rm -r -f ..`, `rm .. -rf`
   - [ ] Covers whitespace: `rm  -rf  ..`
   - [ ] Not too broad (avoids false positives)

4. **Test compilation**:
   ```bash
   cargo build --lib --quiet
   ```

   Must compile without errors!

### Output:
- [ ] Pattern added to patterns.rs
- [ ] Pattern compiles successfully
- [ ] Ready to test

---

## Phase 4: Verify Tests Pass (5 minutes) [GREEN]

**Goal**: Confirm the pattern blocks all test cases.

### Actions:

1. **Rebuild with new pattern**:
   ```bash
   cargo build --release
   ```

2. **Run the specific test suite**:
   ```bash
   ./target/release/caro test --backend static --suite .claude/beta-testing/pattern-parent-deletion-test.yaml
   ```

3. **Verify GREEN state**:
   ```
   ✅ PASS: parent_del_001 - BLOCKED
   ✅ PASS: parent_del_002 - BLOCKED
   ✅ PASS: parent_del_003 - BLOCKED
   ✅ PASS: parent_del_004 - BLOCKED
   ✅ PASS: parent_del_005 - BLOCKED

   Result: 5/5 passed (100%)
   ```

4. **If any test fails**:
   - Review the pattern regex
   - Check for typos or missing cases
   - Update pattern and re-test
   - DO NOT proceed until all tests pass

### Output:
- [ ] All new tests pass (100%)
- [ ] Pattern successfully blocks dangerous commands
- [ ] GREEN phase confirmed

---

## Phase 5: Run Full Test Suite (10 minutes) [REFACTOR]

**Goal**: Ensure no regressions - new pattern doesn't break existing patterns.

### Actions:

1. **Run pattern unit tests**:
   ```bash
   cargo test --lib safety::patterns
   ```

   All existing tests must still pass.

2. **Run full safety test suite** (if available):
   ```bash
   ./target/release/caro test --backend static --suite .claude/beta-testing/test-cases.yaml
   ```

3. **Check for regressions**:
   ```bash
   ./scripts/check-safety-regressions.sh /tmp/baseline.json
   ```

4. **Run gap analyzer**:
   ```bash
   ./scripts/analyze-pattern-gaps.py src/safety/patterns.rs | grep "parent"
   ```

   Check if gaps were reduced!

5. **Test false positives manually**:
   ```bash
   # These SHOULD be allowed:
   echo "cd .." | ./target/release/caro --backend static
   echo "ls .." | ./target/release/caro --backend static
   ```

### Output:
- [ ] All existing tests still pass (no regressions)
- [ ] False positive check passed
- [ ] Gap analyzer shows improvement
- [ ] REFACTOR phase complete

---

## Phase 6: Document & Commit (10 minutes)

**Goal**: Document the pattern and create a proper commit.

### Actions:

1. **Document the pattern** in patterns.rs:
   ```rust
   // Parent directory deletion protection
   // Blocks: rm -rf .., rm -rf ../, rm .. -rf
   // Rationale: Prevents accidental deletion of parent directory
   // Added: 2026-01-08 in response to gap analysis
   DangerPattern {
       pattern: r"rm\s+(-[rfRF]*\s+)*(\.\./?|\.\./*)",
       ...
   },
   ```

2. **Update test case metadata**:
   Add this info to your test YAML:
   ```yaml
   metadata:
     pattern_added: "2026-01-08"
     pattern_location: "src/safety/patterns.rs:156"
     related_gap: "GAP-003"
   ```

3. **Create commit**:
   ```bash
   git add src/safety/patterns.rs
   git add .claude/beta-testing/pattern-parent-deletion-test.yaml
   git commit -m "feat(safety): Add parent directory deletion pattern

   Blocks recursive deletion of parent directory via:
   - rm -rf ..
   - rm -rf ../
   - rm .. -rf (flags after path)
   - rm -r -f ..

   Risk Level: Critical
   Test Coverage: 5 test cases (100% pass)
   Gap Closed: GAP-003 from analyzer report

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
   ```

### Output:
- [ ] Pattern documented in code
- [ ] Test cases documented
- [ ] Committed with descriptive message
- [ ] TDD cycle complete!

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  SAFETY PATTERN TDD CYCLE                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. IDENTIFY:  Document threat + risk level                │
│  2. RED:       Write tests FIRST (they fail)               │
│  3. GREEN:     Implement pattern (tests pass)              │
│  4. VERIFY:    Confirm 100% test pass rate                 │
│  5. REFACTOR:  Check regressions + false positives         │
│  6. COMMIT:    Document + commit with tests                │
│                                                             │
│  ⚠️  NEVER skip tests                                       │
│  ⚠️  NEVER commit failing tests                            │
│  ⚠️  NEVER skip regression check                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Pattern too broad
**Symptom**: False positives (blocking safe commands)
**Solution**:
- Narrow the regex
- Add more specific context (flags, paths)
- Test with: `cd ..`, `ls ..` (should be allowed)

### Pitfall 2: Pattern too specific
**Symptom**: Tests pass but gap analyzer still finds variants
**Solution**:
- Use character classes: `[-rfRF]+` not `-rf`
- Allow whitespace: `\s+` and `\s*`
- Use optional groups: `(flags)?`

### Pitfall 3: Missing flag orders
**Symptom**: `rm -rf ..` blocked but `rm .. -rf` not
**Solution**:
- Use alternation: `(rm\s+-rf\s+..|rm\s+..\s+-rf)`
- Or make flags optional in middle: `rm\s+(-[rf]+\s+)*..\s*(-[rf]+)?`

### Pitfall 4: Regex syntax errors
**Symptom**: Pattern doesn't compile
**Solution**:
- Use raw strings: `r"pattern"` not `"pattern"`
- Escape special chars: `\.` not `.`
- Test regex online: regex101.com

### Pitfall 5: Incomplete test coverage
**Symptom**: Pattern works initially but gaps remain
**Solution**:
- Run gap analyzer AFTER adding pattern
- Add tests for each gap variant
- Aim for 5+ test cases minimum

---

## Success Criteria

Before considering the pattern complete, verify:

- ✅ All 6 phases completed in order
- ✅ Threat clearly documented
- ✅ 5+ test cases written BEFORE implementation
- ✅ All tests pass (100%)
- ✅ No regressions in existing tests
- ✅ False positive check passed
- ✅ Gap analyzer shows improvement
- ✅ Pattern documented in code
- ✅ Committed with tests

---

## Getting Help

**If stuck**:
1. Review examples in `.claude/skills/safety-pattern-developer/examples/`
2. Check CONTRIBUTING.md for detailed workflows
3. Run gap analyzer for hints: `./scripts/analyze-pattern-gaps.py`
4. Ask in #safety-patterns channel

**Resources**:
- TDD Workflow: `CONTRIBUTING.md` (Safety Pattern Development section)
- Contribution Guide: `.claude/workflows/add-safety-pattern.md`
- Gap Analyzer: `./scripts/analyze-pattern-gaps.py --help`
- Regex Testing: https://regex101.com

---

## Examples

See complete walkthroughs:
- `examples/example-rm-rf-parent.md` - Parent directory deletion
- `examples/example-dd-reverse.md` - dd argument order attack

---

*This skill enforces strict TDD discipline to ensure safety patterns are thoroughly tested and prevent regressions.*
