---
name: checkout-branch
description: Create and checkout a new git branch with conventional naming based on the task description. Use when the user asks to create a branch, start working on a feature/fix, or begin a new task.
allowed-tools: Bash(git checkout:*), Bash(git branch:*), Bash(git status:*), AskUserQuestion
model: haiku
---

# Checkout Branch Skill

This skill helps you create and checkout a new git branch following conventional naming conventions.

## Instructions

When the user asks to create a branch or start working on a task, follow these steps:

### 1. Understand the Task

If the user provides a clear task description, use it directly. If not, use the AskUserQuestion tool to ask:
- What task are they working on?
- What type of work is it? (feature, fix, chore, etc.)

### 2. Determine the Branch Type

Analyze the task description to determine the appropriate type:

- **feat**: New features or enhancements
  - Keywords: "add", "create", "implement", "build", "new feature"
  - Examples: "add user authentication", "implement dark mode"

- **fix**: Bug fixes
  - Keywords: "fix", "resolve", "bug", "issue", "patch"
  - Examples: "fix memory leak", "resolve login error"

- **chore**: Maintenance, dependencies, tooling, configuration
  - Keywords: "update dependencies", "configure", "setup", "maintain"
  - Examples: "update npm packages", "configure eslint"

- **docs**: Documentation changes
  - Keywords: "document", "readme", "docs", "documentation"
  - Examples: "update API docs", "add setup instructions"

- **refactor**: Code restructuring without changing behavior
  - Keywords: "refactor", "restructure", "reorganize", "simplify"
  - Examples: "refactor auth logic", "simplify error handling"

- **test**: Adding or updating tests
  - Keywords: "test", "testing", "unit test", "integration test"
  - Examples: "add unit tests", "update test coverage"

- **style**: Code formatting and style changes
  - Keywords: "format", "style", "lint", "prettier"
  - Examples: "format components", "apply linting rules"

- **perf**: Performance improvements
  - Keywords: "optimize", "performance", "speed up", "improve performance"
  - Examples: "optimize queries", "reduce bundle size"

- **ci**: CI/CD pipeline changes
  - Keywords: "ci", "pipeline", "workflow", "github actions"
  - Examples: "add github actions", "update deploy workflow"

- **security**: Security fixes and improvements
  - Keywords: "security", "vulnerability", "secure", "auth"
  - Examples: "fix xss vulnerability", "improve authentication"

### 3. Generate Branch Name

Convert the task description to a branch name following these rules:

1. **Lowercase**: Convert all characters to lowercase
2. **Kebab-case**: Replace spaces with hyphens
3. **Remove special characters**: Keep only letters, numbers, and hyphens
4. **Trim**: Remove leading/trailing hyphens
5. **Format**: Use pattern `<type>/<description>`

Examples:
- "Add user authentication" → `feat/add-user-authentication`
- "Fix memory leak in parser" → `fix/memory-leak-in-parser`
- "Update API Documentation!" → `docs/update-api-documentation`
- "Refactor: error handling" → `refactor/error-handling`

### 4. Check Current Branch Status

Before creating the branch, check the current status:
```bash
git status
```

If there are uncommitted changes, warn the user and ask if they want to:
- Commit the changes first
- Stash the changes
- Continue anyway (changes will carry over to the new branch)

### 5. Create and Checkout the Branch

Create and checkout the new branch:
```bash
git checkout -b <branch-name>
```

### 6. Confirm Success

After creating the branch:
1. Verify with `git branch` or `git status`
2. Inform the user of the branch name
3. Confirm they're ready to start working

## Best Practices

- **Be descriptive**: Branch names should clearly indicate the work being done
- **Be concise**: Keep names under 50 characters when possible
- **Consistent format**: Always use `<type>/<description>` pattern
- **Check for conflicts**: Ensure branch name doesn't already exist
- **Clean branches**: Remind users to delete branches after merging

## Examples

### Example 1: User provides clear description
```
User: "Create a branch to add user authentication"
Assistant: I'll create a new branch for adding user authentication.
Command: git checkout -b feat/add-user-authentication
Output: Switched to a new branch 'feat/add-user-authentication'
Response: "Created and checked out branch 'feat/add-user-authentication'. You're ready to start working on user authentication!"
```

### Example 2: User needs clarification
```
User: "Create a new branch"
Assistant: [Uses AskUserQuestion to ask what task they're working on]
User: "I need to fix a bug in the login form"
Assistant: I'll create a new branch for fixing the login form bug.
Command: git checkout -b fix/login-form-bug
Output: Switched to a new branch 'fix/login-form-bug'
Response: "Created and checked out branch 'fix/login-form-bug'. Ready to fix the bug!"
```

### Example 3: Uncommitted changes
```
User: "Create a branch to refactor the database layer"
Assistant: [Runs git status and sees uncommitted changes]
Response: "You have uncommitted changes. Would you like to commit them first, stash them, or continue anyway?"
User: "Commit them first"
Assistant: [Uses commit skill to commit changes, then creates branch]
Command: git checkout -b refactor/database-layer
Response: "Committed changes and created branch 'refactor/database-layer'."
```

## Error Handling

- **Branch already exists**: Inform user and ask if they want to checkout the existing branch or choose a different name
- **Not a git repository**: Inform user they need to initialize a git repository first
- **Uncommitted changes**: Warn and provide options as described above
- **Invalid characters**: Clean the branch name by removing invalid characters

## After Creating the Branch

Optionally suggest next steps:
- "Would you like me to help you implement [task]?"
- "Should I create a commit plan for this work?"
- "Need help getting started with this task?"
