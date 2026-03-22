---
name: ralph-wiggum-loop
description: >
  Multi-step autonomous plan execution with bounded iteration (max 10), state persistence,
  dependency checking, error retry with exponential backoff, and human escalation on failure.
  The "Ralph Wiggum loop" enables AI agents to execute complex multi-step plans autonomously
  while maintaining safety bounds and progress tracking. Includes MCP action invocation,
  step dependency validation, graceful error recovery, and comprehensive audit logging. Use
  when: (1) implementing autonomous multi-step task execution, (2) building plan execution
  engines with retry logic, (3) creating bounded loops with state persistence, (4) handling
  step dependencies in workflows, (5) implementing human escalation patterns for blocked tasks.
---

# Ralph Wiggum Loop

## What is the Ralph Wiggum Loop?

> "I'm helping! I'm helping! I'm helping!" — Ralph Wiggum

The Ralph Wiggum loop is a **bounded autonomous execution pattern** that allows AI agents to execute multi-step plans with:
- **Max 10 iterations** (prevents infinite loops)
- **State persistence** (restartable on crash)
- **Dependency checking** (steps execute in correct order)
- **Retry with backoff** (handles transient failures)
- **Human escalation** (blocks on permanent failures)

**Named after Ralph Wiggum** because the agent enthusiastically attempts tasks repeatedly but has a hard limit to prevent runaway behavior.

---

## Architecture

```
Plan.md (approved) → Plan Executor (plan_executor.py)
                            ↓
                   Initialize ExecutionState
                   (iterations_remaining=10)
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
       Check Dependencies            Execute Step
              ↓                           ↓
       All met?                    Success? ───→ Mark [x], decrement iteration
              │                           │
              No                         No (retry 3x)
              ↓                           ↓
        Mark blocked                 Mark [!], escalate
              ↓                           ↓
       Escalate to                vault/Needs_Action/
      vault/Needs_Action/
              ↓
       iterations_remaining == 0? ───→ Escalate (max iterations)
              │
             No
              ↓
         Next Step ──→ Loop back
```

---

## Quick Start

### 1. Plan Structure

```markdown
<!-- vault/Plans/PLAN_client_onboarding_001.md -->
---
plan_id: plan_client_onboarding_001
objective: "Onboard new client - draft intro email, create calendar invite, post LinkedIn announcement"
total_steps: 3
completed_steps: 0
status: awaiting_approval
approval_required: true
iterations_used: 0
max_iterations: 10
---

# Plan: Client Onboarding - Acme Corp

**Objective:** Complete new client onboarding for Acme Corp

## Steps

- [ ] **Step 1:** Draft intro email to client (action_type: mcp_email)
  - Dependencies: none
  - MCP Server: email-mcp
  - Tool: send_email
  - Params: {to: "client@acme.com", subject: "Welcome!", body: "..."}

- [ ] **Step 2:** Create calendar invite for kickoff meeting (action_type: create_file)
  - Dependencies: step_1
  - File: vault/Pending_Approval/Calendar/kickoff_invite.md

- [ ] **Step 3:** Post LinkedIn announcement (action_type: mcp_linkedin)
  - Dependencies: step_1, step_2
  - MCP Server: linkedin-mcp
  - Tool: create_post
  - Params: {text: "Excited to welcome Acme Corp..."}
```

### 2. Plan Executor Implementation

```python
# agent_skills/plan_executor.py
from dataclasses import dataclass
from typing import List, Optional
import time

@dataclass
class ExecutionState:
    plan_id: str
    current_step: int
    iterations_remaining: int
    last_action: str
    last_action_timestamp: str
    loop_start_time: str
    status: str  # executing | completed | blocked | escalated

class RalphWiggumLoop:
    """Autonomous multi-step plan executor with bounded iterations"""

    def __init__(self, plan_path: str, max_iterations: int = 10):
        self.plan_path = plan_path
        self.plan = self.load_plan(plan_path)
        self.max_iterations = max_iterations

        # Initialize or load execution state
        state_path = f"vault/In_Progress/{self.plan['plan_id']}/state.md"
        if os.path.exists(state_path):
            self.state = self.load_state(state_path)
        else:
            self.state = ExecutionState(
                plan_id=self.plan['plan_id'],
                current_step=1,
                iterations_remaining=max_iterations,
                last_action="initialized",
                last_action_timestamp=datetime.utcnow().isoformat(),
                loop_start_time=datetime.utcnow().isoformat(),
                status="executing"
            )

    def execute(self):
        """
        Main execution loop

        Returns:
            bool: True if plan completed, False if blocked/escalated
        """
        print(f"🔄 Starting Ralph Wiggum loop for {self.plan['objective']}")
        print(f"   Max iterations: {self.max_iterations}")

        while self.state.iterations_remaining > 0:
            print(f"\n--- Iteration {self.max_iterations - self.state.iterations_remaining + 1}/{self.max_iterations} ---")

            # Get current step
            step = self.plan['steps'][self.state.current_step - 1]

            # Check dependencies
            if not self.check_dependencies(step):
                print(f"⏸️  Step {self.state.current_step} blocked - dependencies not met")
                self.handle_blocked_step(step)
                return False

            # Execute step
            try:
                self.execute_step(step)

                # Mark step complete
                self.mark_step_complete(step)

                # Update state
                self.state.current_step += 1
                self.state.iterations_remaining -= 1
                self.state.last_action = f"completed step {step['step_num']}"
                self.save_state()

                # Check if all steps complete
                if self.state.current_step > self.plan['total_steps']:
                    print("✅ All steps complete!")
                    self.handle_plan_complete()
                    return True

            except Exception as e:
                print(f"❌ Step {self.state.current_step} failed: {e}")

                # Retry with exponential backoff
                if not self.retry_step(step):
                    # All retries failed - escalate
                    self.handle_step_failure(step, e)
                    return False

        # Max iterations reached - escalate
        print(f"⚠️  Max iterations ({self.max_iterations}) reached - escalating")
        self.handle_max_iterations_escalation()
        return False

    def check_dependencies(self, step: dict) -> bool:
        """Check if step dependencies are met"""
        dependencies = step.get('dependencies', [])

        if not dependencies or dependencies == ['none']:
            return True

        # Check each dependency step is completed
        for dep in dependencies:
            dep_num = int(dep.replace('step_', ''))
            dep_step = self.plan['steps'][dep_num - 1]

            if not dep_step.get('completed', False):
                return False

        return True

    def execute_step(self, step: dict):
        """Execute a single plan step"""
        action_type = step['action_type']

        if action_type.startswith('mcp_'):
            # Invoke MCP server
            self.execute_mcp_action(step)

        elif action_type == 'create_file':
            # Create file in vault
            self.execute_file_creation(step)

        elif action_type == 'notify_human':
            # Create notification for human
            self.execute_human_notification(step)

        else:
            raise ValueError(f"Unknown action_type: {action_type}")

    def execute_mcp_action(self, step: dict):
        """Invoke MCP server for step action"""
        from agent_skills.mcp_client import call_mcp_tool

        # Extract MCP details
        server = step['mcp_server']
        tool = step['tool']
        params = step['params']

        # Invoke MCP
        result = call_mcp_tool(server, tool, params)

        # Log MCP action
        log_mcp_action(
            mcp_server=server,
            action=tool,
            outcome="success",
            plan_id=self.plan['plan_id'],
            step_num=step['step_num']
        )

        # Store result in step
        step['mcp_result'] = result

    def execute_file_creation(self, step: dict):
        """Create vault file as step action"""
        file_path = step['file_path']
        content = step.get('content', '')

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"📄 Created file: {file_path}")

    def execute_human_notification(self, step: dict):
        """Create notification for human action"""
        notification_path = f"vault/Needs_Action/plan_notification_{self.plan['plan_id']}_step_{step['step_num']}.md"

        content = f"""---
plan_id: {self.plan['plan_id']}
step_num: {step['step_num']}
action_required: true
---

# Human Action Required

**Plan:** {self.plan['objective']}
**Step:** {step['description']}

{step.get('notification_message', 'Manual action required - see plan for details')}
"""

        with open(notification_path, 'w') as f:
            f.write(content)

        print(f"📢 Created notification: {notification_path}")

    def mark_step_complete(self, step: dict):
        """Mark step as [x] in Plan.md"""
        step['completed'] = True

        # Update Plan.md file
        plan_content = open(self.plan_path).read()

        # Replace checkbox: - [ ] → - [x]
        step_pattern = f"- \\[ \\] \\*\\*Step {step['step_num']}:\\*\\*"
        step_replacement = f"- [x] **Step {step['step_num']}:**"

        updated_content = re.sub(step_pattern, step_replacement, plan_content)

        with open(self.plan_path, 'w') as f:
            f.write(updated_content)

        # Update plan completion count
        self.plan['completed_steps'] += 1

    def retry_step(self, step: dict, max_retries: int = 3) -> bool:
        """Retry failed step with exponential backoff"""
        for attempt in range(max_retries):
            try:
                # Wait with exponential backoff: 5s, 10s, 20s
                if attempt > 0:
                    wait_time = 5 * (2 ** attempt)
                    print(f"⏳ Retry {attempt + 1}/{max_retries} in {wait_time}s...")
                    time.sleep(wait_time)

                # Retry execution
                self.execute_step(step)
                print(f"✅ Step succeeded on retry {attempt + 1}")
                return True

            except Exception as e:
                print(f"❌ Retry {attempt + 1} failed: {e}")

        return False

    def handle_step_failure(self, step: dict, error: Exception):
        """Handle permanent step failure - escalate to human"""
        # Mark step as [!] in Plan.md
        step['status'] = 'failed'

        plan_content = open(self.plan_path).read()
        step_pattern = f"- \\[ \\] \\*\\*Step {step['step_num']}:\\*\\*"
        step_replacement = f"- [!] **Step {step['step_num']}:** (FAILED)"

        updated_content = re.sub(step_pattern, step_replacement, plan_content)

        with open(self.plan_path, 'w') as f:
            f.write(updated_content)

        # Create escalation file
        escalation_path = f"vault/Needs_Action/plan_blocked_{self.plan['plan_id']}.md"

        content = f"""---
plan_id: {self.plan['plan_id']}
step_num: {step['step_num']}
severity: high
action_required: true
---

# Plan Blocked - Step Failed

**Plan:** {self.plan['objective']}
**Blocked Step:** {step['description']}

**Error:** {str(error)}

**Recovery Instructions:**
1. Review step details in [[{os.path.basename(self.plan_path)}]]
2. Fix the underlying issue
3. Restart plan execution

**Full Error Details:**
```
{traceback.format_exc()}
```
"""

        with open(escalation_path, 'w') as f:
            f.write(content)

        # Update state
        self.state.status = "blocked"
        self.save_state()

        print(f"⚠️  Plan blocked - escalated to: {escalation_path}")

    def handle_max_iterations_escalation(self):
        """Handle max iterations reached - escalate"""
        escalation_path = f"vault/Needs_Action/plan_escalated_{self.plan['plan_id']}.md"

        content = f"""---
plan_id: {self.plan['plan_id']}
severity: medium
action_required: true
max_iterations_reached: true
---

# Plan Escalated - Max Iterations Reached

**Plan:** {self.plan['objective']}
**Iterations Used:** {self.max_iterations}

The plan has reached the maximum iteration limit ({self.max_iterations}) without completing all steps.

**Current Progress:**
- Completed: {self.plan['completed_steps']}/{self.plan['total_steps']} steps
- Current Step: {self.state.current_step}

**Next Actions:**
1. Review plan progress in [[{os.path.basename(self.plan_path)}]]
2. Check for circular dependencies or stuck steps
3. Manually complete remaining steps OR restart with higher iteration limit

**Full Iteration History:**
See vault/Logs/Plan_Execution/{self.plan['plan_id']}.md
"""

        with open(escalation_path, 'w') as f:
            f.write(content)

        # Update state
        self.state.status = "escalated"
        self.save_state()

        print(f"⚠️  Plan escalated - max iterations: {escalation_path}")

    def handle_plan_complete(self):
        """Handle successful plan completion"""
        # Update Plan.md status
        self.update_plan_status("completed")

        # Move to Done
        done_path = f"vault/Done/{os.path.basename(self.plan_path)}"
        shutil.move(self.plan_path, done_path)

        # Clean up execution state
        state_dir = f"vault/In_Progress/{self.plan['plan_id']}/"
        if os.path.exists(state_dir):
            shutil.rmtree(state_dir)

        # Update dashboard
        from agent_skills.dashboard_updater import update_dashboard
        update_dashboard()

        print(f"✅ Plan completed: {self.plan['objective']}")
        print(f"   Iterations used: {self.max_iterations - self.state.iterations_remaining}")

    def save_state(self):
        """Persist execution state to vault/In_Progress/"""
        state_dir = f"vault/In_Progress/{self.plan['plan_id']}/"
        os.makedirs(state_dir, exist_ok=True)

        state_path = os.path.join(state_dir, 'state.md')

        content = f"""---
plan_id: {self.state.plan_id}
current_step: {self.state.current_step}
iterations_remaining: {self.state.iterations_remaining}
last_action: {self.state.last_action}
last_action_timestamp: {self.state.last_action_timestamp}
loop_start_time: {self.state.loop_start_time}
status: {self.state.status}
---

# Execution State: {self.plan['objective']}

**Current Step:** {self.state.current_step}/{self.plan['total_steps']}
**Iterations Remaining:** {self.state.iterations_remaining}/{self.max_iterations}
**Status:** {self.state.status}

**Last Action:** {self.state.last_action}
**Timestamp:** {self.state.last_action_timestamp}
"""

        with open(state_path, 'w') as f:
            f.write(content)
```

---

## Plan Watcher

```python
# scripts/plan_watcher.py
from agent_skills.plan_executor import RalphWiggumLoop
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PlanApprovalHandler(FileSystemEventHandler):
    def on_moved(self, event):
        """Detect approved plans"""
        if not event.is_directory and 'Approved/Plans' in event.dest_path:
            # Parse plan
            plan_path = event.dest_path

            # Start Ralph Wiggum loop
            executor = RalphWiggumLoop(plan_path)
            executor.execute()

def watch_approved_plans():
    """Monitor vault/Approved/Plans/ for approved plans"""
    observer = Observer()
    observer.schedule(
        PlanApprovalHandler(),
        path="vault/Pending_Approval/",
        recursive=True
    )
    observer.start()

    print("📋 Plan watcher active")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
```

---

## Safety Features

### Bounded Iterations

```python
# Prevent infinite loops
MAX_ITERATIONS = 10  # Hard limit

# Escalate when limit reached
if iterations_remaining == 0:
    escalate_to_human()
```

### State Persistence

```python
# Restart-safe execution
state_path = f"vault/In_Progress/{plan_id}/state.md"

# On crash, resume from last saved state
if os.path.exists(state_path):
    state = load_state(state_path)
    resume_from_step(state.current_step)
```

### Dependency Validation

```python
# Never execute steps out of order
def check_dependencies(step):
    for dep in step['dependencies']:
        if not is_step_complete(dep):
            return False  # Block execution
    return True
```

---

## Testing

```python
# tests/integration/test_plan_execution.py
def test_ralph_wiggum_loop():
    """Test multi-step plan execution"""

    # Create test plan
    plan = create_test_plan(steps=[
        {"step_num": 1, "action_type": "mcp_email", "dependencies": []},
        {"step_num": 2, "action_type": "create_file", "dependencies": ["step_1"]},
        {"step_num": 3, "action_type": "mcp_linkedin", "dependencies": ["step_1", "step_2"]}
    ])

    # Mock MCP calls
    with patch('agent_skills.mcp_client.call_mcp_tool') as mock_mcp:
        mock_mcp.return_value = {"success": True}

        # Execute plan
        executor = RalphWiggumLoop(plan_path='test_plan.md')
        result = executor.execute()

        # Verify success
        assert result == True
        assert executor.state.current_step > executor.plan['total_steps']
        assert mock_mcp.call_count == 2  # email + linkedin (file doesn't use MCP)

def test_max_iterations_escalation():
    """Test escalation when max iterations reached"""

    # Create circular dependency plan (infinite loop)
    plan = create_circular_plan()

    executor = RalphWiggumLoop(plan_path='circular_plan.md', max_iterations=5)
    result = executor.execute()

    # Verify escalation
    assert result == False
    assert executor.state.status == "escalated"
    assert os.path.exists(f"vault/Needs_Action/plan_escalated_{executor.plan['plan_id']}.md")
```

---

## Configuration

```bash
# .env
MAX_PLAN_ITERATIONS=10  # Default: 10
PLAN_RETRY_ATTEMPTS=3   # Default: 3
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Plan stuck in loop** | Check vault/In_Progress/{plan_id}/state.md |
| **Max iterations reached** | Review plan for circular dependencies |
| **Step always failing** | Check vault/Needs_Action/plan_blocked_*.md |
| **State corrupted** | Delete vault/In_Progress/{plan_id}/ and restart |

---

## Key Files

- `agent_skills/plan_executor.py` - Ralph Wiggum loop implementation
- `scripts/plan_watcher.py` - Monitor approved plans
- `vault/Plans/` - Plan definitions
- `vault/In_Progress/` - Active execution state
- `vault/Needs_Action/plan_*.md` - Escalations

---

**Production Ready:** Bounded iterations, state persistence, dependency validation, retry logic, comprehensive error handling, human escalation patterns.

**Remember:** Like Ralph Wiggum, the agent is enthusiastic and helpful, but has firm limits to prevent chaos. Max 10 iterations ensures autonomous execution stays safe and bounded.
