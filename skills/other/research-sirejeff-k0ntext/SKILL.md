---
description: RPI Research Phase - Systematic codebase exploration with parallel agents and chunked output
---

# Context Engineering: Research Phase (Enhanced)

When invoked, perform systematic codebase exploration using parallel agents:

## Key Innovation: Inter-Phase Awareness

This research phase **KNOWS** how RPI-Plan will consume its output:
- Output structured into research chunks (CHUNK-R1, CHUNK-R2, etc.)
- Each chunk is self-contained with files, dependencies, and status
- RPI-Plan will create a CHUNK-Pn todolist per CHUNK-Rn
- Chunk manifest enables sequential processing by RPI-Plan

## Process

1. **Initialize Research Document**
   - Create `.claude/research/active/[feature]_research.md`
   - Use template from `.claude/research/RESEARCH_TEMPLATE.md`

2. **Spawn Parallel Agents (3-5 agents)**
   
   ```
   Agent 1: API/Route Entry Points       → CHUNK-R1
   Agent 2: Business Logic & Models      → CHUNK-R2
   Agent 3: Database/Storage Layer       → CHUNK-R3
   Agent 4: External Integrations        → CHUNK-R4
   Agent 5: Test Coverage Analysis       → CHUNK-R5
   ```
   
   Each agent receives:
   - Feature name and objective
   - Assigned domain
   - Required output format (chunk structure)
   - Line number requirement for all file references

3. **Per-Agent Chunk Output**
   Each agent produces a self-contained chunk:
   ```markdown
   ## CHUNK-Rn: [Domain]
   **Status:** COMPLETE
   **Parallel Agent:** Agent N
   **Ready for Planning:** Yes
   
   ### Files Explored
   | File | Lines | Key Findings |
   
   ### Code Flow Analysis
   [call chain with file:line refs]
   
   ### Dependencies (This Chunk)
   - External: [APIs]
   - Internal: [services]
   ```

4. **Aggregate Chunk Results**
   - Create chunk manifest table
   - Combine all agent outputs
   - Verify all chunks are COMPLETE

5. **Generate Inter-Phase Contract**
   ```
   EXPECTED_CONSUMER: rpi-plan
   CHUNK_PROCESSING_ORDER: sequential (R1 → R2 → R3 → R4 → R5)
   MARK_AS_PLANNED_WHEN: chunk todolist created
   REQUIRED_OUTPUT: CHUNK-Pn per CHUNK-Rn
   ```

6. **Generate Summary**
   - 150-word summary for Plan phase
   - Reference key files from each chunk
   - Recommend approach

## Chunk Manifest Format (Required)

```markdown
| Chunk ID | Domain | Status | Files | Ready for Planning |
|----------|--------|--------|-------|-------------------|
| CHUNK-R1 | API/Routes | COMPLETE | 3 | ✅ |
| CHUNK-R2 | Business Logic | COMPLETE | 4 | ✅ |
| CHUNK-R3 | Database | COMPLETE | 2 | ✅ |
| CHUNK-R4 | External | COMPLETE | 1 | ✅ |
| CHUNK-R5 | Tests | COMPLETE | 3 | ✅ |
```

## Context Budget
- Target: 25% of 200k tokens (50k)
- Per-agent budget: ~10k tokens each
- Compaction: After each agent returns
- Final output: ~20k tokens (research doc only)

## Output
Research document saved to `.claude/research/active/` with:
- Chunk manifest
- Per-chunk details
- Inter-phase contract for RPI-Plan

## Next Step
After completion, run `/context-eng:plan $ARGUMENTS`

RPI-Plan will read chunk manifest and create CHUNK-Pn todolist per CHUNK-Rn
