---
name: plan-mode
description: Guide for creating structured plans with numbered steps and quality gates
---

# Plan Mode Skill

Use this skill when creating a plan for workflow implementation.

## Plan Structure

Your plan MUST follow this structure:

### 1. Analysis
- What needs to be done and why?
- What is the current state vs. desired state?
- What are the constraints or requirements?

### 2. Approach
- High-level strategy for implementation
- Key design decisions
- Which patterns or libraries to use

### 3. Steps
- Numbered, concrete steps (3-10 steps typically)
- Each step should be specific and actionable
- Include which files will be modified
- Mention which tools/imports are needed
- Consider dependencies between steps

### 4. Quality Gates
- List gates that should pass after execution
- Always include: `validate`, `dry`
- Add optional gates if needed: `pytest`, `ruff`, `typecheck`

## Example Plan

```markdown
## Analysis
The workflow needs to fetch stock prices from Yahoo Finance API to provide
real-time data. Currently, there's no data fetching capability.

## Approach
We will create a new tool `yahoo_finance` in tools/ that wraps the yfinance
library, then integrate it into the workflow using a @step decorator.

## Steps
1. Create tools/yahoo_finance/tool.py with fetch_stock_price() function
2. Add yfinance dependency to tool's config.yaml
3. Update workflow run.py to import yahoo_finance
4. Add @step("fetch_prices") that calls yahoo_finance.fetch_stock_price()
5. Update dry_run.py with mock stock data for testing
6. Add test case in test.py for the fetch step

## Quality Gates
- validate: Structural validation must pass
- dry: Dry run with mocks must complete successfully
- pytest: All unit tests must pass
```

## Tips

- Keep steps atomic and sequential
- Don't skip validation in your plan
- Always consider the dry run path
- Think about error cases and edge conditions
- Reference existing code patterns when possible
