---
name: make-it-pretty
description: Improve code readability through formatting and structure enhancements
disable-model-invocation: false
---

# Make It Pretty

I'll improve code readability while preserving exact functionality.

## Token Optimization Strategy

**Target Reduction: 65%** (3,000-4,500 → 1,050-1,575 tokens)

### Core Optimization Patterns

**1. Focused Scope (Save 60-70%)**
```bash
# ❌ AVOID: Reading entire codebase
Glob "**/*.{js,ts,jsx,tsx,py}" && Read all files

# ✅ PREFER: Focused file analysis
# User-specified file
Read "/path/to/specific-file.ts"

# OR recently changed code
git diff --name-only HEAD~3 | head -5
Read changed-files-only
```

**2. Template-Based Formatting (Save 50-60%)**
```bash
# ❌ AVOID: Manual formatting analysis
Read file → analyze patterns → apply improvements

# ✅ PREFER: Template-based patterns
# Use cached style patterns from .claude/cache/make-it-pretty/
1. Load project style guide (if cached)
2. Apply consistent naming conventions
3. Use formatter configs (prettier, black, gofmt)
```

**3. Git Diff for Changed Code (Save 70-80%)**
```bash
# ❌ AVOID: Analyzing all project files
Glob "**/*" → Read all → identify ugly code

# ✅ PREFER: Focus on recent changes
git diff HEAD~3 --name-only --diff-filter=AM | head -5
Read only-changed-files
```

**4. Bash-Based Formatter Execution (Save 80-90%)**
```bash
# ❌ AVOID: Manual formatting via Edit tool
Read → Edit line-by-line → Write

# ✅ PREFER: Use existing formatters
# JavaScript/TypeScript
npx prettier --write "src/**/*.{js,ts}"

# Python
black . --line-length 88

# Go
gofmt -w .

# Rust
cargo fmt
```

**5. Progressive Improvements (Save 50-60%)**
```bash
# ❌ AVOID: All improvements at once
Fix naming + structure + types + complexity in one pass

# ✅ PREFER: One aspect at a time
Pass 1: Naming (variables, functions)
Pass 2: Structure (extraction, grouping)
Pass 3: Types (annotations, specificity)
Pass 4: Cleanup (unused code, redundancy)
```

**6. Early Exit When Clean (Save 90%)**
```bash
# ❌ AVOID: Analyzing already-clean code
Read all files → check each → report "already clean"

# ✅ PREFER: Quick validation check
1. Check formatter config exists
2. Run formatter in check mode
3. Exit if no changes needed

# Example
npx prettier --check "src/**/*.ts" && exit 0
```

### Implementation Checklist

**Before Starting:**
- [ ] Ask user for specific file(s) to improve
- [ ] If no file specified, use `git diff --name-only HEAD~3`
- [ ] Limit to 3-5 files per session
- [ ] Check if formatters are configured

**During Execution:**
- [ ] Create git checkpoint: `git stash push -m "pre-prettify"`
- [ ] Use Bash for formatter execution (prettier, black, gofmt)
- [ ] Load cached style patterns from `.claude/cache/make-it-pretty/`
- [ ] Apply one improvement type per pass
- [ ] Run tests after each pass if available

**After Completion:**
- [ ] Cache new style patterns discovered
- [ ] Report improvements made (naming, structure, types)
- [ ] Suggest remaining improvements for future sessions

### Caching Strategy

**Cache Location:** `.claude/cache/make-it-pretty/`

**Cached Data:**
1. **style-guide.json** - Project naming conventions
   - Variable naming patterns (camelCase, snake_case)
   - Function naming patterns
   - File naming patterns
   - Indentation preferences (tabs vs. spaces)

2. **type-patterns.json** - Type annotation standards
   - Common type definitions
   - Generic type usage
   - Type import patterns

3. **formatter-config.json** - Detected formatters
   - Prettier config
   - ESLint config
   - Black config
   - Language-specific formatters

**Cache Invalidation:**
- Clear cache when formatter configs change
- Refresh after major refactoring
- User can force refresh with `--no-cache` flag

### Usage Patterns

**Standard Usage:**
```bash
# Improve specific file
/make-it-pretty src/components/UserProfile.tsx

# Improve recently changed files
/make-it-pretty --recent

# Focus on specific aspect
/make-it-pretty --naming src/utils/helpers.ts
/make-it-pretty --structure src/api/client.ts
/make-it-pretty --types src/models/user.ts

# Dry run (preview changes)
/make-it-pretty --dry src/components/*.tsx
```

**Focus Area Flags:**
- `--naming` - Only improve variable/function names
- `--structure` - Only reorganize code structure
- `--types` - Only improve type annotations
- `--dry` - Preview changes without applying
- `--no-cache` - Force refresh of style patterns

### Expected Token Usage

**Optimized Pattern:**
- File scope identification: 50-100 tokens
- Load cached style patterns: 100-200 tokens
- Bash formatter execution: 100-200 tokens
- Targeted improvements: 500-800 tokens
- Validation & report: 200-300 tokens
- **Total: 1,050-1,575 tokens (65% reduction)**

**Comparison (Previous Unoptimized):**
- Read entire codebase: 1,000-1,500 tokens
- Manual pattern analysis: 800-1,200 tokens
- Line-by-line edits: 600-1,000 tokens
- Comprehensive improvements: 400-600 tokens
- Full testing: 200-300 tokens
- **Total: 3,000-4,500 tokens**

**Token Savings: 1,950-2,925 tokens (65% reduction)**

### Optimization Status

- ✅ **Optimized** (Phase 2 Batch 3D-F, 2026-01-26)
- ✅ Focused scope (user-specified or git diff)
- ✅ Template-based formatting patterns
- ✅ Bash-based formatter execution
- ✅ Progressive improvements
- ✅ Early exit when clean
- ✅ Caching style patterns

## Strategic Thinking Process

<think>
Before making any changes, I need to consider:

1. **Code Analysis**
   - What makes this code "ugly" or hard to read?
   - Are there complex nested structures that need simplification?
   - Is the naming unclear or inconsistent?
   - Are there repeated patterns that could be abstracted?

2. **Safety Considerations**
   - Which changes are purely cosmetic (safe)?
   - Which might affect behavior (risky)?
   - Are there implicit dependencies on current structure?
   - Could renaming break external references?

3. **Improvement Strategy**
   - Priority 1: Clear naming (variables, functions, files)
   - Priority 2: Reduce complexity (extract functions, simplify logic)
   - Priority 3: Remove redundancy (DRY principle)
   - Priority 4: Improve type safety (if applicable)

4. **Validation Approach**
   - How can I ensure functionality remains identical?
   - What tests exist to verify behavior?
   - Should I add temporary logging to verify flow?
</think>

Based on this analysis, I'll proceed safely:

**Safety First:**
- Create git checkpoint before changes
- Use **Write** tool to create backups
- Track all modifications systematically

I'll identify files to beautify based on:
- Files you specify, or if none specified, analyze the entire application
- Recently modified code
- Our conversation context

**Improvements I'll Make:**
- Variable and function names for clarity
- Code organization and structure
- Remove unused code and clutter
- Simplify complex expressions
- Group related functionality
- Fix loose or generic type declarations
- Add missing type annotations where supported
- Make types more specific based on usage

**My Approach:**
1. Analyze current code patterns and type usage
2. Apply consistent naming conventions
3. Improve type safety where applicable
4. Reorganize for better readability
5. Remove redundancy without changing logic

**Quality Assurance:**
- All functionality remains identical
- Tests continue to pass (if available)
- No behavior changes occur
- Clear commit messages for changes

**Important**: I will NEVER:
- Add "Co-authored-by" or any Claude signatures
- Include "Generated with Claude Code" or similar messages
- Modify git config or user credentials
- Add any AI/assistant attribution to the commit

This helps transform working code into maintainable code without risk.