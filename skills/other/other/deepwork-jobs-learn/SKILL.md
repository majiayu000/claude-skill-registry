---
name: deepwork_jobs.learn
description: "Analyzes conversation history to improve job instructions and capture learnings. Use after running a job to refine it."
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Conversation Analyzed**: Did the agent review the conversation for DeepWork job executions?
            2. **Confusion Identified**: Did the agent identify points of confusion, errors, or inefficiencies?
            3. **Instructions Improved**: Were job instructions updated to address identified issues?
            4. **Instructions Concise**: Are instructions free of redundancy and unnecessary verbosity?
            5. **Shared Content Extracted**: Is lengthy/duplicated content extracted into referenced files?
            6. **doc spec Reviewed (if applicable)**: For jobs with doc spec outputs, were doc spec-related learnings identified?
            7. **doc spec Updated (if applicable)**: Were doc spec files updated with improved quality criteria or structure?
            8. **Bespoke Learnings Captured**: Were run-specific learnings added to AGENTS.md?
            9. **File References Used**: Do AGENTS.md entries reference other files where appropriate?
            10. **Working Folder Correct**: Is AGENTS.md in the correct working folder for the job?
            11. **Generalizable Separated**: Are generalizable improvements in instructions, not AGENTS.md?
            12. **Sync Complete**: Has `deepwork sync` been run if instructions were modified?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Conversation Analyzed**: Did the agent review the conversation for DeepWork job executions?
            2. **Confusion Identified**: Did the agent identify points of confusion, errors, or inefficiencies?
            3. **Instructions Improved**: Were job instructions updated to address identified issues?
            4. **Instructions Concise**: Are instructions free of redundancy and unnecessary verbosity?
            5. **Shared Content Extracted**: Is lengthy/duplicated content extracted into referenced files?
            6. **doc spec Reviewed (if applicable)**: For jobs with doc spec outputs, were doc spec-related learnings identified?
            7. **doc spec Updated (if applicable)**: Were doc spec files updated with improved quality criteria or structure?
            8. **Bespoke Learnings Captured**: Were run-specific learnings added to AGENTS.md?
            9. **File References Used**: Do AGENTS.md entries reference other files where appropriate?
            10. **Working Folder Correct**: Is AGENTS.md in the correct working folder for the job?
            11. **Generalizable Separated**: Are generalizable improvements in instructions, not AGENTS.md?
            12. **Sync Complete**: Has `deepwork sync` been run if instructions were modified?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
---

# deepwork_jobs.learn

**Standalone skill** - can be run anytime

> Creates and manages multi-step AI workflows. Use when defining, implementing, or improving DeepWork jobs.


## Instructions

**Goal**: Analyzes conversation history to improve job instructions and capture learnings. Use after running a job to refine it.

# Learn from Job Execution

## Objective

Think deeply about this task. Reflect on the current conversation to identify learnings from DeepWork job executions, improve job instructions with generalizable insights, and capture bespoke (run-specific) learnings in AGENTS.md files in the deepest common folder that would contain all work on the topic in the future.

## Task

Analyze the conversation history to extract learnings and improvements, then apply them appropriately:
- **Generalizable learnings** → Update job instruction files
- **Bespoke learnings** (specific to this run) → Add to AGENTS.md in the deepest common folder for the topic

### Step 1: Analyze Conversation for Job Executions

1. **Scan the conversation** for DeepWork slash commands that were run
   - Look for patterns like `/job_name.step_id`
   - Identify which jobs and steps were executed
   - Note the order of execution

2. **Identify the target folder**
   - This should be the deepest common folder that would contain all work on the topic in the future
   - Should be clear from conversation history where work was done
   - If unclear, run `git diff` to see where changes were made on the branch

3. **If no job was specified**, ask the user:
   - "Which DeepWork job would you like me to learn from?"
   - List available jobs from `.deepwork/jobs/`

### Step 2: Identify Points of Confusion and Inefficiency

Review the conversation for:

1. **Confusion signals**
   - Questions the agent asked that shouldn't have been necessary
   - Misunderstandings about what a step required
   - Incorrect outputs that needed correction
   - Ambiguous instructions that led to wrong interpretations

2. **Inefficiency signals**
   - Extra steps or iterations that were needed
   - Information that had to be repeated
   - Context that was missing from instructions
   - Dependencies that weren't clear

3. **Error patterns**
   - Failed validations and why they failed
   - Quality criteria that were misunderstood
   - Edge cases that weren't handled

4. **Success patterns**
   - What worked particularly well
   - Efficient approaches worth preserving
   - Good examples that could be added to instructions

### Step 3: Classify Learnings

For each learning identified, determine if it is:

**Generalizable** (should improve instructions):
- Would help ANY future run of this job
- Addresses unclear or missing guidance
- Fixes incorrect assumptions in instructions
- Adds helpful examples or context
- Examples:
  - "Step instructions should mention that X format is required"
  - "Quality criteria should include checking for Y"
  - "Add example of correct output format"

**doc spec-Related** (should improve doc spec files):
- Improvements to document quality criteria
- Changes to document structure or format
- Updated audience or frequency information
- Examples:
  - "The report should include a summary table"
  - "Quality criterion 'Visualization' needs clearer requirements"
  - "Documents need a section for action items"

**Bespoke** (should go in AGENTS.md):
- Specific to THIS project/codebase/run
- Depends on local conventions or structure
- References specific files or paths
- Would not apply to other uses of this job
- Examples:
  - "In this codebase, API endpoints are in `src/api/`"
  - "This project uses camelCase for function names"
  - "The main config file is at `config/settings.yml`"

### Step 3.5: Identify doc spec-Related Learnings

Review the conversation for doc spec-related improvements:

1. **Quality Criteria Changes**
   - Were any quality criteria unclear or insufficient?
   - Did the agent repeatedly fail certain criteria?
   - Are there new criteria that should be added?

2. **Document Structure Changes**
   - Did the user request different sections?
   - Were parts of the document format confusing?
   - Should the example document be updated?

3. **Metadata Updates**
   - Has the target audience changed?
   - Should frequency or path patterns be updated?

**Signals for doc spec improvements:**
- User asked for changes to document format
- Repeated validation failures on specific criteria
- Feedback about missing sections or information
- Changes to how documents are organized/stored

### Step 4: Update Job Instructions (Generalizable Learnings)

For each generalizable learning:

1. **Locate the instruction file**
   - Path: `.deepwork/jobs/[job_name]/steps/[step_id].md`

2. **Make targeted improvements**
   - Add missing context or clarification
   - Include helpful examples
   - Clarify ambiguous instructions
   - Update quality criteria if needed

3. **Keep instructions concise**
   - Avoid redundancy - don't repeat the same guidance in multiple places
   - Be direct - remove verbose explanations that don't add value
   - Prefer bullet points over paragraphs where appropriate

4. **Preserve instruction structure**
   - Keep existing sections (Objective, Task, Process, Output Format, Quality Criteria)
   - Add to appropriate sections rather than restructuring
   - Maintain consistency with other steps

5. **Track changes for changelog**
   - Note what was changed and why
   - Prepare changelog entry for job.yml

### Step 4b: Extract Shared Content into Referenced Files

Review all instruction files for the job and identify content that:
- Appears in multiple step instructions (duplicated)
- Is lengthy and could be extracted for clarity
- Would benefit from being maintained in one place

**Extract to shared files:**

1. **Create shared files** in `.deepwork/jobs/[job_name]/steps/shared/`
   - `conventions.md` - Coding/formatting conventions used across steps
   - `examples.md` - Common examples referenced by multiple steps
   - `schemas.md` - Data structures or formats used throughout

2. **Reference from instructions** using markdown includes or explicit references:
   ```markdown
   ## Conventions

   Follow the conventions defined in `shared/conventions.md`.
   ```

3. **Benefits of extraction:**
   - Single source of truth - update once, applies everywhere
   - Shorter instruction files - easier to read and maintain
   - Consistent guidance across steps

### Step 4.5: Update doc spec Files (doc spec-Related Learnings)

If doc spec-related learnings were identified:

1. **Locate the doc spec file**
   - Find doc spec references in job.yml outputs (look for `doc_spec: .deepwork/doc_specs/[doc_spec_name].md`)
   - doc spec files are at `.deepwork/doc_specs/[doc_spec_name].md`

2. **Update quality_criteria array**
   - Add new criteria with name and description
   - Modify existing criteria descriptions for clarity
   - Remove criteria that are no longer relevant

3. **Update example document**
   - Modify the markdown body to reflect structure changes
   - Ensure the example matches updated criteria

4. **Update metadata as needed**
   - target_audience: If audience has changed
   - frequency: If production cadence has changed
   - path_patterns: If storage location has changed

**Example doc spec update:**
```yaml
# Before
quality_criteria:
  - name: Visualization
    description: Include charts

# After
quality_criteria:
  - name: Visualization
    description: Include Mermaid.js charts showing spend breakdown by service and month-over-month trend
```

### Step 5: Create/Update AGENTS.md (Bespoke Learnings)

The AGENTS.md file captures project-specific knowledge that helps future agent runs.

1. **Determine the correct location**
   - Place AGENTS.md in the deepest common folder that would contain all work on the topic in the future
   - This ensures the knowledge is available when working in that context
   - If uncertain, place at the project root

2. **Use file references where possible**
   - Instead of duplicating information, reference source files
   - This keeps AGENTS.md in sync as the codebase evolves
   - Pattern: "See `path/to/file.ext` for [description]"

3. **AGENTS.md structure**: See `.deepwork/jobs/deepwork_jobs/templates/agents.md.template` for the standard format.

4. **Writing entries**
   - Be concise but specific
   - Always prefer file references over inline content
   - Use line numbers when referencing specific code: `file.ext:42`
   - Group related learnings together

### Step 6: Update Job Version and Changelog

If instruction files were modified:

1. **Bump version in job.yml**
   - Patch version (0.0.x) for instruction improvements
   - Minor version (0.x.0) if quality criteria changed

2. **Add changelog entry**
   ```yaml
   - version: "[new_version]"
     changes: "Improved [step] instructions based on execution learnings: [brief description]"
   ```

### Step 7: Sync and Relay Instructions

1. **Run deepwork sync** (if instructions were modified)
   ```bash
   deepwork sync
   ```

2. **If skills were regenerated**, look at the "To use the new skills" section in the `deepwork sync` output and **relay these exact reload instructions to the user** (e.g., "Type 'exit' then run 'claude --resume'" for Claude Code)

## File Reference Patterns

When adding entries to AGENTS.md, prefer these patterns:

**Good (references)**:
```markdown
- API endpoints follow REST conventions. See `src/api/routes.ts` for examples.
- Error handling pattern: See `src/utils/errors.ts:15-30`
- Configuration schema: Defined in `config/schema.json`
```

**Avoid (duplicating)**:
```markdown
- API endpoints should return JSON with this format: { status: ..., data: ... }
- Error handling should use try/catch with custom error classes
- Configuration requires these fields: name, version, ...
```

## Quality Criteria

- Conversation has been analyzed for job executions
- Points of confusion and inefficiency are identified
- Learnings are correctly classified (generalizable vs bespoke)
- Job instructions updated for generalizable improvements
- Instructions are concise - no redundancy or unnecessary verbosity
- Shared/lengthy content extracted into referenced files where appropriate
- AGENTS.md created/updated with bespoke learnings
- File references used instead of duplicating content
- AGENTS.md is in the correct folder (the deepest common folder for the topic)
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>`

## Example Dialog

```
User: /deepwork_jobs.learn

Claude: I'll analyze this conversation for learnings from DeepWork job executions.

**Conversation Analysis**

I found the following job executions:
1. `/competitive_research.identify_competitors` - Completed
2. `/competitive_research.research_competitors` - Completed with 2 iterations
3. `/competitive_research.comparative_analysis` - Completed

**Identified Issues**

1. **Confusion in step 2**: The instructions didn't specify that competitor research should include pricing information. This caused an extra iteration.

2. **Missing context**: The agent had to ask about the industry focus, which should have been carried forward from step 1.

**Classification**

- Generalizable: Add pricing to research requirements in instructions
- Bespoke: This project focuses on B2B SaaS in the HR tech space

**Actions Taken**

1. Updated `.deepwork/jobs/competitive_research/steps/research_competitors.md`:
   - Added "Include pricing information (tiers, models, approximate ranges)" to research requirements
   - Added note about carrying forward industry context from previous step

2. Created `./competitive_research_output/AGENTS.md`:
   ```markdown
   # Project Context for Competitive Research

   ## Job-Specific Context

   ### competitive_research

   #### Industry Focus
   - Domain: B2B SaaS, HR Technology sector
   - See `identify_competitors_output.md` for market definition

   #### Competitors Identified
   - Reference: `competitor_list.md` for full details

   ## Last Updated
   - Date: 2024-01-15
   - From conversation about: Initial competitive analysis run
   ```

3. Updated job.yml version to 1.0.1 with changelog entry

4. Ran `deepwork sync`

**Summary**

Updated job instructions and created AGENTS.md with bespoke learnings. To get the updated skills, type 'exit' then run 'claude --resume'.
```

## Handling Edge Cases

**No job executions found**:
- Ask user which job they'd like to analyze
- Or offer to review available jobs

**Multiple jobs executed**:
- Analyze each job separately
- Create separate AGENTS.md entries or files as appropriate

**AGENTS.md already exists**:
- Read existing content
- Append new learnings to appropriate sections
- Update "Last Updated" section

**No issues found**:
- Document what worked well
- Consider if any successful patterns should be added to instructions as examples

**Sensitive information**:
- Never include secrets, credentials, or PII in AGENTS.md
- Reference config files instead of including values


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

**User Parameters** - Gather from user before starting:
- **job_name**: Name of the job that was run (optional - will auto-detect from conversation)


## Work Branch

Use branch format: `deepwork/deepwork_jobs-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/deepwork_jobs-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `AGENTS.md`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

Stop hooks will automatically validate your work. The loop continues until all criteria pass.

**Criteria (all must be satisfied)**:
1. **Conversation Analyzed**: Did the agent review the conversation for DeepWork job executions?
2. **Confusion Identified**: Did the agent identify points of confusion, errors, or inefficiencies?
3. **Instructions Improved**: Were job instructions updated to address identified issues?
4. **Instructions Concise**: Are instructions free of redundancy and unnecessary verbosity?
5. **Shared Content Extracted**: Is lengthy/duplicated content extracted into referenced files?
6. **doc spec Reviewed (if applicable)**: For jobs with doc spec outputs, were doc spec-related learnings identified?
7. **doc spec Updated (if applicable)**: Were doc spec files updated with improved quality criteria or structure?
8. **Bespoke Learnings Captured**: Were run-specific learnings added to AGENTS.md?
9. **File References Used**: Do AGENTS.md entries reference other files where appropriate?
10. **Working Folder Correct**: Is AGENTS.md in the correct working folder for the job?
11. **Generalizable Separated**: Are generalizable improvements in instructions, not AGENTS.md?
12. **Sync Complete**: Has `deepwork sync` been run if instructions were modified?


**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "learn complete, outputs: AGENTS.md"

This standalone skill can be re-run anytime.

---

**Reference files**: `.deepwork/jobs/deepwork_jobs/job.yml`, `.deepwork/jobs/deepwork_jobs/steps/learn.md`