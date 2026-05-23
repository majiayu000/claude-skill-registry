---
name: orchestration-prompts
description: Write prompts for orchestrator workflows with phases and aggregation. Use when designing multi-phase workflows, writing agent command prompts, or implementing result aggregation patterns.
allowed-tools: Read, Grep, Glob
---

# Orchestration Prompts Skill

Write prompts for orchestrator workflows with proper phase design and result aggregation.

## Purpose

Guide the creation of prompts for multi-agent orchestration workflows, including phase transitions, agent commands, and result aggregation.

## When to Use

- Writing orchestrator system prompts
- Designing phase-specific agent commands
- Creating aggregation and reporting prompts
- Building workflow transition logic

## Prerequisites

- Understanding of orchestrator architecture (@single-interface-pattern.md)
- Familiarity with lifecycle patterns (@agent-lifecycle-crud.md)
- Knowledge of result patterns (@results-oriented-engineering.md)

## Prompt Types

### 1. Orchestrator System Prompt

The identity prompt that defines orchestrator behavior:

```markdown
# Orchestrator Agent

## Purpose
Manage and coordinate specialized agents to accomplish complex tasks.
You do NOT perform work directly - you orchestrate other agents.

## Capabilities
- Create specialized agents from templates
- Command agents with detailed prompts
- Monitor agent progress
- Aggregate and report results
- Delete agents when work is complete

## Workflow Pattern
1. Analyze task requirements
2. Create appropriate agents
3. Command agents with detailed instructions
4. Monitor progress
5. Aggregate results
6. Report to user
7. Delete agents

## Context Protection
- Keep your context focused on orchestration
- Delegate detailed work to specialized agents
- Do not read files directly
- Do not write code

## Available Templates
- scout-fast: Quick reconnaissance (haiku)
- builder: Code implementation (sonnet)
- reviewer: Code review (sonnet)
- planner: Task planning (sonnet)

## Available Tools
- create_agent(template, name)
- command_agent(agent_id, prompt)
- check_agent_status(agent_id)
- list_agents()
- delete_agent(agent_id)
- read_agent_logs(agent_id)
```

### 2. Scout Command Prompts

Commands to send to reconnaissance agents:

```markdown
## Scout Command: Codebase Analysis

Analyze the codebase for [SPECIFIC_AREA].

Focus on:
1. File structure and organization
2. Key patterns and conventions
3. Dependencies and relationships
4. Potential issues or concerns

Provide results in this format:

### Files Analyzed
[List of files examined]

### Key Findings
1. [Finding with file reference]
2. [Finding with file reference]

### Patterns Observed
- [Pattern 1]
- [Pattern 2]

### Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]

### Status
[completed/partial/blocked]
```

### 3. Builder Command Prompts

Commands to send to implementation agents:

```markdown
## Builder Command: Implementation

Implement [FEATURE] based on the scout report.

### Requirements
[From scout findings or user request]

### Approach
[Suggested implementation approach]

### Files to Modify
- [file1.ts]: [changes needed]
- [file2.ts]: [changes needed]

### Files to Create
- [new-file.ts]: [purpose]

### Constraints
- Follow existing patterns
- Maintain backwards compatibility
- Add appropriate tests

Provide results in this format:

### Consumed Assets
[Files read, reports used]

### Produced Assets
[Files created or modified]

### Changes Summary
[Brief description of changes]

### Tests
[Test results if applicable]

### Status
[completed/partial/blocked]
```

### 4. Reviewer Command Prompts

Commands to send to review agents:

```markdown
## Reviewer Command: Verification

Review the implementation from [BUILDER_AGENT].

### Context
[Scout findings and builder changes]

### Review Criteria
1. Correctness: Does it meet requirements?
2. Quality: Does it follow patterns?
3. Security: Are there vulnerabilities?
4. Performance: Are there concerns?
5. Tests: Is coverage adequate?

Provide results in this format:

### Consumed Assets
[Files reviewed, reports referenced]

### Findings by Severity

**Blocker:**
[Issues that must be fixed]

**High Risk:**
[Significant concerns]

**Medium Risk:**
[Should be addressed]

**Low Risk:**
[Nice to fix]

### Verdict
[Pass/Pass with recommendations/Fail]

### Recommendations
[Prioritized list of improvements]

### Status
[completed]
```

### 5. Aggregation Prompts

Prompts for combining results:

```markdown
## Aggregation: Final Report

Compile final report from all agent results.

### Input
- Scout report: [summary]
- Builder report: [summary]
- Reviewer report: [summary]

### Output Format

## Task Completion Report

**Task:** [Original task]
**Duration:** [Total time]
**Cost:** [Total cost]

### Phase Summary

| Phase | Agents | Duration | Status |
| --- | --- | --- | --- |
| Scout | [n] | [time] | [status] |
| Build | [n] | [time] | [status] |
| Review | [n] | [time] | [status] |

### Results

**Files Created:**
[List]

**Files Modified:**
[List]

### Review Summary
[From reviewer]

### Outstanding Items
[Any remaining work]

### Conclusion
[1-2 sentence summary]
```

## Workflow Phase Design

### Standard Phases

| Phase | Purpose | Agents | Output |
| --- | --- | --- | --- |
| Scout | Understand | 1-3 scouts | Findings report |
| Plan | Design | 1 planner | Implementation plan |
| Build | Implement | 1-2 builders | Code changes |
| Review | Verify | 1 reviewer | Review report |
| Report | Summarize | Orchestrator | Final report |

### Phase Transitions

```text
Scout Complete --> Aggregate Findings --> Plan Phase
Plan Complete --> Validate Plan --> Build Phase
Build Complete --> Aggregate Changes --> Review Phase
Review Complete --> Check Verdict --> Report or Iterate
```

### Conditional Flows

```markdown
## Conditional: Review Failure

If reviewer verdict is "Fail":
1. Parse blocking issues
2. Create builder agent
3. Command: Fix specific issues
4. Re-run review phase
5. Maximum 3 iterations

If still failing after 3 iterations:
1. Report partial completion
2. List unresolved issues
3. Request user intervention
```

## Prompt Engineering Tips

### For Orchestrator Prompts

- Be explicit about not doing work directly
- List available tools and templates
- Define clear workflow pattern
- Emphasize context protection

### For Agent Commands

- Include all needed context
- Specify exact output format
- List files to examine/modify
- Set clear scope boundaries

### For Aggregation

- Define input sources
- Specify output structure
- Include metrics to calculate
- Handle partial results

## Output Format

When writing orchestration prompts, provide:

```markdown
## Orchestration Prompt Design

### Orchestrator System Prompt
[Full system prompt]

### Agent Command Templates

**Scout Commands:**
[Template with placeholders]

**Builder Commands:**
[Template with placeholders]

**Reviewer Commands:**
[Template with placeholders]

### Phase Transitions
[Flow diagram or description]

### Aggregation Format
[Final report template]

### Error Handling
[Failure scenarios and responses]
```

## Design Checklist

- [ ] Orchestrator system prompt complete
- [ ] Scout command template created
- [ ] Builder command template created
- [ ] Reviewer command template created
- [ ] Aggregation format defined
- [ ] Phase transitions documented
- [ ] Error handling covered
- [ ] Output formats standardized

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| Vague commands | Poor agent output | Specific instructions |
| No output format | Unparseable results | Standard templates |
| Missing context | Agent re-discovers info | Include scout findings |
| No error handling | Workflow breaks | Conditional flows |
| Orchestrator doing work | Context pollution | Strict delegation |

## Cross-References

- @single-interface-pattern.md - Orchestrator architecture
- @results-oriented-engineering.md - Result formats
- @multi-agent-context-protection.md - Context boundaries
- @orchestrator-design skill - System design

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
