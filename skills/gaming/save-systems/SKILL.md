---
name: Save Data Patterns
description: This skill should be used when the user asks about "save game", "save data", "load game", "save slot", "persistent storage", "game progress", "save state", "bytemuck serialization", "save corruption", "auto-save", "high scores", "settings persistence", "save file", "load data", "game save", or implements save/load functionality for Nethercore ZX games.
version: 0.1.0
---

# Save Data Patterns

Implementation patterns for persistent game data on Nethercore ZX. Covers the save/load FFI, data structure design, serialization, and rollback-safe save timing.

## FFI Reference

```rust
/// Save data to a slot.
/// - slot: 0-7 (8 slots available)
/// - data_ptr: Pointer to data in WASM memory
/// - data_len: Length in bytes (max 64KB = 65,536 bytes)
/// Returns: 0 = success, 1 = invalid slot, 2 = data too large
fn save(slot: u32, data_ptr: *const u8, data_len: u32) -> u32;

/// Load data from a slot.
/// - slot: 0-7
/// - data_ptr: Buffer in WASM memory
/// - max_len: Maximum bytes to read
/// Returns: Bytes read (0 if empty or error)
fn load(slot: u32, data_ptr: *mut u8, max_len: u32) -> u32;

/// Delete a save slot.
/// Returns: 0 = success, 1 = invalid slot
fn delete(slot: u32) -> u32;
```

**Checking if save exists:** No `save_exists()` function. Call `load()` with a small buffer and check if return > 0.

```rust
fn save_exists(slot: u32) -> bool {
    let mut buf = [0u8; 4];
    unsafe { load(slot, buf.as_mut_ptr(), 4) > 0 }
}
```

## Rollback Safety Rule

**CRITICAL:** Save operations must ONLY occur in `render()`, NEVER in `update()`.

| Function | `update()` | `render()` |
|----------|------------|------------|
| `save()` | NEVER | SAFE |
| `load()` | On init only | SAFE |
| `delete()` | NEVER | SAFE |

**Why?** During rollback, `update()` may execute multiple times for the same frame. Saving in `update()` causes:
- Corrupted saves (partial state)
- Duplicate save operations
- Desynced state between clients

Safe pattern—save on explicit user action in render:

```rust
static mut PENDING_SAVE: bool = false;

#[no_mangle]
pub extern "C" fn update() {
    // Flag save request, don't actually save
    if button_pressed(0, button::START) && in_pause_menu() {
        unsafe { PENDING_SAVE = true; }
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        if PENDING_SAVE {
            PENDING_SAVE = false;
            perform_save(0);  // Actually save here
        }
    }
    // ... render
}
```

## What to Save

Organize save data into categories:

| Category | Examples | Slot Strategy |
|----------|----------|---------------|
| Progress | Level, checkpoints, unlocks | Slots 0-5 (6 save files) |
| Settings | Volume, controls, display | Slot 6 (shared) |
| High Scores | Leaderboards, best times | Slot 7 (shared) |

**Progress data** (per-playthrough):
- Current level/stage
- Player stats (health, lives, items)
- World state (enemies defeated, doors opened)
- Playtime in frames

**Settings** (global, one slot):
- Audio volume (0-100)
- Control mappings
- Accessibility options

**High scores** (global, one slot):
- Top 10 scores with initials
- Best completion times
- Achievement flags

## Save Data Structure

Use a versioned header for forward compatibility:

```rust
use bytemuck::{Pod, Zeroable};

const SAVE_MAGIC: u32 = 0x5A585356;  // "ZXSV"
const SAVE_VERSION: u32 = 1;

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct SaveHeader {
    magic: u32,        // Identifies valid save
    version: u32,      // For migration
    checksum: u32,     // CRC32 of data
    data_len: u32,     // Actual data length
}

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct GameSave {
    header: SaveHeader,
    // Progress
    level: u8,
    checkpoint: u8,
    health: u8,
    lives: u8,
    items: [u8; 16],
    // Stats
    playtime_frames: u32,
    enemies_defeated: u16,
    secrets_found: u8,
    _padding: u8,
}
```

Key requirements for `bytemuck`:
- `#[repr(C)]` for consistent layout
- All fields must be `Pod` (plain old data)
- Explicit padding for alignment

## Saving and Loading

```rust
fn perform_save(slot: u32) -> bool {
    let save = create_save_data();
    let bytes = bytemuck::bytes_of(&save);

    let result = unsafe { save(slot, bytes.as_ptr(), bytes.len() as u32) };
    result == 0
}

fn perform_load(slot: u32) -> Option<GameSave> {
    let mut save = GameSave::zeroed();
    let bytes = bytemuck::bytes_of_mut(&mut save);

    let read = unsafe { load(slot, bytes.as_mut_ptr(), bytes.len() as u32) };
    if read == 0 { return None; }

    // Validate
    if save.header.magic != SAVE_MAGIC { return None; }
    if !verify_checksum(&save) { return None; }

    // Version migration if needed
    if save.header.version < SAVE_VERSION {
        migrate_save(&mut save);
    }

    Some(save)
}
```

## Error Handling

```rust
enum SaveError {
    Success,
    InvalidSlot,    // slot > 7
    DataTooLarge,   // > 64KB
}

fn save_with_error(slot: u32, data: &[u8]) -> Result<(), SaveError> {
    match unsafe { save(slot, data.as_ptr(), data.len() as u32) } {
        0 => Ok(()),
        1 => Err(SaveError::InvalidSlot),
        2 => Err(SaveError::DataTooLarge),
        _ => Err(SaveError::InvalidSlot),
    }
}
```

Budget check before saving:

```rust
fn can_save(data_len: usize) -> bool {
    data_len <= 65536  // 64KB limit
}
```

## Auto-Save Pattern

Auto-save at safe points (level transitions, checkpoints):

```rust
static mut AUTO_SAVE_PENDING: bool = false;

fn on_checkpoint_reached() {
    unsafe { AUTO_SAVE_PENDING = true; }
}

fn on_level_complete() {
    unsafe { AUTO_SAVE_PENDING = true; }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        if AUTO_SAVE_PENDING && !in_gameplay() {
            // Only auto-save when not actively playing
            AUTO_SAVE_PENDING = false;
            perform_auto_save();
        }
    }
}
```

Safe auto-save timing:
- After level complete screen
- On pause menu open
- After cutscene ends
- NEVER during active gameplay

## Slot Management UI

```rust
struct SaveSlotInfo {
    occupied: bool,
    level: u8,
    playtime: u32,
}

fn get_slot_info(slot: u32) -> SaveSlotInfo {
    let mut buf = [0u8; size_of::<GameSave>()];
    let read = unsafe { load(slot, buf.as_mut_ptr(), buf.len() as u32) };

    if read == 0 {
        return SaveSlotInfo { occupied: false, level: 0, playtime: 0 };
    }

    let save: GameSave = *bytemuck::from_bytes(&buf);
    SaveSlotInfo {
        occupied: true,
        level: save.level,
        playtime: save.playtime_frames,
    }
}

fn format_playtime(frames: u32) -> (u32, u32, u32) {
    let seconds = frames / 60;
    let minutes = seconds / 60;
    let hours = minutes / 60;
    (hours, minutes % 60, seconds % 60)
}
```

## Additional Resources

### Reference Files

For detailed serialization and migration patterns:
- **`references/serialization-patterns.md`** — bytemuck usage, CRC32 checksums, version migration strategies, complex data structures
