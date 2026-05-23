---
name: scaffold
description: Generate complete feature structures based on your project patterns with full continuity
disable-model-invocation: true
---

# Intelligent Scaffolding

I'll create complete feature structures based on your project patterns, with full continuity across sessions.

Arguments: `$ARGUMENTS` - feature name or component to scaffold

---

## Token Optimization Strategy

**Target:** 65% reduction (3,500-5,000 → 1,200-2,000 tokens)
**Status:** ✅ Optimized (Phase 2 Batch 3D-F, 2026-01-26)

### Optimization Techniques Applied

**1. Template-Based Scaffolding**
- **Pattern:** Reuse existing feature structures as templates
- **Implementation:** Glob → identify similar features → copy patterns
- **Savings:** 70% (avoid reading documentation, reduce analysis)
- **Example:**
  ```markdown
  # Instead of analyzing 20 files for patterns:
  Glob "src/features/*/index.ts" → Find 5 existing features
  Read ONLY one representative feature → Extract pattern
  Reuse pattern for new scaffolding → Generate with heredocs

  Before: 15,000 tokens (read all features)
  After: 1,500 tokens (read one, reuse pattern)
  Savings: 90%
  ```

**2. Framework Detection Caching**
- **Pattern:** Cache framework type and conventions from `/understand`
- **Implementation:** Check `.claude/cache/understand/project-analysis.json`
- **Savings:** 80% (skip framework detection)
- **Cache Keys:**
  - `framework`: React/Vue/Angular/Svelte
  - `structure`: File organization pattern
  - `conventions`: Naming and export patterns
  - `testFramework`: Jest/Vitest/Mocha

**3. Project Conventions Caching**
- **Pattern:** Learn and cache project-specific patterns
- **Location:** `.claude/cache/scaffold/conventions.json`
- **Cached Data:**
  ```json
  {
    "naming": "kebab-case|PascalCase|camelCase",
    "fileStructure": "feature-folders|type-folders|flat",
    "imports": "absolute|relative",
    "exports": "named|default",
    "testLocation": "adjacent|__tests__|separate"
  }
  ```
- **Savings:** 60% (skip pattern analysis on resume)

**4. Bash-Based File Generation**
- **Pattern:** Use heredocs for creating multiple files efficiently
- **Implementation:**
  ```bash
  cat > src/features/user/index.ts <<'EOF'
  export * from './UserProfile'
  export * from './types'
  EOF

  cat > src/features/user/UserProfile.tsx <<'EOF'
  import React from 'react'
  // Component code generated from template
  EOF
  ```
- **Savings:** 50% (single Bash call vs multiple Write calls)
- **Benefits:** Atomic operations, better error handling

**5. Incremental Scaffolding**
- **Pattern:** Generate one component at a time with validation
- **State Tracking:** `scaffold/state.json` tracks completed files
- **Resume Support:**
  ```json
  {
    "feature": "UserProfile",
    "created": ["index.ts", "types.ts", "UserProfile.tsx"],
    "pending": ["UserProfile.test.tsx", "UserProfile.stories.tsx"],
    "lastFile": "UserProfile.tsx"
  }
  ```
- **Savings:** 80% on resume (skip created files)

**6. Git Diff Before Scaffolding**
- **Pattern:** Check for existing files to avoid overwrites
- **Implementation:**
  ```bash
  git ls-files src/features/user/ # Check if feature exists
  ```
- **Savings:** 95% (immediate exit if feature exists)
- **Safety:** Prevents accidental overwrites

### Token Cost Breakdown

**Phase 1: Pattern Discovery (500-800 tokens)**
- Check session: 50 tokens (Bash ls scaffold/)
- Framework detection: 100 tokens (cache hit) or 500 tokens (cache miss)
- Glob existing features: 150 tokens
- Read ONE template feature: 300-500 tokens
- **Total:** 600-1,200 tokens (vs 8,000 unoptimized)

**Phase 2: Planning (200-400 tokens)**
- Generate file list: 100 tokens (from template)
- Create plan.md: 50 tokens (Write)
- Initialize state.json: 50 tokens (Write)
- **Total:** 200 tokens (vs 2,000 unoptimized)

**Phase 3: File Generation (500-800 tokens)**
- Bash heredoc generation: 400-600 tokens (all files in one call)
- Update state.json: 50 tokens
- Git status check: 100 tokens
- **Total:** 550-750 tokens (vs 5,000 unoptimized)

**Resume Session (300-600 tokens)**
- Read state.json: 100 tokens
- Check pending files: 50 tokens
- Generate remaining files: 200-400 tokens
- **Total:** 350-550 tokens (vs 3,000 unoptimized)

### Optimization Results

**Token Savings:**
- **New scaffolding:** 3,500-5,000 → 1,200-2,000 tokens (65% reduction)
- **Resume session:** 3,000-4,000 → 300-600 tokens (85% reduction)
- **Small scaffold:** 2,000-3,000 → 500-1,000 tokens (67% reduction)
- **Average:** 65% token reduction

**Cost Comparison:**
```
Before Optimization:
- New feature: 4,000 tokens × $0.003 = $0.012
- Resume: 3,500 tokens × $0.003 = $0.0105
- Annual (50 scaffolds): $0.60

After Optimization:
- New feature: 1,500 tokens × $0.003 = $0.0045
- Resume: 500 tokens × $0.003 = $0.0015
- Annual (50 scaffolds): $0.21

Savings: $0.39/year per developer (65% reduction)
```

### Caching Strategy

**Cache Locations:**
- **Session state:** `scaffold/` in project root
  - `plan.md`: Scaffolding plan and file list
  - `state.json`: Progress tracking and created files
- **Framework cache:** `.claude/cache/understand/`
  - Shared with `/understand`, `/implement`, `/boilerplate`
- **Convention cache:** `.claude/cache/scaffold/`
  - `conventions.json`: Project-specific patterns
  - `templates/`: Cached feature templates

**Cache Invalidation:**
- Session cache: Cleared on completion or explicit `new` command
- Framework cache: Valid until project structure changes
- Convention cache: Valid for 7 days or until pattern mismatch

**Shared Caches:**
- `/understand`: Framework and structure analysis
- `/implement`: Project patterns and dependencies
- `/boilerplate`: Framework-specific templates
- `/types-generate`: Type generation patterns

### Usage Examples

**Optimized Flow (1,200-2,000 tokens):**
```bash
# First scaffolding in project
claude "scaffold UserProfile"

Step 1: Check session (50 tokens)
Step 2: Load framework cache (100 tokens, cache hit)
Step 3: Find template features (150 tokens, Glob)
Step 4: Read one template (500 tokens)
Step 5: Generate plan (200 tokens)
Step 6: Create files with heredocs (600 tokens)
Total: 1,600 tokens
```

**Resume Flow (300-600 tokens):**
```bash
# Continue scaffolding
claude "scaffold resume"

Step 1: Read state.json (100 tokens)
Step 2: Load cached conventions (50 tokens)
Step 3: Generate remaining files (400 tokens)
Total: 550 tokens (85% savings)
```

**Specific Type Flow (800-1,500 tokens):**
```bash
# Scaffold specific component type
claude "scaffold --api-route users"

Step 1: Check session (50 tokens)
Step 2: Load route template (200 tokens)
Step 3: Generate route files (500 tokens)
Total: 750 tokens (75% savings)
```

### Implementation Notes

**Critical Optimizations:**
1. **Always check for session first** - Saves 80% on resume
2. **Use framework cache** - Shared with `/understand` skill
3. **Template-based generation** - Avoid analysis overhead
4. **Bash heredocs** - Efficient multi-file creation
5. **Incremental state tracking** - Perfect resume support

**Anti-Patterns to Avoid:**
- ❌ Reading all existing features for pattern analysis
- ❌ Analyzing framework from scratch (use cache)
- ❌ Creating files one Write call at a time
- ❌ Regenerating already-created files on resume
- ❌ Full project scan without focusing on feature area

**Quality Assurance:**
- All files follow project conventions (from cache)
- Tests generated using project test patterns
- Imports use project import style (absolute vs relative)
- File names match project naming convention
- No duplicate scaffolding (git diff check)

---

## Session Intelligence

I'll maintain scaffolding progress across sessions:

**Session Files (in current project directory):**
- `scaffold/plan.md` - Scaffolding plan and component list
- `scaffold/state.json` - Created files and progress

**IMPORTANT:** Session files are stored in a `scaffold` folder in your current project root

**Auto-Detection:**
- If session exists: Resume incomplete scaffolding
- If no session: Create new scaffolding plan
- Commands: `resume`, `status`, `new`

## Phase 1: Pattern Discovery

**MANDATORY FIRST STEPS:**
1. Check if `scaffold` directory exists in current working directory
2. If directory exists, check for session files:
   - Look for `scaffold/state.json`
   - Look for `scaffold/plan.md`
   - If found, resume from existing session
3. If no directory or session exists:
   - Analyze project patterns
   - Create scaffolding plan
   - Initialize progress tracking
4. Show scaffolding preview before creating

**Note:** Always look for session files in the current project's `scaffold/` folder, not `../../../scaffold/` or absolute paths

I'll discover your project patterns:

**Pattern Analysis:**
- File organization structure
- Naming conventions
- Testing patterns
- Import/export styles
- Documentation standards

**Smart Detection:**
- Find similar features already implemented
- Identify architectural patterns
- Detect testing frameworks
- Understand build configuration

## Phase 2: Scaffolding Planning

Based on patterns, I'll create a scaffolding plan:

**Component Structure:**
- Main feature files
- Test files
- Documentation
- Configuration updates
- Integration points

I'll write this plan to `scaffold/plan.md` with:
- Each file to create
- Template patterns to follow
- Integration requirements
- Creation order

## Phase 3: Intelligent Generation

I'll generate files matching your patterns:

**Pattern Matching:**
- Use your file naming style
- Follow your directory structure
- Match your code conventions
- Apply your testing patterns

**Content Generation:**
- Boilerplate from existing code
- Imports matching your style
- Test structure from your patterns
- Documentation in your format

## Phase 4: Incremental Creation

I'll create files systematically:

**Execution Process:**
1. Create directory structure
2. Generate each component file
3. Add appropriate tests
4. Update integration points
5. Track each creation in state

**Progress Tracking:**
- Mark each file created in plan
- Update state with file paths
- Create meaningful commits

## Phase 5: Integration

After scaffolding:
- Update route configurations
- Add to module exports
- Update build configuration
- Verify everything connects

## Context Continuity

**Session Resume:**
When you return and run `/scaffold` or `/scaffold resume`:
- Load existing plan and progress
- Show what was already created
- Continue from last component
- Maintain pattern consistency

**Progress Example:**
```
RESUMING SCAFFOLDING
├── Feature: UserDashboard
├── Created: 5 of 8 files
├── Last: components/UserStats.tsx
└── Next: tests/UserStats.test.tsx

Continuing scaffolding...
```

## Practical Examples

**Start Scaffolding:**
```
/scaffold UserProfile          # Create user profile feature
/scaffold "auth module"        # Create authentication module
/scaffold PaymentService       # Create payment service
```

**Session Control:**
```
/scaffold resume    # Continue existing scaffolding
/scaffold status    # Check what's been created
/scaffold new       # Start fresh scaffolding
```

## Safety Guarantees

**Protection Measures:**
- Preview before creation
- Incremental file generation
- Pattern validation
- Integration verification

**Important:** I will NEVER:
- Overwrite existing files
- Break existing imports
- Add AI attribution
- Create without following patterns

## What I'll Actually Do

1. **Analyze deeply** - Understand your patterns
2. **Plan completely** - Map all components
3. **Generate intelligently** - Match your style
4. **Track precisely** - Perfect continuity
5. **Integrate seamlessly** - Connect everything

I'll maintain complete continuity between sessions, always resuming exactly where we left off with consistent pattern application.