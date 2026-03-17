---
name: create-meta-prompts
description: "Generate meta-prompts for Claude-to-Claude pipelines and multi-stage workflows. Use when creating optimized prompts for complex workflows, delegating to subagents, or managing multi-stage execution. Includes XML output structuring, metadata injection, and chain provenance. Not for simple single-turn prompts, manual messaging, or non-Claude integrations. Keywords: prompt chain, delegation, multi-stage, workflow orchestration, Claude-to-Claude."
---

<mission_control>
<objective>Generate meta-prompts for Claude-to-Claude pipelines with structured XML output and metadata for multi-stage workflows.</objective>
<success_criteria>Prompt folder created in .claude/workspace/prompts/, SUMMARY.md generated, chain provenance maintained</success_criteria>
</mission_control>

## Quick Start

**If you need to create a single prompt:** Follow Phase 1 (Intake) → Phase 2 (Generate) → Phase 3 (Present).

**If you need a prompt chain:** Use Chain Detection → Generate multiple prompts → Execute sequentially with dependency handling.

**If you need purpose-specific templates:** Reference ## PATTERN: Purpose Templates for Do/Plan/Research/Refine patterns.

## Navigation

| If you need... | Read this section... |
| :------------- | :------------------- |
| Create a meta-prompt | ## PATTERN: Workflow |
| Purpose-specific templates | ## PATTERN: Purpose Templates |
| Purpose inference | ## PATTERN: Autonomous Purpose Detection |
| Chain detection and dependencies | ## PATTERN: Dependency Management |
| Execution modes | ## PATTERN: Execution Engine |
| SUMMARY.md structure | ## PATTERN: SUMMARY.md Template |
| Common mistakes | ## ANTI-PATTERN: Common Mistakes |
| Quality verification | ## Recognition Questions |

## PATTERN: Workflow

**Generate and execute meta-prompts for multi-stage workflows:**

| Phase | Action | Result |
| :---- | :------ | :------ |
| **1. Intake** | Determine purpose, gather requirements | Clear prompt scope |
| **2. Chain Detection** | Check for existing research/plan files | Referenced context |
| **3. Generate** | Create prompt using purpose-specific patterns | Structured prompt folder |
| **4. Present** | Show decision tree for running | User can execute, review, or save |
| **5. Execute** | Run prompt(s) with dependency-aware engine | XML output with metadata |
| **6. Summarize** | Create SUMMARY.md for human scanning | Quick-ler + key findings |

### Folder Structure

```
.claude/workspace/prompts/
├── 001-auth-research/
│   ├── completed/
│   │   └── 001-auth-research.md    # Prompt (archived after run)
│   ├── auth-research.md            # Full output (XML for Claude)
│   └── SUMMARY.md                  # Executive summary (markdown for human)
├── 002-auth-plan/
│   ├── completed/
│   │   └── 002-auth-plan.md
│   ├── auth-plan.md
│   └── SUMMARY.md
├── 003-auth-implement/
│   ├── completed/
│   │   └── 003-auth-implement.md
│   └── SUMMARY.md                  # Do prompts create code elsewhere
├── 004-auth-research-refine/
│   ├── completed/
│   │   └── 004-auth-research-refine.md
│   ├── archive/
│   │   └── auth-research-v1.md     # Previous version
│   └── SUMMARY.md
```

## PATTERN: Autonomous Purpose Detection

### 1. Purpose Gate (CRITICAL - First Action)

**BEFORE analyzing anything**, infer purpose from context.

**IF context provided:** Infer purpose from keywords:
- `implement`, `build`, `create`, `fix`, `add`, `refactor` → Do
- `plan`, `roadmap`, `approach`, `strategy`, `decide`, `phases` → Plan
- `research`, `understand`, `learn`, `gather`, `analyze`, `explore` → Research
- `refine`, `improve`, `deepen`, `expand`, `iterate`, `update` → Refine

**IF context unclear:** Trust inference from available information. Do not ask questions—proceed with best judgment.

### 2. Topic Identifier

Derive topic from context. Convert to kebab-case automatically:
- Spaces → hyphens
- CamelCase → kebab-case
- Underscores → hyphens

### 3. Chain Detection

Scan `.claude/workspace/prompts/*/` for existing `*-research.md` and `*-plan.md` files. If found:

```yaml
header: "Reference"
question: "Should this prompt reference any existing research or plans?"
options:
  - label: "{file1}"
    description: "Found in .prompts/{folder1}/"
  - label: "{file2}"
    description: "Found in .prompts/{folder2}/"
  - label: "None"
    description: "Start fresh without referencing existing files"
multiSelect: true
```

### 4. Purpose-Specific Questions

**For Do prompts:**

```yaml
header: "Output type"
question: "What are you creating?"
options:
  - label: "Code/feature"
    description: "Software implementation"
  - label: "Document/content"
    description: "Written material, documentation"
  - label: "Design/spec"
    description: "Architecture, wireframes, specifications"
```

```yaml
header: "Scope"
question: "What level of completeness?"
options:
  - label: "Production-ready"
    description: "Ship to users, needs polish and tests"
  - label: "Working prototype"
    description: "Functional but rough edges acceptable"
  - label: "Proof of concept"
    description: "Minimal viable demonstration"
```

**For Plan prompts:**

```yaml
header: "Plan for"
question: "What is this plan leading to?"
options:
  - label: "Implementation"
    description: "Break down how to build something"
  - label: "Decision"
    description: "Weigh options, choose an approach"
  - label: "Process"
    description: "Define workflow or methodology"
```

**For Research prompts:**

```yaml
header: "Depth"
question: "How deep should the research go?"
options:
  - label: "Overview"
    description: "High-level understanding, key concepts"
  - label: "Comprehensive"
    description: "Detailed exploration, multiple perspectives"
  - label: "Exhaustive"
    description: "Everything available, edge cases included"
```

**For Refine prompts:**

```yaml
header: "Target"
question: "Which output should be refined?"
options:
  - label: "{file1}"
    description: "In .prompts/{folder1}/"
  - label: "{file2}"
    description: "In .prompts/{folder2}/"
```

```yaml
header: "Improvement"
question: "What needs improvement?"
options:
  - label: "Deepen analysis"
    description: "Add more detail, examples, or rigor"
  - label: "Expand scope"
    description: "Cover additional areas or topics"
  - label: "Correct errors"
    description: "Fix factual mistakes or outdated info"
  - label: "Restructure"
    description: "Reorganize for clarity or usability"
```

### 5. Decision Gate

After receiving answers, present decision gate:

```yaml
header: "Ready"
question: "Ready to create the prompt?"
options:
  - label: "Proceed"
    description: "Create the prompt with current context"
  - label: "Ask more questions"
    description: "I have more details to clarify"
  - label: "Let me add context"
    description: "I want to provide additional information"
```

Loop until "Proceed" selected.

## PATTERN: Purpose Templates

### Do Pattern (Execution)

```xml
## Objective

{Clear statement of what to build/create/fix}

Purpose: {Why this matters, what it enables}
Output: {What artifact(s) will be produced}

## Context

{Referenced research/plan files if chained}
[topic]-research.md
[topic]-plan.md

{Project context}
[relevant-files]

## Requirements

{Specific functional requirements}
{Quality requirements}
{Constraints and boundaries}

## Implementation

{Specific approaches or patterns to follow}
{What to avoid and WHY}
{Integration points}

## Output

Create/modify files:
- `./path/to/file.ext` - {description}

## Verification

Before declaring complete:
- {Specific test or check}
- {How to confirm it works}
- {Edge cases to verify}

## Success Criteria

{Clear, measurable criteria}
- SUMMARY.md created with files list and next step
```

### Plan Pattern (Roadmaps)

```xml
## Objective

Create a {plan type} for {topic}.

Purpose: {What decision/implementation this enables}
Input: {Research or context being used}
Output: {topic}-plan.md with actionable phases/steps

## Context

Research findings: [research-file]

## Planning Requirements

{What the plan needs to address}
{Constraints to work within}
{Success criteria for the planned outcome}

## Output Structure

Save to: `.prompts/{num}-{topic}-plan/{topic}-plan.md`

Structure using XML:

```xml
<plan>

## Summary

{One paragraph overview of the approach}

  <phases>

#### Phase 1: {Phase Name}

## Objective

{What this phase accomplishes}

## Tasks

<task priority="high">{Specific actionable task}
        <task priority="medium">{Another task}

      <deliverables>
        <deliverable>{What's produced}


## Dependencies

{What must exist before this phase}

    <!-- Additional phases -->


  <metadata>

### {high|medium|low}

{Why this confidence level}


## Dependencies

{External dependencies needed}

    <open_questions>
      {Uncertainties that may affect execution}


## Assumptions

{What was assumed in creating this plan}

```

### Research Pattern (Information Gathering)

```xml
## Objective

Research {topic} to inform {subsequent use}.

Purpose: {What decision/implementation this enables}
Scope: {Boundaries of the research}
Output: {topic}-research.md with structured findings

## Research Scope

<include>
{What to investigate}
{Specific questions to answer}

<exclude>
{What's out of scope}
{What to defer to later research}

## Sources

Priority sources with exact URLs:
Official documentation:
- https://example.com/official-docs

Search queries:
- "{topic} best practices {current_year}"
- "{topic} latest version"

## Verification Checklist

□ Verify ALL known options (enumerate below)
□ Document exact file locations/URLs for each option
□ Verify precedence/hierarchy rules if applicable
□ Confirm syntax and examples from official sources
□ Check for recent updates or changes

## Output Structure

Save to: `.prompts/{num}-{topic}-research/{topic}-research.md`

Structure using XML:

```xml
<research>

## Summary

{2-3 paragraph executive summary of key findings}


  <findings>
    <finding category="{category}">
      <title>{Finding title}
      <detail>{Detailed explanation}
      <source>{Where this came from}
      <relevance>{Why this matters for the goal}


  <recommendations>
    <recommendation priority="high">
      <action>{What to do}

## Rationale

{Why}


  <code_examples>
    {Relevant code patterns, snippets, configurations}


  <metadata>

### {high|medium|low}

{Why this confidence level}


## Dependencies

{What's needed to act on this research}

    <open_questions>
      {What couldn't be determined}


## Assumptions

{What was assumed}


    <quality_report>
      <sources_consulted>
        {List URLs of official documentation}

      <claims_verified>
        {Key findings verified with official sources}

      <claims_assumed>
        {Findings based on inference or incomplete information}


```
```

### Refine Pattern (Iteration)

```xml
## Objective

Refine {topic}-{original_purpose} based on feedback.

Target: [prompt-file]
Current summary: [summary-file]

Purpose: {What improvement is needed}
Output: Updated {topic}-{original_purpose}.md with improvements

## Context

Original output: [prompt-file]

<feedback>
{Specific issues to address}
{What was missing or insufficient}
{Areas needing more depth}

<preserve>
{What worked well and should be kept}
{Structure or findings to maintain}

## Requirements

- Address all feedback points
- Maintain original structure and metadata format
- Keep what worked from previous version
- Update confidence based on improvements

## Output

1. Archive current to: `.prompts/{num}-{topic}-{original_purpose}/archive/{topic}-{original_purpose}-v{n}.md`
2. Write improved to: `.prompts/{num}-{topic}-{original_purpose}/{topic}-{original_purpose}.md`
3. Create SUMMARY.md with version info and changes
```

## PATTERN: Dependency Management

### Detection

Scan prompt contents for cross-references to determine dependencies:

1. Parse each prompt for `.claude/workspace/prompts/{number}-{topic}/` patterns
2. Build dependency graph
3. Detect cycles (error if found)
4. Determine execution order

### Inference Rules

If no explicit cross-references found, infer from purpose:

- Research prompts: No dependencies (can run parallel)
- Plan prompts: Depend on same-topic research
- Do prompts: Depend on same-topic plan

Override with explicit references when present.

### Missing Dependencies

If a prompt references output that doesn't exist:

1. Check if it's another prompt in this session (will be created)
2. Check if it exists in `.claude/workspace/prompts/*/` (already completed)
3. If truly missing: Warn user and offer options

## PATTERN: Execution Engine

### Single Prompt

1. Read prompt file contents
2. Delegate to implementation specialist
3. Include: complete prompt contents, output location
4. Wait for completion
5. Validate output
6. Archive prompt to `completed/` subfolder
7. Report results with next-step options

### Sequential Execution

For chained prompts where each depends on previous output.

1. Build execution queue from dependency order
2. For each prompt:
   a. Read prompt file
   b. Spawn Task agent
   c. Wait for completion
   d. Validate output
   e. If validation fails → stop, report failure, offer recovery
   f. If success → archive prompt, continue
3. Report consolidated results

**Progress Reporting:**
```
Executing 1/3: 001-auth-research... ✅
Executing 2/3: 002-auth-plan... ✅
Executing 3/3: 003-auth-implement... (running)
```

### Parallel Execution

For independent prompts with no dependencies.

1. Read all prompt files
2. **CRITICAL**: Spawn ALL Task agents in a SINGLE message
3. Wait for all to complete
4. Validate all outputs
5. Archive all prompts
6. Report consolidated results

### Mixed Dependencies (DAGs)

For complex graphs (e.g., two parallel research → one plan).

1. Analyze dependency graph from file references
2. Group into execution layers:
   - Layer 1: No dependencies (run parallel)
   - Layer 2: Depends only on layer 1
   - Layer 3: Depends on layer 2, etc.
3. Execute each layer (parallel within, sequential between)
4. Stop if any dependency fails

**Example:**
```
Layer 1 (parallel): 001-api-research, 002-db-research
Layer 2 (after layer 1): 003-architecture-plan
```

## PATTERN: SUMMARY.md Template

Every executed prompt creates this file for human scanning:

```markdown
# {Topic} {Purpose} Summary

**{Substantive one-liner describing outcome}**

## Version
{v1 or "v2 (refined from v1)"}

## Changes from Previous
{Only include if v2+}

## Key Findings
- {Most important finding or action}
- {Second key item}
- {Third key item}

## Files Created
{Only include for Do prompts}
- `path/to/file.ts` - Description

## Decisions Needed
{Specific actionable decisions, or "None"}

## Blockers
{External impediments, or "None"}

## Next Step
{Concrete forward action}

---
*Confidence: {High|Medium|Low}*
*Iterations: {n}*
*Full output: {filename.md}*
```

### One-Liner Requirements

Must be substantive - describes actual outcome, not status.

| Good | Bad |
| :--- | :--- |
| "JWT with jose library and httpOnly cookies recommended" | "Research completed" |
| "4-phase implementation: types → JWT core → refresh → tests" | "Plan created" |
| "JWT middleware complete with 6 files in src/auth/" | "Implementation finished" |

### Purpose Variations

- **Research**: Emphasize key recommendation, decision readiness. Next step: Create plan.
- **Plan**: Emphasize phase breakdown, assumptions needing validation. Next step: Execute first phase.
- **Do**: Emphasize files created, test status. Next step: Run tests or execute next phase.
- **Refine**: Emphasize what improved, version number. Include Changes from Previous.

## PATTERN: Metadata Requirements

For Research and Plan outputs, require XML metadata:

```xml
<metadata>

### {high|medium|low}

{Why this confidence level}


## Dependencies

{External requirements that must be met}

    <open_questions>
      {What couldn't be determined or needs validation}


## Assumptions

{Context assumed that might need validation}

```

### Confidence Levels

- **high**: Official docs, verified patterns, clear consensus, few unknowns
- **medium**: Mixed sources, some outdated info, minor gaps, reasonable approach
- **low**: Sparse documentation, conflicting info, significant unknowns, best guess

## ANTI-PATTERN: Common Mistakes

### Mistake 1: Skipping Chain Detection

❌ **Wrong:** Created new research prompt without checking existing prompts → Duplicate work.

✅ **Correct:** Before generating, scan `.claude/workspace/prompts/*/` for existing research/plan files → Reference existing outputs.

### Mistake 2: Missing Metadata in Research/Plan Outputs

❌ **Wrong:** Prompt outputs research.md without `<confidence>`, `<dependencies>`, `<assumptions>` → Planning prompt lacks context.

✅ **Correct:** Include metadata requirements in prompt template.

### Mistake 3: Empty SUMMARY.md

❌ **Wrong:** Created SUMMARY.md with "Research completed" → No value for human scanning.

✅ **Correct:** Require substantive SUMMARY.md with one-liner, key findings, decisions, blockers, next step.

### Mistake 4: No Validation Before Archiving

❌ **Wrong:** Archived prompt immediately after execution without checking output → Broken chains continue downstream.

✅ **Correct:** Validate before archiving: file exists, not empty, required metadata present, SUMMARY.md created.

### Mistake 5: Sequential Failure Without Stop

❌ **Wrong:** Prompt 2 of 3 failed → Continued to prompt 3 → Waste.

✅ **Correct:** For sequential chains, stop immediately on failure:
```
❌ Failed at 2/3: 002-auth-plan
Completed: 001-auth-research ✅
Not started: 003-auth-implement
```

### Mistake 6: Missing Decision Tree

❌ **Wrong:** Created prompt → Immediately executed → User had no opportunity to review.

✅ **Correct:** Present decision tree after prompt creation:
```
Prompt created. What's next?
1. Run now
2. Review/edit first
3. Save for later
```

### Mistake 7: Asking Instead of Inferring

❌ **Wrong:** Ask "What do you want?" without attempting inference first.

✅ **Correct:** Trust ability to infer from context. If context is sparse, make educated assumptions and proceed.

## EDGE: Validation

### Output Validation Checklist

After each prompt completes, verify:

1. **File exists**: Check output file was created
2. **Not empty**: File has content (> 100 chars)
3. **Metadata present** (for research/plan): Check for required XML tags
4. **SUMMARY.md exists**: Check SUMMARY.md was created
5. **SUMMARY.md complete**: Has required sections
6. **One-liner is substantive**: Not generic like "Research completed"

### Validation Failure Handling

If validation fails:

- Report what's missing
- Offer options:
  - Retry the prompt
  - Continue anyway (for non-critical issues)
  - Stop and investigate

### Sequential Failure

Stop the chain immediately:

```
❌ Failed at 2/3: 002-auth-plan
Completed:
- 001-auth-research ✅ (archived)
Failed:
- 002-auth-plan: Output file not created
Not started:
- 003-auth-implement
What's next?
1. Retry 002-auth-plan
2. View error details
3. Stop here (keep completed work)
```

### Parallel Failure

Continue others, report all results:

```
Parallel execution completed with errors:
✅ 001-api-research (archived)
❌ 002-db-research: Validation failed - missing <confidence> tag
✅ 003-ui-research (archived)
What's next?
1. Retry failed prompt (002)
2. View error details
3. Continue without 002
```

## Recognition Questions

| Question | Recognition |
| :------- | :---------- |
| Purpose identified correctly? | Do/Plan/Research/Refine inferred from context |
| Topic identifier derived? | kebab-case format, auto-converted |
| Chain detection performed? | Existing research/plan files scanned and referenced |
| Correct purpose template used? | Do/Plan/Research/Refine pattern matched to purpose |
| Purpose inferred autonomously? | No AskUserQuestion used—trust inference |
| Prompt folder created correctly? | `.claude/workspace/prompts/{number}-{topic}-{purpose}/` |
| Output location specified? | Prompt includes file path for output |
| SUMMARY.md requirement included? | All prompts require human-scannable summary |
| Metadata requirements included? | Research/Plan outputs require XML metadata |
| Validation checklist complete? | File exists, content present, metadata valid |

---

<critical_constraint>
**Portability Invariant:** This skill must work in a project with ZERO external rules access (no CLAUDE.md, CLAUDE.local.md, or .claude/rules/ dependencies). All necessary patterns and philosophy are self-contained in this file. Never use relative paths pointing outside the skill itself. When referencing other components, use: "invoke `skill-name`" or "invoke `skill-name` and read its file".
</critical_constraint>
