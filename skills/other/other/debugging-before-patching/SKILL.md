---
name: debugging-before-patching
description: Systematic debugging and error diagnosis. Use when debugging errors, fixing bugs, diagnosing problems in code or data, or when the user reports something not working.
user-invocable: false
---

# Debugging Before Patching

When something doesn't work or the user reports an error, **diagnose first — never jump straight to writing fixes**.

## The Process

1. **Diagnose first** — Write diagnostic scripts, print intermediate values, trace data flow. Understand WHY it fails before writing any fix.
2. **Share findings** — Tell the user what you found and what the root cause is.
3. **Propose, don't patch** — Describe the fix and check with the user before implementing.
4. **Never force values** — If names/labels/data don't match, find where the mismatch originates. Don't paper over it with forced assignments.

## What NOT to Do

- Do NOT skip straight to writing patches, especially not multiple rounds of blind patches
- Do NOT guess at fixes and iterate — each failed attempt wastes time and erodes trust
- Do NOT suppress warnings or errors to make code "work"
- Do NOT force-assign values (e.g., hardcoding a name mapping) when the real issue is upstream
- Do NOT silently drop data to avoid errors

## Diagnostic Strategies

### Trace data flow
When a value is wrong at step N, trace backwards:
- What was the value at step N-1? N-2?
- Where did it first become wrong?
- What transformation introduced the error?

### Print intermediate state
```r
# Before the problematic operation
cat("Input dimensions:", nrow(data), "x", ncol(data), "\n")
cat("Key column values:", head(unique(data$key)), "\n")
cat("NAs in key:", sum(is.na(data$key)), "\n")

# After the problematic operation
cat("Output dimensions:", nrow(result), "x", ncol(result), "\n")
```

```python
# Before the problematic operation
print(f"Input dimensions: {data.shape}")
print(f"Key column values: {data['key'].unique()[:10]}")
print(f"NAs in key: {data['key'].isna().sum()}")

# After the problematic operation
print(f"Output dimensions: {result.shape}")
```

### Check assumptions
- Are column names what you expect? (`names(data)` / `data.columns`)
- Are types correct? (`str(data)` / `data.dtypes`)
- Are there unexpected NAs, duplicates, or empty strings?
- Do join keys actually match between datasets?

### Reproduce minimally
When possible, isolate the problem to a small reproducible example before attempting a fix.

## When the User Reports an Error

1. Read the full error message and traceback carefully
2. Identify which line/operation failed
3. Check the state of inputs to that operation (types, dimensions, values)
4. Report what you found before proposing any change
5. If the cause is ambiguous, describe the possibilities and ask the user

## Edge Cases That Require Extra Caution

- **Data mismatches after joins** — almost always means a key mismatch, not a bug to "fix"
- **Unexpected NAs** — trace where they were introduced, don't just `na.rm = TRUE`
- **Wrong labels/names** — find where the naming diverged, don't remap manually
- **Empty results after filtering** — check whether the filter criteria match the actual data values
- **"It worked before"** — check what changed: new data? Updated package? Different environment?