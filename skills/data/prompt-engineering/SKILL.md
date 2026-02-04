---
name: prompt-engineering
description: Use when creating prompts for Claude or other LLMs, need help structuring prompts effectively, want to improve prompt quality, or need templates for simple or complex prompting tasks. Provides Anthropic's official 10-component framework, best practices for Claude 4.x models, and ready-to-use templates.
---

# Prompt Engineering for Claude

Expert guidance for creating effective prompts using Anthropic's official best practices and the 10-component framework.

## When to Use This Skill

Use this skill when you need to:
- Create a new prompt for Claude or other LLMs
- Improve an existing prompt's effectiveness
- Structure complex multi-step prompting tasks
- Learn prompt engineering best practices
- Get templates for quick or comprehensive prompts

## Anthropic's 10-Component Framework

This is the official structure for professional prompts:

1. **Task Context (WHO & WHAT)** - Define Claude's role and overall task
2. **Tone Context (HOW)** - Specify desired communication style
3. **Background Data** - Provide all relevant context and documents
4. **Detailed Task Description** - Be explicit about requirements and rules
5. **Examples (Multishot)** - Show 1-3 examples of desired output
6. **Conversation History** - Include relevant prior context
7. **Immediate Task** - State the specific deliverable needed NOW
8. **Thinking Step-by-Step** - Encourage deliberate reasoning (Chain of Thought)
9. **Output Formatting** - Define structure explicitly
10. **Prefilled Response** - Start Claude's response to guide style

## Core Best Practices for Claude 4.x

### Be Explicit
**Less Effective**: "Create a dashboard"
**More Effective**: "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."

### Add Context (Explain WHY)
**Less Effective**: "NEVER use ellipses"
**More Effective**: "Your response will be read aloud by text-to-speech, so never use ellipses since TTS engines cannot pronounce them."

### Use Examples
Show concrete examples of what you want rather than just describing it.

### Encourage Reasoning
Add: "Think through this step-by-step before responding" or "Show your reasoning in <thinking> tags"

### Structure with XML Tags
Use tags like `<background>`, `<task>`, `<rules>`, `<examples>`, `<format>` to organize complex prompts.

## Quick Templates

### Minimal Template (Simple Tasks)

```xml
<system_prompt>
[Define role/identity - 1-2 sentences]
</system_prompt>

<task>
[What needs to be done? Be specific.]
</task>

<rules>
- [Key requirement or constraint]
- [Another rule or boundary]
</rules>

[Provide any additional context, background, or data needed]

<format>
[How should the output be structured?]
</format>
```

### Comprehensive Template (Complex Tasks)

```xml
<system_prompt>
You are a [ROLE with specific expertise and background].
[Add relevant experience, specialization, or perspective]
</system_prompt>

<tone>
[Communication style: professional/casual/technical/accessible]
[Formality level: formal/conversational/colloquial]
</tone>

<background>
[All relevant context, prior conversations, domain knowledge, data, documents]

Key Context:
- [Context point 1]
- [Context point 2]
- [Context point 3]
</background>

<task>
<objective>
[Clear, specific statement of what needs to be accomplished]
</objective>

<constraints>
- [Specific requirement 1]
- [Specific requirement 2]
- [Limitation or boundary 1]
</constraints>

<success_criteria>
[How will we know the response is successful?]
- [Criterion 1]
- [Criterion 2]
</success_criteria>
</task>

<rules>
**MUST:**
- [Required action or behavior 1]
- [Required action or behavior 2]

**MUST NOT:**
- [Prohibited action or pattern 1]
- [Prohibited action or pattern 2]

**CONSIDER:**
- [Nice-to-have or contextual guidance]
</rules>

<examples>
<good_example>
[Concrete example of desired output]
</good_example>

<bad_example>
[Example of what to avoid]
</bad_example>
</examples>

<thinking>
Before responding, carefully consider:
1. [Key question or analysis step]
2. [Another critical consideration]
3. [Final validation step]

Show your reasoning in thinking tags if it helps with complex analysis.
</thinking>

<format>
[Detailed specification of how output should be structured]

Structure:
1. [Section 1 with description]
2. [Section 2 with description]
3. [Section 3 with description]

Style:
- [Writing style requirement]
- [Formatting requirement]
- [Tone requirement]
</format>

[ANY ADDITIONAL DATA OR CONTEXT]
```

## Advanced Techniques

### Chain of Thought
Add explicit reasoning prompts:
- "Think through this step-by-step"
- "Before answering, consider..."
- "Show your reasoning in <thinking> tags"

### Extended Thinking
For complex problems: "Take your time to reason through this carefully"

### Multishot Prompting
Provide 2-3 concrete examples showing input → desired output

### Role Prompting
Define expertise: "You are a senior software architect with 15 years experience in distributed systems"

### Long-Horizon Tasks
For tasks spanning multiple sessions:
```xml
<multi_window_guidance>
Your context window will be automatically compacted as it approaches its limit.
Do not stop tasks early due to token budget concerns.
Save your current progress to memory as you approach your token budget limit.
Always be persistent and complete tasks fully.
</multi_window_guidance>
```

## When to Use Which Template

**Use Minimal Template when:**
- Straightforward request
- Context is already clear
- You want quick results
- Task is well-defined

**Use Comprehensive Template when:**
- Task is complex or multi-step
- Deep analysis or reasoning needed
- Context requires extensive background
- Output quality is critical
- Production or team use
- Building prompts for reuse

## Pro Tips

1. **Include real data** - Concrete metrics beat generic examples
2. **Show, don't tell** - Examples are more powerful than descriptions
3. **Explain WHY** - Context on requirements improves reasoning
4. **Define success** - Explicit criteria improve output quality
5. **Use thinking** - Explicitly encourage reasoning for complex tasks
6. **Iterate** - First attempt often isn't perfect; refine the prompt
7. **Be specific about format** - Tell Claude exactly how you want the answer structured

## Common Mistakes to Avoid

- Being too vague or generic
- Not providing examples
- Forgetting to specify output format
- Not explaining WHY requirements matter
- Omitting relevant context
- Not using structured tags for complex prompts
- Forgetting to encourage reasoning for complex tasks

## Quick Reference

**System Prompts** (via API): Define Claude's role/identity only
**User Prompts** (via API): Provide task, context, data, instructions

**XML Tags for Structure:**
- `<background>` - Context and data
- `<task>` - What needs to be done
- `<rules>` - Requirements and constraints
- `<examples>` - Show desired output
- `<thinking>` - Encourage reasoning
- `<format>` - Define output structure

**Model Selection:**
- **Opus 4** - Most powerful, complex reasoning, high-stakes tasks
- **Sonnet 4.5** - Balanced, great for coding and everyday use
- **Haiku 4.5** - Fastest, simple tasks and high-volume operations

## Source

This skill is based on the comprehensive Claude Prompt Engineering Guide downloaded from: https://github.com/ThamJiaHe/claude-prompt-engineering-guide

Full templates and examples available at: `~/claude-prompt-engineering-guide/`
