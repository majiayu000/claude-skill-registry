---
name: resume-handoff
description: Resume work from a handoff, checkpoint, or finalize artifact
---

# Resume from Handoff Artifact

Resume work from a previous session's artifact (handoff, checkpoint, or finalize). These artifacts are YAML files in `thoughts/shared/handoffs/` created by `/handoff`, `/checkpoint`, or `/finalize` commands.

## Artifact Format Reference

Artifacts are YAML files with frontmatter:
```yaml
---
schema_version: "1.0.0"
mode: handoff | checkpoint | finalize
date: 2026-01-14T01:23:45.678Z
session: session-folder-name
outcome: SUCCEEDED | PARTIAL_PLUS | PARTIAL_MINUS | FAILED
primary_bead: bead-id  # required for handoff/finalize
---
goal: What the session accomplished
now: Current focus / what to do next
next:
  - Step 1
  - Step 2
done_this_session:
  - task: Description
    files: [path1, path2]
continuation_prompt: |
  Instructions for resuming
```

## Invocation

### 1. Path provided: `/resume-handoff <path-to-artifact.yaml>`

Read the artifact immediately. Skip discovery.

### 2. Bead ID provided: `/resume-handoff <bead-id>`

Find artifacts related to that bead. First search filenames and directory names:

```bash
find "thoughts/shared/handoffs" -name "*.yaml" 2>/dev/null | grep -i "<bead-id>" | sort -r | head -20
```

If no match by filename/directory, search inside YAML frontmatter:
```bash
grep -rl "primary_bead.*<bead-id>" "thoughts/shared/handoffs/" 2>/dev/null
```

Use the most recent match (by date prefix in filename, e.g. `2026-01-21`).

### 3. No parameters: `/resume-handoff`

**Discover and list available artifacts.** Do NOT just ask the user for a path.

Run this discovery script:

```bash
python3 - <<'PYEOF'
import os, re, pathlib

project = os.environ.get("CLAUDE_PROJECT_DIR") or os.environ.get("CODEX_PROJECT_DIR") or os.getcwd()
root = pathlib.Path(project) / "thoughts" / "shared" / "handoffs"
if not root.exists():
    print("NO_HANDOFFS_DIR")
    raise SystemExit

artifacts = []
for yaml_file in root.rglob("*.yaml"):
    # Skip events/ subdirectory
    if "events" in yaml_file.parts:
        continue
    try:
        text = yaml_file.read_text()
        # Parse frontmatter
        match = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not match:
            continue
        front = {}
        for line in match.group(1).splitlines():
            if ":" in line and not line.startswith("  "):
                key, _, val = line.partition(":")
                front[key.strip()] = val.strip().strip('"')

        # Mode fallback: frontmatter → status field → filename → unknown
        mode = front.get("mode") or front.get("status", "")
        if not mode:
            fname = yaml_file.stem.lower()
            for m in ("handoff", "checkpoint", "finalize"):
                if m in fname:
                    mode = m
                    break
            else:
                mode = "unknown"

        date = front.get("date", "")
        bead = front.get("primary_bead", "")
        outcome = front.get("outcome", "")

        # Parse body for goal
        body = text[match.end():]
        goal_match = re.search(r"^goal:\s*[\"']?(.+?)[\"']?\s*$", body, re.MULTILINE)
        goal = goal_match.group(1).strip() if goal_match else ""

        artifacts.append({
            "path": str(yaml_file),
            "mode": mode,
            "date": date[:16],  # trim to YYYY-MM-DDTHH:MM
            "bead": bead,
            "outcome": outcome,
            "goal": goal[:80],
        })
    except Exception:
        continue

if not artifacts:
    print("NO_ARTIFACTS_FOUND")
    raise SystemExit

# Sort by date field (descending), falling back to filename for date-less artifacts
artifacts.sort(key=lambda a: a["date"] or "0000", reverse=True)

# Show most recent 10
for i, a in enumerate(artifacts[:10]):
    bead_str = f" [{a['bead']}]" if a['bead'] else ""
    print(f"{i+1}. [{a['mode']}] {a['date']}{bead_str} {a['outcome']}")
    print(f"   {a['goal']}")
    print(f"   {a['path']}")
    print()
PYEOF
```

Present the results and ask which one to resume from (even if only one — let the user confirm).

**Tip for user:** "You can also invoke directly: `/resume-handoff thoughts/shared/handoffs/<session>/<filename>.yaml`"

**Note:** Discovery only finds `.yaml` artifacts. Older `.md` format artifacts are not listed but can be opened by direct path.

## Process

### Step 1: Read and Parse the Artifact

1. **Read the YAML artifact completely** using the Read tool (no limit/offset)
2. **Extract key fields from frontmatter:**
   - `mode` — handoff, checkpoint, or finalize
   - `primary_bead` — the bead this work is tied to
   - `outcome` — how the previous session ended
   - `date` — when it was created
3. **Extract key fields from body:**
   - `goal` — what the session was working on
   - `now` — what the next session should focus on
   - `next` — ordered list of next steps
   - `done_this_session` — what was completed (with file references)
   - `blockers` — anything blocking progress
   - `questions` — unresolved questions
   - `decisions` — decisions made and rationale
   - `worked` / `failed` — what worked and what didn't
   - `continuation_prompt` — specific instructions for resuming
   - `files_to_review` — files worth examining with notes
   - `git` — branch, commit, remote info

### Step 2: Load Bead Context (if primary_bead exists)

```bash
bd show <primary_bead>
```

Check bead status. If the bead is closed, note that — the user may want to reopen it or create a new bead.

If the bead is open but not in_progress:
```bash
bd update <primary_bead> --status=in_progress
```

### Step 3: Verify Current State

1. **Check git state:**
   - Is the branch from the artifact still checked out?
   - Has the commit moved forward since the artifact was created?
   - Are there uncommitted changes?

2. **Check referenced files:**
   - Do files mentioned in `done_this_session` and `files_to_review` still exist?
   - Have they been modified since the artifact date?

3. **Check for related specs** (if the goal references a feature):
   - Look in `specs/` for related spec/plan/tasks files

4. **Read critical files** mentioned in:
   - `files_to_review` (with their notes)
   - `continuation_prompt` references
   - `done_this_session` file lists (skim for context)

Do NOT use sub-agents for reading these files — read them directly to maintain context.

### Step 4: Present Analysis

Present a clear summary to the user:

```
## Resuming from [mode] artifact

**Date:** [date]
**Bead:** [primary_bead] — [bead status]
**Previous outcome:** [outcome]
**Goal:** [goal]

### What was done
- [done_this_session items]

### What to do next
[now field, plus next items]

### Current state
- Branch: [current branch vs artifact branch]
- Files: [verified / changed / missing]
- Bead: [status]

### Blockers / Questions (if any)
- [blockers]
- [questions]

### Decisions from previous session
- [decisions with rationale]

### What worked / What didn't
- Worked: [worked items]
- Failed: [failed items — avoid repeating these]

**Recommended first action:** [most logical next step]

Shall I proceed?
```

### Step 5: Get Confirmation and Work

Wait for user confirmation, then begin working on the `next` steps.

If the artifact has a `continuation_prompt`, follow those specific instructions as the starting point.

## Edge Cases

### Finalize artifact (completed work)
If the artifact mode is `finalize`, the work was marked as done. Tell the user:
"This is a finalize artifact — the previous session marked this work as complete with outcome [outcome]. Are you looking to continue related work, or review what was done?"

### Stale artifact (old date)
If the artifact is more than 7 days old, warn:
"This artifact is from [date] ([N days ago]). The codebase may have changed significantly. I'll verify the current state carefully before proceeding."

### Missing bead
If `primary_bead` is set but `bd show` fails, warn and offer concrete recovery:
"The bead [id] referenced in this artifact was not found. It may have been closed or deleted. Options:
1. Create a new bead: `bd create --title="[goal from artifact]" --type=task`
2. Continue without a bead (just follow the next steps)
3. Search for a similar bead: `bd list --status=open`"

### No artifacts found
If discovery finds nothing:
"No handoff artifacts found in `thoughts/shared/handoffs/`. This could mean no previous sessions created handoffs, or the directory doesn't exist yet. Would you like to start fresh?"

## Example Interactions

### Discovery mode (no args)
```
User: /resume-handoff
Assistant: [runs discovery script]

I found 3 recent artifacts:

1. [handoff] 2026-01-21T19:08 [Continuous-Claude-v3-sx8] PARTIAL_PLUS
   Fix continuity lifecycle
   thoughts/shared/handoffs/Continuous-Claude-v3-sx8-continuity/2026-01-21_19-08_continuity_handoff.yaml

2. [checkpoint] 2026-01-17T17:01 [Continuous-Claude-v3-7x6] PARTIAL_PLUS
   Restore CC3 setup
   thoughts/shared/handoffs/Continuous-Claude-v3-7x6-restore-cc3-setup/2026-01-17_17-01_restore-cc3-setup_checkpoint.yaml

3. [finalize] 2026-01-14T21:35 [Continuous-Claude-v3-xsp] SUCCEEDED
   CC artifact non-interactive flow
   thoughts/shared/handoffs/Continuous-Claude-v3-xsp-cc-artifact-non-interactive-flow/2026-01-14_21-35_cc-artifact-non-interactive-flow_finalize.yaml

Which one would you like to resume from?
```

### Direct path
```
User: /resume-handoff thoughts/shared/handoffs/memory-hooks-investigation/2026-01-21_19-08_memory-hooks-investigation_checkpoint.yaml
Assistant: [reads the YAML artifact, loads bead context, verifies git state, presents analysis]
```

### Bead ID
```
User: /resume-handoff Continuous-Claude-v3-7x6
Assistant: [searches for artifacts containing that bead ID, finds the most recent one, proceeds]
```