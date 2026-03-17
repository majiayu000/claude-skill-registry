---
name: review
description: Perform a code review on recent changes
---

# /review - Code Review Workflow

## Purpose

Performs a comprehensive code review of changes in the current branch compared to main. This skill combines:
1. **CodeRabbit AI Review** - Automated AI-powered code analysis
2. **Manual Review** - Claude's targeted review of Swift 6.0 compliance, accessibility, and testing

## Usage

```
/review              # Full review: CodeRabbit + manual review
/review staged       # Review only staged changes
/review <file>       # Review specific file (manual only)
/review --quick      # Quick review (CodeRabbit only)
/review --manual     # Skip CodeRabbit, manual review only
```

## Workflow

### 1. Run CodeRabbit Automated Review

Always start with CodeRabbit for comprehensive AI analysis:

```bash
# For uncommitted changes (most common)
/Users/ramerman/.local/bin/coderabbit review --prompt-only --type uncommitted

# For committed changes not yet merged
/Users/ramerman/.local/bin/coderabbit review --prompt-only --type committed

# For all changes
/Users/ramerman/.local/bin/coderabbit review --prompt-only
```

CodeRabbit provides:
- File-by-file analysis with line numbers
- Issue severity classification (potential_issue, nitpick, refactor_suggestion)
- AI agent prompts for automated fixes
- Security and performance issue detection

### 2. Fix Critical CodeRabbit Issues

Address issues marked as `potential_issue` before proceeding:
- These are bugs, security issues, or incorrect behavior
- Use the provided "Prompt for AI Agent" as guidance
- Run CodeRabbit again after fixes to verify

### 3. Manual Review Checklist

After CodeRabbit, perform manual checks for project-specific requirements:

#### Swift 6.0 Concurrency Compliance
- `@MainActor` annotations on UI code
- Actor-based services for shared state
- `@Sendable` types for cross-actor boundaries
- No data races or concurrency warnings
- Proper async/await usage

#### Code Quality
- No force unwraps (`!`) - use `guard`/`if-let`
- Comprehensive error handling
- Meaningful variable and function names
- Functions under 50 lines where possible
- No magic numbers or hardcoded strings
- Proper use of access control (`private`, `internal`, `public`)

#### Testing Requirements
- Test coverage for new code
- Tests follow "Real Over Mock" philosophy
- Descriptive test names: `test<Feature>_<Scenario>_<Expected>`
- Edge cases covered
- Integration tests for complex flows

#### iOS Standards
- Accessibility labels on all interactive elements
- `LocalizedStringKey` for user-facing text
- Adherence to `docs/ios/IOS_STYLE_GUIDE.md`
- Proper memory management (no retain cycles)
- SwiftUI best practices

### 4. Generate Report

Combine CodeRabbit findings with manual review:

**CodeRabbit Issues**
- Count of potential_issue items
- Count of nitpicks
- Count of refactor_suggestions

**Manual Review**
- Critical Issues (must fix)
- Suggestions (nice to have)
- Positive Notes (well-done aspects)

## Success Criteria

- All CodeRabbit `potential_issue` items addressed
- All manual critical issues identified and fixed
- Clear, actionable feedback provided
- `/validate` passes after all fixes

## Examples

**Full review with CodeRabbit:**
```
User: /review
Claude: Running CodeRabbit review on uncommitted changes...

[CodeRabbit Output]
============================================================================
File: UnaMentis/Core/Audio/AudioSegmentCache.swift
Line: 61 to 70
Type: potential_issue

Prompt for AI Agent: Fix cache size calculation...
============================================================================

CodeRabbit found:
- 2 potential_issue items
- 5 nitpicks
- 3 refactor_suggestions

Fixing potential issues first...
[Makes fixes]

Running manual review checklist...

## Summary
- CodeRabbit issues fixed: 2
- Nitpicks addressed: 3 (2 skipped as minor)
- Manual issues found: 0
- Status: READY FOR COMMIT
```

**Quick review (CodeRabbit only):**
```
User: /review --quick
Claude: Running quick CodeRabbit review...

Found 2 potential issues:
1. AudioSegmentCache.swift:61 - Cache size calculation bug
2. SessionView.swift:2134 - AVAudioPlayer retention issue

Run `/review` for full analysis including manual checks.
```

## CodeRabbit Authentication

If CodeRabbit is not authenticated:
```bash
/Users/ramerman/.local/bin/coderabbit auth login
```

Follow the prompts to authenticate via browser.

## Integration

This skill should be run:
- After completing any feature implementation
- Before creating a pull request
- After `/validate` passes
- When reviewing changes

The workflow is: Code -> `/validate` -> `/review` -> Fix issues -> Commit
