---
name: finalize
description: Create finalize document for session closure and memorial
---

# Finalize Session

You are tasked with writing a finalize document to close out a session with a complete memorial of what was accomplished. This is a **session memorial** - more comprehensive than a handoff, capturing solutions, decisions, and closure.

## When to Use

Use `/finalize` when:
- A bead/task is complete and you want to document the solution
- A session ends with concrete accomplishments worth memorializing
- You want to capture final decisions and their rationale
- The work is done and needs formal closure (not just handoff)

**Key difference from /handoff:**
- **Handoff**: Transfer work to next session (ongoing)
- **Finalize**: Memorial of completed work (closure)

## Process

### 1. Gather Session Context

First, determine the bead you're working on:

```bash
bd list --status=in_progress
```

If no bead is in progress, finalize requires a bead - ask the user which bead to finalize.

### 2. Use writeArtifact() Function

This skill uses the unified artifact system. Call writeArtifact() from the hook system:

```typescript
// In .claude/hooks - this is conceptual, actual implementation in hooks
import { writeArtifact } from './src/shared/artifact-writer.js';
import { createArtifact } from './src/shared/artifact-schema.js';

const artifact = createArtifact(
  'finalize',  // mode
  'Goal achieved in this session',
  'Work is complete',
  'SUCCEEDED',  // or PARTIAL_PLUS, PARTIAL_MINUS, FAILED
  {
    primary_bead: 'beads-xxx',
    session: 'beads-xxx-auth-refactor',
    session_id: 'abc12345',
  }
);

// Add finalize-specific fields
artifact.final_solutions = [
  {
    problem: 'Description of problem',
    solution: 'What was implemented',
    rationale: 'Why this approach'
  }
];

artifact.final_decisions = [
  {
    decision: 'Key architectural choice',
    rationale: 'Why we chose this',
    alternatives_considered: ['Option A', 'Option B'],
    why_this: 'Specific reasons for final choice'
  }
];

const path = await writeArtifact(artifact);
```

### 3. Required Fields

**Core fields (all artifacts):**
- `goal`: What this session accomplished
- `now`: Final status / closure statement
- `outcome`: SUCCEEDED | PARTIAL_PLUS | PARTIAL_MINUS | FAILED
- `primary_bead`: The bead being finalized (REQUIRED for finalize)
- `session`: Session folder name (bead + slug)

**Finalize-specific fields:**
- `final_solutions`: Array of problem/solution/rationale
- `final_decisions`: Array of decisions with full rationale
- `artifacts_produced`: Files created/modified with notes

**Optional but recommended:**
- `done_this_session`: Array of completed tasks with files
- `decisions`: Record of key decisions (can use simpler format)
- `worked`: What worked well
- `failed`: What didn't work and why
- `findings`: Key discoveries
- `git`: Branch, commit, PR status
- `files`: created, modified, deleted arrays

### 4. Output Location

All finalize artifacts are written to:
```
thoughts/shared/handoffs/<session>/YYYY-MM-DD_HH-MM_<title>_finalize.yaml
```

Format: YAML frontmatter + YAML body (no Markdown body)

### 5. Mark Outcome (Optional)

If integrated with outcome tracking:

```bash
# Mark the most recent artifact
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "${CLAUDE_PROJECT_DIR:-.}")
cd "$PROJECT_ROOT/opc" && uv run python scripts/core/artifact_mark.py --latest --outcome SUCCEEDED
```

### 6. Close the Bead

After finalizing, close the associated bead:

```bash
bd close <bead-id> --reason "Completed - see finalize artifact"
```

### 7. Confirm Completion

Respond to the user:

```
Finalize document created! Session closed with outcome: [OUTCOME].

Bead <bead-id> marked as complete.

Artifact location: thoughts/shared/handoffs/<session>/[filename]
```

---

## Example Finalize Structure

```yaml
---
schema_version: "1.0.0"
mode: finalize
date: 2026-01-14T01:23:45.678Z
session: unified-artifact-system
session_id: abc12345
outcome: SUCCEEDED
primary_bead: Continuous-Claude-v3-ug8.7
---

goal: Implement unified artifact system with finalize support
now: System complete and tested

done_this_session:
  - task: Created finalize skill
    files:
      - .claude/skills/finalize/SKILL.md
  - task: Integrated writeArtifact() function
    files:
      - .claude/skills/finalize/SKILL.md

final_solutions:
  - problem: Need unified artifact system for checkpoint/handoff/finalize
    solution: Created writeArtifact() function with schema validation
    rationale: Single function reduces duplication and ensures consistency

final_decisions:
  - decision: Use YAML frontmatter for all artifacts
    rationale: Parseable by both humans and machines
    alternatives_considered:
      - Pure markdown
      - JSON files
    why_this: YAML is readable and structured, frontmatter preserves markdown body

artifacts_produced:
  - path: .claude/hooks/src/shared/artifact-writer.ts
    note: Main writer implementation
  - path: .claude/hooks/src/shared/artifact-schema.ts
    note: TypeScript schema definitions

worked:
  - Unified schema approach reduces maintenance
  - JSON Schema validation catches errors early
failed:
  - Initial attempt at markdown-only format was too unstructured

git:
  branch: feat/continuity-system
  commit: abc1234
  pr_ready: "https://example.com/pull/123"

files:
  created:
    - .claude/skills/finalize/SKILL.md
  modified:
    - .claude/hooks/src/shared/artifact-writer.ts

test: npm test --prefix .claude/hooks
```

---

## Notes

- **Be comprehensive**: Finalize is the memorial - capture everything important
- **Focus on solutions**: Document what was built and why
- **Capture decisions**: Include alternatives considered and rationale
- **Link artifacts**: Reference key files with notes
- **Close the loop**: Mark bead as complete after finalize
- **primary_bead is REQUIRED**: Finalize must be tied to a bead

This skill provides formal closure for completed work, creating a lasting record of what was accomplished and why.
