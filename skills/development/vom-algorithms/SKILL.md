---
name: vom-algorithms
description: "Implements and extends the Visual Object Model (VOM) algorithms for terminal UI element detection in agent-tui. Use when: (1) Modifying cli/src/vom/ segmentation or classification code, (2) Adding new UI element roles or detection patterns, (3) Implementing incremental updates or performance optimizations, (4) Working with terminal screen buffers, cell styles, or coordinate systems, (5) Debugging element detection issues, (6) Extending the VOM pipeline architecture."
---

# VOM Algorithms

## Core Concepts

The Visual Object Model treats a terminal as a 2D grid of styled cells and identifies UI elements through a two-stage pipeline:

```
ScreenBuffer → Segmentation → Clusters → Classification → Components
   (cells)        (RLE)      (regions)   (heuristics)    (UI elements)
```

**Key data structures** (see `cli/src/vom/mod.rs`):
- `ScreenBuffer`: 2D grid of `Cell` (char + style)
- `Cluster`: Style-homogeneous text region with bounds
- `Component`: Classified UI element with role and hash

## Algorithm Selection Guide

| Task | Reference |
|------|-----------|
| Modify segmentation logic | [01-run-length-encoding.md](references/01-run-length-encoding.md) |
| Add multi-row component detection | [02-connected-component-labeling.md](references/02-connected-component-labeling.md) |
| Understand traversal order | [03-raster-scan-traversal.md](references/03-raster-scan-traversal.md) |
| Add/modify element role detection | [04-heuristic-classification.md](references/04-heuristic-classification.md) |
| Work with element positioning | [05-bounding-box-computation.md](references/05-bounding-box-computation.md) |
| Debug terminal rendering | [06-vt100-state-machine.md](references/06-vt100-state-machine.md) |
| Implement element tracking | [07-content-hashing.md](references/07-content-hashing.md) |
| Refactor tokenization | [08-lexical-analysis.md](references/08-lexical-analysis.md) |
| Add pattern matchers | [09-pattern-matching.md](references/09-pattern-matching.md) |
| Handle wide/emoji chars | [10-unicode-terminal-handling.md](references/10-unicode-terminal-handling.md) |
| Fix coordinate issues | [11-grid-coordinate-systems.md](references/11-grid-coordinate-systems.md) |
| Optimize updates | [12-incremental-updates.md](references/12-incremental-updates.md) |
| Understand full pipeline | [13-vom-pipeline-architecture.md](references/13-vom-pipeline-architecture.md) |
| Implement click targeting | [14-hit-testing-click-targeting.md](references/14-hit-testing-click-targeting.md) |

## Quick Implementation Patterns

### Adding a New Role

1. Add variant to `Role` enum in `cli/src/vom/mod.rs`
2. Add detection function in `cli/src/vom/classifier.rs`
3. Insert in priority order within `infer_role()`
4. Add tests

```rust
// classifier.rs
fn is_progress_bar(text: &str) -> bool {
    let bar_chars = ['█', '▓', '▒', '░', '─', '━'];
    let count = text.chars().filter(|c| bar_chars.contains(c)).count();
    count > text.len() / 2
}

fn infer_role(cluster: &Cluster, cursor_row: u16, cursor_col: u16) -> Role {
    // ... existing checks ...
    if is_progress_bar(&cluster.text) {
        return Role::ProgressBar;
    }
    // ... rest of cascade ...
}
```

### Modifying Segmentation

Read [01-run-length-encoding.md](references/01-run-length-encoding.md) first. Key file: `cli/src/vom/segmentation.rs`

Current predicate: style equality. To change grouping logic:

```rust
fn should_merge(current: &Cluster, cell: &Cell) -> bool {
    current.style == cell.style
    // Add additional conditions here
}
```

### Implementing Element Tracking

Read [07-content-hashing.md](references/07-content-hashing.md) and [12-incremental-updates.md](references/12-incremental-updates.md).

```rust
// Track elements across frames
let prev_hash = component.visual_hash;
// After re-segmentation, find by hash:
let same_element = new_components.iter().find(|c| c.visual_hash == prev_hash);
```

## Code Locations

| Concept | File |
|---------|------|
| Terminal emulation | `cli/src/terminal.rs` |
| Segmentation | `cli/src/vom/segmentation.rs` |
| Classification | `cli/src/vom/classifier.rs` |
| Data types | `cli/src/vom/mod.rs` |
| Snapshot command | `cli/src/handlers.rs` |

## Complexity Targets

- Segmentation: O(W×H) single pass
- Classification: O(clusters) with O(text_len) per cluster
- Full snapshot: < 5ms for 80×24 terminal

## Testing Patterns

```rust
#[test]
fn test_new_element_detection() {
    let cluster = make_cluster("█████░░░░░", CellStyle::default(), 0, 0);
    let role = infer_role(&cluster, 99, 99);
    assert_eq!(role, Role::ProgressBar);
}
```

Always test:
1. Positive detection (element recognized)
2. Negative cases (similar but different elements)
3. Boundary conditions (edge of screen, empty text)
4. Style variations (bold, inverse, colored)
