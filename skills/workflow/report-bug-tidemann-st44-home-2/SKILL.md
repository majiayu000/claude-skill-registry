---
name: report-bug
description: Quickly report bugs and minor issues to GitHub Issues
user-invocable: true
allowed-tools: Bash, AskUserQuestion, mcp__claude-in-chrome__*
---

# Bug Reporter Skill

Quick bug reporting tool that creates properly formatted GitHub issues.

## Usage

```
/report-bug <description>
```

**Examples:**

```
/report-bug There is a padding around the login page that creates a white border around the background
/report-bug Task card hover effect not working in Safari
/report-bug API returns 500 when deleting a task that doesn't exist
```

## How It Works

When invoked, this skill will:

1. **Capture the bug description** from user input
2. **Ask clarifying questions** (area, severity)
3. **Create a GitHub issue** with proper formatting
4. **Apply appropriate labels** (bug + area + priority)
5. **Add to milestone** (MVP Launch)
6. **Return the issue URL**

## Issue Template

```markdown
## Description

[User's bug description]

## Area

[Frontend/Backend/Database]

## Priority

[Severity level]

## Expected Behavior

[If provided]
```

## Workflow

1. User runs: `/report-bug <description>`
2. Skill asks for:
   - Area (Frontend/Backend/Database)
   - Priority (MVP Blocker/Critical/High/Medium/Low)
3. Skill creates GitHub issue with:
   - Title: "Bug: [short description]"
   - Labels: `bug` + area + priority
   - Milestone: "MVP Launch"
4. Returns issue URL to user

## Priority Levels

- **MVP Blocker** (`mvp-blocker`) - Breaks core functionality, must fix before launch
- **Critical** (`critical`) - Blocks important features
- **High** (`high-priority`) - Should fix soon, affects UX
- **Medium** (`medium-priority`) - Default, should fix but not urgent
- **Low** (`low-priority`) - Nice to have

## Area Labels

- `frontend` - Angular UI, components, pages, styles
- `backend` - Fastify API, routes, business logic
- `database` - PostgreSQL schema, migrations, queries

## Examples

### Example 1: UI Bug

```
/report-bug There is a padding around the login page that creates a white border around the background
```

Creates:

- Title: "Bug: Padding around login page creates white border"
- Labels: `bug`, `frontend`, `medium-priority`
- Milestone: "MVP Launch"

### Example 2: Critical API Bug

```
/report-bug API returns 500 when deleting a task that doesn't exist
```

User selects: Backend, Critical

Creates:

- Title: "Bug: API returns 500 when deleting non-existent task"
- Labels: `bug`, `backend`, `critical`
- Milestone: "MVP Launch"

## Implementation

The skill should:

1. Parse the bug description from ARGUMENTS
2. Ask user for area and priority using AskUserQuestion
3. Format a proper issue body
4. Create the issue using `gh issue create`
5. Return the issue URL

Keep it simple and fast - the goal is to make bug reporting frictionless.

## Capturing Live Screenshots (Optional Enhancement)

For visual bugs, capture evidence from the production site at **home.st44.no**:

### Take Screenshot

```bash
# 1. Get tab context
tabs_context_mcp(createIfEmpty: true)

# 2. Navigate to the affected page
navigate(url: "https://home.st44.no/...", tabId: <id>)

# 3. Take screenshot
computer(action: "screenshot", tabId: <id>)

# Include screenshot ID in bug report description
```

### Record Bug Reproduction (For Complex Bugs)

```bash
# 1. Start recording
gif_creator(action: "start_recording", tabId: <id>)
computer(action: "screenshot", tabId: <id>)  # Initial frame

# 2. Reproduce the bug steps
computer(action: "left_click", coordinate: [x, y], tabId: <id>)
# ... more steps ...

# 3. Capture final state
computer(action: "screenshot", tabId: <id>)
gif_creator(action: "stop_recording", tabId: <id>)

# 4. Export GIF
gif_creator(action: "export", download: true, filename: "bug-reproduction.gif", tabId: <id>)
```

### When to Capture Visual Evidence

- **Always** for visual/UI bugs (layout, styling, positioning)
- **Recommended** for UX issues (confusing flows, unexpected behavior)
- **Optional** for API/backend bugs (unless UI shows error state)

Visual evidence helps developers understand and fix bugs faster.

## Related Resources

- **Live Debug Skill**: `.claude/skills/live-debug/SKILL.md` - Full browser debugging documentation
