---
name: reviewing-code
description: Use this skill when reviewing pull requests, branch changes, or code diffs. Triggers on "review this PR", "review my changes", "code review", "review branch", or when user shares a GitHub PR URL.
---

# Code Review Skill

Review PR and branch changes with focus on quality, tests, complexity, and performance.

## Review Philosophy

This review focuses on substantive issues that matter:
- **NOT linting**: Skip formatting, import order, naming conventions (linters handle these)
- **Completeness**: Is the implementation complete? Any TODOs or partial implementations?
- **Tests**: Are tests added? Are they meaningful and cover edge cases?
- **Complexity**: Does this increase codebase complexity without justification?
- **Performance**: Any regressions in hot paths or resource-intensive code?
- **Duplication**: Is similar code already in the codebase?
- **Side effects**: Any unintended consequences from these changes?

## Multi-Model Review (Optional)

This skill can leverage additional AI models for more comprehensive reviews. It automatically detects and uses available CLI tools, running them in parallel for speed.

### Supported Tools

| Tool | Command | Description |
|------|---------|-------------|
| Gemini | `gemini` | Uses gemini-2.5-pro for additional code analysis |
| Codex | `codex review` | Uses OpenAI's Codex with dedicated review mode |

### Step 0: Detect and Run External Reviews

Before starting the main review, check for available tools and run them **synchronously** (background jobs don't work reliably in Claude's Bash tool due to PID issues with temp files):

```bash
# Detect available tools
command -v gemini >/dev/null 2>&1 && echo "Gemini available" || echo "Gemini not available"
command -v codex >/dev/null 2>&1 && echo "Codex available" || echo "Codex not available"
```

**IMPORTANT**: Run external reviews synchronously, not in the background. The `$$` variable doesn't work correctly across separate Bash tool invocations.

**For PR reviews:**
```bash
# Gemini review (run synchronously with timeout)
gh pr diff PR_NUMBER | timeout 120 gemini -p "$(cat <<'PROMPT'
Review this code diff for a PR. Focus on:
- Bugs and logic errors
- Missing error handling
- Test coverage gaps
- Performance issues
- Security concerns

Format your response as markdown with these sections:
## Critical Issues
## Important Suggestions
## Minor Notes

Be specific with file paths and line numbers where possible.
PROMPT
)"
```

```bash
# Codex review (if available, run separately)
codex review --base BASE_BRANCH
```

**For uncommitted changes:**
```bash
git diff | timeout 120 gemini -p "Review this code diff. Focus on bugs, missing error handling, test coverage gaps, performance issues, and security concerns. Format as markdown with Critical Issues, Important Suggestions, and Minor Notes sections."
```

**For branch changes:**
```bash
git diff origin/master...HEAD | timeout 120 gemini -p "Review this code diff. Focus on bugs, missing error handling, test coverage gaps, performance issues, and security concerns. Format as markdown with Critical Issues, Important Suggestions, and Minor Notes sections."
```

**Alternative: Use temp files with fixed names (if you want to capture output):**
```bash
# Use fixed temp file names instead of $$
git diff origin/master...HEAD | gemini -p "Review this diff..." > /tmp/claude-gemini-review.md 2>&1

# Later, read the output
cat /tmp/claude-gemini-review.md

# Clean up when done
rm -f /tmp/claude-gemini-review.md /tmp/claude-codex-review.md
```

### Fallback Behavior

| Available Tools | Behavior |
|----------------|----------|
| Gemini + Codex | Full multi-model synthesis |
| Gemini only | Gemini + Claude synthesis |
| Codex only | Codex + Claude synthesis |
| Neither | Standard Claude-only review |

## Workflow

### Step 1: Identify Changes to Review

**If given a PR URL:**
```bash
# Extract PR info
gh pr view PR_NUMBER --json title,body,additions,deletions,files

# Get the diff
gh pr diff PR_NUMBER
```

**If reviewing current branch:**
```bash
# Find the base branch
git log --oneline -1 origin/master

# Show what will be in the PR
git diff origin/master...HEAD --stat
git diff origin/master...HEAD
```

**If reviewing uncommitted changes:**
```bash
git diff --stat
git diff
```

### Step 2: Gather Context

Before reviewing, understand the intent:
1. Read the PR description or commit messages
2. Check for linked issues or documentation
3. Look for project-specific guidelines:
   ```bash
   # Check for project CLAUDE.md or AGENTS.md
   cat CLAUDE.md 2>/dev/null || cat AGENTS.md 2>/dev/null || echo "No project guidelines found"
   ```

### Step 3: Review the Changes

For each file changed, evaluate these key areas:

1. **Implementation Completeness**
   - Are all code paths handled?
   - Any placeholder or stub code left behind?
   - Do error messages make sense?

2. **Test Quality**
   - Are tests added for new functionality?
   - Do tests verify behavior, not just coverage?
   - Are edge cases tested?
   - Would these tests catch a regression?

3. **Complexity Impact**
   - Does this add new abstractions? Are they justified?
   - Is there a simpler way to achieve the same goal?
   - Does it follow existing patterns in the codebase?

4. **Performance Considerations**
   - Any new loops over large datasets?
   - Unnecessary memory allocations in hot paths?
   - I/O operations that could be batched?

5. **Duplication Check**
   - Search for similar existing code:
     ```bash
     # Look for similar function names or patterns
     rg "similar_function_name" --type py
     ```

### Step 3.5: Synthesize Multi-Model Reviews (If Available)

If external reviews were collected in Step 0, synthesize them with your findings:

1. **If you saved to temp files, read them:**
   ```bash
   # Check for Gemini review
   [ -f /tmp/claude-gemini-review.md ] && cat /tmp/claude-gemini-review.md

   # Check for Codex review
   [ -f /tmp/claude-codex-review.md ] && cat /tmp/claude-codex-review.md
   ```

2. **Cross-reference findings:**
   - Issues found by **multiple models** → Higher confidence, prioritize in "Must Address"
   - **Unique findings** from each model → Evaluate independently, include if valid
   - **Contradicting assessments** → Note the disagreement and provide your judgment

3. **Deduplicate and merge:**
   - Combine similar issues into single entries
   - Use the clearest explanation from any source
   - Add model agreement indicator where multiple models agree

4. **Clean up temp files:**
   ```bash
   rm -f /tmp/claude-gemini-review.md /tmp/claude-codex-review.md
   ```

### Step 4: Provide Feedback

Structure your review as:

```markdown
## Summary
[1-2 sentence overview of the changes and overall assessment]

## Models Used
[Only include if multi-model review was performed]
- Gemini (gemini-2.5-pro): ✓ / ✗
- Codex: ✓ / ✗

## Model Comparison
[Only include if 2+ models were used. Brief summary of how the reviews differed.]

| Aspect | Gemini | Codex | Claude |
|--------|--------|-------|--------|
| Focus | [e.g., Security-heavy] | [e.g., Performance-focused] | [e.g., Logic/completeness] |
| Severity | [e.g., Flagged 3 critical] | [e.g., Flagged 1 critical] | [e.g., Flagged 2 critical] |

**Key differences:**
- [Where models disagreed or had unique insights]
- [What one model caught that others missed]

**Consensus areas:**
- [Issues all models agreed on]

## Key Findings

### Must Address
1. **[Issue title]** (`file:line`) [Gemini + Codex + Claude]
   - Detail about the issue
   - Code example if helpful
   - **Risk**: Why this matters
   - **Consensus**: All models flagged this issue

2. **[Next issue title]** (`file:line`) [Claude]
   - Details...
   - **Risk**: Why this matters

### Should Consider
3. **[Issue title]** (`file:line`) [Gemini]
   - Details...

### Minor Notes
- [Observation]
- [Another observation]

## Tests
[Assessment of test coverage and quality]

## Complexity Assessment
[Does this increase or decrease overall codebase complexity?]
```

**IMPORTANT formatting rules:**
- Use a **single incrementing number sequence** across all sections (Must Address items 1-N, Should Consider continues from N+1, etc.)
- Use **bullet points (-)** for sub-details under each numbered finding, never restart numbering
- Each numbered finding should have a bold title followed by file:line reference in backticks
- Include a **Risk:** bullet point explaining why the issue matters
- **Model attribution**: Add `[Model names]` after the file reference to show which models identified the issue
  - `[Gemini + Codex + Claude]` - All three models agree (highest confidence)
  - `[Gemini + Claude]` or `[Codex + Claude]` - Two models agree
  - `[Claude]`, `[Gemini]`, or `[Codex]` - Single model finding

## Review Scope Guidelines

**In scope:**
- Logic errors and bugs
- Missing error handling for realistic failure modes
- Test coverage and test quality
- Performance regressions
- Unnecessary complexity
- Code duplication
- Incomplete implementations
- Violations of project guidelines (from CLAUDE.md/AGENTS.md)

**Out of scope (linter territory):**
- Code formatting
- Import ordering
- Variable naming style
- Type annotation style
- Docstring format

## Example Review

**User**: "Review my changes on this branch"

**Claude**:
1. Detects available tools (Gemini, Codex)
2. Runs `git diff origin/master...HEAD --stat` to see scope
3. Kicks off Gemini and Codex reviews in parallel (if available)
4. Runs `git diff origin/master...HEAD` to get full diff
5. Checks for project guidelines
6. Reviews each changed file
7. Reads external review outputs and synthesizes findings
8. Cross-references issues across models, prioritizing consensus
9. Provides structured feedback with model attribution

## Notes

- Always read the full diff before providing feedback
- Check commit messages for context on why changes were made
- When in doubt about intent, ask before assuming something is wrong
- Prioritize actionable feedback over stylistic preferences
