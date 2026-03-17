---
name: cfn-compilation-error-fixer
description: "Two-phase compilation error fixer for Rust and TypeScript using Cerebras LLM bulk processing + dedicated agent cleanup. Use when you have 20+ compilation errors that need fast bulk reduction, or when errors are mostly mechanical (type mismatches, missing imports, syntax issues)."
version: 2.0.0
tags: [rust, typescript, compilation, cerebras, error-fixer, cfn]
status: production
---

# CFN Compilation Error Fixer

Two-phase workflow for fixing large-scale compilation errors in Rust and TypeScript projects using Cerebras LLM bulk processing + dedicated agent cleanup.

## Skill Structure

```
.claude/skills/cfn-compilation-error-fixer/
├── SKILL.md                          # This file
├── HANDOFF.md                        # Detailed handoff documentation
├── package.json                      # Dependencies and npm scripts
├── index.js                          # Main entry point
├── bin/
│   └── fix-errors.sh                 # Executable script
├── lib/
│   └── fixer/
│       ├── package.json              # Runtime dependencies
│       ├── cerebras-wrapper.ts       # Cerebras SDK wrapper
│       ├── cerebras-gated-fixer-v2.ts # Rust fixer (self-contained)
│       ├── typescript-gated-fixer-v2.ts # TypeScript fixer (self-contained)
│       └── tsconfig.json             # TypeScript configuration
└── lib/
    └── gates/
        └── typescript-gates.ts       # TypeScript validation gates
```

## Overview

This skill orchestrates:
1. **Phase 1**: Cerebras LLM bulk fixer (fast, cheap, ~95%+ reduction)
2. **Phase 2**: Dedicated CFN agent (high quality cleanup)

## Phase 1: Cerebras Bulk Fixer

### When to Use
- 20+ compilation errors
- Need fast bulk reduction
- Errors are mostly mechanical (type mismatches, missing imports, syntax issues)
- Both Rust and TypeScript projects supported

### How to Run - Rust

```bash
# Setup (one-time)
cd /mnt/c/Users/masha/Documents/claude-flow-novice/.claude/skills/cfn-compilation-error-fixer
npm install

# Option 1: Run from skill directory
export CEREBRAS_API_KEY="your-key"
npm run fix:rust

# Option 2: Run from your Rust project directory
cd /path/to/your/rust-project
export CEREBRAS_API_KEY="your-key"
npx tsx /mnt/c/Users/masha/Documents/claude-flow-novice/.claude/skills/cfn-compilation-error-fixer/lib/fixer/cerebras-gated-fixer-v2.ts

# Option 3: Use the executable script
./bin/fix-errors.sh rust

# Option 4: Use Node.js entry point
node index.js rust

# Additional flags
npm run fix:rust -- --dry-run        # Preview patches without writing
npm run fix:rust -- --verbose        # Debug output
npm run fix:rust -- --no-layer3      # Skip LLM review layer
npm run fix:rust -- --no-clippy      # Skip clippy checks

# With explicit project path
npx tsx cerebras-gated-fixer-v2.ts --project=/path/to/rust-project

# With environment variable
export RUST_PROJECT_PATH=/path/to/rust-project
npx tsx cerebras-gated-fixer-v2.ts
```

### How to Run - TypeScript

```bash
# Setup (one-time)
cd /mnt/c/Users/masha/Documents/claude-flow-novice/.claude/skills/cfn-compilation-error-fixer
npm install

# Option 1: Run from skill directory
export CEREBRAS_API_KEY="your-key"
npm run fix:ts

# Option 2: Run from your TypeScript project directory
cd /path/to/your/typescript-project
export CEREBRAS_API_KEY="your-key"
npx tsx /mnt/c/Users/masha/Documents/claude-flow-novice/.claude/skills/cfn-compilation-error-fixer/lib/fixer/typescript-gated-fixer-v2.ts

# Option 3: Use the executable script
./bin/fix-errors.sh typescript
./bin/fix-errors.sh ts  # Short form

# Option 4: Use Node.js entry point
node index.js typescript
node index.js ts

# Additional flags
npm run fix:ts -- --dry-run          # Preview patches without writing
npm run fix:ts -- --verbose          # Debug output

# With explicit project path
npx tsx typescript-gated-fixer-v2.ts --project=/path/to/typescript-project
```

### Architecture

```
┌─────────────────┐
│  cargo check    │ → Parse Rust errors
└────────┬────────┘
         ▼
┌─────────────────┐
│ Cerebras LLM    │ → Generate fix (zai-glm-4.6)
└────────┬────────┘
         ▼
┌─────────────────────────────────────────┐
│     LAYER 1: 12 Structural Gates        │
├─────────────────────────────────────────┤
│ A: LineCount    B: FnSignature          │
│ C: ImportDup    D: BraceBalance         │
│ E: SemanticDiff F: OrphanedCode         │
│ G: ImportPath   H: PatternDup           │
│ I: ImplLocation J: TypeCast             │
│ K: MatchArm     L: Regression           │
└────────┬────────────────────────────────┘
         ▼ (up to 3 retries with feedback)
┌─────────────────────────────────────────┐
│     LAYER 2: cargo check validation     │
└────────┬────────────────────────────────┘
         ▼
┌─────────────────────────────────────────┐
│     LAYER 3: LLM Review Gate            │
└────────┬────────────────────────────────┘
         ▼
┌─────────────────┐
│  Write to file  │
└─────────────────┘
```

### Expected Results

#### Rust
- **Input**: 200+ errors
- **Output**: 10-20 errors (95%+ reduction)
- **Quality**: 4-5/10 (some semantic issues)

#### TypeScript
- **Input**: 100+ errors
- **Output**: 5-10 errors (95%+ reduction)
- **Quality**: 4-5/10 (some semantic issues)

### Logs
- `/tmp/rust-fix-patches/` - Rust fix patches directory
- `/tmp/typescript-fix-patches/` - TypeScript fix patches directory
- `/tmp/v2-retry-run.log` - Full run output
- `/tmp/gate-rejections.json` - Gate rejection details
- Console output with detailed progress

---

## Phase 2: Dedicated Agent Cleanup

### When to Use
- After Phase 1 completes
- <20 errors remaining (Rust) or <10 errors (TypeScript)
- Need high-quality fixes (8-10/10)
- Errors are semantic or complex

### How to Invoke - Rust

Spawn a rust-developer or cfn-system-expert agent with this prompt:

```
You are a Rust compilation error fixer. Fix the remaining errors in the Rust codebase.

CONTEXT:
- Cerebras LLM already fixed ~95% of errors
- Quality validation found some semantic issues in applied fixes
- Remaining errors need high-quality fixes

WORKING DIRECTORY:
cd <YOUR_RUST_PROJECT_PATH>  # e.g., /path/to/rust-project

STEP 1: Get current error count and locations
SQLX_OFFLINE=true cargo check 2>&1 | grep -E "^error\[E" | sort | uniq -c | sort -rn

STEP 2: For each error file, fix in order of dependency:
1. Read the FULL file to understand context
2. Identify the root cause (not just the symptom)
3. Apply minimal fix that preserves semantics
4. Run SQLX_OFFLINE=true cargo check to verify
5. If new errors appear, fix those too

RULES:
- Read FULL file before editing (not just error snippets)
- Preserve ALL existing imports, don't duplicate
- Use proper Rust idioms (? operator, as casts, trait bounds)
- Fix root causes first (cascading errors will resolve)
- Verify with cargo check after EACH file
- Maintain CFN compliance standards

COMMON ERROR TYPES:
- E0308 (type mismatch): Add explicit casts or fix generics
- E0412/E0433/E0425 (missing type/import): Add use statements
- E0599 (wrong method): Fix method chain (e.g., .ok_or_else() on Result)
- E0277 (trait not implemented): Add trait implementations
- E0382 (borrow checker): Fix ownership issues

Report final error count when done.
```

### How to Invoke - TypeScript

Spawn a typescript-developer or cfn-system-expert agent with this prompt:

```
You are a TypeScript compilation error fixer. Fix the remaining errors in the TypeScript codebase.

CONTEXT:
- Cerebras LLM already fixed ~95% of errors
- Quality validation found some semantic issues in applied fixes
- Remaining errors need high-quality fixes

WORKING DIRECTORY:
cd <YOUR_TYPESCRIPT_PROJECT_PATH>  # e.g., /path/to/typescript-project

STEP 1: Get current error count and locations
npm run type-check 2>&1 | grep -E "error TS" | sort | uniq -c | sort -rn

STEP 2: For each error file, fix in order of dependency:
1. Read the FULL file to understand context
2. Identify the root cause (not just the symptom)
3. Apply minimal fix that preserves semantics
4. Run npm run type-check to verify
5. If new errors appear, fix those too

RULES:
- Read FULL file before editing (not just error snippets)
- Preserve ALL existing imports, don't duplicate
- Use proper TypeScript idioms (type guards, interfaces, generics)
- Fix root causes first (cascading errors will resolve)
- Verify with tsc after EACH file
- Maintain CFN compliance standards

COMMON ERROR TYPES:
- TS2307 (module not found): Fix import paths or install missing packages
- TS2322 (type mismatch): Add type annotations or fix type inference
- TS2339 (property not exists): Add interface definitions or type assertions
- TS7006 (implicit any): Add explicit type annotations
- TS2688 (cannot find type definition): Install @types packages

Report final error count when done.
```

### Expected Results
- **Input**: 10-20 errors (Rust) or 5-10 errors (TypeScript)
- **Output**: 0 errors
- **Quality**: 9-10/10

---

## Full Workflow Example

### Rust Workflow

```bash
# 1. Check initial error count
cd <YOUR_RUST_PROJECT_PATH>
SQLX_OFFLINE=true cargo check 2>&1 | grep -c "^error\["
# Output: 342

# 2. Run Phase 1 (Cerebras bulk fixer)
cd /mnt/c/Users/masha/Documents/claude-flow-novice/.claude/skills/cfn-compilation-error-fixer
export CEREBRAS_API_KEY="your-key"
npm run fix:rust 2>&1 | tee /tmp/rust-fix.log
# Output: 342 → 15 (95.6% reduction)

# 3. Validate Phase 1 results
cd <YOUR_RUST_PROJECT_PATH>
SQLX_OFFLINE=true cargo check 2>&1 | grep -E "^error\[" | wc -l
# Output: 15

# 4. Run Phase 2 (dedicated agent cleanup)
# Spawn rust-developer agent with prompt above
# Output: 15 → 0

# 5. Final verification
SQLX_OFFLINE=true cargo check
# Output: Finished dev profile [unoptimized + debuginfo] target(s) in X.XXs
```

### TypeScript Workflow

```bash
# 1. Check initial error count
cd <YOUR_TYPESCRIPT_PROJECT_PATH>
npm run type-check 2>&1 | grep -c "error TS"
# Output: 156

# 2. Run Phase 1 (Cerebras bulk fixer)
cd /mnt/c/Users/masha/Documents/claude-flow-novice/.claude/skills/cfn-compilation-error-fixer
export CEREBRAS_API_KEY="your-key"
npm run fix:ts 2>&1 | tee /tmp/typescript-fix.log
# Output: 156 → 7 (95.5% reduction)

# 3. Validate Phase 1 results
cd <YOUR_TYPESCRIPT_PROJECT_PATH>
npm run type-check 2>&1 | grep "error TS" | wc -l
# Output: 7

# 4. Run Phase 2 (dedicated agent cleanup)
# Spawn typescript-developer agent with prompt above
# Output: 7 → 0

# 5. Final verification
npm run type-check
# Output: No type errors found
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `./HANDOFF.md` | Detailed handoff documentation |
| `./lib/fixer/cerebras-gated-fixer-v2.ts` | Rust fixer (self-contained) |
| `./lib/fixer/typescript-gated-fixer-v2.ts` | TypeScript fixer (self-contained) |
| `./lib/gates/typescript-gates.ts` | TypeScript validation gates |
| `./bin/fix-errors.sh` | Executable wrapper script |
| `./index.js` | Node.js entry point |
| `/tmp/gate-rejections.json` | Gate rejection log (runtime) |
| `/tmp/v2-retry-run.log` | Full run output (runtime) |
| `/tmp/rust-fix-patches/` | Rust fix patches (runtime) |
| `/tmp/typescript-fix-patches/` | TypeScript fix patches (runtime) |

## Environment Requirements

### System Requirements
- Node.js 18+
- Rust 1.70.0+ (for Rust projects)
- TypeScript 4.5+ (for TypeScript projects)

### Environment Variables
- `CEREBRAS_API_KEY`: Your Cerebras API key (required for LLM fixes)
- `CFN_ALLOW_FALLBACK=true`: Allow running without Cerebras SDK (read-only mode)
- `SQLX_OFFLINE=true`: For cargo check without database (Rust projects)
- `RUST_PROJECT_PATH`: Override default Rust project path
- `TYPESCRIPT_PROJECT_PATH`: Override default TypeScript project path

### Default Project Paths
- Rust: `/mnt/c/Users/masha/Documents/ourstories-v2/services/rust-services`
- TypeScript: Current working directory

---

## Troubleshooting

### Common Issues

1. **"tsx is not installed"**
   ```bash
   npm install -g tsx
   # Or use local version
   npx tsx [file]
   ```

2. **"Cerebras SDK not found"**
   - Install the SDK: `npm install @cerebras/cerebras_cloud_sdk`
   - Or use fallback mode: `CFN_ALLOW_FALLBACK=true npm run fix:rust`

3. **Permission denied on fix-errors.sh**
   ```bash
   chmod +x bin/fix-errors.sh
   ```

4. **"Module not found" errors**
   ```bash
   cd /mnt/c/Users/masha/Documents/claude-flow-novice/.claude/skills/cfn-compilation-error-fixer
   npm install
   ```

5. **High memory usage**
   - Use `--max-tokens 2000` to limit LLM response size
   - Process errors in smaller batches

### Debug Mode

Enable verbose logging to see detailed processing:
```bash
npm run fix:rust -- --verbose
npm run fix:ts -- --verbose
```

### Performance Tuning

- For large codebases (500+ errors): Use `--parallel-calls 5` to reduce API calls
- For slow systems: Use `--no-layer3` to skip LLM review
- For quick testing: Use `--dry-run` to preview fixes

### Recovery

If fixes break the build:
```bash
# Rust
cd <RUST_PROJECT>
git checkout -- src/
SQLX_OFFLINE=true cargo check

# TypeScript
cd <TYPESCRIPT_PROJECT>
git checkout -- src/
npm run type-check
```