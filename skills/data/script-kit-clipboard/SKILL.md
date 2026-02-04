---
name: script-kit-clipboard
description: Clipboard history module for Script Kit GPUI. Use when working with clipboard monitoring, history storage, entry management, image handling, or paste functionality. Triggers on clipboard_history, ClipboardEntry, copy_entry_to_clipboard, init_clipboard_history.
---

# Script Kit Clipboard History

SQLite-backed clipboard history with background monitoring for Script Kit GPUI.

## Architecture Overview

```
src/clipboard_history/
├── mod.rs              # Public API re-exports
├── monitor.rs          # Background polling thread
├── database.rs         # SQLite CRUD operations
├── cache.rs            # LRU caching (entries + images)
├── clipboard.rs        # Copy-to-clipboard operations
├── types.rs            # ClipboardEntry, TimeGroup, ContentType
├── config.rs           # Retention/size configuration
├── image.rs            # PNG/RGBA encoding/decoding
├── blob_store.rs       # File-based image storage
├── change_detection.rs # macOS NSPasteboard changeCount
└── db_worker/          # Message-passing DB architecture
```

## Core Types

### ClipboardEntry (full payload)
```rust
pub struct ClipboardEntry {
    pub id: String,           // UUID
    pub content: String,      // Text or image reference
    pub content_type: ContentType, // Text | Image
    pub timestamp: i64,       // Unix ms
    pub pinned: bool,
    pub ocr_text: Option<String>,
}
```

### ClipboardEntryMeta (list views - no payload)
```rust
pub struct ClipboardEntryMeta {
    pub id: String,
    pub content_type: ContentType,
    pub timestamp: i64,
    pub pinned: bool,
    pub text_preview: String,    // First 100 chars or "[Image]"
    pub image_width: Option<u32>,
    pub image_height: Option<u32>,
    pub byte_size: usize,
    pub ocr_text: Option<String>,
}
```

### TimeGroup
```rust
pub enum TimeGroup { Today, Yesterday, ThisWeek, LastWeek, ThisMonth, Older }
```

## Public API

### Initialization
```rust
use clipboard_history::{init_clipboard_history, stop_clipboard_monitoring};

// Start monitoring (call once at app startup)
init_clipboard_history()?;

// Stop monitoring (optional cleanup)
stop_clipboard_monitoring();
```

### Configuration
```rust
use clipboard_history::{set_retention_days, set_max_text_content_len};

set_retention_days(30);           // Default: 30 days
set_max_text_content_len(100_000); // Default: 100KB, 0 = unlimited
```

### Database Operations
```rust
use clipboard_history::{
    get_clipboard_history,      // Full entries
    get_clipboard_history_meta, // Metadata only (efficient)
    get_clipboard_history_page, // Paginated full entries
    get_entry_by_id,
    get_entry_content,
    get_total_entry_count,
    pin_entry, unpin_entry,
    remove_entry, clear_history,
};

// Memory-efficient list view (no content payload)
let meta = get_clipboard_history_meta(100, 0);

// Get full content when needed
if let Some(content) = get_entry_content(&entry_id) {
    // Use content
}
```

### Clipboard Operations
```rust
use clipboard_history::copy_entry_to_clipboard;

// Copy entry back to system clipboard (updates timestamp)
copy_entry_to_clipboard(&entry_id)?;
```

### Time Grouping
```rust
use clipboard_history::{classify_timestamp, group_entries_by_time, TimeGroup};

let group = classify_timestamp(entry.timestamp);
let grouped = group_entries_by_time(entries); // Vec<(TimeGroup, Vec<ClipboardEntry>)>
```

### Image Caching
```rust
use clipboard_history::{cache_image, get_cached_image, decode_to_render_image};

// Decode once, cache for display
if let Some(content) = get_entry_content(&id) {
    if let Some(render_image) = decode_to_render_image(&content) {
        cache_image(&id, render_image);
    }
}

// Retrieve cached image
if let Some(image) = get_cached_image(&id) {
    // Display image
}
```

## Image Storage Formats

Three formats supported (auto-detected by prefix):

| Format | Prefix | Storage | Use Case |
|--------|--------|---------|----------|
| Blob | `blob:{hash}` | File on disk | New images (most efficient) |
| PNG | `png:{base64}` | SQLite | Legacy entries |
| RGBA | `rgba:W:H:{base64}` | SQLite | Legacy format |

Blob storage path: `~/.scriptkit/clipboard/blobs/<sha256>.png`

## Background Monitoring

The monitor thread:
1. Polls clipboard every 50ms (macOS with changeCount) or 500ms (content-based)
2. Detects changes via NSPasteboard changeCount (cheap) then content hash
3. Deduplicates via SHA-256 content hash
4. Updates timestamp for re-copied entries
5. Prunes entries older than retention period (hourly)
6. Runs WAL checkpoint every 10 prune cycles

## Caching Strategy

Two LRU caches:

1. **Entry Cache** (500 entries) - ClipboardEntryMeta for fast list rendering
2. **Image Cache** (100 images) - Decoded RenderImage (~100-400MB max)

Incremental cache updates via:
- `upsert_entry_in_cache()` - Add/update single entry
- `remove_entry_from_cache()` - Remove single entry
- `update_pin_status_in_cache()` - Update pin + re-sort

## Database Schema

```sql
CREATE TABLE history (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    content_hash TEXT,
    content_type TEXT NOT NULL DEFAULT 'text',
    timestamp INTEGER NOT NULL,  -- Unix milliseconds
    pinned INTEGER DEFAULT 0,
    ocr_text TEXT,
    text_preview TEXT,
    image_width INTEGER,
    image_height INTEGER,
    byte_size INTEGER DEFAULT 0
);

CREATE INDEX idx_timestamp ON history(timestamp DESC);
CREATE INDEX idx_pinned_timestamp ON history(pinned DESC, timestamp DESC);
CREATE INDEX idx_dedup ON history(content_type, content_hash);
```

Database location: `~/.scriptkit/db/clipboard-history.sqlite`

## Common Patterns

### Efficient List View
```rust
// Use metadata-only query for list rendering
let entries = get_clipboard_history_meta(50, offset);

for entry in entries {
    let preview = entry.display_preview(); // "50×50 image" or truncated text
    let group = classify_timestamp(entry.timestamp);
    // Render list item with preview
}

// Load full content only on selection
fn on_entry_selected(id: &str) {
    if let Some(content) = get_entry_content(id) {
        // Display full content or copy to clipboard
    }
}
```

### Image Display
```rust
// Check cache first, decode on-demand
fn get_image_for_display(id: &str) -> Option<Arc<RenderImage>> {
    if let Some(cached) = get_cached_image(id) {
        return Some(cached);
    }
    
    let content = get_entry_content(id)?;
    let image = decode_to_render_image(&content)?;
    cache_image(id, image.clone());
    Some(image)
}
```

### Pinned Entries First
Entries are automatically sorted: pinned DESC, timestamp DESC. No additional sorting needed for display.
