---
name: create-prompt
description: Expert prompt engineering for creating effective prompts for Claude, GPT, and other LLMs. Use when writing system prompts, user prompts, few-shot examples, or optimizing existing prompts for better performance.
---

<objective>
Create highly effective prompts using proven techniques from Anthropic and OpenAI research. This skill covers all major prompting methodologies: clarity, structure, examples, reasoning, and advanced patterns.

Every prompt created should be clear, specific, and optimized for the target model.
</objective>

<quick_start>
<workflow>

1. **Clarify purpose**: What should the prompt accomplish?
2. **Identify model**: Claude, GPT, or other (techniques vary slightly)
3. **Select techniques**: Choose from core techniques based on task complexity
4. **Structure content**: Use XML tags (Claude) or markdown (GPT) for organization
5. **Add examples**: Include few-shot examples for format-sensitive outputs
6. **Define success**: Add clear success criteria
7. **Test and iterate**: Refine based on outputs
   </workflow>

<core_structure>
Every effective prompt has:

```xml
<context>
Background information the model needs
</context>

<task>
Clear, specific instruction of what to do
</task>

<requirements>
- Specific constraints
- Output format
- Edge cases to handle
</requirements>

<examples>
Input/output pairs demonstrating expected behavior
</examples>

<success_criteria>
How to know the task was completed correctly
</success_criteria>
```

</core_structure>
</quick_start>

<core_techniques>
<technique name="be_clear_and_direct">
**Priority**: Always apply first

- State exactly what you want
- Avoid ambiguous language ("try to", "maybe", "generally")
- Use "Always..." or "Never..." instead of "Should probably..."
- Provide specific output format requirements

See: [references/clarity-principles.md](references/clarity-principles.md)
</technique>

<technique name="use_xml_tags">
**When**: Claude prompts, complex structure needed

Claude was trained with XML tags. Use them for:

- Separating sections: `<context>`, `<task>`, `<output>`
- Wrapping data: `<document>`, `<schema>`, `<example>`
- Defining boundaries: Clear start/end of sections

See: [references/xml-structure.md](references/xml-structure.md)
</technique>

<technique name="few_shot_examples">
**When**: Output format matters, pattern recognition easier than rules

Provide 2-4 input/output pairs:

```xml
<examples>
<example number="1">
<input>User clicked signup button</input>
<output>track('signup_initiated', { source: 'homepage' })</output>
</example>
</examples>
```

See: [references/few-shot-patterns.md](references/few-shot-patterns.md)
</technique>

<technique name="chain_of_thought">
**When**: Complex reasoning, math, multi-step analysis

Add explicit reasoning instructions:

- "Think step by step before answering"
- "First analyze X, then consider Y, finally conclude Z"
- Use `<thinking>` tags for Claude's extended thinking

See: [references/reasoning-techniques.md](references/reasoning-techniques.md)
</technique>

<technique name="system_prompts">
**When**: Setting persistent behavior, role, constraints

System prompts set the foundation:

- Define Claude's role and expertise
- Set constraints and boundaries
- Establish output format expectations

See: [references/system-prompt-patterns.md](references/system-prompt-patterns.md)
</technique>

<technique name="prefilling">
**When**: Enforcing specific output format (Claude-specific)

Start Claude's response to guide format:

```
Assistant: {"result":
```

Forces JSON output without preamble.
</technique>

<technique name="context_management">
**When**: Long-running tasks, multi-session work, large context usage

For Claude 4.5 with context awareness:

- Inform about automatic context compaction
- Add state tracking (JSON, progress.txt, git)
- Use test-first patterns for complex implementations
- Enable autonomous task completion across context windows

See: [references/context-management.md](references/context-management.md)
</technique>
</core_techniques>

<prompt_creation_workflow>
<step_0>
**Gather requirements** using AskUserQuestion:

1. What is the prompt's purpose?
   - Generate content
   - Analyze/extract information
   - Transform data
   - Make decisions
   - Other

2. What model will use this prompt?
   - Claude (use XML tags)
   - GPT (use markdown structure)
   - Other/multiple

3. What complexity level?
   - Simple (single task, clear output)
   - Medium (multiple steps, some nuance)
   - Complex (reasoning, edge cases, validation)

4. Output format requirements?
   - Free text
   - JSON/structured data
   - Code
   - Specific template
     </step_0>

<step_1>
**Draft the prompt** using this template:

```xml
<context>
[Background the model needs to understand the task]
</context>

<objective>
[Clear statement of what to accomplish]
</objective>

<instructions>
[Step-by-step process, numbered if sequential]
</instructions>

<constraints>
[Rules, limitations, things to avoid]
</constraints>

<output_format>
[Exact structure of expected output]
</output_format>

<examples>
[2-4 input/output pairs if format matters]
</examples>

<success_criteria>
[How to verify the task was done correctly]
</success_criteria>
```

</step_1>

<step_2>
**Apply relevant techniques** based on complexity:

- **Simple**: Clear instructions + output format
- **Medium**: Add examples + constraints
- **Complex**: Add reasoning steps + edge cases + validation
  </step_2>

<step_3>
**Review checklist**:

- [ ] Is the task clearly stated?
- [ ] Are ambiguous words removed?
- [ ] Is output format specified?
- [ ] Are edge cases addressed?
- [ ] Would a person with no context understand it?
      </step_3>
      </prompt_creation_workflow>

<anti_patterns>
<pitfall name="vague_instructions">
❌ "Help with the data"
✅ "Extract email addresses from the CSV, remove duplicates, output as JSON array"
</pitfall>

<pitfall name="negative_prompting">
❌ "Don't use technical jargon"
✅ "Write in plain language suitable for a non-technical audience"
</pitfall>

<pitfall name="no_examples">
❌ Describing format in words only
✅ Showing 2-3 concrete input/output examples
</pitfall>

<pitfall name="missing_edge_cases">
❌ "Process the file"
✅ "Process the file. If empty, return []. If malformed, return error with line number."
</pitfall>

See: [references/anti-patterns.md](references/anti-patterns.md)
</anti_patterns>

<reference_guides>
**Core principles:**

- [references/clarity-principles.md](references/clarity-principles.md) - Being clear and direct
- [references/xml-structure.md](references/xml-structure.md) - Using XML tags effectively

**Techniques:**

- [references/few-shot-patterns.md](references/few-shot-patterns.md) - Example-based prompting
- [references/reasoning-techniques.md](references/reasoning-techniques.md) - Chain of thought, step-by-step
- [references/system-prompt-patterns.md](references/system-prompt-patterns.md) - System prompt templates
- [references/context-management.md](references/context-management.md) - Context windows, long-horizon reasoning, state tracking

**Best practices by vendor:**

- [references/anthropic-best-practices.md](references/anthropic-best-practices.md) - Claude-specific techniques
- [references/openai-best-practices.md](references/openai-best-practices.md) - GPT-specific techniques

**Quality:**

- [references/anti-patterns.md](references/anti-patterns.md) - Common mistakes to avoid
- [references/prompt-templates.md](references/prompt-templates.md) - Ready-to-use templates
  </reference_guides>

<success_criteria>
A well-crafted prompt has:

- Clear, unambiguous objective
- Specific output format with example
- Relevant context provided
- Edge cases addressed
- No vague language (try, maybe, generally)
- Appropriate technique selection for task complexity
- Success criteria defined
  </success_criteria>
