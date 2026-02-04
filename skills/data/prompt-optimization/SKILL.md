---
name: prompt-optimization
description: Transform vague requests into production-ready, hallucination-free prompts optimized for Claude 4.x. Applies investigation-first protocols, anti-hallucination guards, extended thinking patterns, and multishot examples. Use when user requests prompt improvement, optimization, or asks to fix hallucinations, structure vague requests, apply Claude 4.x best practices, or create production-grade prompts.
---

# Prompt Optimization Skill

## Overview

Transform any request into an optimized, production-ready prompt for Claude 4.x that eliminates hallucinations and ensures first-response accuracy. Apply investigation-first protocols, extended thinking patterns, and anti-hallucination guards.

## When to Use

Trigger this skill when:
- User requests prompt improvement or optimization
- Prompt contains "optimize", "improve my prompt", "make this better"
- Vague requests need clarification and structure
- Existing prompts show hallucination issues
- User mentions "investigation first", "anti-hallucination", "production-ready"

## Quick Start

### Basic Optimization
```
User: "optimize: [paste prompt]"
→ Analyze structure
→ Apply Claude 4.x patterns
→ Return production version
```

### Eliminate Hallucinations
```
User: "fix hallucinations in: [prompt]"
→ Add investigation protocol
→ Insert verification checkpoints
→ Remove speculation triggers
```

## Core Optimization Framework

### 6 Key Strategies

#### 1. Context & Motivation
Explain WHY, not just WHAT.

```xml
❌ WEAK: "Never use ellipses"
✅ STRONG: "Your response will be read by text-to-speech, 
so never use ellipses since TTS cannot pronounce them."
```

#### 2. Investigation-First
NEVER provide answers before investigating.

```xml
<investigation_required>
When user asks: "Fix this bug"

❌ DON'T: Immediately suggest fixes
✅ DO: 
1. Examine code structure
2. Identify error location
3. Trace execution path
4. Review logs
5. Form evidence-based hypothesis
6. THEN suggest solution
</investigation_required>
```

#### 3. Multishot Examples
Provide 2-3 examples covering different scenarios.

```xml
<multishot_pattern>
- Typical case (80% of scenarios)
- Edge case (unusual but valid)
- Error case (what NOT to do)
</multishot_pattern>
```

#### 4. Explicit Output Format
Define EXACTLY what output should look like.

```xml
<output_format>
Structure:
1. **Summary** (2-3 sentences)
2. **Key Findings** (bullets)
3. **Recommendations** (numbered)
4. **Next Steps** (actions)

Do NOT include opinions or speculation.
</output_format>
```

#### 5. Extended Thinking
For complex tasks, enable step-by-step reasoning.

```xml
<thinking_protocol>
Break down the problem:
1. What are we achieving?
2. What info do we have?
3. What steps are needed?
4. What could go wrong?
5. How do we verify?
</thinking_protocol>
```

#### 6. Anti-Hallucination Guards

```xml
<anti_hallucination>
<rules>
1. NEVER make up facts/statistics
2. ALWAYS cite sources when available
3. Use "I don't know" when uncertain
4. Investigate before answering
5. Verify against context
</rules>

<when_uncertain>
If info not in context:
- State what you DO know
- Explain what's missing
- Suggest how to find it
- DON'T guess
</when_uncertain>
</anti_hallucination>
```

## Optimized Prompt Template

Use this structure:

```xml
<role>
Specific expert role with domain knowledge
</role>

<context>
Why this task matters and background
</context>

<investigation>
What to check before responding:
- Information to gather
- Resources to consult
- Questions to clarify
</investigation>

<thinking>
Step-by-step approach:
1. Analyze request
2. Identify requirements
3. Consider edge cases
4. Plan response
5. Verify assumptions
</thinking>

<execution>
How to perform the task:
- Steps to follow
- Tools/methods to use
- Quality checks
</execution>

<output_format>
Exact format for response
</output_format>

<anti_hallucination>
Never speculate. If uncertain, state clearly.
</anti_hallucination>

<examples>
<example type="typical">[Ex 1]</example>
<example type="edge">[Ex 2]</example>
<example type="error">[Ex 3]</example>
</examples>
</optimized_prompt_template>
```

## Claude 4.x Features

### Extended Thinking
Enable for complex reasoning tasks.

```xml
<extended_thinking>
Use when task requires:
- Multi-step analysis
- Complex problem solving
- Long-horizon planning

Pattern: "Think step-by-step:
1. [Step]
2. [Step]
3. [Verification]"
</extended_thinking>
```

### Parallel Tool Calling
Run multiple operations simultaneously.

```xml
<parallel_tools>
✅ DO: Call tools in parallel when independent
❌ DON'T: Sequential when unnecessary

Example: "Fetch user AND load settings AND check permissions"
→ All run simultaneously
</parallel_tools>
```

### Long-Horizon Tasks
Track progress across interactions.

```xml
<long_horizon>
<state_management>
- Create progress.txt
- Log completed subtasks
- Note blockers
- Update after each step
</state_management>

<continuation>
When resuming:
1. Read progress.txt
2. Verify last state
3. Continue next task
4. Update progress
</continuation>
</long_horizon>
```

## MCP Integration

```xml
<mcp_pattern>
<discovery>
1. Check MCP resources
2. Identify relevant tools
3. Load contextual prompts
</discovery>

<execution>
User asks about data:
1. Search MCP resources
2. Use MCP tools for real-time data
3. Apply MCP formatting prompts
4. Combine response
</execution>

<example>
"What's in Q4 sales report?"
→ MCP Resource: google_drive://Q4_Sales.xlsx
→ MCP Tool: parse_excel()
→ MCP Prompt: sales_summary_template
→ Return formatted analysis
</example>
</mcp_pattern>
```

## Real-World Examples

### Example 1: Vague → Structured

**Before:** "Help me build a website"

**After:** See [website-build-example.md](references/website-build-example.md)

### Example 2: Bug Fix → Investigation-First

**Before:** "My app crashes on submit"

**After:** See [bug-fix-example.md](references/bug-fix-example.md)

### Example 3: Data Analysis → Verification-First

**Before:** "Analyze this CSV"

**After:** See [data-analysis-example.md](references/data-analysis-example.md)

## Advanced Patterns

### Self-Verification
```xml
<self_verification>
After generating response:
1. Review vs requirements
2. Check hallucinations
3. Verify facts
4. Confirm format
5. Test edge cases

Issues found? Revise before delivery.
</self_verification>
```

### Progressive Refinement
```xml
<progressive_refinement>
For complex prompts:
1. Start basic
2. Test samples
3. Identify failures
4. Add guards
5. Retest
6. Document

Iterate based on performance.
</progressive_refinement>
```

### Context Management
```xml
<context_optimization>
For large prompts:
1. **Essential First**: Core instructions at top
2. **Progressive Disclosure**: Details on-demand
3. **References**: Link vs including
4. **Examples Last**: After instructions

If >2000 words:
- Split into skill + references/
- Use MCP for external resources
</context_optimization>
```

## Guidelines

### Always Do:
✅ Investigate before answering
✅ Provide multiple examples
✅ Define clear output format
✅ Include anti-hallucination guards
✅ Explain WHY, not just WHAT
✅ Use XML for structure
✅ Test with edge cases

### Never Do:
❌ Skip investigation
❌ Assume intent
❌ Single example only
❌ Ambiguous output format
❌ Ignore hallucination risks
❌ Vague instructions
❌ Deliver untested prompts

### Red Flags (Fix These):
🚩 "Create something" (too vague)
🚩 No examples
🚩 Missing output format
🚩 No verification steps
🚩 Assumes context
🚩 No anti-hallucination guards
🚩 Single-shot examples

## Output Template

Deliver this when optimizing:

```markdown
# Optimized Prompt

[Complete optimized prompt in XML format]

---

## Optimization Summary

**Changes Made:**
- Added investigation protocol
- Included multishot examples
- Defined output format
- Added anti-hallucination guards
- [Others]

**Expected Improvements:**
- Hallucination reduction: ~X%
- First-response accuracy: ~Y%
- Clarity: High/Medium/Low

**Testing Checklist:**
- [ ] Typical case
- [ ] Edge case
- [ ] Error/invalid input
- [ ] Ambiguous request
- [ ] Missing info

---

Ready to use!
```

## Quality Metrics

| Metric | Target |
|--------|--------|
| Hallucination Rate | <5% |
| First-Response Success | >90% |
| Iterations Needed | 1-2 |
| Clarity Score | High |

## Additional Resources

For detailed examples and deep-dive topics:
- See `references/` directory for complete examples
- Claude 4.x documentation
- MCP specification
- Anthropic prompt engineering guide

---

*Version: 1.0.0 | Optimized for Claude 4.x*
