---
name: Debug Workflow
description: Guides developers through scenario test debugging using Ruby debug gem step execution. Provides interactive debugging patterns and test helper context.
---

# Debug Workflow Skill

Guide for debugging failing scenario tests using Ruby debug gem step execution and interactive debugging workflow.

## When to Use This Skill

Use this skill when:
- You need to debug a failing scenario test
- You want to understand test execution behavior interactively
- You need guidance on setting up the debug environment
- You want to learn the four core debugging patterns
- You're integrating debugging into the TDD cycle

## Your Primary Role

Help developers debug failing scenario tests by:
1. **Analyzing test structure** — Understanding what the test expects
2. **Setting up debug environment** — Installing gem, preparing test command
3. **Guiding interactive debugging** — Walking through step execution
4. **Interpreting state** — Helping read variables, file system, command outputs
5. **Identifying root causes** — Connecting debug findings to actual code issues

## When Developers Ask For Help

### Scenario 1: "How do I debug test/scenario/new_scenario_test.rb?"

**Your approach:**
1. Read the test file to understand structure
2. Identify what assertions are being tested
3. Show the exact debug command: `ruby -r debug -Itest test/scenario/new_scenario_test.rb`
4. Explain available debug commands (step, next, pp, continue, help)
5. Reference the official guide: `.claude/docs/step-execution-guide.md`

### Scenario 2: "My test is failing. Debug session output shows..."

**Your approach:**
1. Analyze the debug output they provide
2. Explain what it means (variable values, execution state)
3. Suggest next debug steps
4. Guide use of specific debugging commands:
   - `pp output` to inspect ptrk command output
   - `system("ls -la #{tmpdir}")` to check file system
   - `info locals` to see all variables
5. Help interpret findings in context of test expectations

### Scenario 3: "I'm in a debug session. This assertion is failing..."

**Your approach:**
1. Ask what the failure is (output mismatch, missing file, wrong status code?)
2. Suggest specific inspection commands
3. Walk through how to check file system or variable values
4. Guide toward identifying the root cause
5. Propose where in the implementation to look for the bug

## Core Debugging Patterns

Guide developers through these four patterns:

### Pattern 1: Check Command Success

```ruby
output, status = run_ptrk_command("new #{project_id}", cwd: tmpdir)
# Debug: Is ptrk command succeeding?

(rdbg) pp status.success?       # true or false?
(rdbg) pp status.exitstatus     # 0 or non-zero?
(rdbg) pp output                # What's the error message?
```

When debugging: Distinguish between command logic errors and execution problems. Check exit code first, then inspect output.

### Pattern 2: Verify File System State

```ruby
assert Dir.exist?(File.join(project_dir, "storage", "home"))
# Debug: Was the directory actually created?

(rdbg) system("ls -la #{tmpdir}")         # List all created dirs
(rdbg) system("find #{tmpdir} -type d")   # Find all directories
(rdbg) system("ls -la #{project_dir}")    # List project contents
```

When debugging: Use `system()` calls to explore actual vs expected file structure. This shows what was really created.

### Pattern 3: Check Assertion Pattern Matching

```ruby
assert_match(/expected_pattern/, output)
# Debug: Does the output actually contain the pattern?

(rdbg) pp output                        # See full output
(rdbg) pp output.lines                  # Split into lines
(rdbg) pp output.include?("pattern")    # Check for substring
(rdbg) pp output.match?(/regex_pattern/)  # Check regex match
```

When debugging: Show exact output so differences from expectations are clear. Help developers see where the mismatch is.

### Pattern 4: Multi-Step Workflow Debugging

```ruby
run_ptrk_command("new #{project_id}", cwd: tmpdir)
run_ptrk_command("env list", cwd: project_dir)
run_ptrk_command("env set --latest", cwd: project_dir)
# Debug: Which step fails? What's the state after each?

(rdbg) step                           # Execute first command
(rdbg) system("ls -la #{tmpdir}")     # Check what's created
(rdbg) continue                       # Skip to next command
(rdbg) pp output                      # Check its output
(rdbg) step                           # Execute third command
```

When debugging: Break workflow into steps, check state after each. Use `continue` to jump between steps efficiently.

## Available Debugger Commands

These are the tools developers have in the `(rdbg)` prompt:

| Command | Short | Purpose | Example |
|---------|-------|---------|---------|
| `step` | `s` | Step to next line (enter method calls) | `(rdbg) step` |
| `next` | `n` | Step over next line (skip method calls) | `(rdbg) next` |
| `continue` | `c` | Continue until next breakpoint | `(rdbg) continue` |
| `finish` | `f` | Continue until method returns | `(rdbg) finish` |
| `pp var` | | Pretty-print variable value | `(rdbg) pp output` |
| `pp var.class` | | Show variable's class | `(rdbg) pp status.class` |
| `pp var.inspect` | | Show inspected details | `(rdbg) pp output.inspect` |
| `info locals` | | Show all local variables | `(rdbg) info locals` |
| `list` | `l` | Show code context (5 lines) | `(rdbg) list` |
| `system(cmd)` | | Execute shell command | `(rdbg) system("ls -la #{tmpdir}")` |
| `help` | `h` | Show all debugger commands | `(rdbg) help` |
| `quit` | `q` | Exit debugger | `(rdbg) quit` |

## Test Helper Functions Reference

The tests use these helpers (from `test/test_helper.rb`):

```ruby
# Generate unique project ID for test isolation
project_id = generate_project_id
# Returns: "20251203_015500_abc123f" (timestamp + hash)

# Execute ptrk CLI command in specified directory
output, status = run_ptrk_command("new my-project", cwd: tmpdir)
# Returns: [String output, Process::Status status]
# - output: stdout or stderr combined
# - status: Process::Status with .success? and .exitstatus
```

When debugging: Use these to understand what test data is, what commands are being run.

## Important Context About Tests

- **Test isolation**: Each test uses `Dir.mktmpdir` with `generate_project_id()`
- **Working directory**: Tests run in tmpdir, not actual project
- **Exit codes matter**: Always check `status.success?` after ptrk commands
- **File permissions**: tmpdir has normal read/write/execute permissions
- **Cleanup**: tmpdir is automatically cleaned up when test exits

## Common Test Structure

Most scenario tests follow this pattern:

```ruby
def test_something_meaningful
  Dir.mktmpdir do |tmpdir|
    project_id = generate_project_id
    output, status = run_ptrk_command("new #{project_id}", cwd: tmpdir)

    # Assertions about project structure, command output, etc
    assert status.success?
    assert File.exist?(...)
    assert_match(/pattern/, output)
  end
end
```

When debugging: Help developers understand the test setup, identify where the failure occurs, and inspect the state at that point.

## Integration with TDD Cycle

Help developers apply debugging workflow within t-wada style TDD:

1. **Red Phase**: Run test normally, see failure
   ```bash
   bundle exec ruby -Itest test/scenario/your_test.rb
   ```
   → Failure is expected, shows what needs fixing

2. **Green Phase**: Debug to understand expected behavior
   ```bash
   ruby -r debug -Itest test/scenario/your_test.rb
   ```
   → Use step execution to see what should happen
   → Modify implementation code based on findings

3. **RuboCop Phase**: Lint the code
   ```bash
   bundle exec rubocop test/scenario/your_test.rb --autocorrect
   ```

4. **Refactor Phase**: Debug again to verify changes work
   ```bash
   ruby -r debug -Itest test/scenario/your_test.rb
   ```
   → Ensure refactoring didn't break behavior

5. **Commit Phase**: Clean git history
   ```bash
   git add . && git commit -m "..."
   ```

## Reference Documentation

Always direct developers to these resources:

- **`.claude/docs/step-execution-guide.md`** — Comprehensive guide
  - Complete installation instructions
  - Basic workflow walkthrough
  - Detailed practical examples
  - Advanced techniques
  - Troubleshooting section

- **`CLAUDE.md`** — Project development guide
  - Quick start for debugging
  - Integration with TDD cycle
  - Test helper reference
  - Common debugging patterns

- **`.claude/examples/debugging-session-example.md`** — Real-world example
  - Actual debug session transcript
  - Common inspection patterns
  - Troubleshooting during debug sessions

- **`test_helper.rb`** — Test utilities implementation
  - Test helper function definitions
  - Test case base class setup
