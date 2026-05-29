---
name: script-kit-notifications
description: |
  Work with Script Kit's unified notification system supporting toasts, HUDs, banners, and system notifications.
  Use when implementing user feedback, status updates, progress indicators, or any transient messages.
  Triggers: "notification", "toast", "HUD", "alert", "feedback", "progress notification", "show message".
---

# Script Kit Notifications

Unified notification system with multiple delivery channels, deduplication, rate limiting, and history.

## Architecture Overview

```
NotificationService (GPUI Global)
├── Active notifications with timer state
├── History (max 100 entries)
├── Rate limiting per source
└── Do Not Disturb mode

Channels:
├── InAppToast    → gpui-component Notification (top-right stack)
├── InAppHud      → HudManager (bottom-center overlay)
├── InAppBanner   → Future: banner bar
├── InAppInline   → Future: inline messages
├── System        → Future: macOS notifications
└── Dialog        → Future: blocking dialogs
```

## Quick Start

### Initialize at App Startup

```rust
NotificationService::init(cx);
```

### Show Notifications

```rust
// Via update_global (preferred)
cx.update_global::<NotificationService, _>(|service, cx| {
    service.success("Task completed!", cx);
    service.error("Failed to save", cx);
    service.warning("Low disk space", cx);
    service.info("Update available", cx);
    service.hud("Copied!", cx);  // Brief overlay
});
```

### Builder Pattern for Custom Notifications

```rust
let notif = Notification::new()
    .content(NotificationContent::Rich {
        icon: IconRef::parse("lucide:check-circle"),  // Returns Option<IconRef>
        title: "Build Complete".to_string(),
        message: Some("23 files compiled".to_string()),
    })
    .channel(NotificationChannel::InAppToast)
    .duration(Duration::from_secs(5))
    .priority(NotificationPriority::High)
    .action("Open", "open")
    .primary_action("View Logs", "view-logs")
    .from_script("/path/to/build.ts")
    .dedupe("build-complete");

cx.update_global::<NotificationService, _>(|service, cx| {
    service.notify(notif, cx);
});
```

## Notification Types

### Content Variants

```rust
NotificationContent::Text(String)                    // Simple text
NotificationContent::TitleMessage { title, message } // Title + body
NotificationContent::Rich { icon: Option<IconRef>, title, message: Option<String> }   // Icon + title + optional body
NotificationContent::Progress { title, progress, message } // Progress bar
NotificationContent::Html(String)                    // HTML (HUD only)
```

### Factory Methods

| Method | Icon | Duration | Priority |
|--------|------|----------|----------|
| `Notification::success(msg)` | check-circle | 3s | Normal |
| `Notification::error(msg)` | x-circle | 5s | High |
| `Notification::warning(msg)` | alert-triangle | 4s | Normal |
| `Notification::info(msg)` | info | 3s | Normal |
| `Notification::hud(msg)` | none | 2s | Normal |
| `Notification::progress(title, 0.5)` | none | persistent | Normal |

## HUD Manager (System Overlay)

For brief, non-intrusive feedback like Raycast's `showHUD()`.

### Direct Usage

```rust
use crate::hud_manager::{show_hud, show_hud_with_action, HudAction};

// Simple HUD
show_hud("Copied!".to_string(), Some(2000), cx);

// HUD with action button
show_hud_with_action(
    "Log saved".to_string(),
    Some(3000),
    "Open".to_string(),
    HudAction::OpenFile(PathBuf::from("/tmp/log.txt")),
    cx,
);
```

### HUD Actions

```rust
HudAction::OpenFile(PathBuf)      // Open in configured editor
HudAction::OpenUrl(String)        // Open in default browser
HudAction::RunCommand(String)     // Execute shell command
```

### HUD Behavior

- **Position**: Bottom-center of screen containing mouse cursor
- **Stacking**: Up to 3 simultaneous HUDs, stacked vertically
- **Queuing**: Additional HUDs queue until slots free
- **Styling**: Transparent pill with theme colors
- **Click-through**: Plain HUDs ignore mouse; action HUDs receive clicks

## Toast Manager

For in-app toast notifications (staging queue for gpui-component).

### Usage Pattern

```rust
let mut toast_manager = ToastManager::new();

// Push toasts from anywhere
let id = toast_manager.push(Toast::new("Message", colors).duration_ms(Some(5000)));

// In render loop, drain to gpui-component
for pending in toast_manager.drain_pending() {
    window.push_notification(/* convert pending to Notification */);
}

// Periodic cleanup
toast_manager.tick();      // Auto-dismiss expired
toast_manager.cleanup();   // Remove dismissed from memory
```

### Toast Lifecycle

1. `push()` → Assigned UUID, added to queue
2. `drain_pending()` → Moved to gpui-component renderer
3. `tick()` → Checks timers, marks expired as dismissed
4. `cleanup()` → Removes dismissed toasts from memory

## Deduplication & Replacement

### Deduplication

Prevent duplicate notifications within a short window:

```rust
// Same dedupe_key = only first shows, others increment count
let notif = Notification::new()
    .content(NotificationContent::Text("File changed".into()))
    .dedupe("file-watcher");

// Access dedupe count for display
if let Some(active) = service.get(id) {
    println!("Occurred {} times", active.dedupe_count + 1);
}
```

### Replacement

Replace existing notifications with same key:

```rust
// Progress updates replace each other
let notif = Notification::progress("Downloading...", 0.5)
    .with_replace_key("download-progress");

// Script-based notifications auto-set replace_key
let notif = Notification::info("Building...")
    .from_script("/scripts/build.ts");  // replace_key = "script:/scripts/build.ts"
```

## Rate Limiting

Per-source rate limiting (250ms window) prevents notification spam:

```rust
// Rapid calls from same source get rate-limited
for _ in 0..10 {
    service.notify(Notification::info("Update").from_script("/fast.ts"), cx);
}
// Only first notification shows; rest are silently dropped
```

## Timer Control

Pause/resume timers when window visibility changes:

```rust
// Window hidden
cx.update_global::<NotificationService, _>(|service, _| {
    service.pause_timers();
});

// Window shown
cx.update_global::<NotificationService, _>(|service, _| {
    service.resume_timers();
});
```

## Do Not Disturb

```rust
cx.update_global::<NotificationService, _>(|service, _| {
    service.enable_dnd();   // Suppress all except Urgent priority
    service.disable_dnd();
    service.toggle_dnd();
    
    if service.is_dnd_enabled() { /* ... */ }
});

// Urgent notifications bypass DND
let urgent = Notification::error("Critical!")
    .priority(NotificationPriority::Urgent);
```

## Query Methods

```rust
cx.update_global::<NotificationService, _>(|service, _| {
    // Active notifications
    let active = service.active_notifications();
    let count = service.active_count();
    let has_any = service.has_active();
    
    // Visible toasts (max 3)
    let toasts = service.visible_toasts();
    let overflow = service.overflow_toast_count();
    
    // History
    let history = service.history();
    
    // By ID
    if let Some(notif) = service.get(id) {
        println!("Dedupe count: {}", notif.dedupe_count);
    }
});
```

## Progress Notifications

```rust
// Show progress
let id = cx.update_global::<NotificationService, _>(|service, cx| {
    service.progress("Downloading...", 0.0, cx)
});

// Update progress
cx.update_global::<NotificationService, _>(|service, _| {
    service.update_progress(id, 0.5, Some("50% complete".into()));
});

// Complete (dismiss replaces it)
cx.update_global::<NotificationService, _>(|service, cx| {
    service.dismiss(id, DismissReason::Programmatic, cx);
    service.success("Download complete!", cx);
});
```

## Key Files

| File | Purpose |
|------|---------|
| `src/notification/mod.rs` | Module exports |
| `src/notification/types.rs` | Core types: Notification, channels, content |
| `src/notification/service.rs` | NotificationService GPUI Global |
| `src/toast_manager.rs` | ToastManager queue for gpui-component |
| `src/hud_manager.rs` | HudManager for system overlays |

## Constants

```rust
// NotificationService
const MAX_HISTORY_SIZE: usize = 100;
const MAX_VISIBLE_TOASTS: usize = 3;
const RATE_LIMIT_WINDOW_MS: u64 = 250;

// HudManager
const DEFAULT_HUD_DURATION_MS: u64 = 2000;
const MAX_SIMULTANEOUS_HUDS: usize = 3;
const HUD_STACK_GAP: f32 = 45.0;
const HUD_WIDTH: f32 = 200.0;
const HUD_HEIGHT: f32 = 36.0;

// ToastManager
const DEFAULT_MAX_VISIBLE: usize = 5;
```
