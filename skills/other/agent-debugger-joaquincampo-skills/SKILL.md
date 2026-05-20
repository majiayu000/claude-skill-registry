---
name: agent-debugger
description: Use when a program crashes, a test fails, or code produces wrong results and reading the source isn't enough to see why. Lets you pause execution at any line and inspect the actual runtime state, variable values, types, call stacks, to find what went wrong. Can attach to running servers by PID — no restart or code changes needed.
allowed-tools: Bash(npx -y agent-debugger:*), Bash(agent-debugger:*)
---

# Agent Debugger

A debugger for AI agents. Set breakpoints, inspect state, evaluate expressions, test fixes in-place. Attach to running servers by PID — no restart, no code changes, no manual setup.

## Philosophy

The debugger is a scalpel, not a flashlight. You don't turn it on to look around. You turn it on to make one precise cut — confirm or kill a specific hypothesis about why the program is broken. If you're "exploring" in the debugger, you've already lost.

**Every session starts before the debugger.** Read the code. Read the traceback. Form a theory. Know exactly what breakpoint you'll set and what eval you'll run before you type a single command. The debugger is the experiment, not the investigation.

**`eval` is the only command that matters.** `vars`, `step`, `stack`, `source` — these are all setup. The eval is the actual experiment. It's where you test your hypothesis against reality. Everything else is scaffolding to get you to the right eval at the right moment.

**Half of all bugs don't need a debugger.** Read the traceback. Read the code. Check the types. Grep for the error message. Look at git blame. Most bugs surrender to careful reading. Reach for the debugger only when the bug depends on runtime state you can't determine statically.

## The Rules

1. **Read first, debug second.** Never start a debug session without reading the relevant code and forming a hypothesis. The debugger confirms theories — it doesn't generate them.

2. **One breakpoint, one question.** Each breakpoint should answer a specific question. "Is `x` a string here?" "Is `balance` negative after this call?" "Does this branch execute?" If you can't articulate the question, you're not ready to debug.

3. **Eval, don't dump.** `vars` dumps everything and answers nothing. `eval "type(data['age'])"` answers exactly one question. Prefer eval. Always.

4. **Never step through loops.** A loop with 100 iterations is 100 step commands. A conditional breakpoint is 1 command. Use `--break "file:line:i == 50"` to jump straight to the iteration that matters.

5. **Two strikes, new theory.** If your hypothesis was wrong twice, stop. Your mental model of the code is broken, not the debugger session. Close, re-read the code, form a completely different theory, then start a new session with different breakpoints. Continuing to probe the same area has exponentially diminishing returns.

6. **Test the fix before writing it.** The debugger gives you a live REPL in the exact context of the bug. Use `eval` to run your proposed fix expression before editing any code. If it works in eval, it'll work in the code.

7. **Prove the fix, write the test.** After fixing, re-run the program to verify. Then write the smallest possible test that catches the bug. A fix without a test is a fix that will regress.

8. **Close the session.** Always. A stale session blocks the next one.

## Bootstrap

- If `agent-debugger` is available globally, use it directly.
- Otherwise, use `npx -y agent-debugger` (zero-install, no prompts).

## Commands

```bash
# If installed globally:
agent-debugger start <script> --break file:line[:condition] [--runtime path] [--args ...]

# If not installed:
npx -y agent-debugger start <script> --break file:line[:condition] [--runtime path] [--args ...]
agent-debugger attach --pid <PID> [--break file:line]    # Attach to running process (no restart needed)
agent-debugger attach [host:]port [--break file:line]    # Attach to existing debug server
agent-debugger eval <expression>        # Run any expression in the current frame
agent-debugger vars                     # List local variables (prefer eval)
agent-debugger step [into|out]          # Step over / into function / out of function
agent-debugger continue                 # Run to next breakpoint / wait for hit after attach
agent-debugger stack                    # Show call stack
agent-debugger break file:line[:cond]   # Add breakpoint mid-session
agent-debugger source                   # Show source around current line
agent-debugger status                   # Show session state and location
agent-debugger close                    # Detach / end debug session
```

Multiple `--break` flags supported. Conditions are expressions: `--break "app.py:42:len(items) > 10"`.

### Debugging a Running Server

Use `attach --pid` to debug any running Python server (uvicorn, Flask, FastAPI, Django, etc.) without restarting it or changing any code. debugpy is auto-installed if missing.

```bash
# Find the server's PID
ps aux | grep uvicorn

# Attach — no restart, no code changes, no setup
agent-debugger attach --pid 12345 --break routes.py:42

# Trigger a request to hit the breakpoint
curl localhost:8000/api/endpoint

# Wait for the breakpoint hit, then inspect
agent-debugger continue
agent-debugger vars
agent-debugger eval "request.body"
agent-debugger close         # detaches without killing the server
```

If the server uses a virtualenv, the debugger auto-detects it and installs debugpy into the correct environment.

#### Alternative: attach by port

If you prefer explicit control, start the server with debugpy and attach by port:

```bash
python -m debugpy --listen 5678 -m uvicorn app:main
agent-debugger attach 5678 --break routes.py:42
```

## Supported Languages

| Language | Extension | Adapter | Requirement |
|----------|-----------|---------|-------------|
| Python | .py | debugpy | Auto-installed on attach. Or: `pip install debugpy` |
| JavaScript/TypeScript | .js/.ts | Node Inspector | Node.js |
| Go | .go | Delve | `go install github.com/go-delve/delve/cmd/dlv@latest` |
| Rust/C/C++ | .rs/.c/.cpp | CodeLLDB | `CODELLDB_PATH` env var |

## The Playbook

These are not suggestions. These are the right way to handle each class of bug.

### Type Bugs

A value has the wrong type somewhere in the pipeline. Don't step through — go straight to the suspect and ask.

```bash
agent-debugger start app.py --break "app.py:25"
agent-debugger eval "type(data['age'])"                  # <class 'str'> — found it
agent-debugger eval "int(data['age'])"                   # 35 — fix is safe
agent-debugger close
```

Two commands after the breakpoint. Done.

### Data Pipeline Bugs

Something in a batch is wrong. Don't look at individual records — assert the shape of the whole batch.

```bash
agent-debugger start etl.py --break "etl.py:90"          # after the transformation
agent-debugger eval "all(isinstance(v, int) for v in result.values())"   # False
agent-debugger eval "[k for k,v in result.items() if not isinstance(v, int)]"  # ['quantity']
agent-debugger close
```

One breakpoint, two evals. The first asks "is anything wrong?", the second asks "what exactly?"

### Loop Bugs (The Wolf Fence)

A loop processes N items and something goes wrong at an unknown iteration. Binary search it.

```bash
agent-debugger start app.py --break "app.py:45:i == 500"    # midpoint
agent-debugger eval "is_valid(result)"                       # True → bug is after 500
agent-debugger close

agent-debugger start app.py --break "app.py:45:i == 750"    # narrow
agent-debugger eval "is_valid(result)"                       # False → bug is between 500-750
agent-debugger close

agent-debugger start app.py --break "app.py:45:i == 625"    # narrow again
```

~10 iterations to find the bug in 1000 items. Not 1000 step commands.

### Invariant Violations

You know what should never happen. Tell the debugger to catch the exact moment it does.

```bash
# "balance should never go negative"
agent-debugger start bank.py --break "bank.py:68:account.balance < 0"

# "every value should be numeric"
agent-debugger start pipeline.py --break "pipeline.py:30:not isinstance(value, (int, float))"

# "list should never exceed 100 items"
agent-debugger start app.py --break "app.py:55:len(results) > 100"
```

If it hits, you've caught the crime in progress. If it doesn't hit, your theory was wrong — move on.

### Recursion / Deep Call Chains

The stack tells you how you arrived. The eval tells you why you're wrong.

```bash
agent-debugger start tree.py --break "tree.py:22"
agent-debugger stack                    # see the recursion depth
agent-debugger eval "current_depth"     # 3
agent-debugger eval "max_depth"         # 3 — off-by-one, should be <, not <=
agent-debugger close
```

### "Where Does This Bad Data Come From?"

You found bad data downstream. Pivot upstream.

```bash
agent-debugger start app.py --break "handler.py:55"
agent-debugger eval "data['age']"          # '35' — string, wrong. But handler didn't create this.
agent-debugger close                       # pivot to the source

agent-debugger start app.py --break "loader.py:22"
agent-debugger eval "raw_row"              # CSV parser returns strings. Root cause.
agent-debugger close
```

Don't fix the symptom at the handler. Fix the cause at the loader.

### "Which of These 3 Functions Is the Culprit?"

Set breakpoints at all suspects. The runtime tells you which one fires.

```bash
agent-debugger start app.py \
  --break "auth.py:30" \
  --break "validate.py:55" \
  --break "handler.py:80"

# Hits validate.py:55 — now you know where to focus
agent-debugger eval "request.payload"
agent-debugger close
```

### Testing a Fix In-Place

You think you know the fix. Prove it before editing.

```bash
# Paused at the crash: total + data['age'] where age is a string
agent-debugger eval "total + int(data['age'])"    # 90 — works
agent-debugger eval "int(data['age'])"            # 35 — safe cast

# Prove it works for the entire dataset
agent-debugger eval "sum(int(d['age']) if isinstance(d['age'], str) else d['age'] for d in users)"
agent-debugger close
# NOW edit the code, with confidence
```

### Falsifying Your Theory

Design evals that would **break** your hypothesis, not confirm it. Confirmation bias is the #1 debugging trap.

```bash
# Theory: "age is a string only in the third record"

# BAD — only confirms
agent-debugger eval "isinstance(data['age'], str)"       # True. But so what?

# GOOD — tries to disprove
agent-debugger eval "isinstance(users[0]['age'], str)"   # False — not all records
agent-debugger eval "isinstance(users[1]['age'], str)"   # False — so it IS specific to record 3
agent-debugger eval "users[2]"                           # {'name': 'Charlie', 'age': '35'} — source data is wrong
```

## Never Do This

**Never step blindly.** If you're running `step` more than 3 times in a row, you need a breakpoint, not more steps.

**Never start without reading code.** The debugger doesn't find bugs. You find bugs by reading code and forming theories. The debugger just confirms them.

**Never dump vars when you have a question.** `vars` is for the rare case when you genuinely don't know what variables exist. If you have a theory, `eval` tests it directly.

**Never debug timing bugs with the debugger.** Pausing execution changes timing. Race conditions disappear under observation. Use logging.

**Never keep going after 2 failed hypotheses.** Close. Re-read. Rethink. Your mental model is wrong, and more debugger commands won't fix your mental model.

**Never leave a session open.** `agent-debugger close`. Always. Every time.

**Never fix without verifying.** Run the program after the fix. If you can, toggle the fix to prove causation. Then write a test.

## Notes

- Use **absolute paths** for breakpoints
- One session at a time — `close` before starting another
- `attach --pid` auto-installs debugpy — no manual setup needed
- `attach --pid` requires lldb (macOS, included with Xcode CLI tools) or gdb (Linux)
- Program stdout goes to the daemon — use `eval` to inspect output values
