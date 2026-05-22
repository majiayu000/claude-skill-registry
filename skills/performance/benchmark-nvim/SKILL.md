---
name: benchmark-nvim
description: Benchmark Neovim startup time and identify slow plugins or configurations
allowed-tools: Bash(hyperfine *), Bash(nvim *), Read
---

# Neovim Startup Benchmark

Measure Neovim startup time and perform performance analysis.

## Steps

### 1. Run benchmark with hyperfine

Execute the following command to measure startup time:

```bash
hyperfine --warmup 3 'nvim --headless +q'
```

### 2. Detailed analysis with startuptime

```bash
nvim --startuptime /tmp/nvim-startup.log --headless +q
```

Read `/tmp/nvim-startup.log` and analyze:

- **Total startup time**: Time shown in the last line of the log
- **Slowest plugins TOP 5**: Items taking the most time in sourcing
- **Phase breakdown**:
  - reading vimrc (init.lua)
  - loading plugins
  - syntax/filetype
  - other

### 3. Output format

Report results in the following format:

```
## Benchmark Results

### hyperfine Results
(Include hyperfine output as-is)

### Slowest Plugins TOP 5
| Rank | Plugin | Time (ms) |
|------|--------|-----------|
| 1    | xxx    | X.XX      |
| ...  | ...    | ...       |

### Phase Breakdown
- init.lua loading: X.XX ms
- Plugin loading: X.XX ms
- Other: X.XX ms

### Optimization Suggestions
(Provide suggestions based on slow plugins if applicable)
```

## Notes

- `--warmup 3` in hyperfine warms up the cache
- Consider lazy.nvim lazy-loading settings in analysis
