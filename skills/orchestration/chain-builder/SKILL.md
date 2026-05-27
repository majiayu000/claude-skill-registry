---
name: Chain Builder
slug: chain-builder
description: Build and execute multi-step prompt chains for complex tasks
category: meta
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "build a chain"
  - "create prompt chain"
  - "chain these prompts"
  - "sequence these tasks"
  - "chain builder"
tags:
  - prompt-chaining
  - automation
  - workflow
---

# Chain Builder

The Chain Builder skill helps you design and execute multi-step prompt chains where the output of one prompt becomes the input to the next. This enables complex, multi-stage processing that would be difficult to accomplish in a single prompt, while maintaining clarity, modularity, and debuggability.

This skill guides you through chain design, identifying optimal breakpoints, managing data flow between steps, handling errors, and validating outputs at each stage. It's particularly valuable for tasks that involve multiple distinct phases like research → analysis → synthesis → formatting, or ideation → planning → implementation → review.

Use this skill when you have complex tasks that benefit from sequential processing, when you need intermediate validation between steps, or when different parts of a task require different specialized prompts or tools.

## Core Workflows

### Workflow 1: Design Prompt Chain from Goal
1. **Clarify** the end goal:
   - What's the final output?
   - What quality standards apply?
   - What constraints exist?
2. **Decompose** into logical stages:
   - Identify distinct phases
   - Determine stage boundaries
   - Order by dependencies
3. **Design** individual prompts:
   - Purpose of each stage
   - Input requirements
   - Output specifications
   - Success criteria
4. **Define** data flow:
   - What passes between stages?
   - What format for intermediate outputs?
   - What state is maintained?
5. **Add** validation:
   - Checkpoints after each stage
   - Quality gates
   - Error handling
6. **Document** the chain:
   - Chain purpose
   - Stage descriptions
   - Data flow diagram
   - Usage examples
7. **Test** end-to-end

### Workflow 2: Execute Existing Chain
1. **Load** chain definition:
   - Read chain specification
   - Understand stages
   - Prepare inputs
2. **Initialize** chain state:
   - Set initial inputs
   - Prepare storage for outputs
   - Initialize tracking
3. **Execute** each stage sequentially:
   - Run stage prompt
   - Validate output
   - **If validation fails**: Handle error
   - **If validation passes**: Continue
   - Store intermediate result
   - Pass output to next stage
4. **Monitor** progress:
   - Track current stage
   - Log outputs
   - Report status
5. **Validate** final output
6. **Report** results and any issues

### Workflow 3: Debug Chain Failure
1. **Identify** failure point:
   - Which stage failed?
   - What was the input to that stage?
   - What error occurred?
2. **Analyze** root cause:
   - Was input malformed?
   - Was prompt unclear?
   - Was validation too strict?
   - Was context insufficient?
3. **Test** stage in isolation:
   - Run stage with known good input
   - Verify prompt works correctly
   - Check output format
4. **Fix** the issue:
   - Update prompt if unclear
   - Adjust validation if too strict
   - Add error handling if needed
   - Improve data passing if malformed
5. **Retest** from failure point
6. **Document** the fix

### Workflow 4: Optimize Chain Performance
1. **Analyze** current chain:
   - Execution time per stage
   - Token usage per stage
   - Success rate per stage
   - Bottlenecks
2. **Identify** optimization opportunities:
   - Stages that could be parallelized
   - Redundant processing
   - Overly complex prompts
   - Unnecessary validation
3. **Refactor** for efficiency:
   - Combine related stages
   - Parallelize independent stages
   - Simplify prompts
   - Optimize data passing
4. **Maintain** quality:
   - Don't sacrifice accuracy for speed
   - Keep validation comprehensive
   - Preserve error handling
5. **Test** optimized chain
6. **Measure** improvements

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Design new chain | "Design a prompt chain for [goal]" |
| Execute chain | "Run this chain: [chain spec]" |
| Debug chain failure | "Debug this chain: [error details]" |
| Optimize chain | "Optimize this chain: [chain spec]" |
| Validate chain design | "Review this chain design: [spec]" |
| Add stage to chain | "Add stage for [purpose] to this chain" |
| Parallelize stages | "Which stages can run in parallel?" |

## Best Practices

- **Keep Stages Focused**: Each stage should have one clear purpose
  - Don't mix research and analysis in one prompt
  - Don't combine formatting with content generation
  - Each stage = one transformation

- **Make Outputs Explicit**: Define exactly what each stage produces
  - Specify format (JSON, markdown, etc.)
  - Define required fields
  - Set quality criteria
  - Provide examples

- **Validate Between Stages**: Catch errors early
  - Check output format
  - Verify required fields exist
  - Validate against criteria
  - Fail fast if something's wrong

- **Handle Errors Gracefully**: Plan for failures
  - Define retry logic
  - Provide fallback options
  - Log failures for debugging
  - Don't cascade bad data

- **Maintain State Carefully**: Track what you need, discard what you don't
  - Pass only necessary data forward
  - Keep intermediate outputs for debugging
  - Clear state between independent chains
  - Version chain state if long-running

- **Optimize Data Passing**: Minimize token usage
  - Extract only needed information
  - Summarize when possible
  - Use references instead of duplication
  - Compress verbose outputs

- **Document Thoroughly**: Make chains maintainable
  - Purpose of each stage
  - Expected inputs/outputs
  - Validation rules
  - Error handling
  - Example executions

- **Test Incrementally**: Build confidence stage by stage
  - Test each stage in isolation
  - Test pairs of stages
  - Test full chain
  - Test with edge cases

## Chain Design Patterns

### Sequential Processing
```
Stage 1: Collect → Stage 2: Process → Stage 3: Format → Output
```
**Use when**: Each stage depends on previous stage's complete output
**Example**: Web scraping → Data cleaning → Analysis → Report generation

### Branching Chain
```
Stage 1: Analyze →
  If condition A: Stage 2a → Merge
  If condition B: Stage 2b → Merge
→ Stage 3: Synthesize
```
**Use when**: Different processing paths based on criteria
**Example**: File type detection → [JSON parser | CSV parser | XML parser] → Normalize

### Parallel Aggregation
```
Input →
  [Stage 1a, Stage 1b, Stage 1c] (parallel) →
  Stage 2: Combine →
  Output
```
**Use when**: Independent analyses that merge later
**Example**: [Syntax check, Type check, Lint] → Aggregate results → Report

### Iterative Refinement
```
Stage 1: Generate →
Stage 2: Critique →
  If quality met: Output
  If not: Refine → back to Stage 1 (max N iterations)
```
**Use when**: Output quality improves through iteration
**Example**: Write → Review → [Good? → Done | Revise → Write]

### Fan-Out/Fan-In
```
Stage 1: Split →
  [Process chunk 1, Process chunk 2, ..., Process chunk N] →
  Stage 2: Merge →
  Output
```
**Use when**: Large input needs parallel processing
**Example**: Split document → [Analyze sections] → Synthesize findings

### Pipeline with Validation
```
Stage 1 → Validate → Stage 2 → Validate → Stage 3 → Validate → Output
```
**Use when**: Quality gates needed between stages
**Example**: Generate → Check syntax → Transform → Check schema → Deploy → Verify

## Chain Specification Format

```yaml
chain:
  name: "Chain Name"
  description: "What this chain accomplishes"
  version: "1.0.0"

  stages:
    - id: "stage_1"
      name: "Stage Name"
      prompt: "Prompt template with {{placeholders}}"
      inputs:
        - name: "input_name"
          source: "user_input | previous_stage | context"
          required: true
      outputs:
        - name: "output_name"
          format: "json | markdown | text"
          schema: "Optional JSON schema"
      validation:
        - type: "format | content | schema"
          rule: "Validation rule"
          on_fail: "retry | skip | abort"
      on_error:
        action: "retry | fallback | abort"
        max_retries: 3

    - id: "stage_2"
      name: "Next Stage"
      prompt: "Use {{stage_1.output_name}} to..."
      # ... rest of stage definition

  execution:
    mode: "sequential | parallel | conditional"
    timeout_per_stage: 300
    max_total_time: 1800
```

## Example Chains

### Research → Analysis → Report Chain
```markdown
**Chain**: Research Report Generator

**Stage 1**: Web Research
- Prompt: "Research [topic] using web search. Find 5-10 authoritative sources."
- Output: List of sources with summaries
- Validation: At least 5 sources, each with URL and summary

**Stage 2**: Content Analysis
- Input: Sources from Stage 1
- Prompt: "Analyze these sources and extract key themes, findings, and insights."
- Output: Structured analysis (JSON)
- Validation: JSON schema with required fields

**Stage 3**: Report Writing
- Input: Analysis from Stage 2
- Prompt: "Write executive report based on analysis. Include summary, findings, recommendations."
- Output: Markdown report
- Validation: Contains required sections

**Stage 4**: Formatting
- Input: Report from Stage 3
- Prompt: "Format report for [platform] with proper structure and styling."
- Output: Platform-ready document
```

### Code Generation → Review → Test Chain
```markdown
**Chain**: Tested Code Generator

**Stage 1**: Generate Code
- Prompt: "Generate [component] with [requirements]"
- Output: Code file(s)
- Validation: Valid syntax, includes all required functions

**Stage 2**: Code Review
- Input: Code from Stage 1
- Prompt: "Review code for bugs, performance issues, best practices"
- Output: Review findings (JSON)
- Validation: Categorized by severity

**Stage 3**: Apply Fixes
- Input: Code and Review findings
- Prompt: "Fix high and medium severity issues"
- Output: Revised code
- Validation: Addresses all high-severity issues

**Stage 4**: Generate Tests
- Input: Final code
- Prompt: "Generate unit tests with >80% coverage"
- Output: Test file(s)
- Validation: Tests run and pass

**Stage 5**: Verify
- Input: Code and tests
- Action: Run tests
- Output: Test results
- Validation: All tests pass
```

### Content Creation Chain
```markdown
**Chain**: Blog Post Creator

**Stage 1**: Research & Ideation
- Prompt: "Research [topic] and generate 5 article angles"
- Output: List of angles with brief descriptions

**Stage 2**: Select & Outline
- Input: Angles from Stage 1
- Prompt: "Select best angle and create detailed outline"
- Output: Article outline

**Stage 3**: Draft Content
- Input: Outline from Stage 2
- Prompt: "Write full article following outline"
- Output: Article draft (markdown)

**Stage 4**: Edit & Polish
- Input: Draft from Stage 3
- Prompt: "Edit for clarity, flow, grammar, and engagement"
- Output: Polished article

**Stage 5**: Generate Metadata
- Input: Article from Stage 4
- Prompt: "Generate title variations, meta description, tags"
- Output: SEO metadata

**Stage 6**: Format for Platform
- Input: Article and metadata
- Prompt: "Format for [CMS] with proper structure"
- Output: Platform-ready post
```

## Debugging Chains

When a chain fails:

1. **Isolate the stage**: Run failed stage independently
2. **Check inputs**: Verify data passed to stage is valid
3. **Inspect output**: See what stage actually produced
4. **Review prompt**: Is it clear and achievable?
5. **Test validation**: Is validation rule appropriate?
6. **Check context**: Does stage have needed information?
7. **Review logs**: What happened during execution?

## Monitoring Chain Health

Track these metrics:

- **Success rate**: % of chains completing successfully
- **Stage failure rate**: Which stages fail most often?
- **Execution time**: How long does chain take?
- **Token usage**: Cost per chain execution
- **Retry rate**: How often do stages need retries?
- **Quality scores**: How good are final outputs?
