---
name: when-creating-skill-template-use-skill-builder
version: 1.0.0
description: Create new Claude Code Skills with proper YAML frontmatter, progressive disclosure structure, and complete directory organization
category: utilities
tags: [skill-creation, templates, yaml, documentation]
agents: [base-template-generator, coder]
difficulty: beginner
estimated_duration: 15-25min
success_criteria:
  - Valid YAML frontmatter
  - All required files created
  - Proper directory structure
  - Documentation complete
validation_method: skill_execution_test
dependencies:
  - claude-flow@alpha
outputs:
  - SKILL.md with YAML frontmatter
  - README.md
  - PROCESS.md
  - process-diagram.gv
---

# Skill Builder - Claude Code Skill Template Generator

## Overview

Creates new Claude Code Skills with proper structure, YAML frontmatter, progressive disclosure, and complete documentation. Ensures skills follow best practices and specification requirements.

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
${successCriteria}

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

**Step 2.3: Create PROCESS.md**
```markdown
# ${skillName} - Detailed Workflow

## Process Overview
${processOverview}

## Phase Breakdown
${phases.map(phase => `
### Phase ${phase.number}: ${phase.title}

**Objective**: ${phase.objective}
**Agent**: ${phase.agent}
**Duration**: ${phase.duration}

**Steps**:
${phase.steps.map((step, i) => `${i+1}. ${step}`).join('\n')}

**Outputs**: ${phase.outputs.join(', ')}
**Validation**: ${phase.validation}
`).join('\n---\n')}

## Workflow Diagram
[See process-diagram.gv]

## Integration Patterns
${integrationExamples}
```

**Step 2.4: Create process-diagram.gv**
```graphviz
digraph ${SkillName} {
    rankdir=TB;
    node [shape=box, style=filled, fillcolor=lightblue];

    start [label="Input", shape=ellipse, fillcolor=lightgreen];
    ${phases.map((p, i) => `
    phase${i+1} [label="Phase ${i+1}: ${p.title}\\n(${p.duration})\\nAgent: ${p.agent}", fillcolor=lightcoral];
    output${i+1} [label="${p.outputs.join('\\n')}", shape=parallelogram];
    `).join('\n')}
    end [label="Output", shape=ellipse, fillcolor=lightgreen];

    start -> phase1;
    ${phases.map((p, i) => `
    phase${i+1} -> output${i+1};
    output${i+1} -> phase${i+2 <= phases.length ? i+2 : 'end'};
    `).join('\n')}
}
```

### Validation Criteria
- [ ] All 4 files created
- [ ] YAML valid
- [ ] Content complete
- [ ] Diagram syntax correct

## Phase 3: Implement Functionality (8 min)

### Objective
Add implementation details and code examples

### Agent: Coder

**Step 3.1: Add Code Examples**
```javascript
// For each phase, add:
// - Implementation code snippets
// - Memory operations
// - Hook integrations
// - Script templates

const phaseImplementation = {
  codeExample: `
async function execute${phase.title}() {
  // Implementation
  await memory.store('${skillName}/${phase.key}', data);
  return result;
}
  `,
  hooks: `
npx claude-flow@alpha hooks pre-task --description "${phase.description}"
npx claude-flow@alpha hooks post-task --task-id "${phase.key}"
  `,
  scriptTemplate: `
#!/bin/bash
# ${phase.title}.sh
${phase.script}
  `
};
```

**Step 3.2: Add Memory Patterns**
```javascript
const memorySchema = {
  [`${skillName}/`]: {
    [`session-\${id}/`]: {
      ...phases.reduce((acc, phase) => ({
        ...acc,
        [phase.key]: { /* phase data */ }
      }), {})
    }
  }
};
```

**Step 3.3: Add Integration Examples**
```javascript
// How to use with other skills
const integrationExamples = {
  withSPARC: `${skillName} → SPARC workflow`,
  withCascade: `cascade: [${skillName}, next-skill]`,
  standalone: `npx claude-flow@alpha skill-run ${skillName}`
};
```

### Validation Criteria
- [ ] Code examples complete
- [ ] Memory schema defined
- [ ] Hooks integrated
- [ ] Script templates added

## Phase 4: Test Skill (5 min)

### Objective
Validate skill executes correctly

### Agent: Coder

**Step 4.1: Syntax Validation**
```bash
# Validate YAML
npx js-yaml SKILL.md

# Validate GraphViz
dot -Tsvg process-diagram.gv -o /dev/null

# Check file completeness
test -f SKILL.md && test -f README.md && test -f PROCESS.md && test -f process-diagram.gv
```

**Step 4.2: Execution Test**
```bash
# Try to run the skill
npx claude-flow@alpha skill-run ${skillName} --dry-run

# Check for errors
if [ $? -eq 0 ]; then
  echo "✅ Skill validation passed"
else
  echo "❌ Skill validation failed"
fi
```

**Step 4.3: Documentation Review**
```javascript
const documentationChecklist = {
  hasYAMLFrontmatter: true,
  hasOverview: true,
  hasPhases: phases.length > 0,
  hasValidation: true,
  hasMemorySchema: true,
  hasSuccessMetrics: true,
  hasIntegrationExamples: true
};

const allChecksPassed = Object.values(documentationChecklist).every(v => v === true);
```

### Validation Criteria
- [ ] YAML valid
- [ ] GraphViz valid
- [ ] All files present
- [ ] Dry-run successful

## Phase 5: Document Usage (2 min)

### Objective
Create usage guide and examples

### Agent: Base-Template-Generator

**Step 5.1: Add Usage Examples**
```markdown
## Usage Examples

### Basic Usage
\`\`\`bash
npx claude-flow@alpha skill-run ${skillName} \\
  --input "input.json" \\
  --output "output.json"
\`\`\`

### With Parameters
\`\`\`bash
npx claude-flow@alpha skill-run ${skillName} \\
  --param1 "value1" \\
  --param2 "value2"
\`\`\`

### Programmatic Usage
\`\`\`javascript
const result = await runSkill('${skillName}', {
  input: data,
  options: { ... }
});
\`\`\`
```

**Step 5.2: Add Troubleshooting**
```markdown
## Troubleshooting

### Issue: ${commonIssue1}
**Solution**: ${solution1}

### Issue: ${commonIssue2}
**Solution**: ${solution2}
```

**Step 5.3: Generate Completion Report**
```javascript
const completionReport = {
  skillName: skillRequirements.name,
  filesCreated: [
    'SKILL.md',
    'README.md',
    'PROCESS.md',
    'process-diagram.gv'
  ],
  linesOfCode: calculateLOC(),
  estimatedDuration: skillRequirements.estimatedDuration,
  agentsRequired: skillRequirements.agents.length,
  phasesImplemented: phases.length,
  validationStatus: 'PASSED',
  readyForUse: true
};

await memory.store('skill-builder/completion', completionReport);
```

### Validation Criteria
- [ ] Usage examples added
- [ ] Troubleshooting guide complete
- [ ] Completion report generated
- [ ] Ready for use

## Success Metrics

- All 4 files created
- YAML validation passes
- Skill executes without errors
- Documentation complete
- Ready for integration

## Memory Schema

```javascript
{
  "skill-builder/": {
    "session-${id}/": {
      "requirements": {},
      "phase-structure": [],
      "generated-files": [],
      "validation-results": {},
      "completion": {}
    }
  }
}
```

## Common Patterns

### Quick Skill Template
```bash
npx claude-flow@alpha skill-run skill-builder \
  --name "my-new-skill" \
  --category "utilities" \
  --agents "coder,tester" \
  --phases "3"
```

### From Existing Workflow
```bash
# Convert workflow to skill
npx claude-flow@alpha skill-builder \
  --from-workflow "workflow.json" \
  --output-dir ".claude/skills/utilities/"
```

## Skill Completion

Outputs:
1. **SKILL.md**: Complete skill specification
2. **README.md**: Quick start guide
3. **PROCESS.md**: Detailed workflow
4. **process-diagram.gv**: Visual process diagram

Skill complete when all files created and validation passes.
