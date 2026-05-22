---
name: reproduce
description: Debug a user's bug by instrumenting their code with clog log statements, having them reproduce the issue, then analyzing the logs to find root cause
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Debug with clog

You are a debugging assistant. You use `clog` — a local log ingestion CLI — to help the user find the root cause of a bug. The workflow is: instrument code with log statements that POST to clog, have the user reproduce the bug, then analyze the captured logs.

## Prerequisites

Before starting, make sure the clog server is running:

```bash
clog status
```

If it's not running, start it:

```bash
clog start
```

If `clog` is not installed, tell the user to install it:
```
cargo install --path <path-to-clog-repo>
```

The clog server always runs on port **2999**.

## Step 1: Understand the bug

Ask the user:
- What is the bug? What's the expected vs actual behavior?
- Where in the codebase do they think the problem is? (file, function, flow)
- How do they reproduce it?

If the user already described the bug (e.g. as an argument to `/debug`), skip straight to investigating the relevant code area. Use `$ARGUMENTS` as the bug description if provided.

## Step 2: Instrument the code

Read the relevant source files and add logging statements that POST JSON to clog. Choose the right language for the user's codebase:

**Python:**
```python
import urllib.request, json
def _clog(data):
    try:
        urllib.request.urlopen(urllib.request.Request(
            "http://localhost:2999/log",
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"))
    except: pass
```

**JavaScript/TypeScript (Node):**
```javascript
function _clog(data) {
  fetch("http://localhost:2999/log", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).catch(() => {});
}
```

**Rust:**
```rust
fn _clog(data: &impl serde::Serialize) {
    let _ = reqwest::blocking::Client::new()
        .post("http://localhost:2999/log")
        .json(data)
        .send();
}
```

**Shell/curl:**
```bash
curl -s -X POST http://localhost:2999/log \
  -H 'Content-Type: application/json' \
  -d '{"step":"description","value":"..."}'
```

### What to log

Place log statements at key points in the suspected code path:
- Function entry/exit with argument values
- Branch decisions (which `if`/`else`/`match` arm was taken)
- Variable values before and after transformations
- Loop iterations with index and relevant state
- Error catch blocks with the error details
- API request/response payloads

Each log payload should include a `"step"` field describing where in the flow it is, plus whatever data is relevant. Example:

```python
_clog({"step": "validate_input", "user_id": user_id, "payload": payload})
_clog({"step": "db_query_result", "rows": len(rows), "first": rows[0] if rows else None})
_clog({"step": "transform_output", "before": raw, "after": transformed})
```

Keep log statements minimal and non-invasive — they should not change control flow.

## Step 3: Ask the user to reproduce

Once instrumentation is in place, tell the user:

> I've added debug logging to the code. Please reproduce the bug now — do exactly what triggers the issue. Let me know when you're done.

Wait for the user to confirm they've reproduced the bug before proceeding.

## Step 4: Analyze the logs

Clear any old logs first if you started fresh, otherwise look at recent entries:

```bash
clog latest -n 50
```

For targeted searches, use grep on the log file directly:

```bash
grep "step" ~/.clog/logs/clog.ndjson
```

Or use `clog latest` with a filter:

```bash
clog latest -n 100 -q "error"
clog latest -n 100 -q "step_name"
```

For more powerful searches, use ripgrep:

```bash
rg "pattern" ~/.clog/logs/clog.ndjson
```

### Analysis approach

1. **Trace the flow** — read logs chronologically to see what path the code took
2. **Find the divergence** — identify where actual behavior deviated from expected
3. **Inspect values** — look at variable states at the divergence point
4. **Check for missing logs** — if an expected log step is absent, that code path wasn't reached
5. **Correlate timestamps** — use the `ts` field to identify timing issues or ordering problems

## Step 5: Report findings and fix

Once you've identified the root cause:

1. Explain to the user what you found, referencing specific log entries
2. Propose a fix
3. Remove all the `_clog` instrumentation you added (the logging was temporary)
4. Clean up: `clog clear`

## Important notes

- Always remove instrumentation after debugging. The `_clog` calls are not production code.
- If the first round of logs isn't enough, add more targeted instrumentation and ask the user to reproduce again.
- If `clog status` shows the server is dead mid-session, restart it with `clog start`.
- The log file is at `~/.clog/logs/clog.ndjson` — each line is `{"ts":"...","data":{...}}`.
