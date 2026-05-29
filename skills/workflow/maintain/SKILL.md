---
name: maintain
description: Workspace maintenance with health checks, index rebuilding, task sync, memory gap detection, archival, inbox processing, and reference file updates
user-invocable: true
help:
  purpose: |-
    Workspace maintenance: health checks, index rebuilding, task sync, inbox processing, and reference file updates.
  use_cases:
    - "Run a health check"
    - "Rebuild indexes"
    - "Process my inbox"
    - "Sync my tasks"
  scope: maintenance,health,sync,rebuild,inbox,update
---
<!-- MAINTENANCE: If modifying this skill, run tests/validate-docs.py
     to check for broken cross-references. See CONTRIBUTING.md. -->

# Maintain skill: health, sync, rebuild, inbox, and update

Comprehensive workspace maintenance with five distinct modes: running health checks, syncing tasks and detecting gaps, rebuilding all index files, batch-processing inbox items with parallel sub-agents, and updating workspace reference files to match the latest plugin version.

---

## Automatic vs user-initiated operations

### Automatic (daily, session-start triggered)

These operations run silently at the start of the first session each day via the core skill's session-start housekeeping check. They require no user interaction and produce no output unless critical issues are found.

| Operation | Script | What it does | Failure behavior |
|-----------|--------|-------------|-----------------|
| Archival sweep | `scripts/archive.py --auto` | Expire ephemeral lines past their `[expires:]` date, check staleness thresholds, move qualifying files to `archive/` | Log failure, continue session |
| Health check | `scripts/health-check.py` | Validate indexes vs files on disk, check for broken wikilinks, flag naming violations | Log failure, continue session |
| Task sync | `scripts/sync.py` | Check `reference/schedule.md` for due recurring/one-time items, scan for orphan tasks | Log failure, continue session |
| Inbox count | (directory listing) | Count files in `inbox/pending/` and update `.housekeeping-state.yaml` | Non-critical, skip on error |

**Triggering:** The core skill reads `reference/.housekeeping-state.yaml` at session start. If `last_run` is not today, it runs the above scripts in sequence, updates the state file, and proceeds to the user's request.

### User-initiated (explicit command only)

These operations are more expensive, require user judgment, or have side-effects that need confirmation. They are invoked via `/maintain <mode>` or natural language ("rebuild indexes", "process inbox", "deep sync").

| Operation | Command | Why not automatic |
|-----------|---------|------------------|
| Full index rebuild | `/maintain rebuild` | Rewrites all `_index.md` files. Expensive for large workspaces. Only needed when indexes are known to be stale or corrupted. |
| Inbox processing | `/maintain inbox` | Spawns sub-agents that create tasks and memory entries. Requires user to review and confirm the processing plan before execution. |
| Comprehensive sync | `/maintain sync --comprehensive` | Queries MCP sources (project tracker, calendar), scans last 90 days of journal. Higher cost. Surfaces items that need user triage. |
| Reference file update | `/maintain update` | Updates workspace reference files to match latest plugin version. Preserves user data. Requires user to review changes before applying. |
| Unarchive content | (manual) | Requires user to select specific archived files to restore. No bulk unarchive. |
| Manual health fixes | `/maintain health` | Script-detected issues that require human judgment (file renames, broken wikilink resolution, frontmatter corrections). |

### Cowork scheduled shortcut

If the user's environment supports Cowork shortcuts with schedules, a `daily-housekeeping` shortcut can run maintenance on a cron schedule (e.g., 8 AM daily) instead of relying on session-start detection. This is the preferred approach when available, as it runs even on days the user doesn't start a session. See the shortcut definition in the plugin's shortcut registry.

The session-start check in the core skill serves as a fallback: if the scheduled shortcut already ran today, `last_run` will be current and the session-start check will be a no-op.

---

## Health mode

Scan for workspace issues, auto-fix where safe, and report problems requiring manual intervention.

### Step 1: Load workspace state

Read the following indexes:
- `memory/_index.md` (master memory index)
- `memory/decisions/_index.md`
- `memory/people/_index.md`
- `memory/initiatives/_index.md`
- `contexts/products/_index.md` (if exists)
- `reference/replacements.md`

### Step 2: Naming pattern validation

#### Decision files

Scan `memory/decisions/` for naming violations:

**Standard pattern:** `YYYY-MM-DD-{slug}.md`

| Violation | Example | Suggested fix |
|-----------|---------|---------------|
| Missing date prefix | `ba-role-definition.md` | Extract date from frontmatter, rename |
| Context-first | `ai-strategy-2026-01-20.md` | Reorder to `2026-01-20-ai-strategy.md` |
| No date anywhere | `legacy-decision.md` | Check frontmatter `date` field, rename |

**Auto-fix (safe):** If frontmatter contains `date` field, suggest rename command.

### Step 3: Frontmatter validation

Scan all memory files for required fields:

| Type | Required fields |
|------|-----------------|
| All memory | `title`, `type`, `summary`, `updated` |
| person | + `tags`, `aliases` |
| decision | + `status`, `decision_maker` |
| product-spec | + `status`, `owner` |

#### Status value validation

For decisions, verify `status` is one of: `proposed`, `decided`, `implemented`, `superseded`, `rejected`

For products/product-specs, verify `status` is one of: `active`, `planned`, `deprecated`

Report invalid values.

### Step 4: Index synchronization

#### Check for orphaned entries

For each category index:
1. List entries in `_index.md`
2. List actual `.md` files in folder
3. Flag entries in index that don't have corresponding files
4. Flag files that aren't in the index

#### Check for stale summaries

For each file in memory:
1. Compare file `updated` date with index entry
2. Flag if file was modified more recently than index was regenerated

**Auto-fix (safe):** Run `/maintain rebuild` to resync all indexes.

### Step 5: Broken wikilink detection

Scan all files in `memory/`, `journal/`, and `contexts/` for wikilinks:

Pattern: `[[Entity Name]]`

For each wikilink:
1. Check if entity exists in `memory/people/_index.md`
2. Check if entity exists in `memory/initiatives/_index.md`
3. Check if entity exists in `memory/products/_index.md`
4. Check if entity exists in `memory/decisions/_index.md`

Flag broken wikilinks (reference to non-existent entity).

### Step 6: Replacements coverage

Scan all journal files from the last 30 days for names:

1. Extract all capitalized multi-word names (potential person names)
2. Extract all acronyms (2-4 capital letters)
3. Cross-reference against `reference/replacements.md`

Flag names/acronyms that appear multiple times but aren't in replacements.

**Auto-fix (safe):** Add flagged items to `reference/replacements.md` with placeholder:
```markdown
| NewName | ?? (needs canonical form) |
```

### Step 7: Information redundancy check

#### Duplicate detection

Scan for potential duplicates:
1. Same entity name in different folders (e.g., person also exists as initiative)
2. Very similar file names in same folder (edit distance < 3)
3. Same `aliases` values across different files

#### Cross-reference check

For each person in `memory/people/`:
1. Check if they're referenced in any task (via task integration notes)
2. Check if they're referenced in any journal entry
3. Flag people with zero references in last 90 days as potentially stale

### Health mode output

Generate report in this format:

```markdown
## Housekeeping report (YYYY-MM-DD)

### Auto-fixed
| Category | File | Issue | Fix applied |
|----------|------|-------|------------|
| naming | decisions/ba-role-definition.md | Missing date prefix | Renamed to 2026-01-15-ba-role-definition.md |
| index | memory/people/_index.md | Orphan entry "Jane Doe" | Removed from index |
| index | (multiple) | Files not in index | Ran rebuild-indexes.py |
| replacements | reference/replacements.md | "JT" uncovered (5 uses) | Added placeholder entry |

### Manual action required
| Category | File | Issue | Suggested fix |
|----------|------|-------|---------------|
| frontmatter | memory/decisions/old.md | Invalid status "pending" | Change to "proposed" |
| wikilink | journal/2026-01/meeting.md | Broken link [[Unknown Person]] | Create memory entry or fix reference |

### Summary
- Auto-fixed: N issues (N renames, N index fixes, N replacement additions)
- Manual action required: N issues
- Workspace health: {healthy | needs attention | degraded}
```

---

## Sync mode

Sync tasks from integration, detect memory gaps, and triage stale items. Optional flag: `--comprehensive` for deep scan mode.

### Step 1: Load current state

Query task integration (read `reference/integrations.md` Tasks section for provider details):
- Execute `list` operation for all configured lists (default: Active, Delegated, Backlog)
- Execute `overdue` operation

Read:
- `memory/people/_index.md`
- `memory/initiatives/_index.md`

### Step 1.5: Check scheduled items and memory gaps

Run the automated sync script:

```bash
python3 scripts/sync.py {workspace_path}
```

This script checks `reference/schedule.md` for due items (recurring and one-time) and scans recent journal entries for memory gaps (people and initiatives referenced but not in memory). Parse the JSON output:

- `schedule.recurring_due`: Recurring items past their next-due date. After completion, advance `next-due` to the next occurrence in schedule.md.
- `schedule.onetime_due`: One-time items past their due date. After completion, remove the entry from schedule.md.
- `memory_gaps.unknown_people`: People referenced in journal but not in memory/people/. Present to user.
- `memory_gaps.unknown_initiatives`: Initiatives referenced but not in memory/initiatives/. Present to user.

Surface due items in the report under "Scheduled items." Merge memory gaps with Step 4 output.

If `scripts/sync.py` is not available, fall back to manual schedule checking:
Read `reference/schedule.md` if it exists. For each entry:
- **[RECURRING]**: Check if `next-due` is today or past. If due, add to triage output as "Scheduled item due."
- **[ONCE]**: Check if `due` is today or past. If due, surface it.

### Step 2: Sync from project tracker (if available)

If project tracker integration is configured:
1. Query for items assigned to user that are not in Active/Delegated tasks
2. Query for items recently completed that are still open as tasks
3. Present deltas: "Found {N} new items in project tracker not in your tasks. Add them?"
4. If accepted, create tasks via the task integration `add` operation in the appropriate list

### Step 3: Triage

Scan all reminders/tasks and flag:

| Condition | Flag |
|-----------|------|
| Past due date (from task integration `overdue` operation) | OVERDUE |
| Created >30 days ago without update (from notes field) | STALE |
| No initiative in notes field | ORPHAN |
| Owner in notes not in memory/people/ | UNKNOWN OWNER |

Present flagged items grouped by category. For each:
- OVERDUE: "Update due date, complete, or remove?"
- STALE: "Still relevant? Update, move to backlog, or remove?"
- ORPHAN: "Link to an initiative or keep as standalone?"
- UNKNOWN OWNER: "Add this person to memory?"

### Step 4: Memory gap detection

Decode all entities referenced in tasks:

1. **People**: Extract all owner names and mentioned people from notes fields. Cross-reference against `memory/people/_index.md`. List undefined people.
2. **Initiatives**: Extract all `[[Initiative]]` references from notes fields. Cross-reference against `memory/initiatives/_index.md`. List undefined initiatives.
3. **Terms**: Scan task titles for capitalized terms, acronyms, and project names not in `reference/replacements.md` or memory indexes. List undefined terms.

Present gaps:
```
## Memory gaps detected

### Undefined people (referenced in tasks but not in memory)
- "Sarah Chen" (owner of 3 tasks) -- Create memory entry?
- "Mike R." (mentioned in 1 task) -- Add to replacements?

### Undefined initiatives
- "Project Phoenix" (linked to 2 tasks) -- Create initiative entry?

### Undefined terms
- "RBAC" (used in 2 task descriptions) -- Add to replacements?
```

For each gap, ask user to provide brief context, then create the memory entry or replacement.

### Sync mode output (default)

```markdown
## Update complete

| Category | Count |
|----------|-------|
| Tasks synced from project tracker | N |
| Overdue tasks flagged | N |
| Stale tasks flagged | N |
| Orphan tasks flagged | N |
| Memory gaps found | N |
| Memory entries created | N |
| Replacements added | N |
```

### Comprehensive mode (`--comprehensive`)

All of default mode, PLUS:

#### Step 5: MCP source scan

If project tracker is configured:
- Query recent items (last 14 days) for action items not captured
- Surface items assigned to user's team members

Query the calendar integration for last 7 days of meetings (see `reference/integrations.md` Calendar section):
- Resolve the start date (7 days ago) to `YYYY-MM-DD` format, execute `list_events` operation with offset=7
- Cross-reference against journal entries
- Flag meetings that occurred but have no journal entry: "You had '{Meeting Title}' on {date} but no meeting notes. Process it?"

If calendar integration is not reachable, skip calendar scan and note the gap.

#### Step 6: Stale memory cleanup

Scan memory for staleness:
- Initiatives tagged `completed` that still have open reminders -> flag
- People not referenced in any reminder or journal entry in last 90 days -> flag for review
- Decisions older than 6 months -> flag for relevance check

Present:
```
## Stale memory candidates

- memory/initiatives/old-project.md -- Tagged completed, 2 open tasks reference it
- memory/people/former-vendor.md -- Not referenced in 90+ days
- memory/decisions/q3-decision.md -- 6+ months old, verify still relevant
```

#### Step 7: Entity discovery

From MCP sources scanned in Step 5:
- Surface new people names not in memory
- Surface new project/initiative names not in memory
- Offer to create entries

#### Comprehensive report

Append to default report:

```markdown
### Comprehensive scan results
| Category | Count |
|----------|-------|
| Unprocessed meetings found | N |
| New entities from MCP sources | N |
| Stale memory candidates | N |
```

---

## Rebuild mode

Regenerate all _index.md files from current file contents and frontmatter.

### Step 1: Memory indexes

For each category in `memory/` (people, initiatives, decisions, products, vendors, competitors, organizational-context):

1. Scan all `.md` files in the folder (excluding `_index.md` and `_template.md`)
2. Read frontmatter from each file: `title`, `aliases`, `tags`, `summary`, `updated`
3. Generate `_index.md` with format:

```markdown
# [Category] index

| Name | Aliases | File | Summary | Updated |
|------|---------|------|---------|---------|
| Entity Name | alias1, alias2 | filename.md | One-line summary | YYYY-MM-DD |
```

For initiatives, separate into Active and Completed sections based on tags.

### Step 2: Master memory index

Generate `memory/_index.md`:

```markdown
# Memory index

| Category | Path | Count |
|----------|------|-------|
| People | memory/people/ | N |
| Initiatives | memory/initiatives/ | N |
| Decisions | memory/decisions/ | N |
| Products | memory/products/ | N |
| Vendors | memory/vendors/ | N |
| Competitors | memory/competitors/ | N |
| Organizational context | memory/organizational-context/ | N |
```

### Step 3: Journal indexes

For each month folder in `journal/`:

1. Scan all `.md` files (excluding `_index.md`)
2. Read frontmatter: `date`, `type`, `title`, `participants`, `initiatives`
3. Generate `journal/YYYY-MM/_index.md`:

```markdown
# [Month Year] journal index

| Date | Type | Title | Participants | Initiatives |
|------|------|-------|-------------|-------------|
| YYYY-MM-DD | meeting | Title | Names | Initiatives |
```

### Step 4: Contexts/products index

Scan `contexts/products/` for product specification files:

1. Scan all `.md` files in the folder (excluding `_index.md`)
2. Read frontmatter: `title`, `type`, `status`, `owner`, `summary`, `updated`
3. Generate `contexts/products/_index.md`:

```markdown
# Product specifications index

| Name | Status | Owner | Summary | Updated |
|------|--------|-------|---------|---------|
| Product Name | active | [[Owner Name]] | One-line summary | YYYY-MM-DD |
```

### Step 5: Decision file validation

For files in `memory/decisions/`:

1. Check naming convention: should be `YYYY-MM-DD-{slug}.md`
2. Flag files that don't match the pattern:
   - Missing date prefix
   - Non-standard date format
   - Context-first naming (e.g., `topic-YYYY-MM-DD.md`)
3. Report suggested renames

### Step 6: Annual rollup (if applicable)

For completed years, generate `journal/YYYY-annual-index.md` consolidating all month indexes.

### Rebuild mode output

Report what was regenerated and any issues found:

```markdown
## Rebuild complete

### Indexes regenerated
| Area | Count |
|------|-------|
| Memory categories | N |
| Journal months | N |
| Contexts/products | N |

### Issues found
| Type | File | Issue | Suggested fix |
|------|------|-------|---------------|
| missing-frontmatter | path/file.md | No frontmatter | Add required fields |
| naming-violation | decisions/file.md | Missing date prefix | Rename to YYYY-MM-DD-slug.md |
| missing-required | path/file.md | Missing `summary` field | Add summary for index |
```

### Script invocation

Run the automated rebuild script for deterministic index generation:

```bash
python3 scripts/rebuild-indexes.py {workspace_path}
```

This script performs Steps 1-5 deterministically (memory indexes, master index, journal indexes, contexts index, decision naming validation). Parse the JSON output and use it to populate the rebuild report.

#### Interpreting script output

The script returns JSON with:
- `stats`: counts of memory categories, journal months, context products, and total entries rebuilt
- `issues`: array of problems found (missing-frontmatter, naming-violation, missing-required fields)
- `total_issues`: count of all issues

Present the `stats` as the "Indexes regenerated" table. Present `issues` as the "Issues found" table. The script handles all file I/O — do not duplicate its work by manually reading and rewriting index files.

#### When to skip the script

If `scripts/rebuild-indexes.py` is not available (e.g., workspace predates script extraction), fall back to the manual procedure above.

### Post-execution checklist
- [ ] All memory category indexes regenerated
- [ ] Master memory index regenerated
- [ ] All journal month indexes regenerated
- [ ] Contexts/products index regenerated
- [ ] Decision naming validated
- [ ] Any missing frontmatter flagged to user
- [ ] Suggested fixes presented

---

## Inbox mode

Batch-process all pending items in the inbox using **isolated parallel sub-agents**. Each item is processed by an independent sub-agent with its own context, ensuring no cross-contamination between items.

### Step 1: Scan inbox

List all files in `inbox/pending/`. For each file:
1. Read the first 50 lines to determine content type
2. Classify as one of: `transcript`, `article`, `email`, `notes`, `unknown`
3. Build processing queue with file path, detected type, and file size

If no pending items, report "Inbox is empty" and exit.

### Step 2: Present processing plan

Before spawning sub-agents, present the plan to the user:

```markdown
## Inbox processing plan

| # | File | Detected type | Proposed action |
|---|------|---------------|-----------------|
| 1 | meeting-2026-02-05.txt | transcript | Process as meeting (tasks + memory) |
| 2 | article-ai-strategy.md | article | Extract wisdom |
| 3 | notes-from-call.txt | notes | Extract tasks + memory |
| 4 | unknown-file.txt | unknown | Skip (manual review needed) |

Process all items? (Confirm before proceeding)
```

Wait for user confirmation before spawning sub-agents. Allow the user to exclude specific items or change detected types.

### Step 2.5: Pre-resolve names across all transcript items

Before spawning sub-agents, perform a single pass of name resolution across ALL confirmed transcript items to ensure consistency and minimize user interruptions.

Apply the **name resolution protocol** (core skill, Memory protocol section):
1. For each transcript item, scan for person names
2. Cross-reference all names against `reference/replacements.md` and `memory/people/_index.md`
3. For transcript items: query calendar integration for each meeting date to retrieve attendee lists
4. Apply contextual resolution from calendar attendees and document context
5. If any names remain ambiguous or unknown across ALL files, batch them into a single user clarification
6. Build a consolidated name resolution table

Pass the resolution table to each sub-agent in its prompt: "Use these resolved canonical names: Christopher = Christopher Smith, Mick = Michael Johnson"

This prevents: (a) each sub-agent independently guessing different resolutions for the same person, (b) the user being asked the same question by multiple sub-agents, (c) wrong names propagating to memory and tasks.

Skip this step if no transcript items are in the confirmed plan.

### Step 3: Parallel sub-agent processing

After user confirmation:

1. Move ALL files from `inbox/pending/` to `inbox/processing/` as a sequential batch. Complete all moves before proceeding.
2. Spawn **one sub-agent per inbox item** using the Task tool. **Launch all sub-agents in a single message** for maximum parallelism.

The move-all-first ordering prevents any concurrent session from double-processing items.

##### Sub-agent template by content type

**Transcript items:**
```
You are processing a meeting transcript from the inbox.
Use the meeting skill pipeline (skills/meeting/SKILL.md) as your execution guide.

Source file: inbox/processing/{filename}

Step 1: Load reference files (MANDATORY before reading transcript)
- Read reference/replacements.md. Apply canonical names to ALL content.
- If the main agent provided a name resolution table, apply those resolved names.
  Do NOT re-resolve names in the table. Only resolve names NOT in the table using replacements.md.
- Read reference/integrations.md (Calendar and Tasks sections).
- Read memory indexes: memory/people/_index.md, memory/initiatives/_index.md, memory/decisions/_index.md.
  These indexes are required for wikilink validation in Step 4.

Step 2: Resolve transcript content
- Read the transcript file.
- Resolve speaker names: if speakers are generic ("Speaker 1"), infer real names from context.
  NEVER use generic speaker labels in output.
- Query calendar integration for this meeting date to retrieve attendee list, official title, and organizer.
  If calendar is unavailable, proceed with transcript data and note the gap.

Step 3: Generate structured report
Produce ALL five sections:
- Topics: discussion points as bullets
- Updates: status updates from people other than the user (name, project, date)
- Concerns: risks raised (who, issue, deadline)
- Decisions: what was decided and who made the call
- Action items: classified as For me / For others / Unassigned

Step 4: Save to journal
- Filename: journal/YYYY-MM/YYYY-MM-DD-meeting-{slug}.md
- Frontmatter: date, title, type: meeting, participants, organizer, topics, initiatives, source
- Body: use [[wikilink]] syntax for all entity references (people, initiatives, decisions)
- BEFORE writing any [[Name]], verify the name exists in the memory indexes read in Step 1.
  If a name does NOT appear in any index AND is not in replacements.md: add it to reference/replacements.md
  with placeholder "?? (needs canonical form)" and include it in the unverified_wikilinks field.
  Do NOT fabricate wikilinks for unverified names.

Step 5: Extract tasks
- Apply accountability test (never create tasks for "Team" or "We" without a specific lead)
- Check for duplicates across all configured task lists
- Create via task integration. Resolve relative dates to YYYY-MM-DD.
- Check each tool response. Only count a task as created if the response confirms success.
- After all creation attempts, execute list_reminders for each list that received new tasks.
  Verify each task appears by matching title. Add any missing tasks to creation_unverified.
  NEVER report tasks as created without verification.

Step 6: Extract memory
- Apply durability test to each insight
- Persist durable insights to memory/ using the folder mapping from the core skill
- Update relevant _index.md files after writing
- Use .lock files for memory writes (cowork protocol)

After all steps complete, move the source file to inbox/completed/{filename}.

Return JSON:
{
  "status": "ok" | "partial" | "error",
  "source_file": "{filename}",
  "content_type": "transcript",
  "journal_path": "journal/YYYY-MM/...",
  "tasks_created": 0,
  "memory_updates": 0,
  "creation_unverified": [],
  "unverified_wikilinks": [],
  "errors": []
}
Status "partial": journal entry was saved but one or more downstream steps failed.
Status "error": the journal entry could not be saved.
```

**Article/wisdom items:**
```
You are extracting wisdom from an article in the inbox.
Use the wisdom extraction pipeline (skills/learn/SKILL.md, Mode B) as your execution guide.

Source file: inbox/processing/{filename}

Step 1: Load reference files (MANDATORY before reading article)
- Read reference/replacements.md. Apply canonical names to ALL content.
- If the main agent provided a name resolution table, apply those resolved names.
  Do NOT re-resolve names in the table.
- Read memory indexes: memory/people/_index.md, memory/initiatives/_index.md, memory/decisions/_index.md.
  Required for wikilink validation before writing to memory.

Step 2: Read and classify article content.

Step 3: Extract insights
- Apply durability test to each insight (all four criteria from core skill memory protocol).
- Discard insights that fail.

Step 4: Persist durable insights to memory
- Map each passing insight to the correct memory folder (people, initiatives, decisions, etc.)
- BEFORE writing any [[wikilink]], verify the entity name exists in the memory indexes read in Step 1.
  If a name does NOT appear in any index: add it to reference/replacements.md with placeholder
  "?? (needs canonical form)" and include it in the unverified_wikilinks field.
  Do NOT fabricate wikilinks for unverified names.
- Update relevant _index.md after each write.
- Use .lock files for memory writes (cowork protocol).

Step 5: Save extraction report
- Filename: journal/YYYY-MM/YYYY-MM-DD-wisdom-{slug}.md

Step 6: Extract tasks
- Apply accountability test.
- Create via task integration.
- Check each tool response. Only count a task as created if the response confirms success.
- After all creation attempts, execute list_reminders for each list that received new tasks.
  Verify each task appears by matching title. Add any missing tasks to creation_unverified.
  NEVER report tasks as created without verification.

After all steps complete, move the source file to inbox/completed/{filename}.

Return JSON:
{
  "status": "ok" | "partial" | "error",
  "source_file": "{filename}",
  "content_type": "article",
  "journal_path": "journal/YYYY-MM/...",
  "insights_persisted": 0,
  "tasks_created": 0,
  "creation_unverified": [],
  "unverified_wikilinks": [],
  "errors": []
}
Status "partial": journal entry was saved but one or more downstream steps failed.
Status "error": the journal entry could not be saved.
```

**Notes items:**
```
You are processing notes from the inbox.

Source file: inbox/processing/{filename}

Step 1: Load reference files (MANDATORY before reading notes)
- Read reference/replacements.md. Apply canonical names to ALL content.
- If the main agent provided a name resolution table, apply those resolved names.
  Do NOT re-resolve names in the table.
- Read reference/integrations.md Tasks section for task creation.
- Read memory indexes: memory/people/_index.md, memory/initiatives/_index.md, memory/decisions/_index.md.
  Required for wikilink validation before writing to memory or journal.

Step 2: Read the notes file.

Step 3: Extract tasks
- Apply accountability test (never create tasks for "Team" or "We" without a specific lead)
- Check for duplicates across all configured task lists
- Create via task integration. Resolve relative dates to YYYY-MM-DD.
- Check each tool response. Only count a task as created if the response confirms success.
- After all creation attempts, execute list_reminders for each list that received new tasks.
  Verify each task appears by matching title. Add any missing tasks to creation_unverified.
  NEVER report tasks as created without verification.

Step 4: Extract durable memory
- Apply durability test to each insight.
- BEFORE writing any [[wikilink]], verify the entity name exists in the memory indexes read in Step 1.
  If a name does NOT appear in any index: add it to reference/replacements.md with placeholder
  "?? (needs canonical form)" and include it in the unverified_wikilinks field.
  Do NOT fabricate wikilinks for unverified names.
- Persist passing insights to memory/. Update relevant _index.md files.
- Use .lock files for memory writes (cowork protocol).

Step 5: Save notes summary
- Filename: journal/YYYY-MM/YYYY-MM-DD-notes-{slug}.md
- Body: use [[wikilink]] syntax for verified entity references only.

After all steps complete, move the source file to inbox/completed/{filename}.

Return JSON:
{
  "status": "ok" | "partial" | "error",
  "source_file": "{filename}",
  "content_type": "notes",
  "journal_path": "journal/YYYY-MM/...",
  "tasks_created": 0,
  "memory_updates": 0,
  "creation_unverified": [],
  "unverified_wikilinks": [],
  "errors": []
}
Status "partial": journal entry was saved but one or more downstream steps failed.
Status "error": the journal entry could not be saved.
```

### Step 4: Collect results and handle failures

After all sub-agents complete, collect JSON results from each sub-agent and evaluate status:

**Status "ok"**: All steps completed successfully. No action needed beyond reporting.

**Status "partial"**: The journal entry was saved but one or more downstream steps failed.
- Do NOT move the source file to `inbox/failed/` (the journal entry exists and is valid).
- Source file is already in `inbox/completed/` (sub-agent moved it).
- In the consolidated report, flag the item with status "partial" and list which steps failed (derive from the `errors[]` array).
- Surface any `unverified_wikilinks[]` so the user can resolve them.
- Surface any `creation_unverified[]` tasks prominently so the user knows to check.

**Status "error"**: The journal entry could not be saved. The sub-agent failed entirely.
- Move the source file from `inbox/processing/` to `inbox/failed/`.
- Create a companion `.error` file at `inbox/failed/{filename}.error` containing the `errors[]` array.

Generate consolidated report (format defined in "Inbox mode output" below).

### Sub-agent input/output contracts (inbox mode)

| Content type | Input | Output | Failure mode |
|-------------|-------|--------|-------------|
| Transcript | Source file, replacements.md, integrations.md, memory indexes (people, initiatives, decisions) | JSON: journal path, tasks created, memory updates, creation unverified, unverified wikilinks | ok/partial: source to completed; error: source to failed with .error file |
| Article | Source file, replacements.md, memory indexes (people, initiatives, decisions) | JSON: journal path, insights persisted, tasks created, creation unverified, unverified wikilinks | ok/partial: source to completed; error: source to failed with .error file |
| Notes | Source file, replacements.md, integrations.md, memory indexes (people, initiatives, decisions) | JSON: journal path, tasks created, memory updates, creation unverified, unverified wikilinks | ok/partial: source to completed; error: source to failed with .error file |

**Shared constraints for all inbox sub-agents:**
- Each sub-agent operates with fully isolated context
- Each sub-agent reads its own copy of reference files (no shared state)
- Memory writes must use `.lock` files (see core skill cowork protocol)
- Task creation checks for duplicates independently per sub-agent
- Task creation MUST be verified via `list_reminders` after all creation attempts
- If a sub-agent fails, other sub-agents continue unaffected

### Inbox mode output

```markdown
## Inbox processing complete

### Processed items
| # | File | Type | Journal | Tasks | Memory | Status |
|---|------|------|---------|-------|--------|--------|
| 1 | meeting-2026-02-05.txt | transcript | journal/2026-02/... | 3 | 2 | ok |
| 2 | article-ai-strategy.md | article | journal/2026-02/... | 0 | 4 | partial (tasks failed) |
| 3 | notes-from-call.txt | notes | journal/2026-02/... | 2 | 1 | ok |

### Partial items
| File | Journal saved | Failed steps | Unverified wikilinks | Unverified tasks |
|------|---------------|-------------|----------------------|------------------|
| article-ai-strategy.md | journal/2026-02/... | tasks (0 created) | [[Unknown Vendor]] | -- |

### Failed items
| File | Error |
|------|-------|
| (none) | |

### Summary
- Items processed: N (ok: N, partial: N)
- Items failed: N
- Tasks created: N (total across all items, verified via list_reminders)
- Tasks unverified: N (created but not confirmed in list)
- Memory updates: N (total across all items)
- Journal entries created: N
- Unverified wikilinks: N (names not found in memory indexes)
```

### Progress tracking (TodoWrite) for inbox mode

```
1. Scan inbox and classify items                   [in_progress → completed]
2. Present processing plan for approval            [pending → completed]
3. Process item: {filename1} (parallel)            [pending → completed]
4. Process item: {filename2} (parallel)            [pending → completed]
5. Process item: {filename3} (parallel)            [pending → completed]
6. Collect results and generate report             [pending → completed]
```

Mark all item-processing todos as `in_progress` simultaneously when spawning sub-agents. Mark each `completed` as its sub-agent returns.

---

## Update mode

Update workspace reference files to match the installed plugin version. Preserves user customizations (name replacements, KPI definitions, schedule items) while applying structural changes from plugin updates.

### Step 1: Version check

Read `reference/.housekeeping-state.yaml` for `plugin_version`.
Read the plugin's `.claude-plugin/plugin.json` for the current version.

If both versions match, report "Workspace reference files are up to date (v{version})" and exit.
If the workspace has no `plugin_version` field, this is the first update — proceed.

### Step 2: Dry-run preview

Run the update script in preview mode:

```bash
python3 scripts/update-reference.py {workspace_path} {plugin_path} --dry-run
```

Parse the JSON output and present to the user:

```markdown
## Reference file update preview (v{old} → v{new})

### Files to update
| File | Action | User data preserved |
|------|--------|-------------------|
| taxonomy.md | Full replace | (none — no user data) |
| integrations.md | Section merge | status: configured (Tasks) |

### New files to create
| File | Description |
|------|-------------|
| shortcuts.md | Command reference |

### Files unchanged
- replacements.md, schedule.md

### Warnings
- (any conflicts or issues)

Proceed with update?
```

Wait for user confirmation.

### Step 3: Apply update

After user confirmation, run without `--dry-run`:

```bash
python3 scripts/update-reference.py {workspace_path} {plugin_path}
```

Parse the JSON output and report:

```markdown
## Reference files updated (v{new})

- Files updated: N
- Files created: N
- Files unchanged: N
- User data preserved: (list)
- Warnings: (list)
```

### When the script is not available

If `scripts/update-reference.py` is not found, provide manual update guidance:

1. **Safe to overwrite** (no user data): `taxonomy.md`, `workflows.md`, `shortcuts.md`, `guardrails.yaml`
   - Copy from plugin source directly

2. **Requires manual merge** (contain user data):
   - `integrations.md`: Copy new constraint rules from plugin, keep your `status:` fields
   - `replacements.md`: Copy updated header/instructions from plugin, keep your name/team/product rows
   - `schedule.md`: Copy updated format spec from plugin, keep your recurring/one-time items
   - `kpis.md`: Copy updated header/instructions from plugin, keep your team/initiative sections

3. **State files** (machine-managed): `.housekeeping-state.yaml`, `maturity.yaml`
   - Add any new keys from plugin source, keep existing values

### Update mode output

```markdown
## Update complete

| Category | Count |
|----------|-------|
| Files updated | N |
| Files created | N |
| Files unchanged | N |
| User data preserved | N sections |
| Warnings | N |
```

---

## Script invocation for health mode

Before performing manual checks, run the automated scripts for deterministic validation:

### Step 0: Run health-check.py

```bash
python3 scripts/health-check.py {workspace_path}
```

This script performs Steps 2-6 deterministically (naming validation, frontmatter checks, index sync, wikilink detection, replacements coverage). Parse the JSON output and use it to populate the issues table in the report. Only manually investigate items the script cannot assess (Step 7: information redundancy, cross-reference depth).

### Step 0b: Run archive.py (optional)

```bash
python3 scripts/archive.py {workspace_path}
```

or for preview only:

```bash
python3 scripts/archive.py {workspace_path} --dry-run
```

This script scans memory files for staleness and archives expired content. Run with `--dry-run` first to preview, then confirm with the user before running without the flag. Parse the JSON output and include archived file counts in the report.

### Interpreting script output

The scripts return JSON. Key fields:
- `health-check.py`: `issues` array (each with category, file, issue, suggested_fix), `auto_fixes` array, `summary` stats
- `archive.py`: `files_archived`, `expired_lines_removed`, `archived_files` array with paths and reasons

After parsing health-check.py JSON, classify each issue by fixability and execute safe auto-fixes:

**Auto-fixable (execute immediately):**

| Issue category | Fix action | Safety condition |
|---------------|-----------|-----------------|
| `naming` (decision files) | Rename file to the `suggested_fix` target | Only if frontmatter `date` field exists and is valid YYYY-MM-DD |
| `index` (orphan entries) | Remove orphan row from the category `_index.md` | Only if source file confirmed absent from disk |
| `index` (files not in index / stale summaries) | Run `python3 scripts/rebuild-indexes.py {workspace_path}` once | Deterministic index regeneration |
| `replacements` (uncovered names) | Add `??` placeholder entries to `reference/replacements.md` | Existing behavior |

**NOT auto-fixable (present to user):**

| Issue category | Why |
|---------------|-----|
| `frontmatter` (missing fields) | Values require user judgment |
| `frontmatter` (invalid status) | Correct status requires understanding intent |
| `wikilink` (broken references) | May need entity creation or reference correction |
| `replacements` (with `??` placeholder) | User must provide canonical name |

If any auto-fix fails (file locked, permission error, target exists), demote it to the manual-fix list with the error reason.

---

## Context budget

**Health mode:**
- Memory indexes: Read all `_index.md` files
- Memory files: Scan frontmatter only (not full content) unless checking wikilinks
- Journal: Scan last 30 days of entries
- Reference: Read `replacements.md`

**Sync mode:**
- Task integration: Up to 3 queries per list
- Memory indexes: Read people and initiatives indexes
- Schedule: Read `reference/schedule.md` if exists
- Project tracker: Up to 3 queries per team
- Calendar: Last 7 days of events (comprehensive mode)
- Journal: Scan last 90 days for staleness and entity discovery (comprehensive mode)

**Rebuild mode:**
- Memory: Scan all files in all categories
- Journal: Scan all month folders
- Contexts: Scan products folder (if exists)
- Reference: None required

**Inbox mode:**
- Main agent: Read `inbox/pending/` file list + first 50 lines of each file for classification
- Each sub-agent: Read its assigned source file + `reference/replacements.md` + `reference/integrations.md` + `memory/people/_index.md` + `memory/initiatives/_index.md` + `memory/decisions/_index.md` (all three indexes mandatory for wikilink validation) + `list_reminders` queries for task verification
- Sub-agents have isolated context; budget is per-item, not cumulative

---

## Absolute constraints

**Health mode:**
- NEVER delete files (only suggest deletions with user confirmation)
- NEVER modify file content (only metadata like replacements and index entries)
- NEVER change wikilink targets without user approval
- **Auto-fix scope:** Execute deterministic fixes (file renames from frontmatter dates, index orphan removal, index rebuilds, replacement placeholder additions). Present non-deterministic issues (missing frontmatter values, invalid enums, broken wikilinks) to the user. If an auto-fix fails, demote to manual.

**Sync mode:**
- NEVER create tasks without user approval
- NEVER fabricate data from missing integrations (report gaps)
- NEVER modify tasks without user confirmation
- ALWAYS use provider-agnostic language (no hardcoded Jira/Asana terminology)
- NEVER skip memory gap detection

**Rebuild mode:**
- NEVER modify file content (only regenerate indexes)
- NEVER delete files
- ALWAYS validate decision naming patterns
- ALWAYS report missing frontmatter
- NEVER skip any category

**Inbox mode:**
- NEVER process items without user confirmation of the processing plan
- NEVER delete source files (move to completed/ or failed/, never remove)
- ALWAYS create .error companion files for failed items
- ALWAYS use `.lock` files for memory writes from parallel sub-agents
- NEVER spawn sub-agents for items classified as `unknown` (require manual review)
- ALWAYS move ALL `inbox/pending/` files to `inbox/processing/` BEFORE spawning any sub-agents
- NEVER write `[[wikilinks]]` for names not verified against memory indexes (flag as unverified instead)
- NEVER report tasks as created without verifying via `list_reminders` after creation

---

## Documentation note

When building future functionality, consider whether the housekeeping script should be updated to include relevant validation elements.
