---
name: docs-update
description: Verify and update derived documentation
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - AskUserQuestion
model: sonnet
---

# Update Documentation

Verify derived documentation against canonical sources and prompt for updates.

## Usage

```
/docs-update
```

## Steps

### 1. Read Canonical Sources

```bash
echo "Reading canonical sources..."
cat .claude/rules/game-state.md
```

### 2. Extract Type Definitions

Parse the following structures from game-state.md:
- Player struct (CANONICAL)
- GameState struct
- State transition rules
- Invariants

### 3. Compare and Identify Mismatches

Compare `docs/api/types.md` with canonical source:

**Check Player section**:
- Verify all 6 fields present: id, position, velocity, lives, lapsCompleted, isEliminated
- Check field comments match game-state.md
- Check invariants are consistent

**Check other types**:
- GridPoint, GridVector, GameState, Track, CellType, GamePhase
- Note any differences found

**If mismatches found**:
- Prompt user with specific differences
- Ask: "Update docs/api/types.md to match canonical? [Y/n]"
- If yes, make the updates manually or guide user

### 4. Verify CLAUDE.md Accuracy

Check that CLAUDE.md references match actual files:

```bash
# Count rules
ACTUAL_RULES=$(ls .claude/rules/*.md | wc -l | tr -d ' ')
LISTED_RULES=$(grep -c '\.md.*-' CLAUDE.md)

if [ "$ACTUAL_RULES" -ne "$LISTED_RULES" ]; then
    echo "⚠️  CLAUDE.md rule list needs updating"
    echo "   Actual: $ACTUAL_RULES, Listed: $LISTED_RULES"
fi

# Count skills
ACTUAL_SKILLS=$(ls -d .claude/skills/*/ | wc -l | tr -d ' ')
LISTED_SKILLS=$(grep -c '^| `/.*`' CLAUDE.md)

if [ "$ACTUAL_SKILLS" -ne "$LISTED_SKILLS" ]; then
    echo "⚠️  CLAUDE.md skill table needs updating"
    echo "   Actual: $ACTUAL_SKILLS, Listed: $LISTED_SKILLS"
fi
```

### 5. Update Canonical References

Ensure all references to canonical sources are correct:

```bash
# Find files referencing Player
grep -l "Player" .claude/rules/*.md docs/**/*.md | while read file; do
    # Check if it has canonical marker
    if ! grep -q "CANONICAL\|canonical" "$file"; then
        # Should reference game-state.md
        if ! grep -q "game-state.md" "$file"; then
            echo "⚠️  $file mentions Player but doesn't reference canonical source"
        fi
    fi
done
```

### 6. Verify Consistency

Run docs-verify to check results:

```bash
/docs-verify
```

### 7. Report Changes

```
Documentation Updated
=====================
Date: [timestamp]

Files checked:
  ✓ .claude/rules/game-state.md (canonical source)
  ✓ docs/api/types.md (derived)
  ✓ .claude/rules/architecture.md (references)
  ✓ CLAUDE.md (index)

Changes made:
  → Updated timestamp in types.md
  → Verified Player definition consistency
  → [Any other changes]

Verification: [Pass/Fail]
  [Results from /docs-verify]
```

## What Gets Updated

**Automatically**:
- Timestamps in types.md
- Canonical reference markers
- Cross-reference checks

**Manually (prompts for confirmation)**:
- Type definitions if canonical changed
- CLAUDE.md if counts mismatch
- Architecture.md if references broken

## Example Output

```
Reading canonical sources...
✓ .claude/rules/game-state.md read

Checking docs/api/types.md...
✓ Player definition matches canonical
✓ All 6 fields present and correct
→ Updating timestamp

Verifying CLAUDE.md...
✓ Rule count matches: 8/8
✓ Skill count matches: 19/19

Checking cross-references...
✓ All references valid

Documentation Updated
=====================

Files modified:
  - docs/api/types.md (timestamp updated)

Source:
  - .claude/rules/game-state.md

Verification: PASSED ✓

Timestamp: 2026-01-25 18:45:00
```

## Use Cases

**After changing types in code**:
```
1. Update game-state.md with new type definition
2. Run /docs-update to regenerate derived docs
3. Run /docs-verify to confirm consistency
```

**After adding new skill**:
```
1. Create skill in .claude/skills/
2. Run /docs-update to check counts
3. Manually add skill to CLAUDE.md table if needed
```

**Periodic maintenance**:
```
/docs-update
→ Refresh timestamps and verify all derived docs
```

## Notes

- Always reads from game-state.md as source of truth
- Non-destructive: prompts before major changes
- Safe to run anytime
- Use with /docs-verify for full documentation maintenance
- Does NOT modify canonical sources (only derived docs)
