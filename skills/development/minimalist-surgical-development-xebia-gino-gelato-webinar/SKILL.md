---
name: minimalist-surgical-development
description: Use when editing an existing codebase and the goal is minimal, standard, and non-invasive changes - prioritizes simplest solution, standard libraries first, and surgical modification without unsolicited refactors
---

# Minimalist & Surgical Development

## Overview

**Code like Kent Beck.** This skill keeps changes small and conventional: solve the stated problem with the least code and the least disruption to existing structure.

## Use when...

- The request emphasizes “minimal changes”, “surgical fix”, “preserve structure”, “don’t refactor”
- The task is to modify existing code rather than build from scratch
- There is temptation to introduce new abstractions, frameworks, or large rewrites

## Symptoms / keywords

- “minimal”, “surgical”, “small diff”, “don’t touch unrelated”, “keep style”, “no refactor”, “standard library first”, “YAGNI”, “KISS”

## Minimalist & Standard Code Generation

- **Principle of Simplicity**: Always provide the most straightforward and minimalist solution possible. The goal is to solve the problem with the least amount of code and complexity. Avoid premature optimization or over-engineering.
- **Standard First**: Heavily favor standard library functions and widely accepted, common programming patterns. Only introduce third-party libraries if they are the industry standard for the task or absolutely necessary.
- **Avoid Elaborate Solutions**: Do not propose complex, "clever", or obscure solutions. Prioritize readability, maintainability, and the shortest path to a working result over convoluted patterns.
- **Focus on the Core Request**: Generate code that directly addresses the user's request, without adding extra features or handling edge cases that were not mentioned.

## Surgical Code Modification

- **Preserve Existing Code**: The current codebase is the source of truth and must be respected. Your primary goal is to preserve its structure, style, and logic whenever possible.
- **Minimal Necessary Changes**: When adding a new feature or making a modification, alter the absolute minimum amount of existing code required to implement the change successfully.
- **Explicit Instructions Only**: Only modify, refactor, or delete code that has been explicitly targeted by the user's request. Do not perform unsolicited refactoring, cleanup, or style changes on untouched parts of the code.
- **Integrate, Don't Replace**: Whenever feasible, integrate new logic into the existing structure rather than replacing entire functions or blocks of code.

## Intelligent Tool Usage

- **Use Tools When Necessary (via subagents)**: When a request requires external information or direct interaction with the environment, dispatch an appropriate subagent to use the necessary tools and return a cited Context Package. The orchestrator must not perform investigation/data-fetching I/O directly.
- **Directly Edit Code When Requested (via subagents)**: If explicitly asked to modify/refactor/add code, dispatch an implementation subagent to apply the changes directly in the codebase. Avoid copy/paste snippets unless requested; default to a small, surgical diff implemented by the subagent.
- **Purposeful and Focused Action**: Tool usage must be directly tied to the user's request. Do not perform unrelated searches or modifications. Every action taken by a tool should be a necessary step in fulfilling the specific, stated goal.
- **Declare Intent Before Tool Use**: Before executing any tool, you must first state the action you are about to take and its direct purpose. This statement must be concise and immediately precede the tool call.

## Quick checklist

- Ensure a research subagent has read the relevant files (with citations) before any changes
- Make the smallest diff that satisfies the requirement
- Prefer existing utilities/abstractions over adding new ones
- Avoid new dependencies unless clearly justified
