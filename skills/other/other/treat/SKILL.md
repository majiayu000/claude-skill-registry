---
name: treat
description: Prune bloated session with a prescription. Removes progress ticks, stale reads, duplicate content, and more.
argument-hint: "[gentle|standard|aggressive]"
disable-model-invocation: true
allowed-tools: Bash(cozempic *), AskUserQuestion
---

Apply a pruning prescription to the current session. Default is `standard` if no argument given.

**When to use `treat` vs `reload`:** prefer the `reload` skill — it does the same prune plus auto-resume in one step (`/exit` → new terminal opens with the pruned session). Use `treat` only when the user explicitly wants to stay in the current session, work in a multi-pane setup, or resume manually.

## Steps

1. **Diagnose first** — show the user what they're working with:
   ```bash
   cozempic current --diagnose
   ```

2. **Dry-run the treatment** — show savings without applying:
   ```bash
   cozempic treat current -rx $ARGUMENTS
   ```
   If no argument was provided, use `standard`:
   ```bash
   cozempic treat current -rx standard
   ```

3. **Show results** — present the dry-run output including token savings (the `Tokens:` line). Always surface both byte and token savings.

4. **Ask confirmation** — use AskUserQuestion to confirm before applying.

5. **Apply on confirmation**:
   ```bash
   cozempic treat current -rx $ARGUMENTS --execute
   ```

6. **Tell the user**: "Treatment applied. A backup was created automatically. To resume with the pruned session, exit and run `claude --resume`. (Tip: next time, the `reload` skill does this in one step — `/exit` and a fresh terminal opens automatically.)"

## Prescriptions

| Rx | Strategies | Typical Savings |
|----|-----------|----------------|
| `gentle` | progress-collapse, file-history-dedup, metadata-strip | 40-55% |
| `standard` | gentle + thinking-blocks, tool-output-trim, stale-reads, system-reminder-dedup | 50-70% |
| `aggressive` | standard + error-retry-collapse, document-dedup, mega-block-trim, envelope-strip | 70-95% |

## Safety
- Always dry-run first — never execute without showing the user what will change
- Backups are automatic (timestamped .bak files)
- Never touches uuid/parentUuid — conversation DAG stays intact
