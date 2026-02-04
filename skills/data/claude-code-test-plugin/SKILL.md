---
name: claude-code-test-plugin
description: Run comprehensive plugin validation test suite
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---

# Test Plugin

Comprehensive test of all Bluera Base plugin functionality (hooks + slash commands).

## ⚠️ EXCLUDED COMMANDS

The following commands are **NOT tested** by this suite:

| Command | Reason |
|---------|--------|
| `/clean` | **DANGEROUS** - Modifies `~/.claude` which is Claude Code's own brain. Can wipe plugin caches, break running sessions, and corrupt config. DO NOT RUN AUTOMATICALLY. |

**DO NOT ADD `/clean` TO THIS TEST SUITE.** Test it manually, in isolation, with explicit user consent.

## Context

!`echo "=== Bluera Base Plugin Test ===" && echo "Hooks: $(ls "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/hooks/"*.sh 2>/dev/null | wc -l | tr -d ' ') files" && echo "Skills: $(ls -d "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/skills/"*/ 2>/dev/null | wc -l | tr -d ' ') directories" && echo "Commands: $(ls "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/commands/"*.md 2>/dev/null | wc -l | tr -d ' ') files"`

## Pre-Test Cleanup

Remove any leftover artifacts from previous test runs:

```bash
rm -rf .bluera/bluera-base/state/milhouse-loop.md
rm -rf /tmp/bluera-base-test
```

## Test Content Setup

Create a temporary test directory with various project types:

```bash
mkdir -p /tmp/bluera-base-test
cd /tmp/bluera-base-test
git init
echo '{"name": "test-project", "version": "1.0.0"}' > package.json
echo 'console.log("test");' > index.js
git add .
git commit -m "initial"
```

## Workflow

Execute each test in order. Mark each as PASS or FAIL.

### Part 1: Hook Registration

1. **Hook File Structure**: Verify hooks.json has expected structure

   ```bash
   PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
   cat "$PLUGIN_PATH/hooks/hooks.json" | jq -e '.hooks.PreToolUse and .hooks.PostToolUse and .hooks.Stop and .hooks.Notification'
   ```

   - Expected: Returns `true` (all hook types registered)
   - PASS if command succeeds with truthy output

2. **Hook Scripts Exist**: Verify all referenced hooks have scripts

   ```bash
   PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
   MISSING=0
   for script in $(grep -oE '[a-z-]+\.sh' "$PLUGIN_PATH/hooks/hooks.json" | sort -u); do
     if [[ ! -f "$PLUGIN_PATH/hooks/$script" ]]; then
       echo "MISSING: $script"
       MISSING=$((MISSING + 1))
     fi
   done
   TOTAL=$(grep -oE '[a-z-]+\.sh' "$PLUGIN_PATH/hooks/hooks.json" | sort -u | wc -l | tr -d ' ')
   echo "Checked $TOTAL referenced scripts, $MISSING missing"
   [[ $MISSING -eq 0 ]] && echo "All hook scripts present"
   ```

   - Expected: All scripts referenced in hooks.json exist
   - PASS if output shows "All hook scripts present"

### Part 2: PreToolUse Hook (block-manual-release.sh)

1. **Block npm version**: Test that manual npm version is blocked

   ```bash
   PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
   echo '{"tool_input": {"command": "npm version patch"}}' | bash "$PLUGIN_PATH/hooks/block-manual-release.sh" 2>&1
   echo "Exit code: $?"
   ```

   - Expected: Message about using /bluera-base:release, exit code 2
   - PASS if output contains "Use /bluera-base:release" and exits 2

2. **Block git tag**: Test that manual git tagging is blocked

   ```bash
   PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
   echo '{"tool_input": {"command": "git tag v1.0.0"}}' | bash "$PLUGIN_PATH/hooks/block-manual-release.sh" 2>&1
   echo "Exit code: $?"
   ```

   - Expected: Blocked with exit code 2
   - PASS if exits 2

3. **Allow skill-prefixed release**: Test that /bluera-base:release skill can run version commands

   ```bash
   PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
   echo '{"tool_input": {"command": "__SKILL__=release npm version patch"}}' | bash "$PLUGIN_PATH/hooks/block-manual-release.sh"
   echo "Exit code: $?"
   ```

   - Expected: Allowed (exit code 0)
   - PASS if exits 0
   - **Note:** When run inside Claude Code, this test may show BLOCKED because the live hook intercepts the outer bash command. The `__SKILL__=release` mechanism works correctly - this is a test isolation artifact. For manual verification, run outside Claude Code.

4. **Allow normal commands**: Test that non-release commands pass through

   ```bash
   PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
   echo '{"tool_input": {"command": "npm install express"}}' | bash "$PLUGIN_PATH/hooks/block-manual-release.sh"
   echo "Exit code: $?"
   ```

   - Expected: Allowed (exit code 0)
   - PASS if exits 0

### Part 3: PostToolUse Hook (post-edit-check.sh)

1. **Anti-pattern Detection**: Test detection of forbidden words

   ```bash
   cd /tmp/bluera-base-test
   echo 'const fallback = true;' >> index.js
   git add index.js
   echo '{"tool_name": "Edit", "tool_input": {"file_path": "index.js"}}' | \
     CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/hooks/post-edit-check.sh" 2>&1
   EXIT=$?
   git checkout index.js 2>/dev/null
   echo "Exit code: $EXIT"
   ```

   - Expected: Detects "fallback" anti-pattern, exit code 2
   - PASS if output mentions anti-pattern and exits 2

2. **Clean Code Passes**: Test that clean code passes validation

   ```bash
   cd /tmp/bluera-base-test
   echo 'const clean = true;' >> index.js
   git add index.js
   echo '{"tool_name": "Edit", "tool_input": {"file_path": "index.js"}}' | \
     CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/hooks/post-edit-check.sh" 2>&1
   EXIT=$?
   git checkout index.js 2>/dev/null
   echo "Exit code: $EXIT"
   ```

   - Expected: No output, exit code 0
   - PASS if exits 0

### Part 4: Stop Hook (milhouse-stop.sh)

1. **No State File**: Test that hook exits cleanly when no milhouse loop active

   ```bash
   cd /tmp/bluera-base-test
   rm -rf .bluera/bluera-base/state/milhouse-loop.md
   PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
   echo '{"transcript_path": "/tmp/test.jsonl"}' | bash "$PLUGIN_PATH/hooks/milhouse-stop.sh" 2>&1
   echo "Exit code: $?"
   ```

   - Expected: Silent exit 0 (no active loop)
   - PASS if exits 0 with no output

2. **Invalid Iteration**: Test handling of corrupted state file

    ```bash
    cd /tmp/bluera-base-test
    mkdir -p .bluera/bluera-base/state
    printf '%s\n' '---' 'iteration: invalid' 'max_iterations: 5' 'completion_promise: "done"' '---' '' 'test prompt' > .bluera/bluera-base/state/milhouse-loop.md
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    echo '{"transcript_path": "/tmp/test.jsonl"}' | bash "$PLUGIN_PATH/hooks/milhouse-stop.sh" 2>&1
    EXIT=$?
    echo "Exit code: $EXIT"
    ```

    - Expected: Warning about invalid iteration, removes file, exits 0
    - PASS if mentions "invalid" and exits 0

### Part 5: Milhouse Setup Hook

1. **Setup Creates State File**: Test milhouse-setup.sh creates proper state

    ```bash
    cd /tmp/bluera-base-test
    rm -rf .bluera/bluera-base/state/milhouse-loop.md
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "$PLUGIN_PATH/hooks/milhouse-setup.sh" --inline "Build the feature" --max-iterations 10 2>&1
    cat .bluera/bluera-base/state/milhouse-loop.md 2>/dev/null | head -10
    ```

    - Expected: State file created with iteration: 1, max_iterations: 10
    - PASS if file exists with correct fields

### Part 6: Slash Commands (Invocation Test)

1. **Commit Command Available**: Run `/bluera-base:commit` (will show clean status)
    - Expected: Shows git status and workflow instructions
    - PASS if command executes without error

2. **Cancel Milhouse Available**: Verify cancel command works when no loop active

    ```bash
    rm -rf /tmp/bluera-base-test/.bluera/bluera-base/state/milhouse-loop.md
    ```

    Then run `/bluera-base:cancel-milhouse`
    - Expected: Message about no active loop
    - PASS if command executes

### Part 7: Skills Verification

1. **All Skills Have SKILL.md**: Verify every skill directory contains SKILL.md

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    MISSING=0
    CHECKED=0
    for dir in "$PLUGIN_PATH/skills/"*/; do
      # Skip template-only directories (contain .template but no SKILL.md)
      if find "$dir" -maxdepth 1 -name "*.template" 2>/dev/null | grep -q . && [ ! -f "$dir/SKILL.md" ]; then
        continue
      fi
      CHECKED=$((CHECKED + 1))
      if [ ! -f "$dir/SKILL.md" ]; then
        echo "MISSING: $dir/SKILL.md"
        MISSING=$((MISSING + 1))
      fi
    done
    echo "Checked $CHECKED skill directories, $MISSING missing SKILL.md"
    [ $MISSING -eq 0 ] && echo "All skills valid"
    ```

    - Expected: All skill directories (except template-only) contain SKILL.md
    - PASS if output shows "All skills valid"

2. **Skills Are Readable**: Verify at least one skill file has content

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    # Find first skill with SKILL.md (skip template-only dirs)
    FIRST_SKILL=""
    for dir in "$PLUGIN_PATH/skills/"*/; do
      if [ -f "$dir/SKILL.md" ]; then
        FIRST_SKILL="$dir"
        break
      fi
    done
    [ -n "$FIRST_SKILL" ] && head -5 "$FIRST_SKILL/SKILL.md"
    ```

    - Expected: Shows skill header/title
    - PASS if file is readable with content

### Part 8: Library Unit Tests

1. **Signals Library Tests**: Run signals.sh unit tests

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    bash "$PLUGIN_PATH/hooks/lib/tests/test-signals.sh"
    ```

    - Expected: 6 tests pass
    - PASS if output contains "6 passed, 0 failed"

2. **State Library Tests**: Run state.sh unit tests

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    bash "$PLUGIN_PATH/hooks/lib/tests/test-state.sh"
    ```

    - Expected: 8 tests pass
    - PASS if output contains "8 passed, 0 failed"

3. **Gitignore Integration Tests**: Run gitignore tests

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    bash "$PLUGIN_PATH/hooks/lib/tests/test-gitignore-integration.sh"
    ```

    - Expected: 4 tests pass
    - PASS if output contains "4 passed, 0 failed"

### Part 9: Checklist Hook

1. **Checklist Hook - No File**: Test that hook exits cleanly when no checklist exists

    ```bash
    cd /tmp/bluera-base-test
    rm -rf .bluera/bluera-base/checklist.md
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "$PLUGIN_PATH/hooks/checklist-remind.sh" 2>&1
    echo "Exit code: $?"
    ```

    - Expected: Silent exit 0 (no checklist file)
    - PASS if exits 0 with no output

2. **Checklist Hook - With Items**: Test that hook returns context when checklist has items

    ```bash
    cd /tmp/bluera-base-test
    mkdir -p .bluera/bluera-base
    printf '%s\n' '# Test Checklist' '' '[ ] Item 1' '[ ] Item 2' > .bluera/bluera-base/checklist.md
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "$PLUGIN_PATH/hooks/checklist-remind.sh" 2>&1
    EXIT=$?
    echo "Exit code: $EXIT"
    ```

    - Expected: JSON output with additionalContext containing "2 items pending"
    - PASS if output contains "CHECKLIST" and "2 items pending"

3. **Checklist Hook - All Completed**: Test that hook exits silently when all items checked

    ```bash
    cd /tmp/bluera-base-test
    printf '%s\n' '# Test Checklist' '' '[x] Item 1' '[x] Item 2' > .bluera/bluera-base/checklist.md
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "$PLUGIN_PATH/hooks/checklist-remind.sh" 2>&1
    EXIT=$?
    rm -rf .bluera/bluera-base/checklist.md
    echo "Exit code: $EXIT"
    ```

    - Expected: Silent exit 0 (no pending items)
    - PASS if exits 0 with no JSON output

### Part 10: TODO Command

1. **TODO File Creation**: Test that TODO.txt can be created

    ```bash
    cd /tmp/bluera-base-test
    rm -rf .bluera/bluera-base/TODO.txt
    mkdir -p .bluera/bluera-base
    # Create minimal TODO file with required sections
    printf '%s\n' "## IMPORTANT" "" "* test item" "" "## TODO TASKS" "" "(none)" "" "## COMPLETED TASKS" "" "(none)" > .bluera/bluera-base/TODO.txt
    test -f .bluera/bluera-base/TODO.txt && echo "File created"
    ```

    - Expected: TODO.txt file is created
    - PASS if file exists

2. **TODO File Structure**: Verify TODO.txt has required sections

    ```bash
    cd /tmp/bluera-base-test
    grep -q "## TODO TASKS" .bluera/bluera-base/TODO.txt && \
    grep -q "## COMPLETED TASKS" .bluera/bluera-base/TODO.txt && \
    grep -q "## IMPORTANT" .bluera/bluera-base/TODO.txt && \
    echo "Structure valid"
    ```

    - Expected: All required sections present
    - PASS if all sections found

### Part 11: Safe Slash Commands

> **Note:** These commands are safe to run - they don't modify the repo structure.

1. **/help**: Run `/bluera-base:help`
   - Expected: Output contains "Commands" section
   - PASS if command executes and shows command list

2. **/explain overview**: Run `/bluera-base:explain overview`
   - Expected: Output contains "What is Bluera Base"
   - PASS if command executes and shows overview

3. **/config show**: Run `/bluera-base:config show`
   - Expected: Output shows config JSON or defaults
   - PASS if command executes without error

4. **/checklist show**: Run `/bluera-base:checklist show`
   - Expected: Shows checklist or "No checklist exists"
   - PASS if command executes without error

5. **/todo show**: Run `/bluera-base:todo show`
   - Expected: Shows TODO or creates file
   - PASS if command executes without error

6. **/learn show**: Run `/bluera-base:learn show`
   - Expected: Shows learnings or "No learnings"
   - PASS if command executes without error

7. **/worktree list**: Run `/bluera-base:worktree list`
   - Expected: Shows worktrees or "No worktrees"
   - PASS if command executes without error

8. **/claude-code-statusline**: Run `/bluera-base:claude-code-statusline`
   - Expected: Shows presets or current config
   - PASS if command executes without error

9. **/claude-code-analyze-config**: Run `/bluera-base:claude-code-analyze-config`
   - Expected: Shows analysis or "No .claude config"
   - PASS if command executes without error

10. **/claude-code-md audit**: Run `/bluera-base:claude-code-md audit`
    - Expected: Shows audit results
    - PASS if command executes without error

### Part 12: Additional Hook Tests

1. **notify.sh - Permission Prompt**:

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    echo '{"notification_type": "permission_prompt", "message": "Test"}' | \
      bash "$PLUGIN_PATH/hooks/notify.sh" 2>&1
    echo "Exit code: $?"
    ```

    - Expected: Exit 0 (notification sent or no notifier available)
    - PASS if exits 0

2. **session-setup.sh**:

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "$PLUGIN_PATH/hooks/session-setup.sh" 2>&1
    echo "Exit code: $?"
    ```

    - Expected: Exit 0 (jq check, permissions fix)
    - PASS if exits 0

3. **session-start-inject.sh**:

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "$PLUGIN_PATH/hooks/session-start-inject.sh" 2>&1
    echo "Exit code: $?"
    ```

    - Expected: Exit 0 (may output context JSON)
    - PASS if exits 0

4. **auto-commit.sh - No Changes**:

    ```bash
    cd /tmp/bluera-base-test
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    echo '{}' | CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "$PLUGIN_PATH/hooks/auto-commit.sh" 2>&1
    echo "Exit code: $?"
    ```

    - Expected: Exit 0 (no uncommitted changes to prompt about)
    - PASS if exits 0

5. **dry-scan.sh - Feature Disabled**:

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    echo '{}' | CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "$PLUGIN_PATH/hooks/dry-scan.sh" 2>&1
    echo "Exit code: $?"
    ```

    - Expected: Exit 0 (feature disabled by default)
    - PASS if exits 0

6. **pre-compact.sh**:

    ```bash
    PLUGIN_PATH="${CLAUDE_PLUGIN_ROOT:-$(pwd)}"
    echo '{"trigger": "manual"}' | CLAUDE_PROJECT_DIR="/tmp/bluera-base-test" bash "$PLUGIN_PATH/hooks/pre-compact.sh" 2>&1
    echo "Exit code: $?"
    ```

    - Expected: Exit 0 (preserves state before compaction)
    - PASS if exits 0

### Part 13: Cleanup

1. **Remove Test Directory**: Clean up test artifacts

    ```bash
    rm -rf /tmp/bluera-base-test
    rm -rf .bluera/bluera-base/state/milhouse-loop.md
    ```

    - Expected: Directory removed
    - PASS if command succeeds

2. **Verify Cleanup**: Confirm test directory is gone

    ```bash
    ls /tmp/bluera-base-test 2>&1 || echo "Cleanup successful"
    ```

    - Expected: Directory not found
    - PASS if directory doesn't exist

## Output Format

After running all tests, report results in this format:

### Plugin Test Results

| # | Test | Status |
|---|------|--------|
| 1 | Hook File Structure | ? |
| 2 | Hook Scripts Exist | ? |
| 3 | Block npm version | ? |
| 4 | Block git tag | ? |
| 5 | Allow skill-prefixed release | ? |
| 6 | Allow normal commands | ? |
| 7 | Anti-pattern Detection | ? |
| 8 | Clean Code Passes | ? |
| 9 | No State File (milhouse-stop) | ? |
| 10 | Invalid Iteration Handling | ? |
| 11 | Setup Creates State File | ? |
| 12 | /bluera-base:commit Command | ? |
| 13 | /bluera-base:cancel-milhouse Command | ? |
| 14 | All Skills Have SKILL.md | ? |
| 15 | Skills Are Readable | ? |
| 16 | Signals Library Tests | ? |
| 17 | State Library Tests | ? |
| 18 | Gitignore Integration Tests | ? |
| 19 | Checklist Hook - No File | ? |
| 20 | Checklist Hook - With Items | ? |
| 21 | Checklist Hook - All Completed | ? |
| 22 | TODO File Creation | ? |
| 23 | TODO File Structure | ? |
| 24 | /help | ? |
| 25 | /explain overview | ? |
| 26 | /config show | ? |
| 27 | /checklist show | ? |
| 28 | /todo show | ? |
| 29 | /learn show | ? |
| 30 | /worktree list | ? |
| 31 | /statusline | ? |
| 32 | /analyze-config | ? |
| 33 | /claude-md audit | ? |
| 34 | notify.sh | ? |
| 35 | session-setup.sh | ? |
| 36 | session-start-inject.sh | ? |
| 37 | auto-commit.sh | ? |
| 38 | dry-scan.sh | ? |
| 39 | pre-compact.sh | ? |
| 40 | Remove Test Directory | ? |
| 41 | Verify Cleanup | ? |

**Result: X/41 tests passed**

## Error Recovery

If tests fail partway through, clean up manually:

```bash
rm -rf /tmp/bluera-base-test
rm -rf .bluera/bluera-base/state/milhouse-loop.md
```
