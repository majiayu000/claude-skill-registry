---
name: reload
description: Treat the current session and auto-resume in a new terminal window.
argument-hint: "[gentle|standard|aggressive]"
disable-model-invocation: true
allowed-tools: Bash(cozempic *), AskUserQuestion
---

Treat the session and spawn an auto-resume watcher that opens a new terminal after you exit.

## Steps

1. **Diagnose first**:
   ```bash
   cozempic current --diagnose
   ```

2. **Dry-run**:
   ```bash
   cozempic treat current -rx $ARGUMENTS
   ```
   If no argument was provided, use `standard`:
   ```bash
   cozempic treat current -rx standard
   ```

3. **Show results** including token savings. Ask confirmation.

4. **Apply reload** (treats + saves + spawns watcher in one shot):
   ```bash
   cozempic reload -rx $ARGUMENTS
   ```
   **Do NOT run `cozempic treat --execute` before `cozempic reload`** — reload already treats internally. Running both would double-treat.

5. **Tell the user**: "Treatment applied. Type `/exit` — a new Terminal window will open automatically with the pruned session."
