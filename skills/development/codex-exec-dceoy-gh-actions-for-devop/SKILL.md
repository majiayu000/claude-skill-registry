---
name: codex-exec
description: Execute development tasks using OpenAI Codex CLI for code generation, refactoring, feature implementation, and bug fixes. Use when the user asks to create code, add features, refactor, fix bugs, or generate tests. Requires Codex CLI installed.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Codex Exec Skill

Use OpenAI Codex CLI to execute development tasks that involve code modifications. This skill **modifies code**.

## When to Use

- User asks to "add", "create", "implement", or "generate" code
- User wants to refactor existing code
- User needs to fix a bug
- User wants to create tests
- User asks to "update" or "modify" code

## Prerequisites

Verify Codex CLI is available:

```bash
codex --version  # Should display installed version
```

## Basic Usage

### Step 1: Understand the Task

Parse what needs to be done:

- What to create/modify?
- Which files are affected?
- What's the expected outcome?
- Any constraints or requirements?

### Step 2: Gather Context

Before executing, understand current state:

```bash
git status  # Check for uncommitted changes
git diff    # See existing modifications
```

Read relevant files to understand patterns.

### Step 3: Execute Codex

Run Codex with clear instructions:

```bash
codex --sandbox=workspace-write exec "[TASK]

Follow these guidelines:
- Follow existing code patterns and conventions
- Add appropriate error handling
- Include necessary imports
- Maintain code quality and readability
- Use TypeScript types where applicable
- Add comments for complex logic

Project context:
- Language: [e.g., TypeScript, Python, Go, Rust]
- Framework: [e.g., React, Django, Express]
- Build tool: [e.g., Vite, webpack, cargo, go build]
- Coding style: [Reference style guide or linter config]"
```

### Step 4: Verify Changes

After execution:

```bash
git status              # See what changed
git diff                # Review modifications
<lint-command>          # Check for errors
<test-command>          # Run tests
```

### Step 5: Report Results

Provide clear summary:

- What files were modified/created
- What changes were made
- Verification results (lint, types, tests)
- Any issues or warnings

## Example Tasks

### Generate New Code

```bash
codex --sandbox=workspace-write exec "Create a UserProfile component in src/components/ with:
- Props: name (string), email (string), avatar (string optional)
- Display user info in a card layout
- Use TypeScript types
- Follow existing component patterns
- Add CSS modules for styling"
```

### Refactor Code

```bash
codex --sandbox=workspace-write exec "Refactor the validation logic in src/components/LoginForm.tsx:
- Extract validation into separate src/utils/validation.ts file
- Create validateEmail and validatePassword functions
- Maintain all existing functionality
- Add TypeScript types"
```

### Fix Bugs

```bash
codex --sandbox=workspace-write exec "Fix the memory leak in src/hooks/useWebSocket.ts:
- The WebSocket connection is not being cleaned up
- Add proper cleanup in useEffect return function
- Ensure connection closes on unmount"
```

### Add Features

```bash
codex --sandbox=workspace-write exec "Add email validation to ContactForm.tsx:
- Use regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
- Show error message below input field
- Validate on blur and submit
- Prevent submission if invalid
- Style error message in red"
```

### Create Tests

```bash
codex --sandbox=workspace-write exec "Create unit tests for src/utils/validation.ts:
- Test validateEmail with valid/invalid inputs
- Test validatePassword with edge cases
- Test error messages
- Use Jest and React Testing Library
- Aim for 100% coverage"
```

## Execution Modes

### Safe Mode (Default)

```bash
codex --sandbox=workspace-write exec "[TASK]"
# Prompts for approval before each action
```

### Preview Mode

```bash
codex --sandbox=workspace-write exec "[TASK]" --dry-run
# Shows what would be done without executing
```

### Automated Mode ⚠️

```bash
codex --sandbox=workspace-write exec "[TASK]" --yes
# Auto-approves all actions - use with caution!
```

**Only use `--yes` for:**

- Low-risk tasks (formatting, comments)
- Isolated environments
- Well-tested operations

**Never use `--yes` for:**

- Production code
- Security-sensitive changes
- Database operations
- File deletions

## Verification Workflow

After Codex executes, ALWAYS:

1. **Review changes**:

   ```bash
   git diff
   ```

2. **Run linter**:

   ```bash
   <lint-command>
   ```

3. **Run tests**:

   ```bash
   <test-command>
   ```

4. **Manual testing**:

   Start your development server and test the functionality manually.

5. **Report status**:
   - ✅ Changes applied successfully
   - ✅ Linter passed
   - ✅ Tests passed
   - ✅ Manual testing confirmed

## Best Practices

✅ **DO:**

- Be specific in task descriptions
- Include file paths
- Specify expected behavior
- Review all changes with `git diff`
- Run linter and tests
- Test manually before declaring success

❌ **DON'T:**

- Use vague instructions like "make it better"
- Skip verification steps
- Use `--yes` for critical code
- Commit without reviewing
- Ignore errors or warnings

## Error Handling

**If execution fails:**

1. Check the error message
2. Verify Codex authentication
3. Try with more specific instructions
4. Break task into smaller steps

**If changes are incorrect:**

1. Revert: `git restore .` or `git restore <file>`
2. Re-execute with better instructions
3. Or fix manually

**If tests fail:**

1. Review what broke
2. Ask Codex to fix the test failures
3. Or fix manually

## Writing Effective Tasks

### Good Task Description

```
"Add email validation to ContactForm.tsx using regex pattern.
Show error message below the input field on blur.
Prevent form submission if email is invalid.
Style the error message in red (#dc2626).
Follow existing form validation patterns."
```

### Poor Task Description

```
"Add validation"  # Too vague
"Fix the form"    # No specifics
```

## Safety Checklist

Before using codex-exec:

- [ ] Understand what will be modified
- [ ] Have clean git state (can rollback)
- [ ] Know which files will be affected
- [ ] Have tests to verify correctness

After using codex-exec:

- [ ] Reviewed changes with `git diff`
- [ ] Ran linter (language-specific)
- [ ] Ran type checker (if applicable)
- [ ] Ran tests (language-specific)
- [ ] Tested manually
- [ ] Ready to commit

## Related Skills

- **codex-ask**: For understanding code before modifying
- **codex-review**: For reviewing changes after modification

## Tips for Success

1. **Start small**: Test with simple tasks first
2. **Be specific**: Include file paths, requirements, constraints
3. **Follow patterns**: Reference existing code to follow
4. **Verify always**: Never skip the verification workflow
5. **Iterate**: Use codex-ask → codex-exec → codex-review cycle

## Limitations

- Cannot run code or execute tests itself
- May not understand complex business logic
- Limited by context window size
- Requires manual verification
- Cannot guarantee correctness

---

**Remember**: This skill MODIFIES code. Always review changes before committing!
