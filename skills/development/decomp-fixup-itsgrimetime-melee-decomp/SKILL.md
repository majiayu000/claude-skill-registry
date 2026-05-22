---
name: decomp-fixup
description: Fix build issues for matched functions in the Melee decompilation project. Use this skill when builds are failing due to header mismatches, signature issues, or caller updates needed after a function has been matched. Invoked with /decomp-fixup [function_name] or automatically when diagnosing build failures.
---

# Melee Build Fixup

You are an expert at fixing build issues in the Melee decompilation project. This skill focuses on resolving compilation errors AFTER a function has been matched to its assembly - the matching work is done, but the build is broken.

## When to Use This Skill

Use `/decomp-fixup` when:
- A matched function causes build failures
- Headers have `UNK_RET`/`UNK_PARAMS` that need real signatures
- Callers need updates after signature changes
- Struct definitions are causing type errors
- Build is failing due to missing prototypes

Use `/decomp` instead when:
- You need to match assembly (get 100% match)
- You're starting fresh on a function

## Finding Functions That Need Fixes

```bash
# Check state for functions that may need build fixes
melee-agent state status

# Look for functions in "committed" state that may have broken builds
# Or check functions with known issues
melee-agent state status <function_name>
```

## Diagnosing Build Errors

### Step 1: Run the Build

```bash
cd <worktree> && python configure.py && ninja
```

The build requires function prototypes by default (same as CI). Common error types:

| Error Pattern | Cause | Solution |
|--------------|-------|----------|
| `implicit declaration of function` | Missing prototype | Add to header |
| `conflicting types for 'func'` | Header/impl mismatch | Fix header signature |
| `too few arguments to function` | Signature changed | Update callers |
| `too many arguments to function` | Signature changed | Update callers |
| `incompatible pointer type` | Type mismatch | Fix types |
| `unknown type name` | Missing include/typedef | Add include |

### Step 2: Locate the Header

Function headers are typically in:
```
melee/include/melee/<module>/forward.h   # Forward declarations
melee/include/melee/<module>/<file>.h    # Full declarations
```

Example paths:
- `ft_*` functions: `melee/include/melee/ft/forward.h` or `melee/include/melee/ft/ftcommon.h`
- `lb*` functions: `melee/include/melee/lb/forward.h`
- `gr*` functions: `melee/include/melee/gr/forward.h`

### Step 3: Find Callers

When you change a function's signature, find and fix all callers:

```bash
grep -r "function_name" <worktree>/src/melee/
grep -r "function_name" <worktree>/include/melee/
```

## Common Fixes

### Fix 1: Header Signature Mismatch

**Problem:** Header has stub declaration, implementation has real signature.

```c
// Before (in header - stub declaration):
/* 0D7268 */ UNK_RET ftCo_800D7268(UNK_PARAMS);

// After (matches implementation):
/* 0D7268 */ void ftCo_800D7268(Fighter* fp, s32 arg1);
```

**Steps:**
1. Find the implementation in `src/melee/`
2. Copy the exact signature
3. Update the header declaration
4. Keep the `/* address */` comment if present

### Fix 2: UNK_RET to Real Return Type

```c
// Before:
UNK_RET func(s32 x);

// After (if implementation returns void):
void func(s32 x);

// After (if implementation returns a value):
s32 func(s32 x);
```

**Note:** `M2C_UNK` can be used as a placeholder return type when the actual type is still being determined.

### Fix 3: UNK_PARAMS to Real Parameters

```c
// Before:
void func(UNK_PARAMS);

// After (from implementation):
void func(HSD_GObj* gobj, s32 action_id, float frame);
```

### Fix 4: Updating Callers

When a signature changes from `void foo(void)` to `void foo(s32 arg)`:

```c
// Before (caller):
foo();

// After (caller - must pass argument):
foo(0);  // Or appropriate value based on context
```

**Finding the right argument:**
- Check assembly at call sites
- Look at r3/r4/etc register values before `bl` instruction
- Check if there's a pattern in similar functions

### Fix 5: Missing Parameter Names

Headers need parameter names for documentation, but types must match:

```c
// Before (missing names):
void func(s32, float, HSD_GObj*);

// After (with names):
void func(s32 action, float frame, HSD_GObj* gobj);
```

### Fix 6: Struct/Type Issues

If a struct field type is wrong:

```c
// Workaround in code (temporary fix):
#define DMG_X1898(fp) (*(float*)&(fp)->dmg.x1898)

// Better: Fix the struct definition in the header
// Before:
s32 x1898;
// After:
float x1898;
```

## Workflow

### Quick Fix (Single Function)

```bash
# 1. Check build error
cd <worktree> && ninja 2>&1 | head -50

# 2. Find header location
grep -r "function_name" <worktree>/include/

# 3. Find implementation
grep -r "function_name" <worktree>/src/melee/

# 4. Compare signatures and fix header

# 5. Find and fix callers if signature changed
grep -r "function_name(" <worktree>/src/melee/

# 6. Rebuild and verify
ninja
```

### Batch Fix (Multiple Issues)

```bash
# 1. Get full error list
cd <worktree> && python configure.py && ninja 2>&1 | tee build_errors.txt

# 2. Categorize errors
grep "conflicting types" build_errors.txt
grep "implicit declaration" build_errors.txt
grep "too few arguments" build_errors.txt

# 3. Fix in dependency order (headers first, then callers)
```

## Committing Fixes

After fixing build issues:

```bash
# Verify build passes
cd <worktree> && python configure.py && ninja

# Commit the fix (in the worktree)
git add -A
git commit -m "Fix build: update <function> signature in header"
```

**Commit message patterns:**
- `Fix build: update ftCo_800D7268 signature in header`
- `Fix build: add missing prototype for lbColl_80008440`
- `Fix build: update callers for gr_800123AB signature change`

## Checklist Before Committing

1. [ ] Build passes
2. [ ] No merge conflict markers in files
3. [ ] Header signatures match implementations exactly
4. [ ] All callers updated if signature changed
5. [ ] No `UNK_RET`/`UNK_PARAMS` left for functions you've implemented

## Common Mistakes

1. **Fixing implementation instead of header** - If match is 100%, don't touch the .c file
2. **Forgetting callers** - One signature change can break many files
3. **Wrong worktree** - Make sure you're in the right subdirectory worktree
4. **Partial fixes** - Don't commit until ALL errors are resolved
5. **Changing matched code** - Only fix headers/callers, not the matched implementation

## Type Reference

Common types in Melee:
- `s8`, `s16`, `s32` - signed integers
- `u8`, `u16`, `u32` - unsigned integers
- `f32`, `f64` - floats
- `BOOL` - boolean (actually s32)
- `HSD_GObj*` - game object pointer
- `Fighter*` - fighter state pointer
- `Vec3` - 3D vector struct
- `M2C_UNK` - unknown type placeholder

## What NOT to Do

1. **Don't modify matched code** - The .c implementation is correct, fix the header
2. **Always verify build passes** - Prototype requirements are enforced by default
3. **Don't leave partial fixes** - Fix everything or nothing
4. **Don't guess signatures** - Check the actual implementation
5. **Don't ignore callers** - They WILL break if signature changes

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't find header | Check `include/melee/<module>/forward.h` |
| Multiple declarations | Search all `.h` files, update all of them |
| Caller in different worktree | Note the file, fix when you work on that subdirectory |
| Circular dependency | May need forward declaration |
| Build still fails after fix | Run `ninja -t clean && ninja` for full rebuild |
