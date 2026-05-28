---
name: resume-session
command: /resume
aliases: ["/continue", "/status", "/where"]
description: Resume a previous session by reading pipeline state and presenting current status
tier: focused
model: sonnet
---

# Resume Session Skill

## Usage

```
/resume              - Show current state and continue where you left off
/resume --details    - Show detailed checkpoint information
/resume --rollback   - Show available rollback points
```

## Behavior

When `/resume` is invoked:

1. **Read pipeline state**:
   ```
   Read: .claude/pipeline-state.json
   ```

2. **Detect session history**:
   - Check `session_tracking.session_history` for previous sessions
   - Find most recent session and its state

3. **Read closeout files** (if they exist):
   ```
   Read: .claude/closeouts/phase-{N}.yaml (for last completed phase)
   ```

4. **Present resumption status**:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  SESSION RESUMED                                                      ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Project: {project_name}                                               ║
║  Current Phase: {N} - {phase_name}                                     ║
║  Status: {in_progress | gate_pending | complete}                      ║
║                                                                        ║
║  Last Session:                                                         ║
║    • Ended: {timestamp}                                                ║
║    • Phases completed: {list}                                          ║
║    • Last checkpoint: {checkpoint_id}                                  ║
║                                                                        ║
║  From Closeout Notes:                                                  ║
║    {next_phase_brief.must_know from closeout}                         ║
║                                                                        ║
║  Watch Out For:                                                        ║
║    {next_phase_brief.watch_out_for from closeout}                     ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [C] Continue with phase-{X}-orchestrator                              ║
║  [D] Show dashboard                                                    ║
║  [R] Show rollback options                                             ║
╚═══════════════════════════════════════════════════════════════════════╝
```

5. **If --details flag**:
   - Read the most recent checkpoint from `checkpoints` array
   - Display full checkpoint details including:
     - All agent states
     - Context snapshot
     - Resumption prompt

6. **If --rollback flag**:
   - List all available rollback points from checkpoints
   - Present rollback menu (see `/rollback` skill)

## Integration with Session Master

This skill is complementary to session-master:
- **session-master**: Auto-invokes on first message, full status presentation
- **/resume**: Manually invoked, includes closeout notes and watch-out-for guidance

## Quick Resume Prompt

If no pipeline-state.json exists but user says `/resume`:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  NO SESSION STATE FOUND                                               ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  This directory doesn't have a .claude/pipeline-state.json file.     ║
║                                                                        ║
║  Options:                                                              ║
║    [I] Initialize new dev-system project                              ║
║    [D] Detect state from artifacts (PRD, tasks, etc.)                 ║
║    [N] Not a dev-system project - proceed normally                    ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Files Read

- `.claude/pipeline-state.json` - Primary state
- `.claude/closeouts/phase-{N}.yaml` - Phase closeout notes
- `.claude/checkpoints/CP-{phase}-{timestamp}.json` - Checkpoint data (if exists)

## Output

After presenting status, hand off to the appropriate phase orchestrator:
- Route based on current phase number
- Include context from closeout notes
