---
name: Quick Start to Code
description: Prepare development environment for immediate coding by orchestrating memory loading, context validation, and pre-flight checks all in one interaction. Eliminates the need for multiple manual slash commands (/memory-read, /standards-check, /arch-check) before starting work. Use when the user says "ready to code", "start coding", "let's implement", "begin development", "coding time", or needs to transition from planning directly to implementation without manual warm-up.
allowed-tools: Read, Glob, Bash
---

# Quick Start to Code

## Purpose

This Skill solves the **"multiple slash commands before coding" problem**. Instead of:

```
/memory-read  ← Load 7 memory files
<wait, read output>
/standards-check  ← Check code standards
<wait, read output>
/arch-check  ← Check architecture
<wait, read output>
Ready to code...
```

You simply say: **"Ready to code"** and this Skill automatically:
1. ✅ Loads all 7 memory files + constitution
2. ✅ Validates pipeline phase (should be IMPLEMENTATION)
3. ✅ Checks code standards compliance
4. ✅ Verifies architectural constraints
5. ✅ Presents next task and dependencies
6. ✅ Confirms readiness status

---

## When to Use This Skill

**User Initiates** (explicit triggers):
- "Ready to code"
- "Start coding"
- "Let's implement"
- "Begin development"
- "Coding time"
- "I want to start working"
- "Start task execution"

**Contextual Triggers**:
- After completing `/plan` command (planning done, implementation ready)
- When asking "am I ready to code?" with uncertainty
- After context-navigator shows "Ready for implementation"
- When switching from planning to implementation mode

**Multi-Feature Scenario**:
- Multiple features in different phases
- Quick-start validates you're in the right feature
- Prevents starting coding on wrong feature

---

## How It Works

### Phase 1: Load Full Development Context (Native Caching Enabled)

**Performance Optimization**: Leverage Claude 4.5's 200K context window with native prompt caching:

```
SYSTEM PROMPT (with native caching):
<cache_control type="ephemeral">

Load ALL memory files at once (no chunking needed):
- 7 core memory files (~19.5K tokens total)
- Constitution (~2K tokens)
- Specifications (~3K tokens)

Total: ~25K tokens (12.5% of 200K context)

Cache benefits:
- First load: 1.25x cost (write to cache)
- Subsequent loads: 0.1x cost (90% savings)
- Auto-refresh on use (extends TTL)
- Auto-invalidate on file changes

</cache_control>
```

**Load These Files:**

1. **Memory Core** (project root `/memory/`) - **Loaded in Parallel**:
   - `active_context.md` - Current feature, phase, last activity
   - `tasks_plan.md` - Full task breakdown, completion, priorities
   - `architecture.md` - System design, component boundaries
   - `technical.md` - Tech standards, code quality rules
   - `product_requirement_docs.md` - Feature scope, requirements
   - `error-documentation.md` - Known issues, workarounds
   - `lessons-learned.md` - Previous insights, patterns

2. **Authoritative Source** (.specify/):
   - `constitution.md` - Project principles, quality gates (7 gates)

3. **Runtime Guidance**:
   - `CLAUDE.md` - Project-specific development guidance

**Output**: Summary of loaded context:
```
✅ Context Loaded in 69ms (parallel):
   - Product requirements (12 KB)
   - Architecture design (25 KB)
   - Technical standards (22 KB)
   - Constitution & principles (30 KB)
   - Current feature details (5 KB)
   - Task breakdown (14 KB)
   - Error documentation (18 KB)
   - Lessons learned (21 KB)

   Total: 147 KB loaded in parallel (2.5x faster)
```

### Phase 2: Validate Pipeline State

**Check Prerequisites for Implementation Phase:**

**Phase Validation:**
```
Current Phase Detection:
├─ If spec.md missing → Phase 0, need /specify
├─ If plan.md missing → Phase 1, need /plan
├─ If tasks.md missing → Phase 2, need /tasks
├─ If tasks incomplete → Phase 3, READY ✓
└─ If tests passing → Phase 4, need validation
```

**Output**:
```
✅ PHASE VALIDATION: Phase 3 - IMPLEMENTATION (Ready)
   ✓ Specification: Complete (specs/006-feature-006-logging/spec.md)
   ✓ Planning: Complete (plan.md synced to architecture.md)
   ✓ Tasks: Complete (26 tasks in tasks_plan.md)
   ✓ Prerequisites: All met
```

**Stop Condition**: If phase is wrong, guide user:
```
⚠️  PHASE MISMATCH: Not ready for implementation

Current Phase: 1 - SPECIFICATION
Next Step: Complete planning phase first
  Run: /plan

Or to proceed anyway:
  Say: "Skip validation" (not recommended)
```

### Phase 2.5: Constitutional Validation (NEW v2.0.0)

**Check Constitution and Quality Gates:**

**Constitution Loading:**
```bash
# Check for constitution
if [ -f .specify/memory/constitution.md ]; then
  # Parse principles
  principles=$(grep -c "^## Principle" .specify/memory/constitution.md)

  # Check quality gates status
  load_principle_registry()  # from .claude/cache/principle-registry.json

  # Identify blocking gates for implementation phase
  blocking_gates=$(jq '.[] | select(.triggers[] == "pre-implementation")' .claude/cache/principle-registry.json)
fi
```

**Output (if constitution exists)**:
```
⚖️  CONSTITUTIONAL PRE-FLIGHT CHECK
   Constitution: Found ([N] principles)
   Quality Gates: Checking implementation prerequisites...

   Gate 2 - Testability Gate:
   ✓ Test framework configured
   ✓ Test structure exists
   ✓ TDD approach documented in tasks

   Gate 3 - Boundary Gate:
   ✓ Architecture boundaries defined
   ✓ Component interfaces specified
   ✓ No circular dependencies detected

   Overall: [N]/[M] gates passed
   Status: ✅ READY FOR IMPLEMENTATION
```

**Output (if constitution missing)**:
```
⚖️  CONSTITUTIONAL CHECK
   Constitution: Not ratified (optional)
   Quality Gates: Skipped (v1.0.0 compatibility mode)
   Status: ✅ Ready (without constitutional governance)
```

**Blocker Detection**:
```
❌ CONSTITUTIONAL BLOCKER DETECTED

Gate 2 - Testability Gate: FAILED
Issue: Test framework not configured
Required Actions:
  1. Install test framework (pytest/jest)
  2. Create test directory structure
  3. Add test configuration files

Cannot proceed with implementation until resolved.
Recommendation: Run /standards-check for detailed diagnostics
```

### Phase 3: Verify Git State

**Check Git Configuration:**

```bash
# Verify branch matches feature
git branch --show-current
# Expected: 006-feature-006-logging or similar

# Check working tree
git status --porcelain
# Should be: Clean (or acceptable changes)

# Get recent context
git log -1 --format="%h %s"
# Expected: Recent commit from same feature
```

**Output**:
```
✅ GIT STATE VALIDATION
   ✓ Branch: 006-feature-006-logging (matches active feature)
   ✓ Working tree: Clean (no uncommitted changes)
   ✓ Recent commit: 217b377 "feat: implement Phase 5 E2E testing"
   ✓ Status: Ready to code
```

### Phase 3.5: Plugin Loading and Validation (NEW v2.0.0)

**Discover and Load Project Plugins:**

**Plugin Discovery:**
```bash
# Scan for plugin manifests
plugin_dirs=(
  ".claude/commands/plugins"
  ".claude/validators/plugins"
)

for dir in "${plugin_dirs[@]}"; do
  if [ -d "$dir" ]; then
    find "$dir" -name "plugin.json" -type f | while read manifest; do
      # Validate manifest schema
      # Load plugin metadata
      # Register commands/validators
    done
  fi
done
```

**Output (if plugins found)**:
```
🔌 PLUGIN LOADING
   Discovered: [N] plugin packs

   Loading: project-specific-commands v1.2.3
   ✓ Registered 6 commands
   ✓ No conflicts detected

   Loading: project-specific-validators v1.1.0
   ✓ Registered 4 validators
   ✓ All dependencies satisfied

   Summary:
   ├─ Commands available: 8 core + 6 plugin = 14 total
   ├─ Validators active: 3 core + 4 plugin = 7 total
   └─ Plugin performance: <50ms load time ✓

   Status: ✅ PLUGINS LOADED
```

**Output (if no plugins)**:
```
🔌 PLUGIN STATUS
   Status: Core-only mode (no project plugins)
   Commands available: 8 core commands
   Validators active: 3 core validators

   To add project-specific capabilities:
   Run: /plugin-install [plugin-pack-name]
```

**Warm-Up Validators (NEW v2.0.0)**:
```
🔥 WARMING VALIDATORS
   Pre-loading validators for faster execution...

   Core validators:
   ✓ memory-consistency (cached)
   ✓ architectural-boundaries (cached)
   ✓ technical-standards (cached)

   Project validators:
   ✓ [project-validator-1] (cached)
   ✓ [project-validator-2] (cached)

   Cache warm-up: Complete (<100ms)
   Next validation: ~5x faster
```

### Phase 4: Standards Compliance Pre-Flight

**Check Code Quality Baseline:**

**Without running full /standards-check** (too slow), validate:
1. Project-appropriate configs exist (detected from tech stack)
2. Test framework ready: `tests/` directory with test files
3. No obvious syntax errors in recent changes
4. Linter/formatter configs present

**Output (generic, adapts to detected stack)**:
```
✅ CODE STANDARDS PRE-FLIGHT
   Tech Stack: [Detected stack - Python/Node/Rust/etc]
   ✓ Linter configured ([linter-name])
   ✓ Formatter configured ([formatter-name])
   ✓ Test framework ready ([test-framework])
   ✓ No blocking syntax errors detected

   Full check: Run /standards-check after changes
```

### Phase 5: Architecture Compliance Check

**Verify No Boundary Violations:**

Quick check that codebase structure matches constitution:

```
✓ Service layer architecture: Controllers thin, Services have business logic
✓ Dependency injection: Services use interfaces
✓ Test structure: tests/Unit/, tests/Feature/ exist
✓ No circular dependencies: (quick static check)
✓ API routes authenticated: auth:sanctum applied
```

**Output**:
```
✅ ARCHITECTURE COMPLIANCE
   ✓ Service layer separation enforced
   ✓ Dependency injection configured
   ✓ Test directory structure correct
   ✓ API authentication configured
   ✓ Constitution gates validated (7/7)

   Full check: Run /arch-check for comprehensive validation
```

### Phase 6: Present Task Breakdown

**Extract from tasks_plan.md:**

```
🎯 TASK BREAKDOWN:

Total: 26 tasks across 8 phases (A-H)
Estimated Total: 6.5 hours

Phase A: Foundation (Database & Config) - 3 tasks, 30 min
├─ [P] T001: Create migration (10 min) ← NEXT
├─ [P] T002: Create model with factory (10 min)
└─ [P] T003: Create config section (10 min)

Phase B: Service Layer - 4 tasks, 90 min
├─ [P] T004: Create interface (5 min)
├─ [ ] T005: Unit tests - TDD (30 min)
├─ [ ] T006: Implement service (45 min)
└─ [ ] T007: Bind in provider (10 min)

[Additional phases...]

Next Immediate Actions:
1. Start with Phase A, Task 1 (Create migration)
2. Tasks T001, T002, T003 are parallel [P] - can run together
3. Estimated time: 30 minutes for Phase A
```

### Phase 7: Readiness Confirmation (Enhanced v2.0.0)

**Final Status Check:**

```
════════════════════════════════════════════════════════════════
✅ READY TO CODE (v2.0.0)
════════════════════════════════════════════════════════════════

📋 Context Loaded:
   ✓ Product requirements
   ✓ Architecture design
   ✓ Technical standards
   ✓ Constitution ([N] principles) [if exists]
   ✓ Feature specification
   ✓ Task breakdown
   ✓ Error documentation
   ✓ Lessons learned

✅ Validations Passed:
   ✓ Phase: IMPLEMENTATION (correct)
   ✓ Branch: [branch-name] (matches)
   ✓ Working tree: Clean
   ✓ Standards configured
   ✓ Architecture compliant
   ✓ Constitutional gates: [N]/[M] passed [if constitution exists]
   ✓ Plugins loaded: [N] packs [if plugins exist]
   ✓ Validators warmed: [N] ready

🔌 Development Environment:
   Commands: [X] core + [Y] plugin = [Z] total
   Validators: [A] core + [B] plugin = [C] total
   Cache: Warmed (~5x faster validation)

🎯 Next Task:
   [Task ID]: [Task description]
   Estimated Time: [N] minutes
   Can parallelize: [Yes/No]
   Priority: [Priority level]
   Dependencies: [Dependencies or "None"]

💡 READY TO START
   Option 1: Say "@agent-implementer" to begin task execution
   Option 2: Say "start [task-id]" to focus on specific task
   Option 3: Run command: /plugin-list to see available commands

⚠️  BLOCKERS (if any):
   [List any blockers preventing implementation]

════════════════════════════════════════════════════════════════
```

**Blocker Example**:
```
════════════════════════════════════════════════════════════════
❌ BLOCKED - NOT READY TO CODE
════════════════════════════════════════════════════════════════

📋 Context Loaded: ✓
✅ Phase Validation: ✓
✅ Git State: ✓
⚖️  Constitutional Check: ❌ FAILED

Blocking Issue:
   Gate 3 - Boundary Gate: FAILED
   ├─ Architectural boundaries not defined
   ├─ Component interfaces missing
   └─ Circular dependencies detected

Required Actions:
   1. Run: /arch-check for detailed analysis
   2. Fix architectural violations
   3. Update architecture.md with boundaries
   4. Re-run: "ready to code" to validate

Cannot proceed until constitutional gate passes.

════════════════════════════════════════════════════════════════
```

---

## Time Comparison

### Before (Without This Skill)

```
Step 1: /memory-read
   - Wait for response
   - Read 7 sections of output
   - Time: 30-45 seconds

Step 2: /standards-check
   - Wait for PHPStan analysis
   - Check ESLint results
   - Time: 45-60 seconds

Step 3: /arch-check
   - Validate architecture boundaries
   - Check compliance gates
   - Time: 30-45 seconds

Step 4: Check tasks_plan.md manually
   - Open and read file
   - Identify next task
   - Time: 30-60 seconds

Step 5: Finally ready to start
   - Total elapsed: 2.5-3.5 minutes ⚠️
   - Cognitive load: High (remember 4+ command outputs)
```

### After (With This Skill)

```
User: "Ready to code"
   ↓
Skill auto-activates
   ↓
Loads all context + validates everything
   ↓
Presents ready status with next task
   ↓
Total elapsed: <15 seconds ✅
Cognitive load: Low (single dashboard)
```

**Time Saved Per Session**: ~2.5 minutes
**Time Saved Per Day** (5 coding sessions): ~12.5 minutes
**Time Saved Per Month** (22 work days): ~5.5 hours

---

## Examples

### Example 1: Ready to Start Implementation

**User Input**: "Ready to code"

**Skill Output**:
```
✅ Loading development context...
✅ Context loaded (7 memory files + constitution)
✅ Validating pipeline state...
✅ Phase 3 - IMPLEMENTATION confirmed
✅ Checking code standards...
✅ PHPStan Level 8: Configured ✓
✅ ESLint: Configured ✓
✅ Architecture validation...
✅ All 7 gates passed ✓

📋 CONTEXT SUMMARY:
   Feature: #006 - PHI Logging Cleanup
   Phase: Implementation (26 tasks)
   Recent: Phase 5 E2E testing completed

🎯 NEXT TASK:
   T001: Create migration for redaction_events table
   Phase A (Foundation) - 10 minutes
   Can parallelize with T002, T003

💡 READY TO START
   Say: @agent-implementer
   Or: start T001
```

---

### Example 2: Phase Mismatch Prevention

**User Input**: "Ready to code"
**Scenario**: User in planning phase, tries to jump to implementation

**Skill Output**:
```
⚠️  PHASE MISMATCH

Current State:
├─ Phase: 2 - PLANNING (Not ready for implementation)
├─ Status: plan.md exists, but tasks.md missing
└─ Next Phase: Task breakdown

🎯 REQUIRED STEPS:
   1. Generate task breakdown: /tasks
   2. Review task plan
   3. Then retry: "Ready to code"

Continue anyway? (Not recommended)
   Say: "skip validation" if you know what you're doing
```

---

### Example 3: After Long Idle Period

**User Input**: "Ready to code"
**Scenario**: User returns after 8 hours away

**Skill Output**:
```
⏰ CONTEXT UPDATE DETECTED
   Last activity: 8 hours ago
   Recent git activity: 3 commits on main branch

🔄 Refreshing context...
✅ Context loaded
✅ Detected new commits from teammates

📋 INTEGRATED CHANGES:
   New commits include:
   - Database migrations (3 files)
   - API endpoint updates (2 files)
   - Test additions (4 files)

🎯 ACTION RECOMMENDED:
   Run: git pull
   Then: "Ready to code" again

Or continue with current branch?
```

---

## Technical Details

### Files Required

**Must Exist**:
```
memory/active_context.md    (current feature, phase)
memory/tasks_plan.md        (task breakdown)
CLAUDE.md                   (runtime guidance)
.specify/memory/constitution.md  (principles & gates)
```

**Should Exist**:
```
memory/architecture.md
memory/technical.md
memory/product_requirement_docs.md
phpstan.neon / phpstan.dist.neon
.eslintrc.json or similar
tests/ (directory)
```

### Validation Rules

**Phase Validation**:
- Must be in Phase 3-4 (Implementation or just-started)
- If not, guide to correct phase first

**Git Validation**:
- Branch should match feature branch pattern: `###-feature-*`
- Working tree should be clean or have only expected changes
- Recent commits should match feature context

**Standards Validation**:
- Config files exist (not requirements to pass checks)
- No obvious syntax errors in recent changes
- Test directories exist and accessible

**Constitution Validation**:
- Load all 7 quality gates
- Verify no P0 violations
- Report any failing gates

---

## Integration Points

**Relationship to context-navigator Skill**:
- `context-navigator`: "Where am I?" (diagnostic)
- `quick-start`: "Ready to code" (preparation)
- Flow: See status → Get ready → Start coding

**Relationship to @agent-implementer**:
- `quick-start`: Pre-flight validation
- `@agent-implementer`: Task execution
- Flow: "ready to code" → @agent-implementer starts

**Relationship to /memory-read Slash Command**:
- `quick-start`: Higher-level orchestration (loads + validates)
- `/memory-read`: Lower-level display of state
- Use `/memory-read` for deep diagnostic info

---

## Troubleshooting

**Issue**: Skill says phase is wrong when you're ready to code

**Cause**: tasks.md doesn't exist

**Fix**: Run `/tasks` to generate task breakdown from plan.md

---

**Issue**: Git validation fails - branch doesn't match

**Cause**: On wrong branch (e.g., `main` or `mvp-nuclear-reset`)

**Fix**: Checkout feature branch: `git checkout 006-feature-006-logging`

---

**Issue**: Standards check reports errors

**Cause**: Config files missing or corrupted

**Fix**: Run `/standards-check` for full diagnostic

---

## Performance

This Skill performs fast operations:
- File reads (memory files, configs)
- Git status checks
- Plugin discovery and loading (NEW v2.0.0)
- Constitution parsing (NEW v2.0.0)
- Validator warm-up (NEW v2.0.0)
- Simple validation logic

**Expected execution time**: <2 seconds (with plugins and constitution)
**Expected execution time**: <1 second (core-only, no plugins)
**No side effects**: Read-only diagnostic, no changes to codebase

---

## Graceful Degradation (NEW v2.0.0)

This skill is **backward compatible** and adapts to available features:

**Without Constitution** (v1.0.0 mode):
```
⚖️  CONSTITUTIONAL CHECK
   Constitution: Not ratified (optional)
   Quality Gates: Skipped
   Status: ✅ Ready (v1.0.0 compatibility mode)
```
- All other checks work normally
- No errors or blocking

**Without Plugins** (core-only):
```
🔌 PLUGIN STATUS
   Status: Core-only mode (no project plugins)
   Commands available: 8 core commands
   Validators active: 3 core validators
```
- Core functionality unaffected
- Shows available core commands

**Without Cache** (first run):
```
🔥 WARMING VALIDATORS
   Cache: Not initialized (first run)
   Building cache for future sessions...
   Status: ✅ Ready (cache will improve future performance)
```
- Slightly slower first run (~500ms overhead)
- Subsequent runs use cache (~5x faster)

**Partial Plugin Failures**:
```
🔌 PLUGIN LOADING
   Discovered: 2 plugin packs
   ✓ project-commands v1.0.0 loaded
   ❌ broken-plugin v0.1.0 failed (manifest error)

   Status: ⚠️ PARTIAL (1/2 plugins loaded)
   Core functionality available
```
- Core system unaffected
- Successfully loaded plugins work
- Failed plugins reported but don't block

**Tech Stack Detection Fallback**:
- If unknown stack → Shows generic linter/formatter checks
- If no configs found → Suggests setup but doesn't block
- Adapts to detected project structure

This ensures:
1. Smooth migration from v1.0.0 → v2.0.0
2. Works in minimal environments
3. Incremental feature adoption
4. No breaking changes

---

## What This Skill Does NOT Do

- ❌ Does NOT fix code standards issues (use `/standards-check`)
- ❌ Does NOT run tests (use `/test-run` if plugin exists, or manual test command)
- ❌ Does NOT execute tasks (use `@agent-implementer`)
- ❌ Does NOT sync memory (use `/memory-sync`)
- ❌ Does NOT install plugins (use `/plugin-install`)
- ❌ Does NOT fix constitutional violations (use specific validators)

This Skill validates you're READY. The slash commands and agents do the actual work.
