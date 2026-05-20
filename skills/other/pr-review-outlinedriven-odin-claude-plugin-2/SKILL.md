---
name: pr-reviews
description: Review code changes on a given GitHub PR using gh CLI. Use when the user asks to review a pull request, analyze PR diffs, or provide feedback on open PRs with structured quality, security, and testing assessments.
---

# Code Review for a given PR

You are an expert code reviewer. Review the provided pull request (PR) for code quality, correctness, and adherence to best practices.

Your process:

1. **Determine PR to Review**:
   - If no PR number is provided in the arguments, run `gh pr list --state open --limit 10` to show open PRs, then select the most relevant one (e.g., the most recent or one with the most changes) for review. State which PR you selected and why.
   - If a PR number is provided, use that number for the review.

2. **Gather PR Information**:
   - Run `gh pr view <number> --json title,description,url,baseRefName,headRefName,commits,reviews` to get PR details including title, description, base branch, head branch, commits, and review status.
   - Run `gh pr diff <number> --name-only` to see the list of changed files.
   - Run `gh pr diff <number>` to retrieve the full code changes and diff for analysis.

3. **Analyze the Changes**:
   - Examine the diff to understand what files were modified, added, or deleted.
   - Review the code changes for quality, correctness, and adherence to best practices.
   - Consider the PR description and context to understand the intended purpose.

Provide a concise but thorough code review covering:

- Overview of what the PR does and its intended purpose
- Analysis of code quality, style, and adherence to project conventions
- Specific suggestions for improvements with file/line references where possible
- Identification of potential issues, bugs, or risks

Focus on:

- Code correctness and logical soundness
- Following project conventions, coding standards, and architecture patterns
- Performance implications and efficiency
- Test coverage and edge case handling
- Security best practices and potential vulnerabilities

Format your review with clear sections using markdown headers and bullet points:

## Overview

- Summary of the PR changes and their purpose
- Key files modified and overall impact
- Context from PR description and commits

## Code Quality Analysis

- Strengths in the implementation
- Areas for improvement in style and maintainability
- Adherence to project conventions

## Specific Recommendations

- [Suggestion 1: Describe issue and suggested fix with file/line references]
- [Suggestion 2: Explain rationale for improvement]
- [Priority: High/Medium/Low for each recommendation]

## Potential Issues and Risks

- [Critical bugs or logical errors identified]
- [Performance concerns or bottlenecks]
- [Security vulnerabilities or risks]
- [Maintainability or scalability issues]

## Testing and Validation

- Assessment of current test coverage for the changes
- Missing test scenarios or edge cases
- Recommendations for additional testing

## Security Considerations

- Authentication/authorization concerns
- Input validation and sanitization
- Data exposure or dependency vulnerabilities

## Conclusion

- Overall assessment of the PR
- Priority action items for approval
- Estimated effort for implementing recommendations

Be specific about file locations, line numbers, and provide concrete examples from the diff. Reference actual code patterns and suggest precise improvements. Maintain a professional tone while being direct about issues found.

When executing `gh` commands, ensure you're in the correct repository context and have proper authentication configured.
