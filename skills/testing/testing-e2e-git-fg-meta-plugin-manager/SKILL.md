---
name: testing-e2e
description: "Execute programmatic E2E tests for all .claude/ components. Use when validating skills, commands, agents, hooks, or MCP servers. Not for unit tests or CI/CD pipelines."
---

<mission_control>
<objective>Execute programmatic E2E tests for all .claude/ components using claude -p in isolated sandbox environments</objective>
<success_criteria>All tests complete with pass/fail report, logs captured, hallucination scenarios detected</success_criteria>
</mission_control>

## Quick Start

**If you need to run all E2E tests:** Use the inline run pattern below.

**If you need to test a specific component:** Use the single-test pattern.

**If you need to understand test patterns:** MUST READ ## PATTERN: Test Definition before creating any tests.

**If you need to debug a test:** Use the verbose inline pattern.

### Inline E2E Run Pattern

```bash
#!/bin/bash
# Inline E2E Runner - No external scripts needed

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SANDBOX_DIR="$PROJECT_ROOT/.sandbox"
LOGS_DIR="$(dirname "${BASH_SOURCE[0]}")/logs"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

# Setup sandbox
rm -rf "$SANDBOX_DIR"
mkdir -p "$SANDBOX_DIR/.claude/skills" "$SANDBOX_DIR/.claude/commands"
mkdir -p "$SANDBOX_DIR/.claude/agents" "$SANDBOX_DIR/Custom_MCP"
mkdir -p "$SANDBOX_DIR/tests" "$LOGS_DIR"

cp -r "$PROJECT_ROOT/.claude/skills" "$SANDBOX_DIR/.claude/"
cp -r "$PROJECT_ROOT/.claude/commands" "$SANDBOX_DIR/.claude/"
cp -r "$PROJECT_ROOT/.claude/agents" "$SANDBOX_DIR/.claude/"
cp "$PROJECT_ROOT/.claude/settings.json" "$SANDBOX_DIR/.claude/" 2>/dev/null || true
cp -r "$PROJECT_ROOT/Custom_MCP" "$SANDBOX_DIR/" 2>/dev/null || true

# Create test scenario
TEST_DIR="$SANDBOX_DIR/tests/skill-development"
mkdir -p "$TEST_DIR"
cat > "$TEST_DIR/test-skill.md" << 'EOF'
# Test: Skill-Development Creates Valid Skill

## Use Cases
| Scenario | Trigger | Expected |
|----------|---------|----------|
| Create minimal skill | Use skill-development | Valid SKILL.md created |

## Validation Conditions
| Condition | Check | Pass |
|-----------|-------|------|
| File created | `[ -f "$OUTPUT_FILE" ]` | Exit 0 |
EOF

# Execute claude -p with CWD in sandbox/.claude/
PROMPT_FILE="$TEST_DIR/test-skill.md"
LOG_FILE="$LOGS_DIR/e2e-$(date +%s).log"

cd "$SANDBOX_DIR/.claude"
"$CLAUDE_BIN" -p "@$PROMPT_FILE" \
  --output-format stream-json \
  --verbose \
  --dangerously-skip-permissions \
  --allowedTools "*" \
  2>&1 | tee "$LOG_FILE"

echo "Logs: $LOG_FILE"
```

### Single-Test Pattern

```bash
# Run one specific test
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
SANDBOX_DIR=".sandbox"
CLAUDE_BIN="claude"

cd "$SANDBOX_DIR/.claude"
"$CLAUDE_BIN" -p "@tests/skill-development/test-skill.md" \
  --output-format stream-json \
  --verbose \
  --dangerously-skip-permissions \
  --allowedTools "*" \
  2>&1 | tee "logs/test.log"
```

### Verbose Debug Pattern

```bash
# Debug with full output
SANDBOX_DIR=".sandbox"
PROMPT="tests/skill-development/test-skill.md"
LOG="logs/debug-$(date +%s).log"

cd "$SANDBOX_DIR/.claude"
claude -p "@$PROMPT" \
  --output-format stream-json \
  --verbose \
  --dangerously-skip-permissions \
  --allowedTools "*" \
  2>&1 | tee "$LOG"

# Check for hallucinations
grep -i "read.*skill\|look at.*skill" "$LOG" && echo "HALLUCINATION: Reading instead of invoking"


## Navigation

| If you need...                       | Read...                                 |
| :----------------------------------- | :-------------------------------------- |
| Test definition format               | ## PATTERN: Test Definition             |
| Claude -p invocation                 | ## PATTERN: Claude Invocation           |
| Sandbox management                   | ## PATTERN: Sandbox Management          |
| Hallucination detection              | ## PATTERN: Hallucination Detection     |
| Validation conditions                | ## PATTERN: Validation Conditions       |
| Component test scenarios             | ## PATTERN: Component Tests             |
| Anti-patterns to avoid               | ## ANTI-PATTERN: Common Mistakes        |
| When to use references               | ## QUALITY PATTERN: When to Use References |

## PATTERN: Test Definition

Every test case MUST be defined in a `test-skill.md` file following this structure:

```markdown
# Test: [Component Name] - [Test Purpose]

## Use Cases
| Scenario | Trigger | Expected Behavior |
|----------|---------|-------------------|
| [Name]   | [What invokes] | [What should happen] |

## Validation Conditions
| Condition | Check Command | Pass Criteria |
|-----------|---------------|---------------|
| [Desc]    | `[command]`   | [Expected result] |

## Risks
| Risk | Mitigation |
|------|------------|
| [What could fail] | [How to prevent] |

## Test Prompts
```yaml
prompt: |
  [Claude instruction]
allowedTools: "Tool1,Tool2"
expectedExitCode: 0
```

## Hallucination Scenarios
| Scenario | Detection |
|----------|-----------|
| [What to test] | [How to verify] |
```

### Required Elements

| Element | Purpose | Required? |
|---------|---------|-----------|
| `Use Cases` | What scenarios are tested | Yes |
| `Validation Conditions` | How to verify pass/fail | Yes |
| `Risks` | What could go wrong | Yes |
| `Test Prompts` | Claude -p input | Yes |
| `Hallucination Scenarios` | Anti-hallucination tests | Yes |

---

## PATTERN: Claude Invocation

### Inline Claude -p Execution

```bash
#!/bin/bash
# Claude -p invocation without external scripts

CLAUDE_BIN="${CLAUDE_BIN:-claude}"
SANDBOX_DIR="${1:-.sandbox}"
PROMPT_FILE="$2"
LOG_FILE="${3:-logs/claude-$(date +%s).log}"

# Validate arguments
[ -d "$SANDBOX_DIR/.claude" ] || { echo "Error: Sandbox missing .claude/"; exit 1; }
[ -f "$PROMPT_FILE" ] || { echo "Error: Prompt file not found"; exit 1; }

# Execute with CWD in sandbox/.claude/
cd "$SANDBOX_DIR/.claude"

"$CLAUDE_BIN" -p "@$PROMPT_FILE" \
  --output-format stream-json \
  --verbose \
  --dangerously-skip-permissions \
  --allowedTools "*" \
  2>&1 | tee "$LOG_FILE"
```

### Required Flags

| Flag | Purpose | Why |
|------|---------|-----|
| `--output-format stream-json` | JSON-line output | Parseable, streamable results |
| `--verbose` | Detailed logging | Debug test failures |
| `--dangerously-skip-permissions` | No prompts | Automated testing |
| `--allowedTools "*"` | All tools allowed | Skills need full access |

### Error Handling

```bash
# Capture exit code
set +e
claude -p "@$PROMPT" --output-format stream-json ... > "$LOG" 2>&1
EXIT_CODE=$?
set -e

# Check for errors
if [ $EXIT_CODE -ne 0 ]; then
  echo "Test failed with exit code: $EXIT_CODE"
  tail -50 "$LOG"
fi
```

---

## PATTERN: Sandbox Management

### Sandbox Structure (Mirrors Project)

```
.sandbox/                      # Regenerated each run
├── .claude/                   # MUST be CWD for claude -p
│   ├── skills/               # Copy of skills to test
│   ├── commands/             # Copy of commands to test
│   ├── agents/               # Copy of agents to test
│   └── settings.json         # Copy of hooks config
├── Custom_MCP/               # Copy of MCP servers to test
├── tests/                    # Pre-created test scenarios
│   ├── skill-review/
│   │   ├── test-skill.md
│   │   └── input.md
│   └── ...
├── logs/                     # Symbolic link to permanent logs
└── work/                     # Working directory
```

### Inline Sandbox Setup

```bash
#!/bin/bash
# Setup sandbox without external scripts

SANDBOX_DIR=".sandbox"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SKILL_DIR="$(dirname "${BASH_SOURCE[0]}")"
LOGS_DIR="$SKILL_DIR/logs"

# Clean and recreate
rm -rf "$SANDBOX_DIR"
mkdir -p "$SANDBOX_DIR/.claude/skills"
mkdir -p "$SANDBOX_DIR/.claude/commands"
mkdir -p "$SANDBOX_DIR/.claude/agents"
mkdir -p "$SANDBOX_DIR/Custom_MCP"
mkdir -p "$SANDBOX_DIR/tests"
mkdir -p "$LOGS_DIR"

# Copy project structure
cp -r "$PROJECT_ROOT/.claude/skills" "$SANDBOX_DIR/.claude/"
cp -r "$PROJECT_ROOT/.claude/commands" "$SANDBOX_DIR/.claude/"
cp -r "$PROJECT_ROOT/.claude/agents" "$SANDBOX_DIR/.claude/"
cp "$PROJECT_ROOT/.claude/settings.json" "$SANDBOX_DIR/.claude/" 2>/dev/null || true
cp -r "$PROJECT_ROOT/Custom_MCP" "$SANDBOX_DIR/" 2>/dev/null || true

echo "Sandbox created at: $SANDBOX_DIR"
```

---

## PATTERN: Hallucination Detection

### Hallucination Scenarios to Test

| Scenario | Detection Method | Pass Criteria |
|----------|------------------|---------------|
| Read instead of invoke | Check prompt for "read" vs "invoke" | Skill triggers correctly |
| Skip verification | Count validation checks run | All checks executed |
| Wrong skill triggered | Compare invoked skill to description | Description matches behavior |
| Skipped critical step | Trace tool calls | All required steps present |
| Generic output | Check for vague/non-specific responses | Contains specific details |

### Inline Hallucination Detection

```bash
#!/bin/bash
# Detect hallucinations without external scripts

LOG_FILE="${1:-logs/latest.log}"
PROMPT_FILE="${2:-}"

HALLUCINATION_FOUND=0

# Check 1: Read instead of invoke
if [ -n "$PROMPT_FILE" ] && [ -f "$PROMPT_FILE" ]; then
  if grep -qi "read.*skill\|look at.*skill\|check.*skill\|examine.*skill" "$PROMPT_FILE" 2>/dev/null; then
    if ! grep -qi "invoke.*skill\|use.*skill\|call.*skill" "$PROMPT_FILE" 2>/dev/null; then
      echo "HALLUCINATION: Prompt suggests reading instead of invoking skill"
      HALLUCINATION_FOUND=1
    fi
  fi
fi

# Check 2: Insufficient verification steps
VERIFICATION_COUNT=$(grep -ci "verify\|validate\|check\|confirm\|ensure\|assert" "$LOG_FILE" 2>/dev/null || echo "0")
if [ "$VERIFICATION_COUNT" -lt 2 ]; then
  echo "HALLUCINATION: Insufficient verification steps ($VERIFICATION_COUNT found, need >= 2)"
  HALLUCINATION_FOUND=1
fi

# Check 3: Generic/vague output
if grep -qi "I understand\|I see\|looks good\|seems right\|that should work\|done\." "$LOG_FILE" 2>/dev/null; then
  LINE_COUNT=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")
  if [ "$LINE_COUNT" -lt 10 ]; then
    echo "HALLUCINATION: Generic output detected (too brief)"
    HALLUCINATION_FOUND=1
  fi
fi

# Check 4: Too many errors
ERROR_COUNT=$(grep -ci "error\|failed\|exception\|cannot\|unable" "$LOG_FILE" 2>/dev/null || echo "0")
if [ "$ERROR_COUNT" -gt 5 ]; then
  echo "HALLUCINATION: Too many errors in output ($ERROR_COUNT)"
  HALLUCINATION_FOUND=1
fi

if [ $HALLUCINATION_FOUND -eq 1 ]; then
  echo "RESULT: Hallucination detected"
  exit 1
else
  echo "RESULT: No hallucination detected"
  exit 0
fi
```

### Quick Hallucination Check

```bash
# One-liner: check for common hallucinations
grep -qi "read.*skill\|look at.*skill\|I understand\|looks good" logs/latest.log && echo "POTENTIAL HALLUCINATION"

# Check verification count
grep -ci "verify\|validate\|check" logs/latest.log
```

---

## PATTERN: Validation Conditions

### Validation Check Types

| Type | Example | Pass Criteria |
|------|---------|---------------|
| File existence | `[ -f "file.md" ]` | Exit code 0 |
| YAML validity | `yaml-frontmatter-valid file.md` | No errors |
| Pattern match | `grep -q '<mission_control>'` | Pattern found |
| JSON validity | `jq . file.json` | Valid JSON |
| Exit code | `claude -p ...; echo $?` | Expected code |

### Validation Runner

```bash
#!/bin/bash
# scripts/validate.sh

TEST_FILE="$1"
SANDBOX_DIR="$2"

# Source test file to get validation conditions
source <(grep -A 100 "## Validation Conditions" "$TEST_FILE" | \
         grep -B 100 "## Risks" | head -n -1)

# Execute each validation
while IFS='|' read -r CONDITION CHECK PASS_CRITERIA; do
  if [ -z "$CONDITION" ] || [[ "$CONDITION" == Condition* ]]; then
    continue
  fi

  eval "$CHECK" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "PASS: $CONDITION"
  else
    echo "FAIL: $CONDITION (expected: $PASS_CRITERIA)"
  fi
done <<< "$(grep "|.*|.*|" "$TEST_FILE" | sed '1d')"
```

---

## PATTERN: Component Tests

### Skills Tests

| Test | Purpose | Hallucination Check |
|------|---------|---------------------|
| Invocation | Skill triggers on correct phrase | No wrong skill |
| Verification | All steps executed | No skipped checks |
| Portability | Zero external dependencies | No external refs |
| Description | Non-spoiling | Body not in desc |

### Commands Tests

| Test | Purpose | Hallucination Check |
|------|---------|---------------------|
| Execution | Command runs successfully | Exit code 0 |
| Description | Triggers correctly | Matches behavior |
| Output | Format correct | Expected structure |

### Agents Tests

| Test | Purpose | Hallucination Check |
|------|---------|---------------------|
| Autonomy | Doesn't spawn other agents | No Task() calls |
| Trigger | Spawns only on conditions | Correct trigger |
| Context | Uses provided context | No missing info |

### Hooks Tests

| Test | Purpose | Hallucination Check |
|------|---------|---------------------|
| Event | Fires on correct event | Event triggered |
| Action | Performs expected action | Action executed |

### MCP Tests

| Test | Purpose | Hallucination Check |
|------|---------|---------------------|
| Tool call | MCP tool returns structure | Valid JSON |
| Integration | Works with skill/agent | Tool used correctly |

---

## ANTI-PATTERN: Common Mistakes

### Anti-Pattern: Missing Sandbox CWD

```
❌ Wrong:
cd /project/root
claude -p "test skill"  # Loads real skills, not sandbox

✅ Correct:
cd .sandbox/.claude
claude -p "test skill"  # Loads sandbox skills
```

**Fix:** Always run claude -p with CWD in `.sandbox/.claude/`

### Anti-Pattern: No Pre-created Tests

```
❌ Wrong:
claude -p "review a skill"  # No test skill created

✅ Correct:
Create tests/skill-review/input.md with test content first
claude -p "Review tests/skill-review/input.md"
```

**Fix:** Always pre-create test scenarios before invocation

### Anti-Pattern: Ignoring Exit Codes

```
❌ Wrong:
claude -p "..." > log.txt  # Ignores failure
echo "Test complete"

✅ Correct:
set +e
claude -p "..." > log.txt 2>&1
EXIT=$?
set -e
if [ $EXIT -ne 0 ]; then
  echo "FAILED: Exit code $EXIT"
  exit 1
fi
```

**Fix:** Capture and check exit codes

### Anti-Pattern: Temporary Logs

```
❌ Wrong:
claude -p "..." > /tmp/test.log  # Lost after session

✅ Correct:
mkdir -p .claude/skills/testing-e2e/logs
claude -p "..." | tee .claude/skills/testing-e2e/logs/test-$(date +%s).log
```

**Fix:** Logs to permanent folder

---

## EDGE: Cross-Component Integration

### Integration Test Scenarios

| Scenario | Components | Validation |
|----------|------------|------------|
| Skill uses command | skill + command | Command invoked correctly |
| Agent invokes skill | agent + skill | Skill triggered |
| Hook blocks action | hook + tool | Action blocked |
| MCP with skill | skill + MCP | Tool returns valid |
| Multi-component | skill + agent + hook | All work together |

### Integration Test Example

```markdown
# Test: Skill-Authoring with self-learning

## Use Cases
| Scenario | Trigger | Expected |
|----------|---------|----------|
| Create and refine | skill-development + self-learning | Valid skill + refinements |

## Validation
| Check | Command | Pass |
|-------|---------|------|
| Skill created | `[ -f "output/SKILL.md" ]` | Exit 0 |
| Refinement output | `grep "Issue:" output.md` | Found |
```

---

## Recognition Questions

| Question | Answer Should Be... |
| :------- | :------------------ |
| Is CWD in `.sandbox/.claude/`? | Yes, for all claude -p calls |
| Are test scenarios pre-created? | Yes, before each test |
| Are logs permanent? | Yes, in logs folder |
| Is hallucination tested? | Yes, all scenarios covered |
| Are all components tested? | Skills, commands, agents, hooks, MCP |

---

## Validation Checklist

Before claiming test execution complete:

- [ ] Sandbox created with mirrored structure
- [ ] CWD verified in `.sandbox/.claude/` before each run
- [ ] Test scenarios pre-created (no on-the-fly creation)
- [ ] Claude -p invoked with correct flags (stream-json, verbose, skip-permissions)
- [ ] Logs captured to permanent folder
- [ ] Pass/fail reported for each test
- [ ] Hallucination scenarios detected and reported
- [ ] Cross-component integration tested
- [ ] Exit codes captured and checked

---

## QUALITY PATTERN: When to Use References

MUST READ `references/patterns_test-cases.md` when:
- You need 20+ test case patterns for inspiration
- You need templates for hallucination detection
- You need validation condition templates (file, YAML, JSON, exit code)
- You need component-specific test scenarios (skills, commands, agents, hooks, MCP)

Keep in SKILL.md (don't move to references):
- Core workflow and quick start
- Sandbox invariant (CWD requirement)
- Error handling patterns
- Recognition questions

**Why references/ exists:** `patterns_test-cases.md` has 509 lines with 20+ examples—putting this in SKILL.md would create a skill that no one reads. References are for "ultra-situational" lookup, not core workflow.

---

<critical_constraint>
**E2E Testing Invariant:**

1. Sandbox MUST mirror project structure (`.sandbox/.claude/` and `.sandbox/Custom_MCP/`)
2. CWD for claude -p MUST be inside `.sandbox/.claude/`
3. Test scenarios MUST be pre-created before invocation (no late creation)
4. Logs MUST go to permanent folder (not /tmp or /dev/null)
5. All tests MUST include hallucination detection scenarios
6. Exit codes MUST be captured and checked (never ignore failures)

Claude -p loads skills/commands from relative paths—wrong CWD = wrong results.
</critical_constraint>

---

## Common Mistakes to Avoid

### Mistake 1: Wrong CWD for Claude -p

❌ **Wrong:**
```bash
cd /tmp
claude -p "test prompt"
```

✅ **Correct:**
```bash
cd .sandbox/.claude/
claude -p "test prompt"
```

### Mistake 2: Creating Test Scenarios On-The-Fly

❌ **Wrong:**
```bash
# Test creates file mid-execution
claude -p "Create a new skill"
```

✅ **Correct:**
```bash
# Pre-create scenario first
# Scenario already exists at .sandbox/.claude/skills/my-test-skill/
claude -p "Test the skill"
```

### Mistake 3: Skipping Hallucination Detection

❌ **Wrong:**
```bash
# Only checks if output exists
if [ -f output.md ]; then echo "PASS"; fi
```

✅ **Correct:**
```bash
# Check for hallucinations (false claims, wrong file paths)
# Inline detection - no external script needed
grep -qi "read.*skill\|look at.*skill\|I understand" output.md && echo "HALLUCINATION"
```

### Mistake 4: Ignoring Exit Codes

❌ **Wrong:**
```bash
claude -p "test" > output.md
# Ignores exit code
```

✅ **Correct:**
```bash
claude -p "test" > output.md
if [ $? -ne 0 ]; then echo "FAIL: claude -p failed"; exit 1; fi
```

### Mistake 5: Temporary Logs

❌ **Wrong:**
```bash
claude -p "test" > output.md
# Log lost after session
```

✅ **Correct:**
```bash
claude -p "test" 2>&1 | tee logs/run-$(date +%Y%m%d-%H%M%S).log
```

---

## Best Practices Summary

✅ **DO:**
- Create sandbox with mirrored `.claude/` structure
- Run claude -p from inside `.sandbox/.claude/`
- Pre-create all test scenarios before invocation
- Capture logs to permanent folder
- Test for hallucinations (false claims, wrong assumptions)
- Check exit codes for all commands
- Test all component types (skills, commands, agents, hooks, MCP)

❌ **DON'T:**
- Run from wrong directory (breaks relative paths)
- Create test scenarios mid-test (changes variables)
- Skip hallucination detection (misses false outputs)
- Ignore exit codes (misses failures)
- Use /tmp or /dev/null for logs (lose evidence)
- Test only one component type (misses integration issues)

---
