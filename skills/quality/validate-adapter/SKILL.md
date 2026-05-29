---
name: validate-adapter
description: Validates adapter files against live platform documentation to detect stale mappings,missing features, and outdated version information
user-invocable: true
disable-model-invocation: true
argument-hint: "--target <platform> [--update]"
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

# Validate Adapter

Validate an adapter file against live platform documentation to detect stale mappings, missing features, and outdated version information. Optionally apply updates in-place when the `--update` flag is provided.

**CRITICAL: Complete ALL 4 phases.** The workflow is not complete until Phase 4: Report & Apply is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Summary and confirmation -> AskUserQuestion
- Report presentation -> AskUserQuestion
- Action selection -> AskUserQuestion
- Removal decisions -> AskUserQuestion

Text output should only be used for:
- Displaying progress updates between phases
- Presenting intermediate analysis results
- Explaining context or classification reasoning

If you need the user to make a choice or provide input, use AskUserQuestion.

**NEVER do this** (asking via text output):
```
Would you like to apply updates or export the report?
1. Apply updates
2. Export report
3. View details
```

**ALWAYS do this** (using AskUserQuestion tool):
```yaml
AskUserQuestion:
  questions:
    - header: "Validation Complete"
      question: "How would you like to proceed?"
      options:
        - label: "View detailed findings"
          description: "Show full per-entry breakdown grouped by classification"
        - label: "Apply updates"
          description: "Update stale/missing entries in the adapter file"
        - label: "Export report"
          description: "Write validation report as a markdown file"
      multiSelect: false
```

### Composability

This skill can be invoked standalone via `/validate-adapter` or loaded as a sub-workflow by other skills (e.g., `update-ported-plugin`). When loaded as a sub-workflow:

- The caller may only need Phases 1-3 (the analysis) and not Phase 4 (the interactive report)
- If the caller has already set `SKIP_REPORT = true` in context, stop after Phase 3 and return the validation report data structure to the caller
- If no `SKIP_REPORT` flag is present, execute all 4 phases (standalone behavior)

### Plan Mode Behavior

**CRITICAL**: This skill performs an interactive validation workflow, NOT an implementation plan. When invoked during Claude Code's plan mode:

- **DO NOT** create an implementation plan for how to build the validation feature
- **DO NOT** defer validation to an "execution phase"
- **DO** proceed with the full validation workflow immediately
- **DO** write updated adapter files or reports as normal

## Phase Overview

Execute these phases in order, completing ALL of them:

1. **Load & Parse** - Parse arguments, read adapter format spec and adapter file
2. **Platform Research** - Spawn researcher agent to investigate current platform state
3. **Compare & Analyze** - Compare adapter sections against research findings
4. **Report & Apply** - Present findings and optionally update the adapter

---

## Phase 1: Load & Parse

**Goal:** Parse arguments, load the adapter format specification, read the target adapter file, and extract its current state.

### Step 1: Parse Arguments

Parse `$ARGUMENTS` for:
- `--target <platform>` -- Target platform slug (default: `opencode`)
- `--update` -- Enable in-place update mode (default: `false`)

Set `TARGET_PLATFORM` from `--target` value (default: `opencode`).
Set `UPDATE_MODE` from `--update` flag (default: `false`).

### Step 2: Load Adapter Format Specification

Read the adapter format reference to understand the expected 9-section structure:
```
Read: ${CLAUDE_PLUGIN_ROOT}/references/adapter-format.md
```

Record the 9 required/optional sections:
1. Platform Metadata
2. Directory Structure
3. Tool Name Mappings
4. Model Tier Mappings
5. Frontmatter Translations
6. Hook/Lifecycle Event Mappings
7. Composition Mechanism
8. Path Resolution
9. Adapter Version

### Step 3: Load Adapter File

Read the adapter file for the target platform:
```
Read: ${CLAUDE_PLUGIN_ROOT}/references/adapters/${TARGET_PLATFORM}.md
```

**Error handling -- adapter not found:**

If the adapter file does not exist:
1. Use Glob to list available adapters:
   ```
   Glob: ${CLAUDE_PLUGIN_ROOT}/references/adapters/*.md
   ```
2. Present available options:
   ```yaml
   AskUserQuestion:
     questions:
       - header: "Adapter Not Found"
         question: "No adapter found for '${TARGET_PLATFORM}'. Which adapter would you like to validate?"
         options:
           - label: "{adapter-1}"
             description: "Adapter file: {adapter-1}.md"
           - label: "{adapter-2}"
             description: "Adapter file: {adapter-2}.md"
         multiSelect: false
   ```
3. If no adapters exist at all, inform the user and exit:
   ```
   ERROR: No adapter files found in ${CLAUDE_PLUGIN_ROOT}/references/adapters/.
   Create an adapter first using /port-plugin or manually following the adapter format spec.
   ```

### Step 4: Parse Adapter Sections

Parse all 9 sections from the adapter file by matching H2 (`##`) headers against the section names defined in the adapter format specification.

For each section found:
- Record section name, start line, end line, and raw content
- Count the number of table rows / list entries / code block entries (these are the "entries" for classification)

For each expected section NOT found:
- Record it as missing from the adapter

### Step 5: Extract Metadata

From the **Adapter Version** section (Section 9), extract:
- `adapter_version` -- semver version of this adapter file
- `target_platform_version` -- version of the platform the adapter was written for
- `last_updated` -- ISO 8601 date of last review/update

If any of these fields are missing, record them as `unknown`.

### Step 6: Present Summary and Confirm

```yaml
AskUserQuestion:
  questions:
    - header: "Adapter Validation Summary"
      question: |
        Adapter loaded for validation:

        | Field | Value |
        |-------|-------|
        | Platform | ${TARGET_PLATFORM} |
        | Adapter Version | ${adapter_version} |
        | Target Platform Version | ${target_platform_version} |
        | Last Updated | ${last_updated} |
        | Sections Found | ${found_count} / 9 |
        | Update Mode | ${UPDATE_MODE ? 'Enabled' : 'Disabled'} |

        Proceed with platform research?
      options:
        - label: "Proceed"
          description: "Spawn researcher agent to investigate current platform state"
        - label: "Cancel"
          description: "Cancel validation"
      multiSelect: false
```

If the user selects "Cancel", exit the workflow.

---

## Phase 2: Platform Research

**Goal:** Spawn the researcher agent to gather current platform documentation and compare against the adapter.

### Step 1: Spawn Researcher Agent

Spawn the researcher agent using the Task tool with `subagent_type: "agent-alchemy-plugin-tools:researcher"`:

```
Task tool prompt:
"Research the current state of the plugin/extension system for: ${TARGET_PLATFORM}

You are validating an existing adapter file for this platform. The adapter was last updated on ${last_updated} and targets platform version ${target_platform_version}.

Focus your research on:
1. The current version of ${TARGET_PLATFORM} and any version changes since ${target_platform_version}
2. Plugin system changes, new features, or API modifications since the adapter was written
3. Deprecated or removed features that the adapter may still reference
4. New capabilities or configuration options not present in the adapter

The adapter file is located at: ${CLAUDE_PLUGIN_ROOT}/references/adapters/${TARGET_PLATFORM}.md

Read the adapter file and perform your Phase 4: Adapter Comparison against your research findings. Pay special attention to:
- Tool name changes or new tools added to the platform
- Directory structure changes
- Configuration format changes
- Model/provider changes
- Hook/lifecycle system changes
- Composition mechanism changes

Return a structured platform profile with your Adapter Comparison section fully populated."
```

**Retry logic:** If the Task tool call fails (agent error, timeout, or empty response), retry once automatically. If the retry also fails, proceed to research failure handling in Step 3.

### Step 2: Process Research Findings

When the researcher agent returns its platform profile:

1. Store the full response as `RESEARCH_FINDINGS`
2. Extract key data points:
   - `research_platform_version` -- current platform version found by research
   - `documentation_quality` -- excellent/good/fair/poor/none
   - `overall_confidence` -- high/medium/low
   - `sources_consulted` -- count and list of sources
   - `stale_mappings` -- list from the Adapter Comparison section
   - `missing_mappings` -- list from the Adapter Comparison section
3. Display brief research summary as a progress update (text output, not AskUserQuestion):
   ```
   Research complete:
   - Documentation quality: ${documentation_quality}
   - Overall confidence: ${overall_confidence}
   - Sources consulted: ${sources_count} (${official_count} official, ${community_count} community)
   - Platform version found: ${research_platform_version} (adapter targets: ${target_platform_version})
   ```

### Step 3: Handle Research Failure

If the researcher agent fails or returns empty results:

1. Inform the user of the failure
2. Offer options:
   ```yaml
   AskUserQuestion:
     questions:
       - header: "Research Failed"
         question: "The researcher agent could not gather platform documentation. How would you like to proceed?"
         options:
           - label: "Retry research"
             description: "Spawn the researcher agent again"
           - label: "Manual validation"
             description: "Skip research; validate adapter structure only (no staleness detection)"
           - label: "Cancel"
             description: "Cancel the validation workflow"
         multiSelect: false
   ```
3. If "Retry research": go back to Step 1
4. If "Manual validation": proceed to Phase 3 with empty research findings (all entries will be classified as "Uncertain")
5. If "Cancel": exit the workflow

---

## Phase 3: Compare & Analyze

**Goal:** Compare each adapter section against research findings and classify every entry.

### Step 1: Section-by-Section Comparison

For each of the 9 adapter sections, compare the adapter content against the research findings.

**Special handling for low-confidence research:** If the researcher reported `overall_confidence: low` for an entire topic area, or if the Adapter Comparison section has no data for a given adapter section, mark the entire section as **Uncertain** rather than making unreliable per-entry classifications.

### Step 2: Classify Entries

For each mapping/entry in each adapter section, classify it as one of:

| Classification | Meaning | Criteria |
|---------------|---------|----------|
| **Current** | Matches research findings | Adapter value aligns with what research found; no changes needed |
| **Stale** | Outdated information | Research has newer/different data for this entry; adapter needs updating |
| **Missing** | Not in adapter | Platform has features/capabilities that the adapter does not cover |
| **Removed** | No longer supported | Adapter references features the platform has deprecated or removed |
| **Uncertain** | Cannot determine | Research confidence is low; unable to reliably classify this entry |

Classification rules by section:

**Platform Metadata:**
- Compare `documentation_url`, `repository_url`, `plugin_docs_url` against research-discovered URLs
- Check if `notes` still accurately describe the platform status
- Flag URL changes as Stale; flag removed URLs as Removed

**Directory Structure:**
- Compare `plugin_root`, `skill_dir`, `agent_dir`, etc. against research-discovered paths
- Flag changed paths as Stale; flag new directories as Missing

**Tool Name Mappings:**
- Compare each tool mapping against research tool equivalents
- Flag renamed tools as Stale; flag new platform tools as Missing; flag removed tools as Removed

**Model Tier Mappings:**
- Compare model identifiers against research-discovered models
- Flag renamed or updated model identifiers as Stale; flag new tiers as Missing

**Frontmatter Translations:**
- Compare field mappings against research-discovered config format
- Flag changed field names as Stale; flag new fields as Missing

**Hook/Lifecycle Event Mappings:**
- Compare event mappings against research-discovered lifecycle events
- Flag new events as Missing; flag removed events as Removed

**Composition Mechanism:**
- Compare mechanism, syntax, and capabilities against research findings
- Flag changed behavior as Stale

**Path Resolution:**
- Compare resolution strategy and patterns against research findings
- Flag changed patterns as Stale

**Adapter Version:**
- Compare `target_platform_version` against `research_platform_version`
- If versions differ, classify as Stale
- Check `last_updated` age -- if older than 6 months, add a note

### Step 3: Build Validation Report

Construct the validation report with the following structure:

**Per-section breakdown:**
```
| Section | Total Entries | Current | Stale | Missing | Removed | Uncertain |
|---------|--------------|---------|-------|---------|---------|-----------|
| Platform Metadata | N | N | N | N | N | N |
| Directory Structure | N | N | N | N | N | N |
| Tool Name Mappings | N | N | N | N | N | N |
| ... | ... | ... | ... | ... | ... | ... |
| **Totals** | **N** | **N** | **N** | **N** | **N** | **N** |
```

**Overall health score:**
```
Health Score = (Current entries / Total classified entries) * 100
```

Exclude Uncertain entries from the denominator (they neither help nor hurt the score). If all entries are Uncertain, report the health score as "N/A -- insufficient research data".

**Stale entries detail list:**
```
| Section | Entry | Current Value | Suggested Value | Source |
|---------|-------|--------------|-----------------|--------|
| {section} | {entry name} | {adapter value} | {research value} | {source URL or description} |
```

**Missing entries detail list:**
```
| Section | Feature | Description | Suggested Mapping |
|---------|---------|-------------|-------------------|
| {section} | {feature name} | {research description} | {suggested adapter value} |
```

**Removed entries detail list:**
```
| Section | Entry | Adapter Value | Evidence |
|---------|-------|--------------|----------|
| {section} | {entry name} | {current adapter value} | {evidence of removal from research} |
```

Store the complete report as `VALIDATION_REPORT`.

If `SKIP_REPORT = true` (sub-workflow mode), return `VALIDATION_REPORT` to the caller and stop here. Do not proceed to Phase 4.

---

## Phase 4: Report & Apply

**Goal:** Present the validation report to the user and optionally apply updates.

### Step 1: Present Validation Report

Determine the health indicator based on the health score:
- 90-100%: "Healthy"
- 70-89%: "Needs Attention"
- 50-69%: "Outdated"
- 0-49%: "Critically Outdated"
- N/A: "Insufficient Data"

Build the action options based on context:
- Always include "View detailed findings" and "Export report"
- Include "Apply updates" only if `UPDATE_MODE = true` AND there are stale/missing/removed entries
- If `UPDATE_MODE = false` and there are findings, include a note that `--update` flag enables in-place updates

```yaml
AskUserQuestion:
  questions:
    - header: "Adapter Validation Report"
      question: |
        ## ${TARGET_PLATFORM} Adapter -- ${health_indicator}

        **Health Score: ${health_score}%**

        | Metric | Count |
        |--------|-------|
        | Current | ${current_count} |
        | Stale | ${stale_count} |
        | Missing | ${missing_count} |
        | Removed | ${removed_count} |
        | Uncertain | ${uncertain_count} |

        ${stale_count + missing_count + removed_count > 0 ?
          stale_count + " stale, " + missing_count + " missing, and " + removed_count + " removed entries found." :
          "All entries are current. No updates needed."}

        How would you like to proceed?
      options:
        - label: "View detailed findings"
          description: "Show full per-entry breakdown grouped by classification"
        - label: "Apply updates"
          description: "Update the adapter file with research-backed corrections (requires --update flag)"
        - label: "Export report"
          description: "Write validation report to a markdown file"
      multiSelect: false
```

### Step 2: View Detailed Findings

If the user selects "View detailed findings":

1. Present the full per-entry breakdown grouped by classification:

   **Stale Entries** (if any):
   Show the stale entries detail list with current value, suggested value, and source.

   **Missing Entries** (if any):
   Show the missing entries detail list with feature name, description, and suggested mapping.

   **Removed Entries** (if any):
   Show the removed entries detail list with entry name, current value, and evidence.

   **Uncertain Entries** (if any):
   Show uncertain entries with a note explaining the low research confidence.

   **Current Entries** (if any):
   Show a summary count per section (do not list every current entry individually).

2. After presenting details, re-present the action choice:
   ```yaml
   AskUserQuestion:
     questions:
       - header: "Next Steps"
         question: "What would you like to do with these findings?"
         options:
           - label: "Apply updates"
             description: "Update the adapter file with research-backed corrections"
           - label: "Export report"
             description: "Write validation report to a markdown file"
           - label: "Done"
             description: "Exit without taking action"
         multiSelect: false
   ```

### Step 3: Apply Updates

If the user selects "Apply updates":

**Guard check:** If `UPDATE_MODE = false`, inform the user:
```
Update mode is not enabled. Re-run with the --update flag to apply changes:
  /validate-adapter --target ${TARGET_PLATFORM} --update
```
Then return to the action choice prompt.

If `UPDATE_MODE = true`, proceed with updates:

1. **Update stale entries:**
   For each stale entry in the validation report:
   - Read the current adapter file section containing the entry
   - Use Edit to replace the old value with the research-suggested value
   - Record the change: `{ section, entry, old_value, new_value }`

2. **Add missing entries:**
   For each missing entry in the validation report:
   - Determine the correct adapter section for the new entry
   - Use Edit to add the new entry in the appropriate location within the section
   - Follow the formatting conventions of the existing entries in that section
   - Record the addition: `{ section, entry, new_value }`

3. **Handle removed entries:**
   For each removed entry, ask the user individually:
   ```yaml
   AskUserQuestion:
     questions:
       - header: "Removed Feature: ${entry_name}"
         question: |
           The adapter references "${entry_name}" in the ${section} section,
           but research indicates this feature has been removed from ${TARGET_PLATFORM}.

           Evidence: ${evidence}

           What should be done with this entry?
         options:
           - label: "Remove entry"
             description: "Delete this entry from the adapter"
           - label: "Keep with deprecation note"
             description: "Keep the entry but add a deprecation note"
         multiSelect: false
   ```
   - If "Remove entry": use Edit to remove the entry from the adapter
   - If "Keep with deprecation note": use Edit to append `[DEPRECATED]` to the entry's notes column

4. **Update metadata:**
   In the Adapter Version section:
   - Bump `adapter_version` patch number (e.g., `1.0.0` -> `1.0.1`)
   - Update `last_updated` to today's date (ISO 8601 format)
   - Update `target_platform_version` to `research_platform_version` if it changed
   - Append to the `changelog` field:
     ```
     ${new_version} (${today}): Validation-driven update — ${stale_count} stale entries updated, ${missing_count} missing entries added, ${removed_count} removed entries handled.
     ```

5. **Write updated adapter file:**
   ```
   Write: ${CLAUDE_PLUGIN_ROOT}/references/adapters/${TARGET_PLATFORM}.md
   ```

6. **Display update summary:**
   ```
   Adapter updated successfully:
   - Stale entries updated: ${updated_stale_count}
   - Missing entries added: ${added_missing_count}
   - Removed entries handled: ${handled_removed_count}
   - New adapter version: ${new_version}
   - Target platform version: ${research_platform_version}
   ```

### Step 4: Export Report

If the user selects "Export report":

1. Determine the output directory:
   - If an `OUTPUT_DIR` was provided by a caller (sub-workflow mode), use it
   - Otherwise default to the project root

2. Write the validation report as markdown:
   ```
   Write: ${OUTPUT_DIR}/adapter-validation-${TARGET_PLATFORM}.md
   ```

   The report file should include:
   - Report header with platform name, date, and health score
   - Per-section breakdown table
   - Stale entries detail list
   - Missing entries detail list
   - Removed entries detail list
   - Uncertain entries list with confidence notes
   - Research sources consulted
   - Recommendation (update adapter / adapter is current / insufficient data)

3. Inform the user of the export location:
   ```
   Validation report exported to: ${OUTPUT_DIR}/adapter-validation-${TARGET_PLATFORM}.md
   ```

---

## Error Handling

### Missing Adapter File
Handled in Phase 1 Step 3. The user is offered available alternatives or informed that no adapters exist.

### Researcher Agent Failure
Handled in Phase 2 Step 3. The user can retry, proceed with structural validation only, or cancel.

### Empty Research Results
If the researcher returns a profile with all sections marked as "unknown" or confidence "low":
- Proceed to Phase 3 but classify all entries as **Uncertain**
- In Phase 4, note that the health score is "N/A" due to insufficient research data
- Recommend the user provide documentation URLs directly or try again later

### Malformed Adapter File
If the adapter file cannot be parsed (missing H2 headers, unrecognized structure):
1. Report which sections were found and which are missing or malformed
2. Offer to validate only the parseable sections
3. Note structural issues in the validation report

---

## Agent Coordination

The researcher agent is spawned via Task tool with `subagent_type: "agent-alchemy-plugin-tools:researcher"`. The researcher uses Sonnet model and has access to WebSearch, WebFetch, Read, Glob, Grep, and Context7 tools.

Key coordination points:
- Pass the adapter file path to the researcher so it can perform its Phase 4: Adapter Comparison
- The researcher returns a structured platform profile with an Adapter Comparison section
- This skill consumes the Adapter Comparison data to drive the classification in Phase 3
- If the researcher fails, this skill degrades gracefully to structural validation only
