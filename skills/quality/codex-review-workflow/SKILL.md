---
name: codex-review-workflow
version: 1.0.0
description: Automated code review workflow using OpenAI Codex CLI. Implements iterative fix-and-review cycles until code passes validation or reaches iteration limit. Use when building features requiring automated code validation, security checks, or quality assurance through Codex CLI.
category: automation
tags:
  - automation
  - code-review
  - quality
  - testing
triggers:
  - 'review with codex'
  - 'run codex review'
  - 'automated code review'
  - 'validate with codex'
  - 'codex cli'
prerequisites:
  - Codex CLI installed and available
  - Git repository (or --skip-git-repo-check flag)
related_skills:
  - testing-strategist
  - security-engineer
  - quality-auditor
  - technical-writer
related_mcps:
  - code-quality-scanner
  - security-scanner
---

# Codex Review Workflow

## Overview

Automated code review workflow using OpenAI Codex CLI. Implements iterative fix-and-review cycles to ensure code quality through automated validation.

**Use when:** Building features that require automated code review, iterative refinement cycles, or validation against specific quality standards using Codex CLI.

## When to Use This Skill

✅ **Use this skill when:**

- User explicitly requests Codex CLI review (e.g., "Review this with Codex")
- Implementing features that require automated code validation
- Building code that must meet specific quality standards
- Iterative review and refinement is needed
- Validating security, bugs, and best practices automatically

❌ **Skip this skill when:**

- User only wants manual code review
- Codex CLI is not available in the environment
- Task is purely exploratory or research-based
- Simple code that doesn't require formal review

## Prerequisites

- Codex CLI installed and available on PATH
- Git repository (or use `--skip-git-repo-check` flag)
- Verify installation: `codex --version`

## Core Workflow

This skill follows a structured 6-step process:

### 1. Complete the Coding Task

Implement the user's requested feature using standard best practices. Ensure code is well-structured before submitting for review.

**Track progress with TodoWrite:**

- Implement the requested feature/fix
- Run initial Codex CLI review
- Fix issues found in review (if any)
- Run final Codex CLI review
- Report final status

### 2. Run Initial Codex CLI Review

**Git requirement:** Codex CLI requires a git repository. If not in a git repo, run `git init` first, or use `--skip-git-repo-check` flag (not recommended for production).

Execute Codex CLI review using `codex exec` (NOT `codex review`):

```bash
# For a specific file
codex exec "Review the code in <file_name> for bugs, security issues, best practices, and potential improvements. Provide specific, actionable feedback with line numbers and examples."

# For multiple files
codex exec "Review the files auth.py, user.py, and session.py for bugs, security issues, best practices, and potential improvements. Provide specific feedback for each file."

# With working directory context
codex exec "Review the code in email_validator.py for bugs, security issues, best practices, and potential improvements. Provide specific feedback." -C /path/to/project

# With specific model
codex exec "Review <file_name>..." -m gpt-5-codex

# With custom configuration
codex exec "Review <file_name>..." -c model="o3"
```

**Key points:**

- Be specific in prompts about what to review
- Request line numbers and specific examples
- Use appropriate timeout (120000ms = 2 minutes recommended)

### 3. Analyze Review Results

Codex CLI returns structured markdown output with **variable formats**. Look for:

**Critical issue indicators (MUST FIX):**

- Sections: **Bug**, **Security**, **Key Issues**, **Key Findings**
- Severity markers: "High:", "Medium:", "critical", "vulnerability"

**Quality improvements (LOWER PRIORITY):**

- Sections: **Maintainability**, **Usability**, **Best Practices**, **Suggestions**
- Severity markers: "Low:"

**Confirmation indicators (success):**

- Sections: **Resolved Checks**, **Review**, **Review Findings**
- Phrases: "No remaining findings", "All issues resolved", "All [N] issues look resolved"
- Check marks (✅) or confirmation language

**Decision criteria:**

- **Complete:** No Bug/Security/Key Issues sections AND only suggestions remain
- **Complete:** Resolved Checks with all previous issues confirmed fixed
- **Complete:** Phrases like "No remaining findings" or "All issues resolved"
- **Continue:** Bug/Security/Key Issues sections present → Proceed to step 4

### 4. Fix Identified Issues

For each issue identified:

1. Locate the problematic code
2. Understand the issue
3. Apply the fix using Edit tool
4. Document what changed and why

**Best practices:**

- Fix all issues in a single iteration before re-reviewing
- Prioritize critical errors over warnings
- Explain each fix clearly to the user
- Preserve functionality while addressing issues

### 5. Run Follow-up Codex CLI Review

After applying fixes, run targeted review:

```bash
codex exec "Review the updated <file_name> code. Check if the previous issues have been fixed: 1) issue description, 2) issue description, etc. Report any remaining issues or confirm the code is now correct."
```

This helps Codex:

- Focus on whether specific issues were resolved
- Identify any new problems introduced
- Provide clear pass/fail confirmation

Analyze results:

- **All issues fixed:** Mark workflow complete, report success
- **Issues remain:** Determine whether to iterate (check limits)

### 6. Handle Iteration Limits

**Maximum iterations:** 2 review cycles (initial + 1 re-review)

**Why limit:**

- Prevents infinite loops
- Some issues require human judgment
- Complex problems need architectural changes

**When max reached:**

1. Mark current task status in TodoWrite
2. Summarize what was fixed and what remains
3. Show final Codex CLI output to user
4. Ask user whether to:
   - Continue with manual fixes
   - Adjust the approach
   - Accept current state

## Examples

### Example 1: Simple Fix Workflow

```
User: "Add a function to calculate fibonacci numbers and review it with Codex"

Claude:
1. Creates fibonacci function
2. Checks for git repo, runs git init if needed
3. Runs: codex exec "Review fibonacci.py for bugs, edge cases, and best practices."
4. Codex output:
   - **Bug** `fibonacci.py:5`: Missing input validation for negative numbers
   - **Maintainability** `fibonacci.py:10`: Consider adding type hints
5. Adds input validation and type hints
6. Runs: codex exec "Review updated fibonacci.py. Check if input validation added."
7. Codex output:
   **Resolved Checks**
   - `fibonacci.py:5` Input validation is now present
   - `fibonacci.py:10` Type hints added
8. Reports completion
```

### Example 2: Multiple Iterations (Security)

```
User: "Implement user authentication and run through Codex review"

Claude:
1. Implements auth system across multiple files
2. Runs: codex exec "Review auth.py, user.py, session.py for security vulnerabilities."
3. Codex output:
   - **Security** `auth.py:23`: Password stored without hashing
   - **Security** `session.py:45`: Session tokens don't expire
   - **Bug** `user.py:67`: SQL injection vulnerability
   - **Security** `auth.py:89`: Missing CSRF protection
   - **Bug** `user.py:12`: No input validation
4. Fixes all 5 issues
5. Runs targeted review: "Check if these issues are fixed: password hashing, session expiration, SQL injection, CSRF, input validation."
6. Codex output:
   **Resolved Checks**
   - All 5 issues confirmed fixed
   **Findings**
   - Minor style suggestions
7. Reached iteration limit (2 reviews)
8. Reports: "All critical security issues fixed. Minor style suggestions remain."
9. Asks user about style fixes
```

### Example 3: First-Pass Success

```
User: "Write a date formatter helper, review with Codex"

Claude:
1. Creates date formatting function with error handling
2. Runs: codex exec "Review utils/date_formatter.py for bugs, edge cases."
3. Codex output:
   No bugs or critical issues. Code properly handles:
   - None values with error messages
   - Invalid format strings
   - Timezone conversions
   **Suggestions**
   - Could add more detailed error messages
4. Reviews suggestion, decides optional for current use case
5. Marks task complete
```

## Integration Notes

### Codex CLI Commands

```bash
# Basic review
codex exec "Review <file_name> for bugs, security issues, best practices. Provide specific feedback with line numbers."

# With working directory
codex exec "Review <file_name>..." -C /path/to/project

# With specific model
codex exec "Review <file_name>..." -m gpt-5-codex

# Skip git check (not recommended)
codex exec "Review <file_name>..." --skip-git-repo-check
```

### Git Repository Requirement

```bash
# Check if in git repo
git status

# Initialize if needed
git init

# Alternative: skip check
codex exec "..." --skip-git-repo-check
```

## Error Handling

**Codex CLI not found:**

- Check: `which codex` or `codex --version`
- Inform user Codex CLI unavailable
- Offer to complete task without automated review

**Git repository error:**

- Error: "Not inside trusted directory and --skip-git-repo-check not specified"
- Solution: Run `git init`
- Alternative: Add `--skip-git-repo-check`

**Codex CLI errors:**

- Common errors:
  - `unexpected argument` - Check syntax, use `codex exec` not `codex review`
  - Authentication errors - User may need `codex login`
- Attempt once more with corrected parameters
- If persistent, ask user for guidance

**Ambiguous results:**

- If unsure about pass/fail, err on side of caution
- Look for "Key Issues" vs "Suggestions" sections
- Show output to user and ask for clarification

**Long-running reviews:**

- Codex may take 30-120 seconds for complex reviews
- Use appropriate timeout (120000ms recommended)

## Best Practices

1. **Always use TodoWrite** for workflow step tracking
2. **Show Codex output** at each review stage
3. **Explain fixes clearly** - avoid silent fixes
4. **Respect iteration limits** - avoid infinite loops
5. **Preserve functionality** - address issues without breaking features
6. **Ask when uncertain** - consult user when feedback is ambiguous

## Customization Options

- Adjust iteration limits (default: 2 reviews)
- Specify custom Codex CLI commands
- Provide configuration file for Codex rules
- Define files to include/exclude from review
- Set severity thresholds (errors only vs warnings)

## Related Skills

- **testing-strategist**: For creating test suites to complement code review
- **security-engineer**: For manual security reviews and threat modeling
- **quality-auditor**: For comprehensive quality assessments
- **technical-writer**: For documenting review findings and improvements

## Tools & Dependencies

**Required:**

- Codex CLI (OpenAI)
- Git (for repository context)

**Recommended:**

- TodoWrite tool (progress tracking)
- Edit tool (applying fixes)

## Tips for Success

1. **Write good initial code** - Better starting point = fewer iterations
2. **Be specific in review prompts** - "Check for SQL injection in login function" vs "Review this"
3. **Group related files** - Review auth system as a whole, not file-by-file
4. **Fix all issues at once** - More efficient than fixing one at a time
5. **Use targeted follow-up prompts** - Ask about specific fixes, not general review
6. **Know when to stop** - Some issues require human judgment or architectural changes

---

**Skill Type:** Automation
**Difficulty:** Intermediate
**Estimated Time:** Varies by task (review: 1-2min, fixes: 5-30min per iteration)
**Integration:** Codex CLI, Git
