---
name: local-review
description: Review current changes against project guidelines before PR
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: reviewer
---

# Local Review

Perform a comprehensive self-review of changes before creating a pull request.

## Instructions

1. **Gather Context**
   - Get current branch name
   - Find associated workflow folder
   - Read the original issue/concept and plan

2. **Get Changes**
   - Run `git diff main...HEAD` to see all changes
   - Run `git log main...HEAD --oneline` to see commits
   - List all modified files

3. **Review Against Guidelines**

   ### CODING_GUIDELINES.md Checklist

   **Architecture**
   - [ ] Three-layer command pattern followed (Cobra → Wrapper → Execute)
   - [ ] Config loaded once and passed through
   - [ ] Using `internal/git/` wrappers, not direct git calls
   - [ ] Custom error types from `internal/errors`

   **Code Style**
   - [ ] Imports organized: stdlib, third-party, local
   - [ ] Naming conventions followed
   - [ ] Exported functions documented
   - [ ] No ignored errors

   **Configuration Precedence**
   - [ ] Three-layer hierarchy: defaults → git config → flags
   - [ ] Pointer types for optional booleans
   - [ ] Flags always win

   **Anti-Engineering**
   - [ ] No unnecessary abstractions
   - [ ] No premature optimization
   - [ ] Changes focused on the task

   ### TESTING_GUIDELINES.md Checklist

   **Test Structure**
   - [ ] One test case per function (no table-driven for integration)
   - [ ] Descriptive test names
   - [ ] Test comments with Steps section

   **Test Implementation**
   - [ ] Using testutil helpers
   - [ ] Proper setup/cleanup
   - [ ] Testing success and error paths

   **Working Directory**
   - [ ] Using `cmd.Dir`, not `os.Chdir()` where possible
   - [ ] If `os.Chdir()` used, proper save/restore

   ### COMMIT_GUIDELINES.md Checklist

   - [ ] Commit messages follow format
   - [ ] Subject line ≤50 characters
   - [ ] Type matches change (feat/fix/refactor/test/docs)
   - [ ] Issue referenced in footer
   - [ ] No AI attribution lines

   ### Documentation Checklist

   - [ ] Manpage updated if command/options changed
   - [ ] Config documentation updated if config changed
   - [ ] Help text updated

4. **Code Quality Checks**
   ```bash
   # Build check
   go build ./...

   # Test check
   go test ./...

   # Format check
   go fmt ./...

   # Vet check
   go vet ./...
   ```

5. **Generate Review Report**

   Create a summary with:

   ```markdown
   # Local Review: <branch-name>

   ## Summary
   - Files changed: <count>
   - Lines added: <count>
   - Lines removed: <count>
   - Commits: <count>

   ## Checklist Results

   ### Passed
   - <item 1>
   - <item 2>

   ### Issues Found
   - [ ] <issue 1> - <file:line> - <description>
   - [ ] <issue 2> - <file:line> - <description>

   ### Warnings
   - <warning 1>

   ## Quality Checks
   - Build: PASS/FAIL
   - Tests: PASS/FAIL (<count> passed)
   - Format: PASS/FAIL
   - Vet: PASS/FAIL

   ## Recommendations
   1. <recommendation>
   2. <recommendation>

   ## Ready for PR?
   <YES/NO - explain if NO>
   ```

6. **Report Findings**
   - If issues found, list them with specific file:line references
   - Suggest fixes for each issue
   - Indicate if changes are PR-ready

## Issue Categories

### Blocking (must fix)
- Test failures
- Build errors
- Missing error handling
- Security concerns
- Guideline violations

### Warnings (should fix)
- Missing documentation
- Inconsistent naming
- Suboptimal patterns

### Suggestions (nice to have)
- Code clarity improvements
- Additional test cases
- Performance optimizations
