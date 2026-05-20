---
name: quality-scan
description: Updates dependencies, cleans up junk files, and performs comprehensive quality scans across codebase to identify critical bugs, logic errors, and workflow problems. Spawns specialized agents for targeted analysis and generates prioritized improvement tasks. Use when improving code quality, before releases, or investigating issues.
---

# quality-scan

<task>
Your task is to perform comprehensive quality scans across the socket-sdk-js codebase using specialized agents to identify critical bugs, logic errors, and workflow problems. Before scanning, update dependencies and clean up junk files to ensure a clean and organized repository. Generate a prioritized report with actionable improvement tasks.
</task>

<context>
**What is Quality Scanning?**
Quality scanning uses specialized AI agents to systematically analyze code for different categories of issues. Each agent type focuses on specific problem domains and reports findings with severity levels and actionable fixes.

**socket-sdk-js Architecture:**
This is Socket Security's TypeScript/JavaScript SDK that:
- Provides programmatic access to Socket.dev security analysis
- Implements HTTP client with retry logic and rate limiting
- Handles API authentication and request/response validation
- Generates strict TypeScript types from OpenAPI specifications
- Supports package scanning, SBOM generation, and organization management
- Implements comprehensive test coverage with Vitest

**Scan Types Available:**
1. **critical** - Crashes, security vulnerabilities, resource leaks, data corruption
2. **logic** - Algorithm errors, edge cases, type guards, off-by-one errors
3. **workflow** - Build scripts, CI issues, cross-platform compatibility
4. **security** - GitHub Actions workflow security (zizmor scanner)
5. **documentation** - README accuracy, outdated docs, missing documentation

**Why Quality Scanning Matters:**
- Catches bugs before they reach production
- Identifies security vulnerabilities early
- Improves code quality systematically
- Provides actionable fixes with file:line references
- Prioritizes issues by severity for efficient remediation
- Keeps dependencies up-to-date
- Cleans up junk files for a well-organized repository

**Agent Prompts:**
All agent prompts are embedded in `reference.md` with structured <context>, <instructions>, <pattern>, and <output_format> tags following Claude best practices.
</context>

<constraints>
**CRITICAL Requirements:**
- Read-only analysis (no code changes during scan)
- Must complete all enabled scans before reporting
- Findings must be prioritized by severity (Critical → High → Medium → Low)
- Must generate actionable tasks with file:line references
- All findings must include suggested fixes

**Do NOT:**
- Fix issues during scan (analysis only - report findings)
- Skip critical scan types without user permission
- Report findings without file/line references
- Proceed if codebase has uncommitted changes (warn but continue)

**Do ONLY:**
- Update dependencies before scanning
- Run enabled scan types in priority order (critical → logic → workflow)
- Generate structured findings with severity levels
- Provide actionable improvement tasks with specific code changes
- Report statistics and coverage metrics
- Deduplicate findings across scans
</constraints>

<instructions>

## Process

Execute the following phases sequentially to perform comprehensive quality analysis.

### Phase 1: Validate Environment

<prerequisites>
Verify the environment before starting scans:
</prerequisites>

```bash
git status
```

<validation>
**Expected State:**
- Working directory should be clean (warn if dirty but continue)
- On a valid branch
- Node modules installed

**If working directory dirty:**
- Warn user: "Working directory has uncommitted changes - continuing with scan"
- Continue with scans (quality scanning is read-only)

</validation>

---

### Phase 2: Update Dependencies

<action>
Update dependencies across Socket Security SDK repositories to ensure latest versions:
</action>

**Target Repositories:**
1. **socket-sdk-js** (current repository)
2. **socket-cli** (`../socket-cli/`)
3. **socket-btm** (`../socket-btm/`)
4. **socket-registry** (`../socket-registry/`)

**Update Process:**

For each repository, run dependency updates:

```bash
# socket-sdk-js (current repo)
pnpm run update

# socket-cli
cd ../socket-cli && pnpm run update && cd -

# socket-btm
cd ../socket-btm && pnpm run update && cd -

# socket-registry
cd ../socket-registry && pnpm run update && cd -
```

<validation>
**For each repository:**
1. Check if directory exists (skip if not found)
2. Run `pnpm run update` command
3. Report success or failure
4. Track updated packages count
5. Continue even if some repos fail

**Expected Results:**
- Dependencies updated in available repositories
- Report number of packages updated per repository
- Note any repositories that were skipped (not found)
- Continue with scan even if updates fail

**Track for reporting:**
- Repositories updated: N/4
- Total packages updated: N
- Failed updates: N (continue with warnings)
- Skipped repositories: [list]

</validation>

---

### Phase 3: Repository Cleanup

<action>
Clean up junk files and organize the repository before scanning:
</action>

**Cleanup Tasks:**

1. **Remove SCREAMING_TEXT.md files** (all-caps .md files) that are NOT:
   - Inside `.claude/` directory
   - Inside `docs/` directory
   - Named `README.md`, `LICENSE`, or `SECURITY.md`

2. **Remove temporary test files** in wrong locations:
   - `.test.mjs` or `.test.mts` files outside `test/` or `__tests__/` directories
   - Temp files: `*.tmp`, `*.temp`, `.DS_Store`, `Thumbs.db`
   - Editor backups: `*~`, `*.swp`, `*.swo`, `*.bak`
   - Test artifacts: `*.log` files in root or package directories (not logs/)

```bash
# Find SCREAMING_TEXT.md files (all caps with .md extension)
find . -type f -name '*.md' \
  ! -path './.claude/*' \
  ! -path './docs/*' \
  ! -name 'README.md' \
  ! -name 'LICENSE' \
  ! -name 'SECURITY.md' \
  | grep -E '/[A-Z_]+\.md$'

# Find test files in wrong locations
find . -type f \( -name '*.test.mjs' -o -name '*.test.mts' \) \
  ! -path '*/test/*' \
  ! -path '*/__tests__/*' \
  ! -path '*/node_modules/*'

# Find temp files
find . -type f \( \
  -name '*.tmp' -o \
  -name '*.temp' -o \
  -name '.DS_Store' -o \
  -name 'Thumbs.db' -o \
  -name '*~' -o \
  -name '*.swp' -o \
  -name '*.swo' -o \
  -name '*.bak' \
\) ! -path '*/node_modules/*'

# Find log files in wrong places (not in logs/ or build/ directories)
find . -type f -name '*.log' \
  ! -path '*/logs/*' \
  ! -path '*/build/*' \
  ! -path '*/node_modules/*' \
  ! -path '*/.git/*'
```

<validation>
**For each file found:**
1. Show the file path to user
2. Explain why it's considered junk
3. Ask user for confirmation before deleting (use AskUserQuestion)
4. Delete confirmed files: `git rm` if tracked, `rm` if untracked
5. Report files removed

**If no junk files found:**
- Report: "✓ Repository is clean - no junk files found"

**Important:**
- Always get user confirmation before deleting
- Show file contents if user is unsure
- Track deleted files for reporting

</validation>

---

### Phase 4: Determine Scan Scope

<action>
Ask user which scans to run:
</action>

**Default Scan Types** (run all unless user specifies):
1. **critical** - Critical bugs (crashes, security, resource leaks)
2. **logic** - Logic errors (algorithms, edge cases, type guards)
3. **workflow** - Workflow problems (scripts, CI, git hooks)
4. **security** - GitHub Actions security (template injection, cache poisoning, etc.)
5. **documentation** - Documentation accuracy (README errors, outdated docs)

**User Interaction:**
Use AskUserQuestion tool:
- Question: "Which quality scans would you like to run?"
- Header: "Scan Types"
- multiSelect: true
- Options:
  - "All scans (recommended)" → Run all scan types
  - "Critical only" → Run critical scan only
  - "Critical + Logic" → Run critical and logic scans
  - "Custom selection" → Ask user to specify which scans

**Default:** If user doesn't specify, run all scans.

<validation>
Validate selected scan types exist in reference.md:
- critical-scan → reference.md line ~5
- logic-scan → reference.md line ~100
- workflow-scan → reference.md line ~300
- security-scan → reference.md line ~400
- documentation-scan → reference.md line ~810

If user requests non-existent scan type, report error and suggest valid types.
</validation>

---

### Phase 5: Execute Scans

<action>
For each enabled scan type, spawn a specialized agent using Task tool:
</action>

```typescript
// Example: Critical scan
Task({
  subagent_type: "general-purpose",
  description: "Critical bugs scan",
  prompt: `${CRITICAL_SCAN_PROMPT_FROM_REFERENCE_MD}

Focus on src/ directory (HTTP client, SDK class, type generation scripts).

SDK-specific patterns to check:
- HTTP client error handling (src/http-client.ts)
- API method validation (src/socket-sdk-class.ts)
- Type generation scripts (scripts/generate-*.mjs)
- Promise handling and retry logic
- JSON parsing errors
- Rate limiting and timeout handling

Report findings in this format:
- File: path/to/file.ts:lineNumber
- Issue: Brief description
- Severity: Critical/High/Medium/Low
- Pattern: Code snippet
- Trigger: What input triggers this
- Fix: Suggested fix
- Impact: What happens if triggered

Scan systematically and report all findings. If no issues found, state that explicitly.`
})
```

**For each scan:**
1. Load agent prompt template from `reference.md`
2. Customize for socket-sdk-js context (focus on src/, scripts/, test/)
3. Spawn agent with Task tool using "general-purpose" subagent_type
4. Capture findings from agent response
5. Parse and categorize results

**Execution Order:** Run scans sequentially in priority order:
- critical (highest priority)
- logic
- workflow
- security
- documentation (lowest priority)

**Agent Prompt Sources:**
- Critical scan: reference.md starting at line ~12
- Logic scan: reference.md starting at line ~100
- Workflow scan: reference.md starting at line ~300
- Security scan: reference.md starting at line ~400
- Documentation scan: reference.md starting at line ~810

<validation>
**Structured Output Validation:**

After each agent returns, validate output structure before parsing:

```bash
# 1. Verify agent completed successfully
if [ -z "" ]; then
  echo "ERROR: Agent returned no output"
  exit 1
fi

# 2. Check for findings or clean report
if ! echo "" | grep -qE '(File:.*Issue:|No .* issues found|✓ Clean)'; then
  echo "WARNING: Agent output missing expected format"
  echo "Agent may have encountered an error or found no issues"
fi

# 3. Verify severity levels if findings exist
if echo "" | grep -q "File:"; then
  if ! echo "" | grep -qE 'Severity: (Critical|High|Medium|Low)'; then
    echo "WARNING: Findings missing severity classification"
  fi
fi

# 4. Verify fix suggestions if findings exist
if echo "" | grep -q "File:"; then
  if ! echo "" | grep -q "Fix:"; then
    echo "WARNING: Findings missing suggested fixes"
  fi
fi
```

**Manual Verification Checklist:**
- [ ] Agent output includes findings OR explicit "No issues found" statement
- [ ] All findings include file:line references
- [ ] All findings include severity level (Critical/High/Medium/Low)
- [ ] All findings include suggested fixes
- [ ] Agent output is parseable and structured

**For each scan completion:**
- Verify agent completed without errors
- Extract findings from agent output (or confirm "No issues found")
- Parse into structured format (file, issue, severity, fix)
- Track scan coverage (files analyzed)
- Log any validation warnings for debugging
</validation>

---

### Phase 6: Aggregate Findings

<action>
Collect all findings from agents and aggregate:
</action>

```typescript
interface Finding {
  file: string           // "src/http-client.ts:89"
  issue: string          // "Potential null pointer access"
  severity: "Critical" | "High" | "Medium" | "Low"
  scanType: string       // "critical"
  pattern: string        // Code snippet showing the issue
  trigger: string        // What causes this issue
  fix: string            // Suggested code change
  impact: string         // What happens if triggered
}
```

**Deduplication:**
- Remove duplicate findings across scans (same file:line, same issue)
- Keep the finding from the highest priority scan
- Track which scans found the same issue

**Prioritization:**
- Sort by severity: Critical → High → Medium → Low
- Within same severity, sort by scanType priority
- Within same severity+scanType, sort alphabetically by file path

<validation>
**Checkpoint:** Verify aggregation:
- Total findings count
- Breakdown by severity (N critical, N high, N medium, N low)
- Breakdown by scan type
- Duplicate removal count (if any)
</validation>

---

### Phase 7: Generate Report

<action>
Create structured quality report with all findings:
</action>

```markdown
# Quality Scan Report

**Date:** YYYY-MM-DD
**Repository:** socket-sdk-js
**Scans:** [list of scan types run]
**Files Scanned:** N
**Findings:** N critical, N high, N medium, N low

## Critical Issues (Priority 1) - N found

### src/http-client.ts:89
- **Issue**: Potential null pointer access in retry logic
- **Pattern**: `const result = response.data.items[0]`
- **Trigger**: When API returns empty array
- **Fix**: `const items = response.data?.items ?? []; if (items.length === 0) throw new Error('No items found'); const result = items[0]`
- **Impact**: Crashes SDK, breaks user applications
- **Scan**: critical

## High Issues (Priority 2) - N found

[Similar format for high severity issues]

## Medium Issues (Priority 3) - N found

[Similar format for medium severity issues]

## Low Issues (Priority 4) - N found

[Similar format for low severity issues]

## Scan Coverage

- **Critical scan**: N files analyzed in src/, scripts/
- **Logic scan**: N files analyzed (API methods, type generation)
- **Workflow scan**: N files analyzed (package.json, scripts/, .github/)

## Recommendations

1. Address N critical issues immediately before next release
2. Review N high-severity logic errors in HTTP client
3. Schedule N medium issues for next sprint
4. Low-priority items can be addressed during refactoring

## No Findings

[If a scan found no issues, list it here:]
- Critical scan: ✓ Clean
- Logic scan: ✓ Clean
```

**Output Report:**
1. Display report to console (user sees it)
2. Offer to save to file (optional): `reports/quality-scan-YYYY-MM-DD.md`

<validation>
**Report Quality Checks:**
- All findings include file:line references
- All findings include suggested fixes
- Findings are grouped by severity
- Scan coverage statistics included
- Recommendations are actionable
</validation>

---

### Phase 8: Complete

<completion_signal>
```xml
<promise>QUALITY_SCAN_COMPLETE</promise>
```
</completion_signal>

<summary>
Report these final metrics to the user:

**Quality Scan Complete**
========================
✓ Dependency updates: N repositories, N packages updated
✓ Repository cleanup: N junk files removed
✓ Scans completed: [list of scan types]
✓ Total findings: N (N critical, N high, N medium, N low)
✓ Files scanned: N
✓ Report generated: Yes
✓ Scan duration: [calculated from start to end]

**Dependency Update Summary:**
- socket-sdk-js: N packages updated
- socket-cli: N packages updated (or skipped)
- socket-btm: N packages updated (or skipped)
- socket-registry: N packages updated (or skipped)

**Repository Cleanup Summary:**
- SCREAMING_TEXT.md files removed: N
- Temporary test files removed: N
- Temp/backup files removed: N
- Log files cleaned up: N

**Critical Issues Requiring Immediate Attention:**
- N critical issues found
- Review report above for details and fixes

**Next Steps:**
1. Address critical issues immediately
2. Review high-severity findings
3. Schedule medium/low issues appropriately
4. Re-run scans after fixes to verify

All findings include file:line references and suggested fixes.
</summary>

</instructions>

## Success Criteria

- ✅ `<promise>QUALITY_SCAN_COMPLETE</promise>` output
- ✅ Dependencies updated in available repositories
- ✅ All enabled scans completed without errors
- ✅ Findings prioritized by severity (Critical → Low)
- ✅ All findings include file:line references
- ✅ Actionable suggestions provided for all findings
- ✅ Report generated with statistics and coverage metrics
- ✅ Duplicate findings removed

## Scan Types

See `reference.md` for detailed agent prompts with structured tags:

- **critical-scan** - Null access, promise rejections, race conditions, resource leaks
- **logic-scan** - Off-by-one errors, type guards, edge cases, algorithm correctness
- **workflow-scan** - Scripts, package.json, git hooks, CI configuration
- **security-scan** - GitHub Actions workflow security (runs zizmor scanner)
- **documentation-scan** - README accuracy, outdated examples, incorrect package names, missing documentation

All agent prompts follow Claude best practices with <context>, <instructions>, <pattern>, <output_format>, and <quality_guidelines> tags.

## Commands

This skill is self-contained. No external commands needed.

## Context

This skill provides systematic code quality analysis for socket-sdk-js by:
- Updating dependencies before scanning to ensure latest versions
- Spawning specialized agents for targeted analysis
- Using Task tool to run agents autonomously
- Embedding agent prompts in reference.md following best practices
- Generating prioritized, actionable reports
- Supporting partial scans (user can select specific scan types)

For detailed agent prompts with best practices structure, see `reference.md`.
