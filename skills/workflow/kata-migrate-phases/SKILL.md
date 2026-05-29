---
name: kata-migrate-phases
description: Migrate phase directories to globally sequential numbering, fixing duplicate numeric prefixes across milestones. Triggers include "migrate phases", "fix phase numbers", "renumber phases", "phase collision", "fix phase collisions", "fix duplicate phases", "phase numbering migration".
metadata:
  version: "0.1.0"
allowed-tools: Read Write Bash
---
<objective>
Detect and fix duplicate phase numeric prefixes caused by per-milestone numbering. Migrates all phase directories to globally sequential numbering.

Projects with multiple milestones may have colliding prefixes (e.g., `01-foundation` from v0.1.0 and `01-setup` from v0.2.0 both in `completed/`). This causes `find ... -name "01-*" | head -1` to return the wrong directory.
</objective>

<context>
@.planning/STATE.md
@.planning/ROADMAP.md
</context>

<process>

<step name="detect_collisions">

Scan all phase directories for duplicate numeric prefixes:

```bash
DUPES=$(for state in active pending completed; do
  ls .planning/phases/${state}/ 2>/dev/null
done | grep -oE '^[0-9]+' | sort -n | uniq -d)

# Also check flat directories (unmigrated projects)
FLAT_DUPES=$(ls .planning/phases/ 2>/dev/null | grep -E '^[0-9]' | grep -oE '^[0-9]+' | sort -n | uniq -d)

ALL_DUPES=$(echo -e "${DUPES}\n${FLAT_DUPES}" | sort -nu | grep -v '^$')
echo "Duplicate prefixes: ${ALL_DUPES:-none}"
```

If no duplicates found:

```
No phase prefix collisions detected. All phase directories have unique numeric prefixes.
```

Exit.
</step>

<step name="validate_environment">

Read ROADMAP.md and STATE.md. Confirm project is active:

```bash
[ -f .planning/ROADMAP.md ] || { echo "ERROR: No ROADMAP.md found. Not a Kata project."; exit 1; }
[ -f .planning/STATE.md ] || { echo "ERROR: No STATE.md found. Not a Kata project."; exit 1; }
```

Display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► PHASE MIGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ Duplicate prefixes detected: [list]
◆ Building chronology from ROADMAP.md...
```
</step>

<step name="build_milestone_chronology">

Parse ROADMAP.md to build globally sequential phase numbering. Milestones appear in chronological order.

**Completed milestones:** Each `<details>` block contains phase lists. Parse phases in document order.

**Current milestone:** Parse `#### Phase N:` headings from the active section.

Build a chronology array. Each entry: `{global_seq} {phase_name}` where `phase_name` is the slug from the phase heading (e.g., "foundation", "api-endpoints").

```bash
GLOBAL_SEQ=0
CHRONOLOGY=""

# Parse all "Phase N: name" lines from ROADMAP.md in document order.
# Completed milestones appear in <details> blocks; current milestone uses #### headings.
# Both formats contain "Phase N: name" — grep catches all.
while IFS= read -r line; do
  name=$(echo "$line" | grep -oE 'Phase [0-9.]+: .+' | sed 's/Phase [0-9.]*: //' | sed 's/\*\*$//' | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
  if [ -n "$name" ]; then
    CHRONOLOGY="${CHRONOLOGY}${GLOBAL_SEQ} ${name}\n"
    GLOBAL_SEQ=$((GLOBAL_SEQ + 1))
  fi
done < <(grep -E 'Phase [0-9.]+:' .planning/ROADMAP.md)
```

Decimal phases (2.1, 2.2) get sequential integer numbers after their parent. Document order determines sequence.

Display: `Chronology ([N] phases): 00 → foundation, 01 → api-endpoints, ...`
</step>

<step name="map_directories_to_phases">

Match each phase name from the chronology to its existing directory. Search across `active/`, `pending/`, `completed/`, and flat fallback.

For each chronology entry `{seq} {name}`:
1. Find directories whose slug matches `{name}` across all states
2. If multiple matches, use the one whose numeric prefix matches the original milestone-local number
3. Build mapping: `STATE/OLD_DIR → STATE/NEW_PREFIX-SLUG`

Strip numeric prefix from each directory name to get slug, compare against chronology name. Build `MAPPING` as newline-delimited entries: `STATE/OLD_DIR → PADDED-SLUG`.

Display the full mapping table.
</step>

<step name="present_migration_plan">

Display the rename table:

```
Migration Plan:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  completed/01-foundation      → completed/00-foundation
  completed/02-api-endpoints   → completed/01-api-endpoints
  completed/01-setup           → completed/02-setup
  ...
  active/01-current-work       → active/15-current-work

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: [N] directories to rename
```

Use AskUserQuestion:
- header: "Migration"
- question: "Rename [N] directories to globally sequential numbers?"
- options:
  - "Proceed" — Execute all renames
  - "Cancel" — Abort migration

If cancelled, exit with "Migration cancelled."
</step>

<step name="execute_renames">

Two-pass approach to avoid mid-rename collisions (established pattern from `kata-move-phase`):

**Pass 1:** Rename all directories to temporary names: `mv OLD tmp-{seq}-{slug}`

**Pass 2:** Rename from temporary to final: `mv tmp-{seq}-{slug} {padded}-{slug}`

For active/pending phases in Pass 2, also rename internal files (`*-PLAN.md`, `*-RESEARCH.md`, `*-CONTEXT.md`, `*-SUMMARY.md`) by replacing the old phase prefix with the new padded prefix: `sed "s/^[0-9.]*-/${PADDED}-/"`.

Completed phase internal files left unchanged. Wildcard lookup (`*-PLAN.md`) handles them.

Display:
```
◆ Pass 1: Renamed [N] directories to temporary names
◆ Pass 2: Renamed [N] directories to final names
◆ Active/pending internal files updated: [count]
```
</step>

<step name="update_documentation">

**Update ROADMAP.md current milestone phase numbers:**

For the current (non-archived) milestone section, update `#### Phase N:` headings to use new global numbers. Match phase names to chronology to determine correct new number.

**Update STATE.md current position:**

Update the current phase reference to use the new global number. Find the line referencing the active phase and update its number.

**Leave historical `<details>` blocks unchanged.** They are archived records. Milestone archive files in `.planning/milestones/` are authoritative.

Display:

```
◆ Updated ROADMAP.md current milestone phase numbers
◆ Updated STATE.md current position
```
</step>

<step name="verify">

Re-run collision detection:

```bash
DUPES=$(for state in active pending completed; do
  ls .planning/phases/${state}/ 2>/dev/null
done | grep -oE '^[0-9]+' | sort -n | uniq -d)

FLAT_DUPES=$(ls .planning/phases/ 2>/dev/null | grep -E '^[0-9]' | grep -oE '^[0-9]+' | sort -n | uniq -d)

ALL_DUPES=$(echo -e "${DUPES}\n${FLAT_DUPES}" | sort -nu | grep -v '^$')
```

If clean:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► MIGRATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ [N] directories renamed to globally sequential numbers
✓ No duplicate prefixes remain
✓ ROADMAP.md and STATE.md updated
```

If duplicates remain: report as error with details.
</step>

<step name="commit">

Check planning config:

```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

**If `COMMIT_PLANNING_DOCS=false`:** Skip git operations.

**If `COMMIT_PLANNING_DOCS=true` (default):**

```bash
git add .planning/phases/ .planning/ROADMAP.md .planning/STATE.md
git commit -m "$(cat <<'EOF'
chore: migrate phase directories to globally sequential numbering
EOF
)"
```
</step>

</process>

<anti_patterns>
- Don't rename completed phase internal files (wildcard lookup handles them, reduces risk)
- Don't modify historical `<details>` blocks in ROADMAP.md (archived records)
- Don't rename one directory at a time without temp pass (causes mid-rename collisions)
- Don't ask per-directory confirmation (impractical for 30+ phases)
- Don't run migration on projects with no collisions (detect and exit early)
</anti_patterns>

<success_criteria>
- [ ] Duplicate phase prefixes detected across all state directories
- [ ] Chronology built from ROADMAP.md in document order
- [ ] Migration plan displayed with full rename table
- [ ] User confirmation obtained before any renames
- [ ] Two-pass rename executed without collisions
- [ ] Active/pending internal files renamed to match new prefix
- [ ] Completed phase internal files left unchanged
- [ ] ROADMAP.md current milestone phase numbers updated
- [ ] STATE.md current position updated
- [ ] Historical `<details>` blocks unchanged
- [ ] Verification confirms no remaining collisions
- [ ] Changes committed (if commit_docs enabled)
- [ ] Idempotent: re-run on clean project exits with "no collisions"
</success_criteria>
