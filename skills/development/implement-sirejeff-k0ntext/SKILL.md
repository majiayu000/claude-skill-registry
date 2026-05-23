---
description: RPI Implement Phase - Execute chunk-based todolists with atomic changes and continuous testing
---

# Context Engineering: Implement Phase (Enhanced)

When invoked, execute the approved implementation plan chunk by chunk:

## Key Innovation: Inter-Phase Awareness

This implement phase **KNOWS**:
- RPI-Plan structured chunks for atomic implementation
- Each CHUNK-Pn contains a complete, ordered todolist
- Chunk dependencies dictate execution order
- Marking chunks complete updates both plan AND research documents
- Context reset is needed after every 3 chunks or 35% utilization

## Prerequisites
- Approved plan at `.claude/plans/active/[feature]_plan.md`
- Plan contains chunk manifest with chunk-todolists
- If not found, run `/context-eng:plan $ARGUMENTS` first

## Golden Rules

```
ONE CHUNK → COMPLETE TODOLIST → MARK DONE → NEXT CHUNK
ONE TODO → ONE CHANGE → ONE TEST → ONE COMMIT
```

## Chunk-Based Implementation Loop

```
FOR each CHUNK-Pn in dependency_order:
  IF dependencies_complete:
    1. Load CHUNK-Pn todolist
    
    FOR each TODO in todolist:
      a. Make atomic change
      b. Run todo-specific test
      c. If PASS: commit, mark TODO ✅
      d. If FAIL: STOP, investigate, fix
    END TODO LOOP
    
    2. Update chunk documentation
    3. Mark CHUNK-Pn as IMPLEMENTED
    4. Update research CHUNK-Rn to IMPLEMENTED
    
    IF chunks_processed % 3 == 0 OR context > 35%:
      Context reset (save progress, reload plan)
    END IF
    
    5. Proceed to next ready chunk
  END IF
END CHUNK LOOP
```

## Process

1. **Load Plan Document**
   - Read `.claude/plans/active/[feature]_plan.md`
   - Extract chunk manifest and dependency graph
   - Verify plan status is APPROVED

2. **Determine Execution Order**
   Based on chunk dependency graph:
   - Independent chunks first (parallel capable)
   - Dependent chunks in order
   - Final chunks (e.g., test additions)

3. **For Each Chunk (in dependency order):**
   
   a. **Check dependencies complete**
   
   b. **Execute each todo atomically:**
      - Make single change
      - Run specified test
      - If pass: commit with message
      - If fail: STOP, investigate, fix
   
   c. **After all todos complete:**
      - Mark CHUNK-Pn as IMPLEMENTED
      - Update CHUNK-Rn in research to IMPLEMENTED
      - Commit chunk documentation updates
   
   d. **Context management:**
      - After every 3 chunks: reload plan
      - If >35% utilization: save, compact, continue

4. **Run Full Test Suite**
   After all chunks complete

5. **Documentation Updates (MANDATORY)**
   - Check `CODE_TO_WORKFLOW_MAP.md` for affected workflows
   - Update workflow files with new line numbers
   - Update function signatures if changed

6. **Context Reset (Every 3 Chunks)**
   - Update chunk progress in plan
   - Re-read plan document
   - Verify scope alignment
   - Compact if >35% utilization

7. **Finalize**
   - Move plan to `.claude/plans/completed/`
   - Move research to `.claude/research/completed/`
   - Run `/context-eng:validate` to verify

## Chunk Status Updates

### Update Plan Document
```markdown
| Chunk | Status | Todos Done | Commit | Research Updated |
|-------|--------|------------|--------|------------------|
| P1 | ✅ IMPLEMENTED | 4/4 | abc123 | ✅ R1 |
| P2 | ▶️ IMPLEMENTING | 2/5 | - | - |
```

### Update Research Document
Mark each CHUNK-Rn status:
- FOUND → COMPLETE → PLANNED → **IMPLEMENTED**

## Error Handling

| Error Type | Response |
|------------|----------|
| Syntax Error | STOP. Fix immediately in same todo. |
| Import Error | Check file paths, verify imports. |
| Test Failure | Do NOT add more code. Investigate first. |
| 3+ Failures in chunk | Mark chunk BLOCKED, try next independent chunk. |
| 3+ Chunks blocked | STOP. Start new session. |

## Commit Format

Per-todo:
```
feat(chunk-Pn): Todo N - description
Implements: [feature] chunk N
```

Per-chunk completion:
```
feat(chunk-Pn): Complete chunk - [domain]
Completes: CHUNK-Pn, Updates: CHUNK-Rn
```

## Context Budget
- Plan: 15k tokens
- Active code (per chunk): ~10k tokens
- Test results (per chunk): ~5k tokens
- Max active (3 chunks): ~45k tokens (22.5%)
