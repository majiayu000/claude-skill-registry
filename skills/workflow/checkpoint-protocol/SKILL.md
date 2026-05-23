---
name: checkpoint-protocol
description: Human interaction protocol with automation-first rule. Defines checkpoint types and when to use them.
---

# Checkpoint Protocol

// Project Autopilot - Checkpoint Protocol Skill
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Golden Rule:** If it has CLI/API, Claude does it. Humans only do what requires judgment.

---

## Checkpoint Types

### Distribution

| Type | Frequency | When to Use |
|------|-----------|-------------|
| `checkpoint:human-verify` | 90% | User confirms it works |
| `checkpoint:decision` | 9% | User chooses between options |
| `checkpoint:human-action` | 1% | Truly unavoidable manual step |

---

## Type 1: Human-Verify (90%)

Claude automates everything, human just confirms it works.

### When to Use
- Visual verification (UI looks right)
- Interactive flows (click through app)
- Functional verification (feature works as expected)

### Format

```xml
<task type="auto">
  <name>Start dev server</name>
  <action>Run `npm run dev` in background</action>
  <verify>curl localhost:3000 returns 200</verify>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Dashboard - server at http://localhost:3000</what-built>
  <how-to-verify>
    Visit http://localhost:3000/dashboard and verify:
    1. Desktop (>1024px): sidebar visible, cards display data
    2. Mobile (375px): single column, bottom nav visible
    3. Click "Settings" - modal opens
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

### Key Rules

- **Claude starts servers** - User never runs `npm run dev`
- **Claude sets up data** - User never creates test data
- **Claude provides URLs** - User just clicks links
- **User only looks** - Visual/functional confirmation

### Example Output

```markdown
🟢 checkpoint:human-verify

## Built: User Dashboard

**Server running:** http://localhost:3000/dashboard

### Please verify:
1. ✅ Page loads without errors
2. ✅ User data displays correctly
3. ✅ Sidebar navigation works
4. ✅ Mobile view is responsive

**Resume:** Type "approved" or describe issues
```

---

## Type 2: Decision (9%)

Human must make a choice affecting implementation.

### When to Use
- Technology selection (which library)
- Architecture decisions (approach A vs B)
- Design choices (layout, color, UX)
- Business logic (pricing, limits, rules)

### Format

```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>Select authentication provider</decision>
  <context>
    Need user auth for the app. Three options with tradeoffs.
  </context>
  <options>
    <option id="supabase">
      <name>Supabase Auth</name>
      <pros>Built-in with DB, free tier generous, email templates</pros>
      <cons>Less customizable UI, vendor lock-in</cons>
    </option>
    <option id="clerk">
      <name>Clerk</name>
      <pros>Best DX, beautiful UI, social logins easy</pros>
      <cons>Paid after 10k MAU, another vendor</cons>
    </option>
    <option id="custom">
      <name>Custom JWT</name>
      <pros>Full control, no external dependencies</pros>
      <cons>More implementation work, security responsibility</cons>
    </option>
  </options>
  <resume-signal>Select: supabase, clerk, or custom</resume-signal>
</task>
```

### Key Rules

- **Present balanced options** - No prescriptive recommendation
- **Include context** - Why this decision matters
- **Show tradeoffs** - Pros AND cons for each
- **No "correct" answer** - All options are valid

### Example Output

```markdown
🟡 checkpoint:decision

## Decision Required: Authentication Provider

**Context:** Need user auth. Three approaches available.

| Option | Pros | Cons |
|--------|------|------|
| **Supabase** | Built-in, free tier | Less customizable |
| **Clerk** | Best DX, beautiful UI | Paid after 10k users |
| **Custom JWT** | Full control | More work |

**Select:** supabase, clerk, or custom
```

---

## Type 3: Human-Action (1% - RARE)

Truly unavoidable manual step. **Exhaust all automation first.**

### When to Use (Only These Cases)
- Email verification clicks (can't automate)
- 3D Secure / MFA in payment flow
- OAuth consent screens in browser
- Physical hardware interaction
- Captcha solving

### When NOT to Use
- ❌ Running CLI commands (Claude runs them)
- ❌ Creating accounts (Claude uses API/CLI)
- ❌ Starting servers (Claude runs them)
- ❌ Creating files (Claude creates them)
- ❌ Configuration (Claude edits files)
- ❌ Database setup (Claude runs migrations)

### Format

```xml
<task type="auto">
  <name>Create SendGrid account</name>
  <action>Use API to create account, request verification email</action>
</task>

<task type="checkpoint:human-action">
  <action>Complete email verification</action>
  <why-manual>Email verification requires clicking link in your inbox</why-manual>
  <instructions>
    1. Check your inbox for email from SendGrid
    2. Click the verification link
    3. Return here when done
  </instructions>
  <resume-signal>Type "done" when verified</resume-signal>
</task>
```

### Key Rules

- **Try automation FIRST** - Only ask for help when blocked
- **Explain why manual** - User should know why this can't be automated
- **Minimize steps** - Do everything possible before/after the manual step
- **Golden rule:** If it has CLI/API, Claude MUST do it

### Example Output

```markdown
🔴 checkpoint:human-action

## Manual Step Required: Email Verification

**Why manual:** Email verification links can't be automated

### Instructions:
1. Check your inbox for email from SendGrid
2. Click "Verify Email" button
3. Return here when done

**Resume:** Type "done" when verified
```

---

## Automation-First Checklist

Before using ANY checkpoint, ask:

```
□ Can I do this with a CLI command?
□ Can I do this with an API call?
□ Can I do this by editing a file?
□ Can I start/stop a server myself?
□ Can I create test data myself?
□ Can I run a script for this?
```

If ANY answer is YES → Don't ask user to do it.

---

## Common Anti-Patterns

### ❌ Wrong: Asking User to Run Commands

```markdown
Please run: npm run dev
```

### ✅ Right: Claude Runs Commands

```bash
# Claude executes
npm run dev &
# Then presents checkpoint
Visit http://localhost:3000 to verify
```

---

### ❌ Wrong: Asking User to Create Files

```markdown
Please create a file at src/config.ts with:
[content]
```

### ✅ Right: Claude Creates Files

```bash
# Claude creates the file
Write src/config.ts
# Done - no checkpoint needed
```

---

### ❌ Wrong: Asking User to Set Up Database

```markdown
Please create a PostgreSQL database called "myapp"
```

### ✅ Right: Claude Uses CLI

```bash
# Claude executes
createdb myapp
psql myapp < schema.sql
# Done - no checkpoint needed
```

---

### ❌ Wrong: Decision as Human-Action

```markdown
Should I use React or Vue?
Please choose and let me know.
```

### ✅ Right: Use Decision Checkpoint

```xml
<task type="checkpoint:decision">
  <decision>Frontend framework</decision>
  <options>
    <option id="react">React - Larger ecosystem</option>
    <option id="vue">Vue - Simpler learning curve</option>
  </options>
</task>
```

---

## Checkpoint Flow in Execution

```
FOR each plan:
    IF plan.autonomous == true:
        Execute all tasks automatically
        Generate LOGBOOK.md

    ELSE IF plan has checkpoint:
        Execute tasks up to checkpoint

        SWITCH checkpoint.type:
            CASE human-verify:
                Present what was built
                Show verification steps
                WAIT for "approved" or issues

            CASE decision:
                Present options with tradeoffs
                WAIT for selection
                Continue with selected option

            CASE human-action:
                Present instructions
                WAIT for "done"

        Continue remaining tasks
        Generate LOGBOOK.md
```

---

## Integration with Wave Execution

```yaml
# Plan with checkpoint (runs sequentially, not parallel)
---
phase: 3
plan: 06
wave: 3
autonomous: false
checkpoint:
  type: human-verify
  after_task: 4
  what: "Integration tests pass, dashboard functional"
depends_on: ["04", "05"]
---
```

- Plans with checkpoints are NOT spawned in parallel
- They run sequentially after parallel wave completes
- Checkpoint pauses execution until user responds

---

## Three-Level Threshold System

### Threshold Levels

```yaml
thresholds:
  warning:
    cost: 10.00        # Log warning, continue
    context: 30        # Log warning, continue (percentage)
    variance: 20       # Log warning, continue (percentage)
    errors: 2          # Log warning, continue (count)

  alert:
    cost: 25.00        # Pause for acknowledgment
    context: 40        # Prepare checkpoint
    variance: 30       # Pause for review
    errors: 3          # Pause for investigation

  stop:
    cost: 50.00        # Hard stop, require user action
    context: 50        # Must checkpoint, terminate
    variance: 50       # Escalate to user
    errors: 5          # Hard stop, likely systemic issue
```

### Threshold Actions

| Level | Action | User Impact |
|-------|--------|-------------|
| **Warning** | Log message, continue | No interruption |
| **Alert** | Pause until acknowledged | One-time acknowledgment |
| **Stop** | Hard stop, checkpoint | Must address issue |

---

## Threshold Handling Protocol

```
FUNCTION handleThreshold(type, level, value, state):
    """
    Handle threshold breach based on level.
    """
    LOG "⚠️ Threshold triggered: {type} at {level} ({value})"

    SWITCH level:
        CASE "warning":
            # Log and continue
            LOG "📝 Warning: {type} reached {value}"
            logToMetrics(type, level, value)
            CONTINUE

        CASE "alert":
            # Check if already acknowledged
            IF state.acknowledged[type]:
                LOG "⏩ Alert acknowledged previously, continuing..."
                CONTINUE
            ELSE:
                # Pause for acknowledgment
                LOG "🔶 ALERT: {type} at {value}"
                LOG ""
                LOG "This threshold requires acknowledgment to continue."
                LOG "Type 'ack' to acknowledge and continue, or 'stop' to halt."

                response = waitForUserResponse()

                IF response == "ack":
                    state.acknowledged[type] = {
                        value: value,
                        acknowledged_at: now(),
                        session_id: getCurrentSessionId()
                    }
                    saveState(state)
                    LOG "✅ Acknowledged. Continuing..."
                    CONTINUE
                ELSE:
                    createCheckpoint("alert_stop")
                    EXIT

        CASE "stop":
            # Hard stop
            LOG "🛑 STOP: {type} at {value}"
            LOG ""
            LOG "This threshold requires immediate action."
            LOG "Execution cannot continue until issue is resolved."

            createCheckpoint("threshold_stop", {
                type: type,
                value: value,
                reason: "Threshold exceeded"
            })

            EXIT_WITH_CHECKPOINT
```

### Threshold Monitoring

```
FUNCTION monitorThresholds(execution_state):
    """
    Continuously monitor thresholds during execution.
    """
    thresholds = loadThresholds()

    # Cost threshold
    IF execution_state.total_cost >= thresholds.stop.cost:
        handleThreshold("cost", "stop", execution_state.total_cost, execution_state)
    ELSE IF execution_state.total_cost >= thresholds.alert.cost:
        handleThreshold("cost", "alert", execution_state.total_cost, execution_state)
    ELSE IF execution_state.total_cost >= thresholds.warning.cost:
        handleThreshold("cost", "warning", execution_state.total_cost, execution_state)

    # Context usage threshold
    context_percent = calculateContextUsage()
    IF context_percent >= thresholds.stop.context:
        handleThreshold("context", "stop", context_percent, execution_state)
    ELSE IF context_percent >= thresholds.alert.context:
        handleThreshold("context", "alert", context_percent, execution_state)
    ELSE IF context_percent >= thresholds.warning.context:
        handleThreshold("context", "warning", context_percent, execution_state)

    # Variance threshold
    variance = calculateVariance(execution_state.estimated, execution_state.actual)
    IF variance >= thresholds.stop.variance:
        handleThreshold("variance", "stop", variance, execution_state)
    ELSE IF variance >= thresholds.alert.variance:
        handleThreshold("variance", "alert", variance, execution_state)
    ELSE IF variance >= thresholds.warning.variance:
        handleThreshold("variance", "warning", variance, execution_state)

    # Error count threshold
    IF execution_state.error_count >= thresholds.stop.errors:
        handleThreshold("errors", "stop", execution_state.error_count, execution_state)
    ELSE IF execution_state.error_count >= thresholds.alert.errors:
        handleThreshold("errors", "alert", execution_state.error_count, execution_state)
    ELSE IF execution_state.error_count >= thresholds.warning.errors:
        handleThreshold("errors", "warning", execution_state.error_count, execution_state)
```

---

## Acknowledgment Persistence

### Storage Location

```
.autopilot/state/acknowledgments.json
```

### Structure

```json
{
  "acknowledgments": {
    "cost": {
      "acknowledged_at": "2026-01-29T14:30:00Z",
      "value_at_ack": 26.50,
      "session_id": "session-abc123"
    },
    "context": {
      "acknowledged_at": "2026-01-29T15:00:00Z",
      "value_at_ack": 42,
      "session_id": "session-def456"
    }
  },
  "last_reset": null
}
```

### Persistence Protocol

```
FUNCTION loadAcknowledgments():
    """
    Load acknowledgments from persistent storage.
    """
    path = ".autopilot/state/acknowledgments.json"
    IF fileExists(path):
        RETURN parseJSON(readFile(path))
    ELSE:
        RETURN {acknowledgments: {}, last_reset: null}

FUNCTION saveAcknowledgment(type, value):
    """
    Persist acknowledgment for future sessions.
    """
    acks = loadAcknowledgments()
    acks.acknowledgments[type] = {
        acknowledged_at: now(),
        value_at_ack: value,
        session_id: getCurrentSessionId()
    }
    writeJSON(".autopilot/state/acknowledgments.json", acks)

FUNCTION resetAcknowledgments():
    """
    Clear all acknowledgments (--reset-alerts flag).
    """
    acks = {
        acknowledgments: {},
        last_reset: now()
    }
    writeJSON(".autopilot/state/acknowledgments.json", acks)
    LOG "✅ All alert acknowledgments cleared"
```

### Reset Command

```bash
# Reset all acknowledgments
/autopilot:takeoff --reset-alerts

# or during execution
/autopilot:cockpit --reset-alerts
```

---

## Additional Checkpoint Triggers

### Trigger Configuration

```yaml
checkpoint_triggers:
  # Task/Phase events
  - type: task_complete
    frequency: every
    action: update_state

  - type: phase_complete
    frequency: every
    action: checkpoint_and_verify

  # Context management
  - type: context_warning
    threshold: 30%
    action: log_warning

  - type: context_alert
    threshold: 40%
    action: prepare_checkpoint

  - type: context_stop
    threshold: 50%
    action: force_checkpoint

  # Cost management
  - type: cost_warning
    threshold: $10
    action: log_warning

  - type: cost_alert
    threshold: $25
    action: pause_for_ack

  - type: cost_stop
    threshold: $50
    action: hard_stop

  # Error handling
  - type: error_threshold
    count: 3
    action: pause_and_investigate

  # Time management
  - type: time_elapsed
    duration: 30min
    action: suggest_checkpoint

  # User interaction
  - type: user_interrupt
    signal: Ctrl+C
    action: graceful_checkpoint
```

### Trigger Protocol

```
FUNCTION checkTriggers(execution_state):
    """
    Check all checkpoint triggers.
    """
    triggers = loadTriggers()

    FOR each trigger IN triggers:
        SWITCH trigger.type:
            CASE "task_complete":
                # Always triggered after task
                IF execution_state.just_completed_task:
                    updateState(execution_state)

            CASE "phase_complete":
                IF execution_state.just_completed_phase:
                    createCheckpoint("phase_complete")
                    verifyPhaseGoals(execution_state.phase)

            CASE "context_warning", "context_alert", "context_stop":
                context_pct = calculateContextUsage()
                IF context_pct >= trigger.threshold:
                    executeTriggerAction(trigger, context_pct)

            CASE "cost_warning", "cost_alert", "cost_stop":
                IF execution_state.total_cost >= trigger.threshold:
                    executeTriggerAction(trigger, execution_state.total_cost)

            CASE "error_threshold":
                IF execution_state.error_count >= trigger.count:
                    pauseAndInvestigate(execution_state.recent_errors)

            CASE "time_elapsed":
                elapsed = now() - execution_state.session_start
                IF elapsed >= trigger.duration:
                    suggestCheckpoint("time_elapsed", elapsed)

            CASE "user_interrupt":
                IF signalReceived(SIGINT):
                    gracefulCheckpoint(execution_state)
```

---

## Autonomous vs Human-Verify Plans

### Plan Types

```yaml
# Autonomous plan (no checkpoint needed)
---
phase: 1
plan: 01
autonomous: true
checkpoint: null
---

# Tasks execute without interruption
# Summary generated at end
```

```yaml
# Human-verify plan (requires confirmation)
---
phase: 3
plan: 06
autonomous: false
checkpoint:
  type: human-verify
  after_task: 4
  what: "Dashboard functional, data displays correctly"
---

# Pauses after task 4 for verification
# Continues after "approved" response
```

### Execution Protocol

```
FUNCTION executePlan(plan):
    """
    Execute plan based on autonomous flag.
    """
    IF plan.autonomous == true:
        # Full autonomous execution
        LOG "🤖 Autonomous execution: Phase {plan.phase}, Plan {plan.plan}"

        FOR each task IN plan.tasks:
            executeTask(task)
            monitorThresholds(state)  # Still check thresholds

        generateSummary(plan)
        updateState(state)

    ELSE:
        # Execute with checkpoint
        LOG "👤 Human-verify execution: Phase {plan.phase}, Plan {plan.plan}"

        FOR index, task IN enumerate(plan.tasks):
            executeTask(task)
            monitorThresholds(state)

            # Check if checkpoint is after this task
            IF plan.checkpoint AND index + 1 == plan.checkpoint.after_task:
                presentCheckpoint(plan.checkpoint)
                response = waitForUserResponse()

                IF response == "approved":
                    LOG "✅ Checkpoint approved, continuing..."
                ELSE:
                    # User reported issues
                    handleIssues(response)

        generateSummary(plan)
        updateState(state)
```

### Plan Type Selection

```
FUNCTION determinePlanType(phase, plan):
    """
    Determine if plan should be autonomous or human-verify.
    """
    # Always human-verify for these cases:
    IF plan.has_ui_changes:
        RETURN {autonomous: false, reason: "UI changes require visual verification"}

    IF plan.has_user_flows:
        RETURN {autonomous: false, reason: "User flows require functional verification"}

    IF plan.is_integration:
        RETURN {autonomous: false, reason: "Integration requires end-to-end verification"}

    IF phase.is_final:
        RETURN {autonomous: false, reason: "Final phase requires comprehensive verification"}

    # Default to autonomous for:
    IF plan.is_infrastructure:
        RETURN {autonomous: true, reason: "Infrastructure can be verified programmatically"}

    IF plan.is_backend_only:
        RETURN {autonomous: true, reason: "Backend verified by tests"}

    IF plan.is_setup:
        RETURN {autonomous: true, reason: "Setup verified by existence checks"}

    # Default: based on phase position
    IF phase.number <= 2:
        RETURN {autonomous: true, reason: "Early phases typically autonomous"}
    ELSE:
        RETURN {autonomous: false, reason: "Later phases need verification"}
```

---

## Threshold Output Formats

### Warning (No Interruption)

```
📝 Warning: Cost at $11.50 (threshold: $10)
   Continuing execution...
```

### Alert (Requires Acknowledgment)

```
╔══════════════════════════════════════════════════════╗
║           🔶 ALERT: Threshold Reached                 ║
╠══════════════════════════════════════════════════════╣
║  Type:      Cost                                      ║
║  Current:   $26.50                                    ║
║  Threshold: $25.00 (alert)                            ║
║  Next:      $50.00 (stop)                             ║
╠══════════════════════════════════════════════════════╣
║  This alert requires acknowledgment to continue.      ║
║                                                       ║
║  Type 'ack' to acknowledge and continue               ║
║  Type 'stop' to halt execution                        ║
╚══════════════════════════════════════════════════════╝
```

### Stop (Hard Stop)

```
╔══════════════════════════════════════════════════════╗
║           🛑 STOP: Threshold Exceeded                 ║
╠══════════════════════════════════════════════════════╣
║  Type:      Cost                                      ║
║  Current:   $52.30                                    ║
║  Threshold: $50.00 (stop)                             ║
╠══════════════════════════════════════════════════════╣
║  Execution HALTED. Checkpoint created.                ║
║                                                       ║
║  Options:                                             ║
║  1. Increase threshold in .autopilot/config.yaml      ║
║  2. Review and optimize remaining work                ║
║  3. Resume with /autopilot:cockpit --reset-alerts     ║
╚══════════════════════════════════════════════════════╝

Waypoint saved: .autopilot/waypoints/stop-20260129-143000.json
```
