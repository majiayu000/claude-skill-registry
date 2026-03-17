---
name: notify-file-watcher
description: Cross-platform file system watching with the notify crate
tags: [rust, filesystem, watcher, events]
---

# notify-file-watcher

Cross-platform filesystem notification library for Rust. Provides native event-driven watching on macOS (FSEvents), Linux (inotify), and Windows (ReadDirectoryChangesW).

## Key Types

### RecommendedWatcher
Platform-specific watcher selected automatically. Use `recommended_watcher()` for convenience:

```rust
use notify::{recommended_watcher, RecursiveMode, Watcher};

let mut watcher = recommended_watcher(|res| {
    match res {
        Ok(event) => println!("event: {:?}", event),
        Err(e) => println!("watch error: {:?}", e),
    }
})?;

watcher.watch(Path::new("/path"), RecursiveMode::Recursive)?;
```

### Event
Contains:
- `kind: EventKind` - What happened
- `paths: Vec<PathBuf>` - Affected paths
- `attrs: EventAttributes` - Optional metadata (tracker ID, info, source)

### EventKind
Top-level event classification:
- `Any` - Catch-all for unknown events
- `Access(AccessKind)` - File opened/closed/executed (not all platforms)
- `Create(CreateKind)` - File/folder created
- `Modify(ModifyKind)` - Content/name/metadata changed
- `Remove(RemoveKind)` - File/folder deleted
- `Other` - Meta-events about the watch itself

### RecursiveMode
- `Recursive` - Watch directory and all subdirectories
- `NonRecursive` - Watch only the specified directory

## Usage in script-kit-gpui

### Watcher Architecture
Script-kit uses three specialized watchers in `src/watcher.rs`:

1. **ConfigWatcher** - Watches `~/.scriptkit/kit/config.ts`
   - NonRecursive on parent directory
   - Filters events to target filename only
   
2. **ThemeWatcher** - Watches `~/.scriptkit/kit/theme.json`
   - Same pattern as ConfigWatcher
   
3. **ScriptWatcher** - Watches `~/.scriptkit/kit/main/scripts/` and `/extensions/`
   - Recursive watching
   - Filters by extension (.ts, .js, .md)
   - Dynamic watch addition when extensions directory appears

### Callback Pattern
Events are forwarded to a control channel for processing:

```rust
let (control_tx, control_rx) = channel::<ControlMsg>();

let mut watcher = recommended_watcher({
    let tx = control_tx.clone();
    move |res: notify::Result<notify::Event>| {
        let _ = tx.send(ControlMsg::Notify(res));
    }
})?;
```

### Filtering Events
Filter irrelevant events early:

```rust
fn is_relevant_event_kind(kind: &notify::EventKind) -> bool {
    !matches!(kind, notify::EventKind::Access(_))  // Ignore access events
}

fn is_relevant_script_file(path: &Path) -> bool {
    // Skip hidden files
    if path.file_name().and_then(|n| n.to_str()).map(|n| n.starts_with('.')).unwrap_or(false) {
        return false;
    }
    // Check extensions
    matches!(path.extension().and_then(|ext| ext.to_str()), Some("ts") | Some("js") | Some("md"))
}
```

## Debouncing

### Manual Debouncing (script-kit approach)
Trailing-edge debounce with per-file tracking:

```rust
const DEBOUNCE_MS: u64 = 500;

// Per-file pending events with timestamps
let mut pending: HashMap<PathBuf, (Event, Instant)> = HashMap::new();

// On event: update timestamp
pending.insert(path.clone(), (event, Instant::now()));

// On timeout: flush expired events
let now = Instant::now();
pending.retain(|path, (ev, timestamp)| {
    if now.duration_since(*timestamp) >= Duration::from_millis(DEBOUNCE_MS) {
        emit_event(ev);
        false  // Remove from pending
    } else {
        true   // Keep waiting
    }
});
```

### Built-in Debouncer (notify-debouncer-mini/full)
For simpler use cases:

```rust
use notify_debouncer_mini::{new_debouncer, DebouncedEventKind};
use std::time::Duration;

let (tx, rx) = channel();
let mut debouncer = new_debouncer(Duration::from_millis(500), tx)?;
debouncer.watcher().watch(path, RecursiveMode::Recursive)?;
```

**notify-debouncer-mini**: Lightweight, simple events
**notify-debouncer-full**: Includes file ID tracking, renames, cache

## Event Types

### Create Events
```rust
notify::EventKind::Create(CreateKind::File)    // New file
notify::EventKind::Create(CreateKind::Folder)  // New directory
notify::EventKind::Create(CreateKind::Any)     // Unknown creation
```

### Modify Events
```rust
notify::EventKind::Modify(ModifyKind::Data(DataChange::Content))  // File content changed
notify::EventKind::Modify(ModifyKind::Data(DataChange::Size))     // Size changed
notify::EventKind::Modify(ModifyKind::Name(RenameMode::From))     // Renamed from
notify::EventKind::Modify(ModifyKind::Name(RenameMode::To))       // Renamed to
notify::EventKind::Modify(ModifyKind::Metadata(MetadataKind::Any)) // Attributes changed
```

### Remove Events
```rust
notify::EventKind::Remove(RemoveKind::File)    // File deleted
notify::EventKind::Remove(RemoveKind::Folder)  // Directory deleted
```

### Access Events (platform-specific)
```rust
notify::EventKind::Access(AccessKind::Open(AccessMode::Read))   // File opened
notify::EventKind::Access(AccessKind::Close(AccessMode::Write)) // File closed after write
```

## Recursive vs Non-recursive

### Use Recursive When:
- Watching a scripts/plugins directory with subdirectories
- Unknown directory structure depth
- Need to catch all nested changes

```rust
watcher.watch(&scripts_path, RecursiveMode::Recursive)?;
```

### Use NonRecursive When:
- Watching a single config file (watch parent directory)
- Watching for directory creation in a known location
- Performance-critical with known shallow structure

```rust
// Watch parent to catch config file changes including atomic saves
let watch_path = config_path.parent().unwrap();
watcher.watch(watch_path, RecursiveMode::NonRecursive)?;

// Then filter to target file
let touches_target = event.paths.iter()
    .any(|p| p.file_name() == Some(target_name));
```

## Error Handling

### Supervisor Pattern with Exponential Backoff
Script-kit wraps watchers in a supervisor loop:

```rust
const INITIAL_BACKOFF_MS: u64 = 100;
const MAX_BACKOFF_MS: u64 = 30_000;
const MAX_NOTIFY_ERRORS: u32 = 10;

fn compute_backoff(attempt: u32) -> Duration {
    let delay_ms = INITIAL_BACKOFF_MS.saturating_mul(2u64.saturating_pow(attempt));
    Duration::from_millis(delay_ms.min(MAX_BACKOFF_MS))
}

// In supervisor loop
loop {
    match watch_loop(...) {
        Ok(()) => break,  // Normal shutdown
        Err(e) => {
            let backoff = compute_backoff(attempt);
            sleep(backoff);
            attempt += 1;
        }
    }
}
```

### Consecutive Error Threshold
Restart watcher after too many consecutive errors:

```rust
if consecutive_errors >= MAX_NOTIFY_ERRORS {
    return Err(notify::Error::generic("Too many consecutive notify errors"));
}
```

## Storm Coalescing

When many events arrive quickly (git operations, bulk copy), collapse to a single reload:

```rust
const STORM_THRESHOLD: usize = 200;

if pending.len() >= STORM_THRESHOLD {
    pending.clear();
    full_reload_at = Some(Instant::now());  // Emit single FullReload after debounce
}
```

## Atomic Save Handling

Editors save files differently:
- **Truncate**: Modify existing file (simple modify event)
- **Atomic**: Write to temp file, rename/move over original (Delete + Create sequence)

Merge delete+create into FileChanged:

```rust
fn merge_script_event(pending: &mut HashMap<PathBuf, (Event, Instant)>, path: &PathBuf, new_event: Event, timestamp: Instant) {
    if let Some((existing, _)) = pending.get(path) {
        let merged = match (existing, &new_event) {
            (FileDeleted(_), FileCreated(_)) | (FileCreated(_), FileDeleted(_)) => {
                Some(FileChanged(path.clone()))
            }
            _ => None,
        };
        if let Some(merged) = merged {
            pending.insert(path.clone(), (merged, timestamp));
            return;
        }
    }
    pending.insert(path.clone(), (new_event, timestamp));
}
```

## Anti-patterns

### 1. Blocking in Callback
**Bad**: The callback runs on notify's internal thread
```rust
// DON'T: blocks notify's event processing
let watcher = recommended_watcher(|res| {
    heavy_processing(res);  // Blocks!
})?;
```

**Good**: Forward to channel, process elsewhere
```rust
let watcher = recommended_watcher(move |res| {
    let _ = tx.send(res);  // Non-blocking
})?;
```

### 2. Ignoring Platform Differences
Different platforms emit different event sequences. Always handle:
- `EventKind::Any` and `EventKind::Other`
- Missing sub-kind information (e.g., `ModifyKind::Any`)

### 3. Not Handling Watcher Lifetime
The watcher stops when dropped. Keep it alive:
```rust
// DON'T
{
    let watcher = recommended_watcher(...)?;
} // Watcher dropped, watching stops!

// DO
struct MyApp {
    _watcher: Box<dyn Watcher>,  // Keep alive
}
```

### 4. Watching Non-existent Paths
Notify errors if path doesn't exist. Check first or handle the error:
```rust
if path.exists() {
    watcher.watch(&path, RecursiveMode::Recursive)?;
}
```

### 5. Not Debouncing
Raw events can be noisy. Always debounce for UI/reload triggers.

### 6. Watching Network Filesystems
NFS, SMB, and WSL paths may not emit events. Use `PollWatcher` as fallback:
```rust
use notify::poll::PollWatcher;

let watcher = PollWatcher::new(callback, Config::default()
    .with_poll_interval(Duration::from_secs(2)))?;
```

## Platform-Specific Notes

### macOS (FSEvents)
- Requires watching parent directory for single-file changes
- May not emit events for files you don't own
- Use `macos_kqueue` feature for kqueue backend instead

### Linux (inotify)
- Has per-user watch limits (`/proc/sys/fs/inotify/max_user_watches`)
- Increase with: `sysctl fs.inotify.max_user_watches=524288`
- Not 100% reliable for large directories

### Windows (ReadDirectoryChangesW)
- Generally reliable
- May have issues with network paths

## Quick Reference

```rust
use notify::{
    recommended_watcher,
    RecursiveMode,
    Result,
    Watcher,
    Event,
    EventKind,
    event::{CreateKind, ModifyKind, RemoveKind, AccessKind},
};
use std::path::Path;
use std::sync::mpsc::channel;

fn watch_files() -> Result<()> {
    let (tx, rx) = channel();
    
    let mut watcher = recommended_watcher(move |res: Result<Event>| {
        if let Ok(event) = res {
            let _ = tx.send(event);
        }
    })?;
    
    watcher.watch(Path::new("./src"), RecursiveMode::Recursive)?;
    
    for event in rx {
        match event.kind {
            EventKind::Create(_) => println!("Created: {:?}", event.paths),
            EventKind::Modify(_) => println!("Modified: {:?}", event.paths),
            EventKind::Remove(_) => println!("Removed: {:?}", event.paths),
            _ => {}
        }
    }
    
    Ok(())
}
```
