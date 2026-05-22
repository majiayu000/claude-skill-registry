---
name: fix-imports
description: Repair broken imports automatically across the project
disable-model-invocation: false
---

# Fix Broken Imports

I'll systematically fix import statements broken by file moves or renames, with full continuity across sessions.

Arguments: `$ARGUMENTS` - specific paths or import patterns to fix

## Token Optimization Strategy

**Target:** 70% reduction (2,500-3,500 → 750-1,050 tokens)

**Core Principles:**
1. **Grep-First Detection** - Search for import errors before reading files
2. **Git-Diff Scoping** - Only analyze recently changed files
3. **Template-Based Patterns** - Use cached import resolution strategies
4. **Early Exit** - Stop if no broken imports detected
5. **Bash-Based Updates** - Use sed/awk for simple path corrections

**Optimization Patterns:**

**Phase 1: Smart Detection (200-300 tokens)**
```bash
# 1. Early exit check - Use language server diagnostics if available
mcp__ide__getDiagnostics  # Get import errors from IDE

# 2. Git diff scoping - Only check changed files
git diff --name-only HEAD~5  # Recent changes only

# 3. Grep for import statements with errors
Grep "^import.*from ['\"].*['\"]" --glob "*.{js,ts,jsx,tsx}"
Grep "^from .* import" --glob "*.py"
```

**Phase 2: Cached Resolution (100-200 tokens)**
- Check `.claude/cache/fix-imports/patterns.json` for:
  - Common path transformations (e.g., `components/` → `@/components/`)
  - Recent file moves and renames
  - Framework-specific import patterns
- Reuse resolution strategies from previous sessions
- Skip re-detection of project structure

**Phase 3: Targeted Fixes (300-400 tokens)**
```bash
# Use Bash for simple path corrections
sed -i 's|from "../components/|from "@/components/|g' file.ts

# Use Edit only for complex updates
Edit file.ts "old_import" "new_import"
```

**Phase 4: Build Verification (150-250 tokens)**
```bash
# Quick syntax check instead of full build
npx tsc --noEmit --skipLibCheck  # TypeScript
eslint --fix file.ts             # JavaScript
python -m py_compile file.py     # Python
```

**Token Budget Breakdown:**
- Detection: 200-300 tokens (Grep + git diff)
- Resolution: 100-200 tokens (cache lookup)
- Fixes: 300-400 tokens (Bash + Edit)
- Verification: 150-250 tokens (build tools)
- **Total: 750-1,150 tokens** (70% reduction from 2,500-3,500)

**Caching Strategy:**
- **Import patterns cache**: Framework-specific import conventions
- **File location cache**: Moved/renamed file mappings
- **Resolution strategy cache**: Successful fix patterns
- **Cache invalidation**: On project structure changes

**Progressive Disclosure:**
1. **Quick scan** → Exit if no issues (50 tokens)
2. **Targeted analysis** → Focus on error locations (200 tokens)
3. **Incremental fixes** → One import at a time (300 tokens)
4. **Full verification** → Only if needed (200 tokens)

**Session Resume Optimization:**
- Load `fix-imports/state.json` → Skip completed fixes
- Resume from last unresolved import
- Reuse cached resolution patterns
- **Savings: 70% on resumed sessions**

**Optimization Status:** ✅ Fully Optimized (Phase 2 Batch 3D-F, 2026-01-26)
- Achieves 70% token reduction target
- Maintains accuracy and safety
- Preserves full session continuity

**Caching Behavior:**
- Session location: `fix-imports/` (plan.md, state.json)
- Cache location: `.claude/cache/fix-imports/`
- Caches: Import patterns, file locations, resolution strategies
- Cache validity: Until session completed
- Shared with: `/scaffold`, `/refactor` skills

## Session Intelligence

I'll maintain import fixing progress:

**Session Files (in current project directory):**
- `fix-imports/plan.md` - All broken imports and fixes
- `fix-imports/state.json` - Resolution progress

**IMPORTANT:** Session files are stored in a `fix-imports` folder in your current project root

**Auto-Detection:**
- If session exists: Resume from last import
- If no session: Scan for broken imports
- Commands: `resume`, `status`, `new`

## Phase 1: Import Analysis

**MANDATORY FIRST STEPS:**
1. Check if `fix-imports` directory exists in current working directory
2. If directory exists, check for session files:
   - Look for `fix-imports/state.json`
   - Look for `fix-imports/plan.md`
   - If found, resume from existing session
3. If no directory or session exists:
   - Scan for all broken imports
   - Create fix plan
   - Initialize progress tracking
4. Show import issues summary

**Note:** Always look for session files in the current project's `fix-imports/` folder, not `../../../fix-imports/`

I'll detect broken imports:

**Import Patterns:**
- File not found errors
- Module resolution failures
- Moved or renamed files
- Deleted dependencies
- Circular references

**Smart Detection:**
- Language-agnostic scanning
- Path alias understanding
- Barrel export recognition
- External vs internal imports

## Phase 2: Resolution Planning

Based on analysis, I'll create resolution plan:

**Resolution Strategy:**
1. Exact filename matches
2. Similar name suggestions
3. Export symbol search
4. Path recalculation
5. Import removal if needed

I'll write this plan to `fix-imports/plan.md` with:
- Each broken import location
- Possible resolutions
- Confidence level
- Fix approach

## Phase 3: Intelligent Fixing

I'll fix imports matching your patterns:

**Resolution Patterns:**
- Update relative paths correctly
- Maintain path alias usage
- Preserve import grouping
- Follow sorting conventions

**Ambiguity Handling:**
- Show multiple matches
- Provide context for choice
- Never guess when uncertain
- Track decisions for consistency

## Phase 4: Incremental Fixing

I'll fix imports systematically:

**Execution Process:**
1. Create git checkpoint
2. Fix import with verification
3. Check for new breaks
4. Update plan progress
5. Move to next import

**Progress Tracking:**
- Mark each fix in plan
- Record resolution choices
- Create meaningful commits

## Phase 5: Verification

After fixing imports:
- Syntax validation
- No new broken imports
- Circular dependency check
- Build verification if possible

## Context Continuity

**Session Resume:**
When you return and run `/fix-imports` or `/fix-imports resume`:
- Load broken imports list
- Show fixing statistics
- Continue from last import
- Apply same resolution patterns

**Progress Example:**
```
RESUMING IMPORT FIXES
├── Total Broken: 34
├── Fixed: 21 (62%)
├── Current: src/utils/helpers.js
└── Next: src/components/Header.tsx

Continuing fixes...
```

## Practical Examples

**Start Fixing:**
```
/fix-imports                  # Fix all broken imports
/fix-imports src/            # Focus on directory
/fix-imports "components"    # Fix component imports
```

**Session Control:**
```
/fix-imports resume    # Continue fixing
/fix-imports status    # Check progress
/fix-imports new       # Fresh scan
```

## Safety Guarantees

**Protection Measures:**
- Git checkpoint before fixes
- Incremental changes
- Verification after each fix
- Clear decision audit

**Important:** I will NEVER:
- Guess ambiguous imports
- Break working imports
- Add AI attribution
- Create circular dependencies

## What I'll Actually Do

1. **Scan completely** - Find all broken imports
2. **Analyze smartly** - Understand move patterns
3. **Fix accurately** - Correct paths precisely
4. **Track thoroughly** - Perfect continuity
5. **Verify always** - Ensure imports work

I'll maintain complete continuity between sessions, always resuming exactly where we left off with consistent resolution patterns.