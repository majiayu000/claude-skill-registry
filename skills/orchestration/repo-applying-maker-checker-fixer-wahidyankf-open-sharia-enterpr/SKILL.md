---
name: repo-applying-maker-checker-fixer
description: Three-stage content quality workflow pattern (Maker creates, Checker validates, Fixer remediates) with detailed execution workflows. Use when working with content quality workflows, validation processes, audit reports, or implementing maker/checker/fixer agent roles.
---

# Maker-Checker-Fixer Pattern (Comprehensive)

This Skill provides complete guidance on the three-stage content quality workflow pattern used across repository agent families for systematic content creation, validation, and remediation.

## Purpose

Use this Skill when:

- Implementing content quality workflows
- Working with maker/checker/fixer agents
- Validating content against conventions
- Applying validated fixes from audit reports
- Understanding agent family structures
- Deciding when to use maker vs fixer for content changes
- Creating new checker or fixer agents
- Executing validation or fix workflows

## The Three Stages

### Stage 1: Maker (Content Creation & Updates)

**Role**: Creates NEW content and updates EXISTING content with all dependencies

**Characteristics**:

- User-driven operation (responds to "create" or "update" requests)
- Comprehensive scope (creates target content AND updates related files)
- Cascading changes (adjusts indices, cross-references, dependencies)
- Proactive management (anticipates what needs updating)

**Tool Pattern**: `Write`, `Edit` (content modification)

**Color**: Blue (writer agents) or Yellow (special case: repo-governance-maker uses bash)

**When to Use Maker**:

- User explicitly requests content creation or updates
- Creating NEW content from scratch
- Making significant changes to EXISTING content
- Need comprehensive dependency management
- User-driven workflow (user says "create" or "update")

**Example Workflow**:

```markdown
User: "Create new TypeScript generics tutorial"

Maker:

1. Creates main content file
2. Creates bilingual version (if applicable)
3. Updates navigation files
4. Ensures overview/index links correct
5. Follows weight ordering convention
6. Uses accessible colors in diagrams
7. Validates all internal links
8. Delivers complete, ready-to-publish content
```

### Stage 2: Checker (Validation) - Detailed Workflow

**Role**: Validates content against conventions and generates audit reports

**Characteristics**:

- Validation-driven (analyzes existing content)
- Non-destructive (does NOT modify files being checked)
- Comprehensive reporting (generates detailed audit in `generated-reports/`)
- Evidence-based (re-validation in fixer prevents false positives)

**Tool Pattern**: `Read`, `Glob`, `Grep`, `Write`, `Bash` (read-only + report generation)

- `Write` needed for audit report files
- `Bash` needed for UTC+7 timestamps

**Color**: Green (checker agents)

**When to Use Checker**:

- ✅ REQUIRED: New content created from scratch
- ✅ REQUIRED: Major refactoring or updates
- ✅ REQUIRED: Before publishing to production
- ✅ REQUIRED: Complex content (tutorials, Hugo)
- ✅ REQUIRED: Critical files (AGENTS.md, conventions)
- ⚠️ OPTIONAL: Small updates to high-quality content

**Criticality Categorization**:

Checkers categorize findings by importance/urgency:

- 🔴 **CRITICAL** - Breaks functionality, blocks users (must fix before publication)
- 🟠 **HIGH** - Significant quality degradation, convention violations (should fix)
- 🟡 **MEDIUM** - Minor quality issues, style inconsistencies (fix when convenient)
- 🟢 **LOW** - Suggestions, optional improvements (consider for future)

**Report Format**: Findings grouped by criticality with emoji indicators

#### Checker Workflow: 5-Step Process

Checker agents follow a consistent 5-step workflow:

```
Step 0: Initialize Report
    ↓
Step 1-N: Validate Content (domain-specific)
    ↓
Final Step: Finalize Report
```

**Step 0: Initialize Report File**

**CRITICAL FIRST STEP - Execute before any validation begins:**

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

**Steps 1-N: Validate Content (Domain-Specific)**

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

**Common Validation Steps by Checker Type**:

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

**Final Step: Finalize Report**

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

**Progressive Writing Methodology**

**CRITICAL REQUIREMENT**: All checker agents MUST write findings progressively.

**Why?** Context compaction during long validation runs can lose buffered findings. Progressive writing ensures audit history survives.

**Implementation Pattern**:

```markdown
Step 0: Initialize Report File
→ Create file immediately with header

Steps 1-N: Validate Content
→ For each validation check:

1. Perform validation
2. Immediately append finding to report file
3. Continue to next check
   → DO NOT buffer findings in memory

Final Step: Finalize Report
→ Update status and add summary
→ File already contains all findings
```

**Example Workflow**:

```markdown
User: "Check the new TypeScript tutorial"

Checker:

1. Reads tutorial file
2. Validates frontmatter (date format, required fields, weight)
3. Checks content structure (heading hierarchy, links)
4. Validates Hugo conventions (absolute paths, no .md)
5. Checks content quality (alt text, accessible colors)
6. Generates audit report: generated-reports/ayokoding-web**2025-12-14--20-45**audit.md
7. Reports findings summary in conversation
8. Does NOT modify the tutorial file
```

### Stage 3: Fixer (Remediation) - Detailed Workflow

**Role**: Applies validated fixes from checker audit reports

**Characteristics**:

- Validation-driven (works from audit reports, not user requests)
- Re-validation before fixing (confirms issues still exist)
- Confidence-based (only applies HIGH confidence fixes automatically)
- Safe application (skips MEDIUM and FALSE_POSITIVE)
- Audit trail (generates fix reports for transparency)

**Tool Pattern**: `Read`, `Edit`, `Glob`, `Grep`, `Write`, `Bash`

- `Edit` for applying fixes (NOT `Write`)
- `Write` for fix report generation
- `Bash` for timestamps

**Color**: Purple (fixer agents)

**When to Use Fixer**:

- ✅ Checker has generated an audit report
- ✅ Issues are convention violations (not content gaps)
- ✅ Fixes are mechanical (field values, formatting)
- ✅ Validation-driven workflow

**When to SKIP Fixer (Manual Preferred)**:

- ❌ Issues require human judgment (narrative quality)
- ❌ Fixes are context-dependent
- ❌ Checker reports unclear/ambiguous
- ❌ User prefers manual control

**Priority-Based Execution**:

Fixers combine criticality (importance) × confidence (certainty) → priority:

| Priority         | Combination                      | Action                               |
| ---------------- | -------------------------------- | ------------------------------------ |
| **P0** (Blocker) | CRITICAL + HIGH                  | Auto-fix immediately, block if fails |
| **P1** (Urgent)  | HIGH + HIGH OR CRITICAL + MEDIUM | Auto-fix or urgent review            |
| **P2** (Normal)  | MEDIUM + HIGH OR HIGH + MEDIUM   | Auto-fix (if approved) or review     |
| **P3-P4** (Low)  | LOW combinations                 | Suggestions only                     |

**Execution Order**: P0 → P1 → P2 → P3-P4

#### Fixer Workflow: 6-Step Process

**1. Report Discovery**

**Auto-detect with manual override (default pattern)**:

```bash
# Auto-detect latest audit report for agent family
ls -t generated-reports/{agent-family}-*-audit.md | head -1
```

**Implementation Steps**:

1. **Auto-detect latest**: Find most recent audit report in `generated-reports/`
2. **Allow manual override**: Accept explicit report path from user
3. **Verify report exists**: Check file exists before proceeding
4. **Parse report format**: Extract UUID chain and timestamp for fix report

**Report Naming**: Uses 4-part format per Temporary Files Convention:

- Pattern: `{agent-family}__{uuid-chain}__{timestamp}__audit.md`
- Example: `docs__a1b2c3__2025-12-14--20-45__audit.md`

**2. Validation Strategy**

**CRITICAL PRINCIPLE**: NEVER trust checker findings blindly. ALWAYS re-validate before applying fixes.

**For EACH finding in audit report**:

```
Read finding → Re-execute validation check → Assess confidence level

HIGH_CONFIDENCE:
  - Re-validation confirms issue exists
  - Issue is objective and verifiable
  - Apply fix automatically

MEDIUM_CONFIDENCE:
  - Re-validation unclear or ambiguous
  - Issue is subjective or context-dependent
  - Skip fix, flag as "needs manual review"

FALSE_POSITIVE:
  - Re-validation disproves issue
  - Skip fix, report to user
  - Suggest checker improvement
```

**Confidence Assessment Criteria**:

**HIGH Confidence** (Apply automatically):

- Objective, verifiable errors
- Clear violation of documented standards
- Pattern-based errors with known fixes
- File-based errors (paths, syntax, format)

**MEDIUM Confidence** (Manual review):

- Subjective quality judgments
- Context-dependent issues
- Ambiguous requirements
- Risky refactoring changes

**FALSE_POSITIVE** (Skip and report):

- Re-validation disproves the issue
- Checker misunderstood context
- Checker used wrong verification source
- Finding no longer applicable

**3. Mode Parameter Handling**

Support `mode` parameter for quality-gate workflows:

**Mode Levels**:

- **lax**: Process CRITICAL findings only (skip HIGH/MEDIUM/LOW)
- **normal**: Process CRITICAL + HIGH findings only (skip MEDIUM/LOW)
- **strict**: Process CRITICAL + HIGH + MEDIUM findings (skip LOW)
- **ocd**: Process all findings (CRITICAL + HIGH + MEDIUM + LOW)

**Implementation**:

```markdown
1. Parse audit report and categorize findings by criticality
2. Apply mode filter before re-validation:
   - lax: Only process CRITICAL findings
   - normal: Process CRITICAL + HIGH findings
   - strict: Process CRITICAL + HIGH + MEDIUM findings
   - ocd: Process all findings
3. Track skipped findings for reporting
4. Document skipped findings in fix report
```

**Reporting Skipped Findings**:

```markdown
## Skipped Findings (Below Mode Threshold)

**Mode Level**: normal (fixing CRITICAL/HIGH only)

**MEDIUM findings** (X skipped - reported but not fixed):

1. [File path] - [Issue description]

**LOW findings** (X skipped - reported but not fixed):

1. [File path] - [Issue description]

**Note**: Run with `mode=strict` or `mode=ocd` to fix these findings.
```

**4. Fix Application**

**Automatic Application** (HIGH confidence only):

- Apply ALL HIGH_CONFIDENCE fixes automatically
- NO confirmation prompts (user already reviewed checker report)
- Skip MEDIUM_CONFIDENCE findings (flag for manual review)
- Skip FALSE_POSITIVE findings (report to improve checker)
- Use appropriate tools based on file location:
  - `.claude/` folders: Use Bash tools (sed, awk, heredoc)
  - `docs/` folders: Use Edit tool
  - Other locations: Use appropriate tools per file type

**Fix Execution Pattern**:

```markdown
For each HIGH_CONFIDENCE finding:

1. Read current file state
2. Apply fix using appropriate tool
3. Verify fix applied correctly
4. Log fix in fix report (progressive writing)
5. Continue to next finding
```

**5. Fix Report Generation**

Generate fix report in `generated-reports/` using same UUID chain as audit:

**File Naming Pattern**:

- Input audit: `{agent-family}__{uuid-chain}__{timestamp}__audit.md`
- Output fix: `{agent-family}__{uuid-chain}__{timestamp}__fix.md`
- Preserve UUID chain and timestamp from source audit

**Report Structure**:

```markdown
# Fix Report: {Agent Name}

**Status**: In Progress / Complete
**Source Audit**: {path to audit report}
**Timestamp**: {YYYY-MM-DD--HH-MM UTC+7}
**UUID Chain**: {uuid-chain}
**Mode**: {lax/normal/strict/ocd}

---

## Fixes Applied

### Fix 1: {Title}

**Status**: ✅ APPLIED / ⏭️ SKIPPED
**Criticality**: {CRITICAL/HIGH/MEDIUM/LOW}
**Confidence**: {HIGH/MEDIUM/FALSE_POSITIVE}
**File**: {path}

**Issue**: {description}

**Changes Applied**: {before → after}

**Tool Used**: {Edit/Bash sed/etc}

---

## Skipped Findings

### {Reason for skipping}

**Count**: X findings

1. {File} - {Issue} - {Reason}

---

## Summary

**Fixes Applied**: X
**Fixes Skipped**: Y (Z MEDIUM_CONFIDENCE, W FALSE_POSITIVE)
**Skipped by Mode**: M (below mode threshold)

**Status**: Complete
**Completed**: {timestamp}
```

**Progressive Writing**: Write findings as they're processed, not buffered to end.

**6. Trust Model: Checker Verifies, Fixer Applies**

**Key Principle**: Fixer trusts checker's verification work (separation of concerns).

**Why Fixers Don't Have Web Tools**:

1. **Separation of Concerns**: Checker does expensive web verification once
2. **Performance**: Avoid duplicate web requests
3. **Clear Responsibility**: Checker = research/verification, Fixer = application
4. **Audit Trail**: Checker documents all sources in audit report
5. **Trust Model**: Fixer trusts checker's documented verification

**How Fixer Re-validates Without Web Access**:

- Read audit report and extract checker's documented sources
- Analyze checker's cited URLs, registry data, API docs
- Apply pattern matching for known error types
- Perform file-based checks (syntax, format, consistency)
- Conservative approach: When in doubt → MEDIUM confidence

**When Fixer Doubts a Finding**:

- Classify as MEDIUM or FALSE_POSITIVE (don't apply)
- Document reasoning in fix report
- Provide actionable feedback for checker improvement
- Flag for manual review

**Example Workflow**:

```markdown
User: "Apply fixes from latest ayokoding-web audit"

Fixer:

1. Auto-detects latest: generated-reports/ayokoding-web**2025-12-14--20-45**audit.md
2. Parses findings (25 issues)
3. Re-validates each finding:
   - 18 findings → HIGH confidence (apply)
   - 4 findings → MEDIUM confidence (skip, manual review)
   - 3 findings → FALSE_POSITIVE (skip, report for checker improvement)
4. Applies 18 fixes
5. Generates fix report: generated-reports/ayokoding-web**2025-12-14--20-45**fix.md
6. Summary: 18 fixed, 4 manual review, 3 false positives
```

## Common Workflows

### Basic: Create → Validate → Fix

```
1. User: "Create new tutorial"
2. Maker: Creates content + dependencies
3. User: Reviews, looks good
4. Checker: Validates, finds minor issues
5. User: Reviews audit, approves fixes
6. Fixer: Applies validated fixes
7. Done: Production-ready
```

### Iterative: Maker → Checker → Fixer → Checker

```
1. User: "Update existing content"
2. Maker: Updates content + dependencies
3. Checker: Validates, finds issues
4. User: Reviews audit, approves fixes
5. Fixer: Applies fixes
6. Checker: Re-validates to confirm
7. Done: Content verified clean
```

**When to use**: Critical content, major refactoring, uncertain fixer confidence

## Agent Families Using This Pattern

Seven agent families implement this pattern:

1. **repo-governance-\*** - Repository-wide consistency
2. **apps-ayokoding-web-\*** - Hugo content (ayokoding-web)
3. **docs-tutorial-\*** - Tutorial quality
4. **apps-ose-platform-web-content-\*** - Hugo content (ose-platform-web)
5. **readme-\*** - README quality
6. **docs-\*** - Documentation factual accuracy
7. **plan-\*** - Plan completeness and structure

Each family has:

- **Maker** (Blue) - Creates/updates content
- **Checker** (Green) - Validates, generates audits
- **Fixer** (Purple/Yellow) - Applies validated fixes

## Best Practices

### For All Roles

1. **Always run checker before publication** - Catches issues early
2. **Review audit reports before fixing** - Understand what will change
3. **Use maker for user-driven creation** - Not fixer
4. **Use fixer for validation-driven fixes** - Not maker
5. **Re-run checker after major fixes** - Verify fixes worked
6. **Report false positives** - Improves checker accuracy over time

### For Checkers

**DO**:

- Initialize report file before validation begins (Step 0)
- Write findings progressively during execution
- Use decision tree for consistent criticality assessment
- Document specific impact for each finding
- Provide clear, actionable recommendations
- Include examples showing broken vs fixed state

**DON'T**:

- Buffer findings in memory (context compaction risk)
- Mix criticality levels in same report section
- Skip impact description
- Provide vague recommendations
- Forget to document verification source (for dual-label agents)

### For Fixers

**DO**:

- ALWAYS re-validate before applying fixes
- Process findings in strict priority order (P0 → P1 → P2 → P3)
- Document confidence assessment reasoning
- Report false positives with improvement suggestions
- Group fixes by priority in report
- Trust checker's documented verification work
- Respect mode parameter thresholds

**DON'T**:

- Trust checker findings without re-validation
- Apply fixes in discovery order (ignore priority)
- Skip MEDIUM confidence manual review flagging
- Apply P2 fixes without user approval
- Try to independently verify web-based findings (trust checker)

## Common Mistakes

### All Roles

- ❌ **Using fixer for content creation** - Use maker instead (fixer is for fixing issues, not creating)
- ❌ **Skipping checker validation** - Always validate before publication
- ❌ **Manual fixes for mechanical issues** - Use fixer for efficiency
- ❌ **Auto-applying MEDIUM confidence fixes** - Needs manual review
- ❌ **Not re-validating before fixing** - Prevents false positive fixes

### Checker-Specific

- ❌ **Buffering findings**: Don't collect all findings in memory and write at end (context compaction risk)
- ❌ **Wrong timestamp format**: Don't use `YYYY-MM-DD HH:MM` (spaces in filenames)
- ❌ **Missing UUID chain**: Don't use timestamp alone for uniqueness
- ❌ **Generic scope**: Don't use same scope for all agents
- ❌ **Conflating verification with criticality**: [Error] is WHAT (factual state), criticality is HOW URGENT

### Fixer-Specific

- ❌ **Skipping re-validation**: Don't trust checker, apply fix directly
- ❌ **Ignoring priority order**: Don't fix findings in discovery order
- ❌ **File-level confidence instead of per-finding**: Each finding assessed independently
- ❌ **Trying to independently verify web findings**: Trust checker's documented verification

## Tool Requirements

### Checkers

Checkers typically need:

- **Read**: Read files to validate
- **Glob**: Find files by pattern
- **Grep**: Extract content patterns (code blocks, commands, etc.)
- **Write**: Initialize and update report file
- **Bash**: Generate UUID, timestamp, file operations
- **WebFetch**: (Optional) Access official documentation
- **WebSearch**: (Optional) Find authoritative sources

**Bash Tool Critical**: Required for UUID generation and report initialization.

### Fixers

Fixers typically need:

- **Read**: Read audit reports and files to fix
- **Edit**: Apply fixes to docs/ files
- **Bash**: Apply fixes to .claude/ files (sed, awk, heredoc)
- **Write**: Generate fix reports
- **Glob/Grep**: Optional - for pattern matching and validation

**NO Web Tools**: Fixers intentionally lack WebFetch/WebSearch (trust checker's verification).

## Integration with Conventions

The pattern integrates with:

- **[Criticality Levels Convention](../../../governance/development/quality/criticality-levels.md)** - Checkers categorize by criticality, fixers use for priority
- **[Fixer Confidence Levels Convention](../../../governance/development/quality/fixer-confidence-levels.md)** - Fixers assess confidence, combine with criticality
- **[Temporary Files Convention](../../../governance/development/infra/temporary-files.md)** - Checker/fixer reports stored in `generated-reports/`
- **[Repository Validation Methodology](../../../governance/development/quality/repository-validation.md)** - Standard validation patterns
- **[AI Agents Convention](../../../governance/development/agents/ai-agents.md)** - Agent structure, tool permissions, color coding

## References

- **[Maker-Checker-Fixer Pattern Convention](../../../governance/development/pattern/maker-checker-fixer.md)** - Complete pattern documentation
- **[Criticality Levels Convention](../../../governance/development/quality/criticality-levels.md)** - Severity classification
- **[Fixer Confidence Levels Convention](../../../governance/development/quality/fixer-confidence-levels.md)** - Confidence assessment
- **[Temporary Files Convention](../../../governance/development/infra/temporary-files.md)** - Report file organization and naming
- **[Repository Validation Methodology](../../../governance/development/quality/repository-validation.md)** - Validation patterns

## Related Skills

- `repo-assessing-criticality-confidence` - Deep dive into criticality/confidence levels and priority matrix
- `repo-generating-validation-reports` - UUID chain generation, report format, progressive writing
- `repo-understanding-repository-architecture` - Understanding the six-layer governance and where patterns fit

---

**Note**: This Skill provides comprehensive action-oriented guidance combining pattern overview with detailed execution workflows. The authoritative convention document contains complete implementation details, examples, and all seven agent families.
