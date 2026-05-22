---
name: anthropic-prompt-engineer
description: Master Anthropic's prompt engineering techniques to generate new prompts or improve existing ones using best practices for Claude AI models.
---

# Anthropic Prompt Engineer

Master the art and science of prompt engineering with Anthropic's proven techniques. Generate new prompts from scratch or improve existing ones using best practices for Claude AI models (Claude 4.x, Sonnet, Opus, Haiku).

## What This Skill Does

Helps you create and optimize prompts for Claude AI using Anthropic's official techniques:
- **Generate new prompts** - Build effective prompts from requirements
- **Improve existing prompts** - Optimize prompts for better results
- **Apply best practices** - Use proven techniques from Anthropic
- **Avoid common mistakes** - Prevent hallucinations and unclear outputs
- **Optimize for Claude 4.x** - Leverage latest model capabilities
- **Structure complex prompts** - Build multi-step, production-ready prompts

## Why Prompt Engineering Matters

**Without proper prompting:**
- Inconsistent or incorrect outputs
- Hallucinations and made-up information
- Unclear or verbose responses
- Wasted tokens and API calls
- Poor performance on complex tasks
- Difficulty reproducing results

**With engineered prompts:**
- Precise, reliable outputs
- Factual, grounded responses
- Clear, formatted results
- Efficient token usage
- Excellent complex task performance
- Reproducible, production-ready results

## Quick Start

### Generate a New Prompt

```
Using the anthropic-prompt-engineer skill, create a prompt that:
- Extracts structured data from customer emails
- Returns JSON format
- Handles missing information gracefully
- Includes 2 examples
```

### Improve an Existing Prompt

```
Using the anthropic-prompt-engineer skill, improve this prompt:

"Analyze this code and tell me if there are bugs"

Make it more effective using Anthropic's best practices.
```

## Core Techniques Summary

### 1. Be Clear and Direct
Provide explicit, unambiguous instructions. Claude 4.x excels with precise direction.

### 2. Use XML Tags for Structure
Organize prompts with semantic tags like `<instructions>`, `<example>`, `<context>`.

### 3. Chain of Thought (CoT)
Ask Claude to think step-by-step for complex reasoning.

### 4. Prefilling
Start Claude's response to guide format and style.

### 5. Few-Shot Examples
Provide 2-5 diverse examples showing the pattern you want.

### 6. Role Assignment
Give Claude a specific role or persona for appropriate context.

## Reference Materials

All techniques, examples, and templates are available in the `references/` directory:

- **core_techniques.md** - Essential techniques with examples
- **advanced_techniques.md** - Advanced methods and optimization
- **common_mistakes.md** - Pitfalls to avoid
- **claude_4_best_practices.md** - Claude 4.x specific guidance
- **prompt_templates.md** - Ready-to-use templates

## Usage Examples

### Example 1: Generate a Data Extraction Prompt

Create a prompt that extracts names, emails, and phone numbers from business cards.

### Example 2: Improve a Vague Prompt

Transform "Write about machine learning" into a structured, effective prompt.

### Example 3: Debug a Failing Prompt

Fix inconsistent outputs by adding structure, examples, and format specification.

## Best Practices Checklist

- [ ] Instructions are clear and specific
- [ ] Output format is explicitly defined
- [ ] Examples align with desired behavior
- [ ] XML tags separate different sections
- [ ] Context is minimal but sufficient
- [ ] Edge cases are addressed
- [ ] Tested on diverse inputs
- [ ] Token usage is optimized

## Key Principles

1. **Empirical Approach** - Test, measure, iterate
2. **Context as Resource** - Every token counts
3. **Clarity Over Cleverness** - Explicit instructions work best
4. **Examples Teach Best** - Show, don't just tell
5. **Structure Helps** - Organization reduces confusion
6. **Iteration Improves** - Refine based on results

## Summary

Master prompt engineering to create:
- Reliable and consistent outputs
- Production-ready prompts
- Token-efficient solutions
- Easy to maintain systems

Apply Anthropic's proven techniques for best results.

---

**Remember:** Good prompts are engineered, not guessed.
