---
name: decomp
description: Match decompiled C code to original PowerPC assembly for Super Smash Bros Melee. Use this skill when asked to match, decompile, or fix a function to achieve 100% match against target assembly. Invoked with /decomp <function_name> or automatically when working on decompilation tasks.
---

# Melee Decompilation Matching

You are an expert at matching C source code to PowerPC assembly for the Melee decompilation project. Your goal is to achieve byte-for-byte identical compilation output.

## Subdirectory Worktrees

The project uses **subdirectory-based worktrees** for parallel agent work. Each source subdirectory gets its own isolated worktree, which enables easy merges since commits to different subdirectories rarely conflict.

**Worktree mapping:**
```
melee/src/melee/lb/*.c     → melee-worktrees/dir-lb/
melee/src/melee/gr/*.c     → melee-worktrees/dir-gr/
melee/src/melee/ft/chara/ftFox/*.c → melee-worktrees/dir-ft-chara-ftFox/
melee/src/melee/ft/chara/ftCommon/*.c → melee-worktrees/dir-ft-chara-ftCommon/
```

**Key points:**
- Source file is **auto-detected** when you claim a function (no flags needed)
- The worktree is created automatically when needed
- Commits stay isolated until collected via `melee-agent worktree collect`
- Local decomp.me server is **auto-detected** (no env vars needed)

**Claiming a function:**
```bash
# Just claim the function - source file is auto-detected
melee-agent claim add lbColl_80008440
```

**High-contention zone:** `ft/chara/ftCommon/` contains 123 behavior files used by ALL characters. Subdirectory locks expire after 30 minutes to prevent blocking.

**Do NOT:**
- Create branches directly in `melee/` - use subdirectory worktrees
- Manually specify `--melee-root` - if you think you need to, stop and ask the user for confirmation, stating your justification
- Work on functions in locked subdirectories owned by other agents

## Worktree State Tracking (CRITICAL)

**Track your worktree state throughout the session.** After every context reset or when resuming work:

```bash
# Verify you're in the correct worktree
pwd                        # Should be melee-worktrees/dir-<module>/
git branch --show-current  # Should be subdirs/<module>
```

**Current session state to remember:**
- **Worktree path**: `melee-worktrees/dir-{module}/`
- **Branch**: `subdirs/{module}`
- **Active function**: (the one you claimed)
- **Active scratch**: (the slug you're iterating on)

**If you're unsure of your location:**
```bash
melee-agent worktree list          # Shows all worktrees
melee-agent claim list             # Shows your active claims
```

**Common mistake after context reset:** Running `git branch` from the project root instead of the worktree, seeing the wrong branch, then committing to the wrong location. Always `cd` to your worktree first.

## Workflow

### Step 0: Automatic Build Validation

When you first run a `melee-agent` command, the system automatically:
1. Validates your worktree builds successfully
2. If the build fails, shows the errors (your uncommitted changes are preserved)
3. Caches the validation result for 30 minutes

You'll see messages like:
- `[dim]Running build validation (this may take a minute)...[/dim]`
- `[green]Worktree build OK[/green]` - you're good to go
- `[yellow]Worktree build has errors - fix before committing[/yellow]` - fix the errors shown

**If build has errors:** Use `/decomp-fixup` skill to diagnose and fix them.

### Step 1: Choose and Claim a Function

**If user specifies a function:** Skip to Step 2.

**Otherwise:** Find a good candidate and claim it:
```bash
# Best: Use recommendation scoring (considers size, match%, module)
melee-agent extract list --min-match 0 --max-match 0.50 --sort score --show-score

# Filter by module for focused work
melee-agent extract list --module lb --sort score --show-score
melee-agent extract list --module ft --sort score --show-score

melee-agent claim add <function_name>  # Claims expire after 3 hours
```

> **CRITICAL:** Once you claim a function, you MUST work on THAT function until completion.
> Do NOT switch to a different function mid-workflow. If `claim add` fails (function already claimed),
> pick a different function from the list. The function you claim is the one you work on.

**Prioritization:** The `--sort score` option ranks functions by:
- **Size:** 50-300 bytes ideal (small enough to match, complex enough to matter)
- **Match %:** Lower is better (more room to improve)
- **Module:** ft/, lb/ preferred (well-documented)

**Avoid 95-99%** matches - remaining diffs are usually context/type issues that require header fixes.

### Step 2: Create Scratch and Read Source

```bash
melee-agent extract get <function_name> --create-scratch
```

This automatically:
- Rebuilds context files to pick up any header changes
- **Preprocesses context** (via `gcc -E`) for m2c decompilation only
- Runs the **m2c decompiler** to generate initial C code with proper type information
- **Restores original context** for MWCC compilation (preprocessed context has GCC-isms)
- If forking an existing scratch, updates context with your local version

**m2c auto-decompilation** provides a rough approximation of the C code with proper types (e.g., `HSD_GObj*` instead of `void*`). Use it as a starting point, then refine.

**To re-run decompilation** on an existing scratch (e.g., after updating context):
```bash
melee-agent scratch decompile <slug>              # Show decompiled code (preprocesses context)
melee-agent scratch decompile <slug> --apply      # Apply to scratch source
melee-agent scratch decompile <slug> -o /tmp/f.c  # Save to file
melee-agent scratch decompile <slug> --no-context # Skip context (faster but less accurate)
```

Then read the source file in `melee/src/` for context. Look for:
- Function signature and local struct definitions (must include these!)
- Nearby functions for coding patterns

### Step 3: Compile and Iterate

Use heredoc with `--stdin` to compile (avoids shell escaping issues):

```bash
cat << 'EOF' | melee-agent scratch compile <slug> --stdin --diff
void func(s32 arg0) {
    if (!arg0 || arg0 != expected) {
        return;
    }
    // ... rest of function
}
EOF
```

**IMPORTANT:** Always use `cat << 'EOF' | ... --stdin` pattern. The quoted `'EOF'` prevents shell expansion of !, !=, $, etc. Do NOT use `--code` with inline source - it corrupts special characters.

The compile shows **match % history**:
```
Compiled successfully!
Match: 85.0%
History: 45% → 71.5% → 85%  # Shows your progress over iterations
```

**Diff markers:**
- `r` = register mismatch → reorder variable declarations
- `i` = offset difference → usually OK, ignore
- `>/<` = extra/missing instruction → check types, casts, operator precedence

**Common fixes:**
- Reorder variable declarations (registers allocated in declaration order)
- Type fixes: `float`→`f32`, `int`→`s32`, `bool`→`BOOL`
- Add/remove parentheses, inline vs temp variables
- Change `if/else` ↔ `switch`

### Step 4: Know When to Stop

- **Match achieved:** score = 0
- **Time limit:** Don't spend more than 10 minutes on a single function
- **Stop iterating:** Stuck with only `r`/`i` diffs, or same changes oscillating

### Step 5: Commit (REQUIRED - DO NOT SKIP)

**Threshold:** Any improvement over the starting match %. Progress is progress.

**BEFORE committing, verify your location:**
```bash
pwd                        # Must be melee-worktrees/dir-<module>/
git branch --show-current  # Must be subdirs/<module>
```

If you're in the wrong directory, `cd` to the correct worktree first. The pre-commit hook will catch this, but it's better to verify upfront.

**Use the workflow command:**
```bash
melee-agent workflow finish <function_name> <slug>
```

This single command:
1. Tests compilation with --dry-run
2. Applies the code to the melee repo
3. Records the function as committed
4. Releases any claims

**If build validation fails** due to header mismatches or caller issues:
```bash
# First, try to fix the issue (use /decomp-fixup skill)
# If unfixable without broader changes, commit anyway with diagnosis:
melee-agent workflow finish <function_name> <slug> --force --diagnosis "Header has UNK_RET but function returns void"
```

The `--force` flag:
- Requires `--diagnosis` to explain why the build is broken
- Stores the diagnosis in the database (visible in `state status`)
- Marks the function as `committed_needs_fix`
- Worktrees with 3+ broken builds block new claims to prevent pile-up

**CRITICAL: Commit Requirements**

Before committing, you MUST ensure:

1. **No merge conflict markers** - Files must not contain `<<<<<<<`, `=======`, or `>>>>>>>` markers.

2. **No naming regressions** - Do not change names of functions, params, variables, etc. from an "english" name to their address-based name, e.g. do not change `ItemStateTable_GShell[] -> it_803F5BA8[]`

3. **No pointer arithmetic/magic numbers** - don't do things like `if (((u8*)&lbl_80472D28)[0x116] == 1) {`, if you find yourself needing to do this to get a 100% match, you should investigate and update the struct definition accordingly.

**Build passes** - The `workflow finish` command validates this. If it fails due to header mismatches or caller issues, use the `/decomp-fixup` skill to resolve them.

## Human Readability

Matching is not just about achieving 100% - the code should be readable. Apply these improvements when the purpose is **clear from the code**:

### Function Names

Rename `fn_XXXXXXXX` when the function's purpose is obvious:
```c
// Before
fn_80022120(data, row, col, &r, &g, &b, &a);

// After - function clearly reads RGBA8 texture coordinates
lbRefract_ReadTexCoordRGBA8(data, row, col, &r, &g, &b, &a);
```

Keep the address-based name if purpose is unclear.

### Parameter Names

Rename parameters when their usage is obvious in the function body:
```c
// Before
void lbBgFlash_800205F0(s32 arg0) {
    if (arg0 < 1) { arg0 = 1; }
    ...
}

// After - clearly a duration/count
void lbBgFlash_800205F0(s32 duration) {
    if (duration < 1) { duration = 1; }
    ...
}
```

Keep `arg0`, `arg1`, etc. if the parameter is unused or purpose is unclear.

### Variable Names

Use descriptive names instead of decompiler defaults:
```c
// Before
s32 temp_r3 = gobj->user_data;
f32 var_f1 = fp->x2C;

// After
FighterData* fp = gobj->user_data;
f32 facing_dir = fp->facing_direction;
```

### Struct Field Access

**Never use pointer arithmetic.** If you need to access a field by offset, update the struct definition:
```c
// BAD - pointer arithmetic
if (((u8*)&lbl_80472D28)[0x116] == 1) {

// GOOD - proper struct access (update struct definition if needed)
if (lbl_80472D28.some_flag == 1) {
```

If you don't know the field name, use an `x` prefix with the offset:
```c
// Acceptable when field purpose is unknown
if (lbl_80472D28.x116 == 1) {
```

**Important:** If you think pointer arithmetic is "required for matching" - you're almost certainly wrong. The real solution is to properly define the struct with correct padding and alignment:

```c
// BAD - pointer arithmetic with index (NEVER DO THIS)
*(s16*)((u8*)gp + idx * 0x1C + 0xDE) = 1;
*(float*)((u8*)gp + idx * 0x1C + 0xCC) += delta;

// GOOD - define the struct properly with padding, then use array access
struct AwningData {
    /* +0x00 */ float accumulator;
    /* +0x04 */ float velocity;
    /* +0x08 */ float position;
    /* +0x0C */ s16 counter;
    /* +0x0E */ s16 prev_counter;
    /* +0x10 */ s16 cooldown;
    /* +0x12 */ s16 flag;
    /* +0x14 */ u8 pad[8];   // Padding to 0x1C stride
};

struct GroundVars {
    u8 x0_b0 : 1;
    u8 pad[0xCC - 0xC5];     // Align array to correct offset
    struct AwningData awnings[2];
};

// Now use clean struct access - this DOES match!
gp->gv.onett.awnings[idx].flag = 1;
gp->gv.onett.awnings[idx].accumulator += delta;
```

The `mulli` instruction pattern (e.g., `mulli r0, r6, 0x1c`) proves the struct stride, which tells you the element size for the array.

### Struct Field Renaming

When you access a field and understand its purpose, rename it:
```c
// Before - in types.h
struct BgFlashData {
    int x4;
    int x8;
    int xC;
};

// After - if you see xC is set from a duration parameter
struct BgFlashData {
    int x4;
    int x8;
    int duration;  // or keep as xC if uncertain
};
```

**Only rename fields you've seen accessed and understood.** Don't guess.

### Conservative Principle

When uncertain, prefer:
- Address-based function names over guessed names
- `arg0`/`arg1` over guessed parameter names
- `x4`/`x8` over guessed field names
- Simple `@brief` over detailed speculative docs

See `/understand` skill for detailed conservative documentation guidelines.

## Type and Context Tips

**Quick struct lookup:** Use the struct command to find field offsets and known issues:
```bash
melee-agent struct offset 0x1898              # What field is at offset 0x1898?
melee-agent struct show dmg --offset 0x1890   # Show fields near offset
melee-agent struct issues                     # Show all known type issues
melee-agent struct callback FtCmd2            # Look up callback signature
melee-agent struct callback                   # List all known callback types
```

**Inspect scratch context (struct definitions, etc.):**
```bash
melee-agent scratch get <slug> --context           # Show context (truncated)
melee-agent scratch get <slug> --grep "StructName" # Search context for pattern
melee-agent scratch get <slug> --diff              # Show instruction diff
melee-agent scratch decompile <slug>               # Re-run m2c decompiler
```

**Refresh context when headers change:**
```bash
melee-agent scratch update-context <slug>          # Rebuild context from repo
melee-agent scratch update-context <slug> --compile  # Rebuild + compile in one step
melee-agent scratch compile <slug> -r              # Compile with refreshed context
```

Use these when:
- You've fixed a header signature in your worktree
- You've updated struct definitions
- Context is stale after pulling upstream changes

**Search context (supports multiple patterns):**
```bash
melee-agent scratch search-context <slug> "HSD_GObj" "FtCmd2" "ColorOverlay"
```

**File-local definitions:** If a function uses a `static struct` defined in the .c file, you MUST include it in your scratch source - the context only has headers.

## Known Type Issues

The context headers may have some incorrect type declarations. When you see assembly that doesn't match the declared type, use these workarounds:

| Field | Declared | Actual | Detection | Workaround |
|-------|----------|--------|-----------|------------|
| `fp->dmg.x1894` | `int` | `HSD_GObj*` | `lwz` then dereferenced | `((HSD_GObj*)fp->dmg.x1894)` |
| `fp->dmg.x1898` | `int` | `float` | Loaded with `lfs` | `(*(float*)&fp->dmg.x1898)` |
| `fp->dmg.x1880` | `int` | `Vec3*` | Passed as pointer arg | `((Vec3*)&fp->dmg.x1880)` |
| `item->xD90.x2073` | - | `u8` | Same as `fp->x2070.x2073` | Access via union field |

**When to suspect a type issue:**
- Assembly uses `lfs`/`stfs` but header declares `int` → should be `float`
- Assembly does `lwz` then immediately dereferences → should be pointer
- Register allocation doesn't match despite correct logic → type mismatch causing extra conversion code

**Workaround pattern:**
```c
/* Cast helpers for mistyped fields */
#define DMG_X1898(fp) (*(float*)&(fp)->dmg.x1898)
#define DMG_X1894(fp) ((HSD_GObj*)(fp)->dmg.x1894)
```

## melee-re Reference Materials

The `melee-re/` submodule contains reverse-engineering documentation that can help with decompilation:

### Symbol Lookup
```bash
# Look up a function by address
grep "80008440" melee-re/meta_GALE01.map

# Find all symbols in an address range
awk '$1 >= "80070000" && $1 < "80080000"' melee-re/meta_GALE01.map
```

### Key Documentation Files

| File | Contents |
|------|----------|
| `melee-re/docs/STRUCT.md` | Function table layouts, callback signatures, memory structures |
| `melee-re/docs/LINKERMAP.md` | Which addresses belong to which modules (SDK, HSD, game code) |
| `melee-re/bin/analysis/ntsc102_defs.py` | Enums for character IDs, stage IDs, action states, item IDs |

### Character ID Mapping

When working on fighter code, know the difference between **external** and **internal** IDs:

```python
# External IDs (CSS order, used in saves/replays)
CaptainFalcon=0x00, DonkeyKong=0x01, Fox=0x02, MrGameNWatch=0x03...

# Internal IDs (used in code, function tables)
Mario=0x00, Fox=0x01, CaptainFalcon=0x02, DonkeyKong=0x03, Kirby=0x04...
```

See `melee-re/bin/analysis/ntsc102_defs.py` for complete mappings.

### Function Table Addresses

From `melee-re/docs/STRUCT.md`:
- **Global action states**: 0x803c2800 (341 entries × 0x20 bytes)
- **Character-specific tables**: 0x803c12e0 (pointers indexed by internal char ID)
- **Stage function tables**: 0x803dfedc (0x1bc bytes, indexed by internal stage ID)
- **Item tables**: 0x803f14c4 (regular), 0x803f3100 (projectiles), 0x803f23cc (pokemon)

### Per-Character Special Move Entry Counts

| Character | Entries | Character | Entries |
|-----------|---------|-----------|---------|
| Mario | 12 | Kirby | 203 |
| Fox | 35 | Marth | 32 |
| Captain Falcon | 23 | Jigglypuff | 32 |
| Link | 31 | Game & Watch | 40 |

Kirby's high count is due to copy abilities.

## PowerPC / MWCC Reference

### Calling Convention
- Integer args: r3, r4, r5, r6, r7, r8, r9, r10
- Float args: f1, f2, f3, f4, f5, f6, f7, f8
- Return: r3 (int/ptr) or f1 (float)

### Register Allocation
- Registers allocated in variable declaration order
- Loop counters often use CTR register (not a GPR)
- Compiler may reorder loads for optimization

### Compiler Flags (Melee)
```
-O4,p -nodefaults -fp hard -Cpp_exceptions off -enum int -fp_contract on -inline auto
```

- `-O4,p` = aggressive optimization with pooling
- `-inline auto` = compiler decides what to inline

## Example Session

```bash
# Find best candidates using recommendation scoring
melee-agent extract list --min-match 0 --max-match 0.50 --sort score --show-score --limit 10
# Pick a function with high score (130+), reasonable size (50-300 bytes)

# Claim the function (source file auto-detected)
melee-agent claim add lbColl_80008440
# → Auto-detected source file: melee/lb/lbcollision.c
# → Claimed: lbColl_80008440
# → Subdirectory: lb
# → Worktree will be at: melee-worktrees/dir-lb/

# Create scratch with full context
melee-agent extract get lbColl_80008440 --create-scratch
# → Created scratch `xYz12`

# Read source file for context, then write and compile
melee-agent scratch compile xYz12 -s /tmp/decomp_xYz12.c --diff
# → 45% match, analyze diff, iterate...

# If stuck, check for type issues
melee-agent struct issues
melee-agent struct offset 0x1898  # What field is at this offset?

# Search for struct definitions in the scratch context
melee-agent scratch search-context xYz12 "CollData" "HSD_GObj"

# Improved the match, FINISH THE FUNCTION (commits + records)
melee-agent workflow finish lbColl_80008440 xYz12

# Check subdirectory worktree status
melee-agent worktree list
```

## Checking Your Progress

Track function states across the pipeline:

```bash
melee-agent state status                  # Shows all tracked functions by category
melee-agent state status --category matched   # Only 95%+ not yet committed
melee-agent state status <func_name>      # Check specific function details
melee-agent state urls <func_name>        # Show all URLs (scratch, PR)
```

**Function statuses:**
- `in_progress` - Being worked on (< 95% match)
- `matched` - 95%+ match, ready to commit
- `committed` - Code applied to repo
- `in_review` - Has an open PR
- `merged` - PR merged to main

## What NOT to Do

1. **Don't search decomp.me first when starting fresh** - find functions from the melee repo
2. **Don't spend >10 minutes on one function** - commit your progress and move on
3. **Don't ignore file-local types** - they must be included in source
4. **Don't keep trying the same changes** - if reordering doesn't help after 3-4 attempts, the issue is likely context-related
5. **Don't skip `workflow finish`** - just marking complete without committing loses your work!
6. **Don't continue working if `claim add` fails** - pick a different function
7. **Don't use raw curl/API calls** - use CLI tools like `scratch get --grep` or `scratch search-context`
8. **Don't switch functions after claiming** - work on the EXACT function you claimed, not a different one

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Undefined identifier | `melee-agent scratch search-context <slug> "name"` or include file-local definition |
| Score drops dramatically | Reverted an inline expansion - try different approach |
| Stuck at same score | Change had no codegen effect - try structural change |
| Only `i` (offset) diffs | Usually fine - focus on `r` and instruction diffs |
| Commit validation fails | Check braces balanced, function name present, not mid-statement |
| Commit compile fails | Missing extern declarations or file-local types - use `--dry-run` first |
| Missing stub marker | Run `melee-agent stub add <function_name>` to add it |
| Stuck at 85-90% with extra conversion code | Likely type mismatch - run `melee-agent struct issues` and check for known issues |
| Assembly uses `lfs` but code generates `lwz`+conversion | Field is float but header says int - use cast workaround |
| Can't find struct offset | `melee-agent struct offset 0xXXX --struct StructName` |
| Struct field not visible in context | Use `M2C_FIELD(ptr, offset, type)` macro for raw offset access |
| Build fails after matching | Use `/decomp-fixup` skill to fix header/caller issues, or `--force --diagnosis` |
| Header has UNK_RET/UNK_PARAMS | Use `/decomp-fixup` skill to update signatures |
| Can't claim function | Worktree may have 3+ broken builds - run `/decomp-fixup` first |
| Context outdated after header fix | `melee-agent scratch update-context <slug>` to rebuild from repo |

**NonMatching files:** You CAN work on functions in NonMatching files. The build uses original .dol for linking, so builds always pass. Match % is tracked per-function.

**Header signature bugs:** If assembly shows parameter usage (e.g., `cmpwi r3, 1`) but header declares `void func(void)`:
1. Use `/decomp-fixup` skill for guidance on fixing headers
2. Fix the header in your worktree
3. Update the scratch context: `melee-agent scratch update-context <slug>` (rebuilds from repo)

## Server Unreachable

If the decomp.me server is unreachable, **STOP and report the issue to the user**. Do NOT attempt to work around it with local-only workflows. The server should always be available - if it's not, something is wrong that needs to be fixed.

## CLI Quick Reference

### Getting Help
```bash
melee-agent --help                    # List all commands
melee-agent scratch --help            # List scratch subcommands
melee-agent scratch compile --help    # Show all flags for compile
```

### Common Flags by Command

| Command | Short | Long | Description |
|---------|-------|------|-------------|
| `scratch compile` | `-s` | `--source` | Source file to compile |
| `scratch compile` | `-d` | `--diff` | Show instruction diff |
| `scratch compile` | `-r` | `--refresh-context` | Rebuild context from repo first |
| `scratch compile` | | `--stdin` | Read source from stdin (use with heredoc) |
| `scratch get` | `-c` | `--context` | Show scratch context |
| `scratch get` | `-d` | `--diff` | Show instruction diff |
| `scratch get` | `-g` | `--grep` | Search context for pattern |
| `scratch update-context` | `-s` | `--source` | Source file for context |
| `scratch update-context` | | `--compile` | Compile after updating |
| `claim add` | `-f` | `--source-file` or `--source` | Source file (auto-detected) |
| `extract list` | | `--module` | Filter by module (e.g., `lb`, `ft`) |
| `extract list` | | `--sort score` | Sort by recommendation score |
| `extract get` | | `--create-scratch` | Create scratch after extracting |
| `extract get` | | `--full` | Show full output including ASM |
| `workflow finish` | | `--force` | Commit even if build has issues |
| `workflow finish` | | `--diagnosis` | Required with `--force` - explain why |

### Heredoc Pattern (Recommended)
```bash
cat << 'EOF' | melee-agent scratch compile <slug> --stdin --diff
void func(void) {
    if (!flag) return;  # Note: quotes around EOF prevent ! escaping
}
EOF
```

## Note on objdiff-cli

The `objdiff-cli diff` command is an **interactive TUI tool for humans** - it requires a terminal and does NOT work for agents. Do not attempt to use it. Agents should always use the decomp.me scratch workflow for matching functions.

If you need to verify match percentage after a build, check `build/GALE01/report.json` which is generated by `ninja`.
