---
name: code-cleanup
description: "Detect stale TODOs, unused imports, and dead code."
user-invocable: false
argument-hint: "[<path-or-scope>]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
triggers:
  - "code cleanup"
  - "find small improvements"
  - "fix neglected issues"
  - "clean up code"
  - "quality of life fixes"
  - "find TODOs"
  - "stale comments"
  - "unused imports"
  - "technical debt scan"
routing:
  triggers:
    - "find dead code"
    - "stale TODOs"
    - "unused imports"
    - "clean up"
    - "tidy code"
    - "remove dead code"
    - "find unused"
  not_for: "multi-phase workflow orchestration or repo reorganization (use workflow). This skill finds dead code and stale TODOs in place."
  category: code-quality
  pairs_with:
    - code-linting
    - universal-quality-gate
    - comment-quality
---

# Code Cleanup Skill

Scan repositories for 9 categories of technical debt (TODOs, unused imports, dead code, missing type hints, deprecated functions, naming inconsistencies, high complexity, duplicate code, missing docstrings), prioritize findings by impact/effort ratio with time estimates, and generate structured markdown reports with exact file:line references. Can apply safe auto-fixes when the user grants explicit permission.

### Examples

**Focused cleanup** -- User says "Clean up the API handlers in src/api/". Read project config, scan src/api/ for all 9 categories, prioritize (5 unused imports auto-fixable, 2 stale TODOs >90d, 1 high-complexity function), present tiered report with auto-fix commands.

**Broad debt scan** -- User says "What's the state of technical debt in this repo?". Identify languages and source directories, run all applicable scans, group 47 findings into Quick Wins (12), Important (8), Polish (27), generate full report with effort estimates: 2h quick wins, 6h important, 4h polish.

**Auto-fix request** -- User says "Fix all the unused imports and sort them". Verify ruff/goimports available, scan for F401 and I001 violations only, report 23 unused imports across 8 files, user confirms, apply fixes, run tests, show diff.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| writing the cleanup report | `report-template.md` | Loads detailed guidance from `report-template.md`. |
| running per-language scans: unused imports, dead code, debug statements | `scan-commands.md` | Loads detailed guidance from `scan-commands.md`. |
| checking which cleanup tools are installed per language | `tools.md` | Loads detailed guidance from `tools.md`. |

## Instructions

### Phase 1: SCOPE

**Goal**: Determine what to scan and verify tooling is available.

**Step 1: Read project context**
- Check for CLAUDE.md, .gitignore, pyproject.toml, go.mod, package.json -- read and follow any repository CLAUDE.md before doing anything else, since it may contain project-specific exclusions or conventions that override defaults
- Identify primary languages and project structure

**Step 2: Determine scan scope**
- If the user specified a directory or issue type, use that exactly -- only scan for requested issue types or smart defaults, never build elaborate reporting dashboards or speculative features
- If the user specified only an issue type (e.g., "find unused imports"), scan all source directories for that type only
- If the request is vague ("clean up code"), ask the user for a target area rather than scanning the entire codebase, because unfocused scans produce overwhelming noise that users cannot act on
- Always exclude: vendor/, node_modules/, .venv/, build/, dist/, generated/, .git/ -- these contain third-party or generated code that the user cannot fix, so including them buries real findings
- Respect .gitignore patterns when determining what to scan

**Step 3: Verify tool availability**

Check which analysis tools are installed so you know what scans are possible before starting. Report missing tools with install commands.

```bash
# Python tools
command -v ruff && echo "ruff: available" || echo "ruff: MISSING (pip install ruff)"
command -v vulture && echo "vulture: available" || echo "vulture: MISSING (pip install vulture)"

# Go tools
command -v gocyclo && echo "gocyclo: available" || echo "gocyclo: MISSING (go install github.com/fzipp/gocyclo/cmd/gocyclo@latest)"
command -v goimports && echo "goimports: available" || echo "goimports: MISSING (go install golang.org/x/tools/cmd/goimports@latest)"
```

If critical tools are missing, offer to proceed with partial scan using available tools (grep, git blame are always available).

**Gate**: Scope defined, languages identified, tool availability known. Proceed only when gate passes.

### Phase 2: SCAN

**Goal**: Detect all cleanup opportunities within scope using deterministic tools.

Run applicable scans based on language and scope. See `references/scan-commands.md` for full command reference.

**Core scans (all languages)**:
1. **Stale TODOs**: grep for TODO/FIXME/HACK/XXX, then age every match with git blame -- a 180-day-old TODO about a data race is fundamentally different from yesterday's "TODO: add test case", so age-based triage is essential for prioritization
2. **Unused imports**: ruff (Python), goimports (Go)
3. **Dead code**: vulture (Python), staticcheck (Go)
4. **Complexity**: radon (Python), gocyclo (Go)

**Extended scans (if tools available)**:
5. Missing type hints (Python: ruff --select ANN)
6. Deprecated function usage (staticcheck, grep for known patterns)
7. Naming inconsistencies (grep for convention violations)
8. Duplicate code (pylint --enable=duplicate-code)
9. Missing docstrings (ruff --select D)

Collect all output with exact file:line references -- never summarize away specifics, because the user needs precise locations to act on findings. For each scan, record:
- Number of findings
- Files affected
- Whether findings are auto-fixable

If a scan tool is unavailable, note it as skipped and continue with remaining scans. Never abort the entire scan because one tool is missing.

**Gate**: All applicable scans complete with raw output collected. Proceed only when gate passes.

### Phase 3: PRIORITIZE

**Goal**: Rank findings by impact/effort ratio and categorize. Never present a flat unsorted list -- a critical 90-day-old security TODO buried among trivial missing docstrings wastes the user's attention.

**Step 1: Assign impact and effort**

| Issue Type | Impact | Effort | Priority Score |
|------------|--------|--------|----------------|
| Stale TODOs (>90 days) | High | Low | 8 |
| Unused imports | Medium | Trivial | 10 |
| Deprecated functions | High | Medium | 6 |
| High complexity (>20) | High | High | 5 |
| Dead code | Medium | Low | 7 |
| Missing type hints | Medium | Medium | 5 |
| Duplicate code | High | High | 5 |
| Missing docstrings | Medium | Medium | 5 |
| Naming inconsistencies | Low | Medium | 3 |
| Magic numbers | Low | Low | 5 |

**Step 2: Group into tiers**
- **Quick Wins** (High priority, low effort): Unused imports, stale TODOs, dead code -- present auto-fixable issues first so the user gets immediate value
- **Important** (High impact, medium+ effort): Deprecated functions, high complexity, duplicates
- **Polish** (Lower impact): Missing types, docstrings, naming, magic numbers

**Step 3: Estimate total effort per tier**

Include time estimates so the user can plan their cleanup budget:

| Issue Type | Time per Instance |
|------------|-------------------|
| Unused imports | 1-2 min (auto-fix) |
| Stale TODOs | 5-15 min each |
| Dead code removal | 5-10 min each |
| Magic numbers | 2-5 min each |
| Missing type hints | 10-20 min per function |
| Missing docstrings | 5-15 min per function |
| Naming fixes | 10-30 min per violation |
| High complexity refactor | 30-120 min per function |
| Duplicate code elimination | 30-90 min per instance |
| Deprecated function replacement | 15-60 min per usage |

Multiply by instance count for tier totals.

**Gate**: All findings categorized and prioritized with effort estimates. Proceed only when gate passes.

### Phase 4: REPORT

**Goal**: Present findings in structured, actionable format.

This skill defaults to read-only scan and report. Do not modify any files during this phase.

Generate report with this structure:
1. Executive summary (total issues, tier counts, estimated effort)
2. Quick Wins with auto-fix commands where available
3. Important issues with specific suggestions
4. Polish items grouped by type
5. Files sorted by issue count

See `references/report-template.md` for complete template.

Print the complete report to stdout so the user can inspect every finding in full.

If the user provided `--output {file}` flag, also write report to the specified file.

For each finding in the report:
- Include exact file:line reference
- Show 3 lines of surrounding context for quick comprehension
- Provide specific fix suggestion or auto-fix command
- Note whether the fix is auto-fixable or requires manual effort

Remove any intermediate scan outputs at completion, keeping only the final report.

**Gate**: Report delivered with all findings, exact references, and actionable suggestions.

### Phase 5: FIX (Optional -- only with explicit permission)

**Goal**: Apply safe, deterministic fixes.

MUST have explicit user permission before proceeding. Never auto-enter this phase -- the user expected a report, not file modifications, and changes may conflict with in-progress work.

**Step 1: Confirm scope with user**

Before applying any fixes, confirm exactly what will be changed:
```markdown
Will apply these auto-fixes:
- Remove {N} unused imports across {N} files
- Sort imports in {N} files
- Format {N} files

{N} files will be modified. Proceed? (y/n)
```

**Step 2: Apply auto-fixes**

Apply fixes in order of safety (most safe first):

```bash
# Python - safe fixes only
ruff check . --select F401,I001 --fix    # Remove unused imports, sort
ruff format .                             # Consistent formatting

# Go - safe fixes only
goimports -w .                            # Remove unused imports, sort, format
gofmt -w .                                # Consistent formatting
go mod tidy                               # Clean up go.mod/go.sum
```

Apply only fixes flagged as safe by ruff in this phase. Keep variable names, function structure, and semantic behavior unchanged.

**Step 3: Validate fixes**

Run the project's existing test suite to verify nothing broke:

```bash
# Python
pytest                  # Run full test suite
ruff check .           # Verify no new lint issues

# Go
go test ./...          # Run full test suite
go build ./...         # Verify build succeeds
golangci-lint run      # Verify no new lint issues
```

**Step 4: Show diff and results**

```bash
git diff --stat        # Summary of changes
git diff               # Full diff for review
```

Present results:
```markdown
## Fix Results
- Files modified: {N}
- Imports removed: {N}
- Tests: PASS ({N} tests)
- Lint: CLEAN

Review diff above. Commit when satisfied.
```

**Step 5: Handle failures**

If tests fail after auto-fix:
1. Roll back ALL changes immediately: `git checkout .`
2. Report exactly which test(s) failed and why
3. Suggest applying fixes incrementally (one file at a time) with testing between each

Keep the repository in a working state after the cleanup pass.

**Gate**: All auto-fixes applied, tests pass, diff shown to user. Repository is in a clean, working state.

---

## Error Handling

### Error: "Required analysis tool not found"
Cause: ruff, vulture, gocyclo, or other tool not installed
Solution:
1. Report which tools are missing with install commands
2. Offer to proceed with partial scan using available tools
3. grep and git blame are always available as fallback

### Error: "Not a git repository"
Cause: Cannot use git blame for TODO aging
Solution: Continue scan but mark all TODO ages as "unknown". Warn user that age-based triage is unavailable.

### Error: "Tests fail after auto-fix"
Cause: Auto-fix changed behavior that tests depend on
Solution:
1. Roll back all changes immediately: `git checkout .`
2. Report which fixes caused failures
3. Suggest applying fixes file-by-file with incremental testing

### Error: "Permission denied modifying files"
Cause: Files are read-only, locked, or user did not grant write permission
Solution:
1. Respect the current permission boundary and report any files that cannot be modified
2. Report which files could not be modified and why
3. Provide the fix commands so user can run them manually

---

## References

### Reference Files
- `${CLAUDE_SKILL_DIR}/references/scan-commands.md`: Language-specific scan commands and expected output
- `${CLAUDE_SKILL_DIR}/references/report-template.md`: Full structured report template
- `${CLAUDE_SKILL_DIR}/references/tools.md`: Tool installation, versions, and capabilities
