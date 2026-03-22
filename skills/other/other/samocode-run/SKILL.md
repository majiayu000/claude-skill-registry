---
name: samocode-run
description: Run and monitor samocode autonomous sessions on projects. Use when user says "run samocode" or wants to continue a samocode session.
---

# Samocode Run

Runs the samocode autonomous orchestrator on a project session and monitors its progress.

## CRITICAL: DO NOT MANUALLY ORCHESTRATE

**When user asks to "run samocode" or "continue samocode", you MUST use this skill.**

DO NOT:
- Launch Task subagents yourself for investigation/planning/implementation phases
- Manually read `_overview.md` and decide what phase to run
- Update `_signal.json` yourself
- Pretend to be the orchestrator

The Python worker (`main.py`) handles ALL of this. Your job is to START the worker and MONITOR its output.

## Trigger Phrases

Use this skill when user says:
- "run samocode"
- "start samocode"
- "continue samocode"
- "let samocode work on it"

## What is Samocode?

Samocode is an autonomous session orchestrator that runs the configured AI CLI provider in a loop to complete complex tasks. It:
- Reads session state from `_overview.md`
- Runs phase-specific agents automatically based on current phase
- Sends Telegram notifications on state changes
- Continues until task is complete or blocked

For workflow details and phase definitions, see `~/samocode/CLAUDE.md`.

## Sessions: Manual vs Autonomous

There's no strict "samocode session" - just sessions. Any session can be worked on:
- **Manually** by you (the parent agent session) - e.g., investigation, Q&A, planning
- **Autonomously** by samocode - e.g., implementation, testing, quality fixes
- **Mixed** - start manually, hand off to samocode, take back control when blocked

This flexibility is intentional. Use samocode for repetitive/long-running phases, work manually when human judgment is needed.

## When to Use

**Only when user explicitly asks for samocode** (see Trigger Phrases above).

Do NOT assume samocode should run just because a session exists.

## Execution

**Arguments:** $ARGUMENTS (session name or project path with session name)

### Steps

1. **Find .samocode config:**
   - Look for `.samocode` file in current working dir or project path
   - Extract the full path to the `.samocode` file (e.g., `~/project/.samocode`)
   - **If `.samocode` file is missing:** ERROR and ask user to create it

2. **Determine session name:**
   - If `$ARGUMENTS` is a session name (e.g., "my-task"), use it directly
   - If `$ARGUMENTS` includes a path, extract session name from it
   - Session will be resolved: exact match → dated match → new session

3. **Check session state (if exists):**
   - Read `_overview.md` Status section
   - **If `Phase: done`:**
     - Ask user: "Session is complete. What new work do you want to do?"
     - Update `_overview.md`:
       - `Phase: investigation`
       - `Last Action: Resuming session for: [user's goal]`
       - `Next: Investigate approach for [user's goal]`
     - Add to Flow Log: `- [MM-DD HH:MM] Resuming: [user's goal]`
   - **If `Blocked: yes` or `blocked`:**
     - Show user the current status (Last Action, Next, reason if available)
     - Ask how to proceed
     - Update status based on user's direction

4. **Start samocode:**
   ```bash
   cd ~/samocode && python main.py \
     --config [PATH_TO_.SAMOCODE] \
     --session [SESSION_NAME] 2>&1
   ```

   **Optional:** Add `--timeout SECONDS` for per-iteration time limit (default: 1800s = 30 min).
   Each child agent iteration is killed if it exceeds this. Increase for complex phases:
   ```bash
   python main.py --config ... --session ... --timeout 3600  # 1 hour per iteration
   ```

   **Do NOT wrap with bash `timeout`** - The orchestrator manages its own timeouts via `--timeout`.
   External timeouts can kill iterations mid-work and corrupt session state.

   Run this in background using `run_in_background: true`

   **Avoid reading background task output directly.** The samocode worker output includes full
   Agent CLI logs which are large (100KB+ per iteration). Monitor progress via `_overview.md`
   and other session files instead.

   If debugging requires checking task output (e.g., investigating a crash):
   - Use `grep` to search for specific errors or patterns first
   - Use `tail -n 2` or `tail -n 5` max - each line can be huge (full JSON)
   - Use `Read` with `offset` and `limit` to read small portions
   - Never read the entire file

5. **Monitor loop (prefer session files over task output):**

   5.1. Start background check (sleep duration by phase: investigation/planning 60s, implementation 120-180s, quality 120s, testing 60s):
   ```bash
   Bash(command="sleep 60 && cat [SESSION]/_overview.md", run_in_background=true)
   ```
   Returns task_id (e.g., "b155903")

   5.2. Wait for result - **DO NOT SKIP, do immediately after 5.1:**
   ```bash
   TaskOutput(task_id="b155903", block=true, timeout=600000)
   ```
   Note: 600000ms (10 min) is the max allowed timeout.

   5.3. Extract from result: Phase, Iteration, Total Iterations, Blocked, Last Action, Next, last 3 Flow Log entries

   5.4. Get recent commits:
   ```bash
   git -C [WORKING_DIR] log --oneline -3
   ```

   5.5. Report to user:
   ```
   Samocode Progress [HH:MM elapsed]
   --------------------------------
   Phase: [phase] (Iteration N/Total)
   Last: [Last Action]
   Next: [Next]

   Recent commits:
   - [hash] [message]

   Flow:
   - [last 2-3 Flow Log entries]
   ```

   5.6. Check stop condition:
   - `Phase: done` → report final summary, STOP
   - `Blocked:` contains `yes` or `waiting` → handle accordingly (see Handling Waiting States), STOP
   - Otherwise → goto step 5.1

   **IMPORTANT: On STOP, clean up monitoring.** When samocode finishes (done/blocked/waiting), do NOT leave pending background sleep tasks running. Stop any active monitoring task via `TaskStop` before reporting the final status. This prevents stale notification floods.

## Handling Waiting States

When samocode signals `waiting`:

**Auto-approve/answer ONLY if user explicitly requested it** (e.g., "run samocode and approve", "accept suggestions", "auto-approve"). Otherwise, report the waiting state and wait for user decision.

**For `waiting_for: plan_approval`:**
1. Report: "Plan ready for review: [full path to plan file]"
2. If user requested auto-approve: proceed to approval
3. Otherwise: Ask "Approve this plan?" and wait
4. On approval, update `_overview.md` (NOT `_signal.json`):
   - `Phase: implementation`
   - `Blocked: no`
   - `Last Action: Plan approved by human`
5. Then restart samocode

**For `waiting_for: qa_answers`:**
1. Report: "Q&A ready: [full path to _qa.md]" (includes suggestions)
2. If user requested to accept suggestions: fill in suggested answers
3. Otherwise: Wait for user to provide/confirm answers
4. Update `_qa.md` with answers
5. Then restart samocode

**CRITICAL: Update `_overview.md`, not `_signal.json`**
The orchestrator reads phase from `_overview.md`. Writing to `_signal.json` alone will cause loops.

## Required `.samocode` File

Every project using samocode MUST have a `.samocode` file in its root:

```
MAIN_REPO=~/path/to/main/repo
WORKTREES=~/path/to/worktrees/
SESSIONS=~/path/to/_sessions/
```

**All three keys are REQUIRED:**
- `MAIN_REPO`: The main working directory (where the child agent runs)
- `SESSIONS`: Where samocode session folders are stored
- `WORKTREES`: Where git worktrees are created

## Session Structure

Sessions are stored in SESSIONS dir (from `.samocode` file), NOT nested inside projects:

```
[SESSIONS_DIR]/
└── [YY-MM-DD]-[session-name]/    # Session folder (e.g., 26-01-15-pyright-ci)
    ├── _overview.md              # Main session state
    ├── _signal.json              # Control signal
    ├── _qa.md                    # Q&A when waiting for human input
    ├── _logs/                    # Agent iteration logs (JSONL)
    │   └── [MM-DD-HHMM]-[NNN]-[phase].jsonl
    ├── [MM-DD-HH:mm]-plan-*.md   # Implementation plans
    ├── [MM-DD-HH:mm]-dive-*.md   # Investigation reports
    └── [MM-DD-HH:mm]-*.md        # Other artifacts
```

## Key Files in _overview.md

```markdown
## Status
Phase: [investigation|planning|implementation|testing|quality|done]
Iteration: N
Blocked: [yes/no]
Last Action: [what happened]
Next: [what to do next]

## Flow Log
- [NNN @ MM-DD HH:MM] Event description -> optional-file.md
```

## Common Issues

1. **Missing .samocode file**: Create `.samocode` file in project root with SESSIONS, WORKTREES, MAIN_REPO
2. **Telegram errors**: Check `~/samocode/.env` has TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
3. **Timeout**: Default is 30 min. Increase provider timeout env var (`CLAUDE_TIMEOUT` or `CODEX_TIMEOUT`) if iterations need more

## Debugging Samocode Bugs

If samocode exhibits bugs or weird behavior (loops, wrong decisions, missing steps, etc.):

1. **Analyze the issue:**
   - Check worker output logs for errors
   - Read `_overview.md` to see what went wrong
   - Check if workflow.md instructions are unclear
   - Check if skills have ambiguous or missing guidance

2. **Suggest fixes - DO NOT auto-implement:**
   - Identify the root cause (workflow.md, skill, or worker code)
   - Propose specific fix to user with explanation
   - Show exact file and changes needed
   - **WAIT FOR USER CONFIRMATION before making any changes**

3. **Samocode source locations:**
   - Worker/orchestrator: `~/samocode/main.py`, `~/samocode/worker/`
   - Workflow prompt: `~/samocode/workflow.md`
   - Skills: `~/samocode/skills/*/SKILL.md`
   - Commands: `~/samocode/commands/*.md`

4. **Common fix patterns:**
   - Infinite loops → Add explicit stop conditions in workflow.md
   - Wrong phase transitions → Clarify phase criteria in workflow.md
   - Missing context → Add more explicit instructions in skill
   - Format errors → Add examples in skill or workflow

**IMPORTANT:** Always propose fixes and wait for user approval. Samocode is critical infrastructure - no cowboy coding.

## Example Usage

```
User: "Run samocode on the hvac project"
→ Find ~/code/hvac-voice-agent/.samocode file
→ Determine session name from context (e.g., "voice-agent")
→ Run: python main.py --config ~/code/hvac-voice-agent/.samocode --session voice-agent
→ Monitor iterations, report progress

User: "Continue the samocode session"
→ Find session name from context or ask user
→ Find .samocode file path
→ Run: python main.py --config [CONFIG_PATH] --session [SESSION_NAME]
→ Monitor iterations, report progress
```

**Remember:** You run `python main.py`, the Python worker runs the configured provider (Claude or Codex). You do NOT run phase agents yourself.
