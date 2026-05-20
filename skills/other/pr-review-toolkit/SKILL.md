---
name: pr-review-toolkit
description: Comprehensive PR review agents specializing in comments, tests, error handling, type design, code quality, and code simplification
source: Converted from Claude plugin
license: See original LICENSE
---

# pr-review-toolkit

Comprehensive PR review agents specializing in comments, tests, error handling, type design, code quality, and code simplification

A comprehensive collection of specialized agents for thorough pull request review, covering code comments, test coverage, error handling, type design, code quality, and code simplification. This plugin bundles 6 expert review agents that each focus on a specific aspect of code quality. Use them individually for targeted reviews or together for comprehensive PR analysis. **Focus**: Code comment accuracy and maintainability **Analyzes:** - Comment accuracy vs actual code 

## When to Use This Skill

Use this skill when you need to:
- Comprehensive PR review agents specializing in comments, tests, error handling, type design, code quality, and code simplification

## How It Works

  ## Review Workflow:
  
  •  **Determine Review Scope**
     - Check git status to identify changed files
     - Parse arguments to see if user requested specific review aspects
     - Default: Run all applicable reviews
  
  •  **Available Review Aspects:**
  
     - **comments** - Analyze code comment accuracy and maintainability

## Key Features



## Usage Example

```
# Mention "pr-review-toolkit" in your request
# Example: "Can you review this code using pr-review-toolkit?"
# Or: "Run pr-review-toolkit on this pull request"
```

## Implementation Notes

- **Original command**: review-pr
- **Agents used**: 6
- **Conversion**: Automated from Claude plugin format
- **Limitations**: Some interactive features may be simplified

## For Best Results

1. Provide clear context and code snippets
2. Specify what aspects to focus on
3. Include any relevant guidelines or requirements
4. Be specific about the review scope

---

*Converted from Claude plugin on 2026-02-22*
