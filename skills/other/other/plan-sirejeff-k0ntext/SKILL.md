---
description: RPI Plan Phase - Create chunk-based todolists from research chunks for rpi-implement consumption
---

# Context Engineering: Plan Phase (Enhanced)

When invoked, create a detailed implementation plan with chunk-based todolists:

## Key Innovation: Inter-Phase Awareness

This plan phase **KNOWS**:
- RPI-Research structured chunks specifically for sequential processing
- RPI-Implement will read each CHUNK-Pn as an atomic implementation unit
- Each CHUNK-Pn todolist must be independently executable
- Chunk dependencies must be explicit for proper execution ordering

## Prerequisites
- Research document exists at `.claude/research/active/[feature]_research.md`
- Research document contains chunk manifest
- If not found, run `/context-eng:research $ARGUMENTS` first

## Chunk Processing Loop

```
FOR each CHUNK-Rn in research_chunks:
  1. Read CHUNK-Rn content
  2. Create CHUNK-Pn todolist:
     - Define atomic action items
     - Specify file:line for each action
     - Assign test for each action
     - Document chunk-specific rollback
  3. Mark CHUNK-Rn status as PLANNED
  4. Define CHUNK-Pn dependencies
  5. Proceed to next CHUNK-R(n+1)
END LOOP
```

## Process

1. **Load Research Document**
   - Read the research document for $ARGUMENTS
   - Extract chunk manifest
   - Extract per-chunk files and line numbers

2. **For Each Research Chunk (CHUNK-Rn):**
   
   a. **Analyze chunk content:**
      - Files explored with line numbers
      - Code flow analysis
      - Dependencies identified
   
   b. **Create CHUNK-Pn todolist:**
      ```markdown
      | # | Action | File | Lines | Risk | Test | Status |
      |---|--------|------|-------|------|------|--------|
      | 1 | [Action] | file.ext | XXX | LOW | test_x | ⏳ |
      ```
   
   c. **Define per-todo details:**
      - Current code snippet
      - Proposed change
      - Test to run after
   
   d. **Mark research chunk as PLANNED**
   
   e. **Document chunk dependencies**

3. **Create Chunk Dependency Graph**
   ```
   CHUNK-P1 → CHUNK-P2 → CHUNK-P3
              ↓
   CHUNK-P4  CHUNK-P5
   ```

4. **Generate Inter-Phase Contract**
   ```
   EXPECTED_CONSUMER: rpi-implement
   CHUNK_PROCESSING_ORDER: dependency-ordered
   MARK_AS_IMPLEMENTED_WHEN: all chunk todos complete
   UPDATE_RESEARCH_STATUS: true
   ```

5. **Create Plan Document**
   - Save to `.claude/plans/active/[feature]_plan.md`
   - Include chunk manifest
   - Include per-chunk todolists
   - Include verification checklist

## Plan Format (Chunk-Based)

```markdown
# Implementation Plan: [Feature]

## Chunk Manifest
| Chunk ID | From Research | Status | Todos | Dependencies | Ready |
|----------|---------------|--------|-------|--------------|-------|
| CHUNK-P1 | CHUNK-R1 | READY | 4 | None | ✅ |
| CHUNK-P2 | CHUNK-R2 | READY | 5 | CHUNK-P1 | ⏳ |

## CHUNK-P1: [Domain] (from CHUNK-R1)

**Status:** READY
**Dependencies:** None
**Update Research When Complete:** Mark CHUNK-R1 as IMPLEMENTED

### Todolist
| # | Action | File | Lines | Risk | Test | Status |
|---|--------|------|-------|------|------|--------|
| 1 | [Action] | file.ext | XXX | LOW | test_x | ⏳ |

### Todo 1: [Action Name]
**File:** path/to/file.ext
**Lines:** X-Y
**Current:** [code block]
**Proposed:** [code block]
**Test:** [command]

### Chunk Completion Criteria
- [ ] All todos complete
- [ ] Update CHUNK-R1 status
- [ ] Proceed to dependent chunks

## Inter-Phase Contract
[contract for rpi-implement]

## Rollback (Per Chunk)
- CHUNK-P1: git revert [hash]
```

## Context Budget
- Research doc: 20k tokens
- Plan creation: 15k tokens
- Total: 35k tokens (17.5%)

## Next Step
After approval, run `/context-eng:implement $ARGUMENTS`

RPI-Implement will:
1. Load chunk manifest
2. Process chunks in dependency order
3. Execute todos atomically per chunk
4. Mark chunks as IMPLEMENTED
5. Update research document status
