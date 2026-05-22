---
name: openai-prompt-engineer
description: Generate and improve prompts using best practices for OpenAI GPT-5 and other LLMs. Apply advanced techniques like chain-of-thought, few-shot prompting, and progressive disclosure.
---

# OpenAI Prompt Engineer

A comprehensive skill for crafting, analyzing, and improving prompts for OpenAI's GPT-5 and other modern Large Language Models (LLMs), with focus on GPT-5-specific optimizations and universal prompting techniques.

## What This Skill Does

Helps you create and optimize prompts using cutting-edge techniques:
- **Generate new prompts** - Build effective prompts from scratch
- **Improve existing prompts** - Enhance clarity, structure, and results
- **Apply best practices** - Use proven techniques for each model
- **Optimize for specific models** - GPT-5, Claude-specific strategies
- **Implement advanced patterns** - Chain-of-thought, few-shot, structured prompting
- **Analyze prompt quality** - Identify issues and suggest improvements

## Why Prompt Engineering Matters

**Without good prompts:**
- Inconsistent or incorrect outputs
- Poor instruction following
- Wasted tokens and API costs
- Multiple attempts needed
- Unpredictable behavior

**With optimized prompts:**
- Accurate, consistent results
- Better instruction adherence
- Lower costs and latency
- First-try success
- Predictable, reliable outputs

## Supported Models & Approaches

### GPT-5 (OpenAI)
- Structured prompting (role + task + constraints)
- Reasoning effort calibration
- Agentic behavior control
- Verbosity management
- Prompt optimizer integration

### Claude (Anthropic)
- XML tag structuring
- Step-by-step thinking
- Clear, specific instructions
- Example-driven prompting
- Progressive disclosure

### Universal Techniques
- Chain-of-thought prompting
- Few-shot learning
- Zero-shot prompting
- Self-consistency
- Role-based prompting

## Core Prompting Principles

### 1. Be Clear and Specific
**Bad:** "Write about AI"
**Good:** "Write a 500-word technical article explaining transformer architecture for software engineers with 2-3 years of experience. Include code examples in Python and focus on practical implementation."

### 2. Provide Structure
Use clear formatting to organize instructions:
```
Role: You are a senior Python developer
Task: Review this code for security vulnerabilities
Constraints:
- Focus on OWASP Top 10
- Provide specific line numbers
- Suggest fixes with code examples
Output format: Markdown with severity ratings
```

### 3. Use Examples (Few-Shot)
Show the model what you want:
```
Input: "User clicked login"
Output: "USER_LOGIN_CLICKED"

Input: "Payment processed successfully"
Output: "PAYMENT_PROCESSED_SUCCESS"

Input: "Email verification failed"
Output: [Your turn]
```

### 4. Enable Reasoning
Add phrases like:
- "Think step-by-step"
- "Let's break this down"
- "First, analyze... then..."
- "Show your reasoning"

### 5. Define Output Format
Specify exactly how you want the response:
```xml
<output_format>
  <summary>One sentence overview</summary>
  <details>
    <point>Key finding 1</point>
    <point>Key finding 2</point>
  </details>
  <recommendation>Specific action to take</recommendation>
</output_format>
```

## Prompt Engineering Workflow

### 1. Define Your Goal
- What task are you solving?
- What's the ideal output?
- Who's the audience?
- What model will you use?

### 2. Choose Your Technique
- **Simple task?** → Direct instruction
- **Complex reasoning?** → Chain-of-thought
- **Pattern matching?** → Few-shot examples
- **Need consistency?** → Structured format + examples

### 3. Build Your Prompt
Use this template:
```
[ROLE/CONTEXT]
You are [specific role with relevant expertise]

[TASK]
[Clear, specific task description]

[CONSTRAINTS]
- [Limitation 1]
- [Limitation 2]

[FORMAT]
Output should be [exact format specification]

[EXAMPLES - if using few-shot]
[Example 1]
[Example 2]

[THINK STEP-BY-STEP - if complex reasoning]
Before answering, [thinking instruction]
```

### 4. Test and Iterate
- Run the prompt
- Analyze output quality
- Identify issues
- Refine and retry
- Document what works

## Advanced Techniques

### Chain-of-Thought (CoT) Prompting

**When to use:** Complex reasoning, math, multi-step problems

**How it works:** Ask the model to show intermediate steps

**Example:**
```
Problem: A store has 15 apples. They sell 60% in the morning and
half of what's left in the afternoon. How many remain?

Please solve this step-by-step:
1. Calculate morning sales
2. Calculate remaining after morning
3. Calculate afternoon sales
4. Calculate final remaining
```

**Result:** More accurate answers through explicit reasoning

### Few-Shot Prompting

**When to use:** Pattern matching, classification, style transfer

**How it works:** Provide 2-5 examples, then the actual task

**Example:**
```
Convert casual text to professional business tone:

Input: "Hey! Thanks for reaching out. Let's chat soon!"
Output: "Thank you for your message. I look forward to our conversation."

Input: "That's a great idea! I'm totally on board with this."
Output: "I appreciate your suggestion and fully support this initiative."

Input: "Sounds good, catch you later!"
Output: [Model completes]
```

### Zero-Shot Chain-of-Thought

**When to use:** Complex problems without examples

**How it works:** Simply add "Let's think step by step"

**Example:**
```
Question: What are the security implications of storing JWTs
in localStorage?

Let's think step by step:
```

**Magic phrase:** "Let's think step by step" → dramatically improves reasoning

### Structured Output with XML

**When to use:** Working with Claude or need parsed output

**Example:**
```
Analyze this code for issues. Structure your response as:

<analysis>
  <security_issues>
    <issue severity="high|medium|low">
      <description>What's wrong</description>
      <location>File and line number</location>
      <fix>How to fix it</fix>
    </issue>
  </security_issues>
  <performance_issues>
    <!-- Same structure -->
  </performance_issues>
  <best_practices>
    <suggestion>Improvement suggestion</suggestion>
  </best_practices>
</analysis>
```

### Progressive Disclosure

**When to use:** Large context, multi-step workflows

**How it works:** Break tasks into stages, only request what's needed now

**Example:**
```
Stage 1: "Analyze this codebase structure and list the main components"
[Get response]

Stage 2: "Now, for the authentication component you identified,
show me the security review"
[Get response]

Stage 3: "Based on that review, generate fixes for the high-severity issues"
```

## Model-Specific Best Practices

### GPT-5 Optimization

**Structured Prompting:**
```
ROLE: Senior TypeScript Developer
TASK: Implement user authentication service
CONSTRAINTS:
- Use JWT with refresh tokens
- TypeScript with strict mode
- Include comprehensive error handling
- Follow SOLID principles
OUTPUT: Complete TypeScript class with JSDoc comments
REASONING_EFFORT: high (for complex business logic)
```

**Control Agentic Behavior:**
```
"Implement this feature step-by-step, asking for confirmation
before each major decision"

OR

"Complete this task end-to-end without asking for guidance.
Persist until fully handled."
```

**Manage Verbosity:**
```
"Provide a concise implementation (under 100 lines) focusing
only on core functionality"
```

### Claude Optimization

**Use XML Tags:**
```
<instruction>
Review this pull request for security issues
</instruction>

<code>
[Code to review]
</code>

<focus_areas>
- SQL injection vulnerabilities
- XSS attack vectors
- Authentication bypasses
- Data exposure risks
</focus_areas>

<output_format>
For each issue found, provide:
1. Severity (Critical/High/Medium/Low)
2. Location
3. Explanation
4. Fix recommendation
</output_format>
```

**Step-by-Step Thinking:**
```
Think through this architecture decision step by step:
1. First, identify the requirements
2. Then, list possible approaches
3. Evaluate trade-offs for each
4. Make a recommendation with reasoning
```

**Clear Specificity:**
```
BAD: "Make the response professional"
GOOD: "Use formal business language, avoid contractions,
address the user as 'you', keep sentences under 20 words"
```

## Prompt Improvement Checklist

Use this checklist to improve any prompt:

- [ ] **Clear role defined** - Is the AI's expertise specified?
- [ ] **Specific task** - Is it unambiguous what to do?
- [ ] **Constraints listed** - Are limitations clear?
- [ ] **Format specified** - Is output structure defined?
- [ ] **Examples provided** - Do you show what you want (if needed)?
- [ ] **Reasoning enabled** - Do you ask for step-by-step thinking (if complex)?
- [ ] **Context included** - Does the AI have necessary background?
- [ ] **Edge cases covered** - Are exceptions handled?
- [ ] **Length specified** - Is output length clear?
- [ ] **Tone/style defined** - Is the desired voice specified?

## Common Prompt Problems & Fixes

### Problem: Vague Instructions
**Before:**
```
"Write some code for user authentication"
```

**After:**
```
"Write a TypeScript class called AuthService that:
- Accepts email/password credentials
- Validates against a User repository
- Returns a JWT token on success
- Throws AuthenticationError on failure
- Includes comprehensive JSDoc comments
- Follows dependency injection pattern"
```

### Problem: No Examples (When Needed)
**Before:**
```
"Convert these variable names to camelCase"
```

**After:**
```
"Convert these variable names to camelCase:

user_name → userName
total_count → totalCount
is_active → isActive

Now convert:
order_status →
created_at →
max_retry_count →"
```

### Problem: Missing Output Format
**Before:**
```
"Analyze this code for problems"
```

**After:**
```
"Analyze this code and output in this format:

## Security Issues
- [Issue]: [Description] (Line X)

## Performance Issues
- [Issue]: [Description] (Line X)

## Code Quality
- [Issue]: [Description] (Line X)

## Recommendations
1. [Priority 1 fix]
2. [Priority 2 fix]"
```

### Problem: Too Complex (Single Shot)
**Before:**
```
"Build a complete e-commerce backend with authentication,
payments, inventory, and shipping"
```

**After (Progressive):**
```
"Let's build this in stages:

Stage 1: Design the authentication system architecture
[Get response, review]

Stage 2: Implement the auth service
[Get response, review]

Stage 3: Add payment processing
[Continue...]"
```

## Using This Skill

### Generate a New Prompt

**Ask:**
```
"Using the prompt-engineer skill, create a prompt for:
[Describe your task and requirements]"
```

**You'll get:**
- Structured prompt template
- Recommended techniques
- Example few-shots if applicable
- Model-specific optimizations

### Improve an Existing Prompt

**Ask:**
```
"Using the prompt-engineer skill, improve this prompt:

[Your current prompt]

Goal: [What you want to achieve]
Model: [GPT-5 / Claude / Other]"
```

**You'll get:**
- Analysis of current issues
- Improved version
- Explanation of changes
- Expected improvement in results

### Analyze Prompt Quality

**Ask:**
```
"Using the prompt-engineer skill, analyze this prompt:
[Your prompt]"
```

**You'll get:**
- Quality score
- Identified weaknesses
- Specific improvement suggestions
- Best practices violations

## Real-World Examples

### Example 1: Code Review Prompt

**Task:** Get thorough, consistent code reviews

**Optimized Prompt:**
```
ROLE: Senior Software Engineer conducting PR review

REVIEW THIS CODE:
[code block]

REVIEW CRITERIA:
1. Security vulnerabilities (OWASP Top 10)
2. Performance issues
3. Code quality and readability
4. Best practices compliance
5. Test coverage gaps

OUTPUT FORMAT:
For each issue found:
- Severity: [Critical/High/Medium/Low]
- Category: [Security/Performance/Quality/Testing]
- Location: [File:Line]
- Issue: [Clear description]
- Impact: [Why this matters]
- Fix: [Specific code recommendation]

At the end, provide:
- Overall assessment (Approve/Request Changes/Comment)
- Summary of critical items that must be fixed
```

### Example 2: Technical Documentation

**Task:** Generate clear API documentation

**Optimized Prompt:**
```
ROLE: Technical writer with API documentation expertise

TASK: Generate API documentation for this endpoint

ENDPOINT DETAILS:
[code/specs]

DOCUMENTATION REQUIREMENTS:
- Target audience: Junior to mid-level developers
- Include curl and JavaScript examples
- Explain all parameters clearly
- Show example responses with descriptions
- Include common error cases
- Add troubleshooting section

FORMAT:
# [Endpoint Name]

## Overview
[One paragraph description]

## Endpoint
`[HTTP METHOD] /path`

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|

## Request Example
```bash
[curl example]
```

## Response
### Success (200)
```json
[example with inline comments]
```

### Errors
- 400: [Description and fix]
- 401: [Description and fix]

## Common Issues
[Troubleshooting guide]
```

### Example 3: Data Analysis

**Task:** Analyze data and provide insights

**Optimized Prompt:**
```
ROLE: Data analyst with expertise in business metrics

DATA:
[dataset]

ANALYSIS REQUEST:
Analyze this data step-by-step:

1. FIRST: Identify key metrics and trends
2. THEN: Calculate:
   - Growth rate (month-over-month)
   - Average values
   - Anomalies or outliers
3. NEXT: Draw business insights
4. FINALLY: Provide actionable recommendations

OUTPUT FORMAT:
## Executive Summary
[2-3 sentences]

## Key Metrics
| Metric | Value | Change | Trend |

## Insights
1. [Insight with supporting data]
2. [Insight with supporting data]

## Recommendations
1. [Action]: [Expected impact]
2. [Action]: [Expected impact]

## Methodology
[Brief explanation of analysis approach]
```

## Best Practices Summary

### DO ✅

- **Be specific** - Exact requirements, not vague requests
- **Use structure** - Organize with clear sections
- **Provide examples** - Show what you want (few-shot)
- **Request reasoning** - "Think step-by-step" for complex tasks
- **Define format** - Specify exact output structure
- **Test iteratively** - Refine based on results
- **Match to model** - Use model-specific techniques
- **Include context** - Give necessary background
- **Handle edge cases** - Specify exception handling
- **Set constraints** - Define limitations clearly

### DON'T ❌

- **Be vague** - "Write something about X"
- **Skip examples** - When patterns need to be matched
- **Assume format** - Model will choose unpredictably
- **Overload single prompt** - Break complex tasks into stages
- **Ignore model differences** - GPT-5 and Claude need different approaches
- **Give up too soon** - Iterate on prompts
- **Mix instructions** - Keep separate concerns separate
- **Forget constraints** - Specify ALL requirements
- **Use ambiguous terms** - "Good", "professional", "better" without definition
- **Skip testing** - Always validate outputs

## Quick Reference

### Prompt Template (Universal)
```
[ROLE]
You are [specific expertise]

[CONTEXT]
[Background information]

[TASK]
[Clear, specific task]

[CONSTRAINTS]
- [Limit 1]
- [Limit 2]

[FORMAT]
[Exact output structure]

[EXAMPLES - Optional]
[2-3 examples]

[REASONING - Optional]
Think through this step-by-step:
[Thinking guidance]
```

### When to Use Each Technique

| Technique | Best For | Example Use Case |
|-----------|----------|------------------|
| Chain-of-Thought | Complex reasoning | Math, logic puzzles, multi-step analysis |
| Few-Shot | Pattern matching | Classification, style transfer, formatting |
| Zero-Shot | Simple, clear tasks | Direct questions, basic transformations |
| Structured (XML) | Parsed output | Data extraction, API responses |
| Progressive Disclosure | Large tasks | Full implementations, research |
| Role-Based | Expert knowledge | Code review, architecture decisions |

### Model Selection Guide

**Use GPT-5 when:**
- Need strong reasoning
- Agentic behavior helpful
- Code generation focus
- Latest knowledge needed

**Use Claude when:**
- Very long context (100K+ tokens)
- Detailed instruction following
- Safety-critical applications
- Prefer XML structuring

## Resources

All reference materials included:
- GPT-5 specific techniques and patterns
- Claude optimization strategies
- Advanced prompting patterns
- Optimization and improvement frameworks

## Summary

Effective prompt engineering:
- **Saves time** - Get right results faster
- **Reduces costs** - Fewer API calls needed
- **Improves quality** - More accurate, consistent outputs
- **Enables complexity** - Tackle harder problems
- **Scales knowledge** - Capture best practices

Use this skill to create prompts that:
- Are clear and specific
- Use proven techniques
- Match your model
- Get consistent results
- Achieve your goals

---

**Remember:** A well-crafted prompt is worth 10 poorly-attempted ones. Invest time upfront for better results.
