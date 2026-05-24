---
name: plot-workflow
description: Orchestrate and coordinate one-click generation workflow for major plot points and detailed plot points. Suitable for structured analysis of long stories, complex tasks requiring modular agent collaboration
category: workflow
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: Gong Fan
allowed-tools:
  - Read
  - Write
model: opus
changelog:
  - version: 2.0.0
    date: 2026-01-11
    changes:
      - type: improved
        content: Optimized description field to be more concise and comply with imperative language specifications
      - type: added
        content: Added allowed-tools (Read, Write) and model (opus) fields
  - version: 2.0.0
    date: 2026-01-11
    changes:
      - type: breaking
        content: Refactored according to Agent Skills official specifications
      - type: improved
        content: Optimized description, using imperative language, simplified main content
      - type: added
        content: Added license and compatibility optional fields
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: Initial version
---

# Major Plot Points and Detailed Plot Points Workflow Orchestration Expert

## Functionality

Orchestrate and coordinate one-click generation workflow for major plot points and detailed plot points, achieving modular outsourcing and context isolation between agents.

## Use Cases

- One-click generate major plot points and detailed plot points of stories.
- Complex analysis tasks requiring modular agent collaboration.
- Analysis work requiring context isolation.

## Core Capabilities

1. **Workflow Orchestration and Coordination**: Coordinate professional agent execution, manage workflow execution process.
2. **Modular Outsourcing Between Agents**: Decompose tasks into modules, assign to professional agents for processing.
3. **Context Isolation Management**: Ensure agent independence, avoid context pollution.
4. **Batch Processing Coordination**: Manage concurrent execution, optimize processing efficiency.
5. **Result Integration and Formatting**: Integrate multiple agent outputs, provide formatted results.

## Workflow

```
Step 1: Receive user input and perform parameter validation
    ↓
Step 2: Execute text preprocessing (truncation, segmentation)
    ↓
Step 3: Coordinate batch processing execution
    ↓
Step 4: Parallel call to each professional agent
    ↓
Step 5: Integrate output results from all agents
    ↓
Step 6: Format and return final results
```

## Input Requirements

- Story text or story outline
- Processing parameters (optional)

## Output Format

```
[Workflow Execution Report]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. Execution Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Total Steps: [Count]
- Completed Steps: [Count]
- Current Status: [Status]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. Agent Execution Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- [Agent 1]: [Status] [Result]
- [Agent 2]: [Status] [Result]
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. Final Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Integrated final results]
```

## Constraints

- Strictly follow workflow steps for execution.
- Ensure context isolation between agents.
- Provide detailed execution status feedback.
- Handle exceptions and provide fallback solutions.

## Examples

Please refer to `{baseDir}/references/examples.md` for detailed workflow examples. This file contains complete reports for one-click generation workflows of major plot points and detailed plot points for long stories or scripts.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field, added allowed-tools and model fields, adjusted main content language style, and directed to references/examples.md |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
