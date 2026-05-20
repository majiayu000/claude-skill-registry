---
name: remember
description: Quickly save a memory to the soul
execution: direct
args: content to remember
---

# Remember

Quickly store something in soul memory.

## Usage

```
/remember <what to remember>
```

## Process

1. **Parse input** - Extract the content after `/remember`
2. **Format as SSL** - Wrap in appropriate domain tag if not already formatted
3. **Store** - Call `remember` tool
4. **Confirm** - Show what was stored

## SSL Formatting

If input doesn't start with `[domain]`, auto-detect and wrap:

| Pattern | Domain |
|---------|--------|
| "prefer..." / "always..." / "never..." | `[preference]` |
| "when X, do Y" | `[pattern]` |
| "watch out..." / "gotcha..." | `[gotcha]` |
| "decided..." / "chose..." | `[decision]` |
| Other | `[note]` |

## Tool Call

```json
{
  "tool": "remember",
  "args": {
    "content": "[domain] formatted content here",
    "tags": ["user-added"]
  }
}
```

## Examples

```
/remember always run tests before committing
→ [preference] always run tests before committing

/remember when debugging, check logs first
→ [pattern] when debugging → check logs first

/remember gotcha: the API returns 200 even on errors
→ [gotcha] the API returns 200 even on errors
```

## Output

```
Remembered: [domain] content
```
