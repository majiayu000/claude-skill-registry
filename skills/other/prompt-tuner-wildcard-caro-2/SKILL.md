---
name: prompt-tuner
description: Improve embedded LLM system prompt based on evaluation test failures
---

# Prompt Tuner

Iteratively improve the embedded backend's system prompt to increase command generation accuracy.

## When to Use

- "tune the prompt"
- "improve embedded accuracy"
- "fix LLM command generation"
- "run prompt tuning cycle"
- After evaluation tests show low accuracy

## Workflow

### Phase 1: Baseline Measurement

Run evaluation tests with embedded backend:

```bash
./target/release/caro test --backend embedded
```

Record:
- Overall accuracy percentage
- Category breakdown (Website Claim, Natural Variant, Edge Case)
- List of failed test cases with expected vs actual commands

### Phase 2: Failure Analysis

For each failed test case, identify the pattern:

| Pattern | Example | Fix |
|---------|---------|-----|
| Wrong path | `find /` instead of `find .` | Add rule: "ALWAYS use current directory '.'" |
| GNU flags | `--max-depth` on macOS | Add rule: "Use BSD-compatible flags" |
| Missing filters | No `-name "*.py"` | Add rule: "Include ALL relevant filters" |
| Time semantics | `-mtime -1` vs `-mtime 1` | Add clear mtime documentation |
| Quote style | Single vs double quotes | Usually equivalent, low priority |
| Flag order | `-type f -name` vs `-name -type f` | Usually equivalent, low priority |

### Phase 3: Prompt Improvement

Edit the system prompt in:
```
src/backends/embedded/embedded_backend.rs
```

Function: `create_system_prompt()`

Improvement strategies:
1. Add explicit rules for common failure patterns
2. Add concrete examples matching test cases
3. Use numbered rules with clear priorities
4. Keep prompt concise (LLMs perform worse with verbose prompts)

### Phase 4: Verification

Build and re-run tests:

```bash
cargo build --release
./target/release/caro test --backend embedded
```

Compare results:
- Did overall accuracy improve?
- Which categories improved/regressed?
- Are remaining failures semantic equivalents (flag order, quotes)?

### Phase 5: Iterate or Commit

If accuracy improved significantly:
```bash
git add src/backends/embedded/embedded_backend.rs
git commit -m "feat(prompt): Improve embedded backend accuracy from X% to Y%"
```

If not improved or regressed:
- Revert changes
- Try different approach
- Consider if test expectations need adjustment

## Success Metrics

| Level | Accuracy | Action |
|-------|----------|--------|
| Poor | < 50% | Major prompt rewrite needed |
| Acceptable | 50-70% | Targeted improvements |
| Good | 70-85% | Minor tuning |
| Excellent | > 85% | Consider semantic equivalence in remaining failures |

## Tips

1. **One change at a time**: Make small, focused improvements
2. **Check equivalents**: Some "failures" are functionally equivalent commands
3. **Test edge cases**: Simple prompts often break on edge cases
4. **BSD vs GNU**: macOS uses BSD utilities, not GNU coreutils
5. **Keep examples minimal**: Too many examples can confuse small models

## Example Session

```
User: /prompt-tuner