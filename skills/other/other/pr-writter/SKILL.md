---
name: pr-writter
description: Analyzes the current branch commits and generates a comprehensive Pull Request summary following project standards.
---

# PR Creation Skill

When I ask you to "create a PR" or "summarize my branch," follow this workflow:

## 1. Context Gathering
- Run `git log main..HEAD --oneline` to see all commits on the current branch.
- Run `git diff main..HEAD` to understand the actual code changes.
- Identify the core problem solved and any associated Issue IDs.

## 2. Generate the PR Summary
Draft a PR description that includes:
- **Title**: A clear, concise summary of the change.
- **Related Issue**: Link the issue this PR addresses.
- **The "What"**: Explain the changes made.
- **Testing**: Describe how the changes were verified (Mocha tests, manual runs, etc.).
- **Scrutiny**: Call out specific areas where you want the reviewer to pay extra attention.

## 3. The "Explain-Code" Breakdown
Using the `explain-code` template, provide a breakdown of the PR for the reviewers:

## 3. Step-by-Step Walkthrough
Walk through the logical flow of the new code changes.

## 4. The Gotcha
Highlight a potential side effect or a common mistake a future developer might make when touching this specific area of the code.
