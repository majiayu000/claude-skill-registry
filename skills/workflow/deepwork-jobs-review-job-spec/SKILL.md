---
name: deepwork_jobs.review_job_spec
description: "Reviews job.yml against quality criteria using a sub-agent for unbiased validation. Use after defining a job specification."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Sub-Agent Used**: Was a sub-agent spawned to provide unbiased review?
            2. **All doc spec Criteria Evaluated**: Did the sub-agent assess all 9 quality criteria?
            3. **Findings Addressed**: Were all failed criteria addressed by the main agent?
            4. **Validation Loop Complete**: Did the review-fix cycle continue until all criteria passed?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response OR
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met AND the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Sub-Agent Used**: Was a sub-agent spawned to provide unbiased review?
            2. **All doc spec Criteria Evaluated**: Did the sub-agent assess all 9 quality criteria?
            3. **Findings Addressed**: Were all failed criteria addressed by the main agent?
            4. **Validation Loop Complete**: Did the review-fix cycle continue until all criteria passed?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response OR
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met AND the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
---

# deepwork_jobs.review_job_spec

**Step 2/4** in **deepwork_jobs** workflow

> Creates and manages multi-step AI workflows. Use when defining, implementing, or improving DeepWork jobs.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/deepwork_jobs.define`

## Instructions

**Goal**: Reviews job.yml against quality criteria using a sub-agent for unbiased validation. Use after defining a job specification.

# Review Job Specification

## Objective

Review the `job.yml` created in the define step against the doc spec quality criteria using a sub-agent for unbiased evaluation, then iterate on fixes until all criteria pass.

## Why This Step Exists

The define step focuses on understanding user requirements and creating a job specification. This review step ensures the specification meets quality standards before implementation. Using a sub-agent provides an unbiased "fresh eyes" review that catches issues the main agent might miss after being deeply involved in the definition process.

## Task

Use a sub-agent to review the job.yml against all 9 doc spec quality criteria, then fix any failed criteria. Repeat until all criteria pass.

### Step 1: Read the Job Specification

Read the `job.yml` file created in the define step:

```
.deepwork/jobs/[job_name]/job.yml
```

Also read the doc spec for reference:

```
.deepwork/doc_specs/job_spec.md
```

### Step 2: Spawn Review Sub-Agent

Use the Task tool to spawn a sub-agent that will provide an unbiased review:

```
Task tool parameters:
- subagent_type: "general-purpose"
- model: "haiku"
- description: "Review job.yml against doc spec"
- prompt: [see below]
```

**Sub-agent prompt template:**

```
Review this job.yml against the following 9 quality criteria from the doc spec.

For each criterion, respond with:
- PASS or FAIL
- If FAIL: specific issue and suggested fix

## job.yml Content

[paste the full job.yml content here]

## Quality Criteria

1. **Valid Identifier**: Job name must be lowercase with underscores, no spaces or special characters (e.g., `competitive_research`, `monthly_report`)

2. **Semantic Version**: Version must follow semantic versioning format X.Y.Z (e.g., `1.0.0`, `2.1.3`)

3. **Concise Summary**: Summary must be under 200 characters and clearly describe what the job accomplishes

4. **Rich Description**: Description must be multi-line and explain: the problem solved, the process, expected outcomes, and target users

5. **Changelog Present**: Must include a changelog array with at least the initial version entry

6. **Complete Steps**: Each step must have: id (lowercase_underscores), name, description, instructions_file, outputs (at least one), and dependencies array

7. **Valid Dependencies**: Dependencies must reference existing step IDs with no circular references

8. **Input Consistency**: File inputs with `from_step` must reference a step that is in the dependencies array

9. **Output Paths**: Outputs must be valid filenames or paths (e.g., `report.md` or `reports/analysis.md`)

## Response Format

Respond with a structured evaluation:

### Overall: [X/9 PASS]

### Criterion Results

1. Valid Identifier: [PASS/FAIL]
   [If FAIL: Issue and fix]

2. Semantic Version: [PASS/FAIL]
   [If FAIL: Issue and fix]

[... continue for all 9 criteria ...]

### Summary of Required Fixes

[List any fixes needed, or "No fixes required - all criteria pass"]
```

### Step 3: Review Sub-Agent Findings

Parse the sub-agent's response:

1. **Count passing criteria** - How many of the 9 criteria passed?
2. **Identify failures** - List specific criteria that failed
3. **Note suggested fixes** - What changes does the sub-agent recommend?

### Step 4: Fix Failed Criteria

For each failed criterion, edit the job.yml to address the issue:

**Common fixes by criterion:**

| Criterion | Common Issue | Fix |
|-----------|-------------|-----|
| Valid Identifier | Spaces or uppercase | Convert to lowercase_underscores |
| Semantic Version | Missing or invalid format | Set to `"1.0.0"` or fix format |
| Concise Summary | Too long or vague | Shorten to <200 chars, be specific |
| Rich Description | Single line or missing context | Add multi-line explanation with problem/process/outcome/users |
| Changelog Present | Missing changelog | Add `changelog:` with initial version entry |
| Complete Steps | Missing required fields | Add id, name, description, instructions_file, outputs, dependencies |
| Valid Dependencies | Non-existent step or circular | Fix step ID reference or reorder dependencies |
| Input Consistency | from_step not in dependencies | Add the referenced step to dependencies array |
| Output Paths | Invalid characters or format | Use valid filename/path format |

### Step 5: Re-Run Review (If Needed)

If any criteria failed:

1. **Spawn a new sub-agent** with the updated job.yml content
2. **Review the new findings**
3. **Fix any remaining issues**
4. **Repeat until all 9 criteria pass**

### Step 6: Confirm Completion

When all 9 criteria pass:

1. **Announce success**: "All 9 doc spec quality criteria pass."
2. **List what was validated**:
   - Valid Identifier
   - Semantic Version
   - Concise Summary
   - Rich Description
   - Changelog Present
   - Complete Steps
   - Valid Dependencies
   - Input Consistency
   - Output Paths
3. **Include the promise**: `<promise>Quality Criteria Met</promise>`
4. **Guide to next step**: "Run `/deepwork_jobs.implement` to generate the step instruction files."

## Example Review Cycle

```
Claude: Let me review the job.yml against the doc spec quality criteria.

[Spawns sub-agent with haiku model]

Sub-agent response:
### Overall: 7/9 PASS

### Criterion Results
1. Valid Identifier: PASS
2. Semantic Version: PASS
3. Concise Summary: FAIL
   Issue: Summary is 245 characters, exceeds 200 char limit
   Fix: Shorten to "Competitive analysis workflow for product positioning"
4. Rich Description: PASS
5. Changelog Present: FAIL
   Issue: No changelog array present
   Fix: Add changelog with initial version entry
6. Complete Steps: PASS
7. Valid Dependencies: PASS
8. Input Consistency: PASS
9. Output Paths: PASS

### Summary of Required Fixes
1. Shorten summary to under 200 characters
2. Add changelog array with initial version

Claude: I found 2 issues. Let me fix them.

[Edits job.yml to shorten summary and add changelog]

Claude: Let me verify the fixes with another review.

[Spawns new sub-agent]

Sub-agent response:
### Overall: 9/9 PASS

### Summary of Required Fixes
No fixes required - all criteria pass

Claude: All 9 doc spec quality criteria pass.

<promise>Quality Criteria Met</promise>

**Next step:** Run `/deepwork_jobs.implement` to generate the step instruction files.
```

## Quality Criteria

- **Sub-Agent Used**: A sub-agent was spawned to provide unbiased review (not just self-review)
- **All doc spec Criteria Evaluated**: The sub-agent assessed all 9 quality criteria from the doc spec
- **Findings Addressed**: All failed criteria were fixed by the main agent
- **Validation Loop Complete**: The review-fix cycle continued until all criteria passed
- **Promise Included**: The response includes `<promise>Quality Criteria Met</promise>` when complete

## Output

The validated `job.yml` file at `.deepwork/jobs/[job_name]/job.yml` that passes all 9 doc spec quality criteria.


### Job Context

Core commands for managing DeepWork jobs. These commands help you define new multi-step
workflows and learn from running them.

The `define` command guides you through an interactive process to create a new job by
asking structured questions about your workflow, understanding each step's inputs and outputs,
and generating all necessary files.

The `learn` command reflects on conversations where DeepWork jobs were run, identifies
confusion or inefficiencies, and improves job instructions. It also captures bespoke
learnings specific to the current run into AGENTS.md files in the working folder.


## Required Inputs


**Files from Previous Steps** - Read these first:
- `job.yml` (from `define`)

## Work Branch

Use branch format: `deepwork/deepwork_jobs-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/deepwork_jobs-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `job.yml`
  **Doc Spec**: DeepWork Job Specification
  > YAML specification file that defines a multi-step workflow job for AI agents
  **Definition**: `.deepwork/doc_specs/job_spec.md`
  **Target Audience**: AI agents executing jobs and developers defining workflows
  **Quality Criteria**:
  1. **Valid Identifier**: Job name must be lowercase with underscores, no spaces or special characters (e.g., `competitive_research`, `monthly_report`)
  2. **Semantic Version**: Version must follow semantic versioning format X.Y.Z (e.g., `1.0.0`, `2.1.3`)
  3. **Concise Summary**: Summary must be under 200 characters and clearly describe what the job accomplishes
  4. **Rich Description**: Description must be multi-line and explain: the problem solved, the process, expected outcomes, and target users
  5. **Changelog Present**: Must include a changelog array with at least the initial version entry. Changelog should only include one entry per branch at most
  6. **Complete Steps**: Each step must have: id (lowercase_underscores), name, description, instructions_file, outputs (at least one), and dependencies array
  7. **Valid Dependencies**: Dependencies must reference existing step IDs with no circular references
  8. **Input Consistency**: File inputs with `from_step` must reference a step that is in the dependencies array
  9. **Output Paths**: Outputs must be valid filenames or paths within the main repo (not in dot-directories). Use specific, descriptive paths that lend themselves to glob patterns, e.g., `competitive_research/competitors_list.md` or `competitive_research/[competitor_name]/research.md`. Avoid generic names like `output.md`.
  10. **Concise Instructions**: The content of the file, particularly the description, must not have excessively redundant information. It should be concise and to the point given that extra tokens will confuse the AI.

  <details>
  <summary>Example Document Structure</summary>

  ```markdown
  # DeepWork Job Specification: [job_name]

  A `job.yml` file defines a complete multi-step workflow that AI agents can execute. Each job breaks down a complex task into reviewable steps with clear inputs and outputs.

  ## Required Fields

  ### Top-Level Metadata

  ```yaml
  name: job_name                    # lowercase, underscores only
  version: "1.0.0"                  # semantic versioning
  summary: "Brief description"      # max 200 characters
  description: |                    # detailed multi-line explanation
    [Explain what this workflow does, why it exists,
    what outputs it produces, and who should use it]
  ```

  ### Changelog

  ```yaml
  changelog:
    - version: "1.0.0"
      changes: "Initial job creation"
    - version: "1.1.0"
      changes: "Added quality validation hooks"
  ```

  ### Steps Array

  ```yaml
  steps:
    - id: step_id                   # unique, lowercase_underscores
      name: "Human Readable Name"
      description: "What this step accomplishes"
      instructions_file: steps/step_id.md
      inputs:
        # User-provided inputs:
        - name: param_name
          description: "What the user provides"
        # File inputs from previous steps:
        - file: output.md
          from_step: previous_step_id
      outputs:
        - competitive_research/competitors_list.md           # descriptive path
        - competitive_research/[competitor_name]/research.md # parameterized path
        # With doc spec reference:
        - file: competitive_research/final_report.md
          doc_spec: .deepwork/doc_specs/report_type.md
      dependencies:
        - previous_step_id          # steps that must complete first
  ```

  ## Optional Fields

  ### Exposed Steps

  ```yaml
  steps:
    - id: learn
      exposed: true                 # Makes step available without running dependencies
  ```

  ### Quality Hooks

  ```yaml
  steps:
    - id: step_id
      hooks:
        after_agent:
          # Inline prompt for quality validation:
          - prompt: |
              Verify the output meets criteria:
              1. [Criterion 1]
              2. [Criterion 2]
              If ALL criteria are met, include `<promise>...</promise>`.
          # External prompt file:
          - prompt_file: hooks/quality_check.md
          # Script for programmatic validation:
          - script: hooks/run_tests.sh
  ```

  ### Stop Hooks (Legacy)

  ```yaml
  steps:
    - id: step_id
      stop_hooks:
        - prompt: "Validation prompt..."
        - prompt_file: hooks/check.md
        - script: hooks/validate.sh
  ```

  ## Validation Rules

  1. **No circular dependencies**: Step A cannot depend on Step B if Step B depends on Step A
  2. **File inputs require dependencies**: If a step uses `from_step: X`, then X must be in its dependencies
  3. **Unique step IDs**: No two steps can have the same id
  4. **Valid file paths**: Output paths must not contain invalid characters and should be in the main repo (not dot-directories)
  5. **Instructions files exist**: Each `instructions_file` path should have a corresponding file created

  ## Example: Complete Job Specification

  ```yaml
  name: competitive_research
  version: "1.0.0"
  summary: "Systematic competitive analysis workflow"
  description: |
    A comprehensive workflow for analyzing competitors in your market segment.
    Helps product teams understand the competitive landscape through systematic
    identification, research, comparison, and positioning recommendations.

    Produces:
    - Vetted competitor list
    - Research notes per competitor
    - Comparison matrix
    - Strategic positioning report

  changelog:
    - version: "1.0.0"
      changes: "Initial job creation"

  steps:
    - id: identify_competitors
      name: "Identify Competitors"
      description: "Identify 5-7 key competitors in the target market"
      instructions_file: steps/identify_competitors.md
      inputs:
        - name: market_segment
          description: "The market segment to analyze"
        - name: product_category
          description: "The product category"
      outputs:
        - competitive_research/competitors_list.md
      dependencies: []

    - id: research_competitors
      name: "Research Competitors"
      description: "Deep dive research on each identified competitor"
      instructions_file: steps/research_competitors.md
      inputs:
        - file: competitive_research/competitors_list.md
          from_step: identify_competitors
      outputs:
        - competitive_research/[competitor_name]/research.md
      dependencies:
        - identify_competitors

    - id: positioning_report
      name: "Positioning Report"
      description: "Strategic positioning recommendations"
      instructions_file: steps/positioning_report.md
      inputs:
        - file: competitive_research/[competitor_name]/research.md
          from_step: research_competitors
      outputs:
        - file: competitive_research/positioning_report.md
          doc_spec: .deepwork/doc_specs/positioning_report.md
      dependencies:
        - research_competitors
  ```
  ```

  </details>

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

Stop hooks will automatically validate your work. The loop continues until all criteria pass.

**Criteria (all must be satisfied)**:
1. **Sub-Agent Used**: Was a sub-agent spawned to provide unbiased review?
2. **All doc spec Criteria Evaluated**: Did the sub-agent assess all 9 quality criteria?
3. **Findings Addressed**: Were all failed criteria addressed by the main agent?
4. **Validation Loop Complete**: Did the review-fix cycle continue until all criteria passed?


**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 2/4 complete, outputs: job.yml"
3. **Continue workflow**: Use Skill tool to invoke `/deepwork_jobs.implement`

---

**Reference files**: `.deepwork/jobs/deepwork_jobs/job.yml`, `.deepwork/jobs/deepwork_jobs/steps/review_job_spec.md`