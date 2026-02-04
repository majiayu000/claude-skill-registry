---
name: validate-report-file
description: Validate that worker-generated reports have all required sections and proper formatting. Use in quality gates, for report completeness checking, or when debugging missing report sections.
allowed-tools: Read
---

# Validate Report File

Validate agent-generated report files for completeness and proper structure.

## When to Use

- Quality gate validation after worker completion
- Debugging missing report sections
- Ensuring report consistency
- Pre-submission validation

## Instructions

### Step 1: Read Report File

Use Read tool to load report file.

**Expected Input**:

- `file_path`: Path to report file (e.g., `bug-hunting-report.md`)

**Tools Used**: Read

### Step 2: Check Required Sections

Verify all required sections are present.

**Required Sections**:

1. **Header** with metadata:
   - Title (# Report Type Report: Version)
   - Generated timestamp
   - Status indicator (✅/⚠️/❌)
   - Version identifier

2. **Executive Summary**:
   - ## Executive Summary heading
   - Key metrics and findings

3. **Detailed Findings**:
   - Varies by report type
   - Must have at least one detail section

4. **Validation Results**:
   - ## Validation Results heading
   - Build/type-check status
   - Overall validation status

5. **Next Steps**:
   - ## Next Steps heading
   - Action items or recommendations

### Step 3: Validate Format

Check formatting and structure.

**Format Rules**:

- Title must be H1 (single #)
- Section headers must be H2 (##)
- Status must include emoji (✅/⚠️/❌)
- Code blocks must use proper markdown
- Lists must be properly formatted

### Step 4: Check Status Consistency

Verify status indicators are consistent.

**Consistency Checks**:

- Header status matches validation status
- If status is "failed", validation should show failures
- If status is "success", validation should show passes

### Step 5: Return Validation Result

Return detailed validation result.

**Expected Output**:

```json
{
  "valid": true,
  "file": "bug-hunting-report.md",
  "sections": {
    "header": true,
    "executiveSummary": true,
    "detailedFindings": true,
    "validationResults": true,
    "nextSteps": true
  },
  "warnings": [],
  "errors": []
}
```

## Error Handling

- **File Not Found**: Return error with file path
- **Missing Sections**: List all missing required sections
- **Invalid Format**: Describe format issues
- **Inconsistent Status**: Warn about status mismatches

## Examples

### Example 1: Valid Report

**Input**:

```
file_path: bug-hunting-report.md
```

**File Content**:

```markdown
# Bug Hunting Report: 2025-10-17

**Generated**: 2025-10-17 14:30:00 UTC
**Status**: ✅ success

---

## Executive Summary

Found 23 bugs across 147 files.

## Detailed Findings

### Critical (3)

- Bug 1
- Bug 2
- Bug 3

## Validation Results

- Type-check: ✅ PASSED
- Build: ✅ PASSED

**Overall**: ✅ PASSED

## Next Steps

1. Review critical bugs
2. Schedule fixes
```

**Output**:

```json
{
  "valid": true,
  "file": "bug-hunting-report.md",
  "sections": {
    "header": true,
    "executiveSummary": true,
    "detailedFindings": true,
    "validationResults": true,
    "nextSteps": true
  },
  "warnings": [],
  "errors": []
}
```

### Example 2: Missing Sections

**Input**:

```
file_path: incomplete-report.md
```

**File Content**:

```markdown
# Bug Report

Some bugs found.
```

**Output**:

```json
{
  "valid": false,
  "file": "incomplete-report.md",
  "sections": {
    "header": false,
    "executiveSummary": false,
    "detailedFindings": false,
    "validationResults": false,
    "nextSteps": false
  },
  "warnings": [],
  "errors": [
    "Missing header metadata (Generated, Status, Version)",
    "Missing section: Executive Summary",
    "Missing section: Detailed Findings",
    "Missing section: Validation Results",
    "Missing section: Next Steps"
  ]
}
```

### Example 3: Inconsistent Status

**Input**:

```
file_path: inconsistent-report.md
```

**File Content**:

```markdown
# Bug Report: 2025-10-17

**Status**: ✅ success

## Executive Summary

Failed to scan files.

## Validation Results

**Overall**: ❌ FAILED
```

**Output**:

```json
{
  "valid": false,
  "file": "inconsistent-report.md",
  "sections": {
    "header": true,
    "executiveSummary": true,
    "detailedFindings": false,
    "validationResults": true,
    "nextSteps": false
  },
  "warnings": ["Status inconsistency: Header shows success (✅) but validation shows failed (❌)"],
  "errors": ["Missing section: Detailed Findings", "Missing section: Next Steps"]
}
```

## Validation

- [ ] Checks all required sections present
- [ ] Validates header metadata
- [ ] Verifies status consistency
- [ ] Detects format issues
- [ ] Returns clear error messages
- [ ] Handles missing files gracefully

## Supporting Files

- `schema.json`: Report structure schema (see Supporting Files section)
