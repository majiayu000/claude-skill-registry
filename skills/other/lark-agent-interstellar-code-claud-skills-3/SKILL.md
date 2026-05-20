---
name: lark-agent
description: |
  Create hierarchical Lark tasks from markdown test plans.

  ACTIVATE THIS SKILL when user:
  - Says "create lark tasks" or "process test file" or "convert test plan"
  - Mentions "lark" + "test" or "test scenarios" or "test cases"
  - Wants to convert markdown test documentation into Lark tasks
  - Has a test file and wants it in Lark

  WORKFLOW:
  1. Ask user for test file path (required)
  2. Ask for owner, priority, target date (optional)
  3. Execute: python .claude/skills/lark-agent/run.py [file] --owner="[name]" --priority=[1-3] --target-date="YYYY-MM-DD"
  4. Parse JSON output
  5. Execute Lark MCP workflow to create tasks
  6. Report results

  DO NOT create test plans yourself - only process existing markdown files unless explicitly asked.

## 🎨 **VISUAL OUTPUT FORMATTING**

**CRITICAL: All lark-agent output MUST use the colored-output formatter skill!**

```bash
bash .claude/skills/colored-output/color.sh skill-header "lark-agent" "Creating Lark tasks..."
bash .claude/skills/colored-output/color.sh progress "" "Processing test file"
bash .claude/skills/colored-output/color.sh success "" "Tasks created successfully"
```

---
version: 1.0.0
author: Claude Code
tags: [lark, testing, automation, markdown, json, task-management]
---

# Lark Agent Skill

Create structured Lark tasks from markdown test documentation with proper hierarchy and verification.

## Overview

The Lark Agent skill provides a complete end-to-end workflow for:
1. **Parsing** markdown test files with clear structure
2. **Generating** structured JSON with test hierarchy
3. **Preparing** Lark task creation workflow (3-level hierarchy)
4. **Preparing** verification workflow
5. **Outputting** complete workflow plan for execution

This skill is designed for teams that maintain test documentation in markdown format and need to convert them into trackable Lark tasks automatically.

## When to Use This Skill

Activate this skill when user:
- Wants to create Lark tasks from test plans
- Mentions "lark", "test cases", "test planning", "test scenarios"
- Has a markdown file with test documentation
- Needs to convert test documentation into Lark tasks
- Wants to process test files into structured tasks

## Workflow

### 1. Markdown Input Processing

The skill accepts markdown files with the following structure:

```markdown
# Test Title
Test description

## Test Scenario: Scenario Name
Scenario description

### Task: Task Name
1. Step one
2. Step two
Expected Result: What should happen
```

### 2. JSON Generation

Converts markdown into structured JSON:

```json
{
  "testOverview": {
    "title": "Test Title",
    "description": "Test description",
    "owner": "Assigned User",
    "targetDate": "2025-11-02",
    "status": "pending"
  },
  "scenarios": [
    {
      "scenarioId": "scenario-0-timestamp",
      "title": "Scenario Name",
      "description": "Scenario description",
      "tasks": [
        {
          "taskId": "task-0-0-timestamp",
          "title": "Task Name",
          "description": "Steps",
          "expectedResult": "Expected outcome",
          "status": "pending"
        }
      ]
    }
  ]
}
```

### 3. Lark Task Creation

Creates hierarchical tasks in Lark via MCP:
- **Level 1**: Parent task (test overview)
- **Level 2**: Scenario tasks (marked as milestones)
- **Level 3**: Individual test tasks

Uses Lark MCP tools:
- `task_v2_tasklist_create` - Create task list
- `task_v2_task_create` - Create parent task
- `task_v2_taskSubtask_create` - Create scenario and individual tasks
- `task_v2_task_addMembers` - Assign users

### 4. Verification & Reporting

After task creation, the skill verifies:
- ✅ Parent task created with correct details
- ✅ All scenario tasks created as milestones
- ✅ All individual tasks created with test steps
- ✅ Task hierarchy is correct (parent → scenarios → tasks)
- ✅ User assignments are correct
- ✅ Dates and priorities match specifications

Generates a comprehensive report showing:
- Number of tasks created at each level
- Any failures or issues encountered
- Confirmation that structure matches requirements
- Recommendations for any issues found

## Usage

### ⚠️ Important: Interactive Mode Not Supported

**Interactive mode (stdin prompts) does NOT work in Claude Code's environment.**

The skill works via **conversational approach with visual indicators**.

### 🎯 How It Works

When user requests Lark task creation:

#### 1️⃣ Show Activation Banner

Display:
```
╔══════════════════════════════════════════════════════════════════╗
║              🚀 LARK AGENT SKILL ACTIVATED 🚀                   ║
║      Converting Test Plans → Structured Lark Tasks              ║
╚══════════════════════════════════════════════════════════════════╝
```

#### 2️⃣ Collect Parameters with Emojis

- **📄 Test file path** (required): "📄 Which test file would you like to process?"
- **👤 Owner name** (optional): "👤 Who should be the task owner? (default: QA Team)"
- **⚡ Priority** (optional): "⚡ What priority? (1=low, 2=medium, 3=high, default: 2)"
- **📅 Target date** (optional): "📅 What's the target completion date? (YYYY-MM-DD)"

#### 3️⃣ Execute Skill with Progress Indicators

Show:
```
🔄 Executing Lark Agent skill...
📂 File: [file-path]
👤 Owner: [owner]
⚡ Priority: [priority]
📅 Target: [date]
```

Execute:
```bash
python .claude/skills/lark-agent/run.py [file-path] \
  --owner="[name]" \
  --priority=[1-3] \
  --target-date="YYYY-MM-DD"
```

#### 4️⃣ Parse Output

Show: `📊 Parsing workflow output...`

#### 5️⃣ Execute Lark MCP Workflow

Show progress:
```
🏗️ Creating Lark tasks...
   ✅ Step 1: Creating task list
   ✅ Step 2: Creating parent task
   ✅ Step 3: Creating scenario tasks
   ✅ Step 4: Creating individual tasks
```

#### 6️⃣ Report Results

Show completion banner:
```
╔══════════════════════════════════════════════════════════════════╗
║              ✅ LARK AGENT WORKFLOW COMPLETED! ✅               ║
╚══════════════════════════════════════════════════════════════════╝

📊 Summary:
   📋 Test: [test title]
   🎯 Scenarios: [count]
   📝 Total Tasks: [count]
```

### Direct Mode (Only Working Mode)

```bash
python .claude/skills/lark-agent/run.py [file-path] --owner="name" --priority=2 --target-date="YYYY-MM-DD"
```

### Available Options

- `file-path` (required): Path to markdown test file
- `--owner` (optional): Task owner name (default: "QA Team")
- `--priority` (optional): 1=low, 2=medium, 3=high (default: 2)
- `--target-date` (optional): Target date YYYY-MM-DD (default: 7 days from today)
- `--task-list-id` (optional): Existing Lark task list ID

### Example Conversation

```
User: Create Lark tasks from tests/manual/login-test.md
Claude: I'll help you create Lark tasks. Who should be the owner?
User: QA Team
Claude: What priority? (1=low, 2=medium, 3=high)
User: 2
Claude: What's the target date? (YYYY-MM-DD)
User: 2025-12-31
Claude: [Executes skill and creates tasks]
```

## Implementation Details

### Scripts

The skill uses the following Python scripts located in `scripts/`:

1. **lark_agent.py** - Main entry point and workflow orchestrator
2. **markdown_parser.py** - Parses markdown and extracts test structure
3. **lark_task_creator.py** - Creates hierarchical Lark tasks via MCP
4. **lark_task_verifier.py** - Verifies task creation and generates reports

These scripts are designed to work with Claude Code's tool calling capabilities for Lark MCP integration.

### References

Documentation in `references/`:

1. **usage-guide.md** - Detailed usage instructions and examples
2. **json-schema.md** - Complete JSON structure specification
3. **markdown-format.md** - Markdown format requirements

### Templates

Example files in `assets/templates/`:

1. **test-template.md** - Template for creating new test files
2. **output-template.json** - Example JSON output structure

## Integration with Lark MCP

This skill uses the following Lark MCP tools:

- `task_v2_task_create` - Create tasks
- `task_v2_tasklist_create` - Create task lists
- `task_v2_taskSubtask_create` - Create subtasks
- `task_v2_task_addMembers` - Assign users
- `timezone` tools - Handle date calculations

## Error Handling

The skill handles common errors:

- **File not found**: Validates file path before processing
- **Invalid markdown structure**: Reports parsing errors with line numbers
- **Lark API errors**: Retries failed task creation and reports issues
- **Date validation**: Ensures dates are valid and in the future

## Best Practices

### Markdown File Structure

- Use clear heading hierarchy (H1 for title, H2 for scenarios, H3 for tasks)
- Include expected results for each task
- Keep task descriptions concise but complete
- Use consistent naming conventions

### Task Organization

- Group related tests into scenarios
- Set realistic target dates
- Assign appropriate owners
- Use meaningful task titles

## Examples

See `references/usage-guide.md` for detailed examples and `assets/templates/` for template files.

## Troubleshooting

### Markdown Parsing Issues

If markdown parsing fails:
1. Check heading hierarchy (H1 > H2 > H3)
2. Ensure proper markdown syntax
3. Verify file encoding (UTF-8)

### Lark Task Creation Issues

If task creation fails:
1. Verify Lark MCP server is running
2. Check user permissions in Lark
3. Validate date formats
4. Review error messages in output

## Version History

### v1.0.0
- Initial release
- Markdown parsing and JSON generation
- Hierarchical Lark task creation
- Basic error handling and validation
