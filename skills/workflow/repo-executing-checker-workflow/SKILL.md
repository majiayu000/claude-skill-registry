---
description: Step-by-step validation workflow for checker agents - initialize report, discover content, validate progressively, finalize with summary. Use when implementing or updating checker agents.
---

# Executing Checker Workflow

Common workflow pattern for all checker agents in the maker-checker-fixer three-stage quality pipeline.

## When This Skill Loads

This Skill auto-loads for checker agents that need standardized workflow for validating content and generating audit reports.

## Core Checker Workflow

Checker agents follow a consistent 5-step workflow:

```
Step 0: Initialize Report
    ↓
Step 1-N: Validate Content (domain-specific)
    ↓
Final Step: Finalize Report
```

### Step 0: Initialize Report File

**CRITICAL FIRST STEP - Execute before any validation begins:**

See `wow-generating-validation-reports` Skill for complete UUID chain generation and report initialization.

**Quick Implementation**:

```bash
# 1. Generate 6-char UUID
MY_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | head -c 6)

# 2. Determine UUID chain (scope-based)
SCOPE="${EXECUTION_SCOPE:-agent-family}"
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

# 3. Generate UTC+7 timestamp
TIMESTAMP=$(TZ='Asia/Jakarta' date +"%Y-%m-%d--%H-%M")

# 4. Create report filename
REPORT_FILE="generated-reports/${AGENT_FAMILY}__${UUID_CHAIN}__${TIMESTAMP}__audit.md"

# 5. Initialize report with header
cat > "$REPORT_FILE" << 'HEADER'
# Validation Report: {Agent Name}

**Status**: In Progress
**Agent**: {agent-name}
**Scope**: {scope-description}
**Timestamp**: {YYYY-MM-DD--HH-MM UTC+7}
**UUID Chain**: {uuid-chain}

---

## Findings

[Findings will be written progressively during validation]
HEADER
```

**Why Initialize Early?**

- Creates file before validation begins (survives context compaction)
- Enables progressive writing (append findings as discovered)
- Provides audit trail even if validation interrupted
- File is readable throughout execution

### Steps 1-N: Validate Content (Domain-Specific)

**Pattern**: Each checker has domain-specific validation steps, but all follow progressive writing.

**Common Validation Step Structure**:

```markdown
### Step {N}: {Validation Type}

**Objective**: {What this step validates}

**Process**:

1. {Discovery action - e.g., "Find all markdown files"}
2. {Extraction action - e.g., "Extract code blocks"}
3. {Validation action - e.g., "Verify against standards"}
4. **Write findings immediately** (progressive writing)

**Success Criteria**: {How to know step completed}

**On Failure**: {Error handling}
```

**Progressive Writing Requirements**:

- Write each finding to report file immediately after discovery
- Don't buffer findings in memory
- Use append mode for file writes
- Include all finding details (file, line, criticality, issue, recommendation)

**Finding Format**:

```markdown
### Finding {N}: {Title}

**File**: path/to/file.md
**Line**: {line-number} (if applicable)
**Criticality**: {CRITICAL/HIGH/MEDIUM/LOW}
**Category**: {category-name}

**Issue**: {Description of what's wrong}

**Recommendation**: {How to fix it}

---
```

### Common Validation Steps by Checker Type

**Content Quality Checkers** (docs, readme, tutorial):

1. Step 1: Discovery - Find files to validate
2. Step 2: Structure - Check heading hierarchy, frontmatter
3. Step 3: Content Quality - Verify active voice, accessibility, formatting
4. Step 4: Standards Compliance - Check against conventions
5. Step 5: Cross-References - Validate internal links

**Factual Accuracy Checkers** (docs, facts):

1. Step 1: Discovery - Find files with verifiable claims
2. Step 2: Extraction - Extract commands, versions, code examples
3. Step 3: Verification - Check claims against authoritative sources (WebSearch/WebFetch)
4. Step 4: Classification - Mark as [Verified]/[Error]/[Outdated]/[Unverified]
5. Step 5: Confidence Assessment - Assign confidence levels

**Link Checkers** (link-general, link-specific):

1. Step 1: Discovery - Find all markdown files
2. Step 2: Extraction - Extract internal and external links
3. Step 3: Internal Validation - Check internal references exist
4. Step 4: External Validation - Check external URLs accessible
5. Step 5: Cache Management - Update link cache

**Structure Checkers** (structure, navigation):

1. Step 1: Discovery - Find folder structure
2. Step 2: Organization - Validate folder patterns
3. Step 3: Weights - Check weight ordering system
4. Step 4: Navigation - Verify prev/next links
5. Step 5: Completeness - Check for missing files

### Final Step: Finalize Report

**Final update to existing report file:**

```bash
# Update report status
cat >> "$REPORT_FILE" << 'SUMMARY'

## Summary

**Total Findings**: {N}

**By Criticality**:
- CRITICAL: {count}
- HIGH: {count}
- MEDIUM: {count}
- LOW: {count}

**Status**: Complete
**Completed**: {YYYY-MM-DD--HH-MM UTC+7}
SUMMARY
```

**Finalization Checklist**:

1. Update status: "In Progress" → "Complete"
2. Count findings by criticality level
3. Add completion timestamp
4. Ensure all findings written to file (progressive writing)
5. Report file path to user

## Tool Requirements

Checkers typically need:

- **Read**: Read files to validate
- **Glob**: Find files by pattern
- **Grep**: Extract content patterns (code blocks, commands, etc.)
- **Write**: Initialize and update report file
- **Bash**: Generate UUID, timestamp, file operations
- **WebFetch**: (Optional) Access official documentation
- **WebSearch**: (Optional) Find authoritative sources

**Bash Tool Critical**: Required for UUID generation and report initialization.

## Integration with Other Skills

**Required Skills** (should be in checker's `skills:` frontmatter):

- `wow-generating-validation-reports` - UUID chain, report format, progressive writing
- `wow-assessing-criticality-confidence` - Criticality level assessment
- Domain-specific Skills (e.g., `docs-validating-factual-accuracy`, `docs-validating-links`)

**Related Documentation**:

- [Temporary Files Convention](../../../../governance/development/infra/temporary-files.md)
- [Maker-Checker-Fixer Pattern](../../../../governance/development/pattern/maker-checker-fixer.md)
- [Criticality Levels Convention](../../../../governance/development/quality/criticality-levels.md)

## Progressive Writing Methodology

**CRITICAL REQUIREMENT**: All checkers MUST write findings progressively.

**Why Progressive Writing?**

- Context compaction during long validation runs can lose buffered findings
- Progressive writing ensures audit history survives
- File is readable during execution (monitoring)
- Findings preserved even if validation interrupted

**Implementation Pattern**:

```markdown
Step 0: Initialize Report File
→ Create file immediately with header

Steps 1-N: Validate Content
→ For each validation check: 1. Perform validation 2. Immediately append finding to report file 3. Continue to next check
→ DO NOT buffer findings in memory

Final Step: Finalize Report
→ Update status and add summary
→ File already contains all findings
```

**Anti-Pattern (Don't Do This)**:

```python
# ❌ BAD: Buffering findings in memory
findings = []
for file in files:
    issue = validate(file)
    findings.append(issue)  # Buffered in memory!

# Write all at end (lost if context compacts)
write_report(findings)
```

**Correct Pattern**:

```python
# ✅ GOOD: Progressive writing
initialize_report()
for file in files:
    issue = validate(file)
    append_to_report(issue)  # Written immediately!

finalize_report()
```

## Common Validation Patterns

### Pattern 1: File-Based Validation

```markdown
Step 1: Discover files using Glob
Step 2: For each file:

- Read content
- Check against standards
- Write findings immediately
  Step 3: Finalize with summary
```

### Pattern 2: Content Extraction and Verification

```markdown
Step 1: Discover files
Step 2: Extract verifiable claims using Grep
Step 3: For each claim:

- Verify against source (WebFetch/WebSearch)
- Assess correctness
- Write finding immediately
  Step 4: Finalize with summary
```

### Pattern 3: Cross-Reference Validation

```markdown
Step 1: Build index of all valid targets
Step 2: Discover files with references
Step 3: For each reference:

- Check against index
- Verify target exists
- Write finding if broken
  Step 4: Finalize with summary
```

## Criticality Assessment

See `wow-assessing-criticality-confidence` Skill for complete guidance.

**Quick Guidelines**:

- **CRITICAL**: Breaks functionality, renders content unusable
- **HIGH**: Significant impact, misleads users, violates core standards
- **MEDIUM**: Quality issues, minor violations, subjective improvements
- **LOW**: Cosmetic issues, suggestions, optional improvements

**Domain-Specific Examples** (add to checker agent, not this Skill):

Each checker should include domain-specific criticality examples relevant to its validation scope.

## Best Practices

1. **Initialize Early**: Create report file before any validation
2. **Write Progressively**: Append findings immediately, don't buffer
3. **Use Bash Tools**: Required for UUID and timestamp generation
4. **Follow Naming**: Use 4-part pattern with UUID chain
5. **Update Status**: "In Progress" during validation, "Complete" when done
6. **Count Findings**: Provide summary by criticality level
7. **Be Specific**: Include file paths, line numbers, clear recommendations
8. **Assess Criticality**: Use consistent criteria across checkers

## Example Workflow Execution

```markdown
Step 0: Initialize Report
→ UUID: a1b2c3
→ Timestamp: 2025-12-14--20-45
→ File: docs**a1b2c3**2025-12-14--20-45\_\_audit.md
→ Status: In Progress

Step 1: Discover Files
→ Found 15 markdown files in docs/

Step 2: Validate Structure
→ File 1: Check heading hierarchy → MEDIUM finding → Write immediately
→ File 2: Check frontmatter → HIGH finding → Write immediately
→ ...continue for all files

Step 3: Validate Content
→ File 1: Check active voice → LOW finding → Write immediately
→ ...continue validation

Step 4: Validate Links
→ Extract 50 links
→ Validate each → 3 CRITICAL findings → Write immediately

Final Step: Finalize Report
→ Update status: Complete
→ Add summary: 1 CRITICAL, 2 HIGH, 4 MEDIUM, 3 LOW
→ Total: 10 findings
```

## Key Takeaways

- **Initialize first**: Create report before validation begins
- **Write progressively**: Append findings immediately during validation
- **Use consistent format**: Follow 4-part naming with UUID chains
- **Be domain-specific**: Customize Steps 1-N for validation type
- **Finalize completely**: Update status and add summary statistics
- **Require Bash**: Essential for UUID and timestamp generation
- **Trust the pattern**: All checkers follow this workflow structure

This workflow ensures consistent, auditable, and resilient validation across all checker agents.
