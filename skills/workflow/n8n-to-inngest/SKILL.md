---
name: n8n-to-inngest
description: Systematic methodology for translating n8n workflow automation into Inngest durable execution workflows. Use when converting n8n workflows to Inngest, migrating from n8n to Inngest, or understanding how n8n concepts map to Inngest patterns. Supports analyzing n8n workflow JSON exports, mapping nodes to Inngest steps, and generating production-ready TypeScript functions with proper error handling and observability.
---

# n8n to Inngest Workflow Translation

## Overview

This skill provides a systematic, repeatable methodology for translating n8n visual workflow automations into Inngest durable execution workflows. It includes conceptual mappings, implementation patterns, common challenges with solutions, and utilities for parsing and generating code.

**When to use this skill:**
- Converting existing n8n workflows to Inngest
- Migrating workflow automation from n8n to Inngest
- Understanding how n8n concepts map to Inngest patterns
- Generating Inngest functions from n8n workflow JSON exports
- Planning workflow migration projects

## Required Input

**The user must provide an n8n workflow JSON export file.** To export a workflow from n8n:
1. Open the workflow in n8n editor
2. Click the "..." menu (top right)
3. Select "Download" or "Export Workflow"
4. Save the JSON file

**First Action:** When this skill is invoked, immediately request the n8n workflow JSON file if not already provided. The translation process cannot begin without analyzing the source workflow structure.

## Translation Process Workflow

Follow this 5-phase workflow for systematic translation:

### Phase 1: Analysis & Decomposition

1. **Export & Parse**: Export n8n workflow as JSON using the workflow export feature
2. **Identify Trigger**: Determine workflow initiation mechanism (webhook, schedule, manual, event)
3. **Map Nodes**: Catalog all nodes and their dependencies using `scripts/parse_n8n_workflow.py`
4. **Extract Logic**: Document business logic, conditions, and loops
5. **Identify Data Flow**: Track data transformations between nodes

**Key Actions:**
- Use `scripts/parse_n8n_workflow.py` to analyze workflow structure and generate a dependency graph
- Document credentials used (will need migration to environment variables)
- Identify complex transformations that need special attention

### Phase 2: Architecture Design

1. **Event Modeling**: Define Inngest events that will trigger the workflow
2. **Function Design**: Determine if single function or multiple coordinated functions needed
3. **Step Breakdown**: Map n8n nodes to Inngest `step.run()` calls
4. **Error Handling**: Plan retry strategies and failure scenarios
5. **State Management**: Design data passing between steps

**Key Decisions:**
- Single function vs. multiple functions (use multiple for parallel operations or reusable sub-workflows)
- Step granularity (each external API call should be its own step for retry isolation)
- Error handling strategy (retries, onFailure handlers, compensating transactions)

### Phase 3: Implementation

1. **Event Schemas**: Define TypeScript types for events and data structures
2. **Function Skeleton**: Create Inngest function structure with proper configuration
3. **Step Implementation**: Convert each n8n node to Inngest step using patterns from `references/patterns.md`
4. **Data Transformation**: Implement logic for data mapping (convert n8n expressions to JavaScript/TypeScript)
5. **Integration**: Connect to external services/APIs with proper authentication

**Best Practices:**
- Use deterministic step IDs (see `scripts/generate_step_id.py`)
- Make steps idempotent (safely retryable)
- Include rich error context for debugging
- Add TypeScript types for all events and step outputs

### Phase 4: Testing & Validation

1. **Unit Tests**: Test individual steps in isolation
2. **Integration Tests**: Test full workflow execution
3. **Edge Cases**: Test error conditions, retries, timeouts
4. **Data Validation**: Ensure Inngest output matches n8n behavior

**Testing Strategy:**
- Use n8n execution logs as test fixtures (capture inputs/outputs)
- Test retry behavior for transient failures
- Validate idempotency by running steps multiple times
- Compare outputs between n8n and Inngest side-by-side

### Phase 5: Deployment & Monitoring

1. **Deploy Function**: Register with Inngest server
2. **Setup Monitoring**: Add observability (OpenTelemetry, logs, metrics)
3. **Gradual Rollout**: Test with real events in staging environment
4. **Performance Tuning**: Optimize step execution and function configuration

## Core Conceptual Mappings

Quick reference for mapping n8n concepts to Inngest equivalents:

| n8n Concept | Inngest Equivalent | Implementation Notes |
|-------------|-------------------|---------------------|
| **Workflow** | `inngest.createFunction()` | May require multiple functions for complex workflows |
| **Webhook Trigger** | Event sent from webhook handler | Webhook receives request → sends event → triggers function |
| **Schedule Trigger** | Cron expression | `cron: "0 9 * * *"` in function config |
| **Manual Trigger** | HTTP endpoint or event | Use `inngest.send()` to invoke |
| **Standard Node** | `step.run()` | Each node becomes a discrete, retryable step |
| **If/Switch Node** | JavaScript conditionals | Use `if/else` or `switch` statements |
| **Loop Node** | `for` loop with `step.run()` | Each iteration can be a retryable step with unique ID |
| **Wait Node** | `step.sleep()` | Built-in sleep: `step.sleep('id', '1h')` |
| **Execute Workflow** | `step.invoke()` | Call another Inngest function and wait for result |
| **HTTP Request** | `step.run()` with fetch | Automatic retries on failure |
| **Code Node** | JavaScript/TypeScript | Direct code execution in step |
| **Set/Merge Node** | Variable assignment | Simple JS object manipulation |
| **Error Workflow** | `onFailure` handler | Define failure handling function in config |

**Data Flow Pattern:**
- **n8n**: Nodes receive `items[]` array, process, output `items[]`
- **Inngest**: Steps receive `event.data` and previous step outputs, return values

For detailed code examples of each pattern, refer to `references/patterns.md`.

## Common Challenges

Common challenges and their solutions are documented in `references/challenges.md`. Key areas covered:

1. **Complex Data Transformations** - Converting n8n expressions to JavaScript/TypeScript
2. **Large Datasets** - Batch processing and fan-out patterns
3. **Credentials Management** - Migrating from n8n credential store to environment variables
4. **Webhook Responses** - Handling synchronous response requirements with async execution
5. **Complex Branching** - Managing Switch nodes with multiple outputs
6. **Human-in-the-Loop** - Using `step.waitForEvent()` for approval workflows

Refer to the challenges reference for detailed solutions with code examples.

## Implementation Checklist

Use this checklist to ensure complete translation:

- [ ] Export n8n workflow as JSON
- [ ] Parse workflow structure using `scripts/parse_n8n_workflow.py`
- [ ] Identify trigger type (webhook, schedule, manual, event)
- [ ] Map all nodes to Inngest steps
- [ ] Extract and migrate credentials to environment variables
- [ ] Convert data transformations from n8n expressions to JavaScript/TypeScript
- [ ] Implement error handling with retries and `onFailure`
- [ ] Handle conditionals (If/Switch nodes) with JavaScript control flow
- [ ] Implement loops with proper deterministic step IDs
- [ ] Add TypeScript type definitions for events and data
- [ ] Write tests using n8n execution data as fixtures
- [ ] Document complex logic from n8n Code nodes
- [ ] Setup monitoring and observability
- [ ] Deploy and test with real events
- [ ] Compare outputs between n8n and Inngest
- [ ] Validate performance and optimize if needed
- [ ] Decommission n8n workflow once fully validated

## Best Practices Summary

**Step Design:**
- Each external API call or database operation should be its own `step.run()` for retry isolation
- Use deterministic, consistent step IDs (avoid timestamps, random values)
- Design steps to be idempotent (safely retryable without side effects)
- Keep steps focused and small for easier debugging and retry management

**Code Quality:**
- Define TypeScript types for all events and step outputs
- Include rich error context for debugging
- Document complex business logic with comments
- Use proper naming conventions (kebab-case for step IDs)

**Error Handling:**
- Configure appropriate retry counts per function
- Use `onFailure` handlers for error workflows
- Implement compensating transactions where needed
- Test retry behavior explicitly

**Data Management:**
- Only pass necessary data between steps (state is stored automatically)
- Avoid large payloads in events (use references instead)
- Validate data at function boundaries

## Resources

### scripts/

**`parse_n8n_workflow.py`**
Parse n8n workflow JSON to extract structure, nodes, connections, and generate dependency graph.

**Usage:**
```bash
python scripts/parse_n8n_workflow.py workflow.json
```

**Output:** JSON structure with nodes, triggers, credentials, and dependency information.

**`generate_step_id.py`**
Generate valid, deterministic Inngest step IDs from n8n node names.

**Usage:**
```bash
python scripts/generate_step_id.py "HTTP Request 1"
# Output: http-request-1
```

### references/

**`patterns.md`**
Detailed code examples for common workflow patterns:
- Simple linear workflows
- Conditional logic (If/Switch nodes)
- Loops and iteration
- Error handling
- Wait/delay operations
- Calling other workflows
- Complete translation examples

Load this reference when implementing specific node types or patterns.

**`challenges.md`**
Common challenges encountered during translation with detailed solutions:
- Complex data transformations
- Large dataset handling
- Credential migration
- Webhook response patterns
- Complex branching logic
- Human-in-the-loop workflows

Load this reference when encountering specific implementation challenges.

### assets/

**`templates/`**
Template Inngest functions for common n8n workflow patterns:
- `linear-workflow.ts` - Simple sequential workflow
- `conditional-workflow.ts` - Workflow with branching logic
- `loop-workflow.ts` - Workflow with iteration
- `approval-workflow.ts` - Human-in-the-loop pattern
- `scheduled-workflow.ts` - Cron-triggered workflow
- `webhook-workflow.ts` - Webhook-triggered workflow

Use these templates as starting points and customize for specific workflows.

## Getting Started

To translate an n8n workflow to Inngest:

1. **Obtain the n8n workflow JSON file** - Request from user if not provided (required to proceed)
2. **Parse** it using `scripts/parse_n8n_workflow.py` to understand structure and dependencies
3. **Analyze** the parser output to identify triggers, node types, and workflow complexity
4. **Choose** the appropriate template from `assets/templates/` based on workflow type
5. **Map** each n8n node to Inngest steps using the conceptual mappings above
6. **Implement** steps following patterns from `references/patterns.md`
7. **Test** thoroughly using the validation checklist
8. **Deploy** with monitoring and observability

Refer to `references/patterns.md` for the complete end-to-end translation example showing the full process.
