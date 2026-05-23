---
name: build-agentic-workflows-chaining-tool-calls
description: Design and build multi-step agentic workflows on AgentPMT that chain tool calls, prompts, loops, and human notifications into reusable automation skills. Use when the user wants to create automated pipelines, chain multiple tools together, build no-code agent workflows, or publish reusable workflow skills.
author: agentpmt
version: 1.0.0
---

# Build Agentic Workflows -- Chaining Tool Calls

Design and build production-ready multi-step automation workflows on the AgentPMT platform. Workflows are directed acyclic graphs (DAGs) that chain tool nodes, prompt nodes, branch/merge conditional paths, for_each loops, and human notification gates into reusable, publishable skills.

## When to Apply

Reference these instructions when:
- Building automated multi-step workflows that chain tool calls
- Creating agent pipelines (research, content, outreach, data processing, monitoring)
- Publishing reusable workflow skills to the AgentPMT marketplace
- Remixing or forking existing public workflows
- Designing DAG-based automation with branching, looping, and human approval gates

## Tool Reference: workflow_skills_manager

All workflow operations use the `workflow_skills_manager` handler. Call `get_instructions` first if you need the full schema reference.

### Actions

| Action | Purpose | Required Params |
|--------|---------|-----------------|
| `fetch_tools` | Discover available tools for building workflows | none (use `tool_search` to filter) |
| `create_new` | Create a new workflow | `name`, `description`, `nodes`, `edges` |
| `update_existing` | Modify a workflow you own | `skill_id` + fields to change |
| `fetch_existing` | List your workflows or fetch one by ID | optional `skill_id`, `query` |
| `search_public` | Browse public published workflows | optional `query` |
| `publish` | Freeze and version a workflow for use | `skill_id` |
| `remix` | Copy a public workflow for editing | `skill_id` |
| `delete` | Remove a workflow you own | `skill_id` |
| `get_instructions` | Get full schema reference | none |

## Workflow Design Process

### Step 1: Understand the Task

Before building, determine:
- What repetitive task is being automated?
- What is the expected input and output?
- What tools are needed? (Use `fetch_tools` with `tool_search` to find them)
- Where does a human need to be involved vs. where can automation handle it?

### Step 2: Discover Available Tools

Use `fetch_tools` to search the tool catalog by keyword:

```json
{
  "action": "fetch_tools",
  "tool_search": "email",
  "limit": 20
}
```

Each returned product includes:
- `_id`: Product ObjectId (use as `product_id` in tool nodes)
- `name`: Product name (use as `product_name` in tool nodes)
- `vendor_id`: Vendor ObjectId
- `is_private`: Whether the tool requires special access
- `description`: What the tool does
- `input_schema` / `parameters`: The tool's parameter schema

Search multiple times with different keywords to find all relevant tools. If a tool exists for a task, use it instead of asking a human.

### Step 3: Design the Workflow Graph

A workflow is a directed acyclic graph (DAG) of nodes connected by edges. There are six node types:

| Type | Purpose | Inputs | Outputs |
|------|---------|--------|---------|
| `tool` | Execute a marketplace product | 1 | 1 (`next`) |
| `prompt` | AI reasoning/data transformation | 1 | 1 (`next`) |
| `for_each` | Iterate over a collection | 1 | 2 (`loop`, `next`) |
| `branch` | Split into conditional paths | 1 | up to 8 (`path_1`..`path_8`) |
| `merge` | Rejoin parallel paths | N (`merge_in_1`..N) | 1 |
| `notify_human` | Request human intervention | 1 | 1 (`next`) |

#### Node Types

**Tool Node** -- Execute a vendor product/tool:
```json
{
  "id": "node-1",
  "type": "tool",
  "label": "Search News Articles",
  "tool": {
    "product_id": "507f1f77bcf86cd799439011",
    "product_name": "News Search",
    "parameters": "{\"query\": \"industry trends\", \"limit\": 10}",
    "instructions": "Search for the latest articles relevant to the user's industry."
  },
  "position": {"x": 100, "y": 100}
}
```

- `product_id` and `product_name`: Required. Get these from `fetch_tools`.
- `parameters`: Optional JSON string of default parameter values.
- `instructions`: Optional guidance for the AI agent executing this step.

**Prompt Node** -- AI reasoning/processing step:
```json
{
  "id": "node-2",
  "type": "prompt",
  "label": "Analyze and Summarize",
  "prompt": {
    "mode": "structured",
    "goal": "Summarize the news articles into a concise briefing",
    "inputs": "Raw news article data from the previous step",
    "outputs": "A structured briefing with key takeaways, trends, and action items",
    "constraints": "Keep the summary under 500 words. Focus on actionable insights.",
    "success_criteria": "The briefing contains at least 3 key takeaways with supporting evidence"
  },
  "position": {"x": 300, "y": 100}
}
```

Two modes:
- **freeform**: Single `text` field for simple instructions.
- **structured**: Fields for `goal`, `inputs`, `outputs`, `constraints`, `success_criteria`, `notes`. Use structured mode for complex reasoning steps.

**For Each Node** -- Iterate over a collection:
```json
{
  "id": "node-3",
  "type": "for_each",
  "label": "Process Each Article",
  "for_each": {
    "item_alias": "article",
    "instructions": "For each article, extract the title, summary, and sentiment."
  },
  "position": {"x": 200, "y": 200}
}
```

- Child nodes are nested inside by setting their `parentId` to the for_each node's `id`.
- Has two outgoing handles: `"loop"` (enters the loop body) and `"next"` (continues after the loop completes).

**Branch Node** -- Split the workflow into conditional paths (up to 8):
```json
{
  "id": "node-branch",
  "type": "branch",
  "label": "Evaluate Risk Level",
  "branch": {
    "description": "Route based on the risk assessment from the previous step",
    "option_count": 3,
    "options": {
      "path_1": {"name": "High Risk", "description": "Score above 80"},
      "path_2": {"name": "Medium Risk", "description": "Score 40-80"},
      "path_3": {"name": "Low Risk", "description": "Score below 40"}
    }
  },
  "position": {"x": 400, "y": 100}
}
```

- `option_count`: Number of outgoing paths (default 2, max 8).
- `options`: Metadata for each path, keyed by handle ID (`"path_1"`, `"path_2"`, etc., or `"true"`/`"false"` for binary branches).
- Each outgoing edge should have a `condition` string describing when that path is taken.
- Always pair with a merge node downstream to rejoin paths.

**Merge Node** -- Rejoin parallel paths back into a single flow:
```json
{
  "id": "node-merge",
  "type": "merge",
  "label": "Continue After Risk Evaluation",
  "merge": {},
  "position": {"x": 800, "y": 100}
}
```

- Has multiple input handles (`"merge_in_1"`, `"merge_in_2"`, etc.) matching the number of incoming branch paths.
- Has a single output handle to continue the flow.
- Use after every branch node to reconverge the paths.

**Notify Human Node** -- Request human intervention:
```json
{
  "id": "node-4",
  "type": "notify_human",
  "label": "Request Approval",
  "notify_human": {
    "request_type": "other",
    "request": "Please review the generated report before it is sent to stakeholders."
  },
  "position": {"x": 500, "y": 100}
}
```

Request types: `add_funds`, `enable_tool`, `enable_workflow`, `other`.
Use sparingly -- only when human judgment or approval is genuinely required.

#### Edge Structure

Edges connect nodes in execution order:
```json
{
  "id": "edge-1",
  "from": "node-1",
  "to": "node-2",
  "sourceHandle": "next",
  "targetHandle": "default"
}
```

- `condition`: Optional string describing when this path is taken. Used on branch node outgoing edges.
- `sourceHandle`: Which output handle the edge originates from. Common values: `"next"` (tool, prompt, notify_human, merge), `"loop"` or `"next"` (for_each), `"path_1"`/`"path_2"`/`"true"`/`"false"` (branch).
- `targetHandle`: Which input handle the edge connects to. Usually `"default"`, or `"merge_in_1"`/`"merge_in_2"` for merge nodes.

#### Graph Rules

1. No cycles. The graph must be a DAG. Use for_each nodes for iteration.
2. Tool, prompt, and notify_human nodes have one input and one output.
3. For_each nodes have one input and two outputs (`"loop"` for the body, `"next"` for after the loop).
4. Branch nodes have one input and up to 8 outputs (`"path_1"` through `"path_8"`, or `"true"`/`"false"`).
5. Merge nodes have multiple inputs (`"merge_in_1"`, `"merge_in_2"`, etc.) and one output.
6. Every branch node should have a corresponding merge node downstream.
7. All node IDs must be unique. Use descriptive IDs like `"fetch-data"`, `"analyze-results"`, `"send-report"`.
8. All edge references must point to existing nodes.

### Step 4: Build and Create

Call `create_new` with the complete workflow definition:

```json
{
  "action": "create_new",
  "name": "Daily Industry News Briefing",
  "description": "Searches for industry news, analyzes key trends, formats a briefing, and emails it to the team.",
  "time_saved_minutes": 30,
  "visibility": "private",
  "nodes": [],
  "edges": []
}
```

- `name`: Clear, descriptive name (what the workflow does).
- `description`: Explain the workflow's purpose, inputs, outputs, and value.
- `time_saved_minutes`: Honest estimate of manual time this replaces.
- `visibility`: Start with `"private"`. Set to `"public"` when ready to share.

### Step 5: Test and Iterate

After creation, use `fetch_existing` with the returned `skill_id` to verify the full graph. Use `update_existing` to fix issues.

### Step 6: Publish

When the workflow is ready:
```json
{
  "action": "publish",
  "skill_id": "<skill_id>",
  "version_bump": "minor"
}
```

- First publish sets version to `1.0.0`.
- Subsequent publishes: `major` (breaking changes), `minor` (new steps/features), `patch` (fixes).
- Publishing creates a frozen snapshot. The live workflow can still be edited, but the published version is immutable until the next publish.

## Workflow Design Principles

### Prefer Tools Over Humans

If a tool exists that can perform a task, use it. Reserve `notify_human` nodes for:
- Approval gates where human judgment is legally or ethically required
- Situations where no tool can accomplish the task
- Final review of high-stakes outputs

### Right-Size the Workflow (3-15 Steps)

- **3-5 steps**: Simple automations (fetch data, process, deliver)
- **6-10 steps**: Standard business workflows (research, analyze, create, review, distribute)
- **11-15 steps**: Complex pipelines (multi-source data, iterative processing, multi-channel delivery)

Every step must add value. Do not pad workflows with unnecessary steps.

### Use Prompt Nodes for Reasoning

Insert prompt nodes between tool nodes when the AI needs to:
- Transform or restructure data between tools
- Make decisions about what to do next
- Synthesize information from multiple sources
- Apply business logic or domain knowledge

### Structure for Reliability

- Place data-fetching tools early in the workflow
- Follow tool nodes with prompt nodes that validate/transform the output
- Group related operations together
- Place delivery/notification steps at the end

### Write Clear Node Labels and Instructions

- **Labels**: Short, action-oriented (e.g., "Fetch Sales Data", "Draft Email", "Send to Slack")
- **Tool instructions**: Explain WHY the tool is being called and HOW its output feeds into the next step
- **Prompt goals**: Be specific about expected inputs and outputs

### Estimate Time Saved Honestly

Calculate `time_saved_minutes` based on how long the equivalent manual process takes.

## High-Value Workflow Patterns

### Research and Report
1. Search multiple data sources (news, analytics, databases)
2. Prompt: synthesize and identify patterns
3. Format into structured report
4. Deliver via email/Slack/document

### Content Pipeline
1. Research topic (news search, data APIs)
2. Prompt: draft content with guidelines
3. Create supporting visuals (charts, images)
4. Publish to platform
5. Notify team of publication

### Customer Outreach
1. Pull customer/lead data (CRM tool)
2. Prompt: personalize messaging based on customer data
3. Send personalized communications (email, messaging)
4. Log activity back to CRM
5. Schedule follow-up (calendar, task manager)

### Data Processing Pipeline
1. Fetch raw data from source
2. For_each: process individual records
   - Transform/validate record (prompt node inside loop)
   - Store processed record (tool node inside loop)
3. Prompt: generate summary statistics
4. Create visualization (chart generator)
5. Distribute results

### Monitoring and Alerting
1. Fetch metrics/data (analytics, blockchain, financial APIs)
2. Prompt: analyze against thresholds and historical patterns
3. Generate alert/report if conditions met
4. Send notification (Discord, Slack, email)
5. Log event for tracking

### Project Coordination
1. Pull tasks/issues from project management tool
2. Prompt: prioritize and identify blockers
3. Draft status update
4. Post to team channel
5. Update project tracker with new assignments

## Browsing and Remixing Public Workflows

Before building from scratch, search for existing public workflows:

```json
{
  "action": "search_public",
  "query": "email report"
}
```

If a relevant workflow exists, remix it:

```json
{
  "action": "remix",
  "skill_id": "<source_skill_id>",
  "name": "My Custom Version"
}
```

This creates a private copy you can modify.

## Node Position Guidelines

- **Horizontal flow**: Increment X by 200 per step. Keep Y constant for linear flows.
- **Branching**: Offset Y by 150-200 for parallel branches.
- **For_each children**: Position inside the parent's visual boundary (similar X, offset Y by 100-150).
- **Start position**: Begin at `{"x": 100, "y": 100}`.

## Common Mistakes to Avoid

1. Creating workflows with only prompt nodes. Use at least one tool node.
2. Adding unnecessary notify_human steps. If a tool can do it, let the tool do it.
3. Forgetting to connect nodes with edges.
4. Using cycles instead of for_each. The graph must be acyclic.
5. Vague prompt nodes. Specify what processing means, what the input looks like, and what the output should be.
6. Not searching for tools first. The catalog has 170+ tools.
7. Overcomplicating simple tasks.
8. Setting unrealistic time_saved_minutes.

## Constraints

- Never create mock or placeholder workflows. Every workflow must use real tool product IDs from `fetch_tools`.
- Never set `visibility` to `"public"` on a workflow that hasn't been tested.
- Never publish a workflow with private tools and public visibility.
- Always include a description that explains what the workflow does, who it's for, and what value it provides.
