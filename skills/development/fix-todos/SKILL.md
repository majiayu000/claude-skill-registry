---
name: fix-todos
description: Intelligent TODO resolution with context-aware implementation
disable-model-invocation: false
---

# Fix TODOs

I'll systematically find and resolve TODO comments in your codebase with intelligent understanding and continuity across sessions.

Arguments: `$ARGUMENTS` - files, directories, or specific TODO patterns to fix

## Token Optimization Strategy

**Target: 60% reduction (3,000-5,000 → 1,200-2,000 tokens)**

This skill implements aggressive optimization for TODO resolution workflows by minimizing file reads, leveraging session state, and using progressive fixing patterns.

### Core Optimization Patterns

**1. Grep-First TODO Discovery (Primary: 60-70% savings)**
```bash
# ALWAYS use Grep to find TODOs - never Read files for scanning
grep -rn "TODO|FIXME|HACK|XXX" --include="*.{js,ts,py,go}" .
grep "TODO:" src/ -C 2  # Get 2 lines context for understanding

# ANTI-PATTERN: Reading files to find TODOs
# Read each .js file  # ❌ NEVER do this
```

**2. Session-Based State Tracking (80% savings on resume)**
```
fix-todos/
├── plan.md           # All TODOs with resolution status
├── state.json        # Current progress, decisions, context
└── resolutions/      # Completed TODO resolutions for reference
```

**Session state prevents re-scanning and re-analyzing:
- Check for `fix-todos/` directory FIRST
- If state.json exists, resume from last TODO
- Only scan for new TODOs if explicitly requested
- Use cached TODO inventory and context

**3. Git Diff for Changed Files with TODOs (70% savings)**
```bash
# Find files with TODOs that changed recently
git diff --name-only HEAD~5 | xargs grep -l "TODO"

# Focus on changed files vs full codebase scan
git diff --name-only | grep -f todo-files.txt
```

**4. Progressive TODO Resolution (one at a time)**
- Fix ONE TODO per iteration
- Update state after each fix
- Commit incrementally
- User can continue/stop at any point
- Reduces context loading by 70%

**5. Early Exit Patterns**
```bash
# Check for session FIRST
ls fix-todos/state.json 2>/dev/null && echo "Session exists"

# Check for TODOs before scanning
grep -q "TODO" . || echo "No TODOs found"

# Skip fixed TODOs from state
grep "^FIXED:" fix-todos/plan.md | wc -l
```

### Optimization Decision Tree

```
START
├── Session exists? (check fix-todos/state.json)
│   ├── YES → Load state (200 tokens)
│   │   ├── Show progress summary
│   │   ├── Resume from last TODO
│   │   └── Fix next TODO (400-800 tokens)
│   └── NO → New session
│       ├── Grep for TODOs (400 tokens)
│       ├── No TODOs? → Early exit (300 tokens)
│       └── Create plan → Fix first TODO (1,200-1,500 tokens)
└── Specific file/pattern?
    ├── Grep in scope only (300 tokens)
    └── Fix matching TODOs (800-1,200 tokens)
```

### Token Cost Breakdown

**Initial Session (1,200-2,000 tokens):**
- Check for session: 100 tokens
- Grep for TODOs: 300-400 tokens
- Categorize TODOs: 200-300 tokens
- Create plan: 200-400 tokens
- Fix first TODO: 400-900 tokens (Read file, Edit, verify)

**Resume Session (400-800 tokens):**
- Load state: 100-200 tokens
- Show progress: 100 tokens
- Read file with next TODO: 200-300 tokens
- Fix TODO: 200-300 tokens

**Specific File Focus (800-1,200 tokens):**
- Grep in file: 100-200 tokens
- Read file: 300-400 tokens
- Fix TODOs: 400-600 tokens

### Template-Based Resolution Patterns

**Cache common TODO resolution templates:**
```typescript
// Error handling template
TODO_TEMPLATES = {
  error_handling: "try { /* existing */ } catch (err) { logger.error(err); throw err; }",
  validation: "if (!input) throw new ValidationError('Required');",
  null_check: "if (value === null) return defaultValue;",
  logging: "logger.debug('Operation:', { context });",
  type_guard: "if (typeof x !== 'expected') throw new TypeError();"
}

// Use templates instead of analyzing patterns every time
```

### Caching Strategy

**Session Location:** `fix-todos/` (current project directory)
- `plan.md` - TODO inventory with status
- `state.json` - Progress, decisions, current TODO
- `resolutions/` - Completed fixes for pattern matching

**Cache Location:** `.claude/cache/fix-todos/`
- `todo-inventory.json` - All TODOs found
- `resolution-patterns.json` - Your code patterns
- `context-snippets/` - Related code for each TODO

**Cache Validity:** Until session completed or user runs `fix-todos new`

**Cache Sharing:** `/find-todos`, `/create-todos`, `/todos-to-issues` can reuse TODO inventory

### Practical Token Savings Examples

**Example 1: Resume existing session**
```
BEFORE optimization (3,500 tokens):
- Re-scan all files for TODOs: 1,200 tokens
- Re-categorize: 400 tokens
- Re-create plan: 500 tokens
- Find next TODO: 300 tokens
- Fix TODO: 1,100 tokens

AFTER optimization (500 tokens):
- Load state: 100 tokens
- Read next TODO file: 200 tokens
- Fix TODO: 200 tokens
Savings: 3,000 tokens (86%)
```

**Example 2: Fix TODOs in specific file**
```
BEFORE optimization (4,000 tokens):
- Read all project files: 2,000 tokens
- Find TODOs everywhere: 800 tokens
- Filter to target file: 200 tokens
- Fix TODOs: 1,000 tokens

AFTER optimization (1,000 tokens):
- Grep in specific file: 200 tokens
- Read file: 300 tokens
- Fix TODOs: 500 tokens
Savings: 3,000 tokens (75%)
```

**Example 3: New session with no TODOs**
```
BEFORE optimization (2,000 tokens):
- Read many files looking for TODOs: 1,800 tokens
- Report none found: 200 tokens

AFTER optimization (300 tokens):
- Grep entire codebase: 200 tokens
- Report none found (early exit): 100 tokens
Savings: 1,700 tokens (85%)
```

### Usage Patterns by Token Cost

**High-efficiency commands (400-800 tokens):**
- `fix-todos resume` - Continue existing session
- `fix-todos src/api/auth.js` - Specific file
- `fix-todos status` - Check progress only

**Medium-efficiency commands (1,200-1,500 tokens):**
- `fix-todos` - New session (first time)
- `fix-todos src/` - Directory scope
- `fix-todos "security"` - Pattern filter

**Avoid if possible (2,000+ tokens):**
- `fix-todos new` when session already exists
- Re-scanning without using cached results
- Fixing all TODOs at once (use progressive mode)

### Optimization Checklist

**Before TODO Discovery:**
- ✅ Check for `fix-todos/state.json` FIRST
- ✅ Load cached TODO inventory if available
- ✅ Use Grep (not Read) for TODO scanning
- ✅ Apply scope filters early (file/pattern)
- ✅ Early exit if no TODOs found

**During TODO Resolution:**
- ✅ Fix ONE TODO at a time (progressive mode)
- ✅ Use git diff to find changed files
- ✅ Apply resolution templates when possible
- ✅ Update state after each fix
- ✅ Commit incrementally

**After TODO Resolution:**
- ✅ Cache resolution patterns for future use
- ✅ Update plan.md with completion status
- ✅ Persist state for next session
- ✅ Clean up session when all TODOs fixed

### Anti-Patterns to Avoid

❌ Reading all files to find TODOs → Use Grep
❌ Re-scanning on every resume → Use session state
❌ Fixing all TODOs in one iteration → Progressive mode
❌ Not checking for existing session → Load state first
❌ Not using cached patterns → Apply templates
❌ Full codebase analysis per TODO → Incremental context

### Expected Performance

**Token Usage:**
- Initial session: 1,200-2,000 tokens
- Resume session: 400-800 tokens
- Specific file: 800-1,200 tokens
- **Average: 1,200 tokens** (vs 3,000-5,000 unoptimized)

**Reduction: 60-75%** (exceeds 60% target)

**Optimization Status:** ✅ Optimized (Phase 2 Batch 3D-F, 2026-01-26)

## Session Intelligence

I'll maintain TODO resolution progress across sessions:

**Session Files (in current project directory):**
- `fix-todos/plan.md` - All TODOs found and resolution status
- `fix-todos/state.json` - Current progress and decisions

**IMPORTANT:** Session files are stored in a `fix-todos` folder in your current project directory

**Auto-Detection:**
- If session exists: Resume from last TODO
- If no session: Scan and create new plan
- Commands: `resume`, `status`, `new`

## Phase 1: Discovery & Analysis

**MANDATORY FIRST STEPS:**
1. Check if `fix-todos` directory exists in current working directory
2. If directory exists, check for session files:
   - Look for `fix-todos/state.json`
   - Look for `fix-todos/plan.md`
   - If found, resume from existing session
3. If no directory or session exists:
   - Scan entire codebase for TODOs
   - Create categorized plan
   - Initialize progress tracking
4. Show TODO summary before starting

I'll find and categorize all TODOs:

**TODO Detection:**
- TODO, FIXME, HACK, XXX markers
- Different priority levels
- Context and complexity assessment
- Related code understanding

**Smart Categorization:**
- **Quick fixes**: Simple validations, null checks
- **Features**: Missing functionality
- **Refactoring**: Code improvements
- **Security**: Safety and validation needs
- **Performance**: Optimization opportunities

## Phase 2: Resolution Planning

Based on analysis, I'll create a resolution plan:

**Priority Order:**
1. Security-critical TODOs
2. Bug-related TODOs
3. Simple improvements
4. Feature additions
5. Performance optimizations

I'll write this plan to `fix-todos/plan.md` with:
- Each TODO location and content
- Proposed resolution approach
- Risk assessment
- Implementation order

## Phase 3: Intelligent Resolution

I'll fix TODOs matching your code patterns:

**Pattern Detection:**
- Find similar implementations in your code
- Match your error handling style
- Use your validation patterns
- Follow your naming conventions

**Resolution Strategies:**
- Error handling → Your try/catch patterns
- Validation → Your input checking style
- Performance → Your optimization approach
- Security → Your safety patterns

## Phase 4: Incremental Implementation

I'll resolve TODOs systematically:

**Execution Process:**
1. Create git checkpoint
2. Fix TODO with contextual understanding
3. Verify functionality preserved
4. Update plan with completion
5. Move to next TODO

**Progress Tracking:**
- Mark each TODO as resolved in plan
- Update state file with decisions
- Create meaningful commits

## Phase 5: Verification

After each resolution:
- Run relevant tests
- Check for regressions
- Validate integration points
- Ensure code quality

## Context Continuity

**Session Resume:**
When you return and run `/fix-todos` or `/fix-todos resume`:
- Load existing plan and progress
- Show completion statistics
- Continue from last TODO
- Maintain all resolution decisions

**Progress Example:**
```
RESUMING TODO FIXES
├── Total TODOs: 47
├── Resolved: 23 (49%)
├── Current: src/api/auth.js:42
└── Next: src/utils/validation.js:15

Continuing resolution...
```

## Practical Examples

**Start Fixing:**
```
/fix-todos                    # Fix all TODOs
/fix-todos src/              # Focus on directory
/fix-todos "security"        # Fix security TODOs
```

**Session Control:**
```
/fix-todos resume    # Continue existing session
/fix-todos status    # Check progress
/fix-todos new       # Start fresh
```

## Safety Guarantees

**Protection Measures:**
- Git checkpoint before changes
- Incremental commits
- Functionality verification
- No TODO removal without implementation

**Important:** I will NEVER:
- Remove TODOs without fixing them
- Break existing functionality
- Add AI attribution
- Implement without understanding context

## Command Suggestions

After resolving critical TODOs:
- `/test` - To ensure fixes work correctly
- `/commit` - To save TODO resolutions

## What I'll Actually Do

1. **Scan comprehensively** - Find all TODOs with context
2. **Plan strategically** - Order by priority and risk
3. **Resolve intelligently** - Match your patterns
4. **Track meticulously** - Perfect session continuity
5. **Verify constantly** - Ensure quality maintained

I'll maintain complete continuity between sessions, always resuming exactly where we left off with full context of previous resolutions.