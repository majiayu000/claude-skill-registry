---
name: embed-acs
description: Auto-embed Acceptance Criteria from living docs into increment spec.md for hook compatibility
---

# Embed Acceptance Criteria from Living Docs

You are helping the user embed Acceptance Criteria from living documentation into increment spec.md.

## Context

**Problem**: The AC sync hook requires ACs to be in spec.md, but some increments use `structure: user-stories` which references external living docs without embedding ACs inline.

**Solution**: This command auto-embeds ACs from living docs into spec.md, ensuring sync hooks work correctly.

**Architecture**: spec.md is ALWAYS the source of truth for ACs, even when living docs exist as a documentation layer. (See ADR-0062)

## Usage

```bash
/sw:embed-acs <increment-id>
```

## Arguments

- `<increment-id>`: Required. Increment ID (e.g., "0050", "50", "0050-feature-name")

## Workflow

### Step 1: Parse and Validate Arguments

1. **Extract increment ID**:
   - Parse from command: `/sw:embed-acs 0050` → "0050"
   - Normalize to 4-digit format: "0050"
   - Support formats: "50", "0050", "0050-feature-name"

2. **Validate increment exists**:
   - List directories in `.specweave/increments/`
   - Find matching increment (e.g., `0050-external-tool-import-phase-1b-7`)
   - If not found: Show error with available increments

**Example output if not found**:
```
❌ Error: Increment 0050 not found

Available increments:
  • 0048-external-tool-import-enhancement
  • 0049-cli-first-init-flow

Usage: /sw:embed-acs <increment-id>
```

### Step 2: Validate Increment Structure

1. **Check spec.md exists**:
   ```bash
   ls .specweave/increments/0050-*/spec.md
   ```

2. **Check for `structure: user-stories` in frontmatter**:
   ```bash
   grep "structure: user-stories" spec.md
   ```

3. **If NOT using living docs structure**:
   ```
   ℹ️  Info: Increment 0050 does not use 'structure: user-stories'

   This command is intended for increments that reference external living docs.
   For standard increments, ACs should already be in spec.md.

   Do you want to proceed anyway? [Y/n]:
   ```

### Step 3: Find Living Docs Path

1. **Extract feature_id from spec.md frontmatter**:
   ```bash
   grep "feature_id:" spec.md | cut -d: -f2 | tr -d ' '
   ```

2. **Construct living docs path**:
   ```
   .specweave/docs/internal/specs/specweave/{feature_id}/
   ```

3. **Validate living docs path exists**:
   ```bash
   ls .specweave/docs/internal/specs/specweave/FS-048/
   ```

4. **If living docs not found**:
   ```
   ❌ Error: Living docs not found for feature FS-048

   Expected path: .specweave/docs/internal/specs/specweave/FS-048/
   Actual path: Not found

   This increment may not have living docs, or they're in a different location.

   Please specify living docs path manually:
     /sw:embed-acs 0050 --living-docs-path <path>
   ```

### Step 4: Extract User Stories from spec.md

1. **Read user_stories from frontmatter**:
   ```yaml
   user_stories:
     - US-001
     - US-002
     - US-004
   ```

2. **Display user stories to embed**:
   ```
   Found 7 user stories in spec.md frontmatter:
     • US-001: Smart Pagination During Init
     • US-002: CLI-First Defaults
     • US-004: Smart Caching with TTL
     • US-005: Dedicated Import Commands
     • US-006: ADO Area Path Mapping
     • US-007: Progress Tracking
     • US-008: Smart Filtering
   ```

### Step 5: Extract ACs from Living Docs

1. **For each user story**, find corresponding file:
   ```bash
   # Try multiple file naming patterns
   find .specweave/docs/internal/specs/specweave/FS-048/ -name "us-001-*.md"
   find .specweave/docs/internal/specs/specweave/FS-048/ -name "US-001.md"
   ```

2. **Extract ACs from each file**:
   ```bash
   grep -E "^### AC-US[0-9]+-[0-9]+:" us-001-smart-pagination-during-init.md
   ```

3. **Display extraction progress**:
   ```
   Extracting ACs from living docs...
     ✓ US-001: Found 5 ACs (AC-US1-01 to AC-US1-05)
     ✓ US-002: Found 4 ACs (AC-US2-01 to AC-US2-04)
     ✓ US-004: Found 5 ACs (AC-US4-01 to AC-US4-05)
     ✓ US-005: Found 7 ACs (AC-US5-01 to AC-US5-07)
     ✓ US-006: Found 6 ACs (AC-US6-01 to AC-US6-06)
     ✓ US-007: Found 6 ACs (AC-US7-01 to AC-US7-06)
     ✓ US-008: Found 6 ACs (AC-US8-01 to AC-US8-06)

   Total: 39 Acceptance Criteria extracted
   ```

### Step 6: Check for Existing ACs

1. **Check if spec.md already has AC section**:
   ```bash
   grep -q "## Acceptance Criteria" spec.md
   ```

2. **If ACs already exist**:
   ```
   ⚠️  Warning: spec.md already contains Acceptance Criteria section

   Found 39 existing ACs in spec.md.

   What would you like to do?
     [R] Replace existing ACs with freshly embedded ones
     [M] Merge (keep existing + add missing)
     [C] Cancel

   Choice:
   ```

3. **If user chooses "Replace"**: Remove old AC section, add new one
4. **If user chooses "Merge"**: Smart merge (add only missing ACs)
5. **If user chooses "Cancel"**: Exit without changes

### Step 7: Format and Embed ACs

1. **Format ACs as markdown**:
   ```markdown
   ## Acceptance Criteria

   <!-- Auto-synced from living docs -->

   ### US-001: Smart Pagination During Init

   - [ ] **AC-US1-01**: 50-Project Limit During Init
   - [ ] **AC-US1-02**: Explicit Choice Prompt
   - [ ] **AC-US1-03**: Async Fetch for "Import All"
   - [ ] **AC-US1-04**: Init Completes < 30 Seconds
   - [ ] **AC-US1-05**: No Timeout Errors

   ### US-002: CLI-First Defaults

   - [ ] **AC-US2-01**: "Import All" as Default Choice
   - [ ] **AC-US2-02**: All Projects Checked in Checkbox Mode
   - [ ] **AC-US2-03**: Clear Deselection Instructions
   - [ ] **AC-US2-04**: Easy Override for "Select None"

   ...
   ```

2. **Find insertion point in spec.md**:
   - After "## Implementation Summary" section, OR
   - Before final line if no summary section

3. **Use Edit tool to insert ACs**:
   ```typescript
   Edit({
     file_path: "spec.md",
     old_string: "**See**: [plan.md](./plan.md)...",
     new_string: "**See**: [plan.md](./plan.md)...\n\n---\n\n" + acMarkdown
   });
   ```

### Step 8: Update metadata.json

1. **Count total ACs**:
   ```bash
   grep -cE "^- \[ \] \*\*AC-US[0-9]+-[0-9]+\*\*:" spec.md
   ```

2. **Update metadata.json**:
   ```json
   {
     "total_acs": 39,
     "completed_acs": 0
   }
   ```

3. **Use Edit tool to update**:
   ```typescript
   Edit({
     file_path: "metadata.json",
     old_string: '"total_acs": 32,',
     new_string: '"total_acs": 39,'
   });
   ```

### Step 9: Validate Embedding

1. **Re-count ACs in spec.md**:
   ```bash
   grep -cE "^- \[[x ]\] \*\*AC-US[0-9]+-[0-9]+\*\*:" spec.md
   ```

2. **Validate format**:
   - All ACs follow pattern: `- [ ] **AC-US1-01**: Title`
   - No duplicate AC IDs
   - All user stories represented

3. **Display validation results**:
   ```
   ✅ Validation: PASSED

   Embedded 39 Acceptance Criteria into spec.md:
     • US-001: 5 ACs
     • US-002: 4 ACs
     • US-004: 5 ACs
     • US-005: 7 ACs
     • US-006: 6 ACs
     • US-007: 6 ACs
     • US-008: 6 ACs

   metadata.json updated: total_acs = 39

   Next steps:
     1. Review embedded ACs in spec.md
     2. Run: /sw:validate 0050
     3. Start work: /sw:do
   ```

## Flags (Optional)

### `--living-docs-path <path>`

Manually specify living docs path if auto-detection fails:

```bash
/sw:embed-acs 0050 --living-docs-path .specweave/docs/internal/specs/specweave/FS-048
```

### `--dry-run`

Preview what would be embedded without modifying files:

```bash
/sw:embed-acs 0050 --dry-run
```

**Output**:
```
[DRY RUN] Would embed 39 ACs into spec.md

Preview:
  • US-001: 5 ACs (AC-US1-01 to AC-US1-05)
  • US-002: 4 ACs (AC-US2-01 to AC-US2-04)
  ...

No files modified.
```

### `--force`

Skip confirmation prompts:

```bash
/sw:embed-acs 0050 --force
```

## Error Handling

### Living Docs Not Found
```
❌ Error: Living docs not found for feature FS-048

Expected: .specweave/docs/internal/specs/specweave/FS-048/
Found: Directory does not exist

Possible solutions:
  1. Check if feature_id in spec.md is correct
  2. Manually specify path: --living-docs-path <path>
  3. Create living docs first: /sw:sync-docs
```

### No User Stories in spec.md
```
❌ Error: No user_stories field in spec.md frontmatter

This command requires user_stories to be listed in spec.md.

Add to spec.md frontmatter:
  user_stories:
    - US-001
    - US-002
    ...
```

### User Story File Not Found
```
⚠️  Warning: User story file not found for US-003

Expected paths tried:
  • .specweave/docs/internal/specs/specweave/FS-048/us-003.md
  • .specweave/docs/internal/specs/specweave/FS-048/US-003.md
  • .specweave/docs/internal/specs/specweave/FS-048/us-003-*.md

Continuing with remaining user stories...
```

### No ACs Found in User Story
```
⚠️  Warning: No ACs found in US-005 file

File: .specweave/docs/internal/specs/specweave/FS-048/us-005-dedicated-import-commands.md

This file may be incomplete or use a different AC format.
Skipping US-005 for now.
```

## Integration with Other Commands

This command is referenced by:

1. **`/sw:validate`**: Suggests running `/sw:embed-acs` when ACs are missing
2. **`/sw:do`**: Pre-start hook suggests this command if validation fails
3. **`/sw:increment`**: Should auto-call this when creating `structure: user-stories` increments

## Examples

### Example 1: Basic Usage

```bash
/sw:embed-acs 0050
```

**Output**:
```
Embedding ACs from living docs for increment 0050-external-tool-import-phase-1b-7...

Living docs path: .specweave/docs/internal/specs/specweave/FS-048/

Extracting ACs...
  ✓ US-001: 5 ACs
  ✓ US-002: 4 ACs
  ✓ US-004: 5 ACs
  ✓ US-005: 7 ACs
  ✓ US-006: 6 ACs
  ✓ US-007: 6 ACs
  ✓ US-008: 6 ACs

✅ Embedded 39 ACs into spec.md
✅ Updated metadata.json (total_acs: 39)
```

### Example 2: Dry Run

```bash
/sw:embed-acs 0050 --dry-run
```

**Output**:
```
[DRY RUN] Embedding ACs for increment 0050...

Would extract 39 ACs from 7 user stories.
No files would be modified.

To apply changes, run without --dry-run flag.
```

### Example 3: Manual Path

```bash
/sw:embed-acs 0050 --living-docs-path .specweave/docs/internal/specs/custom/FS-048
```

**Output**:
```
Using custom living docs path: .specweave/docs/internal/specs/custom/FS-048

Extracting ACs...
  ✓ US-001: 5 ACs
  ...
```

## Related Commands

- `/sw:increment`: Create new increment (should auto-embed ACs)
- `/sw:validate`: Validate increment (checks AC presence)
- `/sw:do`: Start increment (pre-start hook validates ACs)
- `/sw:sync-docs`: Sync living documentation

## Related Documentation

- **ADR-0062**: AC Embedding Architecture
- **CLAUDE.md**: Rule #X (spec.md AC presence requirement)
- **src/utils/ac-embedder.ts**: AC embedding utility (implementation)
- **src/core/validators/ac-presence-validator.ts**: AC presence validation

---

**Important**: This command should NOT be needed in the future if spec generators are updated to auto-embed ACs during increment creation. Consider this a **migration/fix utility** for existing increments.
