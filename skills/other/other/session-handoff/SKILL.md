---
name: session-handoff
model: standard
description: |
  WHAT: Create comprehensive handoff documents that enable fresh AI agents to seamlessly continue work with zero ambiguity. Solves long-running agent context exhaustion problem.
  
  WHEN: (1) User requests handoff/memory/context save, (2) Context window approaches capacity, (3) Major task milestone completed, (4) Work session ending, (5) Resuming work with existing handoff.
  
  KEYWORDS: "save state", "create handoff", "context is full", "I need to pause", "resume from", "continue where we left off", "load handoff", "save progress", "session transfer", "hand off"
---

# Session Handoff

Create handoff documents that enable fresh agents to continue work seamlessly.

## Mode Selection

**Creating a handoff?** User wants to save state, pause work, or context is full.
→ Follow CREATE Workflow

**Resuming from a handoff?** User wants to continue previous work or load context.
→ Follow RESUME Workflow

**Proactive suggestion?** After substantial work (5+ file edits, complex debugging, major decisions):
> "Consider creating a handoff document to preserve this context. Say 'create handoff' when ready."


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install session-handoff
```


---

## CREATE Workflow

### Step 1: Generate Scaffold

Run the smart scaffold script:

```bash
python scripts/create_handoff.py [task-slug]
```

For continuation handoffs (linking to previous work):
```bash
python scripts/create_handoff.py "auth-part-2" --continues-from 2024-01-15-auth.md
```

The script creates `.claude/handoffs/` directory and generates a timestamped file with pre-filled metadata (timestamp, project path, git branch, recent commits, modified files).

### Step 2: Complete the Document

Open the generated file and fill all `[TODO: ...]` sections. Prioritize:

1. **Current State Summary** - What's happening right now
2. **Important Context** - Critical info the next agent MUST know
3. **Immediate Next Steps** - Clear, actionable first steps
4. **Decisions Made** - Choices with rationale (not just outcomes)

See [references/handoff-template.md](references/handoff-template.md) for full structure.

### Step 3: Validate

```bash
python scripts/validate_handoff.py <handoff-file>
```

Checks:
- No `[TODO: ...]` placeholders remaining
- Required sections present and populated
- No potential secrets detected (API keys, passwords, tokens)
- Referenced files exist
- Quality score (0-100)

**Do not finalize handoffs with secrets detected or score below 70.**

### Step 4: Confirm

Report to user:
- Handoff file location
- Validation score and warnings
- Summary of captured context
- First action item for next session

---

## RESUME Workflow

### Step 1: Find Handoffs

```bash
python scripts/list_handoffs.py
```

### Step 2: Check Staleness

```bash
python scripts/check_staleness.py <handoff-file>
```

Staleness levels:
- **FRESH**: Safe to resume
- **SLIGHTLY_STALE**: Review changes first
- **STALE**: Verify context carefully
- **VERY_STALE**: Consider creating fresh handoff

### Step 3: Load and Verify

Read the handoff document completely. If part of a chain, also read the previous handoff.

Follow [references/resume-checklist.md](references/resume-checklist.md):
1. Verify project directory and git branch match
2. Check if blockers resolved
3. Validate assumptions still hold
4. Review modified files for conflicts

### Step 4: Begin Work

Start with "Immediate Next Steps" item #1.

Reference as you work:
- "Critical Files" for important locations
- "Key Patterns Discovered" for conventions
- "Potential Gotchas" to avoid known issues

---

## Handoff Chaining

For long-running projects, chain handoffs to maintain context lineage:

```
handoff-1.md (initial work)
    ↓
handoff-2.md --continues-from handoff-1.md
    ↓
handoff-3.md --continues-from handoff-2.md
```

When resuming from a chain, read the most recent handoff first, then reference predecessors as needed.

---

## Storage

Location: `.claude/handoffs/`
Naming: `YYYY-MM-DD-HHMMSS-[slug].md`

---

## Quality Criteria

Good handoffs have:
- Zero ambiguity about current state
- Clear, numbered next steps
- Rationale for decisions (not just outcomes)
- File paths with line numbers where relevant
- No secrets or credentials

---

## NEVER

- Include API keys, passwords, tokens, or credentials
- Leave TODO placeholders in finalized handoffs
- Skip the validation step
- Create handoffs without the Important Context section
- Finalize handoffs with quality score below 70
