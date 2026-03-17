---
skill_name: phase-gate
activation_code: PHASE_GATE_V1
version: 1.0.0
phase: all
prerequisites:
  - Phase transition detected
  - phase-agents.json configured
outputs:
  - .claude/phase-state.json (updated)
  - Selected executor/auditor agents
description: |
  Manages pre-phase and post-phase agent selection gates.
  Core skill for agent-first pipeline execution.
---

# Phase Gate Skill

## Activation

Triggered automatically at every phase transition:

```
[ACTIVATE:PHASE_GATE_V1]
Parameters:
  gate_type: pre | post
  phase: 1-12
```

## Purpose

Facilitate human-Claude conversations for agent selection at phase boundaries:

1. **Pre-Phase Gate**: Select executor agents before phase begins
2. **Post-Phase Gate**: Select auditor agents after phase completes

## Agent-First Philosophy

In the agent-first pipeline:
- **Agents execute phases**, not skills
- **Skills are playbooks** that guide agent behavior
- **Humans approve agent selection** at every boundary
- **PhD-experts can be invented** when gaps exist

## Execution Flow

### Pre-Phase Gate

```
╔═══════════════════════════════════════════════════════════════════════╗
║              PRE-PHASE GATE: Phase {N} - {Phase Name}                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Phase {N} is about to begin.                                         ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ DEFAULT EXECUTORS                                               │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ PRIMARY:                                                        │   ║
║  │   • {executor-1} - {description}                                │   ║
║  │                                                                 │   ║
║  │ SUPPORT:                                                        │   ║
║  │   • {executor-2} - {description}                                │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ OPTIONAL SPECIALISTS                                            │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │   • {optional-1} - {description}                                │   ║
║  │   • {optional-2} - {description}                                │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ TECH-SPECIFIC (from PRD)                                        │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │   • {tech-agent-1} - for {technology}                           │   ║
║  │   • {tech-agent-2} - for {technology}                           │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [A] Accept defaults                                                   ║
║  [C] Customize selection (add/remove agents)                          ║
║  [I] Invent new PhD-expert for this phase                             ║
║  [V] View agent details                                                ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Pre-Phase Gate Steps

1. **Load Phase Configuration**
   ```javascript
   const phaseConfig = require('.claude/phase-agents.json').phases[phaseNum];
   const techStack = require('.claude/prd-context.json').techStack;
   ```

2. **Determine Default Executors**
   - Read `phaseConfig.executors.default`
   - Add tech-specific agents based on PRD
   - Present to user

3. **Handle User Choice**
   - **Accept**: Proceed with defaults
   - **Customize**: Interactive add/remove
   - **Invent**: Activate `AGENT_INVENTOR_V1`
   - **View**: Show agent system prompts

4. **Lock Executor Selection**
   ```json
   {
     "phase": 6,
     "gate": "pre",
     "executors": ["spec-generator", "typescript-pro", "reactjs-expert"],
     "locked_at": "2025-01-15T10:30:00Z",
     "approved_by": "human"
   }
   ```

5. **Emit Signal**
   ```
   [SIGNAL:PRE_PHASE_{N}_COMPLETE]
   [ACTIVATE:{PHASE_SKILL}]
   ```

### Post-Phase Gate

```
╔═══════════════════════════════════════════════════════════════════════╗
║              POST-PHASE GATE: Phase {N} - {Phase Name}                ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Phase {N} has completed.                                              ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ PHASE OUTPUTS                                                   │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │   • {output-1}: {description}                                   │   ║
║  │   • {output-2}: {description}                                   │   ║
║  │   • {output-3}: {description}                                   │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ DEFAULT AUDITORS                                                │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │   • {auditor-1} - {what they verify}                            │   ║
║  │   • {auditor-2} - {what they verify}                            │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ RECOMMENDED BASED ON OUTPUTS                                    │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │   • {recommended-1} - because {reason}                          │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [A] Accept defaults                                                   ║
║  [C] Customize auditor selection                                      ║
║  [I] Invent specialist auditor for this output                        ║
║  [S] Skip audit (not recommended)                                      ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Post-Phase Gate Steps

1. **Analyze Phase Outputs**
   - Read phase output files
   - Determine what was produced
   - Identify potential risk areas

2. **Recommend Auditors**
   - Start with `phaseConfig.auditors.default`
   - Add recommendations based on output content:
     - Security-sensitive → `security-auditor`
     - Data operations → `data-integrity-auditor`
     - API changes → `api-compatibility-auditor`
     - Performance-critical → `performance-auditor`

3. **Handle User Choice**
   - **Accept**: Run default auditors
   - **Customize**: Add/remove auditors
   - **Invent**: Create specialist auditor
   - **Skip**: Require confirmation, log risk

4. **Lock Auditor Selection**
   ```json
   {
     "phase": 6,
     "gate": "post",
     "auditors": ["spec-reviewer", "security-auditor"],
     "locked_at": "2025-01-15T14:30:00Z",
     "approved_by": "human"
   }
   ```

5. **Execute Audit**
   - Run each auditor against phase outputs
   - Collect findings
   - Determine pass/fail

6. **Handle Audit Results**

   **If PASS:**
   ```
   ╔═══════════════════════════════════════════════════════════════════════╗
   ║                        AUDIT PASSED ✓                                 ║
   ╠═══════════════════════════════════════════════════════════════════════╣
   ║                                                                        ║
   ║  Phase {N} outputs verified by:                                        ║
   ║    ✓ {auditor-1}: PASSED                                               ║
   ║    ✓ {auditor-2}: PASSED                                               ║
   ║                                                                        ║
   ║  Proceeding to Phase {N+1}                                             ║
   ║                                                                        ║
   ╚═══════════════════════════════════════════════════════════════════════╝
   ```

   **If FAIL:**
   ```
   ╔═══════════════════════════════════════════════════════════════════════╗
   ║                        AUDIT FAILED ✗                                 ║
   ╠═══════════════════════════════════════════════════════════════════════╣
   ║                                                                        ║
   ║  Phase {N} audit found issues:                                         ║
   ║                                                                        ║
   ║  {auditor-1}: FAILED                                                   ║
   ║    • Issue 1: {description}                                            ║
   ║    • Issue 2: {description}                                            ║
   ║                                                                        ║
   ║  {auditor-2}: PASSED                                                   ║
   ║                                                                        ║
   ╠═══════════════════════════════════════════════════════════════════════╣
   ║  [R] Remediate issues and re-audit                                     ║
   ║  [O] Override (requires justification)                                 ║
   ║  [B] Back to phase execution                                           ║
   ╚═══════════════════════════════════════════════════════════════════════╝
   ```

7. **Emit Signal**
   ```
   [SIGNAL:POST_PHASE_{N}_COMPLETE]
   [SIGNAL:PHASE_{N}_AUDITED]
   [ACTIVATE:PHASE_GATE_V1] gate_type=pre, phase={N+1}
   ```

## State Management

Track gate states in `.claude/phase-state.json`:

```json
{
  "current_phase": 6,
  "gates": {
    "1": {
      "pre": { "status": "complete", "executors": [...], "timestamp": "..." },
      "post": { "status": "complete", "auditors": [...], "passed": true }
    },
    "6": {
      "pre": { "status": "complete", "executors": [...] },
      "post": { "status": "pending" }
    }
  },
  "invented_agents": [
    { "name": "graphql-phd-expert", "phase": 6, "role": "executor" }
  ]
}
```

## Quick Confirm Mode

For phases where defaults are well-suited:

```
Phase 5 Pre-Gate: [taskmaster-integrator, assignment-agent]
Quick confirm? [Y/n]:
```

User can press Enter to accept, or 'n' to enter full selection mode.

## Agent Availability Check

Before presenting agents, verify availability (agents are bundled in `agents/`):

```bash
# Check if agent exists in local agents directory
if [ ! -f "agents/*/{agent}.md" ]; then
  echo "Agent not found in local pool"
  # Consider inventing a PhD-expert if needed
fi

# Sync to .claude/agents/ if needed
./scripts/pull-agents.sh --config .claude/agent-config.json
```

## Emergency Overrides

For critical situations:

```
[OVERRIDE:SKIP_AUDIT]
Justification: {required}
Risk acknowledged: {yes|no}
Logged at: .claude/audit-log.json
```

Overrides are logged and flagged for review.

## Signals

| Signal | Meaning |
|--------|---------|
| `PRE_PHASE_{N}_COMPLETE` | Executors selected, phase can begin |
| `POST_PHASE_{N}_COMPLETE` | Auditors selected, audit can begin |
| `PHASE_{N}_AUDITED` | Audit complete (pass or overridden) |
| `AGENT_SELECTION_TIMEOUT` | No response, defaults applied |

## Integration with Phase Skills

Phase skills now receive executor context:

```json
{
  "phase": 6,
  "skill": "spec-gen",
  "executors": [
    {"agent": "spec-generator", "role": "primary"},
    {"agent": "typescript-pro", "role": "tech-specific"}
  ],
  "mode": "agent-first"
}
```

The skill becomes the "playbook" that agents follow, not the executor.

## Completion

Outputs:
- Updated `.claude/phase-state.json`
- Agent selection logged
- Audit results recorded (for post-gate)

Transitions to:
- Phase execution (after pre-gate)
- Next phase pre-gate (after post-gate audit passes)
