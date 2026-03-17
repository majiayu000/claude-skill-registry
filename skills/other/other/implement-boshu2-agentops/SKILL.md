---
name: implement
description: 'Execute a single issue with full lifecycle. Triggers: "implement", "work on task", "build this", "start feature", "pick up next issue", "work on issue".'
metadata:
  tier: execution
  dependencies:
    - beads     # optional - for issue tracking via bd CLI
    - standards # loads language-specific standards
---

# Implement Skill

> **Quick Ref:** Execute single issue end-to-end. Output: code changes + commit + closed issue.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Execute a single issue from start to finish.

**CLI dependencies:** bd (issue tracking), ao (ratchet gates). Both optional — see `skills/shared/SKILL.md` for fallback table. If bd is unavailable, use the issue description directly and track progress via TaskList instead of beads.

## Execution Steps

Given `/implement <issue-id-or-description>`:

### Step 0: Pre-Flight Checks (Resume + Gates)

**For resume protocol details, read `skills/implement/references/resume-protocol.md`.**

**For ratchet gate checks and pre-mortem gate details, read `skills/implement/references/gate-checks.md`.**

### Step 1: Get Issue Details

**If beads issue ID provided** (e.g., `gt-123`):
```bash
bd show <issue-id> 2>/dev/null
```

**If plain description provided:** Use that as the task description.

**If no argument:** Check for ready work:
```bash
bd ready 2>/dev/null | head -3
```

### Step 2: Claim the Issue

```bash
bd update <issue-id> --status in_progress 2>/dev/null
```

### Step 3: Gather Context

**USE THE TASK TOOL** to explore relevant code:

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Gather context for: <issue title>"
  prompt: |
    Find code relevant to: <issue description>

    1. Search for related files (Glob)
    2. Search for relevant keywords (Grep)
    3. Read key files to understand current implementation
    4. Identify where changes need to be made

    Return:
    - Files to modify (paths)
    - Current implementation summary
    - Suggested approach
    - Any risks or concerns
```

### Step 4: Implement the Change

**GREEN Mode check:** If test files were provided (invoked by /crank --test-first):
1. Read all provided test files FIRST
2. Read the contract for invariants
3. Implement to make tests pass (do NOT modify test files)
4. Skip to Step 5 verification

Based on the context gathered:

1. **Edit existing files** using the Edit tool (preferred)
2. **Write new files** only if necessary using the Write tool
3. **Follow existing patterns** in the codebase
4. **Keep changes minimal** - don't over-engineer

### Step 5: Verify the Change

**Success Criteria (all must pass):**
- [ ] All existing tests pass (no new failures introduced)
- [ ] New code compiles/parses without errors
- [ ] No new linter warnings (if linter available)
- [ ] Change achieves the stated goal

Check for test files and run them:
```bash
# Find tests
ls *test* tests/ test/ __tests__/ 2>/dev/null | head -5

# Run tests (adapt to project type)
# Python: pytest
# Go: go test ./...
# Node: npm test
# Rust: cargo test
```

**If tests exist:** All tests must pass. Any failure = verification failed.

**If no tests exist:** Manual verification required:
- [ ] Syntax check passes (file compiles/parses)
- [ ] Imports resolve correctly
- [ ] Can reproduce expected behavior manually
- [ ] Edge cases identified during implementation are handled

**If verification fails:** Do NOT proceed to Step 5a. Fix the issue first.

### Step 5a: Verification Gate (MANDATORY)

**THE IRON LAW:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

Before reporting success, you MUST:

1. **IDENTIFY** - What command proves this claim works?
2. **RUN** - Execute the FULL command (fresh, not cached output)
3. **READ** - Check full output AND exit code
4. **VERIFY** - Does output actually confirm the claim?
5. **ONLY THEN** - Make the completion claim

**Forbidden phrases without fresh verification evidence:**
- "should work", "probably fixed", "seems to be working"
- "Great!", "Perfect!", "Done!" (without output proof)
- "I just ran it" (must run it AGAIN, fresh)

#### Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Too simple to verify" | Simple code breaks. Verification takes 10 seconds. |
| "I just ran it" | Run it AGAIN. Fresh output only. |
| "Tests passed earlier" | Run them NOW. State changes. |
| "It's obvious it works" | Nothing is obvious. Evidence or silence. |
| "The edit looks correct" | Looking != working. Run the code. |

**Store checkpoint:**
```bash
bd update <issue-id> --append-notes "CHECKPOINT: Step 5a verification passed at $(date -Iseconds)" 2>/dev/null
```

### GREEN Mode (Test-First Implementation)

When invoked by /crank with `--test-first`, the worker receives:
- **Failing tests** (immutable — DO NOT modify)
- **Contract** (contract-{issue-id}.md)
- **Issue description**

**GREEN Mode Rules:**

1. **Read failing tests FIRST** — understand what must pass
2. **Read contract** — understand invariants and failure modes
3. **Implement ONLY enough** to make all tests pass
4. **Do NOT modify test files** — tests are immutable in GREEN mode
5. **Do NOT add features** beyond what tests require
6. **BLOCKED if spec error** — if contract contradicts tests or is incomplete, write BLOCKED with reason

**Verification (GREEN Mode):**
1. Run test suite → ALL tests must PASS
2. Standard Iron Law (Step 5a) still applies — fresh verification evidence required
3. No untested code — every line must be reachable by a test

**Test Immutability Enforcement:**
- Workers may ADD new test files but MUST NOT modify existing test files provided by the TEST WAVE
- If a test appears wrong, write BLOCKED with the specific test and reason — do NOT fix it

### Step 6: Commit the Change

If the change is complete and verified:
```bash
git add <modified-files>
git commit -m "<descriptive message>

Implements: <issue-id>"
```

### Step 7: Close the Issue

```bash
bd update <issue-id> --status closed 2>/dev/null
```

### Step 7a: Record Implementation in Ratchet Chain

**After successful issue closure, record in ratchet:**

```bash
# Check if ao CLI is available
if command -v ao &>/dev/null; then
  # Get the commit hash as output artifact
  COMMIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "")
  CHANGED_FILES=$(git diff --name-only HEAD~1 2>/dev/null | tr '\n' ',' | sed 's/,$//')

  if [ -n "$COMMIT_HASH" ]; then
    # Record successful implementation
    ao ratchet record implement \
      --output "$COMMIT_HASH" \
      --files "$CHANGED_FILES" \
      --issue "<issue-id>" \
      2>&1 | tee -a .agents/ratchet.log

    if [ $? -eq 0 ]; then
      echo "Ratchet: Implementation recorded (commit: ${COMMIT_HASH:0:8})"
    else
      echo "Ratchet: Failed to record - chain.jsonl may need repair"
    fi
  else
    echo "Ratchet: No commit found - skipping record"
  fi
else
  echo "Ratchet: ao CLI not available - implementation NOT recorded"
  echo "  Run manually: ao ratchet record implement --output <commit>"
fi
```

**On failure/blocker:** Record the blocker in ratchet:

```bash
if command -v ao &>/dev/null; then
  ao ratchet record implement \
    --status blocked \
    --reason "<blocker description>" \
    2>/dev/null
fi
```

**Fallback:** If ao is not available, the issue is still closed via bd but won't be tracked in the ratchet chain. The skill continues normally.

### Step 7b: Post-Implementation Ratchet Record

After implementation is complete:

```bash
if command -v ao &>/dev/null; then
  ao ratchet record implement --output "<issue-id>" 2>/dev/null || true
fi
```

Tell user: "Implementation complete. Run /vibe to validate before pushing."

### Step 8: Report to User

Tell the user:
1. What was changed (files modified)
2. How it was verified (with actual command output)
3. Issue status (closed)
4. Any follow-up needed
5. **Ratchet status** (implementation recorded or skipped)

**Output completion marker:**
```
<promise>DONE</promise>
```

If blocked or incomplete:
```
<promise>BLOCKED</promise>
Reason: <why blocked>
```

```
<promise>PARTIAL</promise>
Remaining: <what's left>
```

## Key Rules

- **Explore first** - understand before changing
- **Edit, don't rewrite** - prefer Edit tool over Write tool
- **Follow patterns** - match existing code style
- **Verify changes** - run tests or sanity checks
- **Commit with context** - reference the issue ID
- **Close the issue** - update status when done

## Without Beads

If bd CLI not available:
1. Skip the claim/close status updates
2. Use the description as the task
3. Still commit with descriptive message
4. Report completion to user

---

## Distributed Mode: Agent Mail Coordination

**For full distributed mode details, read `skills/implement/references/distributed-mode.md`.**

Distributed mode enhances /implement with real-time coordination via MCP Agent Mail when `--mode=distributed`, `--agent-mail`, or `$OLYMPUS_DEMIGOD_ID` is set.

---

## References

- **Agent Mail Protocol:** See `skills/shared/agent-mail-protocol.md` for message format specifications
- **Parser (Go):** `cli/internal/agentmail/` - shared parser for all message types

## Examples

### Implement Specific Issue

**User says:** `/implement ag-5k2`

**What happens:**
1. Agent reads issue from beads: "Add JWT token validation middleware"
2. Explore agent finds relevant auth code and middleware patterns
3. Agent edits `middleware/auth.go` to add token validation
4. Runs `go test ./middleware/...` — all tests pass
5. Commits with message "Add JWT token validation middleware\n\nImplements: ag-5k2"
6. Closes issue via `bd update ag-5k2 --status closed`

**Result:** Issue implemented, verified, committed, and closed. Ratchet recorded.

### Pick Up Next Available Work

**User says:** `/implement`

**What happens:**
1. Agent runs `bd ready` — finds `ag-3b7` (first unblocked issue)
2. Claims issue via `bd update ag-3b7 --status in_progress`
3. Implements and verifies
4. Closes issue

**Result:** Autonomous work pickup and completion from ready queue.

### GREEN Mode (Test-First)

**User says:** `/implement ag-8h3` (invoked by `/crank --test-first`)

**What happens:**
1. Agent receives failing tests (immutable) and contract
2. Reads tests to understand expected behavior
3. Implements ONLY enough to make tests pass
4. Does NOT modify test files
5. Verification: all tests pass with fresh output

**Result:** Minimal implementation driven by tests, no over-engineering.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Issue not found | Issue ID doesn't exist or beads not synced | Run `bd sync` then `bd show <id>` to verify |
| GREEN mode violation | Edited a file not related to the issue scope | Revert unrelated changes. GREEN mode restricts edits to files relevant to the issue |
| Verification gate fails | Tests fail or build breaks after implementation | Read the verification output, fix the specific failures, re-run verification |
| "BLOCKED" status | Contract contradicts tests or is incomplete in GREEN mode | Write BLOCKED with specific reason, do NOT modify tests |
| Fresh verification missing | Agent claims success without running verification command | MUST run verification command fresh with full output before claiming completion |
| Ratchet record failed | ao CLI unavailable or chain.jsonl corrupted | Implementation still closes via bd, but ratchet chain needs manual repair |
