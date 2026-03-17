---
name: agent-capability-assessor
description: Assesses agent capabilities by analyzing agent files and determining what tasks they can handle. Use when you need to evaluate if an existing agent can handle a task or if a new agent is needed. Reviews agent descriptions, skills, and workflows to determine capability match.
---

# Agent Capability Assessor Skill

## Instructions

1. Review the agent file(s) to understand capabilities
2. Analyze agent description, skills, and workflow
3. Compare agent capabilities to task requirements
4. Determine if agent can handle the task effectively
5. Identify capability gaps or strengths
6. Recommend whether to use existing agent or create new one
7. Provide capability assessment report

## Assessment Process

### Step 1: Read Agent File
- Read the agent's markdown file from `.cursor/agents/`
- Understand agent's name, description, and purpose
- Review agent's core principles and workflow
- Note agent's available skills and capabilities

### Step 2: Analyze Capabilities
- Extract key capabilities from agent description
- Identify what types of tasks the agent handles
- Note any limitations or constraints
- Understand agent's workflow and process

### Step 3: Compare to Task Requirements
- Review task description and requirements
- Identify required capabilities for the task
- Match task requirements to agent capabilities
- Note any gaps or mismatches

### Step 4: Make Assessment
- Determine if agent can handle task (Yes/No/Partial)
- Assess quality of match (Excellent/Good/Fair/Poor)
- Identify capability gaps
- Recommend action (Use existing / Create new / Enhance existing)

## Capability Assessment Criteria

### Excellent Match
- Agent's primary purpose aligns with task
- Agent has all required skills
- Agent's workflow fits task requirements
- No significant gaps

### Good Match
- Agent can handle task with minor adjustments
- Agent has most required skills
- Agent's workflow mostly fits
- Minor gaps that can be worked around

### Fair Match
- Agent can handle task but not ideal
- Agent has some required skills
- Agent's workflow partially fits
- Some gaps that may impact effectiveness

### Poor Match
- Agent is not well-suited for task
- Agent lacks key required skills
- Agent's workflow doesn't fit
- Significant gaps that impact effectiveness

### No Match
- Agent cannot handle task
- Agent lacks required capabilities
- Task is outside agent's domain

## Assessment Output Format

```markdown
## Agent Capability Assessment

### Agent: [agent-name]
**File**: `.cursor/agents/[agent-name].md`

### Agent Capabilities
- [Capability 1]
- [Capability 2]
- [Capability 3]

### Task Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

### Capability Match Analysis
**Overall Match**: [Excellent/Good/Fair/Poor/No Match]

**Strengths**:
- [Strength 1]
- [Strength 2]

**Gaps**:
- [Gap 1]
- [Gap 2]

**Recommendation**: [Use existing / Create new / Enhance existing]

**Rationale**: [Explanation of recommendation]
```

## Examples

### Example 1: Good Match

**Input**: Assess if `implementation-engineer` can handle "Implement user login API endpoint"

**Output**:
```markdown
## Agent Capability Assessment

### Agent: implementation-engineer
**File**: `.cursor/agents/implementation-engineer.md`

### Agent Capabilities
- Implements tasks from scrum-master
- Handles both frontend and backend implementation
- Uses api-implementer skill for API endpoints
- Submits to code review and iterates
- Commits changes when approved

### Task Requirements
- Implement API endpoint
- Handle authentication logic
- Write tests
- Submit for review

### Capability Match Analysis
**Overall Match**: Excellent

**Strengths**:
- Primary purpose is implementation
- Has api-implementer skill for API endpoints
- Handles backend implementation
- Includes review and commit workflow

**Gaps**: None

**Recommendation**: Use existing agent

**Rationale**: Implementation-engineer is perfectly suited for this task. It has the api-implementer skill and handles the full implementation workflow including review and commit.
```

### Example 2: Poor Match

**Input**: Assess if `ui-ux-designer` can handle "Set up PostgreSQL database schema"

**Output**:
```markdown
## Agent Capability Assessment

### Agent: ui-ux-designer
**File**: `.cursor/agents/ui-ux-designer.md`

### Agent Capabilities
- Creates design specifications
- Focuses on UI/UX design
- Works with design systems
- Creates markdown design specs (not code)

### Task Requirements
- Set up database schema
- Create tables and relationships
- Write SQL migrations
- Configure database

### Capability Match Analysis
**Overall Match**: No Match

**Strengths**: None relevant

**Gaps**:
- Agent focuses on design, not database work
- Agent creates design specs, not code
- Agent has no database-related skills
- Task is outside agent's domain

**Recommendation**: Create new agent or use infrastructure-engineer

**Rationale**: ui-ux-designer is focused on UI/UX design work and cannot handle database schema setup. This task should be handled by infrastructure-engineer or a specialized database agent.
```

### Example 3: Partial Match

**Input**: Assess if `implementation-engineer` can handle "Design user dashboard layout"

**Output**:
```markdown
## Agent Capability Assessment

### Agent: implementation-engineer
**File**: `.cursor/agents/implementation-engineer.md`

### Agent Capabilities
- Implements tasks from specifications
- Implements design specs from ui-ux-designer
- Handles implementation work
- Does not create design specs

### Task Requirements
- Design dashboard layout
- Create design specifications
- Plan responsive design
- Define component structure

### Capability Match Analysis
**Overall Match**: Poor

**Strengths**:
- Can implement designs once created
- Works with design specifications

**Gaps**:
- Agent does not create design specs
- Agent implements designs, doesn't design them
- Task requires design work, not implementation

**Recommendation**: Use ui-ux-designer instead

**Rationale**: Implementation-engineer implements designs but doesn't create them. This task requires design work, which should be handled by ui-ux-designer. Implementation-engineer would handle the implementation after design is complete.
```

## Multi-Agent Assessment

When assessing multiple agents for a task:

1. Assess each agent individually
2. Compare assessments
3. Rank agents by match quality
4. Recommend best agent or combination

```markdown
## Multi-Agent Capability Assessment

### Task: [task description]

### Agent 1: [agent-name]
**Match**: [Excellent/Good/Fair/Poor]
**Recommendation**: [Use / Don't use]

### Agent 2: [agent-name]
**Match**: [Excellent/Good/Fair/Poor]
**Recommendation**: [Use / Don't use]

### Best Match: [agent-name]
**Rationale**: [Why this agent is best]
```

## Best Practices

- **Read Agent Files Thoroughly**: Understand full agent capabilities
- **Be Specific**: Identify exact capability matches and gaps
- **Consider Workflow**: Agent workflow matters as much as capabilities
- **Think About Quality**: Match quality affects task success
- **Document Gaps**: Clear gap identification helps decision making
- **Recommend Clearly**: Make clear recommendations with rationale
