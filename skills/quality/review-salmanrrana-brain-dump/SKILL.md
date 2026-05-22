---
name: review
description: Run the complete code review pipeline on recent changes. Launches three review agents in parallel to check code quality, error handling, and simplification opportunities.
---

# Code Review Pipeline

You are running the automatic code review pipeline for Brain Dump. This pipeline ensures code quality by running three specialized review agents in parallel.

## Your Task

1. First, identify what files were recently changed by checking `git diff --name-only` or looking at the conversation history for Write/Edit tool usage.

2. Launch ALL THREE review agents in PARALLEL using a single message with multiple Task tool calls:

```
Task 1: pr-review-toolkit:code-reviewer
- Review the recent code changes against project guidelines in CLAUDE.md
- Check for style violations, potential bugs, and adherence to patterns

Task 2: pr-review-toolkit:silent-failure-hunter
- Check for silent failures, inadequate error handling
- Look for empty catch blocks, swallowed errors, missing error messages

Task 3: pr-review-toolkit:code-simplifier
- Analyze for simplification opportunities
- Look for duplicated code, overly complex logic, unnecessary abstractions
```

3. Wait for all three agents to complete.

4. Summarize the findings in a clear format:
   - **Critical Issues**: Must fix before merging
   - **Important Issues**: Should fix, but not blocking
   - **Suggestions**: Nice to have improvements

5. If there are critical issues, offer to fix them.

6. After completing the review, mark it as done by running:
   ```bash
   touch "$CLAUDE_PROJECT_DIR/.claude/.review-completed" 2>/dev/null || touch .claude/.review-completed
   ```

## Important

- Run all three agents in PARALLEL (single message, multiple Task calls)
- Focus on recently modified files only
- Be concise in your summary - the user has access to the full agent outputs
- Always mark review as completed at the end to prevent re-triggering
