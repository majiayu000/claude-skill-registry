---
name: lc-show
description: Show LeetCode problem details and generate Rust template (project)
---

# LeetCode Show

Show problem details and generate Rust template in `problems/` directory.

## Usage

`/lc-show <problem_id>` - Show problem and generate Rust code template

## Instructions

1. Run `leetcode show <problem_id> 2>/dev/null` to display the problem description
2. Show the problem details to the user
3. Run `leetcode show <problem_id> -g -l rust 2>/dev/null` to generate the Rust template
4. Move the generated file to `problems/` directory:
   ```
   mv <problem_id>.<problem-name>.rs problems/
   ```
5. Tell the user the file is ready at `problems/<problem_id>.<problem-name>.rs`

## File Format

```rust
use std::collections::HashMap; // if needed

impl Solution {
    pub fn function_name(...) -> ... {
        // implementation
    }
}
```

Note: `struct Solution;` は含めない（LeetCode側で定義されるため）。rust-analyzer用には build.rs が lib.rs 経由で提供する。

## Commands

- Test: `leetcode test problems/<file>.rs`
- Submit: `leetcode submit problems/<file>.rs`
