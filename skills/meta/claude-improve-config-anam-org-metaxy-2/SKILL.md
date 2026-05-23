---
name: claude-improve-config
description: Self-reflect on the current session to identify mistakes and propose improvements to .claude configuration (CLAUDE.md, hooks, skills).
---

# Claude Config Self-Improvement

Analyze the current session for errors, mistakes, or inefficiencies and propose improvements to the `.claude` configuration to prevent similar issues in the future.

## When to Use

- After a session with significant mistakes or rework
- When you notice patterns that could be prevented with better configuration
- When explicitly requested via `/claude-improve-config`
- Automatically triggered by the `SessionEnd` hook

## Self-Reflection Process

### 1. Analyze the Session

Review the conversation for:

- **Repeated mistakes**: Same error made multiple times
- **Misunderstandings**: User had to correct Claude's interpretation
- **Inefficient workflows**: Better approaches discovered late in the session
- **Tool misuse**: Wrong tool for the job, excessive tool calls
- **Missing context**: Information that would have helped if in CLAUDE.md
- **Ignored instructions**: Existing CLAUDE.md rules that were violated

### 2. Categorize Issues

Rate severity:

- **Critical**: Caused significant rework or user frustration
- **Moderate**: Caused delays or minor corrections needed
- **Minor**: Slight inefficiency but didn't impact outcome

Only propose changes for **critical** or **moderate** issues.

### 3. Propose Configuration Changes

Changes can include:

**CLAUDE.md Updates:**

- New guardrails or constraints
- Clarified existing instructions
- Project-specific patterns to follow

**New Hooks:**

- PreToolUse hooks to prevent specific mistakes
- PostToolUse hooks to validate outputs
- Stop hooks to enforce checks before completion

**New Skills:**

- Reusable knowledge for recurring tasks
- Best practices for specific domains

### 4. Format the Proposal

Present proposals clearly:

```markdown
## Session Reflection

### Issues Identified

1. **[Critical/Moderate]** Brief description of the issue
   - What happened: ...
   - Why it happened: ...
   - Impact: ...

### Proposed Changes

#### Change 1: [Type - CLAUDE.md/Hook/Skill]

**Rationale:** Why this change prevents the issue

**Implementation:**
[Show the exact changes to make]

#### Change 2: ...
```

## Guidelines

- Only propose changes that are **generalizable** - don't add rules for one-off situations
- Keep CLAUDE.md **concise** - prefer hooks for enforcement over verbose instructions
- Test proposed hooks mentally - ensure they won't block legitimate workflows
- Prefer **minimal changes** - one well-designed rule is better than many narrow ones
- Consider **false positives** - hooks should not create friction for normal operations

## Example Proposals

### Example 1: Missing Test Verification

**Issue:** Claude claimed tests passed without running them.

**Proposal:** Add to CLAUDE.md:

```markdown
**Test verification**: Never claim tests pass without showing actual test output. Always run `uv run pytest` with the specific test file before marking test-related tasks complete.
```

### Example 2: Repeated Lint Failures

**Issue:** Code was submitted with lint errors multiple times.

**Proposal:** Add PostToolUse hook for Write/Edit:

```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": "ruff check --select=E,F $TOOL_INPUT.file_path 2>/dev/null || true"
    }
  ]
}
```

### Example 3: Wrong Branch for PR

**Issue:** PR was created against wrong base branch.

**Proposal:** Add to CLAUDE.md:

```markdown
**Pull requests**: Always verify the target branch before creating a PR. For this project, PRs should target `main` unless explicitly specified otherwise.
```

## Non-Examples (Do NOT Propose)

- One-off mistakes that won't recur
- User preference differences (not errors)
- Issues already covered by existing configuration
- Overly specific rules that won't generalize
- Changes that would slow down normal workflows significantly
