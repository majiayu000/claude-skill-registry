---
name: do
description: Execute increment implementation following spec and plan - hooks run after EVERY task
hooks:
  PostToolUse:
    - matcher: Edit
      hooks:
        - type: command
          command: bash plugins/specweave/hooks/v2/guards/task-ac-sync-guard.sh
    - matcher: Write
      hooks:
        - type: command
          command: bash plugins/specweave/hooks/v2/guards/task-ac-sync-guard.sh
---

# Do Increment

**Implementation Execution**: Following spec.md and plan.md to execute the increment work.

You are helping the user implement a SpecWeave increment by executing tasks from tasks.md with automatic documentation updates after EVERY task completion.

## Usage

```bash
# Auto-resumes from last incomplete task
/sw:do <increment-id>

# Or let it find active increment automatically
/sw:do

# Override model selection for all tasks (advanced)
/sw:do <increment-id> --model haiku
/sw:do <increment-id> --model sonnet
/sw:do <increment-id> --model opus
```

## Arguments

- `<increment-id>`: Optional. Increment ID (e.g., "001", "0001", "1", "0042")
  - If omitted, **MUST auto-select best candidate** (see Step 0.5 below)
  - **Smart resume**: Automatically starts from next incomplete task

- `--model <tier>`: Optional. Override model selection for all tasks
  - `haiku`: Fast, cheap execution (simple mechanical tasks)
  - `sonnet`: Legacy option (rarely needed)
  - `opus`: Maximum quality (default for all complex tasks)
  - If omitted, uses model hints from tasks.md (recommended)

---

## Workflow

### Step 0.5: Smart Increment Auto-Selection (MANDATORY when no ID provided)

**🎯 CRITICAL: When user runs `/sw:do` without increment ID, you MUST auto-select the best candidate.**

**DO NOT** ask the user for an increment ID. **DO NOT** fail with "increment ID required". Instead:

1. **Scan for candidates** in this priority order:

   ```bash
   # Priority 1: in-progress (resume work)
   IN_PROGRESS=$(find .specweave/increments -maxdepth 2 -name "metadata.json" -exec grep -l '"status": "in-progress"' {} \; 2>/dev/null | head -1)

   # Priority 2: planned (start next work)
   PLANNED=$(find .specweave/increments -maxdepth 2 -name "metadata.json" -exec grep -l '"status": "planned"' {} \; 2>/dev/null | head -1)

   # Priority 3: ready_for_review with incomplete tasks (needs finishing)
   READY=$(find .specweave/increments -maxdepth 2 -name "metadata.json" -exec grep -l '"status": "ready_for_review"' {} \; 2>/dev/null)

   # Priority 4: backlog with tasks (can start)
   BACKLOG=$(find .specweave/increments -maxdepth 2 -name "metadata.json" -exec grep -l '"status": "backlog"' {} \; 2>/dev/null)
   ```

2. **For each candidate**, check if it has incomplete tasks:

   ```bash
   # Count incomplete tasks in tasks.md (supports multiple formats)
   # Format 1: List items "- [ ] Task"
   INCOMPLETE=$(grep -c '^\- \[ \]' "$INCREMENT_PATH/tasks.md" 2>/dev/null || echo "0")
   # Format 2: Status field "**Status**: [ ] pending"
   INCOMPLETE_STATUS=$(grep -c '\*\*Status\*\*: \[ \]' "$INCREMENT_PATH/tasks.md" 2>/dev/null || echo "0")
   # Total incomplete = sum of all formats
   TOTAL_INCOMPLETE=$((INCOMPLETE + INCOMPLETE_STATUS))
   ```

3. **Select the best candidate**:
   - If `in-progress` increment exists → use it
   - Else if `planned` increment exists → use it
   - Else if `ready_for_review` with incomplete tasks → use it
   - Else if `backlog` increment exists with incomplete tasks → use it (and change status to in-progress)

4. **If candidate found, display selection and continue**:

   ```
   🎯 Auto-selected increment: 0162-lsp-skill-integration

   Status: backlog → in-progress (auto-promoted)
   Tasks: 0/28 completed (0%)
   Priority: P1
   Type: refactor

   Proceeding with execution...
   ```

5. **If NO candidates found (all done), show insights and ask user**:

   ```
   ✅ All increments completed!

   📊 Quick Status:
   ┌─────────────────────────────────────────────────────────────┐
   │  Active: 0 | Backlog: 0 | Completed: 47 | Archived: 125    │
   │  Last completed: 0167-comprehensive-code-review (2 days ago) │
   └─────────────────────────────────────────────────────────────┘

   🔮 Recent completions:
      • 0175-plugin-session-restart-warning (completed 1 day ago)
      • 0174-router-brain-orchestrator (ready_for_review)
      • 0167-comprehensive-code-review (ready_for_review)

   💡 What would you like to do?

   Options:
     A) Create new increment: /sw:increment "feature name"
     B) Close ready_for_review: /sw:done 0174
     C) Resume from backlog: /sw:resume 0162
     D) View full status: /sw:status

   Your choice? [A/B/C/D or type feature name]: _
   ```

**Why This Matters**:
- Users shouldn't need to remember increment IDs
- `/sw:do` should "just work" like `/sw:auto`
- Smart selection saves context switches

---

### Step 0: Self-Awareness Check

**🎯 OPTIONAL BUT RECOMMENDED**: Check if running in SpecWeave repository itself.

This step is particularly useful when implementing SpecWeave features vs user projects, as it provides context for:
- Understanding if changes affect the framework
- Being careful with breaking changes
- Considering backward compatibility

```typescript
import { detectSpecWeaveRepository } from './src/utils/repository-detector.js';

const repoInfo = detectSpecWeaveRepository(process.cwd());

if (repoInfo.isSpecWeaveRepo) {
  console.log('ℹ️  Working on SpecWeave framework increment');
  console.log(`   Confidence: ${repoInfo.confidence}`);
  console.log('');
  console.log('   💡 Reminders:');
  console.log('      • Test changes don\'t break existing user projects');
  console.log('      • Consider backward compatibility');
  console.log('      • Update CLAUDE.md if workflow changes');
  console.log('');
}
```

**When to Show This**:
- On first task execution for the increment
- Skip on subsequent tasks (user already knows context)

**Why This Helps**:
Contributors working on SpecWeave itself need different mindset than users building apps:
- Framework changes affect ALL users
- Breaking changes need deprecation warnings
- Documentation updates are critical

---

### Step 1: Load Context

**Prerequisite**: Increment ID is now available (either from user input or auto-selected in Step 0.5).

1. **Find increment directory**:
   - **Normalize increment ID**:
     - If ID contains dash (e.g., "0153-feature-name"), extract numeric portion before first dash → "0153"
     - Convert to 4-digit format (e.g., "1" → "0001", "153" → "0153")
     - Both formats work: `/sw:do 0153` or `/sw:do 0153-feature-name`
   - Find matching directory: `.specweave/increments/0001-*/` (matches by prefix)
   - Verify increment exists

2. **Load specification and plan**:
   - Read `spec.md` - Understand WHAT and WHY
   - Read `plan.md` - Understand HOW
   - Read `tasks.md` - Understand implementation steps
   - Read `tests.md` - Understand test strategy

3. **🔄 Load Living Docs Context**:

   **Optional but recommended**: Load relevant living documentation context.

   ```bash
   # Extract topic keywords from spec.md title/user stories
   TOPIC=$(grep -m1 "^#" spec.md | sed 's/# //' | tr '[:upper:]' '[:lower:]')

   # Check if related living docs exist
   LIVING_DOCS_ROOT=".specweave/docs/internal"
   RELATED_DOCS=$(find "$LIVING_DOCS_ROOT" -name "*${TOPIC}*" -o -name "*${KEYWORD}*" 2>/dev/null)
   ```

   **If related living docs found**:
   - Read relevant ADRs from `.specweave/docs/internal/architecture/adr/`
   - Read relevant specs from `.specweave/docs/internal/specs/`
   - Read relevant architecture docs from `.specweave/docs/internal/architecture/`

   **Why This Helps**:
   - Ensures implementation follows established patterns
   - Avoids contradicting existing ADRs
   - Provides historical context for design decisions
   - References related features for consistency

   **Example output**:
   ```
   📚 Living Docs Context Loaded:
      • ADR-0023: Database Connection Pooling (relevant)
      • spec-005: User Management (related feature)
      • architecture/auth-flow.md (pattern to follow)
   ```

   **Skip if**: Living docs don't exist or no relevant docs found

4. **Verify readiness**:
   - Check status is "planned" (not already in-progress or completed)
   - Check no blocking dependencies
   - Check tasks.md has tasks to execute

5. **🚨 CRITICAL: Task Count Validation (CRASH PREVENTION!)**:

   **MANDATORY**: Count tasks in tasks.md before proceeding.

   ```bash
   TASK_COUNT=$(grep -c "^### T-" .specweave/increments/<id>/tasks.md)
   ```

   **If TASK_COUNT > 25**:
   ```
   ⚠️ TASK COUNT EXCEEDS SOFT LIMIT

   This increment has X tasks (soft limit: 25)

   >25 tasks = consider splitting for maintainability (per CLAUDE.md rules)

   💡 RECOMMENDED: Split this increment OR execute phase-by-phase:

   Option A - Split into separate increments:
   Pattern: 0116-feature/ → Split into:
     • 0116-feature-phase1/ (T-001 to T-008)
     • 0117-feature-phase2/ (T-009 to T-016)
     • 0118-feature-phase3/ (T-017 to T-025)

   Option B - Phase-by-phase execution (recommended for 15-25 tasks):
     Execute Phase 1 → validate → continue to Phase 2 → ...

   User choice required to proceed.
   ```

   **If TASK_COUNT <= 25**: Proceed to next step

6. **🚨 CRITICAL: Validate AC Presence**:

   **MANDATORY**: Run pre-increment-start validation hook to verify spec.md contains ACs.

   Use the Bash tool to run:
   ```bash
   bash plugins/specweave/hooks/pre-increment-start.sh <increment-path>
   # Example: bash plugins/specweave/hooks/pre-increment-start.sh .specweave/increments/0050-feature-name
   ```

   **Expected Output (Success)**:
   ```
   ✅ AC Presence Validation PASSED
      • spec.md contains 39 ACs
      • Matches metadata.json (39 expected)
      • Ready to start implementation
   ```

   **Expected Output (Failure)**:
   ```
   ❌ AC Presence Validation FAILED
      • spec.md contains 0 ACs (expected 39)
      • ACs are REQUIRED for task-AC sync to work

   💡 Fix: Run /sw:embed-acs <increment-id>
   ```

   **What to Do After Validation**:
   - ✅ **If validation passes**: Proceed to Step 2
   - ❌ **If validation fails**: Show error, run `/sw:embed-acs`, then retry
   - **DO NOT PROCEED** without ACs in spec.md (hooks will fail!)

   **Why This Matters** (ADR-0064):
   - The AC sync hook requires ACs in spec.md to update completion status
   - Without inline ACs, you get 0% AC completion and broken status line
   - Even with external living docs, ACs MUST be embedded in spec.md

**Example output**:
```
📂 Loading increment 0001-user-authentication...

✅ Loaded context:
   • spec.md (6 user stories, 15 requirements)
   • plan.md (Architecture: JWT + PostgreSQL)
   • tasks.md (42 tasks, estimated 3-4 weeks)
   • tests.md (12 test cases, 85% coverage)

🎯 Ready to execute!
```

### Step 1.5: Check TDD Mode

**Read testMode from metadata.json:**

```bash
INCREMENT_PATH=".specweave/increments/<id>"
TEST_MODE=$(cat "$INCREMENT_PATH/metadata.json" | jq -r '.testMode // "test-after"')
```

**If TEST_MODE == "TDD", display TDD reminder banner:**

```
┌─────────────────────────────────────────────────────────────┐
│  🔴 TDD MODE ACTIVE                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  This increment uses Test-Driven Development.               │
│                                                             │
│  WORKFLOW:                                                  │
│  1. [RED]      Write failing test FIRST                     │
│  2. [GREEN]    Minimal code to make test pass               │
│  3. [REFACTOR] Improve code, keep tests green               │
│                                                             │
│  ⚠️  GREEN tasks depend on their RED counterpart!           │
│  💡 Tip: Use /sw:tdd-cycle for guided workflow              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**When executing tasks, detect and display current phase:**

```bash
CURRENT_TASK_TITLE="T-001: [RED] Write failing test for login"

if [[ "$CURRENT_TASK_TITLE" == *"[RED]"* ]]; then
  PHASE="🔴 RED - Writing failing test"
elif [[ "$CURRENT_TASK_TITLE" == *"[GREEN]"* ]]; then
  PHASE="🟢 GREEN - Making test pass"
elif [[ "$CURRENT_TASK_TITLE" == *"[REFACTOR]"* ]]; then
  PHASE="🔵 REFACTOR - Improving code quality"
else
  PHASE=""  # Not a TDD task
fi

if [ -n "$PHASE" ]; then
  echo "Current Phase: $PHASE"
fi
```

**Skip TDD banner if**:
- `testMode` is not "TDD"
- Already showed banner in current session

### Step 1.5.5: TDD Marker Validation (CRITICAL when TDD mode is enabled)

**🚨 CRITICAL: When TDD mode is active, verify tasks.md has TDD markers!**

This step MUST run BEFORE Step 1.6 enforcement to catch the case where TDD is enabled but tasks were NOT generated with `/sw:increment`.

**Check for TDD markers in tasks.md:**

```bash
INCREMENT_PATH=".specweave/increments/<id>"
TASKS_FILE="$INCREMENT_PATH/tasks.md"

# Count TDD markers
RED_COUNT=$(grep -c '\[RED\]' "$TASKS_FILE" 2>/dev/null || echo "0")
GREEN_COUNT=$(grep -c '\[GREEN\]' "$TASKS_FILE" 2>/dev/null || echo "0")
REFACTOR_COUNT=$(grep -c '\[REFACTOR\]' "$TASKS_FILE" 2>/dev/null || echo "0")
TOTAL_MARKERS=$((RED_COUNT + GREEN_COUNT + REFACTOR_COUNT))

echo "TDD Markers found: RED=$RED_COUNT, GREEN=$GREEN_COUNT, REFACTOR=$REFACTOR_COUNT"
```

**If TDD mode is enabled BUT no markers found (TOTAL_MARKERS == 0):**

```typescript
function validateTDDMarkers(tasksContent: string, tddMode: string, tddEnforcement: string): void {
  if (tddMode !== 'TDD') return; // Not TDD mode, skip

  const hasRedMarkers = tasksContent.includes('[RED]');
  const hasGreenMarkers = tasksContent.includes('[GREEN]');
  const hasRefactorMarkers = tasksContent.includes('[REFACTOR]');

  if (!hasRedMarkers && !hasGreenMarkers && !hasRefactorMarkers) {
    // TDD mode enabled but NO markers in tasks.md!
    const message = `
⚠️  TDD MODE ENABLED BUT TASKS LACK TDD MARKERS

Your config has TDD mode enabled:
  testing.defaultTestMode: "TDD"

But tasks.md has NO [RED], [GREEN], [REFACTOR] markers.

This means TDD enforcement CANNOT work because:
  • /sw:do checks task markers to enforce order
  • Without markers, enforcement is silently bypassed

CAUSE: Tasks were likely created manually or before TDD was enabled.

FIX OPTIONS:
  1. (Recommended) Regenerate tasks with /sw:increment
     This will create proper RED→GREEN→REFACTOR triplets

  2. Add markers manually to existing tasks:
     ### T-001: [RED] Write failing test for feature X
     ### T-002: [GREEN] Implement feature X to pass test
     ### T-003: [REFACTOR] Clean up feature X code

  3. Disable TDD mode:
     Set testing.defaultTestMode: "test-after" in config.json
`;

    if (tddEnforcement === 'strict') {
      console.error(message);
      console.error('❌ BLOCKED: Cannot proceed without TDD markers in strict mode.');
      console.error('   Fix tasks.md or change tddEnforcement to "warn".');
      throw new Error('TDD_MARKERS_MISSING');
    } else if (tddEnforcement === 'warn') {
      console.warn(message);
      console.warn('⚠️  Proceeding without TDD enforcement (warn mode)...');
    }
    // If tddEnforcement === 'off', silently continue
  }
}
```

**Enforcement behavior:**

| tddEnforcement | TDD Enabled + No Markers | Behavior |
|----------------|--------------------------|----------|
| `strict` | **BLOCK** | ❌ "Cannot proceed without TDD markers. Run /sw:increment or add markers manually." |
| `warn` (default) | **WARN but allow** | ⚠️ "TDD markers missing. Enforcement bypassed. Consider regenerating tasks." |
| `off` | **No check** | Silent pass |

**Example output (strict mode, no markers):**

```
❌ TDD MARKER VALIDATION FAILED

TDD mode is enabled (testing.defaultTestMode: "TDD")
But tasks.md has 0 TDD markers:
  • [RED] markers: 0
  • [GREEN] markers: 0
  • [REFACTOR] markers: 0

This means TDD discipline CANNOT be enforced!

💡 To fix, choose one:
   1. /sw:increment "feature-name"  ← Regenerate with TDD tasks
   2. Add [RED]/[GREEN]/[REFACTOR] markers to task titles
   3. Set tddEnforcement: "warn" to proceed anyway

Blocked in strict mode. Fix markers or change enforcement level.
```

**Example output (warn mode, no markers):**

```
⚠️  TDD MARKERS MISSING

TDD mode is enabled but tasks.md lacks [RED]/[GREEN]/[REFACTOR] markers.
TDD enforcement is effectively DISABLED for this increment.

💡 For proper TDD discipline, regenerate tasks: /sw:increment "feature"

Proceeding without enforcement (warn mode)...
```

**When this validation passes:**
- TDD mode not enabled → Skip (no validation needed)
- TDD mode enabled + markers found → Pass (proceed to Step 1.6)
- TDD mode enabled + no markers + strict → Block (user must fix)
- TDD mode enabled + no markers + warn → Warn and proceed
- TDD mode enabled + no markers + off → Silent pass

### Step 1.6: TDD Enforcement (MANDATORY when TDD mode is enabled)

**🚨 CRITICAL: When TDD mode is active, enforce RED→GREEN→REFACTOR order!**

**Read enforcement level from config.json:**

```bash
CONFIG_PATH=".specweave/config.json"
TDD_ENFORCEMENT=$(cat "$CONFIG_PATH" | jq -r '.testing.tddEnforcement // "warn"')
# Values: "strict" (blocks), "warn" (allows but warns), "off" (no checks)
```

**Before marking ANY task as complete, check TDD discipline:**

```typescript
function checkTDDViolation(currentTask: Task, allTasks: Task[]): TDDViolation | null {
  // Only check if task has TDD phase marker
  const phase = extractPhase(currentTask.title); // [RED], [GREEN], [REFACTOR]
  if (!phase) return null;

  // Find related tasks in the same triplet (e.g., T-001, T-002, T-003)
  const tripletBase = Math.floor((currentTask.number - 1) / 3) * 3 + 1;

  if (phase === 'GREEN') {
    // GREEN requires RED to be completed first
    const redTask = allTasks.find(t =>
      t.number === tripletBase && t.title.includes('[RED]')
    );
    if (redTask && redTask.status !== 'completed') {
      return {
        type: 'GREEN_BEFORE_RED',
        message: `Cannot complete GREEN task (${currentTask.id}) before RED task (${redTask.id})`,
        redTaskId: redTask.id,
      };
    }
  }

  if (phase === 'REFACTOR') {
    // REFACTOR requires GREEN to be completed first
    const greenTask = allTasks.find(t =>
      t.number === tripletBase + 1 && t.title.includes('[GREEN]')
    );
    if (greenTask && greenTask.status !== 'completed') {
      return {
        type: 'REFACTOR_BEFORE_GREEN',
        message: `Cannot complete REFACTOR task (${currentTask.id}) before GREEN task (${greenTask.id})`,
        greenTaskId: greenTask.id,
      };
    }
  }

  return null; // No violation
}
```

**Enforcement behavior based on level:**

| Level | On Violation | Behavior |
|-------|--------------|----------|
| `strict` | **BLOCK** | ❌ "TDD VIOLATION: Cannot complete GREEN before RED. Complete T-001 [RED] first." |
| `warn` (default) | **WARN but allow** | ⚠️ "TDD Warning: Completing GREEN before RED violates TDD discipline." |
| `off` | **No check** | Silent pass |

**Example output (strict mode):**

```
❌ TDD ENFORCEMENT BLOCKED

You attempted to complete: T-002: [GREEN] Implement login handler
But its RED counterpart is not done: T-001: [RED] Write login test

TDD DISCIPLINE REQUIRES:
  1. 🔴 RED - Write failing test FIRST
  2. 🟢 GREEN - Then implement to pass
  3. 🔵 REFACTOR - Then improve code

💡 Complete T-001 first, then come back to T-002.
   Or disable strict enforcement: Set tddEnforcement: "warn" in config.json
```

**Example output (warn mode):**

```
⚠️  TDD DISCIPLINE WARNING

Completing T-002 [GREEN] before T-001 [RED] violates TDD discipline.

TDD works best when you:
  1. Write the failing test first (RED)
  2. Then implement just enough to pass (GREEN)

Proceeding anyway... (set tddEnforcement: "strict" to block)
```

**When to check:**
- ✅ Before marking any [GREEN] or [REFACTOR] task complete
- ❌ Skip check for [RED] tasks (they can be completed freely)
- ❌ Skip check for non-TDD tasks (no phase marker)

### Step 2: Smart Resume - Find Next Incomplete Task

**🎯 CRITICAL: Auto-resume functionality** - no need to remember which task you were on!

1. **Parse tasks.md**:
   - Scan all tasks in order
   - Check completion status (`[x]` = complete, `[ ]` = incomplete)
   - **Extract model hints** (⚡ haiku, 🧠 sonnet, 💎 opus)
   - Find first incomplete task

2. **Determine starting point**:
   - If all tasks complete → Show completion message
   - If tasks incomplete → Resume from first incomplete task
   - If no tasks started → Start from T001

3. **Show resume context with model optimization**:
   ```
   📊 Resume Context:

   Completed: 3/12 tasks (25%)
   ├─ [✅] T001: ⚡ haiku - Setup auth module (P1) [saved $0.14]
   ├─ [✅] T002: ⚡ haiku - Create user model (P1) [saved $0.14]
   ├─ [✅] T003: 💎 opus - Implement JWT tokens (P1)
   └─ [⏳] T004: ⚡ haiku - Add password hashing (P1) ← RESUMING HERE

   Remaining: 9 tasks (estimated 2 weeks)
   Cost savings so far: $0.28 (67% cheaper than all-Opus)
   ```

**Why smart resume?**
- ✅ No manual tracking needed
- ✅ Seamlessly continue after breaks
- ✅ Prevents duplicate work
- ✅ Shows progress at a glance
- ✅ **Cost optimization through smart model selection**

### Step 3: Update Status to In-Progress (if needed)

If status is "planned", update `spec.md` frontmatter:

```yaml
---
increment: 0001-user-authentication
status: in-progress      # ← Changed from "planned"
started: 2025-10-28      # ← Start date
---
```

If already "in-progress", keep existing metadata.

### Step 4: Execute Tasks Sequentially

**For each task in tasks.md**:

1. **Read task details**:
   - Task ID (T001, T002, etc.)
   - **Model hint** (⚡ haiku, 🧠 sonnet, 💎 opus)
   - Description
   - Acceptance criteria
   - File paths affected
   - Implementation notes

2. **Select execution model**:
   - **Use model from task hint** (recommended, optimizes cost/speed)
   - OR use `--model` override if specified by user
   - Show selected model and reasoning

3. **Execute task**:
   - Follow plan.md architecture
   - Implement using detected tech stack
   - Write clean, maintainable code
   - Add inline documentation
   - **Track cost savings** when using Haiku

3. **Mark task complete** in tasks.md:
   - Change `[ ]` → `[x]`
   - Add completion timestamp
   - Note any deviations from plan

4. **🔥 CRITICAL: After EVERY task completion**:

   **Step A: Hook executes automatically (via .claude/hooks.json)**:
   - 🔊 Plays completion sound (Glass.aiff on macOS)
   - 📝 Shows reminder message
   - ✅ This happens automatically when you mark task complete

   **Step B: Update GitHub Issue (if GitHub plugin enabled)**:
   - Close task GitHub issue (#43, #44, etc.)
   - Check off task in epic issue
   - Post completion comment with stats:
     - Files modified (+lines/-lines)
     - Tests passing
     - Actual vs estimated duration
     - Brief summary of changes
     - Next task
   - Update epic progress (X/Y tasks completed, Z%)
   - Add 'in-progress' label to epic (if first task)

   **Example GitHub sync**:
   ```
   🔗 Syncing to GitHub...
      ✓ Closed task issue #43
      ✓ Checked off [T-001] in epic #42
      ✓ Posted completion comment
      ✓ Updated epic progress: 7/48 tasks (15%)
   ```

   **Step C: Update project documentation inline**:
   - Update CLAUDE.md if task added:
     - New commands or CLI flags
     - New file structure
     - New configuration options
     - New skills or agents
   - Update README.md if task added:
     - User-facing features
     - Installation steps
     - Usage examples
     - API changes
   - Update CHANGELOG.md if task added:
     - Public API changes
     - Breaking changes
     - New features
   - **Update API docs if task is API-related** (only if `apiDocs.enabled` in config):
     - New endpoint → Update openapi.yaml (or regenerate from decorators)
     - On increment close → Generate postman-collection.json from OpenAPI

   **Step D: Continue to next task**:
   - Do NOT call `/sw:sync-docs` yet (wait until all tasks complete)
   - Move to next incomplete task

**Example task execution**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK T001: Create User model (PostgreSQL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Task details:
   • File: src/models/User.ts
   • Model: ⚡ haiku (clear instructions, specific file path)
   • Description: Create User model with Prisma
   • Acceptance: Model has id, email, passwordHash, createdAt fields

⚡ Executing with Haiku (3x faster, ~$0.0025 vs $0.15 Opus)...
   ✓ Created src/models/User.ts
   ✓ Added Prisma schema definition
   ✓ Generated migration file
   ✓ Added inline documentation

✅ Task T001 completed
💰 Cost savings: $0.1475 (98% cheaper than Opus)

🔊 [Glass.aiff plays automatically via hook]
🔔 Task completed! Remember to update documentation...

🔗 Syncing to GitHub (if enabled):
   ✓ Closed task issue #43
   ✓ Checked off [T-001] in epic #42
   ✓ Posted completion comment to #43
   ✓ Updated epic #42 progress: 1/42 tasks (2%)

📝 Updating project documentation:
   ✓ Updated CLAUDE.md (added User model to schema reference)
   ✓ Updated README.md (added database section with example)
   ✓ No CHANGELOG.md update needed (internal model)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Progress: 1/42 tasks (2%) | Cost savings so far: $0.05 | Estimated remaining: 3.9 weeks

Moving to next task...
```

### Step 4: Handle Blockers

If a task cannot be completed:

1. **Document blocker**:
   - Add to tasks.md as note
   - Explain reason (missing dependency, unclear requirement, etc.)

2. **Ask user for clarification**:
   - Present blocker clearly
   - Offer solutions or alternatives
   - Wait for user decision

3. **Continue or pause**:
   - Skip to next task if blocker is non-blocking
   - Pause if blocker is critical

**Example blocker**:
```
⚠️ Blocker on Task T012: "Add email verification"

Issue: Email service provider not specified in plan.md

Options:
  A) Use SendGrid (recommended, $15/month)
  B) Use AWS SES (cheaper, $1/1000 emails)
  C) Use SMTP (self-hosted, free but complex)
  D) Skip for now, add as new task later

Your choice? [A/B/C/D]: _
```

### Step 5: Run Tests Continuously

**After completing tasks that affect testable functionality**:

1. **Run relevant tests**:
   - Unit tests for the module
   - Integration tests if applicable
   - Show pass/fail status

2. **If tests fail**:
   - Show error details
   - Fix immediately
   - Re-run tests
   - Continue only when tests pass

**Example test run**:
```
🧪 Running tests for auth module...

  ✓ User model validation
  ✓ Password hashing
  ✗ JWT token generation (FAILED)
    Expected token to expire in 24h, got 1h

🔧 Fixing test failure...
   • Updated JWT expiry config in plan.md
   • Fixed token generation in src/auth/jwt.ts

Re-running tests...

  ✓ JWT token generation

✅ All tests passing (3/3)
```

### Step 6: Progress Tracking

**Show progress regularly**:

```
📊 Increment Progress: 0001-user-authentication

Tasks completed: 15/42 (36%)
Time elapsed: 1.2 weeks
Estimated remaining: 2.1 weeks
On track: ✅ Yes

Current phase: Backend Implementation
Next phase: Frontend Integration

Recent completions:
  ✓ T012: Add email verification (2h ago)
  ✓ T013: Implement password reset (1h ago)
  ✓ T014: Add rate limiting (30m ago)

Up next:
  [ ] T015: Create login API endpoint
  [ ] T016: Add JWT middleware
```

### Step 7: Completion Check

**When all tasks marked complete**:

```
🎉 All tasks completed!

✅ Tasks: 42/42 (100%)
⏱️  Time taken: 3.2 weeks (vs estimated 3-4 weeks)

🔊 [Playing celebration sound...]

📝 Now syncing implementation learnings to living docs...
```

**CRITICAL: Now run `/sw:sync-docs update` to sync to living docs**:

```bash
/sw:sync-docs update
```

This will:
- Update ADRs with implementation details (Proposed → Accepted)
- Update API documentation with actual endpoints
- Update architecture diagrams with actual system
- Update feature lists with completed features
- May prompt for conflict resolution if needed

**After `/sw:sync-docs update` completes**:

```
✅ Living documentation synchronized!

Next steps:
1. Run full test suite: npm test
2. Validate increment: /sw:validate 0001 --quality
3. Close increment: /sw:done 0001 (PM validates before closing)
```

---

## Hook Integration (CRITICAL!)

**Post-Task Completion Hook** runs after EVERY task via `.claude/hooks.json`:

### Configuration

**File**: `.claude/hooks.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "TodoWrite",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/post-task-completion.sh"
          }
        ]
      }
    ]
  }
}
```

**Hook Script**: `.claude/hooks/post-task-completion.sh`

```bash
#!/bin/bash
# Plays completion sound and outputs reminder JSON
# Output: {"continue": true, "systemMessage": "Task completed! Update docs..."}
```

### Hook Behavior

**After EVERY task completion (via TodoWrite)**:

1. **Play sound synchronously**:
   - macOS: Glass.aiff via `afplay`
   - Linux: complete.oga via `paplay`
   - Windows: chimes.wav via PowerShell
   - Sound plays BEFORE Claude continues

2. **Show reminder**:
   - JSON systemMessage displayed to user
   - Reminds to update CLAUDE.md, README.md inline

3. **Log completion**:
   - Appends to `.specweave/logs/tasks.log`

### Documentation Updates (Manual)

After each task, Claude should manually update:

- **CLAUDE.md**: New commands, file structure, config options, skills, agents
- **README.md**: User-facing features, installation, usage, API changes
- **CHANGELOG.md**: Public API changes, breaking changes, new features

**Living docs sync** (via `/sw:sync-docs update`):
- Only after ALL tasks complete
- Updates `.specweave/docs/` with implementation learnings
- Updates ADRs from Proposed → Accepted
- Updates architecture diagrams with actual system

---

## Examples

### Example 1: Execute Complete Increment

```bash
/sw:do 0001
```

**Output**:
```
📂 Loading increment 0001-user-authentication...

✅ Context loaded (spec.md, plan.md, tasks.md, tests.md)

🔨 Starting execution (42 tasks)...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task T001: Create User model
✅ Completed | 🪝 Docs updated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[... continues for all 42 tasks ...]

🎉 All tasks completed (42/42)

Next: /sw:validate 0001 --quality
```

### Example 2: Execute with Blocker

```bash
/sw:do 0002
```

**Output**:
```
📂 Loading increment 0002-payment-processing...

🔨 Executing tasks...

Task T005: Integrate Stripe payment
⚠️ Blocker: Stripe API key not in .env

Options:
  A) Add API key now (provide test key)
  B) Skip for now, add as separate task
  C) Use mock payment provider

Your choice? [A/B/C]: _
```

### Example 3: Execute with Test Failure

```bash
/sw:do 0003
```

**Output**:
```
📂 Loading increment 0003-reporting-dashboard...

Task T008: Add CSV export
✅ Completed

🧪 Running tests...
  ✗ CSV export test failed
    Expected: 1000 rows
    Got: 999 rows (off-by-one error)

🔧 Fixing test failure...
   • Fixed loop boundary in src/reports/csv.ts

✅ Tests now passing (12/12)

🪝 Docs updated

Next task: T009
```

---

## Error Handling

### Increment Not Found
```
❌ Error: Increment 0001 not found

Available increments:
  • 0002-core-enhancements (planned)
  • 0003-payment-processing (in-progress)

Usage: /sw:do <increment-id>
```

### Increment Not Planned
```
❌ Error: Cannot execute increment 0001 (status: backlog)

Increment must be "planned" before execution.

Run: /sw:increment "User authentication" to plan this increment first.
```

### No Tasks to Execute
```
⚠️ Warning: No tasks found in tasks.md

This usually means:
  1. Tasks weren't auto-generated from plan.md
  2. Tasks.md is empty or missing

Options:
  1. Re-plan increment: /sw:increment 0001 (regenerate tasks)
  2. Add tasks manually: Edit .specweave/increments/0001-name/tasks.md
```

---

## Related Commands

- `/increment`: Plan increment (creates spec.md, plan.md, tasks.md)
- `/validate`: Validate quality before executing
- `/specweave done`: Close increment (PM validates completion)
- `/list-increments`: List all increments with status

---

## Related Skills

- `context-loader`: Loads relevant context (70% token reduction)
- `nodejs-backend`: Node.js implementation knowledge
- `python-backend`: Python implementation knowledge
- `nextjs`: Next.js implementation knowledge
- `frontend`: React/Vue/Angular implementation knowledge

---

---

## 🔐 Auto-Execute with Credentials (MANDATORY)

**When executing deployment tasks, ALWAYS follow auto-execute rules:**

### The Golden Rule

```
❌ FORBIDDEN: "Next Steps: Run wrangler deploy"
❌ FORBIDDEN: "Execute the schema in Supabase SQL Editor"
❌ FORBIDDEN: "Set secret via: wrangler secret put..."

✅ REQUIRED: Execute commands DIRECTLY using available credentials
```

### Before Any Deployment Task

```bash
# Always check for credentials FIRST (presence only - never display values!):
grep -qE "SUPABASE|DATABASE_URL|CF_|AWS_|HETZNER" .env 2>/dev/null && echo "Credentials found in .env"
wrangler whoami 2>/dev/null
aws sts get-caller-identity 2>/dev/null
gh auth status 2>/dev/null
```

### Auto-Execute Decision

| Credentials Found? | Action |
|-------------------|--------|
| ✅ Found | Execute command directly, show success message |
| ❌ Not found | ASK for credential (don't show manual steps) |

### Example: Supabase Migration Task

**If DATABASE_URL exists in .env:**
```bash
source .env
psql "$DATABASE_URL" -f src/db/schema.sql
echo "✅ Schema applied successfully"
```

**If DATABASE_URL missing:**
```markdown
🔐 **Credential Required**

I need your Supabase database URL to execute the migration.

**Please paste your DATABASE_URL:**
[I will save to .env and execute automatically]
```

See: `plugins/specweave/skills/auto-execute/SKILL.md` for full details.

---

## Why "/do" instead of "/do"?

**Universal applicability**: SpecWeave isn't just for software engineering!

- Software projects: Writing code, tests, documentation
- Writing projects: Chapters, articles, research papers
- Design projects: Mockups, prototypes, design systems
- Business projects: Reports, analyses, presentations
- Creative projects: Scripts, storyboards, content

"/do" works for any domain - it's about **executing the planned work**, whatever that work may be.

---

**Important**: This command is designed for continuous execution. It's normal to run `/sw:do` and let it execute multiple tasks sequentially with documentation updates after each one.

**Best Practice**: Always run `/sw:validate 0001 --quality` after execution to ensure quality before closing with `/sw:done`.
