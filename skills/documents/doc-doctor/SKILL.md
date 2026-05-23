---
name: doc-doctor
description: Diagnose documentation issues (format, links, content)
user-invocable: true
allowed-tools: Skill, Read, Glob, Grep, Bash
---

# Documentation Doctor Skill

Unified diagnostic skill for AsciiDoc documentation.

## Parameters

- **target** (optional): File or directory path (default: current directory)
- **depth** (optional): quick|standard|thorough (default: standard)
  - quick: format validation only
  - standard: format + link verification
  - thorough: format + links + content review

## Workflow

### Step 1: Parse Parameters

```
If no target specified:
  target = current directory

Validate depth:
  If depth not in [quick, standard, thorough]:
    depth = standard
```

**Usage:**
```
/doc-doctor [target=<path>] [depth=quick|standard|thorough]

Parameters:
  target - Optional: File (.adoc) or directory (default: .)
  depth  - Optional: Validation depth (default: standard)

Examples:
  /doc-doctor
  /doc-doctor target=standards/java-core.adoc
  /doc-doctor target=standards/ depth=thorough
  /doc-doctor depth=quick
```

### Step 2: Determine Scope

```
If target is file:
  Verify file exists and has .adoc extension
  scope = "single"
  files = [target]

If target is directory:
  Use Glob: {target}/**/*.adoc
  Filter out: target/, node_modules/, hidden directories
  scope = "batch"
  files = discovered files

If no files found:
  Report: "No AsciiDoc files found in {target}"
  Exit
```

### Step 3: Load Documentation Skill

```
Skill: pm-documents:ref-documentation
```

### Step 4: Execute Diagnostic

Map depth to workflow parameters:

| Depth | Format | Links | Content |
|-------|--------|-------|---------|
| quick | Y | N | N |
| standard | Y | Y | N |
| thorough | Y | Y | Y |

**For quick depth:**
```
Execute workflow: validate-format
Parameters:
  target: {target}
  apply_fixes: false
```

**For standard depth:**
```
Execute workflow: comprehensive-review
Parameters:
  target: {target}
  stop_on_error: false
  apply_fixes: false
  skip_content: true
```

**For thorough depth:**
```
Execute workflow: comprehensive-review
Parameters:
  target: {target}
  stop_on_error: false
  apply_fixes: false
  skip_content: false
```

### Step 5: Generate Diagnostic Report

```
═══════════════════════════════════════════════
Documentation Diagnostic Report
═══════════════════════════════════════════════

Scope: {file_count} file(s)
Depth: {depth}

Summary:
Y {clean_count} files clean
! {warning_count} files with warnings
X {error_count} files with errors

Issues by Category:
- Format: {format_issue_count}
- Links: {link_issue_count} (if depth >= standard)
- Content: {content_issue_count} (if depth = thorough)

{If file_count <= 10: show per-file details}

Files with Issues:
{file}: {issue_count} issues
  - Line {N}: {description}
```

## Architecture

**Pattern**: Thin Orchestrator (~100 lines)
- Parses parameters and determines scope
- Delegates ALL validation to ref-documentation skill
- No business logic in skill

**Skill Dependency**: pm-documents:ref-documentation
- Provides: validate-format, verify-links, review-content, comprehensive-review workflows

## Related

- `/doc-create` - Create new documentation from templates
- `/doc-maintain` - Maintain existing documentation
- `ref-documentation` skill - Provides all validation workflows
