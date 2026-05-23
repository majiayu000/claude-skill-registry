---
name: deepwork_jobs.define
description: "Creates a job.yml specification by gathering workflow requirements through structured questions. Use when starting a new multi-step workflow."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **User Understanding**: Did the agent fully understand the user's workflow by asking structured questions?
            2. **Structured Questions Used**: Did the agent ask structured questions (using the AskUserQuestion tool) to gather user input?
            3. **Document Detection**: For document-oriented workflows, did the agent detect patterns and offer doc spec creation?
            4. **doc spec Created (if applicable)**: If a doc spec was needed, was it created in `.deepwork/doc_specs/[doc_spec_name].md` with proper quality criteria?
            5. **doc spec References**: Are document outputs properly linked to their doc specs using `{file, doc_spec}` format?
            6. **Valid Against doc spec**: Does the job.yml conform to the job.yml doc spec quality criteria (valid identifier, semantic version, concise summary, rich description, complete steps, valid dependencies)?
            7. **Clear Inputs/Outputs**: Does every step have clearly defined inputs and outputs?
            8. **Logical Dependencies**: Do step dependencies make sense and avoid circular references?
            9. **Concise Summary**: Is the summary under 200 characters and descriptive?
            10. **Rich Description**: Does the description provide enough context for future refinement?
            11. **Valid Schema**: Does the job.yml follow the required schema (name, version, summary, steps)?
            12. **File Created**: Has the job.yml file been created in `.deepwork/jobs/[job_name]/job.yml`?

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

            1. **User Understanding**: Did the agent fully understand the user's workflow by asking structured questions?
            2. **Structured Questions Used**: Did the agent ask structured questions (using the AskUserQuestion tool) to gather user input?
            3. **Document Detection**: For document-oriented workflows, did the agent detect patterns and offer doc spec creation?
            4. **doc spec Created (if applicable)**: If a doc spec was needed, was it created in `.deepwork/doc_specs/[doc_spec_name].md` with proper quality criteria?
            5. **doc spec References**: Are document outputs properly linked to their doc specs using `{file, doc_spec}` format?
            6. **Valid Against doc spec**: Does the job.yml conform to the job.yml doc spec quality criteria (valid identifier, semantic version, concise summary, rich description, complete steps, valid dependencies)?
            7. **Clear Inputs/Outputs**: Does every step have clearly defined inputs and outputs?
            8. **Logical Dependencies**: Do step dependencies make sense and avoid circular references?
            9. **Concise Summary**: Is the summary under 200 characters and descriptive?
            10. **Rich Description**: Does the description provide enough context for future refinement?
            11. **Valid Schema**: Does the job.yml follow the required schema (name, version, summary, steps)?
            12. **File Created**: Has the job.yml file been created in `.deepwork/jobs/[job_name]/job.yml`?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response OR
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met AND the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
---

# deepwork_jobs.define

**Step 1/4** in **deepwork_jobs** workflow

> Creates and manages multi-step AI workflows. Use when defining, implementing, or improving DeepWork jobs.


## Instructions

**Goal**: Creates a job.yml specification by gathering workflow requirements through structured questions. Use when starting a new multi-step workflow.

# Define Job Specification

## Objective

Create a `job.yml` specification file that defines the structure of a new DeepWork job by thoroughly understanding the user's workflow requirements through an interactive question-and-answer process.

## Task

Guide the user through defining a job specification by asking structured questions. **Do not attempt to create the specification without first fully understanding the user's needs.**

**Important**: Use the AskUserQuestion tool to ask structured questions when gathering information from the user. This provides a better user experience with clear options and guided choices.

The output of this step is **only** the `job.yml` file - a complete specification of the workflow. The actual step instruction files will be created in the next step (`implement`).

### Step 1: Understand the Job Purpose

Start by asking structured questions to understand what the user wants to accomplish:

1. **What is the overall goal of this workflow?**
   - What complex task are they trying to accomplish?
   - What domain is this in? (e.g., research, marketing, development, reporting)
   - How often will they run this workflow?

2. **What does success look like?**
   - What's the final deliverable or outcome?
   - Who is the audience for the output?
   - What quality criteria matter most?

3. **What are the major phases?**
   - Ask them to describe the workflow at a high level
   - What are the distinct stages from start to finish?
   - Are there any dependencies between phases?

### Step 1.5: Detect Document-Oriented Workflows

**Check for document-focused patterns** in the user's description:
- Keywords: "report", "summary", "document", "create", "monthly", "quarterly", "for stakeholders", "for leadership"
- Final deliverable is a specific document (e.g., "AWS spending report", "competitive analysis", "sprint summary")
- Recurring documents with consistent structure

**If a document-oriented workflow is detected:**

1. Inform the user: "This workflow produces a specific document type. I recommend defining a doc spec first to ensure consistent quality."

2. Ask structured questions to understand if they want to:
   - Create a doc spec for this document
   - Use an existing doc spec (if any exist in `.deepwork/doc_specs/`)
   - Skip doc spec and proceed with simple outputs

### Step 1.6: Define the Doc Spec (if needed)

When creating a doc spec, gather the following information:

1. **Document Identity**
   - What is the document called? (e.g., "Monthly AWS Spending Report")
   - Brief description of its purpose
   - Where should these documents be stored? (path patterns like `finance/aws-reports/*.md`)

2. **Audience and Context**
   - Who reads this document? (target audience)
   - How often is it produced? (frequency)

3. **Quality Criteria** (3-5 criteria, each with name and description)
   Examples for a spending report:
   - **Visualization**: Must include charts showing spend breakdown by service
   - **Variance Analysis**: Must compare current month against previous with percentages
   - **Action Items**: Must include recommended cost optimization actions

4. **Document Structure**
   - What sections should it have?
   - Any required elements (tables, charts, summaries)?

### Step 1.7: Create the doc spec File (if needed)

Create the doc spec file at `.deepwork/doc_specs/[doc_spec_name].md`:

**Template reference**: See `.deepwork/jobs/deepwork_jobs/templates/doc_spec.md.template` for the standard structure.

**Complete example**: See `.deepwork/jobs/deepwork_jobs/templates/doc_spec.md.example` for a fully worked example.

After creating the doc spec, proceed to Step 2 with the doc spec reference for the final step's output.

### Step 2: Define Each Step

For each major phase they mentioned, ask structured questions to gather details:

1. **Step Purpose**
   - What exactly does this step accomplish?
   - What is the input to this step?
   - What is the output from this step?

2. **Step Inputs**
   - What information is needed to start this step?
   - Does it need user-provided parameters? (e.g., topic, target audience)
   - Does it need files from previous steps?
   - What format should inputs be in?

3. **Step Outputs**
   - What files or artifacts does this step produce?
   - What format should the output be in? (markdown, YAML, JSON, etc.)
   - Where should each output be saved? (filename/path)
   - Should outputs be organized in subdirectories? (e.g., `reports/`, `data/`, `drafts/`)
   - Will other steps need this output?

   **Important**: Output paths should always be within the main repository directory structure, not in dot-directories like `.deepwork/`. Dot-directories are for configuration and job definitions, not for job outputs. Use paths like `research/competitors/report.md` rather than `.deepwork/outputs/report.md`.
   - **Does this output have a doc spec?** If a doc spec was created in Step 1.6/1.7, reference it for the appropriate output

4. **Step Dependencies**
   - Which previous steps must complete before this one?
   - Are there any ordering constraints?

5. **Step Process** (high-level understanding)
   - What are the key activities in this step?
   - Are there any quality checks or validation needed?
   - What makes a good vs. bad output for this step?

**Note**: You're gathering this information to understand what instructions will be needed, but you won't create the instruction files yet - that happens in the `implement` step.

#### Doc Spec-Aware Output Format

When a step produces a document with a doc spec reference, use this format in job.yml:

```yaml
outputs:
  - file: reports/monthly_spending.md
    doc_spec: .deepwork/doc_specs/monthly_aws_report.md
```

The doc spec's quality criteria will automatically be included in the generated skill, ensuring consistent document quality.

### Capability Considerations

When defining steps, identify any that require specialized tools:

**Browser Automation**: If any step involves web scraping, form filling, interactive browsing, UI testing, or research requiring website visits, ask the user what browser tools they have available. For Claude Code users, **Claude in Chrome** (Anthropic's browser extension) has been tested with DeepWork and is recommended for new users. Don't assume a default—confirm the tool before designing browser-dependent steps.

### Step 3: Validate the Workflow

After gathering information about all steps:

1. **Review the flow**
   - Summarize the complete workflow
   - Show how outputs from one step feed into the next
   - Ask if anything is missing

2. **Check for gaps**
   - Are there any steps where the input isn't clearly defined?
   - Are there any outputs that aren't used by later steps?
   - Are there circular dependencies?

3. **Confirm details**
   - Job name (lowercase, underscores, descriptive)
   - Job summary (one clear sentence, max 200 chars)
   - Job description (detailed multi-line explanation)
   - Version number (start with 1.0.0)

### Step 4: Define Quality Validation (Stop Hooks)

For each step, consider whether it would benefit from **quality validation loops**. Stop hooks allow the AI agent to iteratively refine its work until quality criteria are met.

**Ask structured questions about quality validation:**
- "Are there specific quality criteria that must be met for this step?"
- "Would you like the agent to validate its work before completing?"
- "What would make you send the work back for revision?"

**Stop hooks are particularly valuable for:**
- Steps with complex outputs that need multiple checks
- Steps where quality is critical (final deliverables)
- Steps with subjective quality criteria that benefit from AI self-review

**Three types of stop hooks are supported:**

1. **Inline Prompt** (`prompt`) - Best for simple quality criteria
   ```yaml
   stop_hooks:
     - prompt: |
         Verify the output meets these criteria:
         1. Contains at least 5 competitors
         2. Each competitor has a description
         3. Selection rationale is clear
   ```

2. **Prompt File** (`prompt_file`) - For detailed/reusable criteria
   ```yaml
   stop_hooks:
     - prompt_file: hooks/quality_check.md
   ```

3. **Script** (`script`) - For programmatic validation (tests, linting)
   ```yaml
   stop_hooks:
     - script: hooks/run_tests.sh
   ```

**Multiple hooks can be combined:**
```yaml
stop_hooks:
  - script: hooks/lint_output.sh
  - prompt: "Verify the content is comprehensive and well-organized"
```

**Encourage prompt-based hooks** - They leverage the AI's ability to understand context and make nuanced quality judgments. Script hooks are best for objective checks (syntax, format, tests).

### Step 5: Create the Job Directory and Specification

Only after you have complete understanding, create the job directory and `job.yml` file:

**First, create the directory structure** using the `make_new_job.sh` script:

```bash
.deepwork/jobs/deepwork_jobs/make_new_job.sh [job_name]
```

This creates:
- `.deepwork/jobs/[job_name]/` - Main job directory
- `.deepwork/jobs/[job_name]/steps/` - For step instruction files
- `.deepwork/jobs/[job_name]/hooks/` - For custom validation scripts
- `.deepwork/jobs/[job_name]/templates/` - For example file formats
- `.deepwork/jobs/[job_name]/AGENTS.md` - Job management guidance

**Then create the job.yml file** at `.deepwork/jobs/[job_name]/job.yml`

(Where `[job_name]` is the name of the NEW job you're creating, e.g., `competitive_research`)

**Doc Spec**: See `.deepwork/doc_specs/job_spec.md` for the complete specification with quality criteria.

**Template reference**: See `.deepwork/jobs/deepwork_jobs/templates/job.yml.template` for the standard structure.

**Complete example**: See `.deepwork/jobs/deepwork_jobs/templates/job.yml.example` for a fully worked example.

**Important**:
- Use lowercase with underscores for job name and step IDs
- Ensure file inputs reference steps in dependencies
- No circular dependencies
- At least one output per step
- The `summary` should be concise (max 200 chars)
- The `description` should provide rich context for future refinement
- Include a `changelog` section with an initial entry for version 1.0.0

## Example Dialog

```
Claude: I'll help you define a new DeepWork job. Let's start by understanding what you're trying to accomplish.

What complex task or workflow are you trying to create? What's the overall goal?

User: I want to create competitive research reports for my company

Claude: Great! Let's dig into that. A few questions:

1. What's the final deliverable? Is it a written report, a presentation, or something else?
2. Who is the audience? Your team, executives, clients?
3. How comprehensive should these reports be?

User: It's a written report for our product team. Should be comprehensive - analyzing 3-5 competitors.

Claude: Perfect. Now let's think about the major phases of creating this report. What are the main stages you go through? For example:
- Identifying which competitors to analyze?
- Gathering information about them?
- Analyzing the data?
- Writing the report?

Or is your process different?

User: Yes, that's close. I would say:
1. Identify competitors
2. Research each one
3. Create comparison analysis
4. Write positioning recommendations

Claude: Excellent! Now let's define each step in detail. Starting with "Identify competitors":

1. What inputs do you need to start? Do you already have a market segment in mind, or do you need to specify that?
2. What should the output look like? A list of competitor names? More detailed?
3. How many competitors should be identified?

User: I need to specify the market segment and product category as inputs. The output should be a markdown file with 5-7 competitors and brief descriptions of each.

Claude: Perfect. A few more questions about that output:
1. What should the file be called? Something like `competitors_list.md`?
2. Should it go in the project root, or in a subdirectory like `research/` or `data/`?

User: Just call it `competitors_list.md` in the project root.

Claude: Great. Now for the "Research each one" step:
1. Does it use the competitor list from the first step as input?
2. What kind of research - product features, pricing, marketing, all of the above?
3. What format should the research output be in?
4. Where should that research be saved?

[continues for each step...]

[After gathering all information:]

Claude: Let me summarize the workflow I've designed based on our conversation:

**Job: competitive_research**
Summary: Systematic competitive analysis workflow for product positioning

Description:
A comprehensive workflow for analyzing competitors in your market segment. This job helps product teams understand the competitive landscape by systematically identifying competitors, researching their offerings, creating comparison matrices, and developing strategic positioning recommendations.

The workflow produces:
- A vetted list of key competitors
- Detailed research notes on each competitor
- A comparison matrix highlighting key differentiators
- Strategic positioning recommendations

Designed for product teams conducting quarterly competitive analysis.

**Steps:**

Step 1: identify_competitors
- Input: market_segment (user), product_category (user)
- Output: competitors_list.md (5-7 competitors with descriptions)

Step 2: research_competitors
- Input: competitors_list.md (from step 1)
- Output: research_notes.md (detailed findings for each competitor)
- Depends on: identify_competitors

Step 3: comparative_analysis
- Input: research_notes.md (from step 2)
- Output: comparison_matrix.md (side-by-side analysis)
- Depends on: research_competitors

Step 4: positioning_recommendations
- Input: comparison_matrix.md (from step 3)
- Output: positioning_report.md (strategic recommendations)
- Depends on: comparative_analysis

Does this accurately capture your workflow? Any changes needed?

User: Yes, that's perfect!

Claude: Great! Creating the job.yml specification now...

[Creates .deepwork/jobs/competitive_research/job.yml with the complete spec]

✓ Job specification created!

**File created:**
- .deepwork/jobs/competitive_research/job.yml

**Next step:**
Run `/deepwork_jobs.review_job_spec` to validate the specification against quality criteria.
```

## Important Guidelines

1. **Focus on specification only** - Don't create instruction files yet
2. **Ask structured questions** - Never skip the discovery phase; use the AskUserQuestion tool
3. **Rich context in description** - This helps with future refinement
4. **Validate understanding** - Summarize and confirm before creating
5. **Use examples** - Help users understand what good specifications look like
6. **Understand file organization** - Always ask structured questions about where outputs should be saved and if subdirectories are needed

## Validation Rules

Before creating the job.yml, ensure:
- Job name: lowercase, underscores, no spaces
- Version: semantic versioning (1.0.0)
- Summary: concise, under 200 characters
- Description: detailed, provides context
- Step IDs: unique, descriptive, lowercase with underscores
- Dependencies: must reference existing step IDs
- File inputs: `from_step` must be in dependencies
- At least one output per step
- Outputs can be filenames (e.g., `report.md`) or paths (e.g., `reports/analysis.md`)
- File paths in outputs should match where files will actually be created
- No circular dependencies

## Output Format

### job.yml

The complete YAML specification file (example shown in Step 5 above).

**Location**: `.deepwork/jobs/[job_name]/job.yml`

(Where `[job_name]` is the name of the new job being created)

After creating the file:
1. Inform the user that the specification is complete
2. Recommend that they review the job.yml file
3. Tell them to run `/deepwork_jobs.review_job_spec` next

## Quality Criteria

- Asked structured questions to fully understand user requirements
- User fully understands what job they're creating
- All steps have clear inputs and outputs
- Dependencies make logical sense
- Summary is concise and descriptive
- Description provides rich context for future refinement
- Specification is valid YAML and follows the schema
- Ready for implementation step


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
- **job_purpose**: What complex task or workflow are you trying to accomplish?


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
1. **User Understanding**: Did the agent fully understand the user's workflow by asking structured questions?
2. **Structured Questions Used**: Did the agent ask structured questions (using the AskUserQuestion tool) to gather user input?
3. **Document Detection**: For document-oriented workflows, did the agent detect patterns and offer doc spec creation?
4. **doc spec Created (if applicable)**: If a doc spec was needed, was it created in `.deepwork/doc_specs/[doc_spec_name].md` with proper quality criteria?
5. **doc spec References**: Are document outputs properly linked to their doc specs using `{file, doc_spec}` format?
6. **Valid Against doc spec**: Does the job.yml conform to the job.yml doc spec quality criteria (valid identifier, semantic version, concise summary, rich description, complete steps, valid dependencies)?
7. **Clear Inputs/Outputs**: Does every step have clearly defined inputs and outputs?
8. **Logical Dependencies**: Do step dependencies make sense and avoid circular references?
9. **Concise Summary**: Is the summary under 200 characters and descriptive?
10. **Rich Description**: Does the description provide enough context for future refinement?
11. **Valid Schema**: Does the job.yml follow the required schema (name, version, summary, steps)?
12. **File Created**: Has the job.yml file been created in `.deepwork/jobs/[job_name]/job.yml`?


**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 1/4 complete, outputs: job.yml"
3. **Continue workflow**: Use Skill tool to invoke `/deepwork_jobs.review_job_spec`

---

**Reference files**: `.deepwork/jobs/deepwork_jobs/job.yml`, `.deepwork/jobs/deepwork_jobs/steps/define.md`