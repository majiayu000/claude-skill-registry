---
name: prompt-enhancer
description: "Prompt engineering and optimization for AI/LLMs. Capabilities: transform unclear prompts, reduce token usage, improve structure, add constraints, optimize for specific models, backward-compatible rewrites. Actions: improve, enhance, optimize, refactor, compress prompts. Keywords: prompt engineering, prompt optimization, token efficiency, LLM prompt, AI prompt, clarity, structure, system prompt, user prompt, few-shot, chain-of-thought, instruction tuning, prompt compression, token reduction, prompt rewrite, semantic preservation. Use when: improving unclear prompts, reducing token consumption, optimizing LLM outputs, restructuring verbose requests, creating system prompts, enhancing prompt clarity."
---

# Prompt Enhancer Skill

## Purpose

Transform user prompts into enhanced, production-ready versions that are concise, clean, and optimally structured for AI agents and sub-agents. Includes optimization techniques for reducing LLM output token usage while maintaining semantic accuracy and backward compatibility.

## When to Use This Skill

Use this skill when:
- User explicitly asks to improve, enhance, or optimize a prompt
- User sends an unclear, verbose, or poorly structured prompt
- User mentions they want better results from AI interactions
- User asks for help writing prompts for agents or automation
- User's request lacks clarity or proper structure
- User wants to reduce LLM output tokens or API costs
- User needs to optimize JSON schema for token efficiency
- User requests compact output format while maintaining compatibility

## Core Principles

1. **Conciseness**: Remove unnecessary words while preserving intent
2. **Structure**: Use clear formatting with multiple lines and logical sections
3. **XML Integration**: Mix natural text with XML tags for clarity and parsing
4. **Direct Mission**: Main task/quest/mission should NOT be wrapped in XML elements
5. **Clean Output**: Return ONLY the enhanced prompt - no meta-commentary

## Enhancement Process

### Input Analysis
- Identify the core objective
- Extract key requirements and constraints
- Detect ambiguities or missing information
- Recognize the intended agent or use case

### Task-Based Technique Selection (Optional)
Evaluate if the task would benefit from specific prompting techniques:

**Chain-of-Thought (CoT)**
- Use for: Complex reasoning, math problems, logical deduction, step-by-step analysis
- Implementation: Add instruction to "think step by step" or "show your reasoning"

**Chain-of-Draft**
- Use for: Writing tasks, content creation, iterative refinement
- Implementation: Request initial draft, then progressive improvements

**Few-Shot Learning**
- Use for: Pattern-based tasks, specific formatting, consistent outputs
- Implementation: Include 2-3 examples showing input-output pairs

**ReAct (Reasoning + Acting)**
- Use for: Tool use, multi-step tasks, decision-making processes
- Implementation: Combine reasoning traces with action steps

**Self-Consistency**
- Use for: Tasks needing verification, multiple valid approaches
- Implementation: Request multiple solutions, then synthesis

**Tree-of-Thoughts**
- Use for: Complex problem-solving, exploring alternatives
- Implementation: Ask to explore multiple paths before selecting best

**Role-Based Prompting**
- Use for: Domain-specific expertise, perspective-taking
- Implementation: Assign expert role (e.g., "Act as a senior engineer...")

**Least-to-Most Prompting**
- Use for: Breaking down complex problems into subproblems
- Implementation: Start with simpler versions, build up complexity

**Apply technique only if it materially improves the task outcome.**

### LLM Output Token Optimization

When the goal is to reduce output tokens (API costs) while maintaining functionality:

**Core Strategy: Compact Output + Server-Side Remapping**

The LLM generates ultra-compact format, application remaps to original format for clients. This provides:
- Significant token savings (30-60%)
- 100% backward compatibility
- Negligible remapping overhead (<10 microseconds)

**Optimization Techniques:**

**1. Ultra-Compact JSON Keys**
- Replace long keys with 1-2 character abbreviations
- Examples: `queries` → `q`, `keyword` → `kw`, `filter` → `f`, `sort_by` → `s`
- Savings: 70-85% per key

**2. Short Codes for Repeated Values**
- Replace long IDs/enums with short codes (c1-c18, etc.)
- Example: `category=MjUzOTM=` → `c=c4`
- Provide reverse mapping table in application
- Savings: 75-90% on category/enum values

**3. String Compression for Structured Data**
- Use compact string format instead of nested objects when possible
- Example: `[{"filter_by":"category","operator":"=","value":"c4"}]` → `"c=c4"`
- Parse and expand server-side
- Savings: 60-80% on filter/query structures

**4. Omit Default Values**
- Instruct LLM to omit fields with default values
- Application fills in defaults during remapping
- Example: Omit `"sort_by":"relevant"` when it's the default
- Savings: Additional 10-30% when defaults are common

**5. Operator Abbreviation**
- Use shortest form: `p<50000` instead of `price<50000`
- Parse `p`/`c` prefixes during remapping
- Combine with semicolons: `c=c4;p<50000` for multiple filters

**Implementation Pattern:**

```
System Prompt Structure:
1. Define ultra-compact schema with examples
2. Specify key mappings (q=queries, kw=keyword, etc.)
3. Provide short codes table (c1=category1, c2=category2, etc.)
4. Show examples of compact output
5. Emphasize: omit defaults when possible

Application Layer:
1. Parse compact LLM output
2. Expand abbreviated keys
3. Map short codes to full values
4. Fill in default values
5. Return original format to client
```

**Example Transformation:**

**Before Optimization (Original Output):**
```json
{
  "queries": [
    {"keyword": "milk", "filter": "category=dairy", "sort_by": "relevant"},
    {"keyword": "bread", "filter": "category=bakery", "sort_by": "relevant"}
  ]
}
```

**After Optimization (LLM Output - 60% smaller):**
```json
{
  "q": [
    {"kw": "milk", "f": "c=c8"},
    {"kw": "bread", "f": "c=c3"}
  ]
}
```

**Client Receives:** Original format (remapped automatically)

**Tradeoffs Analysis:**

✅ **Pros:**
- 30-60% token savings typical
- Lower API costs
- Faster LLM response (less to generate)
- 100% backward compatible

⚠️ **Cons:**
- Remapping overhead (<10μs, negligible)
- More complex implementation
- Requires application-side mapping logic
- Prompt becomes slightly less human-readable

**When to Apply:**
- High-volume API usage (>1000 requests/day)
- Cost-sensitive applications
- Output tokens are >50% of total costs
- Schema is stable and well-defined
- Application can handle remapping logic

**When NOT to Apply:**
- Low-volume usage (<100 requests/day)
- Schema frequently changes
- Human readability is critical
- No application layer (direct LLM → client)

### Structural Improvements
- Break complex requests into clear sections
- Use XML tags for: constraints, examples, context, format requirements
- Keep main mission/task as direct natural language
- Apply logical line breaks for readability

### Language Optimization
- Replace verbose phrases with concise alternatives
- Use active voice and direct instructions
- Eliminate redundancy and filler words
- Maintain specificity while reducing length

## XML Tag Usage Guidelines

**Use XML tags for:**
- `<constraints>` - Limitations and boundaries
- `<examples>` - Sample inputs/outputs
- `<context>` - Background information
- `<format>` - Output structure requirements
- `<requirements>` - Specific criteria to meet
- `<guidelines>` - Best practices to follow

**Do NOT use XML tags for:**
- The primary mission statement
- The main task description
- The core request or question

## Output Format

Return ONLY the enhanced prompt with:
- No conversational lead-in
- No explanations or commentary
- No placeholder text
- No quotation marks wrapping the prompt
- No meta-discussion about the enhancement

## Example Transformations

**Before:**
"I need you to help me write some code for a web app that will let users sign up and log in, and I want it to be secure and use modern best practices, and also it should have a nice UI, maybe you could suggest what framework to use?"

**After:**
Create a secure authentication system for a web application with user registration and login functionality.

<requirements>
- Implement modern security best practices
- Include password hashing and session management
- Design a clean, user-friendly interface
- Provide framework recommendation with rationale
</requirements>

<format>
- Code implementation
- Security considerations
- Framework justification
- UI/UX guidelines
</format>

---

**Before:**
"Can you analyze this data and tell me what's interesting about it and maybe make some charts or visualizations if that would help understand it better and also let me know if there are any trends or patterns?"

**After:**
Analyze the provided dataset and identify key insights, trends, and patterns.

<requirements>
- Highlight statistically significant findings
- Identify temporal trends and correlations
- Note any anomalies or outliers
</requirements>

<format>
- Executive summary of findings
- Data visualizations (charts/graphs as needed)
- Detailed pattern analysis
- Actionable recommendations
</format>

---

**Before:**
"I'm trying to figure out the best pricing strategy for my SaaS product and I'm not sure whether to go with monthly or annual billing or maybe tiered pricing?"

**After (with Chain-of-Thought technique applied):**
Determine the optimal pricing strategy for a SaaS product.

<context>
Consider: monthly vs. annual billing, tiered pricing models, market positioning
</context>

<approach>
Think step by step:
1. Analyze target customer segments and their payment preferences
2. Evaluate competitor pricing models in the space
3. Calculate unit economics for each pricing option
4. Assess cash flow implications
5. Consider customer lifetime value impact
</approach>

<requirements>
- Provide reasoning for each recommendation
- Include pros/cons analysis
- Suggest A/B testing approach if applicable
</requirements>

---

**Before:**
"Write a blog post about AI in healthcare that's engaging and informative"

**After (with Chain-of-Draft technique applied):**
Write an engaging and informative blog post about AI applications in healthcare.

<approach>
Use iterative drafting:
1. Create outline with key points and narrative arc
2. Draft introduction and conclusion
3. Develop body sections with examples
4. Refine for clarity, flow, and engagement
</approach>

<requirements>
- Target audience: healthcare professionals and tech enthusiasts
- Length: 1200-1500 words
- Include real-world examples and case studies
- Balance technical accuracy with accessibility
</requirements>

<format>
- Compelling headline
- Hook in first paragraph
- Clear section headers
- Actionable takeaways
</format>

## Real-World Token Optimization Example

**Before (Original Prompt):**
```
Create JSON queries to search for products. Each query should have a keyword, filter with category, and sort_by field. Return in this format: {"queries":[{"keyword":"milk","filter":"category=dairy","sort_by":"relevance"}]}
```

**After (Token-Optimized Prompt):**
```
Generate product search JSON queries. Reject dangerous content.

<rules>
- Each query: ≥1 category filter
- Total: ≥3 keywords (no duplicates)
- Use 'ex' for exact brands/attributes
- Default sort: relevant (omit if default)
- Filter: string format "c=c4" or "c=c4;p<50000"
</rules>

<categories>
c1=household, c2=personal care, c3=bakery, c4=fresh food, c5=oils, c6=dry goods, c7=cleaning, c8=dairy
</categories>

<examples>
"milk vinamilk"→{"q":[{"kw":"milk vinamilk","ex":"vinamilk","f":"c=c8","s":"popular"}]}
"rice noodles meat"→{"q":[{"kw":"rice","f":"c=c6"},{"kw":"noodles","f":"c=c6"},{"kw":"meat","f":"c=c4"}]}
"oranges under 50k"→{"q":[{"kw":"oranges","f":"c=c4;p<50000"}]}
</examples>
```

**Result:**
- LLM generates: `{"q":[{"kw":"milk","f":"c=c8"}]}` (60% smaller)
- Application remaps to: `{"queries":[{"keyword":"milk","filter":"category=dairy","sort_by":"relevance"}]}`
- Client receives original format unchanged
- Token savings: 60.5% on typical 3-query response

## Quality Checklist

Before returning the enhanced prompt, verify:
- ✓ Main objective is clear and unambiguous
- ✓ XML tags are used appropriately (not for main mission)
- ✓ Structure uses multiple lines for readability
- ✓ Language is concise and direct
- ✓ No extraneous commentary included
- ✓ All key requirements preserved
- ✓ Actionable and complete
- ✓ If optimizing tokens: compact schema defined, mapping clear, examples provided

## Implementation Notes

When applying this skill:
1. Read the user's prompt completely
2. Identify enhancement opportunities
3. Apply structural and linguistic improvements
4. Output ONLY the enhanced version
5. Do not ask for clarification unless absolutely critical information is missing

The enhanced prompt should be immediately usable by the user without any modifications.
