---
name: logs
description: View shella daemon and plugin logs. Use when debugging issues, checking what happened, or monitoring plugin output.
argument-hint: "[plugin-name] [lines]"
allowed-tools: Bash(tail:*), Bash(grep:*), Bash(cat:*), Bash(wc:*), Read
---

# Shella Logs

View daemon and plugin logs from `~/.local/state/shella/dev.log`.

## Arguments

- `$ARGUMENTS` may contain:
  - A plugin name to filter by (e.g., "agent", "terminal")
  - A number of lines to show (default: 50)
  - "all" to show more lines
  - "errors" or "error" to filter to errors/warnings only

## Log File Location

```
~/.local/state/shella/dev.log
```

Each line is JSON with fields: `time`, `level`, `prefix`, `msg`, and optional data fields.

## Commands

**Recent logs (last 50 lines)**:
```bash
tail -50 ~/.local/state/shella/dev.log
```

**Filter by plugin** (prefix field contains plugin name):
```bash
grep '"prefix":"agent' ~/.local/state/shella/dev.log | tail -50
```

**Errors only**:
```bash
grep '"level":"error"' ~/.local/state/shella/dev.log | tail -50
```

**Parse and format** for readability - extract time, prefix, level, msg:
```bash
tail -50 ~/.local/state/shella/dev.log | while read line; do
  echo "$line" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(f'{d.get(\"prefix\",\"daemon\"):20} {d.get(\"level\",\"info\"):5} {d.get(\"msg\",\"\")}')" 2>/dev/null || echo "$line"
done
```

## Output

Present logs in a readable format. For JSON lines, extract the key fields (timestamp, prefix, level, message). Highlight errors in your response.

If the log file doesn't exist, tell the user the daemon hasn't been run yet or logs are empty.
