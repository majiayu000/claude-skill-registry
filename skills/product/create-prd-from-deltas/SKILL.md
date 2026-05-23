---
name: create-prd-from-deltas
description: "Generate a prd.json file from deltas ready to implement. Picks deltas with ✓ Plan status, dispatches parallel agents to split each delta into stories, combines results with cross-delta dependencies. Triggers on: create prd from deltas, prd from deltas, plan deltas, deltas prd."
---

# Create PRD from Deltas (Parallel Agent Orchestration)

Generate `prd.json` files from deltas that are ready to implement (status: ✓ Plan).
This skill orchestrates parallel agent execution for efficient delta processing.

> **Note:** This skill generates JSON files compatible with ralph-tui's JSON tracker plugin.

---

## The Job

1. Load `prd-task-creation` skill for schema reference
2. Read `docs/planning/DELTAS.md` to find all deltas with status "✓ Plan"
3. Ask user which deltas to include (if multiple available)
4. Read `docs/planning/DEPENDENCIES.md` for cross-delta dependencies
5. **Dispatch `delta-task-splitter` agents in parallel** (one per delta)
6. Collect agent outputs from their responses (NOT from files they write)
7. Combine into unified prd.json with re-sequenced IDs and cross-delta dependencies
8. Output the assembled `./prd.json`

**Important:** Do NOT start implementing. Just create the prd.json file.

---

## Step 1: Load Schema Reference

Load the `prd-task-creation` skill using the Skill tool.

This provides the JSON schema reference for:
- Validating agent outputs
- Assembling the final prd.json structure
- Ensuring anti-patterns are avoided during combination

---

## Step 2: Delta Discovery

Read the delta inventory and identify ready-to-implement deltas.

### Filter Criteria

Look for deltas with `**Status**: ✓ Plan` in `docs/planning/DELTAS.md`.

### Dependency Checking

Read `docs/planning/DEPENDENCIES.md` to understand any dependencies between deltas.

- If a delta depends on another that is NOT "✓ Plan", note this as a prerequisite
- Order deltas by dependency (prerequisites first)
- If no dependencies exist, order by delta ID

### User Selection

If multiple deltas are ready, ask the user which to include:

```
Found N deltas ready to implement. Which would you like to include in the PRD?

   A. All ready deltas
   B. Only Easy deltas
   C. Only [category] deltas
   D. Specify delta IDs (e.g., "DLT-009, DLT-011")
```

---

## Step 3: Dispatch Agents in Parallel

For each selected delta, dispatch a `delta-task-splitter` agent.

### Preparing Agent Inputs

For each delta, prepare minimal input:

- **delta_id**: The delta identifier (e.g., "DLT-013")
- **story_id_start**: Estimated starting story number (will be re-sequenced after)

**Note:** Agents read their own spec, design, plan, and referenced documents using predictable file paths. This keeps orchestrator context minimal.

### Parallel Dispatch

**CRITICAL:** Use the Task tool with multiple calls in a SINGLE message for parallel execution.

Example with 3 deltas:

```
Use Task tool 3 times in the SAME message:

Task 1:
  subagent_type: "delta-task-splitter"
  prompt: """
    delta_id: DLT-013
    story_id_start: 1
  """

Task 2:
  subagent_type: "delta-task-splitter"
  prompt: """
    delta_id: DLT-014
    story_id_start: 4
  """

Task 3:
  subagent_type: "delta-task-splitter"
  prompt: """
    delta_id: DLT-015
    story_id_start: 7
  """
```

The agents will run in parallel. Each agent reads its own documentation using predictable file paths.

---

## Step 4: Collect and Combine Results

### Collecting Agent Outputs

Each agent returns a JSON object in its response output:

```json
{
  "delta_id": "DLT-XXX",
  "stories": [...],
  "story_count": N,
  "next_story_id": M
}
```

**Important:** Collect these outputs from the agent responses (Task tool results), NOT from files that agents may have written. The delta-task-splitter agents should return JSON data in their output, not write files.

Wait for all agents to complete and collect their outputs.

### Re-sequencing Story IDs

Since agents run in parallel with estimated starting IDs, re-sequence after collection:

1. Order delta results by delta ID (or user-specified order)
2. Build an ID mapping: old ID -> new sequential ID
3. Assign sequential IDs: US-001, US-002, ... across all deltas
4. Update all `dependsOn` references using the ID mapping

Example:
```
Agent 1 (DLT-013) returned: US-001, US-002, US-003
Agent 2 (DLT-014) returned: US-004, US-005, US-006, US-007
Agent 3 (DLT-015) returned: US-008, US-009

After re-sequencing (if needed):
DLT-013: US-001, US-002, US-003
DLT-014: US-004, US-005, US-006, US-007
DLT-015: US-008, US-009
```

### Resolving Cross-Delta Dependencies

From `docs/planning/DEPENDENCIES.md`, identify delta-level dependencies.

For each delta that depends on another:

1. Find the **review story** of the prerequisite delta (last story in that delta's sequence)
2. Add that story ID to the **first story** of the dependent delta's `dependsOn` array

Example: If DLT-015 depends on DLT-014:
- DLT-014's review story is US-007
- DLT-015's first implementation story (US-008) gets `"dependsOn": ["US-007"]`

### Adjusting Priorities

After cross-delta dependencies are set:

1. Stories with no dependencies get priority 1
2. For stories with dependencies: priority = max(dependency priorities) + 1
3. This ensures topological ordering by priority

---

## Step 5: Assemble Final JSON

Combine all stories into the final prd.json structure:

```json
{
  "name": "[Derived from delta names or feature]",
  "branchName": "ralph/[kebab-case-feature-name]",
  "description": "[Summary of included deltas and their purpose]",
  "userStories": [
    // All stories from all agents, re-sequenced with cross-delta deps
  ]
}
```

### Naming Conventions

- **name**: Describe what's being implemented (e.g., "Implement Phase 2 Deltas")
- **branchName**: Kebab-case, prefixed with `ralph/` (e.g., "ralph/phase-2-deltas")
- **description**: Brief summary of included deltas

---

## Step 6: Output and Validation

### Output Location

Assemble and write the final prd.json to `./prd.json` (or user-specified path).

**Note:** This is the ONLY file that should be written. The delta-task-splitter agents return data in their outputs, they do NOT write files.

### Validation Checklist

Before saving, verify:

- [ ] JSON has flat structure (name, branchName, description, userStories at root)
- [ ] NO wrapper object (prd/tasks/metadata)
- [ ] Using "userStories" not "tasks"
- [ ] Using "passes" not "status"
- [ ] All story IDs are sequential (US-001, US-002, ...)
- [ ] All `dependsOn` references point to valid story IDs
- [ ] No circular dependencies
- [ ] Each delta has a review story at the end
- [ ] Quality gates appended to every story's acceptanceCriteria
- [ ] Cross-delta dependencies correctly resolved
- [ ] Priorities reflect dependency ordering

---

## Running with ralph-tui

After creating prd.json:

```bash
ralph-tui run --prd ./prd.json
```

Ralph-tui will:
1. Load stories from prd.json
2. Select the highest-priority story with `passes: false` and no blocking dependencies
3. Generate a prompt with story details + acceptance criteria
4. Run the agent to implement the story
5. Mark `passes: true` on completion
6. Repeat until all stories pass

---

## Error Handling

### Agent Failure

If a `delta-task-splitter` agent fails:

1. Note which delta failed
2. Report the error to the user
3. Offer to retry that specific delta or continue without it

### Invalid Agent Output

If an agent returns invalid JSON:

1. Attempt to parse and extract stories anyway
2. If unparseable, report error and offer to retry
3. Log the raw output for debugging

### Dependency Cycle Detection

Before output, verify no circular dependencies exist:

1. Build a dependency graph from `dependsOn` arrays
2. Detect cycles using topological sort
3. If cycle detected, report affected stories and ask user how to resolve
