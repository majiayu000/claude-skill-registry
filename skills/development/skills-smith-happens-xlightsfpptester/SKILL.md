---
name: skills-smith-happens-xlightsfpptester
description: 'Activation: /rollback or /rollback <phase>'
---

# Rollback Skill

**Activation**: `/rollback` or `/rollback <phase>`

**Purpose**: Restore the project to a previous phase checkpoint. Archives work from later phases and resets pipeline state. Enables starting over from a known good state.

---

## When to Use

- Specifications were wrong, need to redo from Phase 6
- Implementation went in wrong direction
- Major requirements change requires restart from Discovery
- Testing revealed fundamental issues requiring redesign
- Any situation where "going back" is cleaner than fixing forward

---

## What It Does

1. **Reads closeout files** - Finds checkpoint for target phase
2. **Analyzes impact** - Shows what will be archived
3. **Confirms with human** - Never rolls back without approval
4. **Archives later phases** - Moves (not deletes) work to .claude/archived/
5. **Resets pipeline state** - Restores to target phase complete
6. **Updates curator manifest** - Marks archived entries
7. **Prepares for re-entry** - Ready to start next phase fresh

---

## Usage

Interactive (will ask which phase):
```
/rollback
```

Direct to specific phase:
```
/rollback 5
```

With confirmation:
```
/rollback 5 --confirm
```

---

## Rollback Flow

```
/rollback 5

╔═══════════════════════════════════════════════════════════════════════╗
║  ROLLBACK REQUESTED: Phase 5                                          ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Current State: Phase 8 (Code Review) - in progress                   ║
║  Target State:  Phase 5 (Task Decomposition) - complete               ║
║                                                                        ║
║  ─────────────────────────────────────────────────────────────────────║
║                                                                        ║
║  WILL BE ARCHIVED (moved to .claude/archived/):                       ║
║                                                                        ║
║  Canonical Locations:                                                  ║
║    • specs/auth/                    (3 files)                         ║
║    • specs/database/                (2 files)                         ║
║    • src/services/auth/             (4 files)                         ║
║    • src/components/login/          (3 files)                         ║
║    • tests/unit/services/auth/      (4 files)                         ║
║    • reports/review/                (2 files)                         ║
║                                                                        ║
║  Phase Working Directories:                                            ║
║    • .phase-work/phase-06-specification/                              ║
║    • .phase-work/phase-07-implementation/                             ║
║    • .phase-work/phase-08-review/                                     ║
║                                                                        ║
║  Closeout Files (preserved for reference):                            ║
║    • .claude/closeouts/phase-06.yaml                                  ║
║    • .claude/closeouts/phase-07.yaml                                  ║
║                                                                        ║
║  ─────────────────────────────────────────────────────────────────────║
║                                                                        ║
║  WILL BE PRESERVED:                                                    ║
║                                                                        ║
║    • docs/PRD.md                                                      ║
║    • docs/architecture/                                               ║
║    • .taskmaster/tasks/tasks.json                                     ║
║    • .phase-work/phase-01 through phase-05/                           ║
║    • .claude/closeouts/phase-01 through phase-05.yaml                 ║
║                                                                        ║
║  ─────────────────────────────────────────────────────────────────────║
║                                                                        ║
║  Archive Location:                                                     ║
║    .claude/archived/2025-01-15T14-30-from-phase-08/                   ║
║                                                                        ║
║  After rollback, you will re-enter Phase 6 with:                      ║
║    • Clean specification directory                                    ║
║    • Original tasks.json intact                                       ║
║    • Full closeout history preserved                                  ║
║    • Archived work available for reference                            ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  [Y] Proceed with rollback                                            ║
║  [R] Review archived content first                                    ║
║  [D] Show detailed file list                                          ║
║  [N] Cancel rollback                                                  ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## After Rollback

```
╔═══════════════════════════════════════════════════════════════════════╗
║  ROLLBACK COMPLETE                                                    ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Restored to: Phase 5 (Task Decomposition) - complete                 ║
║                                                                        ║
║  Files archived: 18                                                   ║
║  Directories archived: 6                                               ║
║  Archive location: .claude/archived/2025-01-15T14-30-from-phase-08/  ║
║                                                                        ║
║  Pipeline state reset. Ready to re-enter Phase 6.                     ║
║                                                                        ║
║  ─────────────────────────────────────────────────────────────────────║
║                                                                        ║
║  To reference archived work:                                           ║
║    ls .claude/archived/2025-01-15T14-30-from-phase-08/               ║
║                                                                        ║
║  To continue:                                                          ║
║    Just say "Continue to Phase 6" or run /status                      ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## Archive Structure

```
.claude/archived/
└── 2025-01-15T14-30-from-phase-08/
    ├── manifest.yaml           # What was archived and why
    ├── canonical/              # Files from canonical locations
    │   ├── specs/
    │   │   ├── auth/
    │   │   └── database/
    │   ├── src/
    │   │   ├── services/
    │   │   └── components/
    │   └── tests/
    ├── phase-work/             # Phase working directories
    │   ├── phase-06-specification/
    │   ├── phase-07-implementation/
    │   └── phase-08-review/
    └── closeouts/              # Copies of closeout files
        ├── phase-06.yaml
        └── phase-07.yaml
```

---

## Archive Manifest

`.claude/archived/{timestamp}/manifest.yaml`:

```yaml
rollback:
  from_phase: 8
  to_phase: 5
  timestamp: "2025-01-15T14:30:00Z"
  reason: "Specifications were incorrect, need to redo"  # If provided

archived_phases: [6, 7, 8]

canonical_files:
  - original: "specs/auth/SPEC-001-login.md"
    archived: "canonical/specs/auth/SPEC-001-login.md"
  - original: "src/services/auth/auth.service.ts"
    archived: "canonical/src/services/auth/auth.service.ts"
  # ...

phase_work_directories:
  - original: ".phase-work/phase-06-specification/"
    archived: "phase-work/phase-06-specification/"
  # ...

closeout_files:
  - original: ".claude/closeouts/phase-06.yaml"
    archived: "closeouts/phase-06.yaml"
    note: "Also preserved in original location for history"
  # ...

recovery_instructions: |
  To recover this work:
  1. Copy files from this archive to project root
  2. Update pipeline-state.json manually
  3. Or start fresh and reference these files
```

---

## Rollback Safety

### Never Deleted

- Archived files are MOVED, never deleted
- Closeout files remain in original location (copied to archive)
- Git history is preserved (files are archived, not git-removed)

### Can Recover

- All archived work is in `.claude/archived/`
- Each archive has timestamp and manifest
- Copy files back if needed

### Restrictions

- Cannot rollback to Phase 0 (before ideation)
- Cannot rollback past the oldest closeout file
- Rollback requires human confirmation

---

## Related Skills

- `/close-phase` - Create checkpoint before rollback target
- `/status` - See current phase and available checkpoints
- `/archive list` - List all archived rollbacks

---

## Implementation

Creates: `rollback-agent` (invoked by this skill)

The skill:
1. Reads pipeline-state.json for current phase
2. Reads closeout files to find available checkpoints
3. Validates target phase has a closeout
4. Reads curator-manifest.json for files to archive
5. Presents impact analysis
6. On confirmation, moves files to .claude/archived/
7. Resets pipeline-state.json
8. Updates curator-manifest.json
