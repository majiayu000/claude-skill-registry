---
name: dry-run
description: Preview command effects without making changes. Simulates file writes, git operations, agent spawns, and state changes. All reads execute normally for accurate preview. Use --dry-run flag on any command.
---

<objective>
The dry-run skill enables safe command testing by simulating all side effects without execution.

**Problem**: Commands make real changes - creating files, spawning agents, modifying state, executing git operations. Testing commands on production workflows risks unintended modifications.

**Solution**: Add `--dry-run` flag that:
1. Executes all **read** operations (for accurate analysis)
2. Simulates all **write** operations (shows what would change)
3. Previews **agent spawns** (shows what Task() calls would occur)
4. Reports **state changes** (shows YAML mutations)
5. Outputs **standardized summary** (consistent format across commands)

The result: Safe command testing with full visibility into intended effects.
</objective>

<quick_start>
<flag_detection>
**Detect --dry-run in command arguments:**

```bash
# In command process section
DRY_RUN=false
if echo "$ARGUMENTS" | grep -q -- "--dry-run"; then
  DRY_RUN=true
  # Remove flag from arguments for processing
  ARGUMENTS=$(echo "$ARGUMENTS" | sed 's/--dry-run//g' | xargs)
fi
```

**Checking in command logic:**
```markdown
If DRY_RUN is true:
  - Collect intended operations in simulation log
  - Skip actual Write/Edit tool calls
  - Skip actual Task() spawns (log them instead)
  - Skip actual Bash commands with side effects
  - Execute Read/Grep/Glob normally
  - Output dry-run summary at end
```
</flag_detection>

<simulation_output_format>
**Standard dry-run output format:**

```
════════════════════════════════════════════════════════════════════════════════
DRY-RUN MODE: No changes will be made
════════════════════════════════════════════════════════════════════════════════

📁 FILES THAT WOULD BE CREATED:
  ✚ specs/004-auth/spec.md (estimated ~150 lines)
  ✚ specs/004-auth/state.yaml (workflow state)
  ✚ specs/004-auth/NOTES.md (session notes)

📝 FILES THAT WOULD BE MODIFIED:
  ✎ specs/004-auth/state.yaml
    - phase: init → spec
    - status: pending → in_progress

🤖 AGENTS THAT WOULD BE SPAWNED:
  1. spec-phase-agent: "Execute spec phase for user authentication"
  2. clarify-phase-agent: "Clarify requirements"
  3. plan-phase-agent: "Generate implementation plan"

🔀 GIT OPERATIONS THAT WOULD OCCUR:
  • git checkout -b feature/004-auth
  • git add specs/004-auth/
  • git commit -m "feat: initialize auth feature workspace"

📊 STATE CHANGES:
  state.yaml:
    phase: spec → plan → tasks → implement
    status: pending → in_progress → completed

════════════════════════════════════════════════════════════════════════════════
DRY-RUN COMPLETE: 0 actual changes made
Run without --dry-run to execute these operations
════════════════════════════════════════════════════════════════════════════════
```
</simulation_output_format>

<immediate_value>
**Why use dry-run:**

| Scenario | Without --dry-run | With --dry-run |
|----------|-------------------|----------------|
| Testing new feature | Creates real workspace | Shows what would be created |
| Debugging workflow | May corrupt state | Safe preview of operations |
| Learning commands | Trial and error cleanup | Zero-risk exploration |
| CI/CD validation | Real side effects | Validates without changes |
| Training/demos | Need fresh environment | Repeatable demonstrations |
</immediate_value>
</quick_start>

<workflow>
<step number="1">
**Detect dry-run flag**

At command start, check for `--dry-run` in arguments:

```markdown
### Step 0: Dry-Run Detection

Check for --dry-run flag:
```bash
DRY_RUN="false"
if [[ "$ARGUMENTS" == *"--dry-run"* ]]; then
  DRY_RUN="true"
  echo "DRY-RUN MODE ENABLED"
fi
```

If DRY_RUN is true:
- Initialize simulation log array
- Proceed with analysis but skip execution
- Collect all intended operations
```

**Important**: Remove `--dry-run` from arguments before parsing other flags to avoid conflicts.
</step>

<step number="2">
**Execute reads normally**

Read operations are safe and necessary for accurate simulation:

```markdown
**Safe operations (execute normally in dry-run):**
- Read tool: `Read file_path=...`
- Grep tool: `Grep pattern=...`
- Glob tool: `Glob pattern=...`
- Bash (read-only): `ls`, `cat`, `git status`, `git log`, `test -f`
- WebFetch: Documentation/API lookups
- WebSearch: Research queries

**Why**: Accurate simulation requires understanding current state.
```
</step>

<step number="3">
**Simulate write operations**

Intercept and log write operations without executing:

```markdown
**Write operations to simulate:**

**File writes** (Write tool):
```
Instead of: Write file_path="specs/001/spec.md" content="..."
Log: "WOULD CREATE: specs/001/spec.md (~150 lines)"
```

**File edits** (Edit tool):
```
Instead of: Edit file_path="state.yaml" old_string="..." new_string="..."
Log: "WOULD MODIFY: state.yaml (phase: init → spec)"
```

**Bash writes** (Bash tool with side effects):
```
Instead of: Bash command="mkdir -p specs/001"
Log: "WOULD EXECUTE: mkdir -p specs/001"

Instead of: Bash command="git commit -m '...'"
Log: "WOULD EXECUTE: git commit -m '...'"
```
```
</step>

<step number="4">
**Simulate agent spawns**

Log Task() calls without spawning:

```markdown
**Agent spawn simulation:**

Instead of:
```
Task tool call:
  subagent_type: "spec-phase-agent"
  description: "Execute spec phase"
  prompt: "..."
```

Log:
```
WOULD SPAWN AGENT:
  Type: spec-phase-agent
  Description: Execute spec phase
  Expected outputs: spec.md, updated state.yaml
```

**Why not spawn**: Agents perform real work. Dry-run must prevent cascading side effects.
```
</step>

<step number="5">
**Track state changes**

Analyze YAML state mutations:

```markdown
**State change tracking:**

Read current state.yaml, then log intended mutations:

```yaml
# Current state
phase: init
status: pending

# After command (simulated)
phase: spec
status: in_progress
phases:
  spec: completed
```

Log as:
```
STATE CHANGES (state.yaml):
  - phase: init → spec
  - status: pending → in_progress
  - phases.spec: (new) → completed
```
```
</step>

<step number="6">
**Output standardized summary**

Format all collected operations:

```markdown
**Summary template:**

At command end, output:

1. **Header** with dry-run banner
2. **Files created** (new files that would be written)
3. **Files modified** (existing files that would change)
4. **Agents spawned** (Task() calls that would execute)
5. **Git operations** (commits, branches, pushes)
6. **State changes** (YAML mutations)
7. **Footer** with execution instructions

Use consistent emoji prefixes:
- 📁 Files created
- 📝 Files modified
- 🤖 Agents spawned
- 🔀 Git operations
- 📊 State changes
```
</step>
</workflow>

<operation_categories>
<safe_operations>
**Execute normally in dry-run mode:**

| Operation | Tool | Why Safe |
|-----------|------|----------|
| Read file | Read | No side effects |
| Search code | Grep | No side effects |
| Find files | Glob | No side effects |
| Check status | Bash (git status) | Read-only |
| View logs | Bash (git log) | Read-only |
| Test existence | Bash (test -f) | Read-only |
| List files | Bash (ls) | Read-only |
| Fetch docs | WebFetch | Read-only |
| Search web | WebSearch | Read-only |

**All reads provide accurate context for simulation.**
</safe_operations>

<simulated_operations>
**Simulate (log but don't execute) in dry-run mode:**

| Operation | Tool | Simulation Output |
|-----------|------|-------------------|
| Create file | Write | "WOULD CREATE: path (~N lines)" |
| Edit file | Edit | "WOULD MODIFY: path (old → new)" |
| Make directory | Bash (mkdir) | "WOULD EXECUTE: mkdir ..." |
| Git commit | Bash (git commit) | "WOULD EXECUTE: git commit ..." |
| Git branch | Bash (git checkout -b) | "WOULD EXECUTE: git checkout -b ..." |
| Git push | Bash (git push) | "WOULD EXECUTE: git push ..." |
| Run script | Bash (python/node) | "WOULD EXECUTE: python ..." |
| Spawn agent | Task | "WOULD SPAWN: agent-type" |
| Ask user | AskUserQuestion | "WOULD ASK: question text" |

**All writes are logged with expected effects.**
</simulated_operations>

<hybrid_operations>
**Execute carefully in dry-run mode:**

| Operation | Approach |
|-----------|----------|
| State validation | Run validation, report errors |
| Prerequisite checks | Execute checks, report status |
| File existence checks | Execute, use result for simulation |
| Git status queries | Execute, use for accurate preview |

**Some operations need execution for accurate simulation while being side-effect-free.**
</hybrid_operations>
</operation_categories>

<command_integration>
<pattern>
**Standard pattern for command integration:**

Add to command frontmatter:
```yaml
---
argument-hint: "[args] [--dry-run]"
---
```

Add to command process section:

```markdown
### Step 0: Mode Detection

**Detect dry-run mode:**
```bash
DRY_RUN="false"
CLEAN_ARGS="$ARGUMENTS"
if [[ "$ARGUMENTS" == *"--dry-run"* ]]; then
  DRY_RUN="true"
  CLEAN_ARGS=$(echo "$ARGUMENTS" | sed 's/--dry-run//g' | xargs)
  echo "═══════════════════════════════════════════════════════════════════"
  echo "DRY-RUN MODE: No changes will be made"
  echo "═══════════════════════════════════════════════════════════════════"
fi
```

**Initialize simulation log (if dry-run):**
If DRY_RUN is true, initialize arrays:
- FILES_CREATED=()
- FILES_MODIFIED=()
- AGENTS_SPAWNED=()
- GIT_OPERATIONS=()
- STATE_CHANGES=()
```

Add before each operation:
```markdown
If DRY_RUN is true:
  Log operation to appropriate array
  Skip execution
Else:
  Execute operation normally
```

Add at command end:
```markdown
### Final Step: Dry-Run Summary (if applicable)

If DRY_RUN is true:
  Output dry-run summary using format from skill
  Exit without actual changes
```
</pattern>

<example_integration>
**Example: /feature command integration:**

```markdown
### Step 0: Mode Detection

**Detect flags:**
```bash
DRY_RUN="false"
DEEP_MODE="false"
CLEAN_ARGS="$ARGUMENTS"

if [[ "$ARGUMENTS" == *"--dry-run"* ]]; then
  DRY_RUN="true"
  CLEAN_ARGS=$(echo "$CLEAN_ARGS" | sed 's/--dry-run//g')
fi

if [[ "$ARGUMENTS" == *"--deep"* ]]; then
  DEEP_MODE="true"
  CLEAN_ARGS=$(echo "$CLEAN_ARGS" | sed 's/--deep//g')
fi

CLEAN_ARGS=$(echo "$CLEAN_ARGS" | xargs)  # Trim whitespace
```

### Step 1.1: Initialize Feature Workspace

If DRY_RUN is true:
  ```
  Log: "WOULD CREATE: specs/NNN-feature-slug/state.yaml"
  Log: "WOULD CREATE: specs/NNN-feature-slug/NOTES.md"
  Log: "WOULD EXECUTE: python .spec-flow/scripts/spec-cli.py feature '...'"
  ```
  Skip actual execution
Else:
  Execute normally
```
</example_integration>
</command_integration>

<examples>
<example name="feature-dry-run">
**Input**: `/feature "add user dashboard" --dry-run`

**Output**:
```
════════════════════════════════════════════════════════════════════════════════
DRY-RUN MODE: No changes will be made
════════════════════════════════════════════════════════════════════════════════

📁 FILES THAT WOULD BE CREATED:
  ✚ specs/005-add-user-dashboard/state.yaml
  ✚ specs/005-add-user-dashboard/NOTES.md
  ✚ specs/005-add-user-dashboard/interaction-state.yaml
  ✚ specs/005-add-user-dashboard/domain-memory.yaml
  ✚ specs/005-add-user-dashboard/spec.md (after spec-phase-agent)
  ✚ specs/005-add-user-dashboard/plan.md (after plan-phase-agent)
  ✚ specs/005-add-user-dashboard/tasks.md (after tasks-phase-agent)

🤖 AGENTS THAT WOULD BE SPAWNED:
  1. initializer → Initialize domain memory for feature
  2. spec-phase-agent → Generate specification
  3. clarify-phase-agent → Resolve ambiguities
  4. plan-phase-agent → Create implementation plan
  5. tasks-phase-agent → Break down into TDD tasks
  6. worker (N times) → Implement each feature atomically
  7. optimize-phase-agent → Run quality gates
  8. ship-staging-phase-agent → Deploy to staging
  9. finalize-phase-agent → Archive and document

🔀 GIT OPERATIONS THAT WOULD OCCUR:
  • git checkout -b feature/005-add-user-dashboard
  • git add specs/005-add-user-dashboard/
  • git commit (multiple, after each phase)
  • git push origin feature/005-add-user-dashboard

📊 WORKFLOW PHASES:
  init → spec → clarify → plan → tasks → implement → optimize → ship → finalize

════════════════════════════════════════════════════════════════════════════════
DRY-RUN COMPLETE: 0 actual changes made
Run `/feature "add user dashboard"` to execute these operations
════════════════════════════════════════════════════════════════════════════════
```
</example>

<example name="implement-dry-run">
**Input**: `/implement --dry-run`

**Output**:
```
════════════════════════════════════════════════════════════════════════════════
DRY-RUN MODE: No changes will be made
════════════════════════════════════════════════════════════════════════════════

📋 CURRENT STATE:
  Feature: specs/004-auth-system/
  Phase: implement
  Tasks remaining: 8 of 12

📝 FILES THAT WOULD BE MODIFIED:
  ✎ specs/004-auth-system/domain-memory.yaml
    - features[F001].status: pending → completed
    - features[F002].status: pending → in_progress
  ✎ specs/004-auth-system/state.yaml
    - phase: implement (unchanged during execution)
  ✎ src/services/auth.ts (implementation)
  ✎ src/services/auth.test.ts (tests)
  ✎ src/routes/login.ts (implementation)
  ✎ src/routes/login.test.ts (tests)

🤖 AGENTS THAT WOULD BE SPAWNED:
  1. worker → Implement F001: User login endpoint
  2. worker → Implement F002: Session management
  3. worker → Implement F003: Password validation
  4. worker → Implement F004: Token refresh
  (... 4 more workers for remaining features)

🔄 TDD CYCLE PER TASK:
  For each worker:
    1. Write failing tests
    2. Implement feature
    3. Verify tests pass
    4. Update domain-memory.yaml
    5. Commit changes

════════════════════════════════════════════════════════════════════════════════
DRY-RUN COMPLETE: 0 actual changes made
Run `/implement` to execute 8 remaining tasks
════════════════════════════════════════════════════════════════════════════════
```
</example>

<example name="ship-dry-run">
**Input**: `/ship --staging --dry-run`

**Output**:
```
════════════════════════════════════════════════════════════════════════════════
DRY-RUN MODE: No changes will be made
════════════════════════════════════════════════════════════════════════════════

📋 PRE-FLIGHT CHECKS (would execute):
  ✓ Build verification
  ✓ Test suite (127 tests)
  ✓ Type checking
  ✓ Security scan
  ✓ Environment variables

🔀 GIT OPERATIONS THAT WOULD OCCUR:
  • git push origin feature/004-auth-system
  • gh pr create --base staging --head feature/004-auth-system
  • Wait for CI to pass
  • gh pr merge --auto

📦 DEPLOYMENT THAT WOULD OCCUR:
  • Merge to staging branch triggers deploy-staging.yml
  • Vercel/Railway builds from staging
  • Health check endpoints verified
  • Deployment URL: https://staging.example.com (estimated)

📊 STATE CHANGES:
  state.yaml:
    - phases.ship: pending → completed
    - deployment.staging.status: pending → deployed
    - deployment.staging.pr_number: (new) → #42

🤖 AGENTS THAT WOULD BE SPAWNED:
  1. ship-staging-phase-agent → Execute staging deployment

════════════════════════════════════════════════════════════════════════════════
DRY-RUN COMPLETE: 0 actual changes made
Run `/ship --staging` to deploy to staging environment
════════════════════════════════════════════════════════════════════════════════
```
</example>

<example name="quick-dry-run">
**Input**: `/quick "fix typo in README" --dry-run`

**Output**:
```
════════════════════════════════════════════════════════════════════════════════
DRY-RUN MODE: No changes will be made
════════════════════════════════════════════════════════════════════════════════

📋 TASK ANALYSIS:
  Type: Documentation fix
  Scope: Single file
  Estimated changes: <10 lines

📝 FILES THAT WOULD BE MODIFIED:
  ✎ README.md (typo fix)

🔀 GIT OPERATIONS THAT WOULD OCCUR:
  • git add README.md
  • git commit -m "docs: fix typo in README"

🤖 AGENTS THAT WOULD BE SPAWNED:
  1. quick-worker → Execute atomic change with tests

════════════════════════════════════════════════════════════════════════════════
DRY-RUN COMPLETE: 0 actual changes made
Run `/quick "fix typo in README"` to execute
════════════════════════════════════════════════════════════════════════════════
```
</example>
</examples>

<anti_patterns>
<anti_pattern name="executing-writes-in-dry-run">
**Problem**: Accidentally executing write operations in dry-run mode

**Bad approach**:
```markdown
If DRY_RUN:
  echo "Would write file"
Write file...  # WRONG: Executes regardless of dry-run!
```

**Correct approach**:
```markdown
If DRY_RUN:
  Log: "WOULD CREATE: file.md"
Else:
  Write file_path="file.md" content="..."
```

**Rule**: Always wrap write operations in dry-run conditional.
</anti_pattern>

<anti_pattern name="spawning-agents-in-dry-run">
**Problem**: Spawning Task() agents defeats dry-run purpose

**Bad approach**:
```markdown
If DRY_RUN:
  echo "Would spawn agent"
Task(spec-phase-agent)  # WRONG: Agent runs and makes changes!
```

**Correct approach**:
```markdown
If DRY_RUN:
  Log: "WOULD SPAWN: spec-phase-agent"
  Log: "Expected outputs: spec.md"
Else:
  Task(spec-phase-agent)
```

**Rule**: Never spawn agents in dry-run mode.
</anti_pattern>

<anti_pattern name="incomplete-simulation">
**Problem**: Missing operations from dry-run output

**Bad approach**:
```markdown
DRY-RUN OUTPUT:
  Would create spec.md
  # Missing: state.yaml changes, git operations, other files
```

**Correct approach**:
```markdown
DRY-RUN OUTPUT:
  FILES CREATED: spec.md, state.yaml, NOTES.md
  FILES MODIFIED: state.yaml (phase: init → spec)
  GIT OPERATIONS: checkout -b, add, commit
  AGENTS: spec-phase-agent, clarify-phase-agent
```

**Rule**: Log ALL operations that would occur.
</anti_pattern>

<anti_pattern name="skipping-necessary-reads">
**Problem**: Skipping reads makes simulation inaccurate

**Bad approach**:
```markdown
If DRY_RUN:
  Skip reading state.yaml  # WRONG: Can't accurately simulate!
  Guess at current state
```

**Correct approach**:
```markdown
# Always read current state (safe operation)
STATE=$(cat specs/NNN/state.yaml)
CURRENT_PHASE=$(yq eval '.phase' ...)

If DRY_RUN:
  Log: "Current phase: $CURRENT_PHASE → would transition to: spec"
```

**Rule**: Execute reads for accurate simulation context.
</anti_pattern>
</anti_patterns>

<validation>
<success_indicators>
Dry-run implementation is correct when:

1. **Zero side effects**: No files created/modified, no git operations, no agents spawned
2. **Accurate preview**: All intended operations listed in output
3. **Consistent format**: Standard output format across all commands
4. **Readable output**: Clear emoji prefixes, organized sections
5. **Actionable**: Output tells user how to execute for real
6. **Complete**: Shows files, agents, git ops, state changes
</success_indicators>

<validation_checklist>
Before considering dry-run implementation complete:

- [ ] --dry-run flag detected and removed from arguments
- [ ] All Write tool calls wrapped in dry-run conditional
- [ ] All Edit tool calls wrapped in dry-run conditional
- [ ] All Task() calls wrapped in dry-run conditional
- [ ] All Bash writes (mkdir, git commit, etc.) wrapped
- [ ] Read operations execute normally for context
- [ ] Output uses standard format with emoji prefixes
- [ ] Output includes all operation categories
- [ ] Output shows how to run without dry-run
- [ ] No actual changes occur in dry-run mode
</validation_checklist>
</validation>

<commands_supporting_dry_run>
**Commands that support --dry-run flag:**

| Command | Dry-run shows |
|---------|---------------|
| `/feature` | Workspace creation, all phases, agents |
| `/epic` | Epic workspace, sprint planning, parallel execution |
| `/quick` | Quick fix changes, commit |
| `/plan` | Plan.md creation, research |
| `/tasks` | Tasks.md generation |
| `/implement` | Worker spawns, file changes, tests |
| `/optimize` | Quality gate execution, reports |
| `/ship` | Deployment operations, PR creation |
| `/finalize` | Archival, cleanup, documentation |

**Usage**: Add `--dry-run` to any command:
```bash
/feature "add auth" --dry-run
/implement --dry-run
/ship --staging --dry-run
```
</commands_supporting_dry_run>

<success_criteria>
The dry-run skill is successfully applied when:

1. **Flag detection**: `--dry-run` recognized by command
2. **Zero execution**: No files created, modified, or deleted
3. **No agents spawned**: Task() calls logged but not executed
4. **No git changes**: No commits, branches, or pushes
5. **Accurate preview**: All operations that WOULD occur are listed
6. **Standard format**: Consistent output format with clear sections
7. **Actionable output**: User knows how to run command for real
8. **Safe exploration**: Users can test any command without risk
9. **CI/CD ready**: Can validate commands in automation pipelines
10. **Repeatable**: Same dry-run produces same output (deterministic)
</success_criteria>
