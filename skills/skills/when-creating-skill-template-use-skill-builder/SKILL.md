/*============================================================================*/
/* WHEN-CREATING-SKILL-TEMPLATE-USE-SKILL-BUILDER SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-creating-skill-template-use-skill-builder
version: 1.0.0
description: |
  [assert|neutral] Create new Claude Code Skills with proper YAML frontmatter, progressive disclosure structure, and complete directory organization [ground:given] [conf:0.95] [state:confirmed]
category: utilities
tags:
- skill-creation
- templates
- yaml
- documentation
author: system
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute when-creating-skill-template-use-skill-builder workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic utilities processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-creating-skill-template-use-skill-builder",
  category: "utilities",
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
  keywords: ["when-creating-skill-template-use-skill-builder", "utilities", "workflow"],
  context: "user needs when-creating-skill-template-use-skill-builder capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Skill Builder - Claude Code Skill Template Generator

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

Creates new Claude Code Skills with proper structure, YAML frontmatter, progressive disclosure, and complete documentation. Ensures skills follow best practices and specification requirements.

## MCP Requirements

This skill operates using Claude Code's built-in tools only. No additional MCP servers required.

Skill creation uses file operations (Read, Write, Edit, Glob) and directory creation which are core Claude Code capabilities.

## When to Use

- Creating new reusable skills
- Need skill template/boilerplate
- Building skill library
- Standardizing skill format

## Phase 1: Design Skill Structure (5 min)

### Objective
Define skill components and metadata

### Agent: Base-Template-Generator

**Step 1.1: Gather Requirements**
```javascript
const skillRequirements = {
  name: 'when-[condition]-use-[skill-name]',
  category: 'utilities|development|testing|machine-learning',
  description: 'Clear one-sentence purpose',
  agents: ['agent1', 'agent2'],
  phases: [
    { name: 'Phase 1', duration: '5min', objective: '...' },
    // ...
  ],
  triggers: ['When X happens', 'When Y is needed'],
  outputs: ['file1.json', 'report.md']
};

await memory.store('skill-builder/requirements', skillRequirements);
```

**Step 1.2: Define YAML Frontmatter**
```yaml
---
name: when-[trigger]-use-[skill-name]
version: 1.0.0
description: Single sentence describing purpose
category: utilities
tags: [tag1, tag2, tag3]
agents: [agent1, agent2]
difficulty: beginner|intermediate|advanced
estimated_duration: 15-30min
success_criteria:
  - Criterion 1
  - Criterion 2
validation_method: test_type
dependencies:
  - claude-flow@alpha
  - other-dependency
prerequisites:
  - Required condition 1
outputs:
  - output-file-1
  - output-file-2
triggers:
  - Trigger condition 1
  - Trigger condition 2
---
```

**Step 1.3: Plan Phase Structure**
```javascript
const phaseStructure = skillRequirements.phases.map((phase, i) => ({
  number: i + 1,
  title: phase.name,
  objective: phase.objective,
  duration: phase.duration,
  agent: phase.agent,
  steps: phase.steps,
  validation: phase.validation,
  memoryPattern: phase.memoryPattern,
  scriptTemplate: phase.scriptTemplate
}));

await memory.store('skill-builder/phase-structure', phaseStructure);
```

### Validation Criteria
- [ ] Name follows convention
- [ ] All metadata defined
- [ ] Phases planned
- [ ] Agents identified

## Phase 2: Generate Template (5 min)

### Objective
Create skill file structure and boilerplate

### Agent: Base-Template-Generator

**Step 2.1: Create SKILL.md**
```markdown
---
[YAML frontmatter from Phase 1]
---

# ${skillName} - ${shortDescription}

## Overview
${detailedDescription}

## When to Use
${triggers.map(t => `- ${t}`).join('\n')}

## Phase 1: ${phase1.title}

### Objective
${phase1.objective}

### Agent: ${phase1.agent}

**Step 1.1: ${step1.title}**
\`\`\`javascript
${step1.code}
\`\`\`

**Step 1.2: ${step2.title}**
[Implementation details]

### Validation Criteria
${validation.map(v => `- [ ] ${v}`).join('\n')}

### Hooks Integration
\`\`\`bash
npx claude-flow@alpha hooks pre-task --description "${phase1.description}"
\`\`\`

## [Repeat for all phases]

## Success Metrics
- [assert|neutral] ${successCriteria} [ground:acceptance-criteria] [conf:0.90] [state:provisional]

## Memory Schema
\`\`\`javascript
${memorySchema}
\`\`\`

## Skill Completion
${completionCriteria}
```

**Step 2.2: Create README.md**
```markdown
# ${skillName} - Quick Start Guide

## Purpose
${purpose}

## When to Use
${triggers}

## Quick Start
\`\`\`bash
npx claude-flow@alpha skill-run ${skillName}
\`\`\`

## ${phases.length}-Phase Process
${phases.map((p, i) => `${i+1}. **${p.title}** (${p.duration}) - ${p.objective}`).join('\n')}

## Expected Output
${outputExample}

## Success Criteria
${successCriteria}

For detailed documentation, see SKILL.md
```

**

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
  pattern: "skills/utilities/when-creating-skill-template-use-skill-builder/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-creating-skill-template-use-skill-builder-{session_id}",
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

[commit|confident] <promise>WHEN_CREATING_SKILL_TEMPLATE_USE_SKILL_BUILDER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
