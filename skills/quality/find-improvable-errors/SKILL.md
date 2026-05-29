---
name: find-improvable-errors
description: Analyze MCP tool errors across exports to find unhelpful error messages and recommend improvements.
---

# Find Improvable Error Messages

Analyze MCP tool errors across game exports to find error messages that models struggle to recover from. Uses `scripts/analysis/toolbox/mcp_errors.py`.

## Workflow

### Step 1: Run the analysis

Run against all exported games:

```bash
uv run python scripts/analysis/toolbox/mcp_errors.py website/public/games/
```

### Step 2: Identify candidates

Focus on the "Least helpful error messages" section — these are messages where models retry with the same error, meaning the message didn't help them understand what to do differently.

Key metrics:

- **Stuck rate** = same_error retries / total occurrences. Above 20% is bad.
- **Recovery rate** = successful retries / total occurrences. Below 30% is concerning.
- **Volume** matters — a 50% stuck rate on 2 occurrences is noise; on 60 occurrences it's a real problem.

### Step 3: Diagnose why each message fails

For the top 3-5 worst messages, investigate:

1. **Read the error message text.** Is it clear what the model should do differently?
2. **Check the action_type breakdown.** Is the error specific to one action type or spread across many?
3. **Check the model breakdown.** Is it one model struggling or all of them?
4. **Look at example failures.** Sample a few stuck cases from a game export to see what args the model sent and what it tried on retry:

   ```bash
   uv run python -c "
   import gzip, json, glob
   for gz in sorted(glob.glob('website/public/games/*.json.gz'))[-10:]:
       d = json.load(gzip.open(gz, 'rt'))
       events = d.get('llmEvents', [])
       for i, e in enumerate(events):
           if e.get('type') != 'tool_call' or e.get('tool') != 'choose_action': continue
           r = json.loads(e.get('result', '{}'))
           if r.get('error', '') == 'THE ERROR MESSAGE HERE':
               # Show this error and the next tool call from same player
               print(f'Game: {d.get(\"id\")}, Player: {e.get(\"player\")}')
               print(f'  Args: {e.get(\"args\")}')
               print(f'  Result: {e.get(\"result\")[:200]}')
               for j in range(i+1, min(i+5, len(events))):
                   nxt = events[j]
                   if nxt.get('player') == e.get('player') and nxt.get('type') == 'tool_call':
                       print(f'  Next: {nxt.get(\"tool\")} args={nxt.get(\"args\")}')
                       print(f'  Next result: {nxt.get(\"result\", \"\")[:200]}')
                       break
               print()
   "
   ```

5. **Read the Java error site.** Find where `buildError` is called for this message in `BridgeCallbackHandler.java` and understand the context.

### Step 4: Fix the messages

For each improvable message, edit the error string in `BridgeCallbackHandler.java`. Good error messages should:

- **Name the action type** (e.g. "GAME_SELECT requires..." not just "Provide 'index'...")
- **State what params are expected** and what each one does
- **Tell the model what to do first** if it needs to call another tool (e.g. "Call get_action_choices first")
- **Include diagnostic data** where cheap (e.g. valid index range, number of choices)
- **Stay concise** — don't dump full tool docs, just the relevant hint for this specific error

After editing, regenerate the tools JSON:

```bash
mvn -pl Mage.Client.Bridge -am compile -q
make regen-mcp-tools
```

### Step 5: Update the analysis script if needed

If you find error patterns that `mcp_errors.py` doesn't capture well (e.g. new error codes, different tool failures), update the script in `scripts/analysis/toolbox/`. The script should grow to cover new patterns over time.

### Step 6: Verify

```bash
make check
```

### Step 7: Re-run analysis to confirm

Run the analysis again to verify the old bad messages are gone (they'll still appear in historical data but new games should use the improved messages):

```bash
uv run python scripts/analysis/toolbox/mcp_errors.py website/public/games/
```
