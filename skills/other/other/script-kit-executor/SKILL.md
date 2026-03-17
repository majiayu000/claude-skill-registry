---
name: script-kit-executor
description: Script execution engine and builtins for script-kit-gpui
---

# script-kit-executor

The executor module is responsible for running TypeScript/JavaScript scripts with bidirectional JSONL communication. It handles process lifecycle management, SDK preloading, scriptlet execution, error handling, and selected text operations.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Script Execution Flow                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   User selects script                                                │
│          │                                                           │
│          ▼                                                           │
│   ┌──────────────────┐                                               │
│   │ execute_script_  │  1. Find SDK path (~/.scriptkit/sdk/)         │
│   │ interactive()    │  2. Find bun/node executable                  │
│   │ [runner.rs]      │  3. Spawn with process_group(0)               │
│   └────────┬─────────┘                                               │
│            │                                                         │
│            ▼                                                         │
│   ┌──────────────────┐     ┌──────────────────┐                      │
│   │  ScriptSession   │────▶│  SplitSession    │                      │
│   │  (unified)       │     │  (for threading) │                      │
│   └────────┬─────────┘     └──────────────────┘                      │
│            │                        │                                │
│            │ split()                │                                │
│            ▼                        ▼                                │
│   ┌──────────────────┐     ┌──────────────────┐                      │
│   │  Writer Thread   │     │  Reader Thread   │                      │
│   │  (stdin)         │     │  (stdout/stderr) │                      │
│   └──────────────────┘     └──────────────────┘                      │
│            │                        │                                │
│            │  JSONL Messages        │                                │
│            ▼                        ▼                                │
│   ┌────────────────────────────────────────────┐                     │
│   │          Script Process (bun/node)          │                    │
│   │  ┌──────────────────────────────────────┐  │                     │
│   │  │         SDK Preload (kit-sdk.ts)     │  │                     │
│   │  │  - Global functions: arg, div, md    │  │                     │
│   │  │  - IPC message handling              │  │                     │
│   │  └──────────────────────────────────────┘  │                     │
│   └────────────────────────────────────────────┘                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Execution Flow

### 1. Script Discovery and Validation

When a script is selected, the executor:
1. Validates the path exists and has proper encoding
2. Determines file type (TypeScript `.ts` or JavaScript `.js`)
3. Locates the SDK for preloading globals

### 2. Runtime Selection

The executor tries runtimes in order of preference:

```
1. bun with SDK preload (preferred for TypeScript)
   └── Command: bun run --preload ~/.scriptkit/sdk/kit-sdk.ts script.ts

2. bun without preload (fallback)
   └── Command: bun run script.ts

3. node (for JavaScript files)
   └── Command: node script.js
```

### 3. Process Spawning

Scripts are spawned with:
- **Piped stdio**: stdin, stdout, stderr all captured
- **Process groups** (Unix): `process_group(0)` creates new PGID equal to PID
- **Process tracking**: Registered with global `PROCESS_MANAGER`

```rust
// Key spawn configuration
let mut command = Command::new(&executable);
command
    .args(args)
    .stdin(Stdio::piped())
    .stdout(Stdio::piped())
    .stderr(Stdio::piped());

#[cfg(unix)]
command.process_group(0);  // PID becomes PGID
```

### 4. Session Splitting

After spawn, the session is split for concurrent I/O:

```rust
pub struct SplitSession {
    pub stdin: ChildStdin,           // Writer thread owns this
    pub stdout_reader: JsonlReader,   // Reader thread owns this
    pub stderr: Option<ChildStderr>,  // Captured for error reporting
    pub child: Child,
    pub process_handle: ProcessHandle, // MUST stay alive until script exits
}
```

## IPC Communication

### JSONL Protocol

All communication uses newline-delimited JSON (JSONL):

```
Script → App:  {"type":"ARG","prompt":"Enter name"}\n
App → Script:  {"type":"SUBMIT","id":"abc123","value":"John"}\n
```

### Message Handling Categories

1. **Prompt Messages** → Sent to UI via async_channel
2. **Direct Handlers** → Processed in reader thread:
   - `GetSelectedText`, `SetSelectedText`
   - `CheckAccessibility`, `RequestAccessibility`
   - `Clipboard`, `ClipboardHistory`
   - `WindowList`, `WindowAction`

### Writer Thread

```rust
// Bounded channel prevents OOM from slow scripts
let (response_tx, response_rx) = mpsc::sync_channel::<Message>(100);

// Writer thread serializes and sends responses
loop {
    match response_rx.recv() {
        Ok(response) => {
            let json = serialize_message(&response)?;
            writeln!(stdin, "{}", json)?;
            stdin.flush()?;
        }
        Err(_) => break,
    }
}
```

### Reader Thread

```rust
// Event-driven message reading
loop {
    match stdout_reader.next_message_graceful_with_handler(|issue| {
        // Handle protocol parse issues
    }) {
        Ok(Some(msg)) => {
            // Handle message based on type
            match &msg {
                Message::GetSelectedText { .. } => handle_directly(),
                _ => send_to_ui(tx.send_blocking(msg)),
            }
        }
        Ok(None) => break,  // EOF
        Err(e) => break,    // Error
    }
}
```

## Builtins

The `builtins.rs` module provides built-in features that appear in the main search alongside scripts:

### Feature Categories

| Category | Features |
|----------|----------|
| **Core** | Clipboard History, Window Switcher, AI Chat, Notes |
| **System Actions** | Lock Screen, Sleep, Restart, Shut Down, Volume controls |
| **Window Actions** | Tile Left/Right/Top/Bottom, Maximize, Minimize |
| **Script Commands** | New Script, New Scriptlet |
| **Permissions** | Check Permissions, Request Accessibility |
| **Utilities** | Scratch Pad, Quick Terminal |

### Built-in Entry Structure

```rust
pub struct BuiltInEntry {
    pub id: String,           // "builtin-clipboard-history"
    pub name: String,         // "Clipboard History"
    pub description: String,  // "View and manage clipboard history"
    pub keywords: Vec<String>,// ["clipboard", "paste", "copy"]
    pub feature: BuiltInFeature,
    pub icon: Option<String>, // Emoji icon
    pub group: BuiltInGroup,  // Core or MenuBar
}
```

### Configuration

Builtins are toggled via `BuiltInConfig`:

```rust
pub struct BuiltInConfig {
    pub clipboard_history: bool,  // default: true
    pub app_launcher: bool,       // default: true (apps in main search)
    pub window_switcher: bool,    // default: true
}
```

## Scriptlet Execution

Scriptlets are small scripts embedded in markdown, supporting various tool types:

### Supported Tools

| Tool | Extension | Runtime |
|------|-----------|---------|
| `bash`, `sh`, `zsh`, `fish` | `.sh` | Shell |
| `python` | `.py` | python3 |
| `ruby` | `.rb` | ruby |
| `node`, `js` | `.js` | node |
| `kit`, `ts`, `bun`, `deno` | `.ts` | bun with SDK |
| `applescript` | - | osascript |
| `transform` | `.ts` | bun (get/set selected text) |
| `open` | - | open/xdg-open |
| `paste`, `type`, `submit` | - | Accessibility (macOS only) |

### Scriptlet Execution Flow

```rust
pub fn run_scriptlet(scriptlet: &Scriptlet, options: ScriptletExecOptions) {
    // 1. Process conditionals (if/else based on flags)
    let content = process_conditionals(&content, &options.flags);
    
    // 2. Variable substitution
    let content = format_scriptlet(&content, &options.inputs, &options.positional_args);
    
    // 3. Apply prepend/append
    let content = build_final_content(&content, &options.prepend, &options.append);
    
    // 4. Execute based on tool type
    match tool {
        "bash" | "sh" | "zsh" => execute_shell_scriptlet(),
        "python" => execute_with_interpreter("python3"),
        "kit" | "ts" => execute_typescript(),
        "transform" => execute_transform(),  // macOS only
        // ...
    }
}
```

## Error Handling

### Stack Trace Parsing

```rust
pub fn parse_stack_trace(stderr: &str) -> Option<String> {
    // Looks for patterns:
    // - Lines starting with "at "
    // - Error:, TypeError:, ReferenceError:, SyntaxError:
    // Returns up to 20 lines of stack trace
}
```

### Suggestion Generation

Based on error patterns and exit codes:

| Pattern | Suggestion |
|---------|------------|
| "cannot find module" | Run 'bun install' |
| "syntaxerror" | Check for syntax errors |
| "referenceerror" | Check imports/definitions |
| Exit code 127 | Command not found |
| Exit code 137 (SIGKILL) | Out of memory or killed |
| Exit code 139 (SIGSEGV) | Memory access violation |

### Stderr Buffer

A ring buffer captures stderr for post-mortem analysis:

```rust
pub struct StderrBuffer {
    lines: Arc<Mutex<VecDeque<String>>>,
    max_lines: usize,    // default: 500
    max_bytes: usize,    // default: 4KB
}

// Usage
let capture = spawn_stderr_reader(stderr, script_path);
// ... script runs ...
let stderr_text = capture.get_contents_with_timeout(Duration::from_millis(100));
```

## Process Cleanup

### ProcessHandle

Tracks process lifetime and ensures cleanup:

```rust
pub struct ProcessHandle {
    pid: u32,
    script_path: String,
    killed: bool,
}

impl Drop for ProcessHandle {
    fn drop(&mut self) {
        PROCESS_MANAGER.unregister_process(self.pid);
        self.kill();  // SIGTERM → wait 250ms → SIGKILL
    }
}
```

### Kill Escalation Protocol

```
1. Send SIGTERM to process group
2. Poll every 50ms for up to 250ms
3. If still alive, send SIGKILL
```

## Auto-Submit Mode

For autonomous testing, enable via environment variables:

| Variable | Description |
|----------|-------------|
| `AUTO_SUBMIT=true` | Enable auto-submit |
| `AUTO_SUBMIT_DELAY_MS=200` | Delay before submit (default: 100) |
| `AUTO_SUBMIT_VALUE=foo` | Override value to submit |
| `AUTO_SUBMIT_INDEX=2` | Select choice by index |

```rust
pub struct AutoSubmitConfig {
    pub enabled: bool,
    pub delay: Duration,
    pub value_override: Option<String>,
    pub index: usize,
}
```

## Anti-patterns

### 1. Dropping ProcessHandle Early

```rust
// WRONG: ProcessHandle dropped, kills the script immediately
let session = execute_script_interactive(&path)?;
drop(session);  // Script is killed!

// CORRECT: Keep session alive until script completes
let session = execute_script_interactive(&path)?;
// ... use session ...
let exit_code = session.wait()?;
```

### 2. Blocking on stdin/stdout in Same Thread

```rust
// WRONG: Deadlock risk
loop {
    let msg = session.receive_message()?;  // Blocks
    session.send_message(&response)?;       // Can't reach if blocked
}

// CORRECT: Split into separate threads
let split = session.split();
std::thread::spawn(move || { /* writer */ });
std::thread::spawn(move || { /* reader */ });
```

### 3. Ignoring Stderr

```rust
// WRONG: Stderr lost, no error context
let output = command.output()?;
println!("{}", String::from_utf8_lossy(&output.stdout));

// CORRECT: Capture stderr for error reporting
let stderr_capture = spawn_stderr_reader(child.stderr.take().unwrap(), path);
// ... on error ...
let stderr = stderr_capture.get_contents_with_timeout(Duration::from_millis(100));
```

### 4. Not Using process_group(0)

```rust
// WRONG: Child processes become orphans
command.spawn()?;

// CORRECT: All children share PGID, can be killed together
#[cfg(unix)]
command.process_group(0);
command.spawn()?;
```

### 5. Unbounded Channels

```rust
// WRONG: OOM risk if script doesn't consume messages
let (tx, rx) = async_channel::unbounded();

// CORRECT: Backpressure via bounded channel
let (tx, rx) = async_channel::bounded(100);
```

## Key Files

| File | Purpose |
|------|---------|
| `runner.rs` | Core execution, process spawning, SDK loading |
| `scriptlet.rs` | Scriptlet parsing and tool-specific execution |
| `errors.rs` | Stack trace parsing, suggestion generation |
| `selected_text.rs` | GetSelectedText/SetSelectedText handlers |
| `stderr_buffer.rs` | Ring buffer for stderr capture |
| `auto_submit.rs` | Testing automation configuration |
| `mod.rs` | Module exports and re-exports |
