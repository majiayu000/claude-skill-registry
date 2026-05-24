---
name: ttt
description: |
  Tmux Talk To - ส่งข้อความไปยัง tmux session อื่น
  ใช้สำหรับ: Multi-agent coordination, parallel execution, workflow automation
model: haiku
allowed-tools: Bash
---

# Tmux Talk To (ttt)

เมื่อ user พิมพ์ `/ttt` ให้ส่งข้อความไปยัง tmux session อื่น

## Usage

```bash
/ttt <session_name> <message>
/ttt <session_name> --esc <message>  # ส่ง ESC ก่อนส่งข้อความ
/ttt --list                          # แสดง tmux sessions ที่มี
```

## Step 1: Parse Arguments

```bash
# Extract session name and message from arguments
SESSION_NAME="$1"
MESSAGE="${@:2}"

# Check for --esc flag
ESC_MODE=false
if [[ "$2" == "--esc" ]]; then
    ESC_MODE=true
    MESSAGE="${@:3}"
fi

# Check for --list flag
if [[ "$1" == "--list" ]]; then
    tmux list-sessions
    exit 0
fi
```

## Step 2: Validate Session

```bash
# Check if session exists
if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "❌ Error: Session '$SESSION_NAME' not found"
    echo ""
    echo "Available sessions:"
    tmux list-sessions
    exit 1
fi
```

## Step 3: Send Message

```bash
# If ESC mode, send ESC first
if [[ "$ESC_MODE" == "true" ]]; then
    tmux send-keys -t "$SESSION_NAME" C-[
    sleep 0.2
fi

# Send message with Enter
tmux send-keys -t "$SESSION_NAME" "$MESSAGE" C-m

echo "✅ ส่งข้อความไปยัง $SESSION_NAME แล้ว"
echo "Message: $MESSAGE"
```

## Examples

### Example 1: Send Simple Message
```bash
/ttt gemini1 "สวัสดี"
# Result: ส่ง "สวัสดี" ไปยัง gemini1 พร้อมกด Enter
```

### Example 2: Send with ESC (if session stuck)
```bash
/ttt gemini1 --esc "สวัสดี"
# Result: กด ESC ก่อน แล้วส่ง "สวัสดี" ไปยัง gemini1
```

### Example 3: List Sessions
```bash
/ttt --list
# Result: แสดง tmux sessions ทั้งหมด
```

### Example 4: Complex Message
```bash
/ttt gemini1 "create workflow for Facebook login"
# Result: ส่งคำสั่งซับซ้อนไปยัง gemini1
```

## Advanced Usage

### Cross-Session Communication
ถ้าต้องการส่งข้อความไปหลาย sessions:

```bash
/ttt gemini1 "analyze workflow" && sleep 1 && /ttt claude1 "summarize results"
```

### Capture Response (Manual)
```bash
# Send message
/ttt gemini1 "hello"

# Wait a bit, then capture response
tmux capture-pane -t gemini1 -p | tail -20
```

## Important Notes

- **C-m**: Enter key in tmux
- **C-[**: ESC key - Use when shell stuck
- **Sleep delay**: Add `sleep 0.5` between commands if needed
- **Session validation**: Always check if session exists first

## Troubleshooting

### Problem: Message not appearing
**Solution**: Try with `--esc` flag to clear any stuck input

```bash
/ttt gemini1 --esc "your message"
```

### Problem: Session not found
**Solution**: List available sessions first

```bash
/ttt --list
```

### Problem: Complex message with quotes
**Solution**: Use single quotes for message

```bash
/ttt gemini1 'say "hello world"'
```

---

ARGUMENTS: $ARGS

## Implementation

Run the following command:

```bash
SESSION_NAME="$1"
shift

# Handle flags
ESC_MODE=false
if [[ "$1" == "--list" ]]; then
    echo "📋 Available tmux sessions:"
    echo ""
    tmux list-sessions
    exit 0
fi

if [[ "$1" == "--esc" ]]; then
    ESC_MODE=true
    shift
fi

MESSAGE="$*"

# Validate session
if [[ -z "$SESSION_NAME" ]]; then
    echo "❌ Error: No session name provided"
    echo ""
    echo "Usage: /ttt <session_name> <message>"
    echo "       /ttt --list"
    exit 1
fi

if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "❌ Error: Session '$SESSION_NAME' not found"
    echo ""
    echo "Available sessions:"
    tmux list-sessions
    exit 1
fi

# Send ESC if needed
if [[ "$ESC_MODE" == "true" ]]; then
    tmux send-keys -t "$SESSION_NAME" C-[
    sleep 0.2
    echo "⎋ Sent ESC to $SESSION_NAME"
fi

# Send message
tmux send-keys -t "$SESSION_NAME" "$MESSAGE" C-m

echo "✅ ส่งข้อความไปยัง $SESSION_NAME แล้ว"
echo "📤 Message: $MESSAGE"
```
