---
name: kata-move-phase
description: Move a phase between milestones or reorder phases within a milestone. Triggers include "move phase", "move phase to milestone", "reorder phase", "reorder phases".
metadata:
  version: "0.1.0"
allowed-tools: Read Write Bash
---
<objective>
Move a pending phase to a different milestone or reorder phases within a milestone.

Purpose: Enable flexible phase reorganization (cross-milestone moves and within-milestone reordering).
Output: Phase moved/reordered, directories renamed, ROADMAP.md updated, STATE.md updated, git commit as historical record.

**Supported operations:**
- Cross-milestone move: `/kata-move-phase 3 to v1.6.0`
- Reorder within milestone: `/kata-move-phase 3 before 1` or `/kata-move-phase 3 after 1`
</objective>

<execution_context>
@.planning/ROADMAP.md
@.planning/STATE.md
</execution_context>

<process>

<step name="parse_arguments">
Parse the command arguments. First arg is always the phase number (integer).

**Detect operation type from second arg:**
- `"to"` + milestone version → cross-milestone move
- `"before"` or `"after"` + target phase number → reorder within milestone

**Cross-milestone move:**
- `/kata-move-phase 3 to v1.6.0`

**Reorder within milestone:**
- `/kata-move-phase 3 before 1` → Phase 3 takes position 1, everything shifts up
- `/kata-move-phase 3 after 1` → Phase 3 takes position 2, phases 2+ shift up

**Validation:**
- If no arguments or missing second arg:

```
ERROR: Phase number and operation required
Usage: /kata-move-phase <phase> to <milestone>
       /kata-move-phase <phase> before|after <position>
```

Exit.

- If second arg is not "to", "before", or "after":

```
ERROR: Invalid operation "{arg}"
Expected: to, before, or after
```

Exit.

Store: PHASE_NUM, OPERATION (move|reorder), and either TARGET_MILESTONE or POSITION+TARGET_POSITION.
</step>

<step name="load_state">
Load project state:

```bash
cat .planning/STATE.md 2>/dev/null
cat .planning/ROADMAP.md 2>/dev/null
```

Parse current milestone version from ROADMAP.md (the milestone marked "In Progress").
</step>

<step name="validate_phase_exists">
Verify the phase exists in ROADMAP.md and find its directory:

1. Search for `#### Phase {N}:` heading within the current milestone
2. Use universal phase discovery (search active/pending/completed with padded and unpadded names, fallback to flat)
3. If not found: `ERROR: Phase {N} not found in roadmap` + list available phases. Exit.
</step>

<step name="validate_phase_movable">
Verify the phase can be moved/reordered:

1. **Must be in pending/** (not active or completed). If not: `ERROR: Phase {N} is in {state}/ and cannot be moved`. Exit.
2. **Must not have SUMMARY.md files** (no executed plans). If found: `ERROR: Phase {N} has completed work`. Exit.
</step>

<step name="validate_target_milestone">
**Cross-milestone move only.** Skip for reorder operations.

1. Target milestone heading must exist in ROADMAP.md. If not: `ERROR: Milestone {target} not found` + list available. Exit.
2. Target must differ from source. If same: `ERROR: Phase already in {milestone}. Use before/after to reorder.` Exit.
</step>

<step name="validate_reorder_target">
**Reorder only.** Skip for cross-milestone moves.

Validate the target position phase exists in the same milestone:

1. Target position phase must exist in ROADMAP.md within the current milestone
2. Target can be any state (active, pending, completed) since we're reordering the roadmap listing
3. The phase being moved must be pending (already validated in validate_phase_movable)

Calculate the effective target position:
- `before N` → target position = N (phase takes position N, everything at N+ shifts up)
- `after N` → target position = N+1 (phase takes position N+1, everything at N+1+ shifts up)

If target position phase not found:

```
ERROR: Phase {target_position} not found in current milestone
Available phases: [list phase numbers]
```

Exit.
</step>

<step name="confirm_reorder">
**Reorder only.** Skip for cross-milestone moves.

Show the planned reorder and wait for confirmation:

```
Reordering Phase {N}: {Name}

Current order:
  Phase 1: {name}
  Phase 2: {name}
  Phase 3: {name}

New order:
  Phase 1: {name}  (was Phase 3)
  Phase 2: {name}  (was Phase 1)
  Phase 3: {name}  (was Phase 2)

This will renumber all phase directories and update ROADMAP.md.

Proceed? (y/n)
```

Wait for confirmation.
</step>

<step name="reorder_roadmap">
**Reorder only.** Skip for cross-milestone moves.

Update ROADMAP.md to reflect the new phase order:

1. Extract all phase sections within the current milestone
2. Remove the moving phase section from its current position
3. Insert it at the target position
4. Renumber ALL phase headings in the milestone sequentially (1, 2, 3, ...)
5. Update all references within the milestone:
   - Phase headings: `#### Phase {old}:` -> `#### Phase {new}:`
   - Phase list entries
   - Progress table rows
   - Plan references: `{old}-01:` -> `{new}-01:`
   - Dependency references: `Depends on: Phase {old}` -> `Depends on: Phase {new}`
   - Decimal phase references if any

Write updated ROADMAP.md.
</step>

<step name="renumber_all_directories">
**Reorder only.** Skip for cross-milestone moves.

Rename ALL phase directories in the milestone to match new numbering. Use a three-pass approach to avoid collision:

1. **Pass 1:** Move the reordering phase to a temp name (`tmp-{slug}`)
2. **Pass 2:** Renumber all remaining phases sequentially. Process order matters:
   - Phases shifting down (higher->lower): process lowest first
   - Phases shifting up (lower->higher): process highest first
   - For each: find across state subdirectories, rename directory and internal files
3. **Pass 3:** Move temp directory to its final numbered position, rename internal files

Handle decimal phases: they follow their parent integer phase and renumber accordingly.
</step>

<step name="calculate_destination_number">
**Cross-milestone move only.** Skip for reorder operations.

Find next phase number in target milestone: parse `#### Phase N:` headings, take highest + 1 (or 1 if empty). Format as two-digit padded.
</step>

<step name="confirm_move">
**Cross-milestone move only.** Skip for reorder operations.

Show: source milestone, target milestone, new phase number, directory rename, number of phases to renumber in source. Wait for confirmation.
</step>

<step name="remove_from_source_milestone">
**Cross-milestone move only.** Skip for reorder operations.

Remove phase section from source milestone in ROADMAP.md and renumber remaining phases to close the gap. Follow the same renumbering approach as kata-remove-phase:
- Phase headings, list entries, progress table rows
- Plan references (`{old}-01:` -> `{new}-01:`)
- Dependency references (`Depends on: Phase {old}` -> `Phase {new}`)
- Decimal phase references
</step>

<step name="add_to_target_milestone">
**Cross-milestone move only.** Skip for reorder operations.

Insert phase section into target milestone in ROADMAP.md at the calculated destination number. Preserve goal, requirements, success criteria. Remove or note cross-milestone dependency references that no longer apply.
</step>

<step name="rename_phase_directory">
**Cross-milestone move only.** Skip for reorder operations (handled by renumber_all_directories).

Rename phase directory to new number within pending/. Rename all files inside (PLAN.md, RESEARCH.md, etc.) to match. Handle decimal phases (N.1, N.2) by moving them with the parent, renumbering to NEW_NUM.1, NEW_NUM.2.
</step>

<step name="renumber_source_directories">
**Cross-milestone move only.** Skip for reorder operations (handled by renumber_all_directories).

Renumber directories of phases that shifted in the source milestone. Process ascending order (for downward shifts). For each: find across state subdirectories, rename directory and internal files within same state.
</step>

<step name="update_state">
Update STATE.md:

**For cross-milestone move:**

1. Add roadmap evolution note:

```markdown
- **Phase {N} moved from {source_milestone} to {target_milestone}** as Phase {NEW_NUM}
```

2. Update total phase count if the source milestone is the current milestone
3. Recalculate progress percentage

**For reorder:**

1. Add roadmap evolution note:

```markdown
- **Phase {N} reordered {before|after} Phase {M}** in {milestone}
```

2. Phase count unchanged (same milestone, same phases)

**Both operations:** Update REQUIREMENTS.md traceability if requirements reference affected phases. Update phase numbers in traceability table for all renumbered phases.
</step>

<step name="commit">
Check planning config:

```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

**If `COMMIT_PLANNING_DOCS=false`:** Skip git operations

**If `COMMIT_PLANNING_DOCS=true` (default):**

```bash
git add .planning/
# Cross-milestone move:
git commit -m "chore: move phase {N} to {target_milestone}"
# Reorder:
git commit -m "chore: reorder phase {N} {before|after} {M}"
```
</step>

<step name="completion">
Present completion summary showing: operation performed, directories renamed, phases renumbered, files updated, commit message. Then offer next actions: `/kata-track-progress`, continue current phase, review roadmap.
</step>

</process>

<anti_patterns>

- Don't move active or completed phases (only pending phases can be moved/reordered)
- Don't move phases with executed plans (SUMMARY.md exists)
- Don't move to the same milestone (use reorder instead)
- Don't reorder to the same position (no-op)
- Don't forget decimal phases (they move with parent integer phase)
- Don't commit if commit_docs is false
- Don't leave gaps in phase numbering after move or reorder
- Don't modify phases outside the source and target milestones
- Don't rename directories without the two-pass temp approach (avoids collisions during reorder)

</anti_patterns>

<edge_cases>

**Phase has PLAN.md files but no SUMMARY.md:**
- Allowed. Rename plan files inside the directory as part of the move/reorder.
- Update plan frontmatter phase references.

**Target milestone is empty (no phases):**
- First phase becomes Phase 1.
- `calculate_destination_number` handles this (NEW_NUM=1 when HIGHEST is empty).

**Last phase in source milestone removed:**
- No renumbering needed in source milestone.
- Source milestone section in ROADMAP.md still has its heading.

**Decimal phases under moved integer phase:**
- Find all decimal phases (N.1, N.2) belonging to the moved integer phase.
- Move them together with the parent.
- Renumber to NEW_NUM.1, NEW_NUM.2 at destination.

**Phase directory doesn't exist yet:**
- Phase may be in ROADMAP.md but directory not created.
- Skip directory operations, proceed with ROADMAP.md updates only.
- Note in completion summary: "No directory to move (phase not yet created)"

**Reorder: moving to adjacent position:**
- `before N+1` or `after N-1` when phase is at position N is a no-op.
- Detect and report: "Phase {N} is already at that position."

**Reorder: only two phases in milestone:**
- Swap positions. Both directories and all references renumbered.

</edge_cases>

<success_criteria>
**Cross-milestone move** is complete when:

- [ ] Source phase validated as pending/unstarted
- [ ] Target milestone validated as existing and different from source
- [ ] Phase section removed from source milestone in ROADMAP.md
- [ ] Remaining source phases renumbered to close gap
- [ ] Phase section added to target milestone with correct number
- [ ] Phase directory renamed to match new number
- [ ] Files inside directory renamed ({old}-NN-PLAN.md -> {new}-NN-PLAN.md)
- [ ] Decimal phases moved with parent (if any)
- [ ] Source directories renumbered (if phases shifted)
- [ ] STATE.md updated with roadmap evolution note
- [ ] Changes committed with descriptive message
- [ ] No gaps in phase numbering at source or destination

**Reorder** is complete when:

- [ ] Phase validated as pending/unstarted
- [ ] Target position validated as existing in same milestone
- [ ] Phase sections reordered in ROADMAP.md
- [ ] All phases in milestone renumbered sequentially
- [ ] All phase directories renamed (two-pass temp approach)
- [ ] Files inside directories renamed to match new numbers
- [ ] Decimal phases renumbered with parent (if any)
- [ ] STATE.md updated with roadmap evolution note
- [ ] Changes committed with descriptive message
- [ ] No gaps in phase numbering

**Both operations:** User informed of all changes.
</success_criteria>
