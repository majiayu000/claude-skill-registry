---
name: tasker-cli
description: Deploy and trigger Tasker tasks on Android. Use for automating Android via Tasker WebUI and adb.
---

# Usage

## First-time setup

```bash
# On phone: Tasker → Preferences → UI → enable "Use Tasker 2025 UI (VERY EARLY)"
# Open any task for editing, tap ⋮ → WebUI
export TASKER_HOST=192.168.1.100
tasker-cli sync-specs
```

## Deploy a task

```bash
tasker-cli deploy task.json --replace   # clear + deploy
tasker-cli deploy task.json --append    # append to existing
tasker-cli deploy task.json --dry-run   # validate only
cat task.json | tasker-cli deploy -     # from stdin
```

## Task definition format

```json
{
  "actions": [
    {
      "action": "Variable Set",
      "args": { "Name": "%url", "To": "https://api.example.com/data" }
    },
    {
      "action": "HTTP Request",
      "args": { "Method": "0", "URL": "%url", "Timeout (Seconds)": "30" }
    },
    { "action": "Flash", "args": { "Text": "Result: %HTTPD" } }
  ]
}
```

Rules:

- Use human-readable action and arg names (from `tasker-cli specs`)
- All arg values must be strings (booleans: `"true"`/`"false"`)
- Use `tasker-cli specs --search <term>` to find action names and required args

## Conditions and control flow

Conditions use `{"e": <lhs>, "b": <operator>, "f": <rhs>}`. Multiple
conditions on one action are ANDed.

String operators: `EqualsString`, `NotEqualsString`, `Matches`, `NotMatches`,
`MatchesRegex`, `NotMatchesRegex`

Math operators: `Equals`, `NotEquals`, `LessThan`, `MoreThan`, `Even`, `Odd`

State operators: `Set`, `NotSet` (no `"f"` value needed)

```json
{"action": "Flash", "args": {"Text": "Low!"}, "condition": [{"e": "%BATT", "b": "LessThan", "f": "20"}]}
{"action": "Stop", "args": {"With Error": "false"}, "condition": [{"e": "%par2", "b": "Equals", "f": "enter"}, {"e": "%GF", "b": "NotEqualsString", "f": "%par1"}]}
{"action": "If", "args": {}, "condition": [{"e": "%BATT", "b": "LessThan", "f": "20"}]}
{"action": "Else"}
{"action": "End If"}
```

## Quirks and pitfalls

### Condition operators must be exact

The WebUI silently accepts invalid operator names but drops the `"b"` field,
producing a broken condition that crashes Tasker with a NullPointerException.
Always use the exact operator names listed above.

### JavaScriptlet cannot see variables with numbers in the name

`%caller1`, `%arr3` etc are invisible to JavaScriptlet. Copy them to a
plain variable first:

```json
{
  "action": "Variable Set",
  "args": { "Name": "%callerinfo", "To": "%caller1" }
}
```

### JavaScriptlet requires Auto Exit for variable export

With `"Auto Exit": "true"` (the default in Tasker's UI but **false** when
omitted in JSON), variables declared with `var` are automatically exported
to Tasker. Without it the JavaScriptlet hangs until timeout. Always set it:

```json
{
  "action": "JavaScriptlet",
  "args": {
    "Code": "var x = 1;",
    "Auto Exit": "true",
    "Timeout (Seconds)": "45"
  }
}
```

### Boolean args need native JSON booleans

String `"true"` silently becomes `false` in the WebUI. Use actual booleans
for boolean-typed args: `"Auto Exit": "true"` works because tasker-cli
coerces it, but the wire format sends `true` not `"true"`.

### Profile caller variable

When a profile triggers a task directly, `%caller1` contains
`profile=enter:Profile Name` or `profile=exit:Profile Name`.
When called via Perform Task, `%caller1` is `task=Task Name`
and `%caller2` has the profile info.

### Global variables need uppercase

`%GF_CURRENT` is global (survives across tasks). `%place` is local
(lowercase, scoped to the current task invocation).

## Other commands

```bash
tasker-cli ping                       # check WebUI connectivity
tasker-cli show                       # show current task actions
tasker-cli specs --search flash       # search action specs
tasker-cli trigger "My Task" --par1 "value"
```

## Environment variables

- `TASKER_HOST` — phone IP (required, or use --host)
- `TASKER_WEBUI_PORT` — WebUI port (default: 8745)
- `TASKER_ADB_PORT` — adb port (default: auto-detect)
