---
name: git-commit
description: Use this skill when user asks to "commit changes", "create a commit", "stage and commit", or wants help with git commit workflow.
version: 1.0.0
allowed-tools: [Read, Bash, Glob, Grep]
---

# Git Commit

Create well-structured git commits with conventional commit messages based on staged changes.

## Parameters

```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "Optional commit message override"
    },
    "type": {
      "type": "string",
      "enum": ["feat", "fix", "docs", "style", "refactor", "test", "chore"],
      "description": "Conventional commit type",
      "default": "auto"
    },
    "scope": {
      "type": "string",
      "description": "Optional scope for the commit"
    }
  }
}
```

## When to Use

- User asks to "commit" changes
- User wants to "save" their work to git
- User asks for help with commit messages
- User wants to stage and commit files

## Methodology

### Phase 1: Status Check
- Run `git status` to see current state
- Run `git diff --staged` to see staged changes
- Run `git diff` to see unstaged changes
- Check recent commit history for message style

### Phase 2: Analysis
1. **Categorize Changes**: Identify what changed (new files, modifications, deletions)
2. **Determine Type**: Is this a feature, fix, refactor, etc.?
3. **Identify Scope**: What component/module is affected?
4. **Summarize Purpose**: What does this change accomplish?

### Phase 3: Commit Creation
- Stage relevant files if not already staged
- Generate conventional commit message
- Execute the commit
- Verify success with `git status`

### Phase 4: Output
Report:
- What was committed
- The commit message used
- The new commit hash

## Guidelines

- Follow Conventional Commits format: `type(scope): description`
- Keep subject line under 72 characters
- Use imperative mood ("Add feature" not "Added feature")
- Don't commit sensitive files (.env, credentials, etc.)
- Don't use --force or --amend unless explicitly requested
- Include meaningful description of WHY, not just WHAT

## Examples

### Example 1: Auto Commit

**User Input**: "Commit my changes"

**Expected Behavior**:
1. Run `git status` and `git diff` to understand changes
2. Analyze the nature of changes
3. Generate appropriate commit message
4. Stage files if needed
5. Create commit and report success

### Example 2: Specific Type

**User Input**: "创建一个 fix 类型的 commit"

**Expected Behavior**:
1. 检查当前的改动
2. 确认这些改动符合 "fix" 类型
3. 生成格式为 `fix(scope): 描述` 的提交信息
4. 执行提交并报告结果
