---
name: routing-table-updater
description: "Maintain /do routing tables when skills or agents change."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
  - Skill
routing:
  triggers:
    - "update routing"
    - "sync routing tables"
    - "routing maintenance"
    - "rebuild routing index"
    - "routing drift"
  category: meta-tooling
  pairs_with:
    - toolkit-evolution
    - generate-claudemd
---

# Routing Table Updater Skill

## Overview

This skill maintains /do routing tables and command references when skills or agents are added, modified, or removed. It implements a **Phase-Gated Pipeline** -- scan, extract, generate, update, verify -- with deterministic script execution at each phase.

The skill reads metadata from all skills and agents (never modifies them) and safely updates `skills/meta/do/SKILL.md`, `skills/meta/do/references/routing-tables.md`, `agents/INDEX.json`, and `commands/*.md` files. All changes are backed up before modification, and markdown syntax is validated before commit.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| batch registration of many skills (invoked by pipeline-scaffolder) | `batch-mode.md` | Loads detailed guidance from `batch-mode.md`. |
| resolving trigger conflicts: priority rules and severity levels | `conflict-resolution.md` | Loads detailed guidance from `conflict-resolution.md`. |
| errors, error handling | `error-handling.md` | Loads detailed guidance from `error-handling.md`. |
| worked update scenarios: new skill, conflict, manual entry, complexity change | `examples.md` | Loads detailed guidance from `examples.md`. |
| extracting trigger phrases: 'use when' clauses, action verbs, domain keywords, complexity inference | `extraction-patterns.md` | Loads detailed guidance from `extraction-patterns.md`. |
| /do routing table structure, auto-generated markers, ordering rules | `routing-format.md` | Loads detailed guidance from `routing-format.md`. |
| skill-entry examples for registering a newly created skill | `skill-examples.md` | Loads detailed guidance from `skill-examples.md`. |

## Instructions

### Phase 1: SCAN -- Discover All Skills and Agents

**Goal**: Find every skill and agent file in the repository.

**Constraints**: Repository must be at agents toolkit root (requires `commands/do.md`); only scan `skills/*/SKILL.md` and `agents/*.md` formats; file permissions must allow reading.

**Step 1: Run scan script**

```bash
python3 ~/.claude/skills/meta/routing-table-updater/scripts/scan.py --repo $HOME/vexjoy-agent
```

**Step 2: Validate scan output**

Expected output is JSON with `skills_found`, `agents_found`, `skills` (array of paths to skills/*/SKILL.md), `agents` (array of paths to agents/*.md).

**Step 3: Check for gaps**

Compare discovered count against expected. If missing, check directory naming, agent file naming, or file permissions.

**Gate**: All skill directories and agent files are discovered without permission errors. Proceed to Phase 2 only after the gate passes. See `references/error-handling.md` for gate failure recovery.

---

### Phase 2: EXTRACT -- Parse Metadata

**Goal**: Extract YAML frontmatter, trigger patterns, complexity, and routing table targets from every discovered file.

**Constraints**: YAML frontmatter must be valid; required fields (`name`, `description`) must be present; trigger patterns extracted from description text; complexity inference must follow `references/extraction-patterns.md`.

**Step 1: Run extraction script**

```bash
python3 ~/.claude/skills/meta/routing-table-updater/scripts/extract_metadata.py --input scan_results.json --output metadata.json
```

**Step 2: Verify extraction completeness**

For each capability, confirm extracted fields: `name`, `description`, `trigger_patterns` (skills), `domain_keywords` (agents), `complexity` (Simple, Medium, Complex), `routing_table` (Intent Detection, Task Type, Domain-Specific, or Combination).

**Step 3: Validate trigger pattern quality**

Review against `references/extraction-patterns.md`. Patterns must be specific enough to avoid false matches, broad enough to catch common phrasings, and free of generic terms.

**Gate**: All YAML parsed successfully, required fields are present, trigger patterns are extracted for skills, and domain keywords are extracted for agents. Proceed to Phase 3 only after the gate passes. See `references/error-handling.md` for gate failure recovery.

---

### Phase 3: GENERATE -- Create Routing Table Entries

**Goal**: Map extracted metadata to routing entries and detect conflicts.

**Constraints**: Deterministic generation (no randomness); entries follow exact /do format spec (`references/routing-format.md`); pattern conflicts detected immediately; entries sorted alphabetically; duplicates within same table block gate passage.

**Step 1: Run generation script**

```bash
python3 ~/.claude/skills/meta/routing-table-updater/scripts/generate_routes.py --input metadata.json --output routing_entries.json
```

**Step 2: Understand the generation process**

1. Load routing format spec from `references/routing-format.md`
2. Map each capability to appropriate routing table
3. Format entries according to /do table structure
4. Detect pattern conflicts (see `references/conflict-resolution.md`)
5. Sort entries alphabetically within tables

**Step 3: Review conflict detection output**

Low-severity conflicts: script applies specificity rules automatically. High-severity conflicts: script blocks gate passage and requires manual resolution.

**Gate**: All capabilities are mapped, entries follow /do format, conflicts are documented, and no duplicates remain within the same table. Proceed to Phase 4 only after the gate passes. See `references/error-handling.md` for gate failure recovery.

---

### Phase 4A: UPDATE -- Safely Modify commands/do.md

**Goal**: Apply generated routing entries to do.md with backup and validation.

**Constraints**: Always create timestamped backup before modification; preserve all hand-written entries (entries without `[AUTO-GENERATED]` marker are never overwritten); markdown table syntax validates after updates; atomic backup/restore on validation failure.

**Step 1: Run update script with backup**

```bash
python3 ~/.claude/skills/meta/routing-table-updater/scripts/update_routing.py --input routing_entries.json --target $HOME/vexjoy-agent/commands/do.md --backup
```

**Step 2: Verify backup exists**

Confirm backup file at `commands/.do.md.backup.{timestamp}` before any modifications proceed.

**Step 3: Review the diff**

The script outputs a diff showing new entries (+), modified entries (- old / + new), and preserved manual entries (unchanged). Review for correctness.

**Step 4: Confirm or abort**

If diff looks correct: confirm to apply. If unexpected: abort and investigate. With --auto-commit: confirmation skipped.

**Step 5: Post-update validation**

The script validates pipe alignment, header separator rows, consistent column counts, and no orphaned rows. On validation failure: automatic restore from backup. Report error details.

**Gate**: Backup created, all manual entries preserved, markdown validated, diff confirmed. If gate fails, RESTORE from backup.

---

### Phase 4B: UPDATE -- Update Command Files

**Goal**: Update command files with current skill/agent references.

**Constraints**: Command files updated only if they reference outdated/invalid skills; backups created for all modified files; all referenced skills must exist; markdown syntax validated after updates.

**Step 1: Run update script with backup**

```bash
python3 ~/.claude/skills/meta/routing-table-updater/scripts/update_commands.py --commands-dir $HOME/vexjoy-agent/commands --metadata metadata.json --backup
```

**Step 2: Understand the update process**

1. Scan command files for skill invocations and references
2. Identify outdated or invalid references (renamed/removed skills)
3. Update references to match current metadata
4. Create backups for all modified command files
5. Validate updated markdown syntax

**Gate**: Backups created for all modified files, all referenced skills exist, markdown validated.

---

### Phase 5: VERIFY -- Validate Routing Correctness

**Goal**: Final validation of all routing tables.

**Constraints**: All auto-generated entries must have `[AUTO-GENERATED]` markers; no duplicate patterns within same routing table; all referenced skills/agents must exist; complexity values must match Simple/Medium/Complex; overlapping patterns documented with priority rules.

**Step 1: Run validation script**

```bash
python3 ~/.claude/skills/meta/routing-table-updater/scripts/validate.py --target $HOME/vexjoy-agent/commands/do.md
```

**Step 2: Understand verification checks**

1. **Structural**: All routing tables present, headers formatted, pipes aligned
2. **Content**: All auto-generated entries marked, no duplicates, all referenced skills/agents exist
3. **Conflicts**: Overlapping patterns documented, priority rules applied
4. **Integration**: Sample pattern matching tests pass

**Gate**: All checks pass. Task complete ONLY if final gate passes. See `references/error-handling.md` for gate failure recovery.

---

## Examples

See `references/skill-examples.md` for worked examples (new skill created, agent description updated, conflict detection, manual entry preserved).

---

## Batch Mode

When invoked by `pipeline-scaffolder` Phase 4 (INTEGRATE), this skill operates in batch mode to register N skills and 0-1 agents in a single pass.

See `references/batch-mode.md` for batch input format, batch process, and the batch vs single mode comparison table.

---

## Integration

This skill is typically invoked after other creation skills complete:

- **After skill-creator**: New skill created, routing tables need updated entry
- **After skill/agent modification**: Description or trigger changes require routing refresh
- **During repository maintenance**: Periodic sync to catch manual drift
- **After pipeline-scaffolder Phase 3**: N skills created for a domain, all need routing (batch mode)

Invocation by other skills:
```
skill: routing-table-updater
```

The skill reads metadata from all skills and agents but never modifies them. It only writes to `skills/meta/do/SKILL.md`, `skills/meta/do/references/routing-tables.md`, `agents/INDEX.json`, and `commands/*.md` files.

---

## Error Handling

See `references/error-handling.md` for the full error matrix (YAML parse errors, routing conflicts, manual entry overwrites, markdown validation failures) and per-phase gate failure recovery.

---

## References

### Reference Files

- `${CLAUDE_SKILL_DIR}/references/routing-format.md`: /do routing table format specification (table structure, entry formats, ordering rules)
- `${CLAUDE_SKILL_DIR}/references/extraction-patterns.md`: Trigger phrase extraction patterns (regex, keyword maps, complexity inference)
- `${CLAUDE_SKILL_DIR}/references/conflict-resolution.md`: Conflict types, priority rules, severity levels, resolution process
- `${CLAUDE_SKILL_DIR}/references/examples.md`: Real-world examples of routing table updates (new skill, updated agent, conflict detection, manual preservation)
- `${CLAUDE_SKILL_DIR}/references/skill-examples.md`: Worked examples for the 5-phase pipeline (Phase 1-5 walkthroughs)
- `${CLAUDE_SKILL_DIR}/references/batch-mode.md`: Batch mode invocation by pipeline-scaffolder (input format, process, comparison)
- `${CLAUDE_SKILL_DIR}/references/error-handling.md`: Error matrix and per-phase gate failure recovery
