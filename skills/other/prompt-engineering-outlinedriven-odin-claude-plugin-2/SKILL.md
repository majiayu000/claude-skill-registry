---
name: prompt-engineering
description: Interactive prompt optimization workflow for LLMs. Use when optimizing, improving, or engineering prompts for Claude, GPT, Gemini, or other language models; covers analysis, model-specific techniques, few-shot examples, XML structuring, and validation.
---

# Interactive Prompt Optimization Workflow

Execute this workflow to systematically improve any prompt for optimal LLM performance.

## Step 1: Analyze Current State

Gather baseline information about your prompt optimization task:

- **Current prompt**: Capture the exact prompt you want to optimize
- **Target model**: Identify the specific model (Claude 4.5, Gemini 3.0, GPT 5.1, etc.)
- **Use case**: Clarify the primary purpose (coding agent, analysis, content generation, conversation)
- **Failure cases**: Document specific examples where current prompt fails or underperforms
- **Success criteria**: Define measurable outcomes (accuracy, format compliance, response time)
- **Test cases**: Create 3-5 representative examples for validation

## Step 2: Identify Model Type

Determine the correct prompting approach based on model architecture:

**Reasoning Models** (Claude 4.x, Gemini 3.0, GPT o-series, DeepSeek-R1):

- **AVOID** explicit CoT phrases like "think step-by-step" or "let's work through this"
- **PROVIDE** rich context with all relevant information upfront
- **LET** the model's internal reasoning handle the thinking process

**Non-Reasoning Models** (GPT-4o, GPT-4.1, Claude with thinking off):

- **USE** explicit CoT prompting with structured thinking tags
- **GUIDE** the reasoning process with step-by-step instructions
- **STRUCTURE** with `<thinking>` and `<answer>` tags

## Step 3: Select Core Techniques

Based on your use case, select and apply appropriate techniques:

**Essential for ALL prompts:**

- **Few-shot examples**: Add 3-5 diverse, representative examples
- **XML structure**: Use tags to separate role, context, examples, task
- **Output format**: Explicitly specify desired response format
- **Context**: Provide all necessary information and constraints

**For complex tasks:**

- **Prompt chaining**: Break into sequential subtasks with clear handoffs
- **Role assignment**: Define expert persona in system prompt
- **Long context handling**: Place lengthy data first, extract relevant quotes

**For coding agents:**

- **Parallel tool calling**: Instruct to call independent tools simultaneously
- **Hallucination prevention**: Require reading files before answering
- **Action bias**: Encourage implementation over suggestion
- **Solution persistence**: Emphasize completing tasks end-to-end

**For analysis tasks:**

- **Structured thinking**: Require step-by-step reasoning
- **Quote grounding**: Extract relevant quotes before analysis
- **Cross-referencing**: Instruct to verify across multiple sources

## Step 4: Apply Techniques Systematically

Transform your prompt using selected techniques:

**1. Add XML structure:**

```xml
<role>You are a [domain] expert specializing in [area].</role>

<context>[Relevant background information, constraints, requirements]</context>

<examples
>[3-5 diverse examples showing desired input/output patterns]</examples>

<task>[Specific user request with explicit constraints and output format]</task>
```

**2. Insert representative examples:**

- Show desired behavior through concrete examples
- Use consistent formatting across all examples
- Include edge cases if relevant
- Demonstrate proper structure and tone

**3. Apply model-specific optimization:**

- **Reasoning models**: Provide comprehensive context without prescriptive thinking instructions
- **Non-reasoning models**: Add explicit Chain of Thought prompts and thinking tags

**4. Specify constraints and format:**

- Define output structure explicitly
- List what to include and what to avoid
- Provide length guidelines if applicable
- Specify handling of edge cases

## Step 5: Test and Validate

Run empirical tests to verify improvements:

**1. Test on failure cases:**

- Run optimized prompt on all documented failure cases
- Verify each now produces acceptable output

**2. Test edge cases:**

- Boundary conditions (empty input, maximum length, etc.)
- Unusual but valid inputs
- Ambiguous scenarios

**3. Compare metrics:**

- Accuracy improvement (before vs after)
- Format compliance rate
- Response consistency across runs
- Execution time (if relevant)

**4. Iterate on gaps:**

- If issues persist: Rephrase instructions for clarity
- If format violations: Make format requirements more explicit
- If inconsistent: Add more examples showing desired behavior
- If slow: Simplify prompt or adjust model parameters

**Handle fallback responses:**

- If model refuses or gives generic responses:
  - Increase temperature parameter
  - Rephrase request to avoid trigger words
  - Check for safety filter activation
  - Try different framing of the same task

## Step 6: Deliver Optimized Prompt

Package your work for deployment or handoff:

**1. Final prompt template:**

- Complete, production-ready prompt text
- Clearly marked sections (role, context, examples, task)
- Proper formatting and structure

**2. Technique annotations:**

- Document which techniques were applied and why
- Note model-specific considerations
- Highlight critical sections

**3. Model-specific callouts:**

- Parameter recommendations (temperature, max_tokens, etc.)
- Model family compatibility notes
- Performance characteristics

**4. Before/after metrics:**

- Quantitative improvement measurements
- Specific failure cases resolved
- Remaining limitations or edge cases

**5. Usage guidelines:**

- When to use this prompt
- How to adapt for variations
- Common pitfalls to avoid

**6. Known edge cases:**

- Scenarios where prompt may still struggle
- Recommended fallback approaches
- Future improvement opportunities
