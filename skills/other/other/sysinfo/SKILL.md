---
name: sysinfo
description: System and process information for Rust applications
version: "0.33"
---

# sysinfo

Cross-platform library for retrieving system information: processes, CPUs, memory, disks, and networks.

## Key Types

### Core Types

| Type | Purpose |
|------|---------|
| `System` | Main struct holding all system information |
| `Process` | Information about a single process |
| `Pid` | Process identifier (platform-specific wrapper) |
| `ProcessesToUpdate` | Enum specifying which processes to refresh |

### Refresh Kind Types (Performance Critical)

| Type | Purpose |
|------|---------|
| `ProcessRefreshKind` | Controls what process info to refresh |
| `RefreshKind` | Controls what system info to refresh |
| `UpdateKind` | `Never`, `OnlyIfNotSet`, or `Always` |

## Usage in script-kit-gpui

### Process Manager (`process_manager.rs`)

The crate is used for **orphan process detection** - checking if child bun processes are still running:

```rust
use sysinfo::{Pid, System};

/// Check if a process is currently running
pub fn is_process_running(&self, pid: u32) -> bool {
    let mut system = System::new();
    system.refresh_processes(sysinfo::ProcessesToUpdate::All, true);
    system.process(Pid::from_u32(pid)).is_some()
}
```

**Key patterns used:**
- `System::new()` - Create minimal system instance
- `refresh_processes(ProcessesToUpdate::All, true)` - Refresh all processes, remove dead ones
- `system.process(Pid::from_u32(pid))` - Look up specific process by PID
- `Pid::from_u32()` - Convert platform u32 to sysinfo's Pid type

## Process Information

### Checking if Process Exists

```rust
use sysinfo::{Pid, ProcessesToUpdate, System};

let mut sys = System::new();
sys.refresh_processes(ProcessesToUpdate::All, true);

// Check by PID
if let Some(process) = sys.process(Pid::from_u32(1234)) {
    println!("Process {} is running", process.name().to_string_lossy());
}

// Check specific PIDs only (more efficient)
let pids = [Pid::from_u32(1234), Pid::from_u32(5678)];
sys.refresh_processes(ProcessesToUpdate::Some(&pids), true);
```

### Process Properties

```rust
// Available on Process
process.pid()           // -> Pid
process.name()          // -> &OsStr (limited to 15 chars on Linux!)
process.exe()           // -> Option<&Path>
process.cmd()           // -> &[OsString]
process.cwd()           // -> Option<&Path>
process.environ()       // -> &[OsString]
process.memory()        // -> u64 (RSS in bytes)
process.virtual_memory() // -> u64
process.cpu_usage()     // -> f32 (percentage)
process.status()        // -> ProcessStatus
process.parent()        // -> Option<Pid>
process.start_time()    // -> u64 (Unix timestamp)
process.run_time()      // -> u64 (seconds)
```

### Killing Processes

```rust
use sysinfo::Signal;

// Simple kill (SIGKILL)
process.kill();

// Kill with specific signal
if let Some(success) = process.kill_with(Signal::Term) {
    println!("Signal sent: {}", success);
}

// Wait for termination
process.wait();
```

## Refresh Patterns

### CRITICAL: Always Refresh Before Reading

sysinfo works on **diffs** - you must refresh to get current data:

```rust
// BAD - stale data
let sys = System::new_all();
let mem = sys.used_memory(); // May be outdated!

// GOOD - fresh data  
let mut sys = System::new();
sys.refresh_memory();
let mem = sys.used_memory();
```

### Performance: Refresh Only What You Need

```rust
use sysinfo::{ProcessRefreshKind, ProcessesToUpdate, System};

// SLOW - refreshes everything
sys.refresh_all();

// FAST - only refresh processes, only memory info
sys.refresh_processes_specifics(
    ProcessesToUpdate::All,
    true, // remove dead processes
    ProcessRefreshKind::nothing().with_memory(),
);

// FASTEST - check specific PIDs only
let pids = [Pid::from_u32(1234)];
sys.refresh_processes(ProcessesToUpdate::Some(&pids), true);
```

### ProcessRefreshKind Builder

```rust
use sysinfo::{ProcessRefreshKind, UpdateKind};

// Nothing (fastest)
ProcessRefreshKind::nothing()

// Everything (slowest)
ProcessRefreshKind::everything()

// Custom - only what you need
ProcessRefreshKind::nothing()
    .with_memory()      // RSS, virtual memory
    .with_cpu()         // CPU usage
    .with_disk_usage()  // Disk I/O
    .with_exe(UpdateKind::OnlyIfNotSet) // Executable path
```

### Reuse System Instance

```rust
// BAD - creates new instance each time
fn check_process(pid: u32) -> bool {
    let mut sys = System::new();
    sys.refresh_processes(ProcessesToUpdate::All, true);
    sys.process(Pid::from_u32(pid)).is_some()
}

// GOOD - reuse instance (especially for CPU usage which needs history)
struct ProcessMonitor {
    sys: System,
}

impl ProcessMonitor {
    fn check_process(&mut self, pid: u32) -> bool {
        self.sys.refresh_processes(ProcessesToUpdate::All, true);
        self.sys.process(Pid::from_u32(pid)).is_some()
    }
}
```

## CPU Usage Notes

CPU usage requires **two measurements** with time between them:

```rust
use sysinfo::{System, MINIMUM_CPU_UPDATE_INTERVAL};
use std::thread;

let mut sys = System::new_all();

// First measurement (will be 0%)
sys.refresh_cpu_usage();

// Wait minimum interval
thread::sleep(MINIMUM_CPU_UPDATE_INTERVAL);

// Second measurement (accurate)
sys.refresh_cpu_usage();

for cpu in sys.cpus() {
    println!("{}%", cpu.cpu_usage());
}
```

## Platform Differences

### Process Names on Linux
- Limited to **15 characters**
- May not match executable name
- Use `process.exe()` for full path when available

### macOS Sandboxing
For App Store apps, use feature flags:
```toml
[dependencies]
sysinfo = { version = "0.33", features = ["apple-app-store"] }
```

### Windows
- Admin privileges may be needed for some process info
- PID is `usize`, not `pid_t`

## Pid Conversions

```rust
use sysinfo::Pid;

// From u32 (most portable)
let pid = Pid::from_u32(1234);

// To u32
let n: u32 = pid.as_u32();

// From/to usize (platform-specific)
let pid = Pid::from(1234_usize);
let n: usize = pid.into();

// Parse from string
let pid: Pid = "1234".parse().unwrap();
```

## Anti-patterns

### Creating System::new_all() Repeatedly

```rust
// BAD - expensive allocation every call
fn get_memory() -> u64 {
    System::new_all().used_memory()
}

// GOOD - reuse instance
fn get_memory(sys: &mut System) -> u64 {
    sys.refresh_memory();
    sys.used_memory()
}
```

### Not Refreshing Before Reading

```rust
// BAD - returns initialization values (often 0)
let sys = System::new();
let procs = sys.processes(); // Empty!

// GOOD
let mut sys = System::new();
sys.refresh_processes(ProcessesToUpdate::All, true);
let procs = sys.processes();
```

### Refreshing Everything When You Need One Thing

```rust
// BAD - refreshes CPUs, memory, processes, etc.
sys.refresh_all();
let mem = sys.used_memory();

// GOOD - only refresh memory
sys.refresh_memory();
let mem = sys.used_memory();
```

### Trusting process.name() on Linux

```rust
// BAD - may be truncated or changed
let name = process.name(); // "my-very-long-a" (truncated!)

// GOOD - use exe when available
let name = process.exe()
    .and_then(|p| p.file_name())
    .map(|n| n.to_string_lossy().to_string())
    .unwrap_or_else(|| process.name().to_string_lossy().to_string());
```

### Reading CPU Usage Without History

```rust
// BAD - first reading is always 0%
let mut sys = System::new_all();
let cpu = sys.global_cpu_usage(); // 0%!

// GOOD - wait for second sample
let mut sys = System::new_all();
std::thread::sleep(sysinfo::MINIMUM_CPU_UPDATE_INTERVAL);
sys.refresh_cpu_usage();
let cpu = sys.global_cpu_usage(); // Accurate!
```

## Common Patterns

### Find Process by Name

```rust
// Exact name match
for process in sys.processes_by_exact_name("bun".as_ref()) {
    println!("{}: {}", process.pid(), process.name().to_string_lossy());
}

// Substring match  
for process in sys.processes_by_name("bun".as_ref()) {
    println!("{}: {}", process.pid(), process.name().to_string_lossy());
}
```

### Monitor Process Until Exit

```rust
use std::time::Duration;

fn wait_for_exit(pid: u32, timeout: Duration) -> bool {
    let mut sys = System::new();
    let deadline = std::time::Instant::now() + timeout;
    let target_pid = Pid::from_u32(pid);
    
    while std::time::Instant::now() < deadline {
        sys.refresh_processes(
            ProcessesToUpdate::Some(&[target_pid]),
            true
        );
        if sys.process(target_pid).is_none() {
            return true; // Process exited
        }
        std::thread::sleep(Duration::from_millis(100));
    }
    false // Timeout
}
```

## Feature Flags

```toml
[dependencies]
sysinfo = { version = "0.33", default-features = false }

# Optional features:
# - multithread: Parallel refresh (increases memory on macOS)
# - serde: Serialize System and related types
# - apple-app-store: Disable APIs prohibited in App Store
# - apple-sandbox: Sandbox-safe subset
```

## References

- [docs.rs/sysinfo](https://docs.rs/sysinfo/0.33)
- [GitHub: GuillaumeGomez/sysinfo](https://github.com/GuillaumeGomez/sysinfo)
- [Migration Guide](https://github.com/GuillaumeGomez/sysinfo/blob/master/migration_guide.md)
