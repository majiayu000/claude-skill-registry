---
name: proceed-by-step
description: Execute markdown-defined plan steps sequentially with user confirmation. Use when progressing through split plan files (created by plan-on-md or plan-steps-split), tracking step status, or working through complex multi-step implementations one step at a time.
---

# Proceed by step

markdownに定義されたstepを1stepずつ進め、完了した段階でuserに確認を取る

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

## How to do

### In case a user doesn't specify step file

- Read main file ({plan-name}.md)
- Read a step file from step-1, and check `Step status`. If it's
  - `Ready`, change it to `In progress`
    - Proceed tasks defined in `{plan-name}-step-0N.md`
    - If you complete every task in it, request a review to me and change the `Step status` to `In review`
    - If I confirm your implementation, change the `Step status` to `Done`
    - Move to the next step
  - `In progress`, stop your operation and report which `Step status` is to me
  - `In review`, stop your operation and report which `Step status` is to me
  - `Pending`, stop your operation and report which `Step status` is to me
  - `Done`, move to the next step since this step can be considered being finished

### In case a user specify step file

- Read main file ({plan-name}.md)
- Read the specified step file, and check `Step status`. If it's
  - `Ready`, change it to `In progress`
    - Proceed tasks defined in the specified step file
    - If you complete every task in it, request a review to me and change the `Step status` to `In review`
    - If I confirm your implementation, change the `Step status` to `Done`
