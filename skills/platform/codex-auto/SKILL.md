/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: SKILL
version: 1.0.0
description: |
  [assert|neutral] Use Codex CLI's Full Auto mode for unattended sandboxed prototyping and scaffolding [ground:given] [conf:0.95] [state:confirmed]
category: platforms
tags:
- codex
- openai
- prototyping
- automation
- full-auto
author: system
cognitive_frame:
  primary: compositional
  goal_analysis:
    first_order: "Execute SKILL workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic platforms processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "SKILL",
  category: "platforms",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Compositional",
  source: "German",
  force: "Build from primitives?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["SKILL", "platforms", "workflow"],
  context: "user needs SKILL capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Codex Full Auto Skill

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Purpose
Leverage Codex CLI's Full Auto mode for unattended, sandboxed prototyping where the AI can autonomously read, write, and execute code without approval - perfect for rapid scaffolding and overnight builds.

## Unique Capability
**What Claude Code Can't Do**: Run completely autonomously without user approval for extended periods. Codex Full Auto mode can prototype entire features, fix broken builds, or scaffold projects while you're away - all in a secure sandbox.

## When to Use

### Perfect For:
✅ Rapid prototyping of new features
✅ Scaffolding entire projects (APIs, apps, tools)
✅ Fixing broken builds while you're away
✅ Automated refactoring tasks
✅ Generating boilerplate code
✅ "Set it and forget it" tasks
✅ Exploring implementation approaches

### Don't Use When:
❌ Need human oversight for critical decisions
❌ Working with production systems
❌ Requires network access (Full Auto disables network)
❌ Need to access resources outside project directory

## How It Works

Codex Full Auto mode:
- ✅ Reads/writes files automatically
- ✅ Executes commands in sandbox
- ✅ Iterates on its own output
- ⚠️ **Network disabled** for security
- ⚠️ **CWD only** - can't access outside project
- ⚠️ Uses macOS Seatbelt / Docker sandbox

## Usage

### Basic Auto Prototyping
```
/codex-auto "Create a REST API with user CRUD operations using Express and SQLite"
```

### Scaffolding
```
/codex-auto "Build a complete todo app with React frontend and Node.js backend, include tests"
```

### Overnight Task
```
/codex-auto "Refactor entire src/ directory to use TypeScript strict mode, fix all type errors"
```

## Safety

Full Auto runs in **secure sandbox**:
- Network: **DISABLED** (no external connections)
- Scope: **CWD only** (current working directory)
- Isolation: **Seatbelt (macOS) / Docker**
- Can't: Access parent dirs, make network calls, modify system

## Command Pattern
```bash
codex --full-auto "Detailed task description"
# Equivalent to: codex -a on-failure -s workspace-write
```

## Real Examples

### Example 1: API Scaffolding
```
/codex-auto "Create Express REST API with:
- User endpoints (CRUD)
- JWT authentication
- Input validation
- Error handling
- SQLite database
- Tests with Jest"

Result: Complete API in ~45 minutes
```

### Example 2: Refactoring
```
/codex-auto "Refactor all components in src/components to use hooks instead of class components, preserve all functionality"

Result: All components refactored, tests passing
```

---

**Note**: Use your ChatGPT Plus ($20/month) subscription. Recommended model: GPT-5-Codex for agentic tasks.

See `.claude/agents/codex-auto-agent.md` for full details.


---
*Promise: `<promise>SKILL_VERIX_COMPLIANT</promise>`*

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
  pattern: "skills/platforms/SKILL/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "SKILL-{session_id}",
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
