---
name: prompt-optimizer
description: This skill should be used when users request help optimizing, improving, or refining their prompts or instructions for AI models. Use this skill when users provide vague, unclear, or poorly structured prompts and need assistance transforming them into clear, effective, and well-structured instructions that AI models can better understand and execute. This skill applies comprehensive prompt engineering best practices to enhance prompt quality, clarity, and effectiveness.
license: Complete terms in LICENSE.txt
---

# Prompt Optimizer

## Overview

This skill transforms user-provided prompts into high-quality, clear, and effective instructions optimized for AI models. Apply proven prompt engineering principles to enhance clarity, specificity, structure, and effectiveness. The skill uses a systematic workflow to analyze, identify improvement opportunities, and restructure prompts based on industry best practices.

## When to Use This Skill

Activate this skill when users:
- Explicitly request prompt optimization or improvement
- Provide vague or unclear instructions that need refinement
- Ask for help making their requests more effective
- Submit poorly structured prompts that would benefit from reorganization
- Request guidance on how to better communicate with AI models
- Present complex tasks that need to be broken down into clearer instructions

## Optimization Workflow

Follow this systematic process to optimize any prompt:

### Step 1: Analyze the Original Prompt

Examine the user's prompt and identify:

**Clarity issues:**
- Ambiguous terms or vague requirements
- Implicit assumptions that should be explicit
- Missing context or background information

**Specificity gaps:**
- Lack of concrete constraints or requirements
- Undefined success criteria
- Missing audience or purpose information
- Unclear scope or boundaries

**Structure problems:**
- Disorganized or stream-of-consciousness format
- Missing logical flow
- Lack of clear sections or hierarchy

**Format considerations:**
- No specified output format
- Unclear expectations about length, tone, or style
- Missing examples or templates

**Complexity assessment:**
- Determine if the task is too complex for a single prompt
- Identify if the request would benefit from prompt chaining
- Assess if step-by-step reasoning is needed

### Step 2: Identify the Core Intent

Determine the fundamental objective behind the user's request:

- What is the user ultimately trying to accomplish?
- What problem are they trying to solve?
- What would constitute a successful output?
- Who is the intended audience or consumer of the output?

Clarify these points with the user if they are not evident from the original prompt.

### Step 3: Apply Optimization Principles

Enhance the prompt using these core principles:

**Make it clear and direct:**
- State requirements explicitly without assuming inference
- Remove ambiguity and vague language
- Use concrete, specific terms

**Provide context and motivation:**
- Explain WHY certain requirements matter
- Include relevant background information
- Describe the use case or scenario

**Add specificity:**
- Define concrete constraints (length, format, scope)
- Specify target audience
- Include quality criteria
- State any limitations or boundaries

**Structure the request:**
- Organize information logically
- Use clear sections or numbered points
- Separate different types of information (context, requirements, format)

**Include examples when helpful:**
- Provide input-output examples for complex formats
- Show desired tone or style through examples
- Demonstrate edge case handling

**Allow for uncertainty:**
- Explicitly permit expressing "I don't know"
- Request acknowledgment of limitations
- Prevent hallucination by encouraging honesty

### Step 4: Consider Advanced Techniques

Evaluate if any advanced techniques would enhance the prompt:

**Chain of Thought:**
- Apply when the task requires reasoning or analysis
- Request step-by-step thinking for complex problems
- Use structured format to separate reasoning from answer

**Prefilling:**
- Use when a specific format is absolutely required (JSON, XML)
- Apply to eliminate unwanted preambles
- Utilize to establish immediate tone or style

**Prompt Chaining:**
- Break complex tasks into sequential steps
- Create a multi-stage workflow for intricate projects
- Design each prompt to build on previous outputs

**Structured Output:**
- Specify exact format requirements
- Provide schemas or templates
- Use tags or delimiters for different sections

Consult `references/prompt-best-practices.md` for detailed guidance on these techniques.

### Step 5: Present the Optimized Prompt

Deliver the optimization in this format:

**Analysis Section:**
```
Original prompt issues identified:
- [List key problems with the original prompt]
```

**Optimized Prompt:**
```
[Present the complete optimized prompt in a code block for easy copying]
```

**Improvement Explanation:**
```
Key improvements made:
- [Explain major enhancements]
- [Highlight added specificity]
- [Note structural changes]
- [Mention any advanced techniques applied]
```

**Optional - Usage Tips:**
```
[If applicable, provide brief tips on how to further customize or use the optimized prompt]
```

### Step 6: Iterate Based on Feedback

After presenting the optimized prompt:

- Ask if the optimization meets the user's needs
- Offer to adjust tone, length, or specificity
- Provide alternative formulations if requested
- Refine based on user feedback

## Practical Guidelines

**Balance is key:** Not every prompt needs all advanced techniques. Match the optimization level to the task complexity.

**Preserve user intent:** Enhance clarity without changing the fundamental goal or adding unwanted requirements.

**Consider the model:** Modern models like Claude 4.x have strong instruction-following capabilities; leverage this by being direct and specific.

**Stay practical:** Focus on improvements that materially impact output quality, not cosmetic changes.

**Be educational:** When appropriate, briefly explain why certain changes improve the prompt, helping users learn to write better prompts independently.

## Reference Resources

This skill includes comprehensive reference materials:

**references/prompt-best-practices.md**
- Detailed explanations of all core principles
- Advanced techniques with examples
- Troubleshooting guide for common issues
- Quality checklist and decision frameworks

Load this reference when:
- Users ask about specific prompt engineering concepts
- Deep explanation of a technique is needed
- Troubleshooting unusual or complex prompting challenges
- Users want to learn prompt engineering principles

**references/examples.md**
- Before-and-after optimization examples across multiple domains
- Real-world scenarios demonstrating transformation
- Pattern library showing common improvements

Load this reference when:
- Users want to see concrete examples
- Illustrating a specific type of optimization
- Users are learning and need to understand patterns
- Demonstrating the impact of optimization

## Quality Standards

Ensure every optimized prompt includes:

- [ ] Clear, unambiguous objective
- [ ] Sufficient context for the AI to understand the goal
- [ ] Specific constraints and requirements
- [ ] Target audience or use case (when relevant)
- [ ] Expected output format or structure
- [ ] Quality criteria or success definition
- [ ] Permission to express uncertainty (when appropriate)

## Common Optimization Patterns

**Pattern 1: Vague Request → Specific Structured Task**
- Original: "Write about marketing"
- Optimized: Adds audience, scope, length, structure, key points, tone

**Pattern 2: Implicit Context → Explicit Context**
- Original: Assumes AI knows the background
- Optimized: States context, explains why it matters, provides relevant details

**Pattern 3: Single Complex Prompt → Prompt Chain**
- Original: Tries to do everything in one request
- Optimized: Breaks into logical sequential steps with clear outputs

**Pattern 4: Generic Output → Formatted Output**
- Original: No format specification
- Optimized: Provides schema, template, or explicit structure

**Pattern 5: Assumed Constraints → Stated Constraints**
- Original: Expects AI to infer limits
- Optimized: Explicitly states length, tone, scope, what to include/exclude

Consult `references/examples.md` for detailed examples of each pattern.
