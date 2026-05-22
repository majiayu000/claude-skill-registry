---
name: cui-documentation
description: General documentation standards for README, AsciiDoc, and technical documentation with validation, formatting, link verification, and content review workflows
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Skill
---

# CUI Documentation Skill

Standards and workflows for writing clear, maintainable technical documentation in CUI projects.

**Note**: This skill covers general documentation. For code documentation, use:
- `pm-dev-java:javadoc` for Java code documentation
- `cui-frontend-development/jsdoc-standards.md` for JavaScript documentation

## Available Workflows

This skill provides nine specialized workflows:

| Workflow | Purpose | Script Used |
|----------|---------|-------------|
| **format-document** | Auto-fix AsciiDoc formatting issues | `asciidoc-formatter.sh` |
| **validate-format** | Validate AsciiDoc format compliance | `asciidoc-validator.sh` |
| **verify-links** | Verify links and cross-references | `verify-adoc-links.py`, `verify-links-false-positives.py` |
| **review-content** | Review content quality and tone | `analyze-content-tone.py` |
| **comprehensive-review** | Orchestrate all review workflows | All scripts (format → links → content) |
| **create-from-template** | Create new document from template | Templates in templates/ |
| **sync-with-code** | Sync documentation with code changes | Analysis + Edit |
| **cleanup-stale** | Remove stale/duplicate documentation | Glob + Read + analysis |
| **refresh-metadata** | Update metadata and cross-references | Read + Edit |

## Workflow: format-document

Auto-fix common AsciiDoc formatting issues with safety features.

### What It Fixes

- Add blank lines before lists
- Convert deprecated `<<>>` syntax to `xref:`
- Fix header attributes
- Remove trailing whitespace

### Parameters

- `target` (required): File path or directory path
- `fix_types` (optional, default: "all"): Types of fixes: "lists", "xref", "headers", "whitespace", "all"

### Steps

**Step 1: Load Documentation Standards**

Read references/asciidoc-formatting.md

**Step 2: Discover Files**

If target is a file:
- Verify file exists and has `.adoc` extension

If target is a directory:
- Use Glob: `{directory}/*.adoc` (non-recursive)
- Filter out `target/` directories

**Step 3: Run Auto-Formatter**

Build command with options:
```bash
OPTIONS=""
if [fix_types != "all"]; then OPTIONS="$OPTIONS -t {fix_type}"; fi
```

```bash
python3 .plan/execute-script.py pm-documents:cui-documentation:docs format $OPTIONS {target}
```

**Step 4: Parse Output**

Extract statistics:
- Files processed
- Files modified
- Issues fixed
- Fix details per file

**Step 5: Report Results**

```
Format Fixes Applied to {target}
Files modified: {count}
Issues fixed: {count}
Changes applied: {list}
```

**Step 6: Validation (after changes applied)**

Run validation:

```bash
python3 .plan/execute-script.py pm-documents:cui-documentation:docs validate {target}
```

---

## Workflow: validate-format

Validate AsciiDoc files for format compliance.

### What It Checks

- Section headers with blank lines
- Proper list formatting
- Blank lines before/after lists
- Code block formatting

### Parameters

- `target` (required): File path or directory path
- `apply_fixes` (optional, default: false): Apply automatic fixes

### Steps

**Step 1: Load Documentation Standards**

Read references/asciidoc-formatting.md

**Step 2: Discover Files**

If target is a file:
- Verify file exists and has `.adoc` extension

If target is a directory:
- Use Glob: `{directory}/*.adoc` (non-recursive)

**Step 3: Run Format Validation**

```bash
python3 .plan/execute-script.py pm-documents:cui-documentation:docs validate {target}
```

**Step 4: Parse Output**

Extract warnings matching `Line [0-9]+`:
- Categorize issues by type
- Track by file and line number

**Step 5: Apply Fixes (if requested)**

If apply_fixes=true:
- For each issue, read file context (±5 lines)
- Use Edit tool to fix the issue
- Track fixes applied

**Step 6: Re-Validate (if fixes applied)**

Re-run validator and compare:
- Before: {total_issues}
- After: {remaining_issues}
- Fixed: {fixed_count}

**Step 7: Generate Report**

```
## AsciiDoc Format Validation Complete

**Status**: ✅ PASS | ⚠️ WARNINGS | ❌ FAILURES

**Summary**: Validated {file_count} file(s)

**Metrics**:
- Files validated: {count}
- Format issues found: {count}
- Issues fixed: {count}
- Issues remaining: {count}

**Issues by Category**:
- Blank line after header: {count}
- Blank line before list: {count}
- Other format violations: {count}

**Details by File**:
### {file_1}
- Line {N}: {issue description}
- Status: ✅ Clean | ⚠️ Issues remaining
```

---

## Workflow: verify-links

Verify all links and cross-references in AsciiDoc files.

### What It Verifies

- Cross-reference file links (xref:)
- Internal anchor references (<<anchor>>)
- Link formats and syntax

### Parameters

- `target` (required): File path or directory path
- `fix_links` (optional, default: false): Fix broken links

### Steps

**Step 1: Load Documentation Standards**

Read references/asciidoc-formatting.md

**Step 2: Discover Files**

If target is a file:
- Verify file exists and has `.adoc` extension

If target is a directory:
- Use Glob: `{directory}/*.adoc` (non-recursive)

**Step 3: Setup Report Directory**

```bash
mkdir -p target/asciidoc-link-verifier
```

**Step 4: Run Link Verification**

```bash
python3 .plan/execute-script.py pm-documents:cui-documentation:docs verify-links --file {file_path} --report target/asciidoc-link-verifier/links.md
```

For directories:
```bash
python3 .plan/execute-script.py pm-documents:cui-documentation:docs verify-links --directory {directory} --report target/asciidoc-link-verifier/links.md
```

**Step 5: Parse Report**

Read `target/asciidoc-link-verifier/links.md` and extract:
- Broken file links
- Broken anchors
- Format violations

**Step 6: Manual Verification (CRITICAL)**

For each "broken" link reported:
1. Extract target path
2. Resolve absolute path: `realpath {relative_target_path}`
3. Verify with Read tool
4. If file EXISTS but script reported broken: Report false positive
5. If file NOT FOUND: Confirm broken

**Step 7: Fix Internal Anchors (if approved)**

For missing anchors:
1. Search for matching section header
2. Add anchor ID: `[#anchor-id]` before header
3. Use Edit tool

**Step 8: Generate Report**

```
## AsciiDoc Link Verification Complete

**Status**: ✅ PASS | ⚠️ WARNINGS | ❌ FAILURES

**Summary**: Verified links in {file_count} file(s)

**Metrics**:
- Files verified: {count}
- Broken file links: {count}
- Broken anchors: {count}
- Issues fixed: {count}

**Details by File**:
### {file_1}
- Line {N}: xref to {target} - {status}
- Line {N}: anchor <<{id}>> - {status}
```

---

## Workflow: review-content

Review AsciiDoc content for quality: correctness, clarity, tone, style, and completeness.

### What It Reviews

- **Correctness**: Factual claims, RFC citations, verifiable statements
- **Clarity**: Concise, unambiguous, clear explanations
- **Tone & Style**: Professional, technical, no marketing language
- **Consistency**: Terminology, formatting patterns
- **Completeness**: No missing sections, TODOs, or gaps

### Parameters

- `target` (required): File path or directory path
- `apply_fixes` (optional, default: false): Apply content fixes

### Steps

**Step 1: Load Documentation Standards**

Read references/tone-and-style.md
Read references/documentation-core.md

**Step 2: Discover Files**

If target is a file:
- Verify file exists and has `.adoc` extension

If target is a directory:
- Use Glob: `{directory}/*.adoc` (non-recursive)

**Step 3: Run Content Analysis**

```bash
python3 .plan/execute-script.py pm-documents:cui-documentation:docs review --file {file_path}
```

For directories:
```bash
python3 .plan/execute-script.py pm-documents:cui-documentation:docs review --directory {directory}
```

**Step 4: Parse JSON Output**

Script returns structured JSON:
```json
{
  "status": "success",
  "data": {
    "files_analyzed": N,
    "average_quality_score": N,
    "issues": [
      {
        "file": "path",
        "line": N,
        "type": "tone|correctness|completeness",
        "severity": "critical|high|medium|low",
        "message": "description"
      }
    ]
  }
}
```

**Step 5: Apply Deep Analysis**

For each issue from script, apply Claude judgment:
- Is the marketing language truly promotional or factual?
- Can claims be verified from context?
- Are TODOs appropriate (e.g., in development docs)?

**Step 6: Categorize by Priority**

**Priority 1 - CRITICAL:**
- Unverified factual claims
- Marketing/promotional language
- Transitional markers in specification docs

**Priority 2 - HIGH:**
- Clarity problems
- Tone issues
- Consistency violations

**Priority 3 - MEDIUM:**
- Minor wording improvements

**Step 7: Apply Fixes (if requested)**

If apply_fixes=true:
- For Priority 1 and 2 issues
- Read file context
- Use Edit tool for fixes
- Ask user before major changes

**Step 8: Generate Report**

```
## AsciiDoc Content Review Complete

**Status**: ✅ PASS | ⚠️ WARNINGS | ❌ FAILURES

**Summary**: Reviewed {file_count} file(s)

**Quality Score**: {average_score}/100

**Metrics**:
- Files reviewed: {count}
- Tone issues: {count}
- Correctness issues: {count}
- Completeness issues: {count}

**Issues by Priority**:
- CRITICAL: {count}
- HIGH: {count}
- MEDIUM: {count}

**Details by File**:
### {file_1}

**Tone Issues:**
- Line {N}: {description}
  - Current: "{text}"
  - Suggested: "{improved}"

**Correctness Issues:**
- Line {N}: {description}

**Completeness Issues:**
- Line {N}: {description}
```

---

## Workflow: comprehensive-review

Orchestrate all review workflows for thorough documentation quality assurance.

### What It Does

Runs three phases in sequence with intelligent failure handling:
1. **Format Validation** (fail-fast on errors)
2. **Link Verification** (continue regardless)
3. **Content Quality Review** (continue regardless)

Provides consolidated report with aggregated results.

### Parameters

- `target` (required): File path or directory path
- `stop_on_error` (optional, default: true): Stop on format errors (Phase 1 failure)
- `apply_fixes` (optional, default: false): Attempt auto-fixes in all phases
- `skip_content` (optional, default: false): Skip Phase 3 (content review)

### Steps

**Step 1: Load Documentation Standards**

Read workflows/review-orchestration.md
Read workflows/link-verification.md
Read workflows/content-review.md

**Step 2: Discover Files**

If target is a file:
- Verify file exists and has `.adoc` extension

If target is a directory:
- Use Glob: `{directory}/*.adoc` (non-recursive)
- Filter out `target/` directories

**Step 3: Phase 1 - Format Validation**

Execute validate-format workflow:
```
Parameters:
  target: {target}
  apply_fixes: {apply_fixes}
```

Parse results:
- Extract format issues count
- Store format status (PASS/WARNINGS/FAILURES)

**Decision Point:**

If format FAILURES found AND stop_on_error=true:
- **STOP** - Skip Phase 2 and 3
- Generate partial report (format only)
- Message: "Format validation FAILED. Fix errors before link/content review."

Otherwise:
- **CONTINUE** to Phase 2

**Step 4: Phase 2 - Link Verification**

Execute verify-links workflow:
```
Parameters:
  target: {target}
  fix_links: {apply_fixes}
```

**Enhanced Link Verification:**

After running verify-adoc-links.py, classify results:

```bash
python3 .plan/execute-script.py pm-documents:cui-documentation:docs classify-links --input target/links.json --output target/classified.json
```

Parse classified results:
- likely-false-positive: Keep links (report for info)
- must-verify-manual: Use Read tool to verify each
- definitely-broken: Ask user before removal

**Manual Verification (link-verification-protocol.md):**

For each must-verify-manual link:
1. Extract target path from xref
2. Resolve absolute path: `realpath {path}`
3. Verify with Read tool
4. If EXISTS: Keep link (report false positive)
5. If NOT FOUND: Ask user before removal

Store link results:
- Broken links count
- False positives count
- Manual verification outcomes

**CONTINUE** to Phase 3 (regardless of link results)

**Step 5: Phase 3 - Content Quality Review**

Skip if skip_content=true

Execute review-content workflow with ULTRATHINK:
```
Parameters:
  target: {target}
  apply_fixes: {apply_fixes}
```

**Enhanced Content Analysis:**

```bash
python3 .plan/execute-script.py pm-documents:cui-documentation:docs analyze-tone --file {file_path} --output target/tone-analysis.json
```

Parse tone analysis JSON:
- promotional: Marketing/buzzword language
- performance_claim: Performance assertions requiring data
- standards_claim: Standards/compatibility claims requiring citations
- missing_sources: Claims without attribution

**ULTRATHINK Analysis (content-review-framework.md):**

For each flagged promotional phrase:
1. Apply decision framework:
   - Does this describe verifiable, specific capability? → Factual
   - Can this be measured or tested? → Factual
   - Does it compare favorably without evidence? → Promotional
2. Generate finding with reasoning
3. Suggest factual alternative

Store content results:
- Promotional language count
- Unverified claims count
- Missing sources count
- ULTRATHINK findings

**Step 6: Aggregate Results**

Combine all phase results:
```
Total files: {count}
Phase 1 (Format): {PASS|WARNINGS|FAILURES} - {issue_count} issues
Phase 2 (Links): {PASS|WARNINGS|FAILURES} - {issue_count} issues
Phase 3 (Content): {PASS|WARNINGS|FAILURES} - {issue_count} issues
```

Overall status:
- ✅ PASS: All phases passed
- ⚠️ WARNINGS: Some non-critical issues
- ❌ FAILURES: Critical issues found

**Step 7: Generate Consolidated Report**

```
# Comprehensive AsciiDoc Review Report

**Target:** {file_path | directory_path}
**Date:** {ISO timestamp}
**Status:** ✅ PASS | ⚠️ WARNINGS | ❌ FAILURES

## Executive Summary

- Files reviewed: {count}
- Total issues: {count}
- Critical issues: {count}

### Issues by Phase

| Phase | Status | Issues |
|-------|--------|--------|
| Format Validation | {✅/⚠️/❌} | {count} |
| Link Verification | {✅/⚠️/❌} | {count} |
| Content Review | {✅/⚠️/❌} | {count} |

## Phase 1: Format Validation

{Results from validate-format workflow}

## Phase 2: Link Verification

### Broken Links
- {file}:{line} - xref:{target} - {reason}

### False Positives
- {file}:{line} - {link} - Verified manually as valid

### Manual Verification Performed
- {count} links verified with Read tool
- {count} confirmed broken
- {count} false positives

## Phase 3: Content Review

### Promotional Language (ULTRATHINK Analysis)
- Line {N}: "{text}"
  - Issue: {marketing/self-praise/subjective}
  - Reasoning: {ULTRATHINK analysis}
  - Suggestion: "{factual alternative}"

### Missing Sources
- Line {N}: Claim requires citation: "{text}"
  - Type: {performance/compatibility/usage}

### Unverified Claims
- Line {N}: {description}

## Recommendations

### Immediate Actions (Critical)
1. {action required}

### Improvements (Warnings)
1. {suggested improvement}

## Tool Usage Statistics
- validate-format: {time}ms
- verify-links: {time}ms
- review-content: {time}ms
- Total: {time}ms
```

---

## Workflow: create-from-template

Create new AsciiDoc documents from predefined templates.

### What It Creates

- Standard specification documents
- README files
- How-to guides

### Parameters

- `type` (required): standard|readme|guide
- `name` (required): Document name (used in title and filename)
- `path` (optional): Output path (default: inferred from type)

### Steps

**Step 1: Validate Parameters**

```
If type not in [standard, readme, guide]:
  Error: "Invalid type. Use: standard, readme, guide"

If name is empty:
  Error: "Name is required"
```

**Step 2: Determine Output Path**

```
If path not specified:
  standard → standards/{name}.adoc
  readme   → {name}/README.adoc or README.adoc
  guide    → docs/{name}.adoc
```

**Step 3: Load Template**

Read template from templates/:
- standard → templates/standard-template.adoc
- readme   → templates/readme-template.adoc
- guide    → templates/guide-template.adoc

**Step 4: Substitute Placeholders**

Replace template placeholders:
- `{{TITLE}}` → Formatted name
- `{{PROJECT_NAME}}` → Name
- `{{GUIDE_TITLE}}` → Formatted guide title
- `{{DESCRIPTION}}` → Empty (user fills in)
- `{{SHORT_DESCRIPTION}}` → Empty (user fills in)
- `{{PURPOSE}}` → Empty (user fills in)

**Step 5: Write File**

Use Write tool to create file at output path.

**Step 6: Validate Created File**

Execute validate-format workflow on new file.

**Step 7: Report Result**

```
Document Created: {output_path}
Type: {type}
Status: ✅ Valid format

Next steps:
1. Edit {output_path} to fill in content
2. Run /doc-doctor target={output_path} to validate
```

---

## Workflow: sync-with-code

Analyze code changes and update documentation to stay in sync.

### What It Does

- Detects code structure changes
- Identifies documentation drift
- Suggests or applies updates

### Parameters

- `target` (required): Documentation file or directory
- `code_path` (optional): Code directory to analyze (default: src/)

### Steps

**Step 1: Analyze Code Structure**

```
Use Glob to find code files:
  {code_path}/**/*.java
  {code_path}/**/*.js
  {code_path}/**/*.ts

Extract:
- Public classes/interfaces
- Public methods
- Configuration patterns
```

**Step 2: Analyze Documentation**

```
Read target documentation files
Extract:
- Documented classes/methods
- Code examples
- Configuration references
```

**Step 3: Identify Drift**

Compare code vs documentation:
- Missing documentation for new code
- Outdated documentation for changed code
- Documentation for removed code

**Step 4: Generate Sync Report**

```
Documentation Sync Analysis
═══════════════════════════════════════

Code analyzed: {file_count} files
Documentation analyzed: {doc_count} files

Drift Detected:
- New code needing docs: {count}
- Outdated documentation: {count}
- Stale documentation: {count}

Details:
{list of specific drift items}

Recommendations:
{specific actions to sync}
```

**Step 5: Apply Updates (if requested)**

For each drift item:
- Ask user for confirmation
- Use Edit tool to update documentation
- Re-validate after changes

---

## Workflow: cleanup-stale

Identify and remove stale or duplicate documentation.

### What It Does

- Finds duplicate content across files
- Identifies orphaned documentation
- Suggests cleanup actions

### Parameters

- `target` (required): Directory to analyze

### Steps

**Step 1: Discover Documentation**

```
Use Glob: {target}/**/*.adoc
Exclude: target/, node_modules/
```

**Step 2: Analyze Content**

For each file:
- Extract title and sections
- Calculate content hash
- Track cross-references

**Step 3: Identify Candidates**

**Duplicates:**
- Files with >80% similar content
- Identical sections across files

**Orphaned:**
- Files not referenced from anywhere
- Files with broken incoming links

**Stale:**
- Files with TODO markers older than threshold
- Files not updated in extended period

**Step 4: Generate Cleanup Report**

```
Documentation Cleanup Analysis
═══════════════════════════════════════

Files analyzed: {count}

Candidates for Cleanup:
- Potential duplicates: {count}
- Orphaned files: {count}
- Stale content: {count}

Duplicates:
{file1} ↔ {file2}: {similarity}%

Orphaned:
{file}: No incoming references

Stale:
{file}: Contains {N} TODOs

Recommendations:
1. {specific action}
```

**Step 5: Execute Cleanup (with confirmation)**

For each approved removal:
1. Update files that reference removed content
2. Remove or consolidate file
3. Re-validate cross-references

---

## Workflow: refresh-metadata

Update metadata, fix cross-references, and refresh table of contents.

### What It Does

- Updates document metadata
- Fixes broken cross-references
- Regenerates table of contents

### Parameters

- `target` (required): File or directory

### Steps

**Step 1: Discover Files**

```
If target is file:
  files = [target]
If target is directory:
  Use Glob: {target}/**/*.adoc
```

**Step 2: Analyze Metadata**

For each file:
- Check header attributes (:toc:, :sectnums:, etc.)
- Identify missing or outdated metadata

**Step 3: Analyze Cross-References**

```
Execute verify-links workflow
Collect: broken internal references
```

**Step 4: Fix Cross-References**

For each broken reference:
1. Search for target content by title/anchor
2. If found at new location: Update reference
3. If not found: Report for manual review

**Step 5: Update Metadata**

Using Edit tool:
- Ensure standard header attributes present
- Fix attribute formatting

**Step 6: Generate Report**

```
Metadata Refresh Complete
═══════════════════════════════════════

Files processed: {count}

Updates Applied:
- Metadata fixed: {count}
- Cross-references fixed: {count}
- Headers updated: {count}

Manual Review Needed:
- {file}: {reason}
```

---

## Reference Documents

All reference material is in the `references/` directory (lookup material - WHAT rules to apply):

| Reference | Purpose | When to Load |
|-----------|---------|--------------|
| `documentation-core.md` | Core documentation principles | Always |
| `asciidoc-formatting.md` | AsciiDoc format rules | Format/validation workflows |
| `tone-and-style.md` | Tone and style requirements | Content review workflow |
| `readme-structure.md` | README structure patterns | README files |
| `organization-standards.md` | Document organization | Structure reviews |

## Workflow Documents

All workflow procedures are in the `workflows/` directory (operational procedures - HOW to execute):

| Workflow | Purpose | When to Load |
|----------|---------|--------------|
| `link-verification.md` | Link verification protocol with manual Read verification | Link workflows |
| `content-review.md` | ULTRATHINK-based tone analysis framework | Content review workflow |
| `review-orchestration.md` | Comprehensive review orchestration | comprehensive-review workflow |

## Scripts

Script: `pm-documents:cui-documentation` → `docs.py`

| Subcommand | Description |
|------------|-------------|
| `stats` | Generate documentation statistics |
| `validate` | Validate AsciiDoc files for compliance |
| `format` | Auto-fix AsciiDoc formatting issues |
| `verify-links` | Verify links and cross-references |
| `classify-links` | Classify broken links to reduce false positives |
| `review` | Analyze content for quality issues |
| `analyze-tone` | Detect promotional language and missing sources |

**Usage Examples:**
```bash
# Generate statistics
python3 .plan/execute-script.py pm-documents:cui-documentation:docs stats -f json /path/to/docs

# Validate formatting
python3 .plan/execute-script.py pm-documents:cui-documentation:docs validate /path/to/file.adoc

# Format files
python3 .plan/execute-script.py pm-documents:cui-documentation:docs format -t all /path/to/docs

# Verify links
python3 .plan/execute-script.py pm-documents:cui-documentation:docs verify-links --directory /path/to/docs

# Analyze tone
python3 .plan/execute-script.py pm-documents:cui-documentation:docs analyze-tone --file /path/to/file.adoc --output report.json
```

## Usage from Commands

Commands invoke this skill and its workflows:

```markdown
# In command file
Skill: pm-documents:cui-documentation

# Then specify workflow
Execute workflow: format-document
Parameters:
  target: "standards/"
```

## Quality Verification Checklist

All documentation must pass:

- [ ] Professional, neutral tone (no marketing language)
- [ ] Proper AsciiDoc formatting
- [ ] Complete code examples
- [ ] Verified references
- [ ] Consistent terminology
- [ ] Documents only existing features
- [ ] All links valid
