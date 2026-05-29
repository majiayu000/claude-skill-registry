---
sidebar_position: 4
title: "Build Your MCP-Wrapping Skill"
description: "Create a production skill that wraps an MCP server with intelligent decision-making, result filtering, and error recovery. Learn to orchestrate code execution through specification-first design."
keywords: [MCP wrapping, skill implementation, client initialization, result filtering, token efficiency, error handling, skill testing]
chapter: 39
lesson: 4
duration_minutes: 45

# HIDDEN SKILLS METADATA
skills:
  - name: "Building MCP-Wrapping Skills"
    proficiency_level: "B2"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can implement a skill that wraps an MCP server with proper client initialization, result filtering logic, and error handling"

  - name: "Orchestrating Code Execution Through MCP"
    proficiency_level: "B2"
    category: "Technical"
    bloom_level: "Create"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can design and test MCP-wrapping skills that demonstrate 30%+ token efficiency gains through intelligent filtering"

  - name: "Testing Skill Implementations"
    proficiency_level: "B2"
    category: "Technical"
    bloom_level: "Evaluate"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can validate skill behavior through end-to-end testing and document effectiveness metrics"

learning_objectives:
  - objective: "Write specification for MCP-wrapping skill including intent, MCP server reference, filtering criteria, and success metrics"
    proficiency_level: "B2"
    bloom_level: "Apply"
    assessment_method: "Students complete spec.md before implementation, design covers intent, architecture, and acceptance tests"

  - objective: "Implement MCP client initialization and tool invocation patterns within a skill"
    proficiency_level: "B2"
    bloom_level: "Apply"
    assessment_method: "Skill successfully initializes MCP client, calls tool with parameters, and processes response"

  - objective: "Design and validate result filtering logic that reduces token consumption by 30%+"
    proficiency_level: "B2"
    bloom_level: "Create"
    assessment_method: "Students measure token count before/after filtering, explain filtering heuristics, and validate against test queries"

  - objective: "Test skill implementation end-to-end with multiple query scenarios from different domains"
    proficiency_level: "B2"
    bloom_level: "Evaluate"
    assessment_method: "Skill execution tests pass across clean input, malformed input, and edge cases; error handling validated"

cognitive_load:
  new_concepts: 9
  assessment: "9 concepts (spec.md for skill, persona implementation, questions as filtering criteria, MCP client initialization, tool invocation, result filtering logic, error handling, skill testing, consumer documentation) within B2 limit (7-10) ✓"

differentiation:
  extension_for_advanced: "Implement dynamic filtering that adapts heuristics based on user experience level detected in queries. Add caching layer to avoid redundant MCP calls. Measure performance impact of filtering strategies."
  remedial_for_struggling: "Start with skeleton implementation. Build one filtering criterion at a time. Test after each addition. Map test queries to expected output before implementing filtering logic."
---

# Build Your MCP-Wrapping Skill

In the previous lesson, you analyzed how skills layer intelligence on top of MCP servers. You saw how `fetching-library-docs` achieves ~77% token reduction through careful filtering. You understood the persona, questions, and principles that guide intelligent decision-making.

Now you're going to build one.

This lesson is different from most programming tutorials. We're not starting with code. We're starting with a **specification**—a clear statement of what your skill should do, why it matters, and how you'll know it works. Once that specification is solid, the implementation becomes straightforward. You'll work collaboratively with AI to build the skill, discovering patterns together rather than following pre-written steps.

By the end of this lesson, you'll have a production-ready MCP-wrapping skill that:
- Wraps an MCP server from Chapter 38 with intelligent filtering
- Reduces token consumption by 30%+ through targeted result filtering
- Handles errors gracefully with fallback strategies
- Works across multiple query scenarios from your domain

Let's build it together.

---

## Step 1: Specification First

The most common failure in skill development happens here: developers skip the specification and jump to coding. They think they know what they're building, start writing code, and discover halfway through that their approach doesn't match their actual needs.

We're not doing that.

Before touching code, you'll write a **specification** that answers four critical questions:

1. **What MCP server are you wrapping?** (intent, library, use cases)
2. **What intelligent decisions does your skill make?** (persona, questions, filtering logic)
3. **How will you measure success?** (token efficiency targets, test coverage)
4. **What happens when something fails?** (error recovery strategy)

### Your First Specification

Choose an MCP server from Chapter 38 that you've built or studied. This could be:
- A documentation fetcher (like Context7 in Chapter 38 examples)
- A database query tool
- A file processor
- A code analysis service
- Any tool that returns results larger than typical Claude context

Now write your spec. Use this template:

```markdown
# Specification: [Your Skill Name]

## Intent
[What problem does this skill solve? Who uses it? When do they invoke it?]

## MCP Server Reference
[Which MCP server does this wrap? What tool does it expose?]

## Success Criteria
- Token efficiency: Achieve 30%+ reduction vs raw MCP output
- Accuracy: Returned results must satisfy 100% of query requirements
- Coverage: Works across [describe domain variety: "3+ different documentation libraries", "5+ query patterns", etc.]
- Reliability: Graceful error handling for [describe failure modes: "missing resources", "timeout", "malformed queries"]

## Filtering Strategy
[What logic will you use to filter MCP results?
- Token counting before/after
- Relevance scoring criteria
- Content extraction rules
- Edge case handling]

## Test Scenarios
[List 3-5 concrete test cases you'll validate against:
1. Scenario: [user query] → Expected output: [what should be returned]
2. Scenario: [edge case] → Expected output: [how should skill handle it]
...]
```

Take 10 minutes to write this. Don't overthink it—your specification will evolve as you implement. The goal is clarity, not perfection.

**Example Specification** (You'll write your own):

```markdown
# Specification: Python-API-Documentation-Fetcher

## Intent
Fetch Python standard library and popular package documentation with automatic filtering for code examples and signatures. Activated when user asks "How do I use X?" or "Show me examples of X."

## MCP Server Reference
Documentation-Context MCP (Chapter 38) exposing `fetch_docs` tool.

## Success Criteria
- Token efficiency: Achieve 40%+ reduction vs raw Context7 output (target: 800 tokens → 480 tokens)
- Accuracy: Returned examples match user's experience level (beginner vs advanced)
- Coverage: Works across Python stdlib, NumPy, Pandas, Requests
- Reliability: Graceful "Not found" message when documentation unavailable

## Filtering Strategy
1. Extract code blocks (marked with ```python)
2. Extract function signatures (def keyword + parameters)
3. Extract usage notes (marked with # Note: or # Warning:)
4. Score by relevance to query keywords
5. Return top 5 highest-scoring segments

## Test Scenarios
1. "How do I use list comprehensions?" → Returns 3-4 examples, signature, one warning
2. "What's NumPy reshape?" → Returns reshape() signature, 2 examples, constraint notes
3. "Pandas concat invalid" → Returns "Not found" with suggestion to try "merge"
4. "Show me decorators" → Returns decorator patterns, syntax, common mistakes
5. "urllib3 connection pooling" → Returns class structure, pool configuration, timeout example
```

---

## Step 2: Persona and Questions Design

Now that you have a specification, let's translate it into the persona and questions your skill will use.

Your **persona** is the expert identity that activates your skill's decision-making. It's not "You are a Python expert" (generic). It's the specific stance your skill takes.

For the documentation fetcher:

**Persona**: "You are an API documentation specialist focused on code clarity. Your role is to (1) identify which library and feature the user is asking about, (2) fetch documentation via MCP, and (3) extract and return ONLY code examples, function signatures, and critical constraints that match the user's apparent experience level."

This persona tells us exactly what the skill optimizes for: clarity through selective extraction.

Now write the **questions** your skill asks itself to make decisions:

1. **Which library is the user asking about?** (Determines which MCP context to fetch)
2. **What specific feature or concept?** (Narrows filtering scope)
3. **What's the user's apparent experience level?** (Filters for beginner vs advanced examples)
4. **Are they looking for examples, syntax, or both?** (Determines extraction priority)
5. **What constraints matter most?** (Performance, security, compatibility?)

These questions drive your filtering logic. Each question you answer shapes what gets filtered and what gets returned.

**Your turn**: Write a persona and 5 questions for your skill. Make them specific to your domain, not generic. The persona should describe what decisions the skill makes. The questions should be answerable from examining the user's query.

---

## Step 3: Building the Skill Collaboratively

This is where the real learning happens. You're not going to build this skill alone. You and AI are going to collaborate—discovering execution patterns together, incorporating your domain constraints, and iterating toward a solution neither of you would have produced independently.

Here's how the collaboration unfolds:

### Part 1: Learning Execution Patterns

Ask AI to show you how to initialize an MCP client and call a tool. Don't just ask "how do I use MCP client?" Ask a specific question that reveals the pattern:

**Your prompt**:
```
I'm building a skill that wraps an MCP server.
I need to initialize an MCP StdIO client that connects to my custom MCP server,
then call a specific tool and process the response.

Show me the pattern for:
1. Initializing the StdIO client
2. Calling a tool with parameters
3. Extracting the tool result
4. Counting tokens in the response before and after filtering

Include error handling for "tool not found" and "timeout" scenarios.
```

AI will show you patterns you might not have discovered—maybe using context managers, error recovery strategies, token counting libraries. You'll see approaches that expand your thinking.

### Part 2: Refining With Your Domain Knowledge

Now AI has suggested an approach. But your domain has specific requirements that AI doesn't know about. You refine the implementation:

**Your response to AI**:
```
This pattern helps, but I need to adjust for my domain constraints:

1. My queries often include comparison requests ("Compare X and Y libraries").
   Your current filtering returns single-library results.
   How do we modify the filtering to support multi-library comparison?

2. My users range from beginners (want simple examples) to advanced (want performance notes).
   I need to detect experience level from the query and adjust filtering accordingly.
   How would you score relevance differently for beginner vs advanced?

3. The MCP server timeout is 5 seconds. If it times out, I should return a cached
   result from previous queries on the same library (if available).
   How would you implement caching without storing full responses?
```

You're articulating your actual requirements, not accepting generic solutions. This is where your domain expertise shapes the implementation.

### Part 3: Iterating Toward a Robust Solution

AI responds to your constraints. You test the solution. It doesn't work quite right. You iterate:

**Round 1**:
- AI suggests filtering by keyword scoring
- You test: some irrelevant results still pass through

**Round 2**:
- You point out: "The scoring weights aren't working. Simple examples are being filtered out for advanced queries."
- AI refines: suggests weighted scoring where query keywords get 60% weight, content type (example vs note) gets 40%
- You test: better, but still not right

**Round 3**:
- You notice: "The experience level detection is too simplistic. 'decorator' is beginner in one context, advanced in another."
- AI proposes: use question marks and "how do I" as beginner signals, "performance", "optimization" as advanced signals
- You test: now working well for 80% of queries

**Round 4**:
- You discover: "The remaining 20% are comparison queries that don't fit either pattern."
- AI suggests: detection for "vs" and "compared to" keywords triggers comparison mode with different filtering
- You test: all patterns working

What emerged is a solution neither of you had at the start. The robustness came through iteration, with each round addressing a specific limitation.

---

## Step 4: Implementation and Testing

Now let's build the actual skill. The specification and persona guide our implementation, so we know exactly what we're building.

### Skeleton Implementation

Your skill has this structure:

```python
# skill.md (SKILL.md structure from Chapter 5)
persona: |
  [Your persona from Step 2]

questions:
  - [Question 1]
  - [Question 2]
  - [Question 3]
  - [Question 4]
  - [Question 5]

principles:
  - Fail gracefully: Return meaningful error messages if MCP unavailable
  - Filter ruthlessly: Prioritize clarity over comprehensiveness
  - Verify early: Check MCP connection before processing queries
  - Cache strategically: Store successful results for timeout recovery

# Implementation follows:
```

### Key Implementation Patterns

**Pattern 1: MCP Client Initialization**

```python
from mcp.client.stdio import StdIOClient

# Initialize client with your MCP server
client = StdIOClient(
    command="python",
    args=["-m", "your_mcp_server_module"],
    timeout=5.0
)

# Connect and verify
with client:
    # Tool calls happen inside this context
    result = client.call_tool("fetch_docs", {"library": "numpy", "topic": "reshape"})
```

The context manager ensures proper cleanup. The timeout prevents hanging. Keep this pattern consistent.

**Pattern 2: Token Counting Before/After**

```python
import tiktoken

def count_tokens(text: str) -> int:
    """Count tokens in text using OpenAI's tokenizer."""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

# Before filtering
raw_response = client.call_tool(...)
tokens_before = count_tokens(raw_response)

# After filtering
filtered_response = filter_results(raw_response, user_query)
tokens_after = count_tokens(filtered_response)

# Calculate savings
savings_percent = ((tokens_before - tokens_after) / tokens_before) * 100
print(f"Token savings: {savings_percent:.1f}%")
```

**Pattern 3: Result Filtering Logic**

Your filtering logic depends on your domain, but here's a template:

```python
def filter_results(raw_response: str, user_query: str) -> str:
    """
    Filter raw MCP response based on user query and experience level.

    Args:
        raw_response: Full response from MCP server
        user_query: Original user question

    Returns:
        Filtered response containing only relevant segments
    """
    # Step 1: Detect experience level
    experience_level = detect_experience_level(user_query)
    # "beginner" or "advanced"

    # Step 2: Extract candidates
    code_examples = extract_code_blocks(raw_response)
    signatures = extract_function_signatures(raw_response)
    notes = extract_notes(raw_response, experience_level)

    # Step 3: Score by relevance
    scored_examples = [
        (example, relevance_score(example, user_query))
        for example in code_examples
    ]
    scored_examples.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Return top N results
    selected = scored_examples[:5]  # Top 5 by relevance

    return format_output(signatures, selected, notes)
```

### Your Implementation Task

Using your specification and persona as a guide:

1. **Write the skill.md structure** (persona, questions, principles)
2. **Implement MCP client initialization** (handle the specific MCP server you're wrapping)
3. **Implement filtering logic** matching your specification's success criteria
4. **Add error handling** for timeout, missing resources, invalid queries
5. **Test with your test scenarios** from Step 1 specification

Use the patterns above as templates. Adapt them to your specific MCP server and filtering needs.

---

## Step 5: Documentation for Skill Consumers

After testing, you'll write documentation so others can use your skill. This is the final validation: if you can't explain clearly how to use your skill, you haven't understood it well enough.

### Usage Guide Template

```markdown
# [Skill Name] Usage Guide

## What This Skill Does

[Explain the skill's purpose in 1-2 sentences. Who uses it? When?]

## When to Activate This Skill

Your skill activates automatically when:
- User query contains keywords matching your activation conditions
- Context suggests the user needs [your domain]
- [Other trigger conditions specific to your skill]

## Success Metrics

This skill is working well when:
- Token efficiency: Results show 30%+ reduction vs raw MCP output
- Accuracy: Returned results directly answer the user's question
- Completeness: All critical information is included (not overly filtered)
- Speed: MCP call completes within timeout (handle gracefully if not)

## Example Queries

| Query | What Skill Should Do | Example Output |
|-------|---------------------|-----------------|
| [Example 1] | [Expected behavior] | [Sample result] |
| [Example 2] | [Expected behavior] | [Sample result] |
| [Example 3 - edge case] | [Expected behavior] | [Sample result] |

## Constraints and Limitations

- [List what this skill does NOT do]
- [List known limitations]
- [List scenarios where fallback behavior triggers]
```

Write your usage guide after testing. It forces you to articulate what your skill actually does vs what you thought it would do.

---

## Try With AI: Building an MCP-Wrapping Skill

Now it's your turn to build. This "Try With AI" section walks you through the complete process using AI collaboration.

### Part 1: Specification Development

Start by clarifying your skill's purpose:

**Prompt 1 - Specification Planning**:
```
I'm building a skill that wraps an MCP server. I want to wrap [your chosen MCP server]
to provide [your domain/use case].

Help me develop a clear specification covering:
1. What problem does this skill solve?
2. What MCP tool does it call?
3. What filtering logic will reduce token consumption?
4. What failure modes might occur?
5. How will I measure success?

Let me be specific about my domain:
[Describe your specific use case, domain, and target users]
```

This step clarifies what you're building before you start coding. Specification quality directly determines implementation quality.

---

### Part 2: Pattern Implementation

Once you have your specification, ask AI to show you the execution patterns:

**Prompt 2 - MCP Client Pattern**:
```
I have this specification for my MCP-wrapping skill:
[Paste your spec here]

Now show me the pattern for implementing this:
1. How do I initialize an MCP client that connects to my server?
2. How do I call the MCP tool and handle the response?
3. How do I count tokens before and after filtering?
4. How do I implement the filtering logic to achieve my token efficiency target?

Include error handling for:
- MCP server not available
- Tool execution timeout
- Tool returns empty result
- Malformed query

Give me complete, testable code that I can run immediately.
```

This step reveals practical patterns you can adapt to your domain. You see error recovery, token measurement, and client initialization working together.

---

### Part 3: Constraint Refinement

Now test the AI's suggested approach and refine based on your actual needs:

**Prompt 3 - Domain Constraints**:
```
I implemented the pattern you showed, and I discovered that my domain has specific
constraints that the generic pattern doesn't handle:

[Describe 2-3 specific constraints from testing:
- Example: "Queries often ask for comparisons between two libraries"
- Example: "My users range from beginner to advanced, and filtering should adapt"
- Example: "The MCP server is slow for large libraries, so I need caching"]

How do I modify the filtering logic to handle these constraints while maintaining
my token efficiency target? Show me concrete code changes that address each constraint.

Here's what I've tried so far:
[Share a code snippet or description of your attempt]

What's not working:
[Describe the specific failure mode or limitation you hit]
```

This step addresses the gap between generic patterns and your domain reality. Real testing reveals which constraints matter most.

---

### Part 4: Testing and Iteration

Run your skill against your test scenarios and discover what needs refinement:

**Prompt 4 - Testing and Debugging**:
```
I tested my skill with these scenarios from my specification:

Test 1: [Your test scenario]
Expected: [What should happen]
Actual: [What actually happened]
Problem: [Why it didn't work]

Test 2: [Your test scenario]
Expected: [What should happen]
Actual: [What actually happened]
Problem: [Why it didn't work]

I can see the pattern: [Describe the common issue you've discovered]

How would you adjust the filtering heuristics or error handling to address this?
Show me specific code changes and explain the reasoning.
```

This step shows how testing surfaces patterns that guide refinement. Theory meets practice when your assumptions collide with actual behavior.

---

### Part 5: Final Validation

Once your skill is working across test scenarios, validate that it meets your specification:

**Prompt 5 - Specification Validation**:
```
I've built a working MCP-wrapping skill. Now I need to validate it against my
original specification.

My spec required:
- Token efficiency: [Your target - example: 30%+ reduction]
- Accuracy: [Your target - example: 100% of queries answered directly]
- Coverage: [Your target - example: Works across 3+ libraries]
- Reliability: [Your target - example: Graceful error handling for timeouts]

Here are my actual results:
- Token efficiency: [Measured - example: 42% reduction achieved]
- Accuracy: [Measured - example: 95% of queries directly answered]
- Coverage: [Tested - example: Works across React, Vue, Svelte]
- Reliability: [Tested - example: Handles timeouts with fallback]

[For each metric that falls short, ask]:
How would you improve this? What's the tradeoff between [metric A] and [metric B]?

[For each metric that exceeds target, ask]:
Was there an unexpected benefit? What drove the better-than-expected result?
```

This step validates your implementation against your original intent. The differences between specification and reality reveal what you've learned.

---

### Success Criteria

You've successfully completed this lesson when:

✓ **Specification written**: You have a clear spec.md that answers the four core questions (what MCP, what intelligent decisions, how to measure success, error recovery)

✓ **Skill implemented**: Your skill successfully initializes an MCP client, calls the target tool, and returns filtered results

✓ **Token efficiency demonstrated**: Your filtered output achieves 30%+ token reduction compared to raw MCP output (measure with tiktoken)

✓ **Error handling validated**: Your skill gracefully handles at least 3 failure scenarios (timeout, missing resource, malformed query)

✓ **Tests passing**: Your skill produces correct results for all test scenarios in your specification

✓ **Documentation complete**: You can explain to another developer how to use your skill and what it optimizes for

✓ **Collaboration evident**: Your implementation shows how specification, pattern discovery, domain constraints, testing, and validation shaped your solution

The skill you've built isn't just code. It's an encoding of expertise in your domain. It knows when to invoke an MCP server, what to ask for, how to filter the results, and how to recover from failure. That's the pattern you'll see again and again as you build more complex skills in Lessons 5-8.

---

### Reference: Skill-Building Prompts

Use these prompts in sequence, adapting based on your specific MCP server and domain:

**Prompt 1: Specification Planning** (What are we building and why?)

```text
I'm building a skill that wraps an MCP server [your server name].

The problem I'm solving: [your domain problem]
The target users: [who needs this]
The MCP server capability: [what does it provide]

Help me write a specification covering intent, success criteria, filtering strategy,
and test scenarios. I want to achieve [your efficiency target]% token reduction.
```

**What you're learning**: Specification clarity—translating vague ideas into measurable requirements before writing any code.

**Prompt 2: Pattern Teaching** (How does MCP client work?)

```text
Show me the complete pattern for:
- Initializing an MCP StdIO client
- Calling a tool with parameters
- Counting tokens before/after with tiktoken
- Implementing filtering that achieves my token efficiency target
- Handling errors: timeout, not found, malformed query

Include the full working code, not just explanations.
```

**What you're learning**: Implementation patterns—recognizing reusable code structures for MCP interaction that you can adapt to any domain.

**Prompt 3: Constraint Teaching** (What's specific about my domain?)

```text
I tested the pattern you showed, and I need to adapt it for my domain:

Constraint 1: [Describe a specific requirement from your domain]
Constraint 2: [Describe another specific requirement]
Constraint 3: [Describe a third specific requirement]

How do I modify the filtering logic to handle these while maintaining token efficiency?
```

**What you're learning**: Domain constraint translation—adapting generic patterns to your specific needs while maintaining efficiency goals.

**Prompt 4: Testing and Debugging** (Why isn't it working?)

```text
I'm testing against these scenarios:

Test case: [Your test]
Expected: [What should happen]
Actual: [What happened]
Problem: [Why it's failing]

How do I fix the filtering to handle this case correctly?
```

**What you're learning**: Iterative refinement—using test results to identify and fix design gaps systematically.

**Prompt 5: Specification Validation** (Does it meet requirements?)

```text
I've built a working skill. Does it match my specification?

Spec requirement: [Your requirement]
Measured result: [What you measured]
Gap (if any): [If it falls short, what's the gap?]

[Ask for each requirement separately]

Overall: Does this skill successfully encode the intelligence layer I specified?
```

**What you're learning**: Validation thinking—measuring whether your implementation meets original intent and identifying any gaps.

**Expected outcome**: You have a tested, documented MCP-wrapping skill that demonstrates 30%+ token efficiency and handles error scenarios gracefully.
