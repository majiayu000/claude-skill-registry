/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: skill
version: 1.0.0
description: |
  [assert|neutral] skill skill for orchestration workflows [ground:given] [conf:0.95] [state:confirmed]
category: orchestration
tags:
- general
author: system
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute skill workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic orchestration processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "skill",
  category: "orchestration",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Aspectual",
  source: "Russian",
  force: "Complete or ongoing?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["skill", "orchestration", "workflow"],
  context: "user needs skill capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# When Automating Workflows Use Hooks Automation

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



---
name: when-automating-workflows-use-hooks-automation
trigger: "when user requests workflow automation, Git integration, or Claude Code operation hooks"
description: "Automated coordination, formatting, and learning from Claude Code operations using intelligent hooks with MCP integration for pre/post task automation"
version: 2.0.0
author: Base Template Generator
category: automation
tags:
  - hooks
  - automation
  - workflow
  - git-integration
  - memory-coordination
  - neural-training
agents:
  - coder
  - reviewer
  - system-architect
  - swarm-memory-manager
  - smart-agent
coordinator: adaptive-coordinator
memory_patterns:
  - swarm/hooks/pre-task-state
  - swarm/hooks/post-task-results
  - swarm/hooks/session-metrics
  - swarm/hooks/neural-patterns
  - swarm/hooks/automation-rules
success_criteria:
  - Hooks configured and active for all operations
  - Pre-task automation executing successfully
  - Post-task coordination working correctly
  - Session state persisted and restorable
  - Neural patterns training from operations
  - Git integration working seamlessly
---

## MCP Requirements

This skill operates using Claude Code's built-in tools only. No additional MCP servers required.

The hooks system (pre-task, post-task, post-edit, session management) is built into Claude Flow and requires no external MCPs. Memory coordination uses Memory MCP which is globally available to all skills.

## Trigger Conditions

Use this skill when:
- User requests automated workflow orchestration
- Git integration needed for commits and operations
- Pre/post task hooks required for coordination
- Session state management and persistence needed
- Neural pattern training from development operations
- Code formatting and quality checks automation
- Memory coordination across multi-agent workflows
- Cross-session context restoration required

## Skill Overview

This skill implements comprehensive hooks automation using Claude Flow's hooks system. It provides pre-operation setup (agent assignment, validation, resource preparation), post-operation automation (formatting, memory updates, neural training), and session management (state persistence, metrics tracking, context restoration).

## 7-Phase Skill-Forge Methodology

### Phase 1: Hooks System Initialization

**Objective**: Set up hooks infrastructure and configuration

**Agent**: `system-architect`

**Activities**:
- Configure Claude Flow hooks system
- Define hook triggers and automation rules
- Set up memory coordination patterns
- Configure Git integration for commits
- Establish quality thresholds
- Define neural training parameters
- Store hooks configuration in memory

**Memory Keys**:
- `swarm/hooks/automation-rules/pre-task-hooks`
- `swarm/hooks/automation-rules/post-task-hooks`
- `swarm/hooks/automation-rules/session-hooks`
- `swarm/hooks/automation-rules/git-integration`
- `swarm/hooks/automation-rules/neural-config`

**Script**:
```bash
npx claude-flow@alpha hooks pre-task --description "Hooks system initialization"
# Configure hooks
cat > .claude-flow-hooks.json << 'EOF'
{
  "preTask": {
    "enabled": true,
    "autoAssignAgents": true,
    "validateCommands": true,
    "prepareResources": true
  },
  "postTask": {
    "enabled": true,
    "autoFormat": true,
    "trainNeural": true,
    "updateMemory": true
  },
  "session": {
    "persistState": true,
    "trackMetrics": true,
    "exportSummary": true
  },
  "git": {
    "autoCommit": false,
    "commitMessageTemplate": true,
    "branchStrategy": "feature"
  }
}
EOF
npx claude-flow@alpha memory store "swarm/hooks/automation-rules/pre-task-hooks" "$(cat .claude-flow-hooks.json)"
npx claude-flow@alpha hooks notify --message "Hooks system initialized"
```

### Phase 2: Pre-Task Hook Automation

**Objective**: Automate operations before each task execution

**Agent**: `coder`

**Activities**

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/orchestration/skill/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "skill-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>SKILL_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
