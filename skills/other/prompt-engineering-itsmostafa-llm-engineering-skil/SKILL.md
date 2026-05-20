---
name: prompt-engineering
description: Crafting effective prompts for LLMs. Use when designing prompts, improving output quality, structuring complex instructions, or debugging poor model responses.
---

# Prompt Engineering

Prompt engineering is the practice of designing inputs that guide LLMs to produce desired outputs. Effective prompts reduce errors, improve consistency, and unlock model capabilities.

## Table of Contents

- [Core Principles](#core-principles)
- [Be Clear and Direct](#be-clear-and-direct)
- [Use Examples (Multishot)](#use-examples-multishot)
- [Chain of Thought](#chain-of-thought)
- [XML Tags](#xml-tags)
- [Role Prompting](#role-prompting)
- [Long Context](#long-context)
- [Output Control](#output-control)
- [Self-Verification](#self-verification)
- [Best Practices](#best-practices)
- [References](#references)

## Core Principles

**Golden rule**: Show your prompt to a colleague with minimal context. If they're confused, the model will be too.

1. **Be explicit** - State exactly what you want; never assume the model knows your preferences
2. **Provide context** - Include what the output is for, who the audience is, and what success looks like
3. **Use structure** - Sequential steps, XML tags, and clear formatting reduce ambiguity
4. **Show examples** - Demonstrations outperform descriptions for complex formats

## Be Clear and Direct

Treat the model as a capable but context-free collaborator. Specify:
- What the task results will be used for
- What audience the output is meant for
- What a successful completion looks like

### Vague vs Specific

```
# Vague
Analyze this data and give insights.

# Specific
Analyze this Q2 sales data for our board presentation.
1. Identify the top 3 revenue trends
2. Flag any anomalies exceeding 15% variance
3. Recommend 2-3 actionable next steps
Format as bullet points, max 200 words.
```

### Sequential Steps

Use numbered lists for multi-step tasks:

```
Your task is to anonymize customer feedback.

Instructions:
1. Replace customer names with "CUSTOMER_[ID]"
2. Replace emails with "EMAIL_[ID]@example.com"
3. Redact phone numbers as "PHONE_[ID]"
4. Leave product names intact
5. Output only processed messages, separated by "---"
```

## Use Examples (Multishot)

Provide 3-5 diverse examples to demonstrate expected behavior. Examples reduce misinterpretation and enforce consistent formatting.

### Structure

```
Categorize customer feedback by issue type and sentiment.

<examples>
<example>
Input: The dashboard loads slowly and the export button is hidden.
Category: UI/UX, Performance
Sentiment: Negative
Priority: High
</example>

<example>
Input: Love the Salesforce integration! Would be great to add Hubspot.
Category: Integration, Feature Request
Sentiment: Positive
Priority: Medium
</example>
</examples>

Now categorize: {{FEEDBACK}}
```

### Tips

- Make examples **relevant** to actual use cases
- Include **edge cases** and potential challenges
- Vary examples to prevent unintended pattern matching
- Wrap in `<example>` tags for clarity

## Chain of Thought

Encourage step-by-step reasoning for complex tasks. This improves accuracy in math, logic, analysis, and multi-factor decisions.

### Basic

```
Determine the best investment option for this client. Think step-by-step.
```

### Guided

Specify what steps to consider:

```
Think before answering:
1. Consider the client's risk tolerance given their 5-year timeline
2. Calculate potential returns for each option
3. Factor in market volatility history
4. Then provide your recommendation
```

### Structured (Recommended)

Separate reasoning from output with tags:

```
Analyze this contract for legal risks.

In <thinking> tags, work through:
- Indemnification implications
- Liability exposure
- IP ownership concerns

Then provide your recommendation in <answer> tags.
```

This makes reasoning visible for debugging and the answer extractable for post-processing.

## XML Tags

Use XML tags to separate prompt components. This prevents instruction/content confusion and improves parseability.

### Common Tags

```
<instructions>Task steps and requirements</instructions>
<context>Background information</context>
<document>Source material to process</document>
<example>Demonstration of expected behavior</example>
<constraints>Boundaries and limitations</constraints>
<output_format>Expected response structure</output_format>
```

### Nested Structure

```
<documents>
  <document index="1">
    <source>annual_report_2023.pdf</source>
    <content>{{REPORT_CONTENT}}</content>
  </document>
  <document index="2">
    <source>competitor_analysis.xlsx</source>
    <content>{{ANALYSIS_CONTENT}}</content>
  </document>
</documents>

<instructions>
Compare revenue trends across both documents.
Identify strategic advantages mentioned in the annual report.
</instructions>
```

### Reference Tags in Instructions

Be explicit when referring to tagged content:

```
Using the contract in <contract> tags, identify all clauses
related to termination.
```

## Role Prompting

Set expertise context via system prompts to improve domain-specific performance.

### System Prompt Pattern

```python
system = "You are a senior securities lawyer at a Fortune 500 company."
user = "Review this acquisition agreement for regulatory risks."
```

### Effective Roles

```
# General
You are a [role] at [organization type].

# Specific (better)
You are the General Counsel of a Fortune 500 tech company
specializing in M&A transactions.

# With behavioral guidance (best)
You are a senior data scientist. You prioritize statistical
rigor over speed. When uncertain, you state assumptions
explicitly and suggest validation approaches.
```

### When to Use

- Complex analysis requiring domain expertise
- Tasks where tone/style matters (legal, medical, executive)
- When a specific perspective would improve output quality

## Long Context

For prompts with large documents (20K+ tokens):

### Document Placement

Place long documents **at the top**, before instructions:

```
<documents>
{{LARGE_DOCUMENT_CONTENT}}
</documents>

<instructions>
Summarize the key findings from the document above.
Focus on financial implications.
</instructions>
```

### Quote Grounding

Ask the model to cite sources before analyzing:

```
<documents>
{{PATIENT_RECORDS}}
</documents>

First, find and quote the relevant sections in <quotes> tags.
Then provide your diagnosis in <analysis> tags, referencing
the quoted evidence.
```

### Multi-Document Metadata

Include source information for attribution:

```
<documents>
  <document index="1">
    <source>quarterly_report_q2.pdf</source>
    <date>2024-07-15</date>
    <content>{{CONTENT}}</content>
  </document>
</documents>
```

## Output Control

### Verbosity Specification

```
<output_format>
- Default responses: 3-6 sentences or ≤5 bullets
- Simple factual questions: ≤2 sentences
- Complex analysis: 1 overview paragraph + ≤5 tagged bullets
</output_format>
```

### Format Constraints

```
Output requirements:
- Use markdown tables for comparisons
- Code blocks for any technical content
- No introductory phrases ("Here's...", "Sure...")
- End with exactly 3 action items
```

### Scope Boundaries

Prevent drift from original intent:

```
Implement EXACTLY and ONLY what is requested.
- Do not add features beyond the specification
- Do not refactor surrounding code
- Choose the simplest valid interpretation
- Ask for clarification rather than assuming
```

## Self-Verification

For high-stakes outputs, include verification steps:

```
<verification>
Before finalizing your response:
1. Re-read the original request
2. Check that all requirements are addressed
3. Verify any specific claims against provided documents
4. Soften language where certainty is low
5. Flag any assumptions you made
</verification>
```

### Uncertainty Acknowledgment

```
When uncertain:
- Explicitly state "Based on the provided context..."
- Offer 2-3 plausible interpretations if ambiguous
- Never fabricate specific details (dates, numbers, quotes)
- Say "I don't have enough information to..." when applicable
```

## Best Practices

1. **Start specific, then generalize** - Begin with detailed prompts; relax constraints only after validating output quality
2. **Test with edge cases** - Include unusual inputs in your evaluation to catch failure modes
3. **Iterate on examples** - When outputs miss the mark, add an example demonstrating the correct behavior
4. **Separate instructions from content** - Use XML tags to prevent the model from confusing your instructions with input data
5. **Put documents before queries** - For long context, place source material at the top of the prompt
6. **Make reasoning visible** - Use `<thinking>` tags to debug why the model produces certain outputs
7. **Constrain output format explicitly** - Specify structure, length, and style to reduce post-processing
8. **Version your prompts** - Track changes to understand what modifications improved or degraded performance
9. **Use system prompts for role, user prompts for task** - Keep role context stable; vary task instructions
10. **Validate with fresh eyes** - Have someone unfamiliar with the task review your prompt for clarity

## References

- [Claude Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [GPT-5 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide)
- [Anthropic Prompt Library](https://docs.anthropic.com/en/prompt-library)
