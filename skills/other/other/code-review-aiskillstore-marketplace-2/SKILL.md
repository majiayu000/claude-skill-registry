---
name: code-review
description: Use this skill when user asks to "review code", "check for issues", "analyze code quality", "find bugs", or wants feedback on code implementation.
version: 1.0.0
allowed-tools: [Read, Glob, Grep]
---

# Code Review

Perform thorough code review analyzing quality, potential bugs, security issues, and suggesting improvements.

## Parameters

```json
{
  "type": "object",
  "properties": {
    "target": {
      "type": "string",
      "description": "File path, directory, or glob pattern to review"
    },
    "focus": {
      "type": "string",
      "enum": ["general", "security", "performance", "maintainability"],
      "description": "Primary focus area",
      "default": "general"
    }
  },
  "required": ["target"]
}
```

## When to Use

- User asks to "review" or "check" code
- User wants to find bugs or issues
- User asks about code quality
- User wants security analysis
- User asks for improvement suggestions

## Methodology

### Phase 1: Context Gathering
- Read the target files
- Understand the codebase structure
- Identify the programming language and framework
- Check for related tests and documentation

### Phase 2: Analysis
1. **Logic Review**: Check for bugs and edge cases
2. **Security Scan**: Look for vulnerabilities (injection, auth issues, etc.)
3. **Performance Check**: Identify bottlenecks and inefficiencies
4. **Style Review**: Check consistency and best practices

### Phase 3: Prioritization
- Categorize issues by severity (Critical, High, Medium, Low)
- Focus on actionable feedback
- Provide concrete examples

### Phase 4: Output
Provide structured review with:
- Summary of findings
- Issues list with severity and line numbers
- Specific improvement suggestions
- Code examples where helpful

## Guidelines

- Be constructive, not just critical
- Provide specific line references
- Explain WHY something is an issue
- Suggest concrete fixes, not just problems
- Acknowledge good patterns when found
- Consider the project's existing style

## Examples

### Example 1: File Review

**User Input**: "Review src/auth.ts for security issues"

**Expected Behavior**:
1. Read the file and understand authentication flow
2. Check for common security issues (SQL injection, XSS, weak crypto)
3. Verify input validation and sanitization
4. Check for proper error handling
5. Provide prioritized list of findings with fixes

### Example 2: Directory Review

**User Input**: "帮我 review 一下 src/utils/ 目录的代码质量"

**Expected Behavior**:
1. 列出并读取目录中的所有文件
2. 分析代码结构、命名、错误处理
3. 检查是否有重复代码或可抽象的模式
4. 用中文输出详细的 review 报告
5. 按严重程度排序问题列表
