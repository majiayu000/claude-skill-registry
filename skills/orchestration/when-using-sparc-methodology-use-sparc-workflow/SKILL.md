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

# When Using SPARC Methodology Use SPARC Workflow

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



---
name: when-using-sparc-methodology-use-sparc-workflow
trigger: "when user requests SPARC methodology, systematic development, or TDD workflow"
description: "Complete SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology workflow with multi-agent coordination for systematic test-driven development"
version: 2.0.0
author: Base Template Generator
category: methodology
tags:
  - sparc
  - methodology
  - tdd
  - systematic-development
  - multi-phase
agents:
  - researcher (specification)
  - planner (pseudocode)
  - system-architect (architecture)
  - coder (refinement)
  - tester (validation)
  - reviewer (quality)
  - api-docs (documentation)
coordinator: hierarchical-coordinator
memory_patterns:
  - swarm/sparc/specification
  - swarm/sparc/pseudocode
  - swarm/sparc/architecture
  - swarm/sparc/refinement
  - swarm/sparc/completion
success_criteria:
  - Detailed specification documented
  - Pseudocode algorithm designed
  - System architecture defined
  - Implementation refined through TDD
  - All tests passing with ≥90% coverage
  - Integration complete and validated
  - Comprehensive documentation generated
---

## Trigger Conditions

Use this skill when:
- User requests SPARC methodology application
- Systematic development workflow needed
- Test-driven development (TDD) approach required
- Complex feature requiring phased approach
- Architecture-first development desired
- Quality gates and validation at each phase needed
- Comprehensive documentation required
- Multi-agent coordinated development

## Skill Overview

SPARC is a systematic development methodology with 5 phases: Specification (requirements), Pseudocode (algorithm design), Architecture (system design), Refinement (TDD implementation), and Completion (integration & documentation). This skill orchestrates all phases with specialized agents coordinating through hierarchical topology and shared memory.

## SPARC Methodology Overview

**S** - Specification: Capture requirements and define success criteria
**P** - Pseudocode: Design algorithm and logic flow
**A** - Architecture: Design system structure and components
**R** - Refinement: Implement through TDD with iterative improvement
**C** - Completion: Integration, validation, and documentation

## 7-Phase Skill-Forge Methodology

### Phase 1: Specification (Requirements Analysis)

**Objective**: Capture comprehensive requirements and define success criteria

**Agent**: `researcher` (specification specialist)

**Activities**:
- Gather and analyze user requirements
- Define functional and non-functional requirements
- Identify constraints and dependencies
- Define acceptance criteria and test scenarios
- Document edge cases and error conditions
- Create requirements specification document
- Store specification in memory

**Memory Keys**:
- `swarm/sparc/specification/requirements`
- `swarm/sparc/specification/acceptance-criteria`
- `swarm/sparc/specification/constraints`
- `swarm/sparc/specification/edge-cases`

**Script**:
```bash
npx claude-flow@alpha hooks pre-task --description "SPARC Phase 1: Specification"
npx claude-flow@alpha hooks session-restore --session-id "sparc-${PROJECT_ID}"

# Capture requirements
cat > docs/sparc/01-specification.md << 'EOF'
# SPARC Phase 1: Specification

## Project: ${PROJECT_NAME}

### Functional Requirements
1. [FR1] User authentication with email/password
2. [FR2] JWT token-based session management
3. [FR3] Password reset via email
4. [FR4] Role-based access control (RBAC)

### Non-Functional Requirements
1. [NFR1] Response time < 200ms for auth endpoints
2. [NFR2] Support 1000 concurrent users
3. [NFR3] 99.9% uptime SLA

### Constraints
- Must use existing PostgreSQL database
- Must integrate with existing email service
- Must follow OWASP security guidelines

### Acceptance Criteria
- User can register with em

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
