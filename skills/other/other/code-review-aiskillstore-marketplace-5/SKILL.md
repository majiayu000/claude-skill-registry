---
name: code-review
description: Automated PR code review with multi-agent analysis
version: 0.1.0-beta
license: MIT
compatibility: opencode
---

Provide a code review for the given pull request.

## Prerequisites

- [GitHub CLI](https://cli.github.com/) installed and authenticated
- `github-pr` skill installed (bundled automatically)
- AGENTS.md files in your repository (optional but recommended)

## Slash Command

### `/code-review [--comment]`

Performs automated code review on a pull request using multiple specialized agents.

**Options:**
- `--comment` - Post the review as inline comments on the PR (default: outputs to terminal only)

**Example:**
```bash
/code-review           # Output to terminal
/code-review --comment # Post as PR comments
```

## Workflow

Follow these steps precisely:

### Step 1: Pre-check

Check if any of the following are true:
- The pull request is closed
- The pull request is a draft
- The pull request does not need code review (e.g. automated PR, trivial change)
- Claude/AI has already commented on this PR

Run the check script:

```bash
bun .opencode/skill/github-pr/check-review-needed.js
```

If `shouldReview` is `false`, stop and do not proceed.

**Note:** Still review Claude/AI-generated PRs - only skip if Claude has already commented on the PR.

### Step 2: Gather Guidelines

Run the guideline discovery script:

```bash
bun .opencode/skill/github-pr/list-guideline-files.js --json
```

This returns file paths (not contents) for relevant AGENTS.md files:
- Root AGENTS.md file, if it exists
- AGENTS.md files in directories containing files modified by the PR

For each guideline file found, fetch its contents to use in compliance checking.

### Step 3: Summarize PR

Launch a haiku agent to view the PR and return a summary including:
- PR title and description
- List of changed files with brief descriptions
- Overall nature of the changes

Use the Task tool with a haiku agent.

### Step 4: Parallel Review

Launch 4 agents in parallel to independently review the changes. Each agent should return a list of issues with:
- Description of the issue
- Reason it was flagged (e.g., "AGENTS.md compliance", "bug", "logic error")
- File path and line number(s)
- Confidence score (0-100)

Provide each agent with the PR title, description, and summary from Step 3.

#### Agents 1 & 2: AGENTS.md Compliance (Sonnet)

Audit changes for AGENTS.md compliance in parallel. When evaluating compliance:
- Only consider AGENTS.md files that share a file path with the file being reviewed (or its parent directories)
- Verify the guideline explicitly mentions the rule being violated
- Quote the exact rule from AGENTS.md in the issue description

#### Agent 3: Bug Detection (Opus)

Scan for obvious bugs. Focus only on the diff itself without reading extra context:
- Flag only significant bugs that will cause incorrect behavior
- Ignore nitpicks and likely false positives
- Do not flag issues that cannot be validated from the diff alone

#### Agent 4: Logic Analysis (Opus)

Look for problems that exist in the introduced code:
- Security issues
- Incorrect logic
- Race conditions
- Resource leaks

Only flag issues within the changed code.

**CRITICAL: HIGH SIGNAL ONLY**

We want:
- Objective bugs that will cause incorrect behavior at runtime
- Clear, unambiguous AGENTS.md violations where you can quote the exact rule being broken

We do NOT want:
- Subjective concerns or "suggestions"
- Style preferences not explicitly required in AGENTS.md
- Potential issues that "might" be problems
- Anything requiring interpretation or judgment calls

If you are not certain an issue is real, do not flag it. False positives erode trust and waste reviewer time.

### Step 5: Validate Issues

For each issue found in Step 4, launch parallel subagents to validate the issue.

The validator receives:
- PR title and description
- Issue description and location
- Relevant code context

The validator's job is to confirm:
- The issue is real and verifiable
- For AGENTS.md issues: the rule exists and applies to this file
- The issue was introduced in this PR (not pre-existing)

**Agent types:**
- Use Opus subagents for bugs and logic issues
- Use Sonnet agents for AGENTS.md violations

### Step 6: Filter Results

Filter out any issues that were not validated in Step 5. This gives our list of high signal issues for review.

### Step 7: Confirm and Post Results

**If no issues were found:** Output "No issues found" to the terminal. Do not post any comment to the PR.

**If issues were found and `--comment` flag is provided:**

Present a summary to the user for confirmation:

```
## Code Review Summary

Found {N} issue(s):

1. **{file}:{line}** - {brief description}
2. **{file}:{line}** - {brief description}
...

Post these as inline comments to PR #{number}? (y/n)
```

**If user confirms (y):** Post inline comments using:

```bash
bun .opencode/skill/github-pr/post-inline-comment.js <pr-number> \
  --path <file> \
  --line <line> \
  [--start-line <start>] \
  --body "<comment>"
```

**If user declines (n):** Do not post comments. The review output remains in the terminal.

**If `--comment` flag is NOT provided:** Output the review to terminal only, do not prompt for confirmation.

**Comment format:**

For small fixes (up to 5 lines changed), include a suggestion:

```markdown
Brief description of the issue (no "Bug:" prefix)

```suggestion
corrected code here
```
```

**Suggestions must be COMPLETE.** If a fix requires additional changes elsewhere (e.g., renaming a variable requires updating all usages), do NOT use a suggestion block. The author should be able to click "Commit suggestion" and have a working fix - no followup work required.

For larger fixes (6+ lines, structural changes, or changes spanning multiple locations), do NOT use suggestion blocks. Instead:
1. Describe what the issue is
2. Explain the suggested fix at a high level
3. Include a copyable prompt for Claude Code that the user can use to fix the issue, formatted as:
   ```
   Fix [file:line]: [brief description of issue and suggested fix]
   ```

**IMPORTANT:** Only post ONE comment per unique issue. Do not post duplicate comments.

## False Positives (Do NOT Flag)

Use this list when evaluating issues in Steps 4 and 5:

- Pre-existing issues
- Something that appears to be a bug but is actually correct
- Pedantic nitpicks that a senior engineer would not flag
- Issues that a linter will catch (do not run the linter to verify)
- General code quality concerns (e.g., lack of test coverage, general security issues) unless explicitly required in AGENTS.md
- Issues mentioned in AGENTS.md but explicitly silenced in the code (e.g., via a lint ignore comment)

## Code Link Format

When linking to code in inline comments, follow this exact format precisely, otherwise the Markdown preview won't render correctly:

```
https://github.com/owner/repo/blob/[full-sha]/path/file.ext#L[start]-L[end]
```

Requirements:
- Must use full git SHA (not abbreviated)
- Repo name must match the repo you're code reviewing
- `#L` notation for line range
- Line range format: `L[start]-L[end]`
- Provide at least 1 line of context before and after

## Confidence Scoring

Each issue is scored 0-100:

| Score | Meaning |
|-------|---------|
| 0 | Not confident, false positive |
| 25 | Somewhat confident, might be real |
| 50 | Moderately confident, real but minor |
| 75 | Highly confident, real and important |
| 100 | Absolutely certain, definitely real |

Only issues scoring **80 or higher** are reported.
