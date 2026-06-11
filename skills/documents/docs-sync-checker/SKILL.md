---
name: docs-sync-checker
description: "Detect documentation drift against filesystem state."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
routing:
  triggers:
    - "check doc drift"
    - "sync documentation"
    - "stale docs"
    - "documentation drift"
    - "README outdated"
  category: documentation
  pairs_with:
    - generate-claudemd
    - codebase-overview
---

# Documentation Sync Checker Skill

Deterministic 4-phase drift detector that compares the filesystem against README entries. Each phase (Scan, Cross-Reference, Detect, Report) has a gate that must pass before proceeding. The skill produces a sync score (percentage of tools properly documented) and actionable fix suggestions for every detected issue.

This skill checks presence, absence, and version alignment only -- it does not judge description quality, generate documentation content, resolve merge conflicts, validate cross-references, or track when drift occurred. Suggested fixes use YAML descriptions verbatim; content generation and quality assessment require different skills.

Optional flags: `--auto-fix` (experimental, requires explicit opt-in), `--strict` (exit code 1 on issues), `--format json` (machine-readable output for CI/CD).

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| documentation work | `documentation-structure.md` | Loads detailed guidance from `documentation-structure.md`. |
| before/after doc-update examples: adding skill docs, removing deprecated agent docs | `examples.md` | Loads detailed guidance from `examples.md`. |
| wiring the checker into CI, pre-commit, or auto-fix mode | `integration-guide.md` | Loads detailed guidance from `integration-guide.md`. |
| expected table and list formats per README file | `markdown-formats.md` | Loads detailed guidance from `markdown-formats.md`. |
| which docs must list which tools; sync score and deprecation rules | `sync-rules.md` | Loads detailed guidance from `sync-rules.md`. |

## Instructions

### Phase 1: SCAN

**Goal**: Discover all skills, agents, and commands in the repository filesystem. All discovery (file existence checks, YAML parsing, markdown extraction) must be deterministic -- no AI judgment on content quality.

**Step 1: Run the scan script**

```bash
python3 skills/meta/docs-sync-checker/scripts/scan_tools.py --repo-root $HOME/vexjoy-agent
```

**Step 2: Validate discovery results**

For each tool type, verify:

Skills (`skills/*/SKILL.md`):
- File has opening `---` and closing `---` YAML delimiters
- YAML contains `name`, `description`, and `version` fields
- `name` field matches directory name (e.g., `skills/code-quality/code-linting/` has `name: code-linting`)

Agents (`agents/*.md`):
- File has valid YAML frontmatter with `name` field
- Filename (without .md) matches YAML `name` value

Commands (`commands/**/*.md`):
- File exists as markdown in commands/ directory
- Namespaced commands in subdirectories (e.g., `commands/code/cleanup.md`) are detected

**Step 3: Count and verify**

```markdown
## Scan Results
Skills found: [N]
Agents found: [N]
Commands found: [N]
YAML errors: [N] (must be 0 to proceed)
```

**Gate**: All tools discovered, all YAML valid, counts >0 for each type. Proceed only after the gate passes.

### Phase 2: CROSS-REFERENCE

**Goal**: Extract documented tools from README files and compare with discovered tools. Each tool type has a primary documentation file: skills belong in `docs/skills.md`, agents in `agents/README.md`, commands in `commands/README.md`.

**Step 1: Run the documentation parser**

```bash
python3 skills/meta/docs-sync-checker/scripts/parse_docs.py --repo-root $HOME/vexjoy-agent --scan-results /tmp/scan_results.json
```

**Step 2: Parse each documentation file**

These are the five documentation files to check -- no others:

| File | Format | What to Extract |
|------|--------|-----------------|
| `docs/skills.md` | Markdown table | Name, Description, Command, Hook columns |
| `agents/README.md` | Table or list | Name, Description fields |
| `commands/README.md` | Markdown list | /command-name - Description items |
| `README.md` | Inline references | Pattern-match `skill: X`, `/command`, `agent-name` |
| `docs/REFERENCE.md` | Section headers | `### tool-name` headers with descriptions |

**Step 3: Build documented-tools registry**

For each documentation file, collect the set of tool names found. This creates a mapping of `{file -> [tool_names]}` that Phase 3 will compare against the filesystem scan.

**Step 4: Verify parse completeness**

- All 5 documentation files found and parsed (warn if any missing)
- No parse errors on table/list structures
- Tool names extracted from each file

**Gate**: All documentation files parsed without errors. Proceed only after the gate passes.

### Phase 3: DETECT

**Goal**: Compare discovered tools with documented tools to identify drift. This is a point-in-time snapshot -- it cannot tell you when drift occurred, only that it exists now.

**Step 1: Compute set differences**

For each tool type and its primary documentation file:
- `missing = filesystem_tools - documented_tools` (tools that exist but are not documented)
- `stale = documented_tools - filesystem_tools` (documented tools that no longer exist -- users waste time trying to invoke non-existent tools, so always flag these)

**Step 2: Check version consistency**

For tools that appear in both sets, compare:
- YAML `version` field vs. documented version (if version is documented)
- Flag mismatches where YAML is authoritative source of truth

**Step 3: Categorize and assign severity**

Severity reflects user impact: missing entries mean tools are undiscoverable, stale entries waste time, version mismatches cause confusion.

| Category | Condition | Severity |
|----------|-----------|----------|
| Missing Entry | Tool in filesystem, not in primary README | HIGH |
| Stale Entry | Tool in README, not in filesystem | MEDIUM |
| Version Mismatch | YAML version differs from documented | LOW |
| Incomplete Entry | Documentation missing required fields | LOW |

**Step 4: Record issue details**

For each issue, capture: tool type, tool name, tool path, affected documentation file(s), severity, and suggested fix action.

**Gate**: All issues categorized with severity. Proceed only after the gate passes.

### Phase 4: REPORT

**Goal**: Generate human-readable report with actionable fix suggestions. Report facts concisely -- show data, not self-congratulatory descriptions. Target 100% sync score; even one missing entry erodes trust in all documentation.

**Step 1: Run the report generator**

```bash
python3 skills/meta/docs-sync-checker/scripts/generate_report.py --issues /tmp/issues.json --output /tmp/sync-report.md
```

**Step 2: Verify report structure**

Report must include these sections:

1. **Summary** -- Total tools, issue counts by severity, sync score
   ```
   sync_score = (total_tools - total_issues) / total_tools * 100
   ```

2. **HIGH Priority: Missing Entries** -- For each missing tool, provide the exact markdown row/item to add to the appropriate README file

3. **MEDIUM Priority: Stale Entries** -- For each stale tool, identify the file and line to remove

4. **LOW Priority: Version Mismatches** -- For each mismatch, show YAML version (authoritative) vs. documented version

5. **Files Checked** -- List each documentation file with count of tools parsed from it

**Step 3: Validate actionability**

Every issue in the report must have a concrete suggested fix. No issue should say "review manually" without specifying what to review and where. The fix should enable a single-commit resolution -- tool files and documentation entries should be added/removed together.

**Step 4: Report format for missing entries**

For each missing skill, generate a suggested table row:
```markdown
| skill-name | Description from YAML | `skill: skill-name` | - |
```

For each missing agent, generate a suggested table row:
```markdown
| agent-name | Description from YAML |
```

For each missing command, generate a suggested list item:
```markdown
- `/command-name` - Description from command file
```

**Step 5: Cleanup**

Remove any helper scripts and debug outputs created during execution.

**Gate**: Report generated with actionable suggestions for every issue.

### Examples

#### Example 1: New Skill Missing from README
User created `skills/my-new-skill/SKILL.md` but forgot to update `docs/skills.md`.
Actions:
1. SCAN discovers `my-new-skill` in filesystem
2. CROSS-REFERENCE parses docs/skills.md, does not find `my-new-skill`
3. DETECT flags as HIGH severity missing entry
4. REPORT suggests exact table row to add to docs/skills.md

#### Example 2: Removed Agent Still Documented
User deleted `agents/old-agent.md` but `agents/README.md` still lists it.
Actions:
1. SCAN does not find `old-agent` in filesystem
2. CROSS-REFERENCE finds `old-agent` in agents/README.md
3. DETECT flags as MEDIUM severity stale entry
4. REPORT suggests removing the row from agents/README.md

#### Example 3: Version Bump Without Doc Update
User updated `version: 2.0.0` in `skills/code-quality/code-linting/SKILL.md` but `docs/REFERENCE.md` still shows `Version: 1.5.0`.
Actions:
1. SCAN reads YAML version as 2.0.0
2. CROSS-REFERENCE reads documented version as 1.5.0 from docs/REFERENCE.md
3. DETECT flags as LOW severity version mismatch
4. REPORT suggests updating version line in docs/REFERENCE.md to 2.0.0

#### Example 4: Batch Changes After Refactor
User created 3 new skills and deleted 2 old ones in a refactoring PR.
Actions:
1. SCAN discovers 3 new skills in filesystem, does not find 2 removed skills
2. CROSS-REFERENCE finds 2 stale entries and 3 absent entries in docs/skills.md
3. DETECT flags 3 HIGH (missing) + 2 MEDIUM (stale) issues
4. REPORT provides exact table rows to add and identifies rows to remove

## Error Handling

### Error: "YAML Parse Error"
Cause: Invalid frontmatter -- missing `---` delimiters, tabs instead of spaces, or missing required fields
Solution:
1. Check file has opening `---` on line 1 and closing `---` after YAML block
2. Verify no tab characters in YAML (spaces only)
3. Confirm required fields present: `name`, `description`, `version`
4. Validate manually: `head -20 {file_path}` and check syntax

### Error: "Documentation File Not Found"
Cause: Expected README file does not exist at expected path
Solution:
1. Verify --repo-root path is correct
2. Check that docs/skills.md, agents/README.md, commands/README.md exist
3. If file is legitimately missing, create a placeholder with the expected table/list header
4. Re-run scan after creating placeholder

### Error: "No Tools Discovered"
Cause: Wrong --repo-root path, empty directories, or no SKILL.md files
Solution:
1. Verify the repo root path points to the correct repository
2. Confirm skills/, agents/, commands/ directories exist and are not empty
3. Check that skill directories contain SKILL.md (not just other files)
4. Run with --debug flag for verbose discovery output

### Error: "Markdown Parse Error"
Cause: Table missing separator row, mismatched column counts, or malformed list items
Solution:
1. Check table has header row, separator row (`|---|---|`), and data rows
2. Verify all rows have the same number of pipe-delimited columns
3. For lists, verify consistent format: `- /command - Description`
4. See `references/markdown-formats.md` for complete format specifications

---

## References
- `${CLAUDE_SKILL_DIR}/references/documentation-structure.md`: Documentation file matrix, required fields per location, cross-reference requirements
- `${CLAUDE_SKILL_DIR}/references/markdown-formats.md`: Expected table/list formats for each README file, parsing rules, common formatting errors
- `${CLAUDE_SKILL_DIR}/references/sync-rules.md`: Synchronization rules, severity levels, deprecation handling, namespace rules
- `${CLAUDE_SKILL_DIR}/references/examples.md`: Before/after examples for adding, removing, updating, and batch documentation changes
- `${CLAUDE_SKILL_DIR}/references/integration-guide.md`: CI/CD setup, pre-commit hooks, auto-fix mode, JSON output, workflow integration
