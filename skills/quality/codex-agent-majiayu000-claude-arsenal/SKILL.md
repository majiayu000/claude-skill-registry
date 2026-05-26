---
name: codex-agent
description: MANDATORY for code review - must use Codex CLI for all code reviews, then apply fixes based on Codex feedback. Also use for cross-verification, debugging, and getting alternative implementations.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Codex Agent Collaboration Skill

This skill enables Claude Code to collaborate with OpenAI's Codex CLI agent.

## MANDATORY: Code Review Workflow

**IMPORTANT**: When performing code review, you MUST follow this workflow:

### Step 1: Call Codex for Review

```bash
codex exec -C <project_path> -s read-only -o /tmp/codex-review.md \
  "Review the code in <file_or_directory>. Check for:
   - Security vulnerabilities
   - Performance issues
   - Code quality and best practices
   - Potential bugs and edge cases
   - Naming and readability
   Provide specific, actionable feedback with file paths and line numbers."
```

### Step 2: Read Codex Feedback

```bash
cat /tmp/codex-review.md
```

### Step 3: Apply Fixes Based on Codex Feedback

For each issue identified by Codex:
1. Read the relevant file
2. Apply the fix using Edit tool
3. Verify the fix addresses Codex's concern

### Step 4: Re-verify with Codex (Optional)

```bash
codex exec -C <project_path> -s read-only \
  "Verify the fixes applied to <files>. Confirm issues are resolved."
```

## Workflow Examples

### Example 1: Review and Fix a Single File

```bash
# Step 1: Get Codex review
codex exec -C /project -s read-only -o /tmp/codex-review.md \
  "Review src/auth/login.ts for security vulnerabilities and code quality issues. Provide specific line numbers and fixes."

# Step 2: Read the feedback
cat /tmp/codex-review.md
```

Then Claude reads the feedback, applies fixes with Edit tool, and optionally re-verifies.

### Example 2: Review Recent Changes

```bash
# Get diff of recent changes
git diff HEAD~1 > /tmp/recent-changes.diff

# Step 1: Have Codex review the diff
codex exec -C /project -s read-only -o /tmp/codex-review.md \
  "Review the changes in the last commit. Check for bugs, security issues, and improvements needed."

# Step 2: Read and apply fixes
cat /tmp/codex-review.md
```

### Example 3: Full Project Review

```bash
# Step 1: Comprehensive review
codex exec -C /project -s read-only -o /tmp/codex-review.md \
  "Perform a comprehensive code review of src/. Focus on:
   1. Security vulnerabilities (OWASP Top 10)
   2. Error handling patterns
   3. Performance bottlenecks
   4. Code duplication
   Prioritize issues by severity (critical/high/medium/low)."

# Step 2: Read prioritized feedback
cat /tmp/codex-review.md
```

## Review Request Format

When asking Codex for review, include:

```
Review <target_files_or_directory>.

Context:
- Project type: <TypeScript/Python/etc>
- Framework: <Express/React/etc>
- Focus areas: <security/performance/quality>

Check for:
1. Security vulnerabilities
2. Performance issues
3. Error handling
4. Code quality
5. Edge cases

Output format:
For each issue:
- File: <path>
- Line: <number>
- Severity: critical/high/medium/low
- Issue: <description>
- Fix: <specific code change>
```

## Applying Fixes

After receiving Codex feedback, apply fixes systematically:

1. **Parse the review** - Extract each issue with file, line, severity
2. **Prioritize** - Fix critical/high issues first
3. **Read file** - Use Read tool to see current code
4. **Apply fix** - Use Edit tool with precise old_string/new_string
5. **Track progress** - Mark each issue as fixed

## Prerequisites

Codex CLI must be installed and authenticated:

```bash
# Install via npm
npm install -g @openai/codex

# Or via Homebrew (macOS)
brew install --cask codex

# Authenticate
codex login
```

## Command Reference

### Basic Command Pattern

```bash
codex exec [options] "<task_description>"
```

### Core Options

| Option | Description |
|--------|-------------|
| `"<task>"` | Task description (positional, must be quoted) |
| `-C <dir>` | Working directory (use absolute path) |
| `-s read-only` | Read-only sandbox (use for reviews) |
| `-o <path>` | Save output to file |
| `--json` | Output as JSON Lines |

### AI-to-AI Communication

When communicating with Codex, PRIORITIZE ACCURACY AND PRECISION:
- Use structured data and exact technical terms
- Provide full file paths and precise details
- Include relevant context from the current codebase
- NO conversational formatting needed

## Other Use Cases

### Cross-Verification (after Claude implements)

```bash
codex exec -C /project -s read-only \
  "Verify the implementation in src/feature/. Check correctness and edge cases."
```

### Get Alternative Implementation

```bash
codex exec -C /project -s read-only -o /tmp/alternative.md \
  "Propose an alternative implementation for the caching in src/cache/manager.ts"
```

### Debugging Assistance

```bash
codex exec -C /project -s read-only \
  "Debug: tests in tests/auth.test.ts failing with timeout. Analyze root cause."
```

## Session Management

For multi-turn reviews:

```bash
# Initial review
codex exec -C /project -s read-only "Review src/api/ for security issues"
# Note session ID from output

# Follow-up after fixes
codex exec resume <session_id> "I've applied the fixes. Please re-verify."
```

## Troubleshooting

### Authentication Issues

```bash
codex logout
codex login
```

### Check Installation

```bash
codex --version
which codex
```

## See Also

- [sandbox-modes.md](sandbox-modes.md) - Sandbox security levels
- [examples.md](examples.md) - More usage examples
- [advanced.md](advanced.md) - Advanced configuration
