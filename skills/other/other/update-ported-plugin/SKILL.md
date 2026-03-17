---
name: update-ported-plugin
description: Updates previously-ported plugins when source plugins change or the target platform evolves
user-invocable: true
disable-model-invocation: true
argument-hint: "--target <platform> [--source-only] [--platform-only] [--output-dir <path>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - Task
---

# Update Ported Plugin

Apply incremental updates to previously-ported plugins when source plugins have changed or the target platform has evolved. Reads the PORT-METADATA embedded in MIGRATION-GUIDE.md to determine the baseline, detects source diffs and platform drift, and applies targeted updates without re-running the full port-plugin workflow.

**CRITICAL: Complete ALL 5 phases.** The workflow is not complete until Phase 5: Output & Refresh is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output. Text output is only for status updates and informational summaries.

### Plan Mode Behavior

**CRITICAL**: This skill performs an interactive update workflow, NOT an implementation plan. Proceed with the full detection and update workflow immediately -- do not defer to an "execution phase".

## Phase Overview

Execute these phases in order, completing ALL of them:

1. **Load Context** -- Parse arguments, locate MIGRATION-GUIDE.md, extract and validate PORT-METADATA
2. **Detect Changes** -- Diff source files against baseline commit, check platform adapter staleness
3. **Apply Source Changes** -- Incrementally update ported files for source modifications
4. **Apply Platform Changes** -- Update ported files for platform adapter drift
5. **Output & Refresh** -- Write files, refresh metadata, update history, and summarize

---

## Phase 1: Load Context

**Goal:** Parse arguments, locate the MIGRATION-GUIDE.md from a previous port, extract the PORT-METADATA block, and validate that the baseline is intact.

### Step 1: Parse Arguments

Parse `$ARGUMENTS` for:
- `--target <platform>` -- Target platform slug (default: `opencode`)
- `--source-only` -- Only detect and apply source changes; skip platform change detection
- `--platform-only` -- Only detect and apply platform changes; skip source change detection
- `--output-dir <path>` -- Override output directory for updated files (default: write in-place)

Set `TARGET_PLATFORM`, `SOURCE_ONLY`, `PLATFORM_ONLY`, and `OUTPUT_DIR` from parsed arguments. If both `--source-only` and `--platform-only` are specified, they are mutually exclusive -- inform the user and proceed with full update (both flags `false`).

### Step 2: Load Settings

Check `.claude/agent-alchemy.local.md` for a `plugin-tools` section (`default-target`, `default-output-dir`). Apply settings as defaults -- CLI arguments override.

### Step 3: Locate MIGRATION-GUIDE.md

Search order: (1) `{OUTPUT_DIR}/MIGRATION-GUIDE.md` if specified, (2) `ported/{TARGET_PLATFORM}/MIGRATION-GUIDE.md`, (3) `Glob: **/MIGRATION-GUIDE.md`.

If multiple found, present for selection:

```yaml
AskUserQuestion:
  questions:
    - header: "Multiple Migration Guides Found"
      question: "Multiple MIGRATION-GUIDE.md files were found. Which one should be updated?"
      options:
        - label: "{path_1}"
          description: "Last modified: {date}"
        - label: "{path_2}"
          description: "Last modified: {date}"
      multiSelect: false
```

If none found, offer options via `AskUserQuestion`: "Run /port-plugin" (start fresh), "Specify path manually", or "Cancel". Handle accordingly. Store the located path as `MIGRATION_GUIDE_PATH` and its parent as `PORT_OUTPUT_DIR`.

### Step 4: Extract PORT-METADATA

Read the MIGRATION-GUIDE.md file and extract the `PORT-METADATA` HTML comment block:

```
Read: {MIGRATION_GUIDE_PATH}
```

Search for the `<!-- PORT-METADATA ... PORT-METADATA -->` block and parse the YAML-like content to extract: `source_commit`, `port_date`, `adapter_version`, `target_platform`, `target_platform_version`, and `components` list (each with `source`, `target`, `fidelity`).

**Error handling -- Missing metadata block:**

```yaml
AskUserQuestion:
  questions:
    - header: "Missing PORT-METADATA"
      question: "The MIGRATION-GUIDE.md does not contain a PORT-METADATA block. How would you like to proceed?"
      options:
        - label: "Reconstruct metadata"
          description: "Scan the output directory and git history to rebuild the metadata block"
        - label: "Run fresh port"
          description: "Start over with /port-plugin"
        - label: "Cancel"
          description: "Exit the update workflow"
      multiSelect: false
```

If reconstructing: scan `PORT_OUTPUT_DIR` for converted files via `Glob`, find the most recent port commit via `git log --oneline --all -- {MIGRATION_GUIDE_PATH}`, and build best-effort metadata. Warn user it may be incomplete.

**Error handling -- Malformed metadata:** Fall back to line-by-line regex extraction of key-value pairs and `- source:` / `target:` / `fidelity:` patterns. If fallback fails, present the reconstruction option.

Store extracted metadata as `PORT_METADATA`.

### Step 5: Validate Baseline

Verify the baseline is intact:

1. **Source commit**: `git rev-parse --verify {PORT_METADATA.source_commit}` -- if not found, set `SOURCE_COMMIT_VALID = false` and warn
2. **Source files**: Check each `component.source` still exists; build `MISSING_SOURCES` list
3. **Target files**: Check each `{PORT_OUTPUT_DIR}/{component.target}` still exists; build `MISSING_TARGETS` list
4. **Adapter file**: Verify `${CLAUDE_PLUGIN_ROOT}/references/adapters/{PORT_METADATA.target_platform}.md` exists

### Step 6: Display Summary and Confirm

Present the baseline summary via `AskUserQuestion`:

```yaml
AskUserQuestion:
  questions:
    - header: "Port Baseline Summary"
      question: |
        Previous port details:
        - Port date: {PORT_METADATA.port_date}
        - Source commit: {PORT_METADATA.source_commit} (short hash)
        - Components: {PORT_METADATA.components.length} ported
        - Adapter version: {PORT_METADATA.adapter_version}
        - Target platform: {PORT_METADATA.target_platform} v{PORT_METADATA.target_platform_version}
        {If MISSING_SOURCES.length > 0:}
        - WARNING: {MISSING_SOURCES.length} source file(s) no longer exist
        {If MISSING_TARGETS.length > 0:}
        - WARNING: {MISSING_TARGETS.length} target file(s) no longer exist
        {If !SOURCE_COMMIT_VALID:}
        - WARNING: Source commit not found in git history (history may have been rewritten)

        Proceed with update check?
      options:
        - label: "Proceed"
          description: "Check for source and platform changes since the last port"
        - label: "View missing files"
          description: "Show details of missing source or target files before proceeding"
        - label: "Cancel"
          description: "Exit the update workflow"
      multiSelect: false
```

If "View missing files": list all missing files, then re-present proceed/cancel. If "Cancel": exit gracefully.

---

## Phase 2: Detect Changes

**Goal:** Identify what has changed since the original port -- both in source plugin files and on the target platform -- and present a combined summary for the user to scope the update.

Run two parallel change detection tracks (unless `--source-only` or `--platform-only` was specified).

### Track A: Source Changes

Skip this track if `PLATFORM_ONLY` is `true`.

#### Step A1: Diff Source Files

```bash
git diff {PORT_METADATA.source_commit}..HEAD -- {space-separated list of source paths}
```

If `SOURCE_COMMIT_VALID` is `false`, fall back to `git log --since="{PORT_METADATA.port_date}"` and diff each file against its state at the closest commit to the port date.

#### Step A2: Detect New and Deleted Files

```bash
git diff --name-status {PORT_METADATA.source_commit}..HEAD -- {source parent directories}
```

Parse output: `A` (new), `D` (deleted), `M` (modified, already in A1), `R` (renamed -- track both paths).

#### Step A3: Classify Changes

For each changed source file, classify the change into one of three categories:

| Classification | Examples | Action |
|---------------|----------|--------|
| **Structural** | Frontmatter changes, new/removed sections, tool list changes, new/removed AskUserQuestion blocks | Re-run conversion logic |
| **Content** | Prompt text modifications, instruction wording, reference path changes, code/table content | Targeted text transformation |
| **Cosmetic** | Whitespace, formatting, comment text, markdown styling changes | Auto-apply without prompting |

Build `SOURCE_CHANGES` list. Each entry: `file_path`, `change_type` (modified/added/deleted/renamed), `classification` (structural/content/cosmetic), `diff_summary`, `diff_lines_added`, `diff_lines_removed`, `affected_sections`, and `component_entry` (matching PORT-METADATA component, or `null` for new files).

New files get `classification: "structural"` and `diff_summary: "New component -- requires full port"`. Deleted files get `classification: "structural"` and `diff_summary: "Source component deleted -- ported version may be orphaned"`.

### Track B: Platform Changes

Skip this track if `SOURCE_ONLY` is `true`.

#### Step B1: Load Validate-Adapter Skill

Read the validate-adapter skill to access its platform validation logic:

```
Read: ${CLAUDE_PLUGIN_ROOT}/skills/validate-adapter/SKILL.md
```

#### Step B2: Run Platform Validation

1. Load the adapter file: `Read: ${CLAUDE_PLUGIN_ROOT}/references/adapters/{TARGET_PLATFORM}.md`

2. Spawn the researcher agent:
   ```yaml
   Task:
     description: "Research current state of {TARGET_PLATFORM}'s plugin system. Compare against adapter. Focus on changes since v{PORT_METADATA.target_platform_version}."
     subagent_type: "agent-alchemy-plugin-tools:researcher"
     input: |
       Target platform: {TARGET_PLATFORM}
       Existing adapter file: ${CLAUDE_PLUGIN_ROOT}/references/adapters/{TARGET_PLATFORM}.md
       Last known platform version: {PORT_METADATA.target_platform_version}
   ```

3. Collect the researcher's platform profile and adapter comparison results.

#### Step B3: Extract Platform Findings

From the researcher's adapter comparison results, extract three categories:

Categorize findings into three types:

| Type | Fields | Default Impact |
|------|--------|----------------|
| **stale** | `adapter_section`, `old_mapping`, `new_mapping`, `affected_components` | breaking or cosmetic |
| **missing** | `adapter_section`, `feature_description`, `potential_benefit` | additive |
| **removed** | `adapter_section`, `feature_description`, `alternative`, `affected_components` | breaking |

#### Step B4: Classify Platform Impact

Classify each finding by cross-referencing against `PORT_METADATA.components`:
- **Breaking**: Stale/removed mapping used by at least one ported component
- **Additive**: New feature that could improve ported components but is not required
- **Cosmetic**: Naming change or minor adjustment with no functional impact

Build `PLATFORM_CHANGES` list from the classified findings.

### Combined Change Summary

After both tracks complete, present the combined results via `AskUserQuestion`:

```yaml
AskUserQuestion:
  questions:
    - header: "Change Detection Summary"
      question: |
        Changes detected since the last port ({PORT_METADATA.port_date}):

        Source changes:
        - {count} files modified ({structural_count} structural, {content_count} content, {cosmetic_count} cosmetic)
        - {added_count} new files detected
        - {deleted_count} files deleted

        Platform changes ({TARGET_PLATFORM}):
        - {stale_count} stale mappings ({breaking_stale_count} breaking)
        - {missing_count} new platform features
        - {removed_count} removed features ({breaking_removed_count} breaking)

        Estimated update scope: {small/medium/large}

        How would you like to proceed?
      options:
        - label: "Apply all changes"
          description: "Process both source and platform changes"
        - label: "Source changes only"
          description: "Apply only source file updates, skip platform changes"
        - label: "Platform changes only"
          description: "Apply only platform-related updates, skip source changes"
        - label: "Select specific changes"
          description: "Choose individual changes to apply"
        - label: "Cancel"
          description: "Exit without making changes"
      multiSelect: false
```

**Scope estimation:**
- **Small**: 0-3 total changes, all cosmetic or content
- **Medium**: 4-10 total changes, or any structural source changes, or any additive platform changes
- **Large**: 10+ total changes, or any breaking platform changes, or any new/deleted source files

If user selects "Select specific changes", present a detailed checklist:

```yaml
AskUserQuestion:
  questions:
    - header: "Select Changes to Apply"
      question: "Select which changes to apply:"
      options:
        - label: "[source] {file_name} ({classification})"
          description: "{diff_summary}"
        - label: "[platform] {finding_type}: {description}"
          description: "Impact: {impact} -- affects {affected_count} component(s)"
      multiSelect: true
```

Store the user's selection as `SELECTED_CHANGES` with two sub-lists: `selected_source_changes` and `selected_platform_changes`.

If user selects "Cancel", exit gracefully.

---

## Phase 3: Apply Source Changes

**Goal:** Incrementally update ported files to reflect source plugin modifications.

Skip this phase entirely if:
- User selected "Platform changes only" in Phase 2
- User selected "Cancel" in Phase 2
- `SOURCE_CHANGES` is empty (no source changes detected)

Initialize tracking:
```
UPDATED_FILES = []      // files modified during this phase
SKIPPED_FILES = []      // files user chose to skip
NEW_COMPONENTS = []     // new source files that need full porting
DELETED_COMPONENTS = [] // source files deleted, ported versions potentially orphaned
```

### Step 1: Apply Cosmetic Changes

Process all cosmetic changes first (these do not require user approval):

For each entry in `SOURCE_CHANGES` where `classification == "cosmetic"`:
1. Read the current ported target file: `Read: {PORT_OUTPUT_DIR}/{component_entry.target}`
2. Apply whitespace and formatting changes to match the updated source
3. Write the updated file using `Edit` tool
4. Add to `UPDATED_FILES` with `update_type: "cosmetic"`

Log: `Applied {count} cosmetic updates automatically.`

### Step 2: Process Modified Components (Structural and Content)

For each entry in `SOURCE_CHANGES` where `change_type == "modified"` and `classification` is `"structural"` or `"content"`:

#### 2a: Load Conversion Context

1. Read the current source file:
   ```
   Read: {source_change.file_path}
   ```

2. Read the current ported target file:
   ```
   Read: {PORT_OUTPUT_DIR}/{source_change.component_entry.target}
   ```

3. Load the appropriate converter reference from `${CLAUDE_PLUGIN_ROOT}/references/`:

   | Source path contains | Load converter |
   |---------------------|---------------|
   | `/agents/` | `agent-converter.md` |
   | `/hooks/` | `hook-converter.md` |
   | `/references/` | `reference-converter.md` |
   | `.mcp.json` | `mcp-converter.md` |
   | Skills (default) | `adapters/{TARGET_PLATFORM}.md` |

4. Also load the adapter file (`adapters/{TARGET_PLATFORM}.md`) if not already loaded.

#### 2b: Apply Structural Changes

For structural changes, re-run conversion on the changed sections:

1. Identify changed sections by comparing the diff against the file structure
2. For each changed section: extract updated content, apply converter mapping rules, replace the corresponding section in the ported target
3. For frontmatter changes: parse updated frontmatter, apply adapter mappings, merge with existing ported frontmatter (preserve target-specific fields, update source-derived fields)
4. For `allowed-tools` / `tools` changes: map new tools through adapter equivalents, remove dropped tools, flag tools with no target equivalent

#### 2c: Apply Content Changes

For content changes, apply targeted text transformations:

1. Identify specific text changes from the diff and locate them in the ported target
2. Apply converter mapping rules to transform the new text
3. Replace the old text, preserving any target-platform-specific modifications from the original port

#### 2d: Check for New Incompatibilities

Load the incompatibility resolver:
```
Read: ${CLAUDE_PLUGIN_ROOT}/references/incompatibility-resolver.md
```

Check if any of the changes introduce new incompatibilities with the target platform:
- New tool references that have no target equivalent
- New composition patterns not supported by the target
- New agent configurations with no mapping

For each new incompatibility found, present it to the user:

```yaml
AskUserQuestion:
  questions:
    - header: "New Incompatibility Detected"
      question: |
        The source change in {file_path} introduces a new incompatibility:

        Feature: {feature_description}
        Issue: {incompatibility_description}
        Severity: {critical/functional/cosmetic}

        How should this be handled?
      options:
        - label: "Apply workaround"
          description: "{workaround_description}"
        - label: "Add TODO placeholder"
          description: "Insert a TODO comment for manual resolution"
        - label: "Skip this change"
          description: "Do not apply this specific change"
      multiSelect: false
```

#### 2e: Confirm and Apply

For each significant change (structural or content with incompatibilities), present a before/after preview:

```yaml
AskUserQuestion:
  questions:
    - header: "Confirm Update: {file_name}"
      question: |
        Source change: {diff_summary}
        Affected section: {section_name}

        The ported file will be updated with the converted changes.
        Apply this update?
      options:
        - label: "Apply"
          description: "Update the ported file"
        - label: "Skip"
          description: "Leave the ported file unchanged for this change"
        - label: "Show diff"
          description: "View the detailed before/after comparison"
      multiSelect: false
```

If "Show diff", display before/after and re-ask. If "Apply", write with `Edit` and add to `UPDATED_FILES`. If "Skip", add to `SKIPPED_FILES`.

### Step 3: Handle New Components

For each entry in `SOURCE_CHANGES` where `change_type == "added"`:

```yaml
AskUserQuestion:
  questions:
    - header: "New Source Component"
      question: |
        A new component was detected: {file_path}

        This file was added since the last port and requires a full conversion.
        The update skill handles incremental changes; full conversions are best
        handled by the port-plugin skill.
      options:
        - label: "Run /port-plugin for this component"
          description: "Recommended: use the full porting workflow for new components"
        - label: "Add to gap report"
          description: "Note this as an unported component in the gap report"
        - label: "Skip"
          description: "Ignore this new component"
      multiSelect: false
```

If "Run /port-plugin": add to `NEW_COMPONENTS` with `action: "port"` and inform user to run it after this update. If "Add to gap report": add with `action: "gap"`.

### Step 4: Handle Deleted Components

For each entry in `SOURCE_CHANGES` where `change_type == "deleted"`:

```yaml
AskUserQuestion:
  questions:
    - header: "Deleted Source Component"
      question: |
        Source component was deleted: {file_path}
        Ported version exists at: {PORT_OUTPUT_DIR}/{target_path}

        The source file no longer exists. What should we do with the ported version?
      options:
        - label: "Delete ported file"
          description: "Remove the ported version since its source no longer exists"
        - label: "Keep as orphaned"
          description: "Keep the ported file but mark it as orphaned in the migration guide"
        - label: "Skip"
          description: "Take no action"
      multiSelect: false
```

If "Delete": remove via `Bash` (`rm {PORT_OUTPUT_DIR}/{target_path}`) and add to `DELETED_COMPONENTS`. If "Keep as orphaned": prepend `<!-- ORPHANED: Source file {source_path} was deleted on {date} -->` and add to `DELETED_COMPONENTS`.

---

## Phase 4: Apply Platform Changes

**Goal:** Update ported files to reflect changes in the target platform since the original port.

Skip this phase entirely if:
- User selected "Source changes only" in Phase 2
- User selected "Cancel" in Phase 2
- `PLATFORM_CHANGES` is empty (no platform changes detected)

### Step 1: Apply Breaking Changes

Process breaking changes first as they affect correctness.

#### 1a: Stale Mappings

For each stale breaking change: identify affected ported files, locate stale mapping instances, and prepare replacements. Present each:

```yaml
AskUserQuestion:
  questions:
    - header: "Stale Platform Mapping"
      question: |
        Platform mapping has changed for {TARGET_PLATFORM}:

        Section: {adapter_section}
        Old: {old_mapping}
        New: {new_mapping}

        Affected files ({affected_count}):
        {list of affected ported files}

        Apply the updated mapping?
      options:
        - label: "Apply to all affected files"
          description: "Update all {affected_count} file(s) with the new mapping"
        - label: "Apply selectively"
          description: "Choose which files to update"
        - label: "Skip"
          description: "Keep the current mapping (may cause issues on the platform)"
      multiSelect: false
```

If "Apply selectively", present each file individually. Apply updates via `Edit` and add to `UPDATED_FILES` with `update_type: "platform_stale"`.

#### 1b: Removed Features

For each removed breaking feature, identify affected files and present:

```yaml
AskUserQuestion:
  questions:
    - header: "Removed Platform Feature"
      question: |
        {TARGET_PLATFORM} has removed or deprecated a feature used by ported components:

        Feature: {feature_description}
        {If alternative:}Alternative: {alternative}
        {If no alternative:}No direct alternative available.

        Affected files ({affected_count}):
        {list of affected ported files}

        How should this be handled?
      options:
        - label: "Apply alternative"
          description: "Replace with: {alternative}"
        - label: "Add TODO placeholder"
          description: "Insert a TODO comment for manual resolution"
        - label: "Remove feature usage"
          description: "Remove references to this feature from ported files"
        - label: "Keep as-is with warning"
          description: "Leave unchanged but add a deprecation warning comment"
      multiSelect: false
```

Apply the selected resolution to each affected file and add to `UPDATED_FILES` with `update_type: "platform_removed"`.

### Step 2: Apply Additive Changes

Present new platform features that could enhance ported components:

```yaml
AskUserQuestion:
  questions:
    - header: "New Platform Features"
      question: |
        {TARGET_PLATFORM} has added new features since the last port.
        Select which ones to apply to your ported components:
      options:
        - label: "{feature_description}"
          description: "Benefit: {potential_benefit} -- affects {affected_count} component(s)"
      multiSelect: true
```

For each selected feature: identify benefiting files, apply using adapter mapping rules, add to `UPDATED_FILES` with `update_type: "platform_additive"`. If none selected, log: `No additive platform changes applied.`

### Step 3: Update Adapter File

After applying platform changes, offer to update the adapter file:

```yaml
AskUserQuestion:
  questions:
    - header: "Update Adapter File"
      question: |
        The adapter file for {TARGET_PLATFORM} may be stale based on the platform changes detected.
        Would you like to update it?
      options:
        - label: "Update adapter"
          description: "Apply validated platform changes to the adapter file"
        - label: "Skip adapter update"
          description: "Leave the adapter file unchanged (note: it may be stale)"
      multiSelect: false
```

If "Update adapter": load validate-adapter (`Read: ${CLAUDE_PLUGIN_ROOT}/skills/validate-adapter/SKILL.md`), execute its update logic, and track the new version. If "Skip": log that adapter is stale and set `ADAPTER_UPDATED = false`.

---

## Phase 5: Output & Refresh

**Goal:** Write all updated files, refresh the PORT-METADATA block, update the migration guide history, refresh the gap report, and present a final summary.

### Step 1: Write Updated Files

For each file in `UPDATED_FILES`: if `OUTPUT_DIR` is specified, write to `{OUTPUT_DIR}/{relative_target_path}` (creating intermediate directories as needed); otherwise write in-place. Track results in `WRITE_RESULTS` (`files_written` and `files_failed` lists). If any writes fail, log the error and continue.

### Step 2: Refresh PORT-METADATA

Get the current HEAD commit hash:
```bash
git rev-parse HEAD
```

Get today's date for the port_date field.

Build the updated PORT-METADATA block:

```markdown
<!-- PORT-METADATA
source_commit: {current_HEAD_hash}
port_date: {today_date}
adapter_version: {new_adapter_version or PORT_METADATA.adapter_version if not updated}
target_platform: {PORT_METADATA.target_platform}
target_platform_version: {new_platform_version or PORT_METADATA.target_platform_version}
components:
{For each component in PORT_METADATA.components that was NOT deleted:}
  - source: {component.source}
    target: {component.target}
    fidelity: {updated_fidelity_score or original if unchanged}
{For any NEW components that were fully ported:}
  - source: {new_source_path}
    target: {new_target_path}
    fidelity: {new_fidelity_score}
PORT-METADATA -->
```

**Fidelity score rules:** Cosmetic/content changes keep original score. Structural changes and platform breaking changes trigger recalculation. Orphaned components are removed from the list.

Replace the old PORT-METADATA block in MIGRATION-GUIDE.md with the updated block using `Edit` tool.

### Step 3: Append Update History

Add an update history entry to MIGRATION-GUIDE.md. If an `## Update History` section already exists, append to it. If not, create it before the PORT-METADATA block.

```markdown
## Update History

### {today_date} -- Incremental Update
- **Source changes**: {modified_count} files updated, {added_count} new, {deleted_count} deleted
- **Platform changes**: {stale_updated_count} mappings updated, {additive_applied_count} features added, {removed_handled_count} removals handled
- **Scope**: {source-only|platform-only|full}
- **Skipped**: {skipped_count} changes skipped by user
- **Components affected**: {affected_component_count}/{total_component_count}
```

If the Update History section already has entries, append the new entry at the top (most recent first).

### Step 4: Refresh GAP-REPORT.md

Check if a GAP-REPORT.md exists in `PORT_OUTPUT_DIR`:

```
Glob: {PORT_OUTPUT_DIR}/GAP-REPORT.md
```

**If exists:** Read it, remove entries that were resolved by this update (mark as `RESOLVED` with date), add new entries for any new gaps (incompatibilities, removed features, skipped breaking changes), and write the updated file.

**If does not exist:** Create a new GAP-REPORT.md (following port-plugin format) only if there are new gaps. If no new gaps, do not create one.

### Step 5: Final Summary

Present the update results via `AskUserQuestion`:

```yaml
AskUserQuestion:
  questions:
    - header: "Update Complete"
      question: |
        Update summary for {TARGET_PLATFORM} port:

        Files updated: {WRITE_RESULTS.files_written.length}
        {For each file: - {path} ({update_type})}

        New gaps introduced: {new_gap_count}
        Gaps resolved: {resolved_gap_count}
        Metadata refreshed: yes
        Adapter updated: {yes/no}

        Components:
        - Updated: {updated_count}
        - Skipped: {skipped_count}
        - New (needs full port): {new_component_count}
        - Deleted/orphaned: {deleted_count}

        Next steps:
        {If NEW_COMPONENTS with action "port":}
        1. Run /port-plugin --target {TARGET_PLATFORM} for {new_count} new component(s)
        {If SKIPPED_FILES.length > 0:}
        2. Review {skipped_count} skipped change(s) for manual handling
        {If ADAPTER_UPDATED == false and PLATFORM_CHANGES.length > 0:}
        3. Consider updating the adapter file with /validate-adapter --target {TARGET_PLATFORM}
        4. Test updated plugins on {TARGET_PLATFORM}
        5. Review MIGRATION-GUIDE.md for full update history
      options:
        - label: "Done"
          description: "Finish the update workflow"
        - label: "View updated files"
          description: "List all files that were modified"
        - label: "Run another update"
          description: "Check for additional changes"
      multiSelect: false
```

If "View updated files": list all written files with paths and update types, then re-present options. If "Run another update": return to Phase 1 Step 3 (re-locate migration guide with refreshed metadata).

---

## Error Handling

If any phase fails:
1. Explain what went wrong
2. Use `AskUserQuestion` to ask how to proceed:
   ```yaml
   AskUserQuestion:
     questions:
       - header: "Error Recovery"
         question: "{Description of what failed}. How would you like to proceed?"
         options:
           - label: "Retry this phase"
             description: "Attempt the failed phase again"
           - label: "Skip to next phase"
             description: "Continue without this phase's output"
           - label: "Cancel"
             description: "Exit the update workflow"
         multiSelect: false
   ```

### Specific Error Scenarios

**Git history unavailable**: If `git` commands fail (not a git repo, corrupted history):
- Log: `WARNING: Git history is unavailable. Source change detection requires git history.`
- If `SOURCE_ONLY` or full update: cannot detect source changes, offer to proceed with platform changes only or cancel
- If `PLATFORM_ONLY`: git is not needed, continue normally

**Adapter file missing**: If the adapter file for `TARGET_PLATFORM` does not exist:
- Log: `WARNING: No adapter file found for {TARGET_PLATFORM}. Platform change detection is limited.`
- Source changes can still be applied using generic conversion logic
- Platform changes cannot be fully evaluated without an adapter

**Ported file write conflict**: If a target file has been manually edited since the last port (detected by comparing file modification time against `PORT_METADATA.port_date`):
- Warn the user that the file appears to have manual edits
- Offer: "Overwrite", "Merge manually", or "Skip"

---

## Reference Files

- `references/adapter-format.md` -- Adapter file format specification (9 mapping sections)
- `references/agent-converter.md` -- Agent conversion logic (frontmatter mapping, body transformation, gap handling, fidelity scoring)
- `references/hook-converter.md` -- Hook conversion logic (event mapping, behavioral classification, workaround strategies)
- `references/reference-converter.md` -- Reference file conversion logic (discovery, path transformation, flattening)
- `references/mcp-converter.md` -- MCP config conversion logic (server mapping, transport types, tool reference renaming, platform support detection)
- `references/incompatibility-resolver.md` -- Incompatibility detection, interactive resolution, batch handling, decision tracking
- `references/adapters/` -- Directory for per-platform adapter files (one markdown file per target platform)
