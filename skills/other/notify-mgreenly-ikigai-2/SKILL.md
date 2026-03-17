---
name: notify
description: Send push notifications to the user via ntfy.sh
---

# Notify

Send push notifications when user attention is needed.

## Usage

```bash
echo '{"title": "Title", "message": "Body"}' | .claude/scripts/notify
```

## Input

- `title` - optional
- `message` - required

## Output

```json
{"success": true, "status": 200}
{"success": false, "status": 401, "error": "..."}
```

## Example

```bash
$ echo '{"title": "Build Complete", "message": "All tests passed"}' | .claude/scripts/notify
{"success":true,"status":200}

$ echo '{"title": "Test"}' | .claude/scripts/notify
{"success":false,"error":"message is required"}
```
