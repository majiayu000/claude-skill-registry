---
name: meta-reviewing-cli-reviewing
description: CLI code review patterns. Use when reviewing CLI applications built with Commander.js, @clack/prompts, picocolors. Covers exit codes, signal handling, error messages, user experience, testing adequacy.
---

# CLI Code Review Patterns

> **Quick Guide:** When reviewing CLI code, verify SIGINT handling, p.isCancel() checks, exit code constants, parseAsync() usage, and user feedback (spinners, clear errors). Check config hierarchy, help text quality, and dry-run support. Distinguish severity (Must Fix vs Should Fix vs Nice to Have) and explain WHY each issue matters.

---

**Detailed Resources:**

- For CLI implementation patterns, see the cli-commander skill
- For general reviewing patterns, see the reviewing skill

---

<critical_requirements>

## CRITICAL: Before Reviewing CLI Code

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST verify SIGINT (Ctrl+C) handling exists in CLI entry point)**

**(You MUST verify p.isCancel() is called after EVERY @clack/prompts call)**

**(You MUST verify exit codes use named constants - flag ANY magic numbers in process.exit())**

**(You MUST verify parseAsync() is used for async actions, not parse())**

**(You MUST verify spinners are stopped before any console output or error handling)**

</critical_requirements>

---

**Auto-detection:** review CLI, check CLI code, CLI PR review, Commander.js review, @clack/prompts review, CLI quality, CLI error handling review, exit codes review

**When to use:**

- Reviewing CLI applications built with Commander.js
- Reviewing interactive prompts using @clack/prompts
- Checking CLI error handling and exit code patterns
- Evaluating CLI user experience (help text, spinners, feedback)
- Verifying CLI testing adequacy
- Reviewing configuration management patterns

**When NOT to use:**

- When implementing CLI code (use cli-commander skill instead)
- For general code review (use reviewing skill)
- For backend API review (use backend-specific reviewing skills)

**Key patterns covered:**

- CLI-specific review checklist
- Exit code and signal handling verification
- User experience review criteria
- Error message quality assessment
- Testing adequacy checklist
- Configuration hierarchy review
- Command structure and organization review
- Severity classification for CLI issues

---

<philosophy>

## Philosophy

**CLI UX is critical.** Unlike web apps with visual feedback, CLI tools communicate entirely through text. Poor error messages, missing progress indicators, or unexpected exits destroy user trust. Review with empathy for the end user.

**When reviewing CLI code:**

- Verify all paths to process.exit() use named constants
- Check that every async operation has visual feedback (spinners)
- Ensure cancellation is handled gracefully everywhere
- Validate error messages explain WHAT failed and HOW to fix it
- Confirm help text is useful and examples are included

**When NOT to be harsh:**

- Don't block PRs for help text wording if functionality is correct
- Don't require spinners for operations under 500ms
- Don't nitpick color choices if they follow existing patterns
- Don't request verbose mode if the CLI is simple enough

**Core principles:**

- **Safety First**: Exit codes and signal handling are non-negotiable
- **User Empathy**: Every error should guide users to resolution
- **Consistency**: All commands should follow the same patterns
- **Testability**: CLI code should be testable without spawning processes

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: CLI Review Checklist

Use this comprehensive checklist for every CLI code review.

#### Entry Point Verification

```markdown
## CLI Entry Point Review

**Signal Handling:**

- [ ] SIGINT handler exists in entry point
- [ ] SIGINT calls process.exit with EXIT_CODES.CANCELLED
- [ ] Other relevant signals handled (SIGTERM for containers)

**Command Registration:**

- [ ] Commands imported and registered cleanly
- [ ] parseAsync() used (not parse()) for async actions
- [ ] Global error handler with catch() on main()
- [ ] configureOutput() used for colored errors
- [ ] showHelpAfterError(true) enabled

**Global Options:**

- [ ] --dry-run supported for destructive operations
- [ ] --verbose supported for debug output
- [ ] --help generates useful output
- [ ] --version displays correct version
```

**Why this matters:** Entry point issues affect every command. Missing SIGINT handling leaves users unable to cancel, missing parseAsync swallows errors silently.

---

### Pattern 2: Exit Code Review

Verify all exit paths use named constants.

#### Exit Code Verification Checklist

```markdown
## Exit Codes Review

**Named Constants:**

- [ ] EXIT_CODES constant file exists (src/cli/lib/exit-codes.ts)
- [ ] All exit codes have JSDoc descriptions
- [ ] Uses `as const` for type inference

**Usage Audit:**

- [ ] No magic numbers in process.exit() calls
- [ ] Correct exit code for each scenario:
  - Success: EXIT_CODES.SUCCESS (0)
  - General error: EXIT_CODES.ERROR (1)
  - Invalid args: EXIT_CODES.INVALID_ARGS (2)
  - User cancelled: EXIT_CODES.CANCELLED
  - Validation failed: EXIT_CODES.VALIDATION_ERROR
```

```typescript
// Must Fix: Magic number exit code
process.exit(1); // What does 1 mean?

// Good: Named constant
process.exit(EXIT_CODES.VALIDATION_ERROR);
```

**Why this matters:** Magic exit codes are unmaintainable. Scripts that depend on your CLI need predictable, documented exit codes.

---

### Pattern 3: Prompt Cancellation Review

Every @clack/prompts call must check for cancellation.

#### Cancellation Handling Audit

```typescript
// Must Fix: Missing isCancel check
const name = await p.text({ message: "Name:" });
// User presses Ctrl+C - name is Symbol, code continues with garbage

// Good: Proper cancellation handling
const name = await p.text({ message: "Name:" });
if (p.isCancel(name)) {
  p.cancel("Setup cancelled");
  process.exit(EXIT_CODES.CANCELLED);
}
```

**Review Checklist:**

```markdown
## Prompt Cancellation Review

For EACH @clack/prompts call (p.text, p.select, p.confirm, p.multiselect):

- [ ] p.isCancel() check immediately follows
- [ ] p.cancel() called with descriptive message
- [ ] process.exit() called with EXIT_CODES.CANCELLED
- [ ] No code executes after isCancel returns true
```

**Why this matters:** Missing isCancel checks cause undefined behavior when users press Ctrl+C. The code continues with a Symbol value instead of the expected string/boolean.

---

### Pattern 4: Async Operation Review

Verify spinners and error handling for all async work.

#### Spinner Usage Review

```typescript
// Must Fix: No feedback for long operation
const data = await fetchRemoteConfig(); // User sees nothing

// Good: Spinner with descriptive messages
const s = p.spinner();
s.start("Fetching configuration...");
try {
  const data = await fetchRemoteConfig();
  s.stop(`Loaded ${data.items.length} items`);
} catch (error) {
  s.stop("Failed to fetch configuration");
  p.log.error(error.message);
  process.exit(EXIT_CODES.NETWORK_ERROR);
}
```

**Review Checklist:**

```markdown
## Async Operations Review

For EACH async operation (API calls, file operations, network):

- [ ] Spinner started with descriptive message
- [ ] Spinner stopped before any console output
- [ ] Spinner stopped before error logging
- [ ] Success message includes result info
- [ ] Error handling exists with appropriate exit code
```

**Why this matters:** Users need feedback that something is happening. Silent operations feel broken.

---

### Pattern 5: Error Message Quality Review

Evaluate error messages for actionability.

#### Error Message Criteria

```markdown
## Error Message Review

For EACH error path:

- [ ] Message explains WHAT failed (not just "Error")
- [ ] Message explains WHY it failed (permission, network, validation)
- [ ] Message suggests HOW to fix it (retry, check config, provide flag)
- [ ] Uses picocolors consistently (red for errors, yellow for warnings)
- [ ] Includes relevant context (file path, option name, command)
```

```typescript
// Must Fix: Unhelpful error
p.log.error("Failed");

// Should Fix: Better but no resolution
p.log.error(`Config file not found: ${configPath}`);

// Good: Actionable error
p.log.error(`Config file not found: ${configPath}`);
p.log.info(`Run 'mycli init' to create one, or specify path with --config`);
```

**Why this matters:** Actionable errors reduce support burden and improve user experience. Users should never be stuck.

---

### Pattern 6: Configuration Hierarchy Review

Verify config resolution follows correct precedence.

#### Config Precedence Checklist

```markdown
## Configuration Review

**Precedence Order (highest to lowest):**

1. [ ] CLI flags (--source, --config)
2. [ ] Environment variables (MYAPP_SOURCE)
3. [ ] Project config (.myapp/config.yaml in cwd)
4. [ ] Global config (~/.myapp/config.yaml)
5. [ ] Default values (hardcoded constants)

**Implementation:**

- [ ] resolveConfig function exists and follows precedence
- [ ] Empty flag values handled (--source "" should error or skip)
- [ ] Missing config files handled gracefully (no crash)
- [ ] Source/origin tracked for debugging (--verbose shows where value came from)
```

**Why this matters:** Incorrect config precedence confuses users. If env var overrides flag, that's a bug.

---

### Pattern 7: Help Text Review

Evaluate command documentation quality.

#### Help Text Checklist

```markdown
## Help Text Review

**Command Documentation:**

- [ ] Description is clear and concise
- [ ] All options have descriptions
- [ ] Required vs optional options clear
- [ ] Default values documented in option descriptions

**Examples Section:**

- [ ] Common use cases shown
- [ ] Examples are copy-paste ready
- [ ] Complex options demonstrated

**Consistency:**

- [ ] Naming follows conventions (--dry-run not --dryRun)
- [ ] Short flags used for common options (-f for --force)
- [ ] Help shown after errors (showHelpAfterError enabled)
```

---

### Pattern 8: Testing Adequacy Review

Verify CLI tests cover critical paths.

#### CLI Testing Checklist

```markdown
## Testing Review

**Command Testing:**

- [ ] Happy path tested for each command
- [ ] Invalid arguments tested (missing required, unknown options)
- [ ] --help output tested
- [ ] exitOverride() used to prevent process.exit in tests

**Prompt Testing:**

- [ ] @clack/prompts mocked properly
- [ ] Cancellation flow tested (isCancel returns true)
- [ ] Validation rejection tested
- [ ] Multiple selection paths tested

**File System Testing:**

- [ ] memfs or vol.reset() used for isolated tests
- [ ] Config loading tested (missing, invalid, valid)
- [ ] File write operations tested

**Exit Code Testing:**

- [ ] Success exits with 0
- [ ] Errors exit with correct non-zero codes
- [ ] Cancellation exits with CANCELLED code
```

---

### Pattern 9: Command Structure Review

Verify command organization is logical.

#### Structure Checklist

```markdown
## Command Structure Review

**Organization:**

- [ ] Related commands grouped as subcommands (config show, config set)
- [ ] Each command in separate file
- [ ] No god commands (> 200 lines)
- [ ] Shared utilities extracted to lib/

**Options:**

- [ ] Global options defined on parent (--verbose, --dry-run)
- [ ] optsWithGlobals() used to access parent options
- [ ] Option names consistent across commands

**Arguments:**

- [ ] Positional arguments have clear names
- [ ] Required vs optional arguments documented
- [ ] Argument validation happens early in action
```

---

### Pattern 10: Security Review

Check for CLI-specific security concerns.

#### Security Checklist

```markdown
## CLI Security Review

**Input Validation:**

- [ ] No shell injection (user input not concatenated into shell commands)
- [ ] File paths validated before operations
- [ ] URLs validated before fetch

**Secrets Handling:**

- [ ] API keys/tokens not logged (even in verbose mode)
- [ ] Sensitive options not shown in help output
- [ ] Config files with secrets have appropriate permissions warning

**Dependency Injection:**

- [ ] Arguments not passed directly to child_process
- [ ] execa or similar used instead of exec when needed
```

</patterns>

---

<decision_framework>

## Decision Framework

### Severity Classification for CLI Issues

```
Is this a safety/correctness issue?
├─ Missing SIGINT handler → MUST FIX
├─ Missing p.isCancel() check → MUST FIX
├─ Magic number exit code → MUST FIX
├─ parse() instead of parseAsync() → MUST FIX
├─ Missing error handling on async → MUST FIX
└─ NO → Is it a user experience issue?
    ├─ Missing spinner for >500ms operation → SHOULD FIX
    ├─ Unhelpful error message → SHOULD FIX
    ├─ Incorrect config precedence → SHOULD FIX
    ├─ Missing --help descriptions → SHOULD FIX
    └─ NO → Is it an enhancement?
        ├─ Could add --json output → NICE TO HAVE
        ├─ Could add more examples in help → NICE TO HAVE
        ├─ Could improve verbose logging → NICE TO HAVE
        └─ Style preference → DON'T MENTION
```

### Approval Decision Framework

**APPROVE when:**

- All SIGINT/cancellation handling verified
- All exit codes use named constants
- parseAsync() used for async commands
- Error handling exists for async operations
- Tests cover critical paths

**REQUEST CHANGES when:**

- Missing p.isCancel() checks (any prompt)
- Magic numbers in process.exit()
- parse() used with async actions
- Missing spinner for long operations
- Unhelpful error messages

**MAJOR REVISIONS NEEDED when:**

- No SIGINT handler in entry point
- Systematic missing cancellation handling
- No exit code constants defined
- No error handling pattern established
- Security vulnerabilities (shell injection)

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues (Must Fix):**

- Missing `process.on("SIGINT", ...)` in entry point
- Missing `p.isCancel()` after ANY prompt call
- Using `process.exit(1)` or `process.exit(0)` instead of named constants
- Using `program.parse()` instead of `program.parseAsync()` with async actions
- Spinner not stopped before error logging (output corruption)
- Shell injection vulnerability (user input in exec/spawn)

**Medium Priority Issues (Should Fix):**

- No spinner for operations likely to exceed 500ms
- Error message says what failed but not how to fix it
- Missing `--dry-run` support for destructive operations
- No verbose mode for debugging
- Config precedence incorrect (env overrides flag)
- Missing validation for user input in prompts
- No `showHelpAfterError(true)` configured

**Common Mistakes:**

- Forgetting to call process.exit() after p.cancel()
- Not using optsWithGlobals() to access parent command options
- Logging before stopping spinner (garbled output)
- Not handling empty string values for flags
- YAML parse errors not caught
- Async errors swallowed in .action() callbacks

**Gotchas & Edge Cases:**

- Commander auto-converts `--my-option` to `myOption` in options object
- Spinner.stop() must be called even on error path
- p.isCancel() returns true for Symbol values, not undefined
- process.exit() in async context may not wait for pending I/O
- Colors may not render in CI environments (check NO_COLOR env)
- Config file might exist but be invalid YAML

</red_flags>

---

<testing>

## Testing CLI Reviews

### What to Look For in CLI Tests

```typescript
// Good: Tests use exitOverride to catch exits
describe("init command", () => {
  beforeEach(() => {
    program.exitOverride();
  });

  it("exits with INVALID_ARGS for missing required option", async () => {
    await expect(
      program.parseAsync(["node", "test", "init"]),
    ).rejects.toThrow();
    // Verify error handling without actually exiting
  });
});

// Good: Prompts are properly mocked
vi.mock("@clack/prompts", () => ({
  select: vi.fn(),
  confirm: vi.fn(),
  text: vi.fn(),
  spinner: vi.fn(() => ({ start: vi.fn(), stop: vi.fn() })),
  isCancel: vi.fn((val) => val === Symbol.for("cancel")),
  cancel: vi.fn(),
  intro: vi.fn(),
  outro: vi.fn(),
  log: { info: vi.fn(), error: vi.fn(), success: vi.fn() },
}));

// Good: File system isolated
vi.mock("fs-extra", async () => {
  const memfs = await import("memfs");
  return memfs.fs.promises;
});

beforeEach(() => {
  vol.reset();
});
```

### Test Coverage Expectations

```markdown
## Minimum Test Coverage for CLI

**Each Command:**

- [ ] Success path with valid arguments
- [ ] Failure path with invalid arguments
- [ ] Help output accessible

**Each Prompt Flow:**

- [ ] Successful completion
- [ ] User cancellation (Ctrl+C)
- [ ] Validation rejection

**Configuration:**

- [ ] Loads from each source (flag, env, project, global)
- [ ] Precedence is correct
- [ ] Missing files handled gracefully

**Exit Codes:**

- [ ] Success returns 0
- [ ] Each error type returns correct code
```

</testing>

---

<example_review_output>

## Example Review Output

````markdown
# CLI Code Review: init command

## Summary

The init command implementation has good structure but is missing critical
cancellation handling that would leave users stuck if they press Ctrl+C.

---

## Must Fix (3 issues)

### 1. Missing p.isCancel() check

**File:** src/cli/commands/init.ts:45
**Issue:** p.select() result not checked for cancellation
**Impact:** If user presses Ctrl+C, code continues with Symbol value causing crash
**Fix:** Add isCancel check:

```typescript
const framework = await p.select({ ... });
if (p.isCancel(framework)) {
  p.cancel("Setup cancelled");
  process.exit(EXIT_CODES.CANCELLED);
}
```
````

### 2. Magic number exit code

**File:** src/cli/commands/init.ts:78
**Issue:** `process.exit(1)` uses magic number
**Impact:** Exit codes become undocumented and unmaintainable
**Fix:** Use `process.exit(EXIT_CODES.ERROR)`

### 3. Using parse() instead of parseAsync()

**File:** src/cli/index.ts:42
**Issue:** `program.parse()` used with async action handlers
**Impact:** Errors in async actions are silently swallowed
**Fix:** Change to `await program.parseAsync(process.argv)`

---

## Should Fix (2 issues)

### 1. Missing spinner for network call

**File:** src/cli/commands/init.ts:52
**Issue:** `fetchTemplates()` has no visual feedback
**Impact:** Users see no progress during network operation
**Fix:** Wrap in spinner:

```typescript
const s = p.spinner();
s.start("Fetching templates...");
const templates = await fetchTemplates();
s.stop(`Found ${templates.length} templates`);
```

### 2. Error message not actionable

**File:** src/cli/commands/init.ts:67
**Issue:** Error says "Config invalid" but not how to fix
**Impact:** Users don't know what's wrong with their config
**Fix:** Include specific validation error and example of correct format

---

## Nice to Have (1 item)

### 1. Add --json output option

**File:** src/cli/commands/init.ts
**Suggestion:** Add `--json` flag for CI/script integration
**Benefit:** Enables automation and tooling integration

---

## What Was Done Well

- Clean command structure with separate files per command
- Good use of picocolors for consistent styling
- SIGINT handler present in entry point
- Config hierarchy follows correct precedence
- Tests cover happy path scenarios

---

## Verdict: REQUEST CHANGES

The Must Fix issues (cancellation handling, magic exit codes, parseAsync)
must be addressed before approval. These are safety issues that affect
all users of the CLI.

```

</example_review_output>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST verify SIGINT (Ctrl+C) handling exists in CLI entry point)**

**(You MUST verify p.isCancel() is called after EVERY @clack/prompts call)**

**(You MUST verify exit codes use named constants - flag ANY magic numbers in process.exit())**

**(You MUST verify parseAsync() is used for async actions, not parse())**

**(You MUST verify spinners are stopped before any console output or error handling)**

**Failure to catch these issues will result in CLIs that crash on Ctrl+C, have undocumented exit codes, and silently swallow errors.**

</critical_reminders>
```
