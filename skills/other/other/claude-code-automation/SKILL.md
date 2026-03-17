---
name: claude-code-automation
description: Run Claude Code programmatically in headless mode or via bidirectional stream-json protocol. Use when building agents, automating Claude, running headless Claude, implementing multi-turn conversations, or integrating Claude CLI into applications.
---

# Claude Code Automation

This skill covers running Claude Code programmatically - either one-shot with `--print` or multi-turn with the bidirectional stream-json protocol.

## Quick Reference

| Mode | Use Case | Key Flags |
|------|----------|-----------|
| Headless (`--print`) | One-shot tasks, background agents | `--print --verbose --output-format stream-json` |
| Bidirectional | Multi-turn conversations, persistent sessions | `--input-format stream-json --output-format stream-json --verbose` |

## Headless Mode (`--print`)

For one-shot execution without interactive prompts.

### Essential Flags

```bash
claude --print \
  --verbose \                              # REQUIRED with stream-json
  --output-format stream-json \
  --model sonnet \
  --permission-mode bypassPermissions \    # Enable file writes
  --append-system-prompt "context here"    # Inject dynamic context
```

### Critical Gotchas

1. **`--verbose` is required** with `stream-json` output - without it, Claude exits silently with status 1

2. **File writes silently fail** without `--permission-mode bypassPermissions`

3. **Session hooks don't run** in `--print` mode - no SessionStart/SessionEnd

4. **`--append-system-prompt` is ephemeral** - NOT re-applied on `--resume`

### Rust Implementation

```rust
pub fn run_headless_claude(prompt: &str, working_dir: &Path, system_prompt: &str) -> Result<()> {
    let mut cmd = Command::new("claude")
        .arg("--print")
        .arg("--verbose")
        .arg("--model").arg("sonnet")
        .arg("--output-format").arg("stream-json")
        .arg("--permission-mode").arg("bypassPermissions")
        .arg("--append-system-prompt").arg(system_prompt)
        .current_dir(working_dir)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    // Write prompt to stdin, process output...
    Ok(())
}
```

## Bidirectional Protocol

For multi-turn conversations with a persistent Claude process.

### Starting a Session

```bash
claude --input-format stream-json --output-format stream-json --verbose
```

### Message Types

**1. Initialize (set system prompt once)**
```json
{
  "subtype": "initialize",
  "systemPrompt": "Custom system prompt",
  "appendSystemPrompt": "Additional context"
}
```

**2. Send user messages**
```json
{
  "type": "user",
  "session_id": "",
  "message": {
    "role": "user",
    "content": [{"type": "text", "text": "Your question here"}]
  },
  "parent_tool_use_id": null
}
```

### Critical Gotcha: control_response

`control_response` is a **top-level type**, NOT a subtype of system:

```rust
// WRONG - never matches
if event.get("type") == Some("system")
    && event.get("subtype") == Some("control_response") { ... }

// CORRECT
if event.get("type") == Some("control_response") {
    info!("Session initialized");
}
```

### Rust Session Pattern

```rust
pub struct ClaudeSession {
    process: Child,
    stdin: ChildStdin,
}

impl ClaudeSession {
    pub fn new(system_prompt: &str) -> Result<Self> {
        let mut process = Command::new("claude")
            .arg("--input-format").arg("stream-json")
            .arg("--output-format").arg("stream-json")
            .arg("--verbose")
            .arg("--model").arg("sonnet")
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()?;

        let mut stdin = process.stdin.take().unwrap();

        // Send initialize message
        let init = serde_json::json!({
            "subtype": "initialize",
            "appendSystemPrompt": system_prompt
        });
        writeln!(stdin, "{}", init)?;
        stdin.flush()?;

        Ok(Self { process, stdin })
    }

    pub fn send_message(&mut self, text: &str) -> Result<()> {
        let msg = serde_json::json!({
            "type": "user",
            "session_id": "",
            "message": {
                "role": "user",
                "content": [{"type": "text", "text": text}]
            },
            "parent_tool_use_id": null
        });
        writeln!(self.stdin, "{}", msg)?;
        self.stdin.flush()?;
        Ok(())
    }
}
```

## Reading JSONL Transcripts

Claude session transcripts can be large. Direct file reads often fail.

**Size limits:**
- 256KB maximum for direct reads
- Individual JSONL lines can be 50k+ characters

**Working solutions:**
```bash
# Extract specific fields with jq
jq -r 'select(.type == "user") | .message.content' file.jsonl | head -20

# Python for complex extraction
python3 -c "
import json
for line in open('file.jsonl'):
    obj = json.loads(line)
    if obj.get('type') == 'user':
        print(obj.get('message', {}).get('content', '')[:200])
"
```

## When to Use Which

**Use headless (`--print`) for:**
- One-off background agents
- Each invocation needs different context
- Truly independent sessions
- Simple automation scripts

**Use bidirectional for:**
- Multi-turn conversations
- When system prompt must persist across messages
- Building interactive applications
- When `--resume` behavior is insufficient

**Use interactive (normal) for:**
- Human conversations
- Sessions requiring workspace trust dialogs
- When hooks are essential
