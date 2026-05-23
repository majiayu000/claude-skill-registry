---
name: plan-steps-split
description: Split plan steps into individual markdown files in Obsidian vault. Use after creating a plan with plan-on-md when you want each step as a separate trackable file.
---

# Plan Steps Splitter

計画の各ステップを個別のMarkdownファイルに分割してObsidian Vaultに保存します。

## When to Use

- Basically after using `plan-on-md` to save main plan
- When steps need individual tracking
- For complex plans with many steps

## Directory Structure

Files are created in the same directory as the main plan:

```
~/uuta/Projects/{project_name}/{branch_name}/
├── {plan-name}.md              (main plan)
├── {plan-name}-step-01.md     (Step 1)
├── {plan-name}-step-02.md     (Step 2)
└── {plan-name}-step-0N.md     (Step N)
```

If you have no idea at where the main plan markdown is located, use git-grep or grep to find it.

## What you add to step files

Add `Step status` into each file to track how much agents has proceeded tasks. Agents are often executed parallelly.

`Step status` only has the following values.

- Ready
- In progress
- In review (use for a review by user)
- Pending
- Done
