---
name: update-pr
description: Complete PR update workflow - updates both title and description with project-aware content. Orchestrates update-pr-title and update-pr-desc commands.
allowed-tools: Skill
user-invocable: true
---

# Update PR Agent

## Agent Type

This is an **orchestrator agent** that coordinates PR title and description updates. Unlike worker skills that perform specific tasks, agents manage workflows and coordinate commands/skills.

## Coordinated Commands

- **update-pr-title**: PR title generation based on commits and changes
- **update-pr-desc**: PR description generation with project-aware content and Mermaid diagrams

## Overview

Provides a complete PR update workflow by orchestrating the update-pr-title and update-pr-desc commands.

## When to Activate

This skill activates when:
- User requests complete PR update
- User wants both title and description updated
- User uses language suggesting comprehensive PR update

## Workflow

### Step 1: Confirm Intent

Ask the user what they want to update:
- Both title and description (default)
- Title only
- Description only

If the user explicitly says "both" or "everything" or just "update PR", default to both.

### Step 2: Gather Options

Collect options from user request or ask if not specified:
- `--pr <number>`: PR number (optional, detects from branch if not provided)
- `--lang <language>`: Language (korean/english, default: korean)
- `--include-load-test`: Include load test results in description (optional)

### Step 3: Execute Commands

Based on user's choice:

**Both title and description (default)**:
1. Execute update-pr-title command with collected options
2. Wait for completion
3. Execute update-pr-desc command with collected options
4. Report combined results

**Title only**:
1. Execute update-pr-title command with collected options

**Description only**:
1. Execute update-pr-desc command with collected options

### Step 4: Report Results

Provide summary:
- PR number and URL
- What was updated (title, description, or both)
- Language used
- For description updates: mention Mermaid charts generated and project type detected
- Any relevant statistics (coverage, test count, etc.)

## Command Execution

Use the Skill tool to execute commands:

**Update title**:
```
Call Skill tool with:
- skill: "update-pr-title" (not a command, it's defined in commands/)
- args: "--pr 123 --lang ko" (if applicable)
```

Note: Since update-pr-title and update-pr-desc are commands (not skills), you should invoke them by reading the command files and executing their instructions, NOT by using the Skill tool.

## Correct Approach

1. Parse user options (--pr, --lang, --include-load-test)
2. Read and execute `commands/update-pr-title.md` instructions
3. Read and execute `commands/update-pr-desc.md` instructions
4. Report combined results

## Example Workflow

### Example 1: Both title and description with Korean

```
User: /update-pr --pr 123 --lang ko

Skill: Updating PR #123 with Korean title and description...

[Reads and executes update-pr-title.md instructions]
✓ Title updated: [SYN-1234] 기능: 사용자 인증 시스템 구현

[Reads and executes update-pr-desc.md instructions]
✓ Description updated with:
  - Project type: Django Backend
  - PR Type: Feature ✨
  - Mermaid diagram: API Flow
  - Test coverage: 85%

PR #123 successfully updated!
View: https://github.com/org/repo/pull/123
```

### Example 2: Current branch, English

```
User: /update-pr --lang eng

Skill: Detecting PR from current branch...

[Detects PR #156 from current branch]
[Executes both update-pr-title and update-pr-desc with English language]

✓ PR #156 updated successfully!
  - Title: [SYN-1234] feat: Implement JWT authentication system
  - Description: Complete with API flow diagram
  - Language: English
```

### Example 3: Title only

```
User: update pr title for PR 123

Skill: Updating only the title for PR #123...

[Executes update-pr-title only]
✓ Title updated: [SYN-1234] 기능: 사용자 프로필 업데이트 API 추가
```

### Example 4: Description only with load test

```
User: update pr description with load test results

Skill: Updating description for current branch PR with load test results...

[Executes update-pr-desc with --include-load-test flag]
✓ Description updated with load test results included
```

## Benefits

1. **Convenient**: Single command for complete PR updates
2. **Consistent**: Ensures title and description match and are coherent
3. **Flexible**: Can update both or just one component
4. **Project-aware**: Automatically adapts content based on detected project type
5. **User-friendly**: Simple interface for complex operations

## Error Handling

- If PR number not provided and cannot detect from branch: Ask user for PR number
- If GitHub MCP not available: Guide user to check GITHUB_TOKEN and .mcp.json configuration
- If command execution fails: Report specific error and suggest remediation
- If user's intent is unclear: Ask for clarification

## Integration with Other Skills/Commands

- **update-pr-title command**: Generates concise PR title following commit message conventions
- **update-pr-desc command**: Generates comprehensive PR description with project-aware content and Mermaid charts
- **mermaid-expert skill**: Used internally by update-pr-desc for diagram generation
