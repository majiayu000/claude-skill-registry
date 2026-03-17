---
name: subtest-isolation
description: Create minimal subtests to isolate and fix complex bugs. Use when a test fails and the issue is buried in complexity.
---

# Subtest Isolation Methodology

When a test fails with complex output or multiple issues, create a minimal subtest to isolate and fix ONE specific problem at a time.

## When to Use This Approach

Use subtest isolation when:
- ✅ Test has multiple moving parts and you can't identify the root cause
- ✅ Visual diff shows one specific element is wrong among many
- ✅ You need to add debug output but the full test is too noisy
- ✅ The bug is structural (wrong algorithm) not just a value mismatch
- ✅ You've tried quick fixes and they didn't work

**Don't use for:**
- ❌ Simple value mismatches you can debug directly
- ❌ Obvious typos or off-by-one errors
- ❌ Issues you can already see the cause of

## The Process

### 1. Identify the Specific Problem

Look at the failing test output and pinpoint EXACTLY what's wrong:
- Which element is mispositioned?
- Which calculation is producing wrong values?
- Which feature is broken?

**Example from test45:**
```
Problem identified: Bottom box has all text overlapping incorrectly.
"center" text appearing at the very top instead of middle.
```

### 2. Create Minimal Reproduction

Create a new test file (e.g., `test45b.pikchr`) with ONLY the problematic element:

```pikchr
# test45b.pikchr - isolate the bottom box issue
box "rjust" rjust above "center" center "ljust" ljust above \
    "rjust" rjust below "ljust" ljust below big big
```

**Key principles:**
- ✅ Include ONLY what's needed to reproduce the bug
- ✅ Remove all unrelated elements (other boxes, arrows, files, etc.)
- ✅ Keep the exact attributes that trigger the bug
- ✅ Name it `<original>b.pikchr` for clarity

### 3. Verify It Fails the Same Way

Run the subtest and confirm it shows the SAME bug:

```bash
cargo run --example simple -- vendor/pikchr-c/tests/test45b.pikchr
# OR
mcp__pikru-test__run_pikru_test test45b
```

**Check that:**
- The specific problem reproduces
- The failure mode is identical
- You haven't accidentally "fixed" it by simplifying

### 4. Add Debug Output

Add targeted debug output to understand what's happening:

```rust
eprintln!("[SLOT HEIGHT] text='{}' slot={:?} font_scale={} charht={} h={}",
    text.value, slot, text.font_scale(), charht, h);

eprintln!("[Y OFFSET] text='{}' slot={:?} calc=[{}] y_offset={} final_y={}",
    positioned_text.value, slot, offset_calc, y_offset, center.y + svg_y_offset);
```

**Debug output best practices:**
- Use `eprintln!` so it goes to stderr (doesn't corrupt SVG output)
- Use clear prefixes like `[SLOT HEIGHT]`, `[Y OFFSET]` for easy grepping
- Show both inputs and outputs of calculations
- Include the actual formula/calculation being performed
- Show intermediate values, not just final results

### 5. Run and Analyze

Run the subtest and analyze the debug output:

```bash
cargo run --example simple -- vendor/pikchr-c/tests/test45b.pikchr 2>&1 | grep '\[SLOT'
```

**Look for:**
- Wrong values (expected vs actual)
- Wrong assignments (text getting wrong slot)
- Wrong calculations (formula producing wrong result)
- Missing or unexpected branches taken

**Example output that revealed the bug:**
```
[SLOT HEIGHT] text='center' slot=Above2 font_scale=1 charht=0.14 h=0.14
```
→ **BUG FOUND:** "center" text assigned to Above2 instead of Center!

### 6. Compare with C Implementation

Run the C implementation on the same subtest:

```bash
vendor/pikchr-c/pikchr --svg-only vendor/pikchr-c/tests/test45b.pikchr | grep '<text'
```

**Compare:**
- Element positions (x, y coordinates)
- Slot assignments (if you can infer them)
- Final output structure

**Example comparison:**
```
C output:    <text y="38.16" ...>center</text>
Rust output: <text y="12.24" ...>center</text>
```
→ Confirms the bug: Rust placing center text way too high

### 7. Fix the Bug

Based on debug output and comparison:
1. Identify the root cause
2. Make the minimal fix needed
3. **Don't over-engineer** - fix THIS bug only

**Example fix:**
```rust
// BUG: wasn't checking t.center
else if t.center {
    Some(TextVSlot::Center)  // ← FIX: explicitly assign Center slot
}
```

### 8. Verify Subtest Passes

Run the subtest again - it should now MATCH:

```bash
mcp__pikru-test__run_pikru_test test45b
```

**Expect:**
```json
{"test_name":"test45b","status":"match","comparison":{"ssim":1.0, ...}}
```

### 9. Remove Debug Output

Clean up the debug statements you added:

```rust
// Remove all the eprintln! statements
// Keep the code clean for production
```

### 10. Verify Original Test Passes

Run the original test to confirm the fix works in context:

```bash
mcp__pikru-test__run_pikru_test test45
```

**If it still fails:**
- There may be MULTIPLE bugs (repeat the process)
- The subtest wasn't complete enough (add more context)
- There's an interaction bug (debug the interaction)

**If it passes:**
- ✅ Bug is fixed!
- ✅ Verify a few other tests still pass
- ✅ Commit with clear message about the fix

### 11. Keep or Remove Subtest

**Keep the subtest if:**
- It tests an important edge case worth preserving
- It could prevent regression
- It's a good minimal example of a feature

**Remove the subtest if:**
- It's purely diagnostic (already covered by original test)
- It duplicates existing test coverage

## Example: test45 → test45b

**Original problem:**
- test45 had complex diagram with files, arrows, boxes
- Bottom box had text positioning bug
- Couldn't see what was wrong amid all the other elements

**Subtest creation:**
```pikchr
# test45b.pikchr - just the problematic box
box "rjust" rjust above "center" center "ljust" ljust above \
    "rjust" rjust below "ljust" ljust below big big
```

**Debug output revealed:**
```
[SLOT HEIGHT] text='center' slot=Above2 ...  ← WRONG! Should be Center
```

**Root cause found:**
- `center` text attribute wasn't being handled in slot assignment
- Text marked "center" was treated as unassigned
- Got first free slot (Above2) instead of Center slot

**Fix applied:**
```rust
// Added center field to PositionedText
// Handle TextAttr::Center in parsing
// Check t.center when assigning initial slots
```

**Result:**
- test45b: MATCH (SSIM 1.0)
- test45: MATCH (SSIM 1.0)
- Bug completely fixed

## Tips and Tricks

### Effective Debug Output

**Show the calculation:**
```rust
eprintln!("calc=[Above: 0.5*{} + 0.5*{} = {}]", hc, ha1, offset);
```

**Track state transitions:**
```rust
eprintln!("[BEFORE] slot={:?} y_offset={}", slot, y_offset);
// ... calculation ...
eprintln!("[AFTER] y_offset={} final_y={}", y_offset, final_y);
```

**Use structured prefixes:**
```rust
[SLOT HEIGHT]   // For slot height calculations
[Y OFFSET]      // For y-coordinate calculations
[ASSIGNMENT]    // For slot assignments
[FINAL]         // For final values
```

### Iterative Refinement

If the first subtest doesn't reproduce the bug:
1. Add back one element at a time
2. Check what's needed to trigger the issue
3. Keep the minimal set that shows the problem

### Multiple Bugs

If you find multiple bugs:
1. Fix them ONE at a time
2. Create separate subtests for each
3. Name them test45b, test45c, etc.
4. Verify each fix independently

### When It's Still Not Clear

If debug output doesn't reveal the issue:
1. Add even MORE detailed logging
2. Compare execution flow with C (use C debug output if available)
3. Check if the bug is earlier in the pipeline (parsing vs rendering)
4. Verify your assumptions about how the code should work

## Checklist

- [ ] Identified specific problem in failing test
- [ ] Created minimal subtest reproducing ONLY that problem
- [ ] Verified subtest fails the same way as original
- [ ] Added targeted debug output
- [ ] Analyzed debug output to find root cause
- [ ] Compared with C implementation output
- [ ] Made minimal fix addressing root cause
- [ ] Verified subtest passes (MATCH status)
- [ ] Removed debug output
- [ ] Verified original test passes
- [ ] Verified other tests still pass
- [ ] Decided whether to keep or remove subtest

## Remember

**The goal is laser focus:**
- Isolate ONE bug
- Understand it completely
- Fix it correctly
- Move on

**Not:**
- Fix multiple bugs at once
- Add features while debugging
- Over-engineer the solution
- Leave debug code in production
