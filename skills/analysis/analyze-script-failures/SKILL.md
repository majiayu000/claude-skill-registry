---
name: analyze-script-failures
description: Analyze script failures to identify source components and propose fixes
tools: Read, Grep, Glob, Bash, AskUserQuestion, Skill
---

# Analyze Script Failures Skill

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below.

Analyzes script failures from the current session to identify the source component, trace how instructions led to the failed call, and propose fixes.

## What This Skill Provides

- Script failure detection from conversation history
- Origin tracing (command/agent/skill that triggered failure)
- Instruction path analysis (how LLM interpreted instructions)
- Root cause categorization
- Fix proposals with lessons learned integration

## When to Activate

Activate when:
- Script execution returns non-zero exit code
- User asks to analyze script failures
- Debugging why a script call failed

## Workflow: Analyze Script Failures

### Step 0: Load Foundation Skills

```
Skill: pm-plugin-development:plugin-architecture
Skill: plan-marshall:diagnostic-patterns
```

These provide architecture principles and non-prompting tool usage patterns.

### Step 1: Gather Failure Data

**A. Description Analysis** (if provided):
- Parse user's description for specific failure context
- Note: Which script, what error, expected behavior

**B. Chat History Analysis**:
- Review conversation for script errors (non-zero exit codes)
- A script error is: `python3 .plan/execute-script.py` returning non-zero result
- Extract: Full script command, exit code, error output
- Note: What command/agent was active when failure occurred

### Step 2: For Each Failure Found

**A. Extract Failure Details**:
- Complete script call including all parameters
- Exit code and error message
- Naming or parameter errors if any

**B. Trace Origin**:

Determine source component type:

| Source Type | How to Identify |
|-------------|-----------------|
| **Command** | Script call within `/command-name` invocation |
| **Agent** | Script call within Task agent context |
| **Skill** | Script call after `Skill: skill-name` activation |

Read source component file to find instruction context.

**C. Analyze Instruction Path**:

1. **Load source component**:
   ```
   Read: {bundle}/{type}s/{name}.md
   ```

2. **Find the instruction** that led to script call:
   - Search for script notation (`python3 .plan/execute-script.py`)
   - Search for script API mentions
   - Note: Is script explicitly documented or was it inferred?

3. **Capture context** (1-5 lines surrounding instruction)

### Step 3: Root Cause Analysis

For each failure, categorize the root cause:

| Category | Description | Fix Location |
|----------|-------------|--------------|
| **Missing Script Instruction** | Script not documented in component | Add to component |
| **Wrong Script Parameters** | Parameters incorrect or missing | Fix component instruction |
| **LLM Invented Script** | No instruction, LLM guessed script call | Add flow step to component |
| **Missing API** | Operation needed but no script exists | Create new script |
| **Script Bug** | Script exists but has bug | Fix script implementation |
| **Script Not Found** | Notation invalid or script missing | Fix notation or add script |

### Step 4: Generate Analysis Report

Display comprehensive analysis:

```
+================================================================+
|          Script Failure Analysis                               |
+================================================================+

## Failure {n}: {short_description}

### The Actual Failure

**Script Call**:
```bash
python3 .plan/execute-script.py {notation} {subcommand} {args}
```

**Error**:
- Exit code: {code}
- Error type: {naming_error | parameter_error | execution_error}
- Message: {error_message}

### Source of Script Call

**Component**: {type}: {name} ({bundle})
**File**: {file_path}:{line_number}

**Context** (instruction that triggered this):
```markdown
{3-5 lines of context from source component}
```

### Root Cause

**Category**: {category from Step 3}
**Analysis**: {why this happened - how LLM interpreted instructions}
```

### Step 5: Propose Solutions

For each failure, generate appropriate fixes:

**If Missing Script Instruction**:
```markdown
## Proposed Fix: Add Script Instruction

Add to {component_file}:

### Script: {notation}

```bash
python3 .plan/execute-script.py {notation} {subcommand} {params}
```

**Reasoning**: Component uses this script but lacks explicit instruction.
```

**If Wrong Script Parameters**:
```markdown
## Proposed Fix: Correct Parameters

Update {component_file} at line {n}:

FROM:
```bash
{incorrect_call}
```

TO:
```bash
{correct_call}
```

**Reasoning**: {explanation of parameter error}
```

**If LLM Invented Script**:
```markdown
## Proposed Fix: Add Workflow Step

The LLM invented this script call because the workflow is missing a step.

Add to {component_file}:

### Step {n}: {step_name}

{workflow step with proper script call}

**Reasoning**: LLM tried to accomplish {goal} but no instruction existed.
```

**If Missing API**:
```markdown
## Proposed Fix: Create New Script

A new script API is needed:

**Script**: {notation}
**Subcommand**: {subcommand}
**Purpose**: {what operation is needed}

**Reasoning**: This operation is sensible for {context} but no script supports it.
```

### Step 6: Interactive Resolution

Present solutions using AskUserQuestion:

```
Based on my analysis, I found {n} script failure(s).

For each failure, which action would you like to take?
```

Options for each failure:
1. **Apply fix** - Apply the proposed fix to the component
2. **Record as lesson** - Document this analysis in lessons learned
3. **Skip** - Take no action for this failure

### Step 7: Apply Selected Actions

For each selected action:

**If Apply fix**:
- Use Edit tool to apply fix to component
- Verify fix applied correctly

**If Record as lesson**:
- Activate: `Skill: plan-marshall:manage-lessons-learned`
- Create lesson with:
  ```bash
  python3 .plan/execute-script.py plan-marshall:lessons-learned:manage-lesson add \
    --component "{source_component}" \
    --category "bug" \
    --title "Script failure: {short_description}" \
    --detail "{detailed analysis and solution}"
  ```

### Step 8: Summary

Display actions taken:

```
+================================================================+
|          Script Failure Analysis Complete                      |
+================================================================+

Failures analyzed: {total}
Fixes applied: {applied_count}
Lessons recorded: {lessons_count}
Skipped: {skipped_count}

Applied fixes:
- {component_1}: {fix_description}
- {component_2}: {fix_description}

Recorded lessons:
- {lesson_id}: {title}
```

## Critical Rules

**Analysis Accuracy**:
- Only report actual script failures (non-zero exits)
- Trace to exact source file and line number
- Read actual component files, don't assume content

**Script Identification**:
- Script calls match pattern: `python3 .plan/execute-script.py {notation}`
- Notation format: `{bundle}:{skill}:{script}`
- Parse full command including subcommand and arguments

**Context Extraction**:
- Show enough context (1-5 lines) to understand the instruction
- Don't expose unrelated conversation content
- Focus on the instruction path that led to failure

**Fix Safety**:
- Proposed fixes must be minimal and targeted
- Don't suggest unrelated improvements
- Preserve existing component structure

**Lessons Learned Integration**:
- Use `plan-marshall:lessons-learned` skill for recording
- Category should reflect nature: bug, improvement, anti-pattern
- Include enough detail for future reference

## Non-Prompting Requirements

This skill is designed to run without user prompts for analysis operations.

**File Operations:**
- `Read(marketplace/**)` - Read marketplace components
- `Grep(marketplace/**)` - Search for patterns
- `Glob(marketplace/**)` - Find files

**Prompting Behavior:**
- Analysis and tracing: Non-prompting
- Fix application: AskUserQuestion for user selection
- Lessons learned: Uses script API (non-prompting)
