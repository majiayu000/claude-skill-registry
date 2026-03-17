---
name: lark-agent-simple
description: |
  Token-efficient Lark task creation from markdown test files.
  Uses 60-70% fewer tokens than lark-agent by executing MCP calls directly.

  ACTIVATE THIS SKILL when user:
  - Says "create lark tasks" or "lark agent simple" or "efficient lark"
  - Wants token-efficient Lark task creation
  - Has a test file and wants it in Lark with minimal overhead

  WORKFLOW:
  1. Parse markdown file to compact JSON (data only, no workflow)
  2. Execute Lark MCP calls directly from slash command
  3. Report results

  DO NOT create test plans yourself - only process existing markdown files.

## 🎨 **VISUAL OUTPUT FORMATTING**

**CRITICAL: All lark-agent-simple output MUST use the colored-output formatter skill!**

```bash
bash .claude/skills/colored-output/color.sh skill-header "lark-agent-simple" "Creating Lark tasks..."
bash .claude/skills/colored-output/color.sh progress "" "Parsing test file"
bash .claude/skills/colored-output/color.sh success "" "Tasks created"
```

---

version: 1.0.0
author: Claude Code
tags: [lark, testing, automation, markdown, token-efficient, mcp]
---

# Lark Agent Simple Skill

Token-efficient Lark task creation from markdown test files with **60-70% token reduction** compared to the original lark-agent.

## Overview

The Lark Agent Simple skill provides an optimized workflow for:
1. **Parsing** markdown test files into minimal JSON (data only)
2. **Executing** Lark MCP calls directly (no workflow generation)
3. **Creating** hierarchical Lark tasks (3-level structure)
4. **Reporting** results with summary

This skill eliminates the token overhead of workflow generation by moving execution logic from Python to the slash command.

## Architecture

### Token Efficiency Design

**Traditional Approach (lark-agent):**
```
Markdown → Python → Workflow Plan JSON (2000-5000 tokens)
→ Claude interprets plan → Claude executes MCP
Total: 10,000-25,000 tokens
```

**Optimized Approach (lark-agent-simple):**
```
Markdown → Python → Minimal Data JSON (500-1000 tokens)
→ Claude executes MCP directly
Total: 3,000-8,000 tokens
```

**Savings: 60-70% token reduction**

### Component Roles

1. **Python Parser** (`lark_agent_simple.py`)
   - Role: Data transformation only (markdown → JSON)
   - Output: Minimal structured data (no workflow instructions)
   - Size: ~150 lines (vs 250+ in original)

2. **Slash Command** (`.claude/commands/lark-agent-simple.md`)
   - Role: Execution logic
   - Contains: Direct MCP call instructions
   - Advantage: Claude executes immediately (no interpretation)

3. **SKILL.md** (this file)
   - Role: Documentation and activation guide
   - Contains: Usage instructions, examples, reference

## When to Use This Skill

Activate this skill when user:
- Wants to create Lark tasks from markdown test files
- Needs token-efficient execution
- Mentions "lark agent simple" or "efficient lark"
- Has existing test documentation in markdown format
- Wants to avoid token overhead of workflow generation

## Usage

### Command

```bash
/lark-agent-simple <markdown-file> [--owner="Name"] [--due-date="YYYY-MM-DD"]
```

### Parameters

- `<markdown-file>` (required): Path to markdown test file
- `--owner` (optional): Task owner name (default: "Test User")
- `--due-date` (optional): Target date YYYY-MM-DD (default: 14 days from now)
- `--start-date` (optional): Start date YYYY-MM-DD (default: today)

### Examples

```bash
# Basic usage
/lark-agent-simple tests/manual/onboarding-test.md

# With custom owner and due date
/lark-agent-simple tests/manual/login-test.md --owner="QA Team" --due-date="2025-12-31"

# With start and due dates
/lark-agent-simple tests/manual/api-test.md --owner="Dev Team" --start-date="2025-10-20" --due-date="2025-11-03"
```

## Markdown Format

Your test file must follow this structure:

```markdown
# Test Title
Test description

## Test Scenario: Scenario Name
Scenario description

### Task: Task Name
1. Step one
2. Step two
3. Step three

Expected Result: What should happen
```

### Format Requirements

- **H1** (`#`): Test title (required)
- **H2** (`##`): Test scenarios (starts with "Test Scenario:")
- **H3** (`###`): Individual tasks (starts with "Task:")
- **Steps**: Numbered list items
- **Expected Result**: Line starting with "Expected Result:"

## Output

### Compact JSON Data

The Python parser outputs minimal JSON:

```json
{
  "success": true,
  "data": {
    "test": {
      "title": "Test Title",
      "description": "Test description",
      "owner": "QA Team",
      "start_date": "2025-10-19",
      "due_date": "2025-11-02"
    },
    "scenarios": [
      {
        "id": "scenario-0-1729300000000",
        "title": "Scenario Title",
        "description": "Scenario description",
        "tasks": [
          {
            "id": "task-0-0-1729300000000",
            "title": "Task Title",
            "description": "Steps...",
            "expected_result": "Expected outcome"
          }
        ]
      }
    ],
    "metadata": {
      "total_scenarios": 3,
      "total_tasks": 10,
      "source_file": "path/to/test.md"
    }
  }
}
```

### Lark Task Structure

Creates 3-level hierarchy:
- **Level 1**: Parent task (test overview)
- **Level 2**: Scenario tasks (marked as milestones if they have subtasks)
- **Level 3**: Individual test tasks

## Integration with Lark MCP

This skill uses the following Lark MCP tools:

- `task_v2_tasklist_create` - Create task list
- `task_v2_task_create` - Create parent task
- `task_v2_taskSubtask_create` - Create scenario and individual tasks

All calls use `useUAT: true` for user access token authentication.

## Workflow Details

The slash command executes this workflow:

1. **Parse Markdown** → Execute Python script → Get compact JSON
2. **Create Tasklist** → Call MCP → Save `tasklistGuid`
3. **Create Parent Task** → Call MCP → Save `parentTaskGuid`
4. **Create Scenarios** → Loop + Call MCP → Save `scenarioGuids[id]`
5. **Create Tasks** → Loop + Call MCP → Save `taskGuids[id]`
6. **Report Summary** → Display counts and IDs

## Error Handling

The parser validates:
- File exists and is markdown (.md or .markdown)
- File has valid structure (H1, H2, H3 hierarchy)
- Dates are in correct format

Errors are returned as:
```json
{
  "success": false,
  "error": "Error message",
  "error_type": "FileNotFoundError"
}
```

## Key Benefits

### Token Efficiency
- **60-70% reduction** in token usage
- Minimal data transfer (no workflow instructions)
- Direct execution (no interpretation overhead)

### Speed
- Faster execution (fewer round trips)
- No workflow generation delay
- Immediate MCP calls

### Maintainability
- Clean separation (data vs logic)
- Logic in one place (slash command)
- Easy to update execution pattern

### Simplicity
- Straightforward data flow
- No complex abstraction layers
- Clear execution path

## Comparison with Original lark-agent

| Aspect | lark-agent (Original) | lark-agent-simple (New) |
|--------|---------------------|------------------------|
| Python Output | Full workflow plan (2000-5000 tokens) | Minimal data (500-1000 tokens) |
| Execution Logic | In Python (generates instructions) | In slash command (direct) |
| MCP Calls | Claude interprets from plan | Claude executes directly |
| Token Usage | 10,000-25,000 per execution | 3,000-8,000 per execution |
| Python Lines | ~250+ lines | ~150 lines |
| Complexity | High (abstraction layers) | Low (direct flow) |
| Speed | Slower (interpretation) | Faster (direct) |

## Files

```
.claude/skills/lark-agent-simple/
├── SKILL.md                          # This file (documentation)
├── run.py                            # Entry point
├── scripts/
│   ├── markdown_parser.py            # Markdown parser (copied from original)
│   └── lark_agent_simple.py          # Minimal parser (data only)
└── examples/
    └── sample-test.md                # Example test file

.claude/commands/
└── lark-agent-simple.md              # Slash command (execution logic)
```

## Testing

To test the parser independently:

```bash
cd .claude/skills/lark-agent-simple
python run.py examples/sample-test.md --owner="Test User" --due-date="2025-12-31"
```

This outputs compact JSON that can be verified before running the full workflow.

## Troubleshooting

### Parser Issues

If parsing fails:
1. Check markdown file structure (H1 > H2 > H3 hierarchy)
2. Verify file encoding is UTF-8
3. Ensure scenario headers start with "Test Scenario:"
4. Ensure task headers start with "Task:"

### MCP Issues

If Lark task creation fails:
1. Verify Lark MCP server is running
2. Check user has permissions in Lark
3. Validate date formats (YYYY-MM-DD)
4. Review error messages from MCP

### Date Issues

If dates are invalid:
1. Use YYYY-MM-DD format only
2. Ensure due date is after start date
3. Check dates are in the future (if required by Lark)

## Version History

### v1.0.0 (Initial Release)
- Minimal JSON parser (data only)
- Direct MCP execution via slash command
- 60-70% token reduction
- 3-level task hierarchy
- Compact output format

## Support

For issues or questions:
- Review this documentation
- Check example files in `examples/`
- Verify markdown format matches requirements
- Test parser independently before full execution

---

**Remember:** This skill is designed for **token efficiency**. If you need detailed workflow tracking or complex verification, consider using the original `lark-agent` skill instead.
