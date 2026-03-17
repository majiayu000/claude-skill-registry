---
name: repo-generating-validation-reports
description: Guidelines for generating validation/audit reports with UUID chains, progressive writing, and UTC+7 timestamps
---

# Generating Validation Reports

Generate validation and audit reports following repository standards for naming, progressive writing, and UUID-based execution tracking.

## When This Skill Loads

This Skill auto-loads for checker and fixer agents that need to generate validation reports in `generated-reports/`.

## Core Knowledge

### Report File Naming Pattern

All reports follow the 4-part pattern:

```
{agent-family}__{uuid-chain}__{YYYY-MM-DD--HH-MM}__{type}.md
```

**Components**:

- `{agent-family}`: Agent name WITHOUT `-checker` suffix (e.g., `docs`, `ayokoding-web`, `plan`)
- `{uuid-chain}`: Execution hierarchy as 6-char hex UUIDs separated by underscores
- `{YYYY-MM-DD--HH-MM}`: UTC+7 timestamp (double dash between date and time)
- `{type}`: Report type (`audit`, `validation`, `fix`)

**Examples**:

```
generated-reports/docs__a1b2c3__2026-01-03--14-30__audit.md
generated-reports/plan__d4e5f6__2026-01-03--15-00__validation.md
generated-reports/ayokoding-facts__a1b2c3_d4e5f6__2026-01-03--16-45__audit.md
```

### UUID Generation

Generate 6-character hexadecimal UUID at agent startup:

```bash
MY_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)
# Example output: a1b2c3
```

**Why 6 characters?**

- 16^6 = 16,777,216 combinations
- Collision probability for 1000 parallel executions: ~0.003%
- Short for readability, long enough for uniqueness

### UUID Chain Logic

**Scope-based execution tracking** enables parent-child hierarchy:

**Tracking File Pattern**: `generated-reports/.execution-chain-{scope}`

**Startup Logic**:

```bash
# 1. Generate own UUID
MY_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)

# 2. Determine scope (from EXECUTION_SCOPE or default to agent-family)
SCOPE="${EXECUTION_SCOPE:-docs}"

# 3. Read parent chain from scope tracking file
CHAIN_FILE="generated-reports/.execution-chain-${SCOPE}"
if [ -f "$CHAIN_FILE" ]; then
  read PARENT_TIME PARENT_CHAIN < "$CHAIN_FILE"
  CURRENT_TIME=$(date +%s)
  TIME_DIFF=$((CURRENT_TIME - PARENT_TIME))

  # If parent is recent (< 5 min), append to chain
  if [ $TIME_DIFF -lt 300 ]; then
    UUID_CHAIN="${PARENT_CHAIN}_${MY_UUID}"
  else
    UUID_CHAIN="$MY_UUID"  # Start new chain
  fi
else
  UUID_CHAIN="$MY_UUID"  # First execution
fi

# 4. Write own chain to tracking file
echo "$(date +%s) $UUID_CHAIN" > "$CHAIN_FILE"
```

**Chain Examples**:

- `a1b2c3` - Root execution (no parent)
- `a1b2c3_d4e5f6` - Child of a1b2c3
- `a1b2c3_d4e5f6_g7h8i9` - Grandchild (2 levels deep)

### UTC+7 Timestamp Generation

Generate timestamp in UTC+7 timezone:

```bash
TIMESTAMP=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")
# Example output: 2026-01-03--14-30
```

**Format**: `YYYY-MM-DD--HH-MM` (double dash between date and time for filesystem compatibility)

### Progressive Writing Methodology

**CRITICAL REQUIREMENT**: All checker agents MUST write findings progressively, not buffer and write once at end.

**Why?** Context compaction during long validation runs can lose buffered findings. Progressive writing ensures audit history survives.

**Implementation Pattern**:

```markdown
Step 0: Initialize Report File

- Generate UUID and chain
- Create report file immediately
- Write header with "In Progress" status

Steps 1-N: Validate Content

- For each validation check:
  1. Perform validation
  2. Immediately write finding to report file (append mode)
  3. Continue to next check
- DO NOT buffer findings in memory

Final Step: Finalize Report

- Update status from "In Progress" to "Complete"
- Add summary statistics
- File already contains all findings from progressive writing
```

### Report Template Structure

**Initial Header** (Step 0):

```markdown
# Validation Report: [Agent Name]

**Status**: In Progress
**Agent**: [agent-name]
**Scope**: [scope-description]
**Timestamp**: [YYYY-MM-DD--HH-MM UTC+7]
**UUID Chain**: [uuid-chain]

---

## Findings

[Findings will be written progressively during validation]
```

**Progressive Findings** (Steps 1-N):

```markdown
### Finding [N]: [Title]

**File**: path/to/file.md
**Line**: 123
**Criticality**: HIGH
**Category**: [category-name]

**Issue**: [Description of what's wrong]

**Recommendation**: [How to fix it]

---
```

**Final Summary** (Last Step):

```markdown
## Summary

**Total Findings**: [N]

- CRITICAL: [count]
- HIGH: [count]
- MEDIUM: [count]
- LOW: [count]

**Status**: Complete
**Completed**: [YYYY-MM-DD--HH-MM UTC+7]
```

### Scope Definitions

Common scopes for execution tracking:

| Agent Family             | Scope              | Tracking File                       |
| ------------------------ | ------------------ | ----------------------------------- |
| wow\_\_rules-checker     | `repo-rules`       | `.execution-chain-repo-rules`       |
| docs\_\_checker          | `docs`             | `.execution-chain-docs`             |
| docs\_\_tutorial-checker | `docs-tutorial`    | `.execution-chain-docs-tutorial`    |
| readme\_\_checker        | `readme`           | `.execution-chain-readme`           |
| plan\_\_checker          | `plan`             | `.execution-chain-plan`             |
| ayokoding-web-\*         | `ayokoding-[lang]` | `.execution-chain-ayokoding-[lang]` |
| ose-platform-web-\*      | `ose-platform`     | `.execution-chain-ose-platform`     |

### Tool Requirements

Agents using this Skill MUST have:

- **Write tool**: Required for creating report files
- **Bash tool**: Required for UUID generation and UTC+7 timestamps

**Example frontmatter**:

```yaml
---
name: example-checker
tools: [Read, Glob, Grep, Write, Bash]
skills: [wow__generating-validation-reports]
---
```

## Reference Documentation

Complete specifications in:

- [Temporary Files Convention](../../../governance/development/infra/temporary-files.md)
- [Timestamp Format Convention](../../../governance/conventions/formatting/timestamp.md)
- [File Naming Convention](../../../governance/conventions/structure/file-naming.md)

## Usage Example

**Checker Agent Startup**:

```bash
# Generate UUID and determine chain
MY_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)
SCOPE="${EXECUTION_SCOPE:-docs}"
CHAIN_FILE="generated-reports/.execution-chain-${SCOPE}"

if [ -f "$CHAIN_FILE" ]; then
  read PARENT_TIME PARENT_CHAIN < "$CHAIN_FILE"
  CURRENT_TIME=$(date +%s)
  TIME_DIFF=$((CURRENT_TIME - PARENT_TIME))

  if [ $TIME_DIFF -lt 300 ]; then
    UUID_CHAIN="${PARENT_CHAIN}_${MY_UUID}"
  else
    UUID_CHAIN="$MY_UUID"
  fi
else
  UUID_CHAIN="$MY_UUID"
fi

echo "$(date +%s) $UUID_CHAIN" > "$CHAIN_FILE"

# Generate timestamp
TIMESTAMP=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")

# Create report filename
REPORT_FILE="generated-reports/docs__${UUID_CHAIN}__${TIMESTAMP}__audit.md"

# Initialize report (progressive writing starts here)
cat > "$REPORT_FILE" << 'REPORT_HEADER'
# Validation Report: docs__checker

**Status**: In Progress
**Agent**: docs__checker
**Scope**: Documentation validation
**Timestamp**: [timestamp]
**UUID Chain**: [uuid-chain]

---

## Findings

REPORT_HEADER

# Continue with validation, writing findings progressively...
```

## Key Principles

1. **Generate UUID early**: First thing at agent startup
2. **Initialize report immediately**: Before any validation begins
3. **Write progressively**: Append findings as you discover them
4. **Use UTC+7 timestamps**: Consistent timezone across all reports
5. **Follow 4-part naming**: Agent-family, UUID chain, timestamp, type
6. **Track execution scope**: Enable parent-child hierarchy for workflows
7. **Require Write+Bash tools**: Essential for report generation

## Common Mistakes to Avoid

❌ **Buffering findings**: Don't collect all findings in memory and write at end (context compaction risk)
✅ **Progressive writing**: Write each finding immediately after discovery

❌ **Wrong timestamp format**: Don't use `YYYY-MM-DD HH:MM` (spaces in filenames)
✅ **Correct format**: Use `YYYY-MM-DD--HH-MM` (double dash separator)

❌ **Missing UUID chain**: Don't use timestamp alone for uniqueness
✅ **UUID chain**: Enables parallel execution without collisions

❌ **Generic scope**: Don't use same scope for all agents
✅ **Specific scope**: Use agent-family or language-specific scope

## Integration with Other Skills

Works alongside:

- `wow__assessing-criticality-confidence` - Categorize findings by severity
- `wow__applying-maker-checker-fixer` - Fixer agents read these reports
- Domain Skills (`apps__ayokoding-web__developing-content`, etc.) - Provide validation criteria

## Benefits

1. **Parallelization-safe**: UUID chains prevent file collisions
2. **Traceable**: Can track parent-child execution hierarchy
3. **Resilient**: Progressive writing survives context compaction
4. **Consistent**: Standard naming across all checker agents
5. **Debuggable**: Timestamp and UUID chain aid troubleshooting
