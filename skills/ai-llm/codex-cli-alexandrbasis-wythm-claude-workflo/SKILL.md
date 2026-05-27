---
name: codex-cli
description: Invoke OpenAI Codex CLI for second-opinion code review, approach validation, and task verification. Use when you need cross-AI validation, a fresh perspective on implementation, or automated code review. Takes 1-10 minutes per request.
allowed-tools:
  - Bash
  - Read
---

# Codex CLI Integration Skill

This skill enables Claude Code to invoke OpenAI Codex CLI (gpt-5.3-codex with high reasoning) for one-shot code review, approach validation, and cross-AI verification.

## When to Use This Skill

### Ideal Use Cases

1. **Second Opinion / Cross-Validation**
   - Verify your implementation approach before writing code
   - Get a different AI perspective on your solution
   - Validate architectural decisions

2. **Code Review**
   - Review uncommitted changes before commit
   - Review changes against a base branch before PR
   - Security-focused code review

3. **Task Verification**
   - Confirm implementation meets requirements
   - Validate that refactoring preserved behavior
   - Check for missed edge cases

4. **Approach Validation**
   - Before starting complex implementation
   - When choosing between multiple approaches
   - For architectural decisions

### When NOT to Use

- Simple, quick tasks (overhead not worth 1-10 min wait)
- Tasks requiring interactive conversation/refinement
- When immediate response is critical
- Trivial changes (typos, formatting)

## Core Commands

### Approach Validation
```bash
codex exec "Review this approach: [description]. Is it sound? What are the tradeoffs?" -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1 && echo "Codex completed"
# Then: Read tool /tmp/codex-result.md
```

### Code Review - Uncommitted Changes
```bash
codex exec review --uncommitted -m gpt-5.3-codex --full-auto > /tmp/codex-review.md 2>&1
# Then: Read tool /tmp/codex-review.md
```

### Code Review - Against Branch
```bash
codex exec review --base main -m gpt-5.3-codex --full-auto > /tmp/codex-review.md 2>&1
# Then: Read tool /tmp/codex-review.md
```

### Custom Analysis
```bash
codex exec "[prompt]" -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1 && echo "Codex completed"
# Then: Read tool /tmp/codex-result.md
```

## Important Notes

1. **One-Shot Only**: Codex runs non-interactively. No follow-up questions possible.

2. **Takes Time**: Expect 1-10 minutes depending on complexity. Use `run_in_background` for long tasks.

3. **Model**: Always use `-m gpt-5.3-codex` for explicit model selection.

4. **Full Auto**: `--full-auto` enables workspace-write sandbox with auto-approval.

5. **Output File**: Use `-o /tmp/codex-result.md` to capture just the final response.

6. **CRITICAL - Token Optimization**: Always redirect stdout to `/dev/null` and read from file. See "Output Handling" below.

## Output Handling Best Practice

**Why this matters:** Without optimization, Bash returns ~4700+ tokens of verbose output (reasoning steps, tool calls, MCP logs). With optimization, you get ~30 tokens + clean file read.

### For `codex exec` (custom prompts)
```bash
# Run with output file + suppress verbose stdout
codex exec "prompt" -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1 && echo "Codex completed"
```
Then read result with **Read tool** (not cat): `/tmp/codex-result.md`

### For `codex exec review` (no -o flag support)
```bash
# Redirect all output to file
codex exec review --uncommitted -m gpt-5.3-codex --full-auto > /tmp/codex-review.md 2>&1
```
Then read result with **Read tool**: `/tmp/codex-review.md`

### Workflow
1. Run codex command with output redirection
2. **Read result file** with Read tool (not Bash cat)
3. Summarize findings to user

## Critical: Provide File Paths in Prompts

**Codex has NO context from Claude Code conversation.** Always include explicit file paths in your prompts:

### For Task Review
```bash
codex exec "Review the task specification at tasks/task-2026-01-09-feature/tech-decomposition.md
Is the implementation plan complete? Any gaps or risks?" -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1
# Read: /tmp/codex-result.md
```

### For Code Review with Context
```bash
codex exec "Review implementation in these files:
- backend/src/application/sessions/use-cases/create-session.use-case.ts
- backend/src/infrastructure/web/dto/sessions/create-session.dto.ts

Check against requirements in: tasks/task-2026-01-09-feature/tech-decomposition.md" -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1
# Read: /tmp/codex-result.md
```

### For Approach Validation
```bash
codex exec "I'm implementing the feature described in tasks/task-2026-01-09-feature/tech-decomposition.md

My approach:
1. [Step 1]
2. [Step 2]

Is this aligned with the requirements?" -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1
# Read: /tmp/codex-result.md
```

### Best Practice
Always include:
- **Task file path** - so Codex knows the requirements
- **Implementation file paths** - so Codex knows what to review
- **Directory path** - for broader context (e.g., `backend/src/application/sessions/`)

## Background Execution Pattern

For tasks that take longer, run in background:

```bash
# Run in background using Bash tool with run_in_background=true
codex exec "[complex prompt]" -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1 && echo "Codex completed"
```

Then read result with **Read tool**: `/tmp/codex-result.md`

## Example Workflows

### Pre-Implementation Validation
```bash
codex exec "I'm about to implement [feature] using [approach].
Review this plan:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Is this approach sound? What issues might I encounter?" -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1
# Read: /tmp/codex-result.md
```

### Security Review
```bash
# Built-in review command (redirect to file)
codex exec review --uncommitted -m gpt-5.3-codex --full-auto > /tmp/codex-review.md 2>&1
# Read: /tmp/codex-review.md

# Or with custom focus:
codex exec "Review the uncommitted changes for security vulnerabilities including XSS, injection, auth issues" -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1
# Read: /tmp/codex-result.md
```

### Cross-AI Verification
```bash
codex exec "I implemented [feature]. The key files are:
- path/to/file1.ts
- path/to/file2.ts

Verify the implementation is correct and complete." -m gpt-5.3-codex --full-auto -o /tmp/codex-result.md > /dev/null 2>&1

## What's New in Codex CLI 0.96.0

Highlights from the latest CLI release:
- `unified_exec` enabled on non-Windows platforms for smoother exec flows.
- Websocket rate-limit signaling via the new `codex.rate_limits` event.
- `thread/compact` available in the v2 app-server API with async behavior and status tracking.

Source: https://developers.openai.com/codex/changelog
# Read: /tmp/codex-result.md
```

## See Also

- `templates.md` - Prompt templates for common operations
- `reference.md` - Complete command and flag reference
