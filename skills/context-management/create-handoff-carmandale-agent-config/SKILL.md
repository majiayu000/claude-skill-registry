---
name: create-handoff
description: Create unified artifact document for checkpoint, handoff, or finalize
---

# Create Unified Artifact

This skill is the **canonical generator** for unified artifacts (checkpoint, handoff, finalize). Use it to capture session state in a consistent schema under the canonical directory.

## When to Use

- **/checkpoint**: quick mid-session snapshot (bead optional)
- **/handoff**: transfer ongoing work to the next session (bead required)
- **/finalize**: memorialize completed work (bead required)

## Process

### 1. Gather Session Context

If a bead is active, capture it. For handoff/finalize, a bead is **required**:

```bash
bd list --status=in_progress
```

### 2. Create the Unified Artifact

Preferred path: use the core generator script (handles timestamps + git metadata):

```bash
~/.claude/scripts/cc-artifact --mode <checkpoint|handoff|finalize> [--bead <BEAD_ID>] [--session-title "<short title>"]
```

Artifacts are written to:

```
thoughts/shared/handoffs/<session>/YYYY-MM-DD_HH-MM_<title>_<mode>.yaml
```

**Filename format:**
- `YYYY-MM-DD_HH-MM`: Date and time (UTC) with hyphen separators
- `<title>`: Slugified session title (or derived from session)
- `<mode>`: checkpoint | handoff | finalize
- Example: `2026-01-14_01-23_auth-refactor_handoff.yaml`

### 3. Required Fields

**Core fields (all artifacts):**
- `schema_version`: "1.0.0"
- `mode`: "checkpoint" | "handoff" | "finalize"
- `date`: ISO 8601 date or date-time (e.g., "2026-01-14T01:23:45.678Z")
- `session`: Session folder name (bead + slug)
- `goal`: What this session accomplished
- `now`: Current focus / next action
- `outcome`: SUCCEEDED | PARTIAL_PLUS | PARTIAL_MINUS | FAILED
- `primary_bead`: Required for handoff/finalize, optional for checkpoint

**Handoff-specific fields (optional):**
- `related_beads`: Related bead IDs
- `files_to_review`: Array of {path, note}
- `continuation_prompt`: Resume instructions

**Finalize-specific fields (optional but recommended):**
- `final_solutions`: Array of {problem, solution, rationale}
- `final_decisions`: Array of decision objects
- `artifacts_produced`: Array of {path, note}

**Optional but recommended:**
- `session_id`: 8-char hex identifier
- `done_this_session`: Array of completed tasks with files
- `next`: Array of next steps
- `blockers`: Array of blocking issues
- `questions`: Array of unresolved questions
- `decisions`: Record of key decisions (simple format) or array of Decision objects
- `worked`: What worked well
- `failed`: What didn't work and why
- `findings`: Record of key discoveries
- `git`: Branch, commit, remote
- `files`: Object with created, modified, deleted arrays
- `test`: Command to verify the work

### 4. YAML Format (Handoff Example)

```yaml
---
schema_version: "1.0.0"
mode: handoff
date: 2026-01-14T01:23:45.678Z
session: Continuous-Claude-v3-ug8.6-auth-refactor
outcome: PARTIAL_PLUS
primary_bead: Continuous-Claude-v3-ug8.6
session_id: abc12345
---

goal: What this session accomplished
now: What next session should do first

done_this_session:
  - task: First completed task
    files:
      - path/to/file1.ts
      - path/to/file2.ts
  - task: Second completed task
    files:
      - path/to/file3.ts

next:
  - First step for next session
  - Second step for next session

blockers:
  - Blocking issue 1
  - Blocking issue 2

questions:
  - Unresolved question 1
  - Unresolved question 2

decisions:
  decision_name: Rationale for this decision

worked:
  - Approach that worked
failed:
  - Approach that failed and why

findings:
  key_finding: Details about this finding

related_beads:
  - beads-xxx
  - beads-yyy

files_to_review:
  - path: src/important-file.ts
    note: Focus on the authentication logic here

continuation_prompt: |
  Start by reviewing the auth flow in src/auth.ts.
  The next step is to implement the refresh token logic.

git:
  branch: feat/auth-system
  commit: abc1234
  remote: origin

files:
  created:
    - new-file.ts
  modified:
    - existing-file.ts

test: npm test
```

### 5. Mark Session Outcome (REQUIRED)

**IMPORTANT:** Before responding to the user, you MUST ask about the session outcome.

Use the AskUserQuestion tool with these exact options:

```
Question: "How did this session go?"
Options:
  - SUCCEEDED: Task completed successfully
  - PARTIAL_PLUS: Mostly done, minor issues remain
  - PARTIAL_MINUS: Some progress, major issues remain
  - FAILED: Task abandoned or blocked
```

After the user responds, the outcome is included in the YAML.

### 6. Confirm Completion

Respond to the user:

```
Artifact created! Outcome: [OUTCOME]

Resume in a new session with:
/resume_handoff thoughts/shared/handoffs/<session>/[filename]
```

---

## Additional Notes

- **Be thorough and concise**: Include key details without excessive verbosity
- **Avoid large code snippets**: Use file:line references (e.g., `src/file.ts:42-56`)
- **Focus on context**: What does the next session need to know?
- **Link files**: Reference important files with notes for next session
- **primary_bead is REQUIRED for handoff/finalize**

This skill provides a single, structured artifact format for checkpoints, handoffs, and finalize events.
