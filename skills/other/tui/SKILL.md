---
name: tui
description: Guide for Splitrail's terminal UI and file watching. Use when modifying the TUI, stats display, or real-time update logic.
---

# Real-Time Monitoring & TUI

Splitrail provides a terminal UI with live updates when analyzer data files change.

## Source Files

- `src/tui.rs` - TUI entry point and rendering
- `src/tui/logic.rs` - TUI state management and input handling
- `src/watcher.rs` - File watching implementation

## Components

### FileWatcher (`src/watcher.rs`)

Watches analyzer data directories for changes using the `notify` crate. Triggers incremental re-parsing on file changes and updates TUI via channels.

### RealtimeStatsManager

Coordinates real-time updates: background file watching, auto-upload to Splitrail Cloud (if configured), and stats updates to TUI via `tokio::sync::watch`.

### TUI (`src/tui.rs`, `src/tui/logic.rs`)

Terminal interface using `ratatui`:
- Daily stats view with date navigation
- Session view with lazy message loading
- Real-time stats refresh

## Key Patterns

- **Channel-based updates** - Stats flow through `tokio::sync::watch` channels
- **Lazy message loading** - Messages loaded on-demand for session view to reduce memory

## Adding Watch Support to an Analyzer

Implement `get_watch_directories()` in your analyzer to return root directories for file watching. See `src/analyzer.rs` for the trait definition.
