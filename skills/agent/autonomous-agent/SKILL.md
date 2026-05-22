<input_guardrails>

## Pre-Execution Validation

Before main skill execution, perform guardrail checks.

### Step 1: Check Configuration

Read `.loa.config.yaml`:

```yaml
guardrails:
  input:
    enabled: true|false
```

**Exit Conditions**:

- `guardrails.input.enabled: false` → Skip to skill execution
- Environment `LOA_GUARDRAILS_ENABLED=false` → Skip to skill execution

### Step 2: Run Danger Level Check

**Script**: `.claude/scripts/danger-level-enforcer.sh --skill autonomous-agent --mode {mode}`

**CRITICAL**: This is a **high** danger level skill (full orchestration control).

| Mode        | Behavior                                      |
| ----------- | --------------------------------------------- |
| Interactive | Require explicit confirmation with reason     |
| Autonomous  | BLOCK (high-risk skill requires --allow-high) |

**Note**: The autonomous-agent skill is classified as `high` rather than `critical`
because it operates through other skills that have their own guardrails.
The orchestrator itself doesn't directly execute dangerous operations.

### Step 3: Run PII Filter

**Script**: `.claude/scripts/pii-filter.sh`

Detect and redact sensitive data before orchestration begins.
Important for multi-phase execution where data flows between skills.

### Step 4: Run Injection Detection

**Script**: `.claude/scripts/injection-detect.sh --threshold 0.65`

**Lower threshold** (0.65 vs default 0.7) because autonomous orchestration
has higher impact potential. More conservative detection.

### Step 5: Log to Trajectory

Write to `grimoires/loa/a2a/trajectory/guardrails-{date}.jsonl`.

### Error Handling

On error: Log to trajectory, **fail-open** (continue to skill).
</input_guardrails>

# Autonomous Agent Orchestrator

<objective>
Execute autonomous work with exhaustive Loa process compliance, mandatory quality gates, self-auditing, remediation loops, and continuous improvement. Match human-level discernment and quality on every deliverable.
</objective>

<issue_integrations>

## Issue Integrations

This skill incorporates solutions from open Loa issues:

| Issue | Title                   | Integration                                            |
| ----- | ----------------------- | ------------------------------------------------------ |
| #71   | Unix Philosophy         | `construct.yaml` with input/output contracts per phase |
| #70   | construct.yaml manifest | Full manifest with skills, execution order, gates      |
| #29   | PRD Iteration Loop      | Phase 7 includes PRD gap check and /refine-prd trigger |
| #48   | Feedback Protocol       | Phase 7 captures learnings in structured YAML          |
| #23   | NOTES.md cleanup        | Structured note format with types and expiry           |

### Resources

- `construct.yaml` - Skill packaging manifest (#70, #71)
- `resources/operator-detection.md` - AI/human adaptation
- `resources/feedback-protocol.md` - Upstream learning flow (#48)
- `resources/prd-iteration.md` - PRD refinement loop (#29)
- `resources/structured-notes.md` - Note format with expiry (#23)
- `resources/phase-checklist.md` - Completion criteria
- `resources/quality-gates.md` - Gate definitions
  </issue_integrations>

<prime_directive>

## Prime Directive

**NO SHORTCUTS. NO EXCEPTIONS.**

You are operating autonomously. Every action reflects on your principal's reputation.
Follow EVERY step. Pass EVERY gate. Audit EVERYTHING.

If uncertain: STOP and ASK rather than proceed with assumptions.
</prime_directive>

<execution_model>

## Execution Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS EXECUTION FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   PREFLIGHT ──▶ DISCOVER ──▶ DESIGN ──▶ IMPLEMENT               │
│       │                                      │                   │
│       │                                      ▼                   │
│       │         ┌──────────────────────  AUDIT ◀─────┐          │
│       │         │                          │         │          │
│       │         │    ┌─────────────────────┤         │          │
│       │         │    │                     │         │          │
│       │         │    ▼                     ▼         │          │
│       │         │  PASS?  ──YES──▶  SUBMIT                      │
│       │         │    │                │                          │
│       │         │   NO                ▼                          │
│       │         │    │          POST-PR-VAL ◀── (v1.25.0)       │
│       │         │    ▼                │                          │
│       │         └─ REMEDIATE    READY_FOR_HITL                   │
│       │              │                │                          │
│       │              │ loop > 3       ▼                          │
│       │              ▼          DEPLOY ──▶ LEARN                 │
│       └────────── ESCALATE ─────────────────────────────────────│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

</execution_model>

<operator_detection>

## Operator Detection

Loa adapts behavior based on operator type. See `resources/operator-detection.md` for full details.

### Configuration

```yaml
# .loa.config.yaml
operator:
  type: auto | human | ai
  ai_config:
    enforce_autonomous_skill: true
    strict_quality_gates: true
    require_audit_before_pr: true
```

### Detection Heuristics (when `type: auto`)

**MANDATORY: Check in this order, first match wins:**

1. **Clawdbot Runtime** (HIGHEST PRIORITY):
   - `CLAWDBOT_GATEWAY_TOKEN` env var exists → **AI_OPERATOR**
   - `CLAWDBOT_GATEWAY_PORT` env var exists → **AI_OPERATOR**
   - `$HOME/.clawdbot/clawdbot.json` exists → **AI_OPERATOR**

2. **Other AI Environments**:
   - `CLAUDECODE=1` → **AI_OPERATOR**
   - `LOA_OPERATOR=ai` → **AI_OPERATOR**
   - `CLAWDBOT_AGENT=true` → **AI_OPERATOR**

3. **Moltbot Workspace Signatures** (any 2+ files = AI_OPERATOR):
   - `AGENTS.md` — Agent instructions
   - `SOUL.md` — Agent identity/personality
   - `IDENTITY.md` — Agent metadata
   - `HEARTBEAT.md` — Cron/heartbeat config
   - `TOOLS.md` — Tool configuration
   - `USER.md` — User context
   - `WORKLEDGER.md` — Work tracking

4. **TTY Detection** (lowest priority):
   - Non-interactive session → **AI_OPERATOR**
   - Interactive TTY → **HUMAN_OPERATOR**

### Behavior Adaptation

| Operator  | Behavior                                                    |
| --------- | ----------------------------------------------------------- |
| **Human** | Interactive, suggestions, flexible process                  |
| **AI**    | Auto-wrap with `/autonomous`, mandatory audit, strict gates |

### Auto-Wrapping

When AI detected and `enforce_autonomous_skill: true`:

```
Human: /implement task-1
AI:    /implement task-1 → auto-wrapped with → /autonomous --target implement
```

All quality gates enforced. No shortcuts.
</operator_detection>

<phase_0_preflight>

## Phase 0: Preflight

**Purpose:** Restore context, verify integrity, detect operator, select work.

### 0.0 Workspace Cleanup (v1.23.0)

**Purpose:** Archive previous cycle artifacts to create clean workspace.

```markdown
1. Run workspace-cleanup.sh --yes --json
2. Parse JSON result
3. Check for security errors (exit 3) → HALT
4. Check for partial state (.staging/.failed exists) → HALT
5. Other errors → log warning, continue
```

**Implementation:**

```bash
# Run cleanup in autonomous mode
CLEANUP_RESULT=$(.claude/scripts/workspace-cleanup.sh --grimoire grimoires/loa --yes --json 2>&1)
CLEANUP_EXIT=$?

case $CLEANUP_EXIT in
  0)
    # Success - check for partial state
    if echo "$CLEANUP_RESULT" | jq -e '.partial_state != null' > /dev/null 2>&1; then
      PARTIAL=$(echo "$CLEANUP_RESULT" | jq -r '.partial_state[]? // empty')
      if [[ -n "$PARTIAL" ]]; then
        echo "HALT: Partial archive state detected - manual intervention required"
        echo "Found: $PARTIAL"
        exit 1
      fi
    fi
    echo "✓ Workspace cleanup complete"
    ;;
  3)
    # Security validation failure - HALT
    echo "HALT: Workspace cleanup security validation failed"
    exit 1
    ;;
  *)
    # Other error - log and continue
    echo "WARNING: Workspace cleanup failed (exit $CLEANUP_EXIT), continuing..."
    ;;
esac
```

**Fail-Closed Policy:** When operating autonomously, any security error or partial state MUST halt the workflow. This prevents propagating errors through subsequent phases.

### 0.1 Operator Detection

```markdown
1. Check environment variables (LOA_OPERATOR, CLAWDBOT_AGENT)
2. Parse AGENTS.md for operator markers
3. Check for HEARTBEAT.md patterns
4. Detect TTY mode
5. Set operator_type: 'human' | 'ai'
6. Load ai_config if operator_type == 'ai'
```

### 0.2 Session Continuity

```markdown
1. Read `grimoires/loa/NOTES.md`
2. Extract "Session Continuity" section
3. Check "Blockers" - if any CRITICAL, HALT
4. Load previous trajectory if continuing work
```

### 0.3 System Zone Integrity

```bash
# MANDATORY - Run before any work
IF .loa-version.json exists:
  echo "✓ Loa mounted"
ELSE:
  echo "✗ Loa not mounted - run /mount first"
  EXIT 1
```

### 0.4 Work Selection

```markdown
1. Read WORKLEDGER.md (or equivalent work queue)
2. Select highest priority item with status "Ready"
3. If no work: check backlog or HEARTBEAT_OK
4. Log work item to trajectory
```

### 0.5 Attention Budget Init

```markdown
1. Set token counters to 0
2. Load thresholds from config
3. Prepare for Tool Result Clearing
```

### Exit Criteria (ALL required)

- [ ] Workspace cleanup completed (or skipped with warning)
- [ ] No partial archive state detected
- [ ] NOTES.md read or created
- [ ] No CRITICAL blockers
- [ ] System Zone verified
- [ ] Work item selected
- [ ] Trajectory started
      </phase_0_preflight>

<phase_1_discovery>

## Phase 1: Discovery

**Purpose:** Understand requirements fully before designing.

**Trigger:** New work without existing PRD

### 1.1 Codebase Grounding

```markdown
IF target codebase not yet analyzed:

1. Run `/ride` on target repository
2. Wait for reality/ artifacts
3. Verify grounding claims have file:line citations
```

### 1.2 Requirements Discovery

```markdown
1. Run `/plan-and-analyze` (discovering-requirements skill)
2. Follow ALL phases of discovery
3. Generate PRD at `grimoires/{project}/prd.md`
```

### 1.3 PRD Quality Check

```markdown
VERIFY PRD contains:

- [ ] Executive summary
- [ ] Problem statement with evidence
- [ ] Goals with measurable metrics
- [ ] User stories with acceptance criteria
- [ ] Technical constraints
- [ ] Dependencies identified
- [ ] Risks with mitigations
```

### 1.4 Flatline PRD Review (v1.22.0)

**Purpose:** Adversarial multi-model review of PRD before proceeding to Design.

````markdown
IF flatline_protocol.enabled AND autonomous_mode.enabled:

1. Execute Flatline Protocol on PRD:

   ```bash
   result=$(.claude/scripts/flatline-orchestrator.sh \
       --doc grimoires/loa/prd.md \
       --phase prd \
       --autonomous \
       --run-id "$run_id" \
       --json)
   ```

2. Handle results per autonomous_mode.actions:

   ```bash
   .claude/scripts/flatline-result-handler.sh \
       --mode autonomous \
       --result "$result" \
       --document grimoires/loa/prd.md \
       --phase prd \
       --run-id "$run_id"
   ```

3. Exit code handling:
   - 0: Continue to Phase 2
   - 1: BLOCKER halt → Generate escalation, STOP workflow
   - 4: Disputed threshold → Generate escalation, STOP workflow

4. Log summary to NOTES.md:
   "Flatline PRD Review: {N} integrated, {M} disputed, {K} blockers"

ELSE:
Skip Flatline review, log "Flatline disabled for PRD phase"
````

### Exit Criteria

- [ ] PRD complete and verified
- [ ] All claims grounded (file:line or [ASSUMPTION])
- [ ] Flatline review passed (if enabled)
- [ ] Trajectory logged
      </phase_1_discovery>

<phase_2_design>

## Phase 2: Design

**Purpose:** Architecture and planning before implementation.

### 2.1 Architecture

```markdown
1. Run `/architect` (designing-architecture skill)
2. Generate SDD at `grimoires/{project}/sdd.md`
3. Include:
   - System diagrams
   - Component design
   - Data flow
   - API contracts
   - Security considerations
```

### 2.2 Sprint Planning

```markdown
1. Run `/sprint-plan` (planning-sprints skill)
2. Generate sprint.md with:
   - Atomic tasks
   - Acceptance criteria per task
   - Dependencies mapped
```

### 2.3 Flatline SDD Review (v1.22.0)

**Purpose:** Adversarial multi-model review of SDD before sprint planning execution.

````markdown
IF flatline_protocol.enabled AND autonomous_mode.enabled:

1. Execute Flatline Protocol on SDD:

   ```bash
   result=$(.claude/scripts/flatline-orchestrator.sh \
       --doc grimoires/loa/sdd.md \
       --phase sdd \
       --autonomous \
       --run-id "$run_id" \
       --json)
   ```

2. Handle results per autonomous_mode.actions:

   ```bash
   .claude/scripts/flatline-result-handler.sh \
       --mode autonomous \
       --result "$result" \
       --document grimoires/loa/sdd.md \
       --phase sdd \
       --run-id "$run_id"
   ```

3. Exit code handling:
   - 0: Continue to Sprint review
   - 1: BLOCKER halt → Generate escalation, STOP workflow
   - 4: Disputed threshold → Generate escalation, STOP workflow

ELSE:
Skip Flatline review, log "Flatline disabled for SDD phase"
````

### 2.4 Design Review

```markdown
VERIFY:

- [ ] SDD traces to PRD requirements
- [ ] All PRD requirements covered
- [ ] Tasks are atomic and testable
- [ ] No circular dependencies
```

### 2.5 Flatline Sprint Review (v1.22.0)

**Purpose:** Adversarial multi-model review of sprint plan before implementation.

````markdown
IF flatline_protocol.enabled AND autonomous_mode.enabled:

1. Execute Flatline Protocol on sprint plan:

   ```bash
   result=$(.claude/scripts/flatline-orchestrator.sh \
       --doc grimoires/loa/sprint.md \
       --phase sprint \
       --autonomous \
       --run-id "$run_id" \
       --json)
   ```

2. Handle results per autonomous_mode.actions:

   ```bash
   .claude/scripts/flatline-result-handler.sh \
       --mode autonomous \
       --result "$result" \
       --document grimoires/loa/sprint.md \
       --phase sprint \
       --run-id "$run_id"
   ```

3. Exit code handling:
   - 0: Continue to Phase 3 (Implementation)
   - 1: BLOCKER halt → Generate escalation, STOP workflow
   - 4: Disputed threshold → Generate escalation, STOP workflow

ELSE:
Skip Flatline review, log "Flatline disabled for sprint phase"
````

### Exit Criteria

- [ ] SDD complete
- [ ] Sprint plan ready
- [ ] Flatline SDD review passed (if enabled)
- [ ] Flatline Sprint review passed (if enabled)
- [ ] Design traces to requirements
      </phase_2_design>

<phase_3_implementation>

## Phase 3: Implementation

**Purpose:** Build the solution with quality.

### 3.1 Task Execution

```markdown
FOR each task IN sprint.md:

1. Read task acceptance criteria
2. Run `/implement` for this task
3. Apply Tool Result Clearing after searches
4. Run relevant tests
5. Commit with conventional message
6. Log to trajectory
7. Update sprint.md status
```

### 3.2 Quality During Implementation

```markdown
CONTINUOUSLY:

- Run linters/formatters
- Execute unit tests after changes
- Check for security issues (no secrets, no vulns)
- Respect attention budget
```

### 3.3 Tool Result Clearing

```markdown
AFTER every search/grep/find:
IF results > 2000 tokens:

1. Extract top 10 relevant files
2. Synthesize to NOTES.md
3. Clear raw results
4. Keep only summary
```

### Exit Criteria

- [ ] All sprint tasks complete
- [ ] All tests passing
- [ ] Changes committed (not pushed)
- [ ] No lint errors
- [ ] Attention budget respected
      </phase_3_implementation>

<phase_4_audit>

## Phase 4: Audit (MANDATORY)

**Purpose:** Verify quality before any external action.

### 4.1 Comprehensive Audit

```markdown
1. Run `/audit-sprint` (auditing-security skill)
2. Audit ALL dimensions:
   - Security (auth, injection, secrets)
   - Architecture (patterns, coupling, cohesion)
   - Code Quality (complexity, duplication, naming)
   - DevOps (CI/CD, monitoring, docs)
   - Domain-specific (blockchain, API, etc.)
```

### 4.2 Scoring

```markdown
FOR each dimension:
Score 1-5 using RUBRICS.md criteria

PASS if ALL dimensions >= audit_threshold (default: 4)
FAIL if ANY dimension < audit_threshold
```

### 4.3 Audit Report

```markdown
Generate audit report with:

- Overall PASS/FAIL
- Scores by dimension
- Findings with severity
- Remediation guidance
- Evidence citations
```

### Gate Decision

```markdown
IF all_scores >= threshold:
→ Proceed to Phase 5 (Submit)
ELSE:
→ Enter Phase 4.5 (Remediation)
```

</phase_4_audit>

<phase_4_5_remediation>

## Phase 4.5: Remediation Loop

**Purpose:** Fix audit failures until quality passes.

### 4.5.1 Analyze Failures

```markdown
1. Parse audit findings
2. Sort by severity: CRITICAL > HIGH > MEDIUM > LOW
3. Identify root causes
```

### 4.5.2 Apply Fixes

```markdown
FOR finding IN sorted_findings:
IF finding.severity IN [CRITICAL, HIGH]: 1. Understand the issue 2. Design minimal fix 3. Apply fix 4. Verify locally 5. Log to trajectory
```

### 4.5.3 Re-Audit

```markdown
1. Run `/audit-sprint` again
2. Check if all scores >= threshold
3. Increment remediation_loop counter
```

### 4.5.4 Loop Control

```markdown
IF all_scores >= threshold:
→ BREAK, proceed to Phase 5
ELIF remediation_loop > max_remediation_loops (default: 3):
→ ESCALATE to human
ELSE:
→ REPEAT from 4.5.1
```

### 4.5.5 Escalation

```markdown
Generate escalation report:

- Summary of issue
- Remediation attempts made
- Remaining failures
- Recommendation for human action

HALT autonomous execution
NOTIFY human via configured channel
```

</phase_4_5_remediation>

<phase_5_submit>

## Phase 5: Submission

**Purpose:** Create high-quality PR.

**Gate:** Only enter if Phase 4 audit PASSED

### 5.1 Branch Push

```markdown
1. Push branch to fork/origin
2. Verify push succeeded
```

### 5.2 PR Creation

```markdown
Create PR with:

- Title: Conventional commit format
- Body:
  - Summary from PRD
  - Changes from sprint.md
  - Link to audit report (if applicable)
  - Trajectory summary
```

### 5.3 PR Quality Check

```markdown
VERIFY PR:

- [ ] Title is descriptive
- [ ] Body explains context
- [ ] No secrets in diff
```

### Exit Criteria

- [ ] Branch pushed
- [ ] PR created
- [ ] Trajectory logged
- [ ] → Proceed to Phase 5.5 (Post-PR Validation)
      </phase_5_submit>

<phase_5_5_post_pr_validation>

## Phase 5.5: Post-PR Validation (v1.25.0)

**Purpose:** Validate PR quality before human review.

**Gate:** Only enter if `post_pr_validation.enabled: true` in `.loa.config.yaml`

### 5.5.1 Invoke Post-PR Orchestrator

```markdown
IF post_pr_validation.enabled:

1. Invoke: .claude/scripts/post-pr-orchestrator.sh --pr-url <pr_url> --mode autonomous
2. Handle exit codes: - 0 (SUCCESS) → state = READY_FOR_HITL - 1 (ERROR) → state = HALTED, log error - 2 (TIMEOUT) → state = HALTED, escalate - 3 (PHASE_FAIL) → state = HALTED, check findings - 4 (BLOCKER) → state = HALTED, Flatline blocker found - 5 (USER_HALT) → state = HALTED, user intervention
   ELSE:
   → Skip to Phase 6 (Deploy) or Phase 7 (Learning)
```

### 5.5.2 Validation Phases

The orchestrator executes these phases in sequence:

| Phase             | Description                            | Fix Loop    |
| ----------------- | -------------------------------------- | ----------- |
| **POST_PR_AUDIT** | Consolidated security/quality audit    | Yes (max 5) |
| **CONTEXT_CLEAR** | Checkpoint, prompt user to `/clear`    | No          |
| **E2E_TESTING**   | Fresh-eyes build and test verification | Yes (max 3) |
| **FLATLINE_PR**   | Optional multi-model review (~$1.50)   | No          |

**State File:** `.run/post-pr-state.json`

### 5.5.3 Resume from Context Clear

When user runs `/autonomous --resume` after context clear:

```markdown
1. Check post-PR state file (.run/post-pr-state.json)
2. If state == CONTEXT_CLEAR:
   - Load checkpoint from NOTES.md Session Continuity
   - Continue with: post-pr-orchestrator.sh --resume
   - E2E testing runs with fresh context
3. On completion:
   - state = READY_FOR_HITL
   - Continue to Phase 6 or Phase 7
```

### 5.5.4 Configuration Reference

```yaml
# .loa.config.yaml
post_pr_validation:
  enabled: true
  phases:
    audit: { enabled: true, max_iterations: 5 }
    context_clear: { enabled: true }
    e2e: { enabled: true, max_iterations: 3 }
    flatline: { enabled: false } # Opt-in, ~$1.50 cost
```

### Exit Criteria

- [ ] Post-PR audit passed (or disabled)
- [ ] E2E tests passed (or disabled)
- [ ] Flatline review passed (or disabled)
- [ ] State = READY_FOR_HITL

**Full Specification:** `.claude/commands/post-pr-validation.md`
</phase_5_5_post_pr_validation>

<phase_6_deploy>

## Phase 6: Deployment (Optional)

**Purpose:** Safely deploy and verify.

**Gate:**

- Post-PR Validation passed (if enabled) OR state = READY_FOR_HITL
- AND (`require_human_deploy_approval == false` OR approval received)

### 6.1 Deployment

```markdown
1. Run `/deploy-production`
2. Monitor deployment progress
3. Capture deployment logs
```

### 6.2 Post-Deploy Audit

```markdown
1. Run `/audit-deployment`
2. Verify:
   - Health checks passing
   - No error rate increase
   - Performance within bounds
   - Functionality working
```

### 6.3 Rollback Trigger

```markdown
IF audit-deploy fails:

1. Initiate rollback
2. Verify rollback success
3. Log incident
4. Escalate to human
```

### Exit Criteria

- [ ] Deployment complete
- [ ] audit-deploy passed
- [ ] OR rollback executed
      </phase_6_deploy>

<phase_7_learning>

## Phase 7: Learning

**Purpose:** Improve from experience, iterate on PRD, feed learnings upstream.

See also:

- `resources/prd-iteration.md` (Issue #29)
- `resources/feedback-protocol.md` (Issue #48)
- `resources/structured-notes.md` (Issue #23)

### 7.1 Extract Learnings

```markdown
Review execution:

- What worked well?
- What required remediation?
- New patterns discovered?
- Process improvements?
- Implementation gaps vs PRD?
```

### 7.2 PRD Iteration Check (Issue #29)

```markdown
1. Parse trajectory for deviations from PRD
2. Identify gaps:
   - Requirements not fully met
   - Features added not in PRD
   - Better approaches discovered
3. Classify: major | minor
4. Decision:
   - Major gaps → invoke /refine-prd OR escalate
   - Minor gaps → log to NOTES.md for future
```

### 7.3 Capture Feedback (Issue #48)

```markdown
1. Generate feedback entries:
   - Gaps → type: gap
   - Friction points → type: friction
   - Patterns observed → type: pattern
   - Improvement ideas → type: improvement
2. Write to grimoires/loa/feedback/{date}.yaml
3. Classify target: loa | clawdbot | registry | skill:{name}
4. Log to trajectory
```

### 7.4 Update Memory (Issue #23)

```markdown
1. Create structured notes for significant items:
   - type: decision (never expires)
   - type: observation (14 day check)
   - type: synthesis (7 day expiry)
2. Update NOTES.md with session summary
3. If significant learning:
   - Update relevant documentation
   - Consider skill improvements
4. Feed to /compound (if enabled)
```

### 7.5 Archive Trajectory

```markdown
1. Close trajectory log
2. Archive to trajectory/{date}.jsonl
3. Clear working memory (apply semantic decay)
```

### 7.6 Prepare Next

```markdown
1. Mark work item complete
2. Update CHANGELOG.md (if applicable)
3. Commit workspace updates
4. If /refine-prd was invoked:
   - Wait for new sprint.md
   - Add new sprints to work queue
5. Ready for next work item
```

### Exit Criteria

- [ ] Learnings extracted
- [ ] PRD iteration check complete
- [ ] Feedback captured for upstream
- [ ] Structured notes created
- [ ] Trajectory archived
- [ ] Work item marked complete
- [ ] Ready for next cycle
      </phase_7_learning>

<resume_support>

## Resume Support (v1.22.0)

The `/autonomous --resume` flag enables resumption of workflows halted by Flatline BLOCKER items.

### Resume Detection

````bash
IF --resume flag provided:
  1. Check for pending escalation report:
     ```bash
     escalation=$(.claude/scripts/flatline-escalation.sh list | jq '.[0]')
     ```

  2. IF escalation exists:
     - Extract run_id, phase, halted_at
     - Validate blocker concerns addressed
     - Resume from last completed phase

  3. IF no escalation:
     - Check NOTES.md for "Flatline Halt" section
     - Resume from last checkpoint
````

### Resume Workflow

````markdown
1. Load escalation report:
   - run_id: Original Flatline run ID
   - phase: Phase where halt occurred (prd, sdd, sprint)
   - blockers: List of BLOCKER items that caused halt

2. Validate blockers addressed:
   FOR each blocker IN escalation.blockers:
   - Re-run Flatline on affected document
   - Verify blocker concern resolved
   - IF still present: HALT with "Blocker not addressed: {id}"

3. Resume execution:
   CASE phase:
   "prd": Resume from Phase 1.4 (Flatline PRD Review)
   "sdd": Resume from Phase 2.3 (Flatline SDD Review)
   "sprint": Resume from Phase 2.5 (Flatline Sprint Review)

4. Log resume event:
   ```json
   {
     "type": "flatline_resume",
     "original_run_id": "{run_id}",
     "phase": "{phase}",
     "blockers_resolved": N,
     "timestamp": "{ISO8601}"
   }
   ```
````

````

### Resume Command

```bash
# Resume from Flatline halt
/autonomous --resume

# Resume with specific escalation
/autonomous --resume --run-id flatline-run-abc123
````

### Exit Criteria for Resume

- [ ] Escalation report found and loaded
- [ ] All blocker concerns addressed
- [ ] Workflow resumed from correct phase
- [ ] Resume event logged to trajectory

### Resume from Post-PR Context Clear (v1.25.0)

When `/autonomous --resume` detects Post-PR Validation context clear state:

```markdown
IF state file (.run/post-pr-state.json) shows state == CONTEXT_CLEAR:

1. Load checkpoint from NOTES.md Session Continuity section
2. Verify PR still exists and is open
3. Continue with: .claude/scripts/post-pr-orchestrator.sh --resume
4. E2E testing runs with fresh context (unbiased by previous work)
5. On success:
   - state = READY_FOR_HITL
   - Continue to Phase 6 (Deploy) if enabled, or Phase 7 (Learning)
6. On failure:
   - Check circuit breaker (same failure 2x → HALT)
   - Apply fix and retry, or escalate
```

**State File:** `.run/post-pr-state.json`
**Checkpoint Location:** `grimoires/loa/NOTES.md` → Session Continuity section
**Full Specification:** `.claude/commands/post-pr-validation.md`
</resume_support>

<attention_budget>

## Attention Budget

This skill MUST enforce attention budget throughout ALL phases.

### Thresholds

| Context       | Limit         | Action             |
| ------------- | ------------- | ------------------ |
| Single search | 2,000 tokens  | Apply TRC          |
| Accumulated   | 5,000 tokens  | MANDATORY TRC      |
| Session total | 15,000 tokens | Checkpoint & yield |

### Tool Result Clearing

After ANY tool returning >2K tokens:

1. **Extract**: Max 10 files, 20 words each
2. **Synthesize**: Write to NOTES.md
3. **Clear**: Remove raw output
4. **Summary**: Keep one-line reference

### Semantic Decay

| Stage    | Age     | Format              |
| -------- | ------- | ------------------- |
| Active   | 0-5min  | Full synthesis      |
| Decayed  | 5-30min | Paths only          |
| Archived | 30+min  | Single-line summary |

</attention_budget>

<factual_grounding>

## Factual Grounding

ALL claims MUST be evidenced.

### Required Format

```markdown
✓ GROUNDED: "Function validates JWT tokens" (src/auth/jwt.ts:45)
✗ UNGROUNDED: The system probably handles auth well
✓ FLAGGED: [ASSUMPTION] Users likely prefer dark mode
```

### Verification

Before any synthesis:

1. Quote exact text from source
2. Cite with absolute path and line
3. Flag assumptions explicitly
   </factual_grounding>

<trajectory_logging>

## Trajectory Logging

Log EVERY significant action to `grimoires/{project}/trajectory/{date}.jsonl`:

```jsonl
{"ts":"2026-01-30T22:30:00Z","agent":"autonomous-agent","phase":0,"action":"preflight_start","status":"started"}
{"ts":"2026-01-30T22:30:05Z","agent":"autonomous-agent","phase":0,"action":"notes_loaded","status":"completed"}
{"ts":"2026-01-30T22:30:10Z","agent":"autonomous-agent","phase":1,"action":"discover_start","skill":"discovering-requirements","status":"started"}
```

### Required Fields

- `ts`: ISO 8601 timestamp
- `agent`: "autonomous-agent"
- `phase`: Current phase number
- `action`: Verb describing action
- `status`: started | completed | failed | escalated

### Optional Fields

- `skill`: Invoked skill name
- `tokens_used`: Token count for this action
- `audit_score`: Scores if auditing
- `remediation_loop`: Loop counter if remediating
  </trajectory_logging>

<quality_commitment>

## Quality Commitment

As an autonomous agent, I commit to:

1. **NEVER skip a phase** - Every phase has value
2. **NEVER skip an audit** - Quality is non-negotiable
3. **NEVER submit without passing** - Reputation matters
4. **ALWAYS log my work** - Transparency enables trust
5. **ALWAYS ask when uncertain** - Assumptions are risks
6. **ALWAYS learn from failures** - Every remediation teaches

This skill exists because autonomous work must be BETTER than rushed work, not just faster.
</quality_commitment>

<context_management>

## Context Management Protocol

For long-running executions that risk context overflow.

### Soft Limit (80K tokens)

When approaching 80K tokens:

1. Summarize completed phases
2. Clear old tool outputs
3. Keep decisions + artifact refs
4. Write checkpoint

### Hard Limit (150K tokens)

When approaching 150K tokens:

1. EMERGENCY: Write full state to checkpoint
2. Clear conversation history
3. Reload from checkpoint summary
4. Continue execution

### Checkpoint Schema

```yaml
version: 1
execution_id: "exec-{timestamp}"
phase: "design"
summary: "Max 500 words..."
decisions: [...]
artifacts: [...]
errors: [...]
```

</context_management>
