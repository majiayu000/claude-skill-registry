---
name: improve-prompt
description: >
  Prompt engineering architect that transforms raw prompts into optimized,
  production-ready prompts. PROACTIVELY activate for: (1) Improve/refine prompts,
  (2) Optimize prompts for specific models, (3) Create prompt chains/sequences,
  (4) Analyze prompt quality, (5) Transform prompts for different contexts.
  
  Triggers: "improve this prompt", "refine prompt", "optimize prompt",
  "make this prompt better", "prompt engineering", "fix my prompt"
---

# Improve Prompt

Transform prompts into optimized, production-ready versions.

## Purpose

Analyze and enhance prompts by:
- Identifying weaknesses and ambiguities
- Applying prompt engineering best practices
- Optimizing for specific models (Claude, Gemini, GPT)
- Structuring for consistent outputs
- Adding appropriate constraints and examples

## When to Use

**Ideal for:**
- Prompts that get inconsistent results
- Prompts that need to work across models
- Complex prompts requiring structure
- Prompts for production use

**Avoid when:**
- Simple, one-off questions
- Conversational queries

## Workflow

### Step 1: Analyze Current Prompt

Evaluate the prompt for:
- **Clarity:** Is the task unambiguous?
- **Completeness:** Is all necessary context provided?
- **Structure:** Is it well-organized?
- **Constraints:** Are boundaries defined?
- **Examples:** Are examples provided if needed?
- **Output format:** Is expected output specified?

### Step 2: Identify Improvements

Common issues to address:
- Vague instructions → Make specific
- Missing context → Add relevant background
- No output format → Specify structure
- No examples → Add few-shot examples
- No constraints → Add guardrails
- Too long → Consolidate and prioritize

### Step 3: Apply Best Practices

**For Claude:**
- Use XML tags for structure
- Leverage extended thinking for complex tasks
- Request step-by-step reasoning
- Use positive framing ("do X" not "don't do Y")

**For all models:**
- Put important instructions at start and end
- Use numbered steps for sequences
- Provide concrete examples
- Specify output format explicitly
- Include edge case handling

### Step 4: Generate Improved Prompt

Output the optimized prompt with:
- Clear structure
- Explicit instructions
- Defined output format
- Examples if beneficial

## Output Format
```markdown
## Prompt Analysis

**Original prompt issues:**
1. [Issue 1]
2. [Issue 2]

**Improvements applied:**
1. [Improvement 1]
2. [Improvement 2]

---

## Improved Prompt

[The optimized prompt, ready to copy]

---

## Usage Notes

- **Best for:** [model/use case]
- **Expected output:** [description]
- **Variations:** [any suggested variations]
```

## Quality Gates

- [ ] All ambiguities resolved
- [ ] Output format specified
- [ ] Appropriate length (not bloated)
- [ ] Tested mentally for edge cases
- [ ] Model-appropriate techniques used

## Examples

**Example: Vague prompt improvement**

*Before:*
Summarize this document

*After:*
Summarize the following document in 3-5 bullet points.
Focus on:

Key findings or conclusions
Important data points
Recommended actions

Format each bullet as: [Topic]: [1-2 sentence summary]
<document>
[Document content here]
</document>
````
