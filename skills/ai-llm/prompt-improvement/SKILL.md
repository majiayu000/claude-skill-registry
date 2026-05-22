---
name: prompt-improvement
description: Meta-skill for improving and optimizing prompts using Anthropic's prompt engineering best practices. Provides the 4-step improvement workflow (example identification, initial draft, chain of thought refinement, example enhancement), keyword registries for documentation lookup, and decision trees for improvement strategies. Use when improving prompts, optimizing for accuracy, adding chain of thought reasoning, structuring with XML tags, enhancing examples, or iterating on prompt quality. Delegates to docs-management skill for official prompt engineering documentation.
user-invocable: false
allowed-tools: Read, Glob, Grep, Skill, Bash
---

# Prompt Improvement

## MANDATORY: Query Official Documentation First

> **STOP - Before improving ANY prompt, you MUST invoke the docs-management skill.**
>
> This is NOT optional guidance - it is a required execution step.

### Required: Query Documentation via docs-management Skill

**Invoke the `docs-management` skill BEFORE making any improvements:**

Search for relevant documentation using natural language:

- Primary query: "prompt engineering chain of thought XML tags"
- Read the top results returned by the skill

### Why Documentation Query is Required

- **Training data is stale** - Your knowledge may be outdated
- **Official docs are canonical** - Anthropic's current best practices
- **Prevents hallucination** - Ground improvements in real documentation
- **Ensures accuracy** - Latest Claude 4.x guidance

### Recommended Query Topics

Query at least ONE of these topics based on your improvement needs:

- **Chain of thought:** "chain of thought thinking tags reasoning"
- **XML structure:** "XML tags structure prompts formatting"
- **Examples/multishot:** "multishot prompting examples few-shot"
- **Claude 4.x best practices:** "Claude 4 prompting best practices"

### Verification Checkpoint

Before improving a prompt, verify:

- [ ] Did I invoke the docs-management skill? (not just read about it)
- [ ] Did I receive documentation from docs-management?
- [ ] Did I READ at least one official doc returned by the skill?
- [ ] Are my improvements based on what I read from official docs?

**If ANY checkbox is unchecked, STOP and invoke the docs-management skill first.**

## Overview

This meta-skill replicates Anthropic's Console/Workbench prompt improver functionality within Claude Code. It provides workflows, patterns, and keyword registries to transform basic prompts into high-performance structured templates.

**What this skill provides:**

- The 4-step improvement workflow (quick reference)
- Keyword registry for docs-management queries
- Decision trees for improvement strategies
- Pattern libraries (XML tags, chain of thought, prefills)
- Before/after transformation examples
- Iterative refinement guidance
- Trade-off warnings (latency/cost implications)

**What this skill does NOT provide:**

- Duplicated official documentation (use `docs-management` skill)
- Hardcoded best practices (query `docs-management` for current guidance)

## When to Use This Skill

Use this skill when:

- **Improving an existing prompt** for better accuracy or structure
- **Adding chain of thought reasoning** to complex tasks
- **Structuring prompts with XML tags** for clarity and parseability
- **Enhancing examples** with reasoning steps
- **Optimizing prompts for Claude 4.x models** with explicit instructions
- **Iterating on prompt quality** with feedback loops
- **Generating test cases** when examples are lacking

## Quick Decision Tree

**What do you want to do?**

1. **Improve a prompt from scratch** -> See [The 4-Step Improvement Workflow](#the-4-step-improvement-workflow)
2. **Add XML structure** -> Query docs-management: "Find documentation about XML tags for structuring prompts"
3. **Add chain of thought** -> Query docs-management: "Find documentation about chain of thought prompting"
4. **Add/improve examples** -> See [references/patterns/example-enrichment-patterns.md](references/patterns/example-enrichment-patterns.md)
5. **Iterate with feedback** -> See [references/workflows/iterative-refinement.md](references/workflows/iterative-refinement.md)
6. **Generate test cases** -> See [references/workflows/test-case-generation.md](references/workflows/test-case-generation.md)
7. **Understand trade-offs** -> See [references/troubleshooting/tradeoffs-guide.md](references/troubleshooting/tradeoffs-guide.md)

## The 4-Step Improvement Workflow

The prompt improver enhances prompts through a structured 4-step process:

### Step 1: Example Identification

- Locate and extract any existing examples from the prompt
- Note the format and structure of current examples
- Identify if examples are missing (if so, consider generating them)

### Step 2: Initial Draft

- Create a structured template with clear sections
- Add XML tags to separate components:
  - `<instructions>` - Task definition and behavioral guidelines
  - `<context>` - Background information and relevant details
  - `<examples>` - Demonstration cases
  - `<formatting>` - Desired output format specification
- Query docs-management: "Find documentation about XML tags for structuring prompts"

### Step 3: Chain of Thought Refinement

- Add step-by-step reasoning instructions
- Include thinking tags: `<thinking>`, `<analysis>`, `<answer>`
- Guide Claude through the problem-solving process
- Query docs-management: "Find documentation about chain of thought prompting"

### Step 4: Example Enhancement

- Update examples to demonstrate the new reasoning process
- Add `<thinking>` steps within examples showing intermediate reasoning
- Ensure examples match the output format specification
- This teaches Claude HOW to reason, not just WHAT to output

**Detailed workflow:** [references/workflows/improvement-workflow.md](references/workflows/improvement-workflow.md)

## What You Get After Improvement

An improved prompt typically includes:

- **Detailed chain-of-thought instructions** guiding Claude's reasoning
- **Clear XML tag organization** separating components
- **Standardized example formatting** with step-by-step reasoning
- **Strategic prefills** guiding initial responses

### Typical Improved Prompt Structure

```xml
<instructions>
Your task definition and behavioral guidelines
</instructions>

<context>
Background information and relevant details
</context>

<examples>
  <example>
    <input>Sample input</input>
    <thinking>Step-by-step reasoning</thinking>
    <output>Expected output</output>
  </example>
</examples>

<formatting>
Specify desired output format and structure
</formatting>
```

## Keyword Registry for docs-management

Use these keywords to query the `docs-management` skill for official documentation:

### Core Techniques

| Topic | Query Keywords |
| --- | --- |
| Prompt Improver | prompt improver, prompt improvement, optimize prompts |
| Chain of Thought | chain of thought, CoT, thinking, step-by-step, reasoning |
| XML Tags | XML tags, structure prompts, tagging, XML structure |
| Examples | multishot, few-shot, example formatting, multishot prompting |
| System Prompts | system prompt, role, persona, Claude role |
| Clarity | clear, direct, explicit, specific instructions, be clear and direct |
| Claude 4.x | Claude 4, Claude 4.5, Sonnet 4.5, Opus 4.5, best practices |

### Advanced Topics

| Topic | Query Keywords |
| --- | --- |
| Prefilling | prefill, response prefill, assistant prefill, output format |
| Long Context | long context, long context tips, document placement |
| Extended Thinking | extended thinking, thinking budget, deep reasoning |
| Prompt Chaining | chain prompts, prompt chaining, multi-step prompts |

### Example Queries

```text
Find documentation about chain of thought prompting and thinking tags
```

```text
Find documentation about XML tags for structuring prompts
```

```text
Find documentation about multishot prompting and example formatting
```

```text
Find documentation about Claude 4 and Claude 4.5 prompting best practices
```

```text
Find documentation about prefilling Claude's response for output control
```

## Performance Expectations

> **Empirical Guidance:** The metrics below are illustrative examples from Anthropic's testing
> at time of publication. Actual results vary by task, domain, and model version.
> These are NOT guarantees - use them as rough benchmarks for improvement potential.

Based on Anthropic's testing, prompt improvement typically yields:

- **30% accuracy increase** on multi-label classification tasks
- **100% word count adherence** on summarization tasks
- **~40% reduction** in prompt iteration cycles

**Important:** Improved prompts produce longer, more thorough responses. Consider trade-offs for latency-sensitive or cost-sensitive applications.

## References Guide

**Load these files based on your specific needs:**

### Workflows

- [Improvement Workflow](references/workflows/improvement-workflow.md) - Detailed 4-step process with quality checks
- [Iterative Refinement](references/workflows/iterative-refinement.md) - Multi-pass improvement with feedback
- [Test Case Generation](references/workflows/test-case-generation.md) - Creating examples when none exist

### Examples

- [Basic Transformations](references/examples/basic-transformations.md) - Simple before/after examples
- [Advanced Transformations](references/examples/advanced-transformations.md) - Complex multi-component prompts
- [Domain-Specific](references/examples/domain-specific.md) - Code, analysis, creative, support domains

### Patterns

- [XML Tagging Patterns](references/patterns/xml-tagging-patterns.md) - Complete tag library with usage
- [Chain of Thought Patterns](references/patterns/cot-patterns.md) - Basic, guided, structured CoT
- [Prefill Patterns](references/patterns/prefill-patterns.md) - Strategic response prefilling
- [System Prompt Patterns](references/patterns/system-prompt-patterns.md) - Role/persona assignment
- [Example Enrichment Patterns](references/patterns/example-enrichment-patterns.md) - Enhancing examples with reasoning

### Troubleshooting

- [Common Issues](references/troubleshooting/common-issues.md) - Problems and fixes
- [Debugging Guide](references/troubleshooting/debugging-guide.md) - Systematic debugging
- [Trade-offs Guide](references/troubleshooting/tradeoffs-guide.md) - When NOT to use improvement

### Metadata

- [Keyword Registry](references/metadata/keyword-registry.md) - Complete keyword-to-topic mappings
- [Tag Reference](references/metadata/tag-reference.md) - Complete XML tag reference

## Related Components

### Companion Agent

- **prompt-improver** - Subagent that executes the 4-step improvement workflow
  - Auto-loads this skill for keyword registries and workflow guidance
  - Use when you need automated prompt improvement execution
  - Invoked by the `/improve-prompt` command

### Slash Command

- **/improve-prompt** - User-facing command for prompt improvement
  - Input modes: direct text, file path, context, iterate
  - Supports `--feedback` for iterative refinement
  - Supports `--generate-examples` for prompts lacking examples

### Related Skills

- **docs-management** - Official documentation access (all documentation queries delegate here)
- **current-date** - Get current UTC date for version history
- **skill-development** - Creating and validating skills

## Version History

- v1.0.0 (2025-12-03): Initial release - Meta-skill for prompt improvement with 4-step workflow, delegation to docs-management, comprehensive pattern library

---

## Last Updated

**Date:** 2025-12-03
**Model:** claude-opus-4-5-20251101
