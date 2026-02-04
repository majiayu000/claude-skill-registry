---
name: portable-pty
description: Cross-platform pseudo-terminal (PTY) management for spawning shell processes
---

# portable-pty

Cross-platform PTY (pseudo-terminal) library from the WezTerm project. Provides a unified API for working with PTYs on macOS, Linux, and Windows.

## Platform Support

| Platform | Implementation |
|----------|----------------|
| macOS    | Native PTY via `/dev/ptmx` |
| Linux    | Native PTY via `/dev/ptmx` or `/dev/pts` |
| Windows  | ConPTY (Windows 10 1809+) |

## Key Types

### `PtySystem` (trait)
Factory for creating PTY pairs. Get the native implementation with:
```rust
use portable_pty::native_pty_system;
let pty_system = native_pty_system();
```

### `PtyPair` (struct)
Contains the master and slave ends of a PTY:
```rust
struct PtyPair {
    pub master: Box<dyn MasterPty + Send>,
    pub slave: Box<dyn SlavePty + Send>,
}
```

### `MasterPty` (trait)
The control end of the PTY. Key methods:
- `resize(PtySize)` - Notify kernel of size change (sends SIGWINCH)
- `get_size()` - Query current PTY size
- `try_clone_reader()` - Get readable handle for child output
- `take_writer()` - Get writable handle for child input (call once!)
- `process_group_leader()` - Get PID of session leader
- `as_raw_fd()` - Get underlying file descriptor (Unix)

### `SlavePty` (trait)
The process end of the PTY:
- `spawn_command(CommandBuilder)` - Spawn a process into the PTY

### `Child` (trait)
Handle to spawned process:
- `try_wait()` - Non-blocking check if process exited
- `wait()` - Block until process exits
- `kill()` - Terminate the process (SIGKILL on Unix)
- `process_id()` - Get the PID

### `PtySize` (struct)
Terminal dimensions:
```rust
PtySize {
    rows: u16,        // Number of text lines
    cols: u16,        // Number of text columns
    pixel_width: u16, // Width in pixels (optional, often 0)
    pixel_height: u16 // Height in pixels (optional, often 0)
}
```

### `CommandBuilder` (struct)
Build commands to spawn. Similar to `std::process::Command`:
```rust
let mut cmd = CommandBuilder::new("bash");
cmd.arg("-c");
cmd.arg("echo hello");
cmd.env("TERM", "xterm-256color");
cmd.cwd("/home/user");
```

## Usage in script-kit-gpui

The `PtyManager` in `src/terminal/pty.rs` wraps portable-pty:

```rust
pub struct PtyManager {
    master: Box<dyn MasterPty + Send>,
    child: Box<dyn Child + Send + Sync>,
    reader: Option<Box<dyn Read + Send>>,
    writer: Box<dyn Write + Send>,
    size: PtySize,
}
```

**Key patterns used:**

1. **Shell detection**: Uses `$SHELL` on Unix, `COMSPEC` on Windows
2. **Environment setup**: Sets `TERM=xterm-256color`, `COLORTERM=truecolor`
3. **Reader separation**: `take_reader()` allows moving reader to background thread
4. **Graceful cleanup**: `Drop` impl kills child if still running

## Process Spawning

### Basic shell spawn
```rust
use portable_pty::{native_pty_system, CommandBuilder, PtySize, PtySystem};

let pty_system = native_pty_system();

let size = PtySize {
    rows: 24,
    cols: 80,
    pixel_width: 0,
    pixel_height: 0,
};

let pair = pty_system.openpty(size)?;

let mut cmd = CommandBuilder::new("bash");
cmd.env("TERM", "xterm-256color");

let child = pair.slave.spawn_command(cmd)?;
```

### With environment and working directory
```rust
let mut cmd = CommandBuilder::new("/bin/zsh");
cmd.args(&["-l"]); // Login shell
cmd.env("TERM", "xterm-256color");
cmd.env("COLORTERM", "truecolor");
cmd.cwd("/home/user/projects");

// Inherit specific env vars
if let Ok(path) = std::env::var("PATH") {
    cmd.env("PATH", path);
}
```

## I/O Handling

### Reading output (blocking)
```rust
let mut reader = pair.master.try_clone_reader()?;
let mut buf = [0u8; 4096];

loop {
    match reader.read(&mut buf) {
        Ok(0) => break, // EOF
        Ok(n) => {
            let output = &buf[..n];
            // Process output bytes (may be partial UTF-8!)
        }
        Err(e) => break,
    }
}
```

### Writing input
```rust
let mut writer = pair.master.take_writer()?;

// Write command with carriage return
writeln!(writer, "ls -la\r")?;
writer.flush()?;

// Or raw bytes
writer.write_all(b"exit\r\n")?;
```

### Non-blocking I/O pattern
Move reader to background thread:
```rust
let reader = pty_manager.take_reader().unwrap();

std::thread::spawn(move || {
    let mut buf = [0u8; 4096];
    loop {
        match reader.read(&mut buf) {
            Ok(0) => break,
            Ok(n) => {
                // Send to channel or process
            }
            Err(_) => break,
        }
    }
});
```

## Resize Handling

Resize triggers SIGWINCH to child process:
```rust
let new_size = PtySize {
    rows: 40,
    cols: 120,
    pixel_width: 0,
    pixel_height: 0,
};

pair.master.resize(new_size)?;
```

**script-kit-gpui pattern:**
```rust
impl PtyManager {
    pub fn resize(&mut self, cols: u16, rows: u16) -> Result<()> {
        let new_size = PtySize {
            rows, cols,
            pixel_width: 0,
            pixel_height: 0,
        };
        self.master.resize(new_size)?;
        self.size = new_size;
        Ok(())
    }
}
```

## Process Lifecycle

### Check if running
```rust
match child.try_wait()? {
    Some(status) => println!("Exited: {:?}", status),
    None => println!("Still running"),
}
```

### Wait for exit
```rust
let status = child.wait()?; // Blocks
if status.success() {
    println!("Process succeeded");
}
```

### Kill process
```rust
child.kill()?; // Sends SIGKILL on Unix
```

## Anti-patterns

### Taking writer multiple times
```rust
// WRONG - will panic or error
let writer1 = pair.master.take_writer()?;
let writer2 = pair.master.take_writer()?; // Error!
```

### Forgetting carriage return
```rust
// WRONG - no line terminator
writer.write_all(b"ls")?;

// CORRECT - include CR or CRLF
writer.write_all(b"ls\r")?;
// or
writer.write_all(b"ls\r\n")?;
```

### Not setting TERM
```rust
// WRONG - many programs won't work correctly
let cmd = CommandBuilder::new("vim");

// CORRECT
let mut cmd = CommandBuilder::new("vim");
cmd.env("TERM", "xterm-256color");
```

### Blocking main thread on read
```rust
// WRONG - blocks UI thread
let mut buf = [0u8; 4096];
reader.read(&mut buf)?; // Blocks!

// CORRECT - read in background thread
std::thread::spawn(move || {
    // reading here
});
```

### Not handling partial UTF-8
```rust
// WRONG - may panic on invalid UTF-8
let output = String::from_utf8(buf.to_vec()).unwrap();

// CORRECT - handle lossy conversion
let output = String::from_utf8_lossy(&buf[..n]);
```

### Forgetting cleanup
```rust
// WRONG - child may become zombie
drop(pty_manager);

// CORRECT - kill before drop (script-kit-gpui pattern)
impl Drop for PtyManager {
    fn drop(&mut self) {
        if self.is_running() {
            let _ = self.kill();
        }
    }
}
```

## Error Handling

All operations return `anyhow::Result`. Common errors:
- PTY creation: Resource exhaustion, permission denied
- Spawn: Command not found, permission denied
- Resize: Invalid dimensions, PTY closed
- I/O: Broken pipe (child exited), would block

## Thread Safety

- `MasterPty` is `Send` but not `Sync`
- Reader and writer can be used from different threads if separated
- `Child` is `Send + Sync`
- Use channels to coordinate between reader thread and main thread

## References

- [docs.rs/portable-pty](https://docs.rs/portable-pty/latest/portable_pty/)
- [GitHub: wezterm/wezterm](https://github.com/wezterm/wezterm) (portable-pty is part of WezTerm)
- script-kit-gpui: `src/terminal/pty.rs`
