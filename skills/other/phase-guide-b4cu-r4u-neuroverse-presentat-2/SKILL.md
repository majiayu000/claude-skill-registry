---
name: Pipeline Phase Guide
description: Intelligently navigate the 7-phase Spec Kit → CCGC workflow by detecting current phase, validating prerequisites, recommending transitions, and tracking per-project state. Use when the user asks "what phase", "what's next", "workflow steps", "guide me through pipeline", or phase keywords like "specify", "plan", "tasks", "implement", "validate", "sync". Essential for multi-project developers maintaining context across different features and codebases simultaneously.
allowed-tools: Read, Write, Glob, Bash
---

# Pipeline Phase Guide

## Purpose

This Skill provides intelligent navigation through your **7-phase Spec Kit + CCGC pipeline**:

```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → (repeat)
        PLANNING PHASES              IMPLEMENTATION PHASES
   └─────────────────────────────────────────────────────┘
          Spec Kit (what/how)        CCGC (build/validate)
```

**Key Problem Solved**: Maintains context across multiple projects with different phases, preventing confusion about "which feature is at which phase?"

---

## The 7-Phase Pipeline Explained

### Phase 0: **Undefined** (No Feature Active)
- **When**: Starting new feature or completed previous feature
- **Files**: None yet
- **Next**: Create specification
- **Slash Command**: `/specify "feature description"`
- **Time**: Variable

### Phase 1: **Specification** (What to Build?)
- **When**: User has written feature specification
- **Files**: `specs/###-feature-name/spec.md` exists
- **Output**: Feature ID, scope, requirements, success criteria
- **Next**: Design the implementation
- **Slash Command**: `/plan`
- **Time**: 1-2 hours

### Phase 2: **Planning** (How to Design?)
- **When**: Design decisions made, architecture defined
- **Files**: `plan.md` created, auto-synced to `memory/architecture.md`
- **Output**: Technical approach, file structure, data model, API contracts
- **Next**: Break down into tasks
- **Slash Command**: `/tasks`
- **Time**: 2-4 hours

### Phase 3: **Task Breakdown** (What's the Work?)
- **When**: Tasks generated and ready for implementation
- **Files**: `tasks.md` created, auto-synced to `memory/tasks_plan.md`
- **Output**: TDD-ordered tasks, dependencies, time estimates
- **Next**: Start implementation
- **Slash Command**: `@agent-implementer` or say "ready to code"
- **Time**: 30 minutes

### Phase 4: **Implementation** (Build It!)
- **When**: Tasks being executed, code being written
- **Files**: Source code files modified, tests created
- **Output**: New feature, tests passing
- **Next**: Run validation suite
- **Slash Command**: `/test-run`, `/standards-check`
- **Time**: 4-8 hours (depends on feature)

### Phase 5: **Validation** (Did We Get It Right?)
- **When**: Code complete, tests passing, standards checked
- **Files**: All tests passing, no PHPStan/ESLint errors
- **Output**: Validated implementation, ready for deployment
- **Next**: Capture learnings
- **Slash Command**: `/memory-sync`
- **Time**: 1-2 hours

### Phase 6: **Learning & Completion** (What Did We Learn?)
- **When**: Memory synced, feature complete
- **Files**: `lessons-learned.md` updated, `error-documentation.md` updated
- **Output**: Team insights, documented patterns
- **Next**: Create PR or start new feature
- **Action**: Merge to main or create PR
- **Time**: 30 minutes

---

## How It Works

### Automatic Phase Detection

The Skill determines current phase by checking file existence:

```bash
Check sequence:
1. Does specs/###-feature-name/spec.md exist?
   NO  → Phase 0 (Undefined)
   YES → Continue

2. Does plan.md exist in spec directory?
   NO  → Phase 1 (Specification complete, planning needed)
   YES → Continue

3. Does tasks.md exist?
   NO  → Phase 2 (Planning complete, tasks needed)
   YES → Continue

4. Are there incomplete tasks in tasks_plan.md?
   YES → Phase 4 (Implementation in progress)
   NO  → Check tests

5. Are tests passing?
   NO  → Phase 4 (Still implementing)
   YES → Phase 5 (Validation phase)

6. Is memory synced?
   NO  → Phase 5 (Validation, need sync)
   YES → Phase 6 (Complete)
```

### Phase-Specific Guidance

For each phase, the Skill provides:

1. **Current State**: What's been completed
2. **Next Action**: Specific next step (slash command or user action)
3. **Prerequisites**: What must be done first
4. **Estimated Time**: How long this phase typically takes
5. **Warnings**: Any blockers or issues

### Transition Validation (Enhanced v2.0.0)

Before recommending transition to next phase, Skill validates:

**Phase 0 → 1 (Start Specification)**:
- [ ] Git repo clean
- [ ] No conflicting features in progress
- [ ] Constitution ratified (optional, NEW v2.0.0)

**Phase 1 → 2 (Start Planning)**:
- [ ] Spec complete (no `[NEEDS CLARIFICATION]` markers)
- [ ] Stakeholder approval obtained
- [ ] Requirements clear and achievable
- [ ] **Quality Gate 1 - Clarity Gate** (NEW v2.0.0):
  - [ ] Requirements unambiguous
  - [ ] Success criteria measurable
  - [ ] Scope well-defined

**Phase 2 → 3 (Start Task Breakdown)**:
- [ ] Plan has Constitution Check completed (if constitution exists)
- [ ] Technical approach finalized
- [ ] No outstanding questions
- [ ] **Quality Gate 2 - Testability Gate** (NEW v2.0.0):
  - [ ] Test strategy defined
  - [ ] Test framework selected
  - [ ] TDD approach documented
- [ ] **Quality Gate 3 - Boundary Gate** (NEW v2.0.0):
  - [ ] Architectural boundaries defined
  - [ ] Component interfaces specified
  - [ ] No circular dependencies

**Phase 3 → 4 (Start Implementation)**:
- [ ] Memory context loaded (`/memory-read` run)
- [ ] No conflicting changes on main branch
- [ ] Development environment ready
- [ ] Tests written (TDD requirement, NEW v2.0.0)
- [ ] Plugins loaded (if project uses plugins, NEW v2.0.0)
- [ ] Validators warmed (if plugins exist, NEW v2.0.0)

**Phase 4 → 5 (Start Validation)**:
- [ ] All tasks completed
- [ ] All tests passing
- [ ] Code standards passing (linter/formatter)
- [ ] No uncommitted changes
- [ ] **Quality Gate 4 - Coverage Gate** (NEW v2.0.0):
  - [ ] Test coverage >80%
  - [ ] Critical paths covered
  - [ ] Edge cases tested
- [ ] **Quality Gate 5 - Security Gate** (NEW v2.0.0):
  - [ ] No SQL injection risks
  - [ ] No hardcoded secrets
  - [ ] Input validation implemented

**Phase 5 → 6 (Start Learning)**:
- [ ] Tests passing (confirmed)
- [ ] Performance targets met
- [ ] Documentation complete
- [ ] Ready for memory sync
- [ ] **Quality Gate 6 - Maintainability Gate** (NEW v2.0.0):
  - [ ] Code reviewed (self or peer)
  - [ ] Complex logic documented
  - [ ] Technical debt minimized

**Phase 6 → 0 (Complete Feature)**:
- [ ] PR merged or changes committed
- [ ] Memory synced
- [ ] Lessons documented
- [ ] **Quality Gate 7 - Documentation Gate** (NEW v2.0.0):
  - [ ] Lessons learned captured
  - [ ] Patterns documented
  - [ ] Known issues recorded

---

## Examples

### Example 1: Initial Feature Discovery

**User Input**: "What phases do I need to go through?"

**Skill Output**:
```
🧭 SPEC KIT + CCGC PIPELINE (7 Phases)
════════════════════════════════════════════════════════════════

┌─ PLANNING (Spec Kit - Upstream) ─┐
│                                   │
│  Phase 1: SPECIFICATION           │
│  └─ Create spec.md with feature   │
│     requirements, scope, success  │
│     criteria                       │
│                                   │
│  Phase 2: PLANNING                │
│  └─ Design implementation         │
│     approach, file structure,     │
│     data model, API contracts     │
│                                   │
│  Phase 3: TASK BREAKDOWN          │
│  └─ Break design into tasks       │
│     (TDD-ordered, estimated)      │
│                                   │
└─ IMPLEMENTATION CHECKPOINT ────────┘
              ↓
┌─ IMPLEMENTATION (CCGC - Downstream) ┐
│                                      │
│  Phase 4: IMPLEMENTATION             │
│  └─ Execute tasks, write code,       │
│     tests before implementation      │
│                                      │
│  Phase 5: VALIDATION                 │
│  └─ Run tests, standards checks,     │
│     verify performance               │
│                                      │
│  Phase 6: LEARNING                   │
│  └─ Capture insights,                │
│     documented patterns,             │
│     sync memory                      │
│                                      │
└─ COMPLETION CHECKPOINT ──────────────┘
              ↓
      Start next feature (Phase 0)

🎯 EACH PHASE INCLUDES:
   - Specific slash commands to execute
   - Files created as outputs
   - Quality gates to pass
   - Estimated time

💡 QUICK START:
   New feature? → /specify "description"
   Have spec? → /plan
   Have plan? → /tasks
   Ready to code? → "ready to code" (quick-start Skill)
════════════════════════════════════════════════════════════════
```

---

### Example 2: Multi-Project Phase Tracking

**User Input**: "What phases are my projects in?"

**Skill Output**:
```
🧭 MULTI-PROJECT PHASE STATUS
════════════════════════════════════════════════════════════════

Project 1: /Users/dev/dev_IECPN
├─ Current Phase: 4 - IMPLEMENTATION (Active)
├─ Feature: #006 - PHI Logging Cleanup
├─ Progress: 0/26 tasks complete
├─ Next: @agent-implementer
└─ Status: Ready to start

Project 2: /Users/dev/api-refactor
├─ Current Phase: 2 - PLANNING (Active)
├─ Feature: #012 - API Gateway
├─ Progress: plan.md created, no tasks
├─ Next: /tasks to generate breakdown
└─ Status: Planning phase complete

Project 3: /Users/dev/ml-pipeline
├─ Current Phase: 1 - SPECIFICATION (Paused)
├─ Feature: #008 - ML Model Pipeline
├─ Progress: spec.md created
├─ Next: /plan to design approach
└─ Status: Waiting for planning

💡 NEXT ACTIONS BY PROJECT:
   dev_IECPN → Start: @agent-implementer (immediate)
   api-refactor → Run: /tasks (before next work)
   ml-pipeline → Continue: /plan (when ready)
════════════════════════════════════════════════════════════════
```

---

### Example 3: Guided Phase Transition with Quality Gates (NEW v2.0.0)

**User Input**: "I'm ready to move from planning to implementation"

**Skill Output**:
```
🧭 PHASE TRANSITION: Planning → Implementation (v2.0.0)
════════════════════════════════════════════════════════════════

Current: Phase 2 - PLANNING
Target: Phase 3-4 - TASK BREAKDOWN → IMPLEMENTATION

✅ Prerequisites Validation:
   [✓] Plan created (plan.md exists)
   [✓] Technical approach finalized
   [✓] No outstanding questions
   [✓] Git working tree clean

⚖️  QUALITY GATES VALIDATION (NEW v2.0.0):
   Constitution: Found (7 principles, 7 gates)

   Gate 2 - Testability Gate:
   [✓] Test strategy defined (TDD with pytest)
   [✓] Test framework documented in plan.md
   [✓] Test-first approach specified in tasks
   Status: ✅ PASSED

   Gate 3 - Boundary Gate:
   [✓] Architectural boundaries defined
   [✓] Component interfaces specified in architecture.md
   [✓] No circular dependencies detected
   Status: ✅ PASSED

   Overall: 2/2 gates passed for this transition
   Status: ✅ CLEAR TO PROCEED

🎯 REQUIRED NEXT STEP:
   Generate task breakdown: /tasks

   This will:
   1. Parse plan.md for implementation approach
   2. Generate TDD-ordered task list
   3. Estimate effort per task
   4. Validate against quality gates
   5. Create tasks.md in specs/###-feature/
   6. Auto-sync to memory/tasks_plan.md

⏱️  Estimated: 5-10 minutes

🎯 AFTER /tasks COMPLETES:
   Say: "ready to code"
   This will activate quick-start Skill to:
   1. Load full development context
   2. Validate phase and prerequisites
   3. Run constitutional pre-flight checks
   4. Load project plugins (if any)
   5. Warm validator cache
   6. Present next task
   7. Confirm readiness
   8. Guide to @agent-implementer

📊 TYPICAL FLOW (v2.0.0):
   /plan → (create plan.md)
   /constitution-check → (validate against gates) [if constitution exists]
   /tasks → (create tasks.md with quality gate validation)
   "ready to code" → (quick-start with plugin loading)
   @agent-implementer → (execute tasks)

Ready to proceed?
```

**With Quality Gate Failure**:
```
🧭 PHASE TRANSITION: Planning → Implementation
════════════════════════════════════════════════════════════════

❌ TRANSITION BLOCKED

⚖️  QUALITY GATES VALIDATION:
   Gate 2 - Testability Gate:
   [✓] Test strategy defined
   [❌] Test framework NOT documented
   [❌] TDD approach missing from plan
   Status: ❌ FAILED

   Gate 3 - Boundary Gate:
   [✓] Architectural boundaries defined
   [⚠️] Component interfaces partially specified
   [✓] No circular dependencies
   Status: ⚠️ WARNING

   Overall: 0/2 gates passed, 1 warning
   Status: ❌ CANNOT PROCEED

🎯 REQUIRED ACTIONS:
   1. Update plan.md with:
      - Test framework selection (pytest/jest/etc)
      - TDD approach documentation
      - Test-first task ordering

   2. Fix warnings:
      - Complete component interface specifications
      - Document API contracts in architecture.md

   3. Re-run: "ready to move from planning to implementation"
      to re-validate quality gates

⏱️  Estimated fix time: 15-20 minutes

📚 REFERENCE:
   Constitution: .specify/memory/constitution.md
   Principles: II (Testability), III (Boundary Respect)
   Quality Gate Docs: Check principle requirements

Cannot proceed until gates pass.
```

---

### Example 4: Phase Mismatch Detection

**User Input**: "Start coding" (but actually in planning phase)

**Skill Output**:
```
⚠️  PHASE MISMATCH

Current State:
├─ Phase: 2 - PLANNING
├─ Feature: #012 - API Gateway
└─ Issue: Can't implement without task breakdown

What's Been Done:
✓ Specification (spec.md)
✓ Planning (plan.md)

What's Missing:
❌ Task Breakdown (tasks.md)

🎯 REQUIRED STEP:
   Run: /tasks

   This generates:
   - TDD-ordered task list
   - Effort estimates
   - Dependency information
   - Parallel opportunities

⏱️  Time: ~5 minutes

After /tasks:
   Then: "ready to code" → Implementation

Can't skip this step because:
   - @agent-implementer requires tasks.md
   - No tasks = no execution plan
   - Task breakdown is critical quality gate

Proceed?
```

---

## Cross-Project State Management

### State Tracking File

Location: `~/.claude/skills/phase-guide/state.json`

**Purpose**: Remember phase for each project

**Format**:
```json
{
  "projects": {
    "/Users/dev/dev_IECPN": {
      "currentPhase": 4,
      "featureId": "006",
      "featureName": "PHI Logging Cleanup",
      "branch": "006-feature-006-logging",
      "lastUpdate": "2025-10-17T10:30:00Z",
      "contextFreshness": "current",
      "lastAction": "@agent-implementer started"
    },
    "/Users/dev/api-refactor": {
      "currentPhase": 2,
      "featureId": "012",
      "featureName": "API Gateway",
      "branch": "012-api-gateway",
      "lastUpdate": "2025-10-16T14:15:00Z",
      "contextFreshness": "stale",
      "lastAction": "/plan completed"
    }
  },
  "lastActiveProject": "/Users/dev/dev_IECPN",
  "lastSync": "2025-10-17T10:30:00Z"
}
```

### Auto-Update Mechanism

State file updates when:
1. Phase transition detected
2. New feature started
3. User switches projects
4. Memory sync occurs
5. Major milestone reached

### Multi-Project Context Switching

**Scenario**: User switches from Project A to Project B

**Skill Behavior**:
1. Detects new project (different directory)
2. Looks up Project B state in state.json
3. Reports previous phase for Project B
4. Shows tasks left off at
5. Guides resumption

---

## Integration with Other Skills

**Relationship to context-navigator**:
- `context-navigator`: "Where am I?" (current snapshot)
- `phase-guide`: "What's next?" (workflow guidance)
- Flow: See state → Understand phase → Navigate transitions

**Relationship to quick-start**:
- `phase-guide`: Detects if you're in right phase for coding
- `quick-start`: Validates and loads context
- Flow: phase-guide says "ready", quick-start confirms "READY"

**Relationship to memory-keeper**:
- `phase-guide`: Tracks phase transitions
- `memory-keeper`: Keeps memory fresh during phase
- Flow: Transition occurs → memory-keeper keeps data current

---

## Troubleshooting

**Issue**: Skill says you're in Phase 1 but you know tasks exist

**Cause**: tasks.md might be in wrong location

**Check**:
```bash
find . -name "tasks.md" -type f
# Should find: specs/###-feature-name/tasks.md
```

**Fix**: Verify tasks.md is in correct location

---

**Issue**: State.json shows wrong phase for a project

**Cause**: Phase detection failed or state not synced

**Fix**: Say "sync state" to force re-detect and update

---

## Performance

This Skill performs:
- Phase detection (file checks)
- State file reads/writes
- Cross-project tracking
- Quality gate validation (NEW v2.0.0)
- Constitution parsing (NEW v2.0.0)

**Expected execution time**: <300ms (with constitution and quality gates)
**Expected execution time**: <200ms (v1.0.0 mode, no constitution)
**Side effects**: Updates state.json (intentional)

---

## Graceful Degradation (NEW v2.0.0)

This skill is **backward compatible** and works without v2.0.0 features:

**Without Constitution** (v1.0.0 mode):
```
⚖️  QUALITY GATES VALIDATION
   Constitution: Not ratified
   Quality Gates: Skipped (v1.0.0 compatibility)
   Status: ✅ Proceeding without constitutional governance
```
- All phase transitions work normally
- Prerequisites checked as in v1.0.0
- No quality gate validation

**Without Quality Gate Cache**:
- Reads constitution directly (slower by ~50ms)
- Parses principles on-demand
- No functional differences

**Partial Quality Gate Failures**:
- Shows which gates passed/failed
- Provides specific remediation steps
- Blocks transition only if CRITICAL gates fail
- WARN/MEDIUM gates show warnings but allow proceed

**Missing v2.0.0 Directories**:
```
No .claude/cache/principle-registry.json → Parse constitution directly
No .specify/memory/constitution.md → Skip quality gates, v1.0.0 mode
```

**Multi-Project State Handling**:
- Works with or without state.json
- Falls back to file-based detection if state missing
- Creates state.json on first use

This ensures:
1. Smooth v1.0.0 → v2.0.0 migration
2. Works without constitution
3. Quality gates optional, not required
4. No breaking changes

---

## What This Skill Does NOT Do

- ❌ Does NOT execute tasks (use `@agent-implementer`)
- ❌ Does NOT run /memory-sync (use memory-keeper Skill or `/memory-sync`)
- ❌ Does NOT modify code (read-only diagnostic)
- ❌ Does NOT make decisions for you (guidance only)
- ❌ Does NOT enforce quality gates (only validates and warns) (NEW v2.0.0)
- ❌ Does NOT fix constitutional violations (provides remediation guidance)

This Skill navigates workflow. Slash commands and agents execute the work.
