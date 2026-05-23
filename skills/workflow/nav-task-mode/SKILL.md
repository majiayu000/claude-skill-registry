---
name: nav-task-mode
description: Unified workflow orchestration for substantial tasks. Auto-detects complexity, defers to matching skills, or provides phase-based execution. Solves workflow conflicts between skills, loop mode, and CLAUDE.md.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
version: 1.0.0
---

# Navigator Task Mode Skill

Unified workflow orchestration that coordinates between skills, loop mode, and direct execution based on task complexity and type.

## Why This Exists

Navigator had three disconnected workflow systems:
1. **Skills** (frontend-component, etc.) - have mini-workflows (Step 1 → Step 7)
2. **Loop Mode** - separate phase system (INIT → COMPLETE)
3. **CLAUDE.md** - documents workflow nobody enforces

**Result**: Conflicts when multiple systems try to run.

**Solution**: Task Mode acts as a coordinator - detecting when skills should handle workflow vs when to provide standalone phase guidance.

## How It Works

```
User Request
    ↓
TASK MODE (this skill)
    ├─ Simple task? → Direct execution (no overhead)
    ├─ Skill matches? → Let skill run (it has workflow)
    └─ Substantial, no skill? → Task Mode phases
```

## When to Invoke

**Auto-invoke when**:
- User starts substantial work (3+ steps expected)
- No obvious skill match (not "create component", "add endpoint", etc.)
- Request involves planning, refactoring, or multi-file changes
- Loop mode is disabled but structured execution needed

**DO NOT invoke if**:
- Trivial task (typo fix, single line change)
- Skill will clearly handle it (component creation, endpoint, migration, etc.)
- User says "quick", "just do", "simple fix"
- Already in Task Mode or Loop Mode

## Configuration

Task Mode settings in `.agent/.nav-config.json`:

```json
{
  "task_mode": {
    "enabled": true,
    "auto_detect": true,
    "defer_to_skills": true,
    "complexity_threshold": 0.5,
    "show_phase_indicator": true
  }
}
```

**Options**:
- `enabled`: Master switch for Task Mode
- `auto_detect`: Auto-detect complexity (vs explicit invocation only)
- `defer_to_skills`: Let matching skills handle their own workflow
- `complexity_threshold`: Score (0-1) required to activate
- `show_phase_indicator`: Show phase banners during execution

## Execution Steps

### Step 1: Analyze Request

**Run complexity detection**:
```bash
python3 functions/complexity_detector.py \
  --request "{USER_REQUEST}" \
  --context "{RECENT_CONTEXT}"
```

**Complexity signals**:
- Multi-file changes expected (+0.3)
- Planning language ("implement", "refactor", "add feature") (+0.2)
- Vague requirements needing research (+0.2)
- Cross-system changes (frontend+backend) (+0.3)
- Testing requirements mentioned (+0.1)

**Simple task signals**:
- Single file mentioned (-0.3)
- Fix/typo/update language (-0.2)
- Specific location given (-0.2)
- "Quick" or "simple" mentioned (-0.3)

**Decision**:
```
IF complexity_score < threshold:
  → Direct execution (exit Task Mode)
```

### Step 2: Check Skill Match

**Run skill detection**:
```bash
python3 functions/skill_detector.py \
  --request "{USER_REQUEST}" \
  --available-skills "{SKILLS_LIST}"
```

**Skill matching rules**:
- "create component" → frontend-component
- "add endpoint" → backend-endpoint
- "database migration" → database-migration
- "write test" → backend-test/frontend-test
- etc.

**Decision**:
```
IF matching_skill AND defer_to_skills:
  → Show: "Detected: {SKILL_NAME} skill will handle this"
  → Exit Task Mode (skill has workflow)
```

### Step 3: Initialize Task Mode

**If substantial task, no skill match**:

**Display activation**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK MODE ACTIVATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {TASK_SUMMARY}
Complexity: {SCORE} (threshold: {THRESHOLD})
Skills matched: None (Task Mode will orchestrate)

Phases:
  ○ RESEARCH - Understand requirements
  ○ PLAN - Create implementation strategy
  ○ IMPL - Execute changes
  ○ VERIFY - Test and validate
  ○ COMPLETE - Commit and document

Starting RESEARCH phase...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4: Execute Phases

**RESEARCH Phase**:
- Use Task agent for codebase exploration
- Identify affected files
- Find existing patterns
- Document unknowns

**Show phase transition**:
```bash
python3 functions/phase_indicator.py \
  --phase "RESEARCH" \
  --status "complete" \
  --next "PLAN"
```

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE: RESEARCH → PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Research completed:
  ✓ Found {N} related files
  ✓ Identified patterns in {LOCATION}
  ✓ Dependencies mapped

Moving to PLAN phase...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**PLAN Phase**:
- Create TodoWrite items
- Identify order of changes
- Document approach

**IMPL Phase**:
- Execute planned changes
- Follow project patterns
- Write tests as appropriate

**VERIFY Phase**:
- Run tests
- Type check
- Build validation
- **Run nav-simplify** (if enabled)

**COMPLETE Phase**:
- Commit changes
- Update documentation
- Close tickets (if PM configured)
- Suggest compact

### Step 5: Complete Task Mode

**Display completion**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK MODE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {TASK_SUMMARY}
Phases:
  ✓ RESEARCH - {DURATION}
  ✓ PLAN - {DURATION}
  ✓ IMPL - {DURATION}
  ✓ VERIFY - {DURATION}
  ✓ COMPLETE

Summary:
- {FILES_CHANGED} files changed
- {TESTS_ADDED} tests added
- Committed: {COMMIT_SHA}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Predefined Functions

### functions/complexity_detector.py

Analyzes request to determine complexity score.

**Usage**:
```bash
python3 functions/complexity_detector.py \
  --request "Refactor the auth system to use JWT" \
  --context "Working on user management"
```

**Returns**:
```json
{
  "complexity_score": 0.7,
  "signals": {
    "multi_file": true,
    "planning_language": true,
    "cross_system": false
  },
  "recommendation": "task_mode",
  "reason": "Refactoring task with multi-file scope"
}
```

### functions/skill_detector.py

Checks if a skill should handle this request.

**Usage**:
```bash
python3 functions/skill_detector.py \
  --request "Add a login component" \
  --available-skills '["frontend-component", "backend-endpoint", "database-migration"]'
```

**Returns**:
```json
{
  "matching_skill": "frontend-component",
  "confidence": 0.95,
  "triggers": ["create component", "add component"],
  "defer": true,
  "reason": "Request matches frontend-component skill triggers"
}
```

### functions/phase_indicator.py

Generates phase transition displays.

**Usage**:
```bash
python3 functions/phase_indicator.py \
  --phase "IMPL" \
  --status "in_progress" \
  --progress 60 \
  --details '{"files_changed": 3, "tests_written": 2}'
```

**Returns**: Formatted phase indicator block.

---

## Integration with Navigator

### With Loop Mode

Task Mode is **lighter weight** than Loop Mode:
- Loop Mode: Strict iteration control, stagnation detection, EXIT_SIGNAL
- Task Mode: Phase guidance, skill coordination, no strict gates

**When to use which**:
- Loop Mode: "Run until done", autonomous iteration
- Task Mode: Substantial task, need structure but not strict iteration

**Can coexist**: Loop Mode wraps Task Mode phases if both active.

### With Skills

Task Mode **defers to skills** by default:
- Skill has its own workflow (Steps 1-7)
- Task Mode doesn't add overhead
- Just shows "Skill X will handle this"

**Override**: Set `defer_to_skills: false` to always use Task Mode phases.

### With nav-simplify

Simplification runs during VERIFY phase:
- After tests pass
- Before committing
- Respects simplification.enabled config

### With Autonomous Completion

COMPLETE phase triggers autonomous protocol:
- Commit changes
- Archive documentation
- Close tickets
- Create markers

---

## Comparison Table

| Aspect | Direct Execution | Task Mode | Loop Mode |
|--------|------------------|-----------|-----------|
| Complexity | Low | Medium-High | High |
| Phase tracking | None | Visual phases | Strict phases |
| Iteration control | None | None | EXIT_SIGNAL |
| Skill coordination | None | Defers | Independent |
| Best for | Quick fixes | Features | Autonomous work |

---

## Examples

### Example 1: Simple Fix (Direct Execution)

```
User: "Fix the typo in README"

→ Complexity: 0.1 (below threshold)
→ Direct execution (no Task Mode overhead)
```

### Example 2: Component Creation (Skill Defers)

```
User: "Create a UserProfile component"

→ Complexity: 0.6
→ Skill match: frontend-component (0.95 confidence)
→ Task Mode defers: "frontend-component skill will handle this"
→ Skill executes its own Step 1-7 workflow
```

### Example 3: Refactoring (Task Mode Active)

```
User: "Refactor auth to use JWT instead of sessions"

→ Complexity: 0.8
→ Skill match: None
→ Task Mode activates
→ RESEARCH: Explore current auth implementation
→ PLAN: Document JWT migration steps
→ IMPL: Execute changes across files
→ VERIFY: Run tests, simplify code
→ COMPLETE: Commit, document
```

### Example 4: With Loop Mode

```
User: "Run until done: implement user roles"

→ Loop Mode activated (explicit trigger)
→ Task Mode phases guide each iteration:
    Iteration 1: RESEARCH phase
    Iteration 2: PLAN + IMPL phases
    Iteration 3: IMPL + VERIFY phases
    Iteration 4: COMPLETE + EXIT_SIGNAL
```

---

## Error Handling

**Config not found**:
```
Task Mode config not found in .nav-config.json.
Using defaults: auto_detect=true, threshold=0.5
```

**Skill detection fails**:
- Fall back to Task Mode (conservative)
- Log warning but continue

**Phase detection ambiguous**:
- Default to current or next logical phase
- Show reasoning for user

---

## Success Criteria

Task Mode succeeds when:
- [ ] Simple tasks execute without overhead
- [ ] Skills handle their matched requests
- [ ] Substantial tasks get phase structure
- [ ] No conflicts between systems
- [ ] User sees clear progress indicators

---

## Verification Checklist

After implementation:
- [ ] "Add login component" → frontend-component runs (not Task Mode)
- [ ] "Refactor auth system" → Task Mode runs (no matching skill)
- [ ] "Fix typo" → Direct execution (not substantial)
- [ ] Phase indicators show during Task Mode
- [ ] Skills continue working unchanged
- [ ] Loop Mode can wrap Task Mode phases

---

**This skill provides unified workflow orchestration, resolving conflicts between Navigator's multiple workflow systems.**
