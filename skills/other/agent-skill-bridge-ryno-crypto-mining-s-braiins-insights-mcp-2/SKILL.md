---
name: agent-skill-bridge
version: 1.0.0
author: claude-command-control
created: 2025-11-22
status: active
complexity: moderate
---

# Agent-Skill Integration Bridge

## Description
Facilitates seamless integration between Claude Skills and the existing Agent framework, enabling skills to invoke agents and vice versa with proper context handoffs.

## When to Use This Skill
- When creating a skill that needs to invoke an agent (Builder, Validator, etc.)
- When an agent needs to leverage a skill for specific workflow
- When orchestrating multi-agent workflows that include skills
- When troubleshooting agent-skill communication issues

## When NOT to Use This Skill
- For simple single-agent tasks (use agents directly)
- For simple single-skill tasks (use skills directly)
- When no integration is needed

## Prerequisites
- Understanding of agent framework (see agent templates)
- Understanding of skill architecture (see skill templates)
- Access to `MULTI_AGENT_PLAN.md` for orchestration
- Familiarity with both agent configs and SKILL.md formats

## Workflow

### Phase 1: Integration Planning

#### Step 1.1: Identify Integration Pattern

**Pattern A: Skill Invokes Agent**
```

User Request
↓
Skill (Primary workflow orchestrator)
↓
Agent (Specialized execution)
↓
Back to Skill (Result synthesis)

```

**Pattern B: Agent Invokes Skill**
```

User Request
↓
Agent (Primary workflow orchestrator)
↓
Skill (Specialized automation)
↓
Back to Agent (Continue workflow)

```

**Pattern C: Orchestrator Pattern**
```

User Request
↓
Orchestrator Skill
├→ Agent A (parallel)
├→ Agent B (parallel)
└→ Skill C (depends on A+B)
↓
Results Synthesis

```

#### Step 1.2: Define Handoff Protocol

Create handoff specification:

```


## Handoff Specification

**From**: [Skill/Agent Name]
**To**: [Agent/Skill Name]
**Trigger**: [When handoff occurs]

**Data Transfer:**

```json
{
  "handoff_type": "skill_to_agent | agent_to_skill",
  "source": "source-name",
  "destination": "destination-name",
  "context": {
    "execution_id": "unique-id",
    "phase": "current-phase",
    "data": {
      // Relevant data structure
    }
  },
  "requirements": {
    "agent_role": "builder | validator | scribe | devops | researcher",
    "expected_output": "description of what agent should produce",
    "quality_criteria": ["criterion1", "criterion2"]
  }
}
```

**Return Path:**

```json
{
  "source": "agent-name",
  "destination": "skill-name",
  "execution_id": "same-unique-id",
  "status": "success | partial | failure",
  "output": {
    // Agent's produced artifact
  },
  "metadata": {
    "duration": "execution-time",
    "quality_score": "0-100",
    "notes": ["note1", "note2"]
  }
}
```

```

### Phase 2: Implementation

#### Step 2.1: Skill-to-Agent Invocation

**In SKILL.md, add agent invocation step:**

```


### Step X: Invoke [Agent Name] Agent

**Purpose**: [Why agent is needed]

**Agent Configuration:**

- **Role**: [builder | validator | scribe | devops | researcher]
- **Context Required**:
    - [File 1]
    - [File 2]
    - [Variable: value]

**Invocation:**

Update `MULTI_AGENT_PLAN.md`:

```markdown
## Phase [N]: [Agent Name] Execution

**Agent**: [Agent Name] (see `.claude/agents/[agent].md`)
**Trigger**: [Skill Name] skill - Step X
**Input**: [What skill provides]

### Tasks for [Agent Name]:
1. [Task 1 with acceptance criteria]
2. [Task 2 with acceptance criteria]

### Expected Output:
[Detailed description]

### Return to Skill:
After completion, return results to [Skill Name] skill for [next step].
```

**Handoff Message:**

```markdown
---
TO: [Agent Name] Agent
FROM: [Skill Name] Skill
EXECUTION_ID: [skill-exec-id]
PHASE: [current-phase]

**Context Provided:**
- [Context item 1]: [Location/value]
- [Context item 2]: [Location/value]

**Tasks:**
1. [Task 1]
2. [Task 2]

**Acceptance Criteria:**
- [Criterion 1]
- [Criterion 2]

**Return Requirements:**
- Output format: [Specification]
- Handoff location: [Where to place results]
- Notification: Update MULTI_AGENT_PLAN.md when complete

**Questions/Blockers:**
Contact: [Skill maintainer]
---
```

**Wait for Agent Completion:**

- Monitor `MULTI_AGENT_PLAN.md` for status updates
- Agent marks tasks complete
- Results available at specified location

**Receive Results:**

```markdown
### Step X+1: Process [Agent Name] Results

Load agent output from [location]

Validate:
- [ ] Output format matches specification
- [ ] Acceptance criteria met
- [ ] No errors reported

IF validation passes:
    Proceed to next step
ELSE:
    Review issues and either:
    - Request agent revision
    - Adapt workflow
    - Escalate to human
```

```

#### Step 2.2: Agent-to-Skill Invocation

**In agent config (e.g., `builder.md`), add skill invocation:**

```


## Workflow Pattern: Invoke [Skill Name] Skill

When [condition for skill invocation]:

1. **Prepare Skill Input:**

```markdown
Create skill-input.json:
{
  "parameter1": "value1",
  "parameter2": "value2",
  "context": {
    // Relevant context from agent
  }
}
```

2. **Invoke Skill:**
Reference skill documentation: `skills/[skill-name]/SKILL.md`

Execute skill with: "Use [skill-name] skill with input from skill-input.json"
3. **Receive Skill Output:**
Skill produces: [expected output]

Validate:
    - [ ] Output format correct
    - [ ] Quality standards met
    - [ ] Integration points clear
4. **Continue Agent Workflow:**
Use skill output to [next agent step]
```

### Phase 3: Orchestration

#### Step 3.1: Multi-Agent-Skill Orchestration

Create orchestrator configuration in `MULTI_AGENT_PLAN.md`:

```


# Multi-Agent-Skill Orchestration Plan

## Workflow: [Workflow Name]

**Orchestrator**: [Lead Skill or Lead Agent]

### Execution Graph:

```
Phase 1: [Orchestrator Skill] - Requirements Gathering
    ↓
Phase 2: [Architect Agent] - System Design (parallel with Phase 3)
    ↓                              ↓
Phase 3: [Research Skill]     Phase 4: [Builder Agent]
    ↓                              ↓
Phase 5: [Orchestrator Skill] - Synthesis
    ↓
Phase 6: [Validator Agent] - Quality Assurance
    ↓
Phase 7: [PR-Generator Skill] - Finalization
```


### Phase Details:

#### Phase 1: [Orchestrator Skill] - Requirements

**Duration**: [X min]
**Output**: Requirements document
**Next**: Triggers Phase 2 and 3 in parallel

#### Phase 2: [Architect Agent] - Design

**Input**: Requirements document from Phase 1
**Tasks**:

- Create ARCHITECTURE.md
- Define component structure
**Output**: Architecture specification
**Next**: Triggers Phase 4


#### Phase 3: [Research Skill] - Technology Analysis

**Input**: Requirements document from Phase 1
**Tasks**:

- Research relevant technologies
- Generate comparison matrix
**Output**: Technology recommendations
**Next**: Merges with Phase 2 output for Phase 4


#### Phase 4: [Builder Agent] - Implementation

**Input**:

- Architecture spec from Phase 2
- Tech recommendations from Phase 3
**Tasks**:
- Implement feature
- Write tests
**Output**: Implemented code
**Next**: Triggers Phase 5

[Continue for all phases...]

### Handoff Protocol:

**Phase N → Phase N+1:**

```json
{
  "from_phase": "N",
  "to_phase": "N+1",
  "handoff_data": {
    "artifacts": ["artifact1.md", "artifact2.js"],
    "context": {},
    "status": "complete",
    "quality_score": 95
  }
}
```

```

## Examples

### Example 1: PR Description Skill → Validator Agent

**Scenario**: PR description skill generates description, needs code quality validation

**Integration:**

```


## PR Description Skill - Step 5: Request Validation

After generating PR description:

1. Create validation request:

```markdown
---
TO: Validator Agent
FROM: PR Description Skill

**Request**: Code quality validation for PR #123

**Files to Review:**
- src/auth/jwt.service.js
- tests/auth/jwt.test.js

**Focus Areas:**
- Test coverage ≥90%
- Security: Token validation
- Performance: No N+1 queries

**Return**: Validation report to `pr-123-validation.md`
---
```

2. Wait for validator completion
3. Receive validation results:

```markdown
## Validation Report: PR #123

**Status**: ✅ APPROVED

**Test Coverage**: 94%
**Security**: ✅ No issues
**Performance**: ✅ Optimized

**Recommendation**: Safe to merge
```

4. Append validation summary to PR description:

```markdown
## Quality Validation

✅ Automated validation passed
- Test coverage: 94%
- Security scan: Clean
- Performance: Optimized

Validated by: Validator Agent
Report: pr-123-validation.md
```

```

### Example 2: Builder Agent → Code Formatter Skill

**Scenario**: Builder implements code, needs consistent formatting applied

**Integration in builder.md:**

```


## After Code Implementation

### Step X: Apply Code Formatting

Instead of manual formatting commands, invoke skill:

1. Prepare context:

```json
{
  "files_changed": ["src/**/*.js", "tests/**/*.js"],
  "style_guide": ".eslintrc.json",
  "formatter": "prettier"
}
```

2. Invoke: "Use code-formatter skill with context from above"
3. Skill returns:

```json
{
  "status": "success",
  "files_formatted": 12,
  "issues_fixed": 45,
  "remaining_issues": 0
}
```

4. Validate formatting:

```bash
npm run lint
```

5. Commit formatted code:

```bash
git add .
git commit -m "style: apply code formatter skill"
```

```

### Example 3: Orchestrator Skill Coordinating 3 Agents

**Scenario**: Feature development requiring Architect → Builder → Validator sequence

```


## Feature Implementation Orchestrator Skill

### Phase 2: Architecture Planning

**Invoke**: Architect Agent

**Handoff:**

```markdown
---
TO: Architect Agent
FROM: Feature Orchestrator Skill
FEATURE: User Authentication

**Requirements:**
- JWT-based authentication
- Refresh token support
- Rate limiting
- Session management

**Deliverables:**
- ARCHITECTURE.md: Auth system design
- SECURITY.md: Security model
- TECH_STACK.md: Libraries selected

**Timeline**: 2 hours
**Budget**: High priority
---
```

**Wait for**: Architect marks complete in MULTI_AGENT_PLAN.md

### Phase 3: Implementation

**Invoke**: Builder Agent

**Handoff:**

```markdown
---
TO: Builder Agent
FROM: Feature Orchestrator Skill
SOURCE: ARCHITECTURE.md from Phase 2

**Tasks:**
Implement auth system per architecture spec

**Acceptance:**
- All tests passing
- Code coverage ≥90%
- Follows ARCHITECTURE.md design

**Timeline**: 6 hours
---
```

**Wait for**: Builder marks complete

### Phase 4: Validation

**Invoke**: Validator Agent

**Handoff:**

```markdown
---
TO: Validator Agent
FROM: Feature Orchestrator Skill
PR: #456

**Review Focus:**
- Security validation
- Test coverage verification
- Performance benchmarking

**Acceptance:**
- Zero critical issues
- Coverage ≥90%
- Performance within targets
---
```

**Receive**: Validation report

### Phase 5: Synthesis

Orchestrator skill compiles:

- Architecture design
- Implementation code
- Validation results
- PR description

**Final Output**: Complete feature package ready for merge

```

## Quality Standards

- Handoffs must include unique execution_id for traceability
- All context required by recipient must be explicitly provided
- Return paths must be clearly defined
- Timeout handling for agent/skill execution
- Graceful degradation if agent/skill unavailable

## Common Pitfalls

### Pitfall 1: Missing Context in Handoff
**Issue**: Agent/skill fails because required context not provided
**Solution**: Always validate context completeness before handoff

```


## Pre-Handoff Checklist

- [ ] All required files accessible
- [ ] All parameters defined
- [ ] Acceptance criteria clear
- [ ] Return path specified
- [ ] Execution ID assigned

```

### Pitfall 2: No Timeout Handling
**Issue**: Waiting indefinitely for agent/skill completion
**Solution**: Implement timeout with fallback

```


### Step X: Invoke [Agent] with Timeout

1. Invoke agent
2. Set timeout: 30 minutes
3. IF timeout:
Log warning
Either:
    - Use partial results
    - Skip this step
    - Request human intervention
```

### Pitfall 3: Circular Dependencies
**Issue**: Skill A calls Agent B which calls Skill A
**Solution**: Design clear dependency graph, avoid cycles

```

✅ GOOD:
Skill → Agent → Skill (different skill)

❌ BAD:
Skill A → Agent → Skill A (circular)

```

## Version History
- 1.0.0 (2025-11-22): Initial release

