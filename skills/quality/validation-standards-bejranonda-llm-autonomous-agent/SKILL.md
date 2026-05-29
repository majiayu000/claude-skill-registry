---
name: validation-standards
description: Tool usage requirements, failure patterns, consistency checks, and validation methodologies for Claude Code operations
version: 1.0.0
---

## Overview

This skill provides comprehensive validation standards for Claude Code tool usage, documentation consistency, and execution flow validation. It defines rules for detecting failures before they occur, identifying common error patterns, and ensuring compliance with best practices.

**When to apply**: Before any file modification, after errors occur, during documentation updates, or when ensuring quality and consistency.

## Tool Usage Validation Standards

### Edit Tool Requirements

**Rule**: Must read file before editing
```
REQUIRED SEQUENCE:
1. Read(file_path)
2. Edit(file_path, old_string, new_string)

VIOLATION SYMPTOMS:
- Error: "File has not been read yet"
- Error: "Read it first before writing"

PREVENTION:
- Track files read in current session
- Validate Read was called before Edit
- Maintain session state of file operations

AUTO-FIX:
IF Edit fails with "not read yet" error
THEN Call Read(file_path) first
THEN Retry Edit operation
```

**Rule**: old_string must exist and be unique
```
REQUIRED:
- old_string appears in file exactly once
- OR use replace_all=true for multiple occurrences

VIOLATION SYMPTOMS:
- Error: "old_string not found"
- Error: "old_string not unique"

PREVENTION:
- Use larger context for uniqueness
- Search file content before editing
- Verify exact match with line numbers

AUTO-FIX:
IF old_string not unique
THEN Expand context with surrounding lines
OR Use replace_all=true parameter
```

### Write Tool Requirements

**Rule**: Read before overwriting existing files
```
REQUIRED FOR EXISTING FILES:
1. Check if file exists (Glob or Bash ls)
2. If exists: Read(file_path) first
3. Then Write(file_path, content)

VIOLATION SYMPTOMS:
- Error: "File has not been read yet"
- Warning: "Overwriting without reading"

PREVENTION:
- Always check file existence first
- Read existing files before writing
- Use Edit instead of Write for modifications

BEST PRACTICE:
- Write: Only for new files
- Edit: For modifying existing files
```

**Rule**: Verify parent directory exists
```
REQUIRED:
- Parent directory must exist before Write
- Use Bash mkdir -p if needed

VIOLATION SYMPTOMS:
- Error: "No such file or directory"
- Error: "Parent directory doesn't exist"

PREVENTION:
- Verify directory structure before Write
- Create directories with mkdir -p
- Use absolute paths to avoid ambiguity

AUTO-FIX:
Extract parent directory from file_path
Check if parent exists
If not: mkdir -p parent_directory
Then: Proceed with Write
```

### NotebookEdit Tool Requirements

**Rule**: Verify cell ID exists
```
REQUIRED:
- cell_id must exist in notebook
- For insert: Specify position or cell_id
- For delete: cell_id must be valid

PREVENTION:
- Read notebook structure first
- Verify cell_id in notebook
- Check cell_type matches operation
```

### Bash Tool Requirements

**Rule**: Use specialized tools instead of Bash
```
PREFER SPECIALIZED TOOLS:
- Read instead of cat/head/tail
- Edit instead of sed/awk
- Write instead of echo > or cat <<EOF
- Grep instead of grep/rg commands
- Glob instead of find/ls

EXCEPTION:
Only use Bash when specialized tool unavailable
- git operations
- npm/pip package managers
- docker/system commands
```

**Rule**: Chain dependent commands with &&
```
REQUIRED FOR DEPENDENCIES:
command1 && command2 && command3

VIOLATION:
command1; command2; command3  # Continues on failure

PREVENTION:
- Use && for sequential dependencies
- Use ; only when failures acceptable
- Use parallel calls for independent commands
```

## Documentation Consistency Standards

### Version Consistency

**Rule**: Synchronize versions across all files
```
FILES REQUIRING VERSION SYNC:
1. .claude-plugin/plugin.json → "version": "X.Y.Z"
2. CHANGELOG.md → ## [X.Y.Z] - YYYY-MM-DD
3. README.md → Version mentions (if any)
4. pattern database → .metadata.plugin_version

VALIDATION:
- Extract version from each file
- Compare all versions
- Flag any mismatches

AUTO-FIX:
Identify canonical version (plugin.json)
Update all other references to match
Create consistency report
```

### Path Consistency

**Rule**: Use consistent paths across documentation
```
COMMON INCONSISTENCIES:
- Standardize to .claude-patterns/ throughout
- learned-patterns.json vs patterns.json
- relative vs absolute paths

VALIDATION:
- Grep for path patterns in all .md files
- Extract unique path variations
- Flag conflicting references

DETECTION REGEX:
\.claude[/-]patterns?/[a-z-]+\.json
\.claude[/-][a-z-]+/

AUTO-FIX:
Determine actual implementation path
Replace all variations with canonical path
Update all documentation files
Verify consistency across project
```

### Component Count Accuracy

**Rule**: Documentation matches actual component counts
```
COMPONENTS TO COUNT:
- Agents: Count agents/*.md files
- Skills: Count skills/*/SKILL.md files
- Commands: Count commands/*.md files

VALIDATION:
actual_agents = count(agents/*.md)
actual_skills = count(skills/*/SKILL.md)
actual_commands = count(commands/*.md)

FOR EACH doc IN [README, CHANGELOG, CLAUDE.md]:
  Extract mentioned counts
  Compare with actual counts
  Flag discrepancies

AUTO-FIX:
Update documentation with actual counts
Add note about component inventory
```

### Cross-Reference Integrity

**Rule**: All referenced files/components must exist
```
REFERENCE TYPES:
- File paths: "See `path/to/file.md`"
- Components: "uses `agent-name` agent"
- Skills: "leverages `skill-name` skill"
- Commands: "run `/command-name`"

VALIDATION:
- Extract all references
- Verify each target exists
- Check naming matches exactly

DETECTION:
- Markdown links: [text](path)
- Inline code: `filename.ext`
- Component names: agent-name, skill-name

AUTO-FIX:
IF reference broken
THEN Search for similar names
OR Remove reference with note
OR Create missing component
```

## Execution Flow Validation

### Dependency Tracking

**Session State Management**:
```python
session_state = {
  "files_read": set(),
  "files_written": set(),
  "tools_used": [],
  "errors_encountered": []
}

# Update on each operation
def track_operation(tool, file_path, result):
    if tool == "Read" and result.success:
        session_state["files_read"].add(file_path)
    elif tool in ["Write", "Edit"]:
        session_state["files_written"].add(file_path)
    session_state["tools_used"].append({
        "tool": tool,
        "file": file_path,
        "timestamp": now(),
        "success": result.success
    })
    if not result.success:
        session_state["errors_encountered"].append({
            "tool": tool,
            "file": file_path,
            "error": result.error_message
        })
```

**Pre-flight Validation**:
```python
def validate_edit(file_path):
    if file_path not in session_state["files_read"]:
        return {
            "valid": False,
            "error": "File has not been read yet",
            "fix": f"Call Read('{file_path}') first"
        }
    return {"valid": True}

def validate_write(file_path):
    file_exists = check_file_exists(file_path)
    if file_exists and file_path not in session_state["files_read"]:
        return {
            "valid": False,
            "warning": "Overwriting without reading",
            "recommendation": f"Read '{file_path}' before overwriting"
        }
    return {"valid": True}
```

### Error Pattern Detection

**Common Error Patterns**:

**Pattern 1: Edit Before Read**
```
Signature:
- Tool: Edit
- Error: "File has not been read yet"

Root Cause:
- Attempted Edit without prior Read

Detection:
- Monitor Edit tool results
- Check for specific error message
- Verify file_path not in files_read set

Auto-Fix:
1. Call Read(file_path)
2. Retry Edit with same parameters
3. Track successful recovery

Learning:
- Store pattern for future prevention
- Increment pre-flight validation confidence
```

**Pattern 2: Path Not Found**
```
Signature:
- Any file tool
- Error: "No such file or directory"

Root Cause:
- Invalid path or typo
- Parent directory doesn't exist

Detection:
- Monitor file operation results
- Parse error message for path issues

Auto-Fix:
1. Extract intended path
2. Use Glob to find similar paths
3. If new file: mkdir -p parent_directory
4. Suggest correct path or create directory
5. Retry operation

Learning:
- Store common typos
- Build path validation dictionary
```

**Pattern 3: Missing Required Parameters**
```
Signature:
- Any tool
- Error: "Required parameter missing"

Root Cause:
- Tool call incomplete
- Parameter name incorrect

Detection:
- Parse error for missing param name
- Check tool schema

Auto-Fix:
1. Identify missing parameter
2. Determine reasonable default or required value
3. Prompt for value if needed
4. Retry with complete parameters

Learning:
- Store tool parameter requirements
- Build parameter validation checklist
```

### State Recovery

**Error Recovery Protocol**:
```
ON ERROR DETECTED:
1. Capture error details
   - Tool name
   - Parameters used
   - Error message
   - Stack trace if available

2. Analyze error pattern
   - Match against known patterns
   - Identify root cause
   - Determine if auto-fixable

3. Apply auto-fix if available
   - Execute corrective action
   - Retry original operation
   - Verify success

4. Store failure pattern
   - Save to pattern database
   - Include fix that worked
   - Update prevention rules

5. Update session state
   - Mark error as resolved
   - Track recovery success
   - Continue execution
```

## Validation Methodologies

### Pre-Execution Validation

**Validation Checklist**:
```
BEFORE EDIT:
□ File has been read in session
□ old_string is unique (or replace_all set)
□ new_string differs from old_string
□ File path is valid

BEFORE WRITE:
□ Parent directory exists
□ If file exists: Has been read first
□ Content is not empty (unless intentional)
□ File path is absolute

BEFORE DOCUMENTATION UPDATE:
□ All related docs identified
□ Current versions extracted
□ Consistency check planned
□ Cross-references validated
```

### Post-Execution Validation

**Validation Checklist**:
```
AFTER FILE MODIFICATION:
□ Operation succeeded
□ Changes are as intended
□ No unintended side effects
□ Related files still consistent

AFTER DOCUMENTATION UPDATE:
□ Versions synchronized
□ Paths consistent
□ Component counts accurate
□ Cross-references valid
□ Examples match implementation
```

### Comprehensive Validation

**Full Project Validation**:
```
1. TOOL USAGE AUDIT
   - Review all tool calls in session
   - Identify any violations
   - Check for best practice compliance

2. DOCUMENTATION CONSISTENCY
   - Scan all .md files
   - Extract all paths, versions, counts
   - Identify inconsistencies
   - Generate consistency report

3. CROSS-REFERENCE CHECK
   - Extract all references
   - Verify all targets exist
   - Check naming accuracy
   - Flag broken links

4. PATTERN COMPLIANCE
   - Query pattern database
   - Compare current vs successful patterns
   - Identify deviations
   - Suggest improvements

5. GENERATE REPORT
   - Validation score (0-100)
   - Issues by severity
   - Recommendations prioritized
   - Auto-fix suggestions
```

## Failure Pattern Database Schema

```json
{
  "failure_patterns": [
    {
      "pattern_id": "edit-before-read-001",
      "error_signature": "File has not been read yet",
      "tool": "Edit",
      "root_cause": "Edit called without prior Read",
      "frequency": 15,
      "auto_fix": {
        "action": "call_read_first",
        "success_rate": 1.0
      },
      "prevention_rule": "validate_file_read_before_edit",
      "examples": [
        {
          "file": "plugin.json",
          "timestamp": "2025-10-21T12:00:00Z",
          "fixed": true
        }
      ]
    }
  ],
  "prevention_rules": {
    "validate_file_read_before_edit": {
      "description": "Check if file was read before attempting Edit",
      "enabled": true,
      "confidence": 1.0,
      "prevented_failures": 8
    }
  },
  "metrics": {
    "total_failures_detected": 23,
    "auto_fixed": 20,
    "prevention_rate": 0.87,
    "false_positives": 2
  }
}
```

## Validation Scoring

**Validation Score Calculation**:
```
Score (0-100) =
  Tool Usage Compliance      (30 points) +
  Documentation Consistency  (25 points) +
  Best Practices Adherence   (20 points) +
  Error-Free Execution       (15 points) +
  Pattern Compliance         (10 points)

GRADING:
90-100: Excellent - No issues
70-89:  Good - Minor issues only
50-69:  Fair - Several issues to address
0-49:   Poor - Major issues require attention

THRESHOLD:
Minimum acceptable: 70/100
```

## When to Apply This Skill

Apply validation standards in these scenarios:

1. **Before file modifications** - Pre-flight checks prevent common errors
2. **After errors occur** - Root cause analysis and auto-fix suggestions
3. **During documentation updates** - Ensure consistency across all docs
4. **On version changes** - Synchronize versions in all relevant files
5. **After adding components** - Update counts and references
6. **Periodic audits** - Comprehensive validation every 10-25 tasks
7. **Before releases** - Full validation ensures quality

## Integration with Other Skills

**Works with**:
- **quality-standards**: Combines validation with quality metrics
- **pattern-learning**: Learns from failures to prevent recurrence
- **code-analysis**: Validates code structure and patterns
- **documentation-best-practices**: Ensures doc quality and consistency

## Success Criteria

Validation is successful when:
- ✓ Zero tool usage violations detected
- ✓ All documentation paths consistent
- ✓ All version numbers synchronized
- ✓ All cross-references valid
- ✓ Component counts accurate
- ✓ Validation score ≥ 70/100
- ✓ Known failure patterns prevented
- ✓ Error recovery successful when needed
