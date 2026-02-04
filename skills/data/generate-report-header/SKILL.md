---
name: generate-report-header
description: Create standardized report headers with metadata for all agent-generated reports. Use when generating bug reports, security audits, dependency reports, or any worker output requiring consistent formatting.
---

# Generate Report Header

Create consistent, well-formatted headers for all agent-generated reports with proper metadata.

## When to Use

- Beginning of all worker-generated reports
- Summary documents
- Validation reports
- Audit reports
- Any standardized output requiring header

## Instructions

### Step 1: Collect Header Information

Gather required information for header.

**Expected Input**:

- `reportType`: String (e.g., "Bug Hunting", "Security Audit", "Version Update")
- `version`: String (e.g., "0.8.0", "2025-10-17", "final")
- `status`: String (success|partial|failed|in_progress)
- `timestamp`: String (optional, ISO-8601 format, defaults to current time)
- `duration`: String (optional, e.g., "3m 45s", "1h 12m")
- `workflow`: String (optional, e.g., "bugs", "security", "dead-code", "dependencies")
- `phase`: String (optional, e.g., "detection", "fixing", "verification")
- `additionalMetadata`: Object (optional, extra fields)

### Step 2: Format Timestamp

Convert timestamp to readable format if needed.

**Format**: "YYYY-MM-DD HH:mm:ss UTC"

**Example**: "2025-10-17 14:30:00 UTC"

### Step 3: Determine Status Emoji

Map status to appropriate emoji.

**Status Mapping**:

- `success`: ✅
- `partial`: ⚠️
- `failed`: ❌
- `in_progress`: 🔄

### Step 4: Generate Header

Create formatted markdown header.

**Expected Output**:

```markdown
# {ReportType} Report: {Version}

**Generated**: {Timestamp}
**Status**: {StatusEmoji} {Status}
**Version**: {Version}
**Duration**: {Duration} (if provided)
**Workflow**: {Workflow} (if provided)
**Phase**: {Phase} (if provided)

---

## Executive Summary
```

**Standard Metrics** (include when available):

- Timestamp (ISO-8601)
- Duration (human-readable)
- Workflow (domain: bugs, security, dead-code, dependencies)
- Phase (detection, fixing, verification)
- Validation Status (✅ PASSED, ⛔ FAILED, ⚠️ PARTIAL)

### Step 5: Add Optional Metadata

Include additional metadata fields if provided.

**Optional Fields**:

- Agent name
- Duration
- File count
- Issue count
- Any custom fields

## Error Handling

- **Missing Report Type**: Return error requesting report type
- **Invalid Status**: Return error listing valid statuses
- **Invalid Timestamp**: Use current time and warn

## Examples

### Example 1: Bug Hunting Report

**Input**:

```json
{
  "reportType": "Bug Hunting",
  "version": "2025-10-17",
  "status": "success",
  "additionalMetadata": {
    "agent": "bug-hunter",
    "filesScanned": 147,
    "bugsFound": 23
  }
}
```

**Output**:

```markdown
# Bug Hunting Report: 2025-10-17

**Generated**: 2025-10-17 14:30:00 UTC
**Status**: ✅ success
**Version**: 2025-10-17
**Agent**: bug-hunter
**Files Scanned**: 147
**Bugs Found**: 23

---

## Executive Summary
```

### Example 2: Version Update Report

**Input**:

```json
{
  "reportType": "Version Update",
  "version": "0.7.0 → 0.8.0",
  "status": "success"
}
```

**Output**:

```markdown
# Version Update Report: 0.7.0 → 0.8.0

**Generated**: 2025-10-17 14:30:00 UTC
**Status**: ✅ success
**Version**: 0.7.0 → 0.8.0

---

## Executive Summary
```

### Example 3: Security Audit (Partial)

**Input**:

```json
{
  "reportType": "Security Audit",
  "version": "final",
  "status": "partial",
  "timestamp": "2025-10-17T14:30:00Z",
  "additionalMetadata": {
    "criticalIssues": 2,
    "highIssues": 5,
    "fixedIssues": 5
  }
}
```

**Output**:

```markdown
# Security Audit Report: final

**Generated**: 2025-10-17 14:30:00 UTC
**Status**: ⚠️ partial
**Version**: final
**Critical Issues**: 2
**High Issues**: 5
**Fixed Issues**: 5

---

## Executive Summary
```

### Example 4: Failed Dependency Update

**Input**:

```json
{
  "reportType": "Dependency Update",
  "version": "2025-10-17",
  "status": "failed",
  "additionalMetadata": {
    "error": "npm install failed",
    "failedPackages": ["package-a", "package-b"]
  }
}
```

**Output**:

```markdown
# Dependency Update Report: 2025-10-17

**Generated**: 2025-10-17 14:30:00 UTC
**Status**: ❌ failed
**Version**: 2025-10-17
**Error**: npm install failed
**Failed Packages**: package-a, package-b

---

## Executive Summary
```

## Validation

- [ ] Generates header with all required fields
- [ ] Formats timestamp correctly
- [ ] Maps status to correct emoji
- [ ] Includes additional metadata when provided
- [ ] Validates status values
- [ ] Uses current time if timestamp missing

## Supporting Files

- `template.md`: Report header template (see Supporting Files section)
