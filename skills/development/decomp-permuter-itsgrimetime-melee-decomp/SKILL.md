---
name: decomp-permuter
description: Use the decomp-permuter to automatically find C code variations that match target assembly. Useful when stuck at 99%+ match with stubborn register allocation issues. Invoked with /decomp-permuter <function_name> <scratch_slug> or when manual matching attempts are exhausted.
---

# Decomp Permuter Skill

Use this skill when you're stuck at a high match percentage (95%+) but can't find the exact code that produces a 100% match. The permuter automatically tries thousands of code variations to find one that matches.

## When to Use

- Stuck at 99%+ match with only register allocation (`r`) diffs
- Manual reordering of declarations hasn't helped
- The diff shows consistent register mismatches (e.g., target uses r5, you get r6)
- You've tried multiple approaches but can't find the right combination

## Prerequisites

The decomp-permuter is located at `~/code/decomp-permuter`.

**Required tools:**
- Python 3 with `pycparser`, `toml`, `Levenshtein` packages
- devkitPPC at `/opt/devkitpro/devkitPPC/bin/` (assembler, objdump)
- Wine (for MWCC compiler)

## Quick Start (import.py)

The melee-decomp project has `permuter_settings.toml` in the root directory. Copy it to melee before using import.py:

```bash
# Copy permuter settings to melee (required before import.py)
cp ~/code/melee-decomp/permuter_settings.toml ~/code/melee-decomp/melee/

cd ~/code/decomp-permuter

# Import with explicit assembly file and function name
./import.py \
  ~/code/melee-decomp/melee/src/melee/path/to/file.c \
  ~/code/melee-decomp/melee/build/GALE01/asm/melee/path/to/file.s \
  --function <func_name> \
  --no-prune  # Avoid pycparser round-trip issues

# Run the permuter
cd ~/code/melee-decomp/melee
~/code/decomp-permuter/permuter.py nonmatchings/<func_name> -j4

# Clean up when done (don't commit permuter_settings.toml to melee)
rm ~/code/melee-decomp/melee/permuter_settings.toml
```

**IMPORTANT:** The `--no-prune` flag is recommended to avoid pycparser creating duplicate struct definitions.

## Recommended: Manual Minimal Setup

For best results with Melee, create a minimal base.c manually. This avoids pycparser issues:

### Why Manual Setup?

The import.py's pycparser round-trip often creates issues:
- Duplicate struct definitions for unions with anonymous members
- Type mismatches from forward declarations
- Large 20K+ line files that are slow to permute

A minimal 100-line base.c is faster and more reliable.

### Step 1: Create the function directory

```bash
mkdir -p ~/code/melee-decomp/melee/nonmatchings/<func_name>
cd ~/code/melee-decomp/melee/nonmatchings/<func_name>
```

### Step 2: Create settings.toml

```toml
func_name = "<func_name>"
compiler_type = "mwcc"
objdump_command = "/opt/devkitpro/devkitPPC/bin/powerpc-eabi-objdump -dr -EB -mpowerpc -M broadway"

# Optional: Tune weights for register allocation issues
[weight_overrides]
perm_reorder_decls = 50.0
perm_temp_for_expr = 30.0
perm_expand_expr = 20.0
```

### Step 3: Create compile.sh

```bash
cat > compile.sh << 'COMPILE_EOF'
#!/usr/bin/env bash
INPUT="$(realpath "$1")"
OUTPUT="$(realpath "$3")"
cd /Users/mike/code/melee-decomp/melee
wine build/compilers/GC/1.2.5n/mwcceppc.exe \
    -Cpp_exceptions off -proc gekko -fp hard -fp_contract on -O4,p \
    -enum int -nodefaults -inline auto -c \
    -i src -i src/MSL -i src/Runtime -i extern/dolphin/include \
    -i src/melee -i src/melee/ft/chara -i src/sysdolphin \
    -DBUILD_VERSION=0 -DVERSION_GALE01 \
    "$INPUT" -o "$OUTPUT" 2>/dev/null
COMPILE_EOF
chmod +x compile.sh
```

### Step 4: Create base.c (Minimal Approach - RECOMMENDED)

Create a minimal base.c with only the necessary type definitions and the target function.
Use C-style comments only (no `//` comments - pycparser doesn't support them).

**Template:**

```c
/* Minimal base.c for <func_name> */
/* Type definitions - only what's needed */

typedef int s32;
typedef unsigned int u32;
typedef float f32;
typedef int bool;
typedef unsigned char u8;

typedef struct Vec3 {
    f32 x, y, z;
} Vec3;

/* Forward declarations for opaque types */
typedef struct HSD_JObj HSD_JObj;

/* Struct definitions with correct offsets */
typedef struct HSD_GObj {
    u8 pad[0x28];
    void* hsd_obj;    /* 0x28 */
    void* user_data;  /* 0x2C */
} HSD_GObj;

/* ... add more structs as needed ... */

/* External function declarations */
void SomeFunction(void);
void AnotherFunction(s32 arg);

/* THE TARGET FUNCTION */
void <func_name>(HSD_GObj* gobj)
{
    /* Copy from your scratch or melee source */
}
```

**Key rules for base.c:**
1. Use C-style `/* comments */` only (no `//` comments)
2. No `#define` macros - inline constant values
3. Include only structs that are directly accessed
4. Add padding bytes to get correct field offsets

### Step 5: Create target.s

Copy the target assembly from the build output, adding the macros.inc prelude:

```bash
ASM_FILE=~/code/melee-decomp/melee/build/GALE01/asm/melee/path/to/file.s

# Copy the macros prelude
cat ~/code/melee-decomp/melee/build/GALE01/include/macros.inc > target.s

# Extract just the target function (.fn ... .endfn block)
# Find the function and copy from .fn to .endfn
sed -n '/\.fn <func_name>/,/\.endfn <func_name>/p' "$ASM_FILE" >> target.s
```

**Or manually:** Open the assembly file, find the `.fn <func_name>` line, copy everything up to and including `.endfn <func_name>`, and paste after the macros.inc content.

### Step 6: Assemble target.o

```bash
/opt/devkitpro/devkitPPC/bin/powerpc-eabi-as \
  -mgekko \
  -I ~/code/melee-decomp/melee/build/GALE01/include \
  target.s \
  -o target.o
```

**Note:** Make sure you're in the nonmatchings/<func_name>/ directory when running this.

## Running the Permuter

```bash
# Run from the melee directory (where nonmatchings/ was created)
cd ~/code/melee-decomp/melee

# Basic run with 4 threads (recommended)
~/code/decomp-permuter/permuter.py nonmatchings/<func_name> -j4

# Debug mode (shows what's happening, useful for first run)
~/code/decomp-permuter/permuter.py nonmatchings/<func_name> --debug

# Run with specific seed (reproducible)
~/code/decomp-permuter/permuter.py nonmatchings/<func_name> -j4 --seed 12345

# Run for a specific number of iterations
~/code/decomp-permuter/permuter.py nonmatchings/<func_name> -j4 --iterations 10000
```

**Scores:**
- Score = 0 means **perfect match**
- Lower score = better match
- Starting scores around 3000-5000 are common
- The permuter saves improvements to `nonmatchings/<func_name>/output-<score>-<n>/`

## Using PERM Macros

For more targeted permutation, add PERM macros to base.c:

```c
// Try two alternatives for an expression
PERM_GENERAL(a = b + c;, a = c + b;)

// Reorder lines
PERM_LINESWAP(
    x = 1;
    y = 2;
    z = 3;
)

// Enable randomization for a block
PERM_RANDOMIZE(
    // permuter will try variations here
    sp.x = sp.x * attr->x4;
    sp.y = sp.y * attr->x4;
    sp.z = sp.z * attr->x4;
)

// Try integers in a range
int val = PERM_INT(0, 10);
```

## Interpreting Results

The permuter shows real-time progress:

```
iteration 935, 13 errors, score = 3910
[it_802CE400] found a better score! (3830 vs 3915)
wrote to nonmatchings/it_802CE400/output-3830-2
```

**Output directory structure:**
```
nonmatchings/<func_name>/
├── base.c           # Your input source
├── compile.sh       # Compilation script
├── settings.toml    # Permuter settings
├── target.s         # Target assembly
├── target.o         # Assembled target
└── output-3830-2/   # Best result found (score 3830)
    ├── source.c     # The improved source code
    ├── diff.diff    # What changed from base.c
    └── score.txt    # The score
```

When a better match is found:
1. Check `output-<score>-<n>/source.c` for the improved code
2. Check `output-<score>-<n>/diff.diff` for what changed
3. Apply the changes to your scratch and verify

## Common Issues

### "Failed to parse C file"

**Cause:** pycparser can't handle some C constructs

**Fix:** Add PERM_IGNORE around problematic code:
```c
PERM_IGNORE(
__asm__ { /* inline asm */ }
)
```

### Duplicate struct definitions after round-trip

**Cause:** pycparser produces duplicate definitions when round-tripping

**Fix:** Use `--no-prune` flag or manually fix base.c:
```bash
./import.py --no-prune path/to/file.c func_name
```

### Assembly file uses .fn/.endfn not glabel

**Note:** import.py handles this format automatically (as of recent versions).

### Include paths not found

**Fix:** The melee project needs `build_system = "ninja"` in permuter_settings.toml for import.py to extract include paths correctly.

## Weight Tuning

For register allocation issues, increase these weights in settings.toml:

```toml
[weight_overrides]
# Higher weight = more likely to try
perm_reorder_decls = 50.0   # Reorder variable declarations
perm_temp_for_expr = 30.0   # Create temp variables
perm_expand_expr = 20.0     # Expand expressions
perm_sameline = 10.0        # Put statements on same line
```

## Workflow Integration

After the permuter finds improvements:

```bash
# 1. Check the best result
cat ~/code/melee-decomp/melee/nonmatchings/<func_name>/output-*/diff.diff | head -30

# 2. Copy the improved source, extracting just the function
# The source.c contains full type defs - extract only the function body

# 3. Integrate changes into your scratch
# Copy the relevant changes from the permuter output to your scratch source

# 4. Compile with your scratch to verify
cat << 'EOF' | melee-agent scratch compile <slug> --stdin --diff
// Your updated function here
EOF

# 5. If improved/matched, commit with workflow
melee-agent workflow finish <func_name> <slug>
```

## Cleanup

After finishing, clean up the nonmatchings directory:

```bash
rm -rf ~/code/melee-decomp/melee/nonmatchings/<func_name>
```

## Reference

- Permuter repo: `~/code/decomp-permuter`
- Documentation: `~/code/decomp-permuter/README.md`
- Manual setup: `~/code/decomp-permuter/USAGE.md`
- Default weights: `~/code/decomp-permuter/default_weights.toml`
- Melee permuter settings: `~/code/melee-decomp/permuter_settings.toml`
