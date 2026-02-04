---
name: ropey
description: Efficient UTF-8 text rope data structure for editors
---

# ropey

Ropey is a UTF-8 text rope library for Rust, optimized for efficient text manipulation in editors. A rope is a tree-based data structure that stores text as a sequence of smaller chunks, enabling O(log N) insertions and deletions at arbitrary positions - far more efficient than String's O(N) for large documents.

## Why Ropes?

Traditional strings require shifting all characters after an edit point, making insertions/deletions O(N). Ropes split text into chunks organized in a tree, so edits only affect local nodes:

- **Insert/Delete**: O(M + log N) where M is the edited text length
- **Index Conversion**: O(log N) 
- **Length Queries**: O(1)
- **Clone**: O(1) with copy-on-write semantics

This makes ropey ideal for text editors handling documents of any size.

## Key Types

### `Rope`
The main ownable text container. Cloning is O(1) via data sharing.

```rust
use ropey::Rope;

let mut rope = Rope::from_str("Hello world!");
rope.insert(6, "beautiful ");
rope.remove(0..6);
assert_eq!(rope, "beautiful world!");
```

### `RopeSlice<'a>`
An immutable view into part of a `Rope`. Behaves like `&str` but for ropes.

```rust
let rope = Rope::from_str("Hello\nWorld\n");
let slice = rope.slice(0..5);  // "Hello"
let line = rope.line(1);       // "World\n" as RopeSlice
```

### `RopeBuilder`
Efficient incremental rope construction for streaming/large files.

```rust
use ropey::RopeBuilder;

let mut builder = RopeBuilder::new();
builder.append("Hello ");
builder.append("world!");
let rope = builder.finish();
```

### Iterators (`ropey::iter`)
- `Bytes` - iterate over raw bytes
- `Chars` - iterate over Unicode chars
- `Lines` - iterate over lines (includes trailing newline)
- `Chunks` - iterate over internal `&str` chunks (for low-level access)

All iterators support bidirectional traversal via `next()` and `prev()`.

## Common Operations

### Creating Ropes

```rust
// From string
let rope = Rope::from_str("content");

// From file
let rope = Rope::from_reader(BufReader::new(File::open("file.txt")?))?;

// Empty
let rope = Rope::new();
```

### Editing

```rust
let mut rope = Rope::from_str("Hello world!");

// Insert at char index
rope.insert(6, "beautiful ");

// Insert single char
rope.insert_char(0, '!');

// Remove range (char indices)
rope.remove(0..6);

// Append another rope
rope.append(other_rope);

// Split at position
let right = rope.split_off(5);
```

### Querying

```rust
let rope = Rope::from_str("Hello\nWorld\n");

// Lengths
rope.len_bytes();  // Total bytes
rope.len_chars();  // Total chars
rope.len_lines();  // Total lines (3 for above)

// Access by index
rope.byte(0);      // First byte
rope.char(0);      // First char: 'H'
rope.line(1);      // Second line as RopeSlice: "World\n"
```

### Slicing

```rust
// By char range
let slice = rope.slice(0..5);
let slice = rope.slice(5..);
let slice = rope.slice(..5);

// By byte range (must align with char boundaries!)
let slice = rope.byte_slice(0..5);
```

### Writing to File

```rust
rope.write_to(BufWriter::new(File::create("output.txt")?))?;
```

## Index Conversions

**Critical:** Ropey uses three distinct indexing systems. Mixing them causes bugs.

| Method | From | To |
|--------|------|----|
| `byte_to_char(byte_idx)` | byte | char |
| `byte_to_line(byte_idx)` | byte | line |
| `char_to_byte(char_idx)` | char | byte |
| `char_to_line(char_idx)` | char | line |
| `line_to_byte(line_idx)` | line | byte (start) |
| `line_to_char(line_idx)` | line | char (start) |

```rust
let rope = Rope::from_str("Hello\nWorld\n");

// Get char index where line 1 starts
let start = rope.line_to_char(1);  // 6

// Get line containing char index 8
let line = rope.char_to_line(8);   // 1

// Convert byte to char (handles multi-byte UTF-8)
let char_idx = rope.byte_to_char(7);
```

### UTF-16 Support (for JS/LSP interop)

```rust
rope.len_utf16_cu();           // Total UTF-16 code units
rope.char_to_utf16_cu(idx);    // char -> UTF-16 index
rope.utf16_cu_to_char(idx);    // UTF-16 -> char index
```

## Indexing Caveats

### 1. Char vs Byte Indices
Ropey's primary indexing is by **char** (Unicode scalar value), not byte. This matters for non-ASCII text:

```rust
let rope = Rope::from_str("cafe");  // 5 bytes, 4 chars
rope.char(3);           // '' (1 char, 2 bytes)
rope.len_chars();       // 4
rope.len_bytes();       // 5
```

### 2. Line Counting
- Lines are zero-indexed
- `len_lines()` counts logical lines (text after last newline = extra line)
- Line iterators include the trailing newline in each line

```rust
let rope = Rope::from_str("a\nb");   // 3 lines: "a\n", "b", ""
let rope = Rope::from_str("a\nb\n"); // 3 lines: "a\n", "b\n", ""
```

### 3. One-Past-End Indexing
Many methods accept one-past-the-end indices:

```rust
let rope = Rope::from_str("abc");  // len_chars() = 3
rope.byte_to_char(3);  // Valid, returns 3
rope.char(3);          // PANICS! char() is strict
```

### 4. CRLF Handling
CRLF (`\r\n`) is treated as a single line break. By default, ropey recognizes:
- `\n` (LF)
- `\r\n` (CRLF)

With `unicode_lines` feature (default): also `\r`, `\x0B`, `\x0C`, `\u{0085}`, `\u{2028}`, `\u{2029}`.

## Low-Level Chunk Access

For performance-critical code, access raw chunks directly:

```rust
// Get chunk containing char index
let (chunk, chunk_byte_idx, chunk_char_idx, chunk_line_idx) = 
    rope.chunk_at_char(char_idx);

// Iterate chunks
for chunk in rope.chunks() {
    // Process &str directly
}

// Use str_utils for operations on chunks
use ropey::str_utils::byte_to_char_idx;
let local_char = byte_to_char_idx(chunk, byte_offset_in_chunk);
```

## Usage in script-kit-gpui

In script-kit-gpui, ropey is used indirectly through `gpui-component`'s Input component for the editor buffer. The crate handles:

- Editor buffer storage with efficient editing
- Char/byte offset conversion (critical for cursor positioning)
- Line-based operations (go to line, line numbers)

The editor.rs file shows patterns for converting between char and byte offsets when dealing with gpui-component's selection API.

## Anti-patterns

### Using byte indices with char methods

```rust
// WRONG - byte index used with char method
let byte_pos = some_api_returning_bytes();
rope.char(byte_pos);  // BUG if byte_pos is a byte index!

// CORRECT
let char_pos = rope.byte_to_char(byte_pos);
rope.char(char_pos);
```

### Assuming 1:1 char:byte mapping

```rust
// WRONG - assumes ASCII
let byte_idx = char_idx;

// CORRECT
let byte_idx = rope.char_to_byte(char_idx);
```

### Forgetting line semantics

```rust
// WRONG - off by one on last line
let line_count = rope.to_string().split('\n').count();

// CORRECT
let line_count = rope.len_lines();
```

### Mutating while iterating

```rust
// WRONG - can't mutate during iteration
for line in rope.lines() {
    rope.insert(0, "prefix");  // BUG!
}

// CORRECT - collect first
let line_count = rope.len_lines();
for i in (0..line_count).rev() {
    let start = rope.line_to_char(i);
    rope.insert(start, "prefix");
}
```

### Ignoring panics on out-of-bounds

```rust
// PANICS if idx >= len_chars()
rope.char(idx);

// SAFE - returns Option
rope.get_char(idx);

// SAFE - returns Result
rope.try_char_to_byte(idx);
```

## Performance Tips

1. **Clone freely** - O(1) due to structural sharing
2. **Use `chunks()` for bulk processing** - avoid per-char overhead  
3. **Prefer `RopeSlice` over `to_string()`** - zero-copy views
4. **Use `RopeBuilder` for construction** - more efficient than repeated inserts
5. **Batch edits at end** - avoid shifting for sequential appends

## Feature Flags

- `simd` (default): SIMD acceleration for counting/searching
- `unicode_lines` (default): Full Unicode line break support
- `cr_lines`: Treat standalone `\r` as line break

## Reference

- [docs.rs/ropey](https://docs.rs/ropey/latest/ropey/)
- [GitHub: cessen/ropey](https://github.com/cessen/ropey)
