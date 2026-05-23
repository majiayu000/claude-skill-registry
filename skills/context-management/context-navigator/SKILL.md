---
name: Project Context Navigator
description: Display comprehensive project status dashboard showing current feature, pipeline phase, task progress, memory health, and recommended next actions. Use when the user asks about project status ("where am I", "what's my context", "current status", "project status"), appears disoriented about their work state, switches contexts between projects, or at session start when context awareness is needed. Essential for multi-project developers using Spec Kit + CCGC workflows.
allowed-tools: Read, Glob, Bash
---

# Project Context Navigator

## Purpose

This Skill provides instant orientation for developers using Spec Kit + CCGC integration pipelines. It replaces the need to manually check multiple files (active_context.md, tasks_plan.md, git status) by displaying a unified dashboard showing:

- Current feature and phase in the pipeline (7-phase workflow)
- Task progress and next immediate action
- Memory system health (file staleness, completeness)
- Architecture and technical standards compliance
- Recommended next steps based on current state

**Key Problem Solved**: Eliminates the "where am I?" disorientation that occurs in CLI-based development without persistent visual cues.

---

## When to Use This Skill

**User Initiates** (explicit triggers):
- "Where am I in the project?"
- "What's my current status?"
- "What phase is this feature in?"
- "Project status"
- "What should I be working on?"
- Switching between projects: "What's the state of [other-project]?"

**Auto-Activate** (contextual triggers):
- Session start (after CLI boots)
- After returning from long idle period (context may have changed)
- Context confusion: "I'm not sure what..."
- State mismatch questions: "Why is branch X but memory says feature Y?"

**Multi-Project Scenarios**:
- Developer maintains 3+ codebases with same Spec Kit + CCGC structure
- Quick switch between projects: Instantly see which feature and phase each is in
- No context loss: Dashboard shows per-project state

---

## How It Works

### Step 1: Gather Current State (Using Native Prompt Caching)

**Performance Optimization**: Leverage Claude 4.5 native prompt caching with `cache_control` blocks:

```
SYSTEM PROMPT (with caching):
[Context about GCSK project and skills]
<cache_control type="ephemeral">

[Load all 7 memory files - auto-cached by Claude API]
- active_context.md
- tasks_plan.md  
- architecture.md
- technical.md
- product_requirement_docs.md
- decisions.md
- glossary.md

[Constitution and specifications]
- constitution.md
- README.md

</cache_control>

Cache benefits:
- 5-minute TTL (auto-refreshes on use)
- 90% cost reduction on cache hits
- No custom cache management needed
- Invalidates automatically when files change
```

Read these files to understand the complete picture:

**Primary State Files** (project root `/memory/`):
- `active_context.md` - Current feature, phase, last activity
- `tasks_plan.md` - Task breakdown, completion status, current focus
- Git status: Current branch, commits since last sync

**Secondary State Files** (.specify/):
- `constitution.md` - Project principles, quality gates
- `README.md` - Project overview

**Diagnostic Info**:
- Git: `git rev-parse --show-toplevel` (detect project)
- Git: `git branch --show-current` (current branch)
- Git: `git log -1 --format=%h (recent commit for context)
- File timestamps: When each memory file was last updated

**Note**: The `load_memory_parallel` function loads all 7 core memory files simultaneously, cached results are reused within 5-minute TTL.

### Step 2: Detect Current Phase (7-Phase Pipeline)

Determine which phase by checking file existence and content:

```
No spec.md (phase 0)
    ↓
spec.md exists (phase 1 - Specification)
    ↓
spec.md + plan.md (phase 2 - Planning)
    ↓
spec.md + plan.md + tasks.md (phase 3 - Task Breakdown)
    ↓
Tasks marked as in-progress/complete (phase 4 - Implementation)
    ↓
All tests passing (phase 5 - Validation)
    ↓
Memory synced (phase 6 - Learning & Completion)
    ↓
New feature ready (back to phase 0/1)
```

### Step 3: Calculate Health Metrics

**Memory Health**:
- Check if all 7 core files exist
- Check timestamps: Which files are stale (>2 hours, >24 hours)?
- Calculate: `health_percentage = (files_exist + files_fresh) / 7 * 100`

**Task Progress**:
- Count completed tasks (marked `[x]` in tasks_plan.md)
- Count total tasks
- Calculate: `completion = completed / total * 100`
- Identify next unchecked task

**Context Freshness**:
- Compare: active_context.md timestamp vs current time
- Compare: git branch vs recorded branch (mismatch detection)
- Compare: git log vs recorded last activity

**Constitutional Compliance (NEW v2.0.0)**:
- Check if `.specify/memory/constitution.md` exists
- If exists: Parse principle count and names
- Check for cached validation results in `.claude/cache/validator-results/`
- Read recent audit logs from `.claude/audit/YYYY-MM-DD.json`
- Determine compliance status per principle
- Calculate overall compliance rate

**Plugin System Status (NEW v2.0.0)**:
- Check if `.claude/commands/plugins/` directory exists
- Scan for `plugin.json` manifests
- Read cached plugin registry from `.claude/cache/plugins.json`
- Count loaded plugin packs and their provides (commands, validators)
- Calculate total available commands (core + plugins)

**Validator Results (NEW v2.0.0)**:
- Check for core validators in `.claude/validators/core/`
- Check for plugin validators in `.claude/validators/plugins/`
- Read recent validator execution results from cache
- Parse exit codes to determine status (0=pass, 1=critical, 2=high, 3=medium, 4=low)
- Aggregate by severity and recency

### Step 4: Display Dashboard

Format output as a visual dashboard with sections:

```
🎯 PROJECT CONTEXT DASHBOARD
════════════════════════════════════════════════════════════════

📦 PROJECT IDENTIFICATION
   Project: [Project Name from git root or CLAUDE.md]
   Directory: [Absolute path]
   Repo: [URL from git remote]

🌿 GIT STATE
   Branch: [current branch]
   Commit: [recent hash + message]
   Status: [working tree clean/dirty + changes count]

📍 PIPELINE PHASE
   Current Phase: [Phase N of 7]: [Phase Name]
   Status: [IN PROGRESS / READY FOR NEXT / COMPLETE]
   Prerequisites: [✅ All met / ❌ Missing X files]

🎪 ACTIVE FEATURE (if applicable)
   Feature ID: [Feature number]
   Name: [Feature name]
   Priority: [P0 CRITICAL / P1 HIGH / etc]
   Status: [Specification / Planning / Implementation / Testing / Complete]

📋 TASK PROGRESS (if in implementation phase)
   Total Tasks: [N tasks]
   Completed: [N tasks]
   In Progress: [N tasks]
   Next Task: [Task ID: Task description (Est. time)]
   Parallel Opportunities: [N tasks marked with [P]]
   Estimated Time to Complete: [Total hours]

📊 MEMORY SYSTEM HEALTH
   Core Files: [M/7 files exist]
   Freshness: [N% fresh, X stale, Y very stale]
   Last Sync: [N hours ago / N days ago]
   Issues: [if any]

⚖️  CONSTITUTIONAL COMPLIANCE (NEW v2.0.0)
   Constitution: [✅ Found / ❌ Not ratified]
   Principles: [N total principles defined]
   Compliance Status:
   ├─ Principle I:   [✅ PASS / ⚠️ WARN / ❌ FAIL] ([last check time])
   ├─ Principle II:  [✅ PASS / ⚠️ WARN / ❌ FAIL] ([last check time])
   ├─ [Additional principles...]
   └─ Overall: [N]/[M] principles compliant ([%] compliance rate)

   Recent Violations: [if any]
   Quality Gates: [N passed / M total]

🔍 VALIDATION RESULTS (NEW v2.0.0)
   Core Validators:
   ├─ memory-consistency:    [✅ PASS / ⚠️ WARN / ❌ FAIL] ([last run])
   ├─ phase-transition:      [✅ PASS / ⚠️ WARN / ❌ FAIL] ([last run])
   └─ architectural-boundaries: [✅ PASS / ⚠️ WARN / ❌ FAIL] ([last run])

   Project Validators: [if plugins exist]
   ├─ [validator-name]:      [✅ PASS / ⚠️ WARN / ❌ FAIL] ([last run])
   └─ [Additional validators...]

   Summary: [N passed, X warnings, Y failures]

🔌 PLUGINS (NEW v2.0.0)
   Status: [✅ Loaded / ⚠️ Partially loaded / ❌ None]
   Loaded Packs: [N plugin packs]
   ├─ [plugin-pack-name] v[X.Y.Z] ([N commands, M validators])
   └─ [Additional plugin packs...]
   Commands Available: [X core + Y plugin = Z total]
   Validators Active: [A core + B plugin = C total]

⚠️  DETECTED ISSUES (if any)
   [List any state mismatches, stale context, missing files, violations, etc.]

🎯 RECOMMENDED NEXT ACTIONS
   1. [Specific action based on phase and compliance status]
   2. [Next step after that]
   3. [Alternative if stuck or blocked by violations]

💡 QUICK COMMANDS
   /memory-read         [Load all memory]
   /memory-sync         [Update stale files]
   /constitution-check  [Run constitutional validation] (NEW v2.0.0)
   /plugin-list         [Show loaded plugins] (NEW v2.0.0)
   /implement           [Start/continue implementation]
   @agent-implementer   [Execute next task]

════════════════════════════════════════════════════════════════
```

### Step 5: Provide Intelligent Recommendations

Based on current phase, suggest specific next actions:

**If Phase 0 (No Spec)**:
```
→ Next: Create feature specification
  Run: /specify "Your feature description"
  Or ask: "I want to build X"
```

**If Phase 1 (Spec Exists)**:
```
→ Next: Create implementation plan
  Run: /plan
  Or ask: "How should we build this?"
```

**If Phase 2-3 (Planning Complete, Tasks Ready)**:
```
→ Next: Load context and start coding
  Run: "ready to code" → quick-start Skill
  Or ask: "start coding"
```

**If Phase 4 (Implementation In Progress)**:
```
→ Next: Continue with next task
  Current Task: [T001: Description]
  Run: @agent-implementer
  Or ask: "implement next task"
```

**If Phase 5 (Tests Passing)**:
```
→ Next: Capture learnings
  Run: /memory-sync
  Or ask: "sync memory"
```

---

## Examples

### Example 1: Session Start (Orientation)

**User Action**: Opens Claude Code CLI at start of day

**Skill Activation**: Automatic (session start context needed)

**Skill Output**:
```
🎯 PROJECT CONTEXT DASHBOARD - IECPN Dashboard
════════════════════════════════════════════════════════════════

📦 PROJECT: IECPN Healthcare Dashboard

🌿 GIT STATE
   Branch: 006-feature-006-logging ✓ (matches active feature)
   Commit: 217b377 "feat: implement Phase 5 E2E testing"
   Status: Clean (no uncommitted changes)

📍 PHASE: 4 / 7 - IMPLEMENTATION (Active)
   Feature: #006 - PHI Logging Cleanup
   Status: IN PROGRESS ✓
   Prerequisites: ✅ All met

🎪 ACTIVE FEATURE
   ID: 006
   Name: PHI Logging Cleanup and Automated Redaction
   Priority: P0 CRITICAL
   Compliance Impact: LGPD Art. 46, HIPAA §164.312
   Tasks: 26 total
   ├─ Completed: 0
   ├─ In Progress: 0
   └─ Next: T001 - Create migration (10 min, [P] parallel)

📊 MEMORY HEALTH
   Files: 7/7 complete ✓
   Freshness: 2 fresh, 1 stale (>2h), 4 current
   Last Sync: 11 hours ago ⚠️
   Recommendation: Run /memory-sync to refresh context

⚠️  CONTEXT ISSUE DETECTED
   active_context.md is 11 hours stale
   Recommend: /memory-sync to update before starting

🎯 NEXT ACTIONS
   1. Refresh context: /memory-sync
   2. Load full context: "ready to code"
   3. Begin implementation: @agent-implementer

💡 QUICK ACTIONS
   Type: "sync memory" → Auto-run /memory-sync
   Type: "ready to code" → Load context + validate
   Type: "start 006" → Begin Feature 006 implementation
════════════════════════════════════════════════════════════════
```

---

### Example 2: Multi-Project Context Switch

**User Action**: "Where am I?" (after switching between 3 projects)

**Skill Activation**: Automatic (context confusion)

**Skill Output**:
```
🎯 MULTI-PROJECT STATUS
════════════════════════════════════════════════════════════════

🔍 DETECTED: You switched projects

📍 CURRENT PROJECT: /Users/dev/personal/dev_IECPN
   Branch: 006-feature-006-logging
   Phase: 4 - IMPLEMENTATION (26 tasks, 0% complete)
   Feature: PHI Logging Cleanup (P0 CRITICAL)
   Memory: Stale (11 hours)
   Next: @agent-implementer

📍 OTHER PROJECTS (in recent git history):
   /Users/dev/work/api-refactor
   Branch: 012-api-gateway
   Phase: 2 - PLANNING (plan.md created, no tasks yet)
   Memory: Current (1 hour old)
   Next: /tasks to generate task breakdown

   /Users/dev/personal/ml-pipeline
   Branch: master
   Phase: 1 - SPECIFICATION (no plan.md yet)
   Memory: Very stale (3 days old)
   Next: /memory-sync, then /plan for design

════════════════════════════════════════════════════════════════
```

---

### Example 3: Detecting State Mismatch

**User Action**: "Project status"

**State Detected**:
- Branch: `mvp-nuclear-reset`
- active_context.md says: Feature 006 in progress
- Git log shows: Phase 6 work completed
- No 006 branch checkout

**Skill Output**:
```
🎯 PROJECT STATUS - State Mismatch Detected
════════════════════════════════════════════════════════════════

⚠️  BRANCH-CONTEXT MISMATCH

Current State:
├─ Git Branch: mvp-nuclear-reset (not a feature branch)
├─ Memory Says: Feature 006 in progress
└─ Conflict: These don't match!

Recent History:
└─ Latest commit: Phase 6 complete (7b82d09)

Analysis:
Most likely: You completed Phase 6, need to start Feature 006
├─ Option 1: Checkout 006 branch to start Feature 006
├─ Option 2: Sync memory to update context to completed state

🎯 RECOMMENDED:
1. Run: /memory-sync
   (Update active_context.md with current state)

2. Then: Choose next action
   - Start Feature 006: git checkout 006-feature-006-logging
   - Start new feature: /specify "description"
   - Review Phase 6 completion: "summary of phase 6"

💡 QUICK FIX
   Type: "sync context" → Auto-run /memory-sync
   Type: "start 006" → Checkout 006 branch + sync
════════════════════════════════════════════════════════════════
```

---

## Technical Implementation Details

### File Locations to Check

**Project Root**:
```
/memory/
├── active_context.md     (1) Current feature, phase, activity
├── tasks_plan.md         (2) Task breakdown and progress
├── architecture.md       (3) System design (reference only)
├── technical.md          (4) Tech standards (reference only)
├── product_requirement_docs.md  (5) Feature scope
├── lessons-learned.md    (6) Implementation insights
└── error-documentation.md (7) Known issues

CLAUDE.md                  → Runtime guidance + project name
```

**Spec Kit**:
```
.specify/
├── memory/constitution.md → Principles, quality gates
└── README.md              → Project overview
```

**Constitutional System (NEW v2.0.0)**:
```
.claude/cache/
├── principle-registry.json       → Parsed constitution principles
├── plugins.json                  → Loaded plugin registry
└── validator-results/            → Recent validator execution results
    ├── architectural-boundaries-[hash].json
    └── memory-consistency-[hash].json

.claude/audit/
└── YYYY-MM-DD.json              → Daily audit log with validation history
```

**Plugin System (NEW v2.0.0)**:
```
.claude/commands/plugins/
└── [plugin-pack-name]/
    ├── plugin.json              → Plugin manifest
    └── [command-name]/          → Plugin commands

.claude/validators/plugins/
└── [plugin-pack-name]/
    ├── plugin.json              → Validator manifest
    └── [validator-name].sh      → Validator scripts
```

**Git Info**:
```
$(git rev-parse --show-toplevel)  → Project root
$(git branch --show-current)      → Current branch
$(git log -1 --format=%h)         → Recent commit
$(git status --porcelain)         → Working tree state
```

### Staleness Indicators

**Freshness Categories**:
- **Current**: Modified within 1 hour
- **Stale**: 1-24 hours old (⚠️)
- **Very Stale**: >24 hours old (🔴)
- **Missing**: File doesn't exist (❌)

### Phase Detection Logic

```bash
# Pseudocode for phase detection
if [ ! -f spec.md ]; then
    phase=0  # No specification
elif [ ! -f plan.md ]; then
    phase=1  # Specification exists, planning needed
elif [ ! -f tasks.md ]; then
    phase=2  # Planning complete, tasks needed
elif grep -q "^\- \[ \]" tasks.md; then
    phase=3  # Tasks exist, implementation needed
elif grep -q "all tests passing\|✅ validation complete" active_context.md; then
    phase=5  # Tests passing, learning phase
else
    phase=4  # Implementation in progress
fi
```

---

## Integration with Other Skills

**Relationship to quick-start Skill**:
- `context-navigator`: Shows status (read-only)
- `quick-start`: Loads full context (write-capable)
- User flow: context-navigator → quick-start → coding

**Relationship to phase-guide Skill**:
- `context-navigator`: Current phase snapshot
- `phase-guide`: Detailed phase-by-phase navigation
- User flow: context-navigator detects phase, phase-guide guides transitions

**Relationship to memory-keeper Skill**:
- `context-navigator`: Detects stale context
- `memory-keeper`: Proactively maintains freshness
- User flow: context-navigator warns staleness, memory-keeper auto-fixes

---

## Troubleshooting

**Issue**: Dashboard shows but recommendations seem wrong

**Diagnosis**: Check if active_context.md accurately reflects current state

**Fix**: Run `/memory-sync` to update memory files

---

**Issue**: Can't determine current phase

**Diagnosis**: Check for spec.md, plan.md, tasks.md existence

**Fix**: Ensure .specify/ and memory/ directories exist

---

## Performance Notes

This Skill performs these fast, read-only operations:
1. File reads (active_context.md, tasks_plan.md, constitution.md)
2. Git status checks
3. File timestamp comparison
4. Cache file reads (plugins.json, principle-registry.json) (NEW v2.0.0)
5. Recent audit log parsing (optional) (NEW v2.0.0)

**Expected execution time**: <500ms
**No side effects**: Pure read-only diagnostic Skill

## Graceful Degradation (NEW v2.0.0)

This skill is **backward compatible** and works in all configurations:

**Without Constitution** (v1.0.0 compatibility):
- Constitutional Compliance section shows: "Constitution: Not ratified"
- All other sections work normally
- No errors or failures

**Without Plugins** (core-only mode):
- Plugins section shows: "Status: None (core commands only)"
- Commands Available shows only core count (8 commands)
- Validators shows only core validators (3 validators)

**Without Cache Files** (fresh installation):
- Reads directly from source files instead of cache
- Slightly slower (<100ms additional overhead)
- No functional differences

**Partial Plugin Failure** (some plugins broken):
- Shows which plugins loaded successfully
- Lists broken plugins with error messages
- Core functionality unaffected

**Missing v2.0.0 Directories**:
```
No .claude/cache/ → "Cache not initialized (run session-start hook)"
No .claude/audit/ → "Audit logging not enabled"
No .claude/validators/plugins/ → "No project validators installed"
```

This ensures developers can:
1. Use v2.0.0 features incrementally
2. Migrate from v1.0.0 without breaking changes
3. Work in minimal environments (core only)
4. Debug plugin issues without losing core functionality
