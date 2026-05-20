---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## Plan File Format

```json
[
  {
    "category": "functional",
    "prd": "${prd_file}#${section_anchor}",
    "description": "${feature_description}",
    "bdd": [
      {
        "title": "${test_title}",
        "description": "${test_description}",
        "steps": ["step_1", "step_2", "step_3"],
        "expected": "${expected_result}"
      }
    ],
    "passes": false
  }
]
```

**命名规则：**
- 计划文件名必须包含 PRD 文件基名，格式：`{prd_basename}-{number}.json`
- `{prd_basename}` = PRD 文件名去掉扩展名（如 `02-architecture-and-features.md` → `02-architecture-and-features`）

**Field descriptions:**
- `category`: Task category (functional, refactor, infrastructure, etc.)
- `prd`: PRD reference, format: `filename#anchor`
- `description`: Used as task title
- `bdd`: Behavior-driven test cases defining verification criteria
- `passes`: Updated to `true` only after **all** tasks are completed and verified (never update individually per task)

**example**
```json
[
  {
    "category": "functional",
    "prd": "02-architecture-and-features.md#4.1",
    "description": "LLM 只看到唯一的 Bash 工具 — JSON Schema 中仅暴露一个名为 Bash 的tool_use 定义",
    "bdd": [
      {
        "title": "Tool Schema 仅包含 Bash",
        "description": "验证发送给 LLM 的 tools 列表中只有一个工具定义",
        "steps": [
          "启动 Agent 实例",
          "获取发送给 LLM API 的 tools 参数",
          "检查 tools 数组的长度和内容"
        ],
        "expected": "tools 数组长度为 1，唯一元素的 name 为 'Bash'，包含 command (string) 输入参数"
      }
    ],
    "passes": false
  }
]
```

## The Process

### Step 1: Load and Review Plan
1. Read plan file (JSON format above)
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed (one todo per feature)

### Step 2: Execute Batch
**Default: First 3 tasks**

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified (execute BDD test steps)
4. Mark as completed

> **⚠ `passes` 字段规则：** 禁止在单个任务完成时更新 `passes`。只有当计划文件中**所有任务**都完成且验证通过后，才能批量将 `passes` 更新为 `true`。

### Step 3: Report
When batch complete:
- Show what was implemented
- Show verification output
- Say: "Ready for feedback."

### Step 4: Continue
Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

### Step 5: Verify All BDD Tests

**Before updating `passes` fields, systematically verify each feature:**

1. Create a TodoWrite with one item per feature for verification tracking
2. For each feature in the plan file:
   - Mark feature as in_progress
   - Execute each BDD test case's steps
   - Verify the expected result is achieved
   - Record verification output
   - Mark feature as completed only if ALL its BDD tests pass

**Verification methods by test type:**

| Test Type | Verification Method |
|-----------|---------------------|
| File exists/not exists | `ls <path>` or Glob tool |
| File contains content | Grep tool or `bun -e` script |
| Function returns value | `bun -e` with import and call |
| Code structure | Grep for patterns, Read file |
| API/behavior | Run test command or script |

**Example verification script:**
```bash
bun -e "
import { functionName } from './src/path/to/module.js';

const result = functionName(args);
console.log('Expected:', expectedValue);
console.log('Actual:', result);
console.log('Pass:', result === expectedValue);
"
```

**If any BDD test fails:**
- Stop verification process
- Report the failure with details
- Ask for guidance before proceeding

### Step 6: Complete Development

After ALL features verified:

1. **Batch update** all `passes` fields to `true` in the plan file
   - Use Write tool to update the entire file
   - Never update `passes` individually during execution

2. **Run project tests:**
   ```bash
   # Run project's test suite
   npm test / bun test / cargo test / pytest / go test ./...
   ```

3. **Handle test results:**
   - If tests related to this migration fail: Fix before proceeding
   - If pre-existing tests fail (existed before migration): Document and proceed
   - Run migration-specific tests to confirm: `bun test <related-test-files>`

4. Announce: "I'm using the finishing-a-development-branch skill to complete this work."
   - **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
   - Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly
- BDD test verification fails

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Verify ALL BDD tests before updating `passes`
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **superpowers:using-git-worktrees** - REQUIRED: Set up isolated workspace before starting
- **superpowers:writing-plans** - Generates plan files following the JSON template structure in this skill
- **superpowers:finishing-a-development-branch** - Complete development after all tasks

**Plan file location conventions:**
- Project plans: `./plans/{prd_basename}-{number}.json`
