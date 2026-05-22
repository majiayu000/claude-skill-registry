---
name: system-prompt-writer
description: This skill should be used when writing or improving system prompts for AI agents, providing expert guidance based on Anthropic's context engineering principles.
---

# System Prompt Writer Skill

This skill provides comprehensive guidelines for writing effective system prompts for AI agents, based on Anthropic's "Effective Context Engineering for AI Agents" principles.

## Core Philosophy: Context Engineering

**Context Engineering** is the art and science of curating what goes into the limited context window. The key principle is:

> "Find the minimum effective dose of information - the smallest possible set of high-signal tokens that maximize the likelihood of the desired outcome."

## System Prompt Writing Guidelines

### 1. Write at the "Right Altitude"

System prompts should be in the **Goldilocks zone** - not too rigid, not too vague.

**Too Rigid (Avoid):**
```
When the user asks about weather, first check the database, then validate the ZIP code format using regex pattern ^\d{5}(?:[-\s]\d{4})?$, then call get_weather_data with exactly these parameters...
```

**Too Vague (Avoid):**
```
Help users with their questions.
```

**Just Right (Use):**
```
You are a weather assistant. When users ask about weather:
1. Validate location information
2. Use available tools to fetch current weather data
3. Present information in a clear, conversational format
4. If data is unavailable, explain why and suggest alternatives
```

### 2. Minimum Effective Information

**Key Question:** Determine the smallest amount of context needed for the agent to succeed.

**Important Note:**
> "Minimal does not necessarily mean short; sufficient information must be provided to the agent up front to ensure it adheres to the desired behavior."

Focus on **high-signal tokens** that drive behavior, not arbitrary brevity.

**Before (Over-specified with low-signal information):**
```
You are a customer service agent for Acme Corp, founded in 1985 by John Smith in Seattle, Washington. Our company values are integrity, innovation, and customer satisfaction. We sell widgets, gadgets, and accessories. Our business hours are Monday-Friday 9am-5pm PST. We have 500 employees across 3 locations...
```

**After (Optimized - minimal but sufficient):**
```
You are an Acme Corp customer service agent. Help customers with product inquiries, orders, and support issues. Use available tools to access order history and product information. Escalate complex technical issues to specialists.
```

The optimized version is shorter AND higher-signal. However, if the agent needs detailed decision-making criteria to function correctly, include them - minimal doesn't mean inadequate.

### 3. Structure for Clarity

**Anthropic Recommendation:**
> "We recommend organizing prompts into distinct sections (like `<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description`, etc) and using techniques like XML tagging or Markdown headers to delineate these sections."

#### The Hybrid Approach: Markdown + XML

Use **Markdown headers** for major sections and **XML tags** for content within each section. This combines:
- **Readability** (Markdown headers are visual and familiar)
- **Structure** (XML tags clearly delineate content and support programmatic parsing)
- **Flexibility** (Matches Anthropic's actual examples and recommendations)

#### CRITICAL: Template Variable Escaping Rules

**The project uses a template system (`src/prompts/template.py`) that processes system prompts with variable substitution using Python's `.format()` method. Understanding and applying the correct escaping is MANDATORY.**

**How the Template System Works:**

```python
# template.py uses this pattern:
system_prompts = system_prompts.format(**context)

# Where context contains variables like:
# {CURRENT_TIME}, {USER_REQUEST}, {FULL_PLAN}, etc.
```

**Escaping Rule:**
- **Single braces `{}`** → Interpreted as template variables that must be replaced
- **Double braces `{{}}`** → Escaped to single braces `{}` in the output

**Implications for Prompt Writing:**

1. **Template Variables (Single Braces):**
   ```markdown
   ---
   CURRENT_TIME: {CURRENT_TIME}
   USER_REQUEST: {USER_REQUEST}
   FULL_PLAN: {FULL_PLAN}
   ---
   ```
   These are **intentional placeholders** that will be replaced with actual values.

2. **Code Samples (Double Braces Required):**
   ```markdown
   ❌ WRONG (Will cause KeyError):
   ```python
   print(f"Total: {value}")
   df_dict = {"key": "value"}
   track_calculation("id", {value})
   ```

   ✅ CORRECT (Use double braces):
   ```python
   print(f"Total: {{value}}")
   df_dict = {{"key": "value"}}
   track_calculation("id", {{value}})
   ```
   ```

**Common Scenarios Requiring Double Braces:**

| Context | Wrong | Correct |
|---------|-------|---------|
| Python f-strings | `f"Count: {n}"` | `f"Count: {{n}}"` |
| Dictionary literals | `{"key": "val"}` | `{{"key": "val"}}` |
| Set literals | `{1, 2, 3}` | `{{1, 2, 3}}` |
| Format strings | `"{:.2f}".format(x)` | `"{{:.2f}}".format(x)` |
| JSON examples | `{"name": "John"}` | `{{"name": "John"}}` |
| Placeholders in text | `Use {variable}` | `Use {{variable}}` |

**Why This Matters:**

Using single braces `{}` in code samples causes the template system to:
1. Attempt to replace `{value}` with a variable named `value` from context
2. Raise `KeyError: 'value'` when the variable doesn't exist
3. Cause agent initialization to fail

**Example from Real Prompt (coder.md):**

```markdown
**Result Storage After Each Task:**
```python
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
result_text = f"""
{{'='*50}}
## Analysis Stage: {{stage_name}}
## Execution Time: {{current_time}}
{{'-'*50}}
Result: {{result_description}}
{{'-'*50}}
Key Insights:
{{key_insights}}
{{'-'*50}}
Files: ./artifacts/category_chart.png
{{'='*50}}
"""
```
```

Notice:
- `{{'='*50}}` → Becomes `{'='*50}` in the actual prompt (Python expression)
- `{{stage_name}}` → Becomes `{stage_name}` (Python f-string variable)
- `{{current_time}}` → Becomes `{current_time}` (Python f-string variable)

**Pre-Writing Checklist:**

Before finalizing any system prompt:
- [ ] Identify all code samples with curly braces
- [ ] Convert ALL `{}` in code samples to `{{}}`
- [ ] Verify template variables (like `{CURRENT_TIME}`) use single braces
- [ ] Test prompt loading to catch any KeyError exceptions

**Recommended Structure:**

```markdown
## Role
<role>
You are a [specific role]. Your objective is to [clear goal].
</role>

## Background Information
<background_information>
[Relevant context that informs decision-making - only include if needed]
</background_information>

## Instructions
<instructions>
- [Key principle 1]
- [Key principle 2]
- When [situation], do [action]
</instructions>

## Tool Guidance
<tool_guidance>
- tool_name: Use when [specific condition]
- tool_name_2: Use when [specific condition]
</tool_guidance>

## Success Criteria
<success_criteria>
- [Criterion 1]
- [Criterion 2]
</success_criteria>

## Constraints
<constraints>
- Do not [constraint 1]
- Always [requirement 1]
</constraints>

## Output Format (optional)
<output_format>
[Expected structure of responses - include only if specific format needed]
</output_format>
```

**Why Hybrid Works Best:**
- ✅ **Human-readable**: Markdown headers provide visual structure
- ✅ **Machine-parseable**: XML tags enable section extraction and processing
- ✅ **Proven pattern**: Matches Anthropic's own examples in documentation
- ✅ **Flexible**: Easy to add/remove sections as needed
- ✅ **Best of both**: Combines readability with programmatic clarity

**Example:**

```markdown
## Role
<role>
You are a data analysis specialist focused on deriving insights from datasets through statistical analysis and visualization.
</role>

## Instructions
<instructions>
- Validate data quality before analysis
- Explain statistical concepts in plain language
- Provide both quantitative results and qualitative insights
- Suggest appropriate analysis methods based on data characteristics
</instructions>

## Tool Guidance
<tool_guidance>
- load_dataset(path): Use when user provides file path or URL
- analyze_statistics(data): Use for numerical summaries and descriptive stats
- create_visualization(data, type): Use to generate charts and plots
- python_repl(code): Use for custom analysis not covered by other tools
</tool_guidance>

## Constraints
<constraints>
- Do not run analysis on incomplete or corrupted data without warning
- Always state confidence levels and statistical significance
- Acknowledge when sample size is too small for reliable inference
</constraints>
```

**Why Structure Matters:**
- Helps the LLM parse different types of information
- Makes prompts easier to maintain and update
- Supports progressive disclosure (load sections as needed)
- Enables programmatic section extraction if needed
- Improves prompt interpretability

### 4. Tool Guidance in Prompts

**Scope Note:** This section focuses on **how to write tool usage guidance in system prompts**. Tool implementation and design are separate concerns handled by tool developers.

**Key Heuristic:**
> "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."

System prompts should provide **clear, unambiguous guidance** about when to use each tool.

#### Poor Tool Guidance

```
You have access to these tools: search_database, call_api, send_email. Use them as needed.
```

**Problems:**
- Vague ("as needed" - when is that?)
- No decision criteria
- Agent must guess when each tool is appropriate

#### Good Tool Guidance

```markdown
## Tool Guidance
<tool_guidance>
Available Tools:
- search_database: Use when user asks about past orders or account history
- call_api: Use for real-time inventory or pricing information
- send_email: Use only after confirming user's explicit consent to send email

Decision Tree:
- Account questions → search_database
- Product availability → call_api
- Follow-up communications → send_email (with consent)
</tool_guidance>
```

**Why This Works:**
- ✅ Specific conditions for each tool
- ✅ Decision tree for common scenarios
- ✅ Clear boundaries (e.g., "only after consent")
- ✅ No ambiguity about which tool to use

#### Best Practices for Tool Guidance

**1. Be Specific About Conditions**

❌ Vague:
```
- lookup_account: Use for account stuff
```

✅ Specific:
```
- lookup_account(email): Use when user asks about their subscription status, billing, or account settings
```

**2. Provide Decision Trees for Complex Scenarios**

```
Tool Selection Logic:
1. Is this about a past order?
   → Yes: search_orders(order_id or email)
   → No: Continue to step 2

2. Does it require real-time data (inventory, pricing)?
   → Yes: call_api(endpoint, params)
   → No: Continue to step 3

3. Is it a general product question?
   → Yes: search_knowledge_base(query)
```

**3. Specify Prerequisites and Constraints**

```
- send_email(to, subject, body):
  * Use ONLY after: user explicitly requests email or confirms consent
  * Do NOT use for: unsolicited communications, marketing
  * Required info: valid email address, clear purpose
```

**4. Handle Overlapping Tool Functionality**

If tools have overlapping use cases, be explicit:

```
When user asks about account:
- For current status (active/inactive): lookup_account_status(email)
- For billing history: lookup_billing(email, months=3)
- For full profile details: get_account_profile(email)

Use the most specific tool for the question asked.
```

#### Common Pitfalls to Avoid

❌ **Assuming shared context with tool names:**
```
- process_payment: Use appropriately
```
What's "appropriate"? Be specific.

❌ **Listing tools without guidance:**
```
Tools: tool1, tool2, tool3, tool4
```
This forces the agent to guess.

❌ **Contradictory or ambiguous criteria:**
```
- search_db: Use for user info
- get_user: Use for user details
```
What's the difference between "info" and "details"?

#### Template: Tool Guidance Section

```markdown
## Tool Guidance
<tool_guidance>
Available Tools:
- [tool_name]([params]): Use when [specific condition or user intent]
- [tool_name_2]([params]): Use when [specific condition]

Decision Framework:
[Provide clear logic for tool selection based on scenarios]

Special Notes:
- [Any constraints, prerequisites, or important caveats]
</tool_guidance>
```

#### Collaboration with Tool Developers

While this skill focuses on **prompt-level guidance**, effective tool usage in prompts depends on well-designed tools. When collaborating with tool developers, request:

- **Clear tool names** that indicate purpose
- **Unambiguous tool descriptions**
- **Minimal overlap** between tools
- **Token-efficient returns** (only necessary data)

If tools are ambiguous or overlapping, even the best prompt guidance won't help. Advocate for clean tool design to make prompts effective.

### 5. Few-Shot Prompting: Use Examples Wisely

**Anthropic's Strong Recommendation:**
> "Providing examples, otherwise known as few-shot prompting, is a well known best practice that we continue to strongly advise."

**Key Principle:**
> "For an LLM, examples are the 'pictures' worth a thousand words."

#### The Right Way: Curate Diverse, Canonical Examples

**DO:**
- Curate 2-3 **diverse, canonical examples** that effectively portray expected behavior
- Choose examples that demonstrate the range of scenarios
- Show both successful outputs AND edge case handling
- Keep examples focused and representative

**DON'T:**
- Stuff a "laundry list of edge cases" into your prompt
- Try to articulate every possible rule through examples
- Include redundant or overlapping examples

#### Example: Good vs. Bad Few-Shot Prompting

**❌ Bad (Laundry List of Edge Cases):**
```
Example 1: If user asks about product X, respond with Y
Example 2: If user asks about product Z, respond with W
Example 3: If user misspells product X, correct it
Example 4: If user is angry about product X, apologize
Example 5: If user asks about unavailable product X, suggest alternative
Example 6: If user asks for discount on X, follow policy
Example 7: If user asks about shipping for X...
[15 more examples covering every possible edge case]
```

**✅ Good (Diverse, Canonical Examples):**
```
Example 1: Standard Product Inquiry
User: "Tell me about the Pro subscription"
Agent: "Our Pro subscription ($50/month) includes unlimited API calls, priority support, and advanced analytics. Would you like to see a feature comparison with other tiers?"

Example 2: Handling Unavailable Items
User: "Can I get the Legacy plan?"
Agent: "The Legacy plan has been discontinued. Based on your needs, I'd recommend our current Pro or Enterprise tiers. What features are most important to you?"

Example 3: Complex Request Requiring Tool Use
User: "Why was I charged twice last month?"
Agent: [Uses search_billing_history tool] "I see two charges on Aug 15: one for your subscription renewal ($50) and one for additional API usage ($12). Would you like me to break down the usage charge?"
```

The three good examples demonstrate:
1. Standard successful interaction
2. Edge case (unavailable product) with graceful handling
3. Tool usage in context

This teaches the LLM the behavior pattern without trying to cover every possible scenario.

### 6. Define Success Criteria

Define explicitly what constitutes successful task completion:

```
Success means:
- User's question is fully answered
- Information is accurate and current
- Response is conversational and helpful
- Appropriate tools were used when needed

May ask clarifying questions if the user's request is ambiguous.
Should acknowledge when sufficient information is unavailable.
```

### 7. Provide Motivation Context

**Anthropic's Claude 4 Guidance:**
> "Provide the motivation behind any instruction to help Claude infer how to behave in edge cases."

Instructions work better when accompanied by the **why** behind them. This helps the agent handle edge cases not explicitly covered.

**Without Motivation (Less Effective):**
```
NEVER use ellipses in your responses.
```

**With Motivation (More Effective):**
```
Your response will be read aloud by a text-to-speech engine, so never use ellipses since the TTS engine will not know how to pronounce them.
```

**Why This Works:**
- Agent understands the underlying constraint (TTS compatibility)
- Can apply the principle to similar situations (avoid other TTS-unfriendly characters)
- Makes better decisions in edge cases not explicitly covered

**Example Patterns:**

| Without Motivation | With Motivation |
|-------------------|-----------------|
| "Keep responses under 100 words" | "Keep responses under 100 words because they'll be displayed on mobile screens with limited space" |
| "Always ask for confirmation" | "Always ask for confirmation before destructive operations because users may not realize the action is irreversible" |
| "Use formal language" | "Use formal language because this agent serves enterprise legal teams who expect professional communication" |

**When to Provide Motivation:**
- Instructions that might seem arbitrary
- Constraints that affect edge case behavior
- Rules where understanding "why" helps with generalization

## Context Management Strategies

### Strategy 1: Just-in-Time Loading

Instead of loading all information upfront, maintain lightweight identifiers:

```
Available knowledge sources:
- Product catalog: /data/products.json
- User manual: /docs/manual.pdf
- FAQ database: knowledge_base://faq

Load specific sections only when relevant to the user's question.
```

### Strategy 2: Progressive Disclosure

Structure prompts to reveal complexity gradually:

**Level 1 (Always loaded - Metadata):**
```
Available capabilities:
1. Order management
2. Product recommendations
3. Technical support
4. Account settings
```

**Level 2 (Loaded when needed - Details):**
```
[Only load detailed instructions for the selected capability]
```

### Strategy 3: Structured Note-Taking

Encourage agents to maintain state outside the main context:

```
Maintain a NOTES.md file to track:
- User preferences discovered during conversation
- Pending actions or follow-ups
- Key decisions made and rationale

Update notes after each significant interaction.
```

## Agent-Specific Patterns

### For Multi-Agent Systems

**Coordinator Agent:**
```
Role: Route user requests to specialized agents
- Analyze request to identify appropriate specialist
- Provide specialist with relevant context summary
- Synthesize responses from multiple specialists if needed
```

**Specialist Agent:**
```
Role: Expert in [domain]
- Assume context summary from coordinator is complete
- Focus deeply on your domain expertise
- Return concise results to coordinator
```

### For Long-Running Tasks

**Compaction Strategy:**
```
When conversation history exceeds 50 messages:
1. Summarize key points and decisions
2. Preserve critical context (user preferences, constraints)
3. Archive full history to /session/[id]/history.json
4. Continue with compacted context
```

**For Multi-Context Window Workflows:**

If your agent handles **complex tasks spanning multiple sessions** or context windows (e.g., large refactoring projects, multi-day analysis), see the specialized guide:

→ **`references/long-horizon-tasks-guide.md`**

This guide covers:
- First context window setup (tests.json, init.sh patterns)
- State management across sessions
- Context persistence prompts
- Multi-session agent templates

**Note:** Most agents don't need these patterns. Only use when tasks genuinely span multiple context windows.

## Anti-Patterns to Avoid

❌ **Over-specification:** Avoid writing step-by-step algorithms - let the LLM reason
❌ **Redundancy:** Avoid repeating information available in tool descriptions
❌ **Premature optimization:** Avoid guessing what context will be needed
❌ **Rigid workflows:** Allow flexibility for unexpected user needs
❌ **Excessive background:** Stick to actionable information
❌ **Incorrect brace escaping:** Avoid using single braces `{}` in code samples instead of double braces `{{}}`

### Anti-Pattern: Missing Brace Escaping

**❌ Problem Example:**
```markdown
## Python Code Pattern
```python
# This will cause KeyError!
result = {"key": "value"}
print(f"Total: {amount}")
for item in {1, 2, 3}:
    track_calculation("id", {value})
```
```

**Why it fails:**
- Template system tries to replace `{key}`, `{amount}`, `{1, 2, 3}`, `{value}`
- Raises `KeyError` when these variables don't exist in template context
- Agent initialization fails before it can even start

**✅ Correct Version:**
```markdown
## Python Code Pattern
```python
# Properly escaped
result = {{"key": "value"}}
print(f"Total: {{amount}}")
for item in {{1, 2, 3}}:
    track_calculation("id", {{value}})
```
```

**Impact:** This is a CRITICAL error that prevents the prompt from loading. Always use double braces in code samples.

## Recommended Prompt Patterns

These patterns from Anthropic's Claude 4 guidance can be embedded in system prompts to improve agent behavior.

### Pattern 1: Default to Action

Use when you want the agent to implement changes rather than just suggest them.

```xml
<default_to_action>
By default, implement changes rather than only suggesting them.
If the user's intent is unclear, infer the most useful likely action and proceed.
</default_to_action>
```

**When to use:**
- Coding assistants that should write code, not just explain
- Automation agents that should execute tasks
- Agents where users expect direct action

**When NOT to use:**
- High-stakes decisions requiring user confirmation
- Destructive operations
- Situations where wrong actions are costly

### Pattern 2: Investigate Before Answering

Use to prevent hallucination and ensure grounded responses.

```xml
<investigate_before_answering>
Never speculate about code you have not opened.
Always read relevant files before answering.
</investigate_before_answering>
```

**When to use:**
- Code analysis agents
- Research agents working with documents
- Any agent where accuracy is critical

**Variations:**
```xml
<verify_before_claiming>
Before making claims about data, always query the source.
Do not assume values or states - verify them first.
</verify_before_claiming>
```

### Pattern 3: Incremental Progress (for complex tasks)

Use when agents handle multi-step or long-running tasks.

```xml
<incremental_progress>
Break complex tasks into smaller steps.
Complete and verify each step before proceeding.
Track progress explicitly and save state when appropriate.
</incremental_progress>
```

**When to use:**
- Multi-step workflow agents
- Agents handling complex analysis
- Long-running task executors

### Combining Patterns

Patterns can be combined based on agent needs:

```markdown
## Behavior
<behavior>
<default_to_action>
Implement changes directly rather than suggesting them.
</default_to_action>

<investigate_before_answering>
Always read files before making claims about their contents.
</investigate_before_answering>

<incremental_progress>
For complex tasks, break into steps and verify each before proceeding.
</incremental_progress>
</behavior>
```

**Note:** Only include patterns relevant to your agent's use case. Don't add patterns "just in case."

**When to use additional patterns** → See `references/claude4-prompt-patterns.md`
- Agent should **suggest instead of implement** → `<do_not_act_before_instructions>`
- Need **parallel tool execution** optimization → `<use_parallel_tool_calls>`
- Want **prose output** instead of bullet points → `<avoid_excessive_markdown>`
- Prevent **over-engineering** in code agents → `<avoid_over_engineering>`
- Building **frontend/web UI** with distinctive design → `<frontend_aesthetics>`

## Domain-Specific System Prompt Patterns

Different agent types benefit from different prompt structures. Use these patterns as starting points.

### Coordinator/Router Agents

**Focus on:**
- Handoff criteria and decision logic
- Context summarization for specialists
- Response synthesis from multiple agents
- Minimal direct task execution

**Key Sections:**
- Role and orchestration objective
- Handoff criteria (when to delegate vs. handle directly)
- Context summarization guidelines
- Response synthesis patterns

**Example Agent Types:**
- Multi-agent coordinator
- Task router
- Workflow orchestrator

**Template Pattern:**
```markdown
## Role
<role>
You are a [coordinator type]. Route requests to specialists and synthesize responses.
</role>

## Handoff Criteria
<handoff_criteria>
Delegate to [Specialist A] when: [conditions]
Delegate to [Specialist B] when: [conditions]
Handle directly when: [conditions]
</handoff_criteria>

## Instructions
<instructions>
- Analyze request to identify appropriate specialist
- Provide specialist with clear, contextualized task
- Synthesize outputs without exposing internal architecture
</instructions>
```

### Planner/Reasoning Agents

**Focus on:**
- Problem decomposition strategies
- Plan structure and detail level
- Reasoning depth and extended thinking
- Dependency identification

**Key Sections:**
- Planning methodology
- Plan output format
- Reasoning guidelines
- Success criteria for plans

**Example Agent Types:**
- Strategic planner
- Task decomposer
- Workflow designer

**Template Pattern:**
```markdown
## Role
<role>
You are a strategic planner. Break complex requests into executable plans.
</role>

## Planning Methodology
<methodology>
- Analyze goals and constraints
- Identify required tools and dependencies
- Create atomic, actionable steps
- Anticipate failure modes
</methodology>

## Plan Structure
<plan_structure>
For each step:
1. Action description
2. Tool(s) to use
3. Expected inputs/outputs
4. Success criteria
</plan_structure>
```

### Execution/Worker Agents

**Focus on:**
- Tool usage and execution safety
- Error handling and recovery
- Output formatting and artifact management
- Validation before execution

**Key Sections:**
- Execution capabilities
- Safety constraints
- Error handling strategy
- Output artifact management

**Example Agent Types:**
- Code executor
- Data analyzer
- File processor

**Template Pattern:**
```markdown
## Role
<role>
You are a code execution specialist. Run Python/bash commands safely and return results.
</role>

## Capabilities
<capabilities>
- Execute Python in REPL environment
- Run bash commands for file operations
- Handle errors gracefully
- Save artifacts to designated locations
</capabilities>

## Safety Constraints
<constraints>
- Validate inputs before execution
- Never execute potentially harmful code
- Confirm destructive operations
- Respect file system boundaries
</constraints>
```

### Report/Content Generation Agents

**Focus on:**
- Content structure and formatting
- Visualization integration
- Style and tone consistency
- Multi-format output

**Key Sections:**
- Report structure templates
- Formatting standards
- Quality criteria
- Output format specifications

**Example Agent Types:**
- Report generator
- Documentation writer
- Presentation creator

**Template Pattern:**
```markdown
## Role
<role>
You are a report generation specialist. Create comprehensive, well-formatted reports.
</role>

## Report Structure
<structure>
Standard sections:
1. Executive Summary
2. Findings/Analysis
3. Visualizations
4. Conclusions/Recommendations
</structure>

## Formatting Standards
<formatting>
- Use consistent heading levels
- Label all charts and tables
- Keep paragraphs concise (3-5 sentences)
- Use bullet points for key findings
</formatting>
```

### Research/Information Gathering Agents

**Focus on:**
- Source evaluation criteria
- Information synthesis
- Citation and attribution
- Confidence level communication

**Key Sections:**
- Search strategy
- Source credibility evaluation
- Synthesis guidelines
- Citation format

**Example Agent Types:**
- Web researcher
- Knowledge synthesizer
- Fact checker

**Template Pattern:**
```markdown
## Role
<role>
You are a research specialist. Gather, synthesize, and present information from sources.
</role>

## Search Strategy
<search_strategy>
1. Formulate specific queries
2. Evaluate source authority and recency
3. Cross-reference across multiple sources
4. Synthesize findings coherently
</search_strategy>

## Source Evaluation
<evaluation_criteria>
- Authority: Is source credible?
- Recency: Is information current?
- Relevance: Does it address the question?
- Objectivity: Is there evident bias?
</evaluation_criteria>
```

## Validation Checklist

Before finalizing your system prompt, verify:

**Scope & Purpose:**
- [ ] Role and objective are crystal clear
- [ ] Agent responsibilities are well-defined
- [ ] Scope boundaries are explicit (what's in/out of scope)

**Content Quality:**
- [ ] Every sentence is necessary (no fluff or redundancy)
- [ ] Instructions are at the "right altitude" (not too rigid, not too vague)
- [ ] Minimum effective information principle applied
- [ ] No over-specification of procedures
- [ ] Domain-specific knowledge included where needed

**Structure & Organization:**
- [ ] Sections are clearly delineated (Markdown + XML hybrid)
- [ ] Logical flow from general to specific
- [ ] Related information grouped together
- [ ] Supporting files properly referenced (examples.md, etc.)

**Template Variable Escaping (CRITICAL):**
- [ ] All template variables use single braces: `{CURRENT_TIME}`, `{USER_REQUEST}`, etc.
- [ ] All code samples with braces use double braces: `{{value}}`, `{{"key": "val"}}`
- [ ] Python f-strings in examples use double braces: `f"Count: {{n}}"`
- [ ] JSON/dict examples use double braces: `{{"name": "John"}}`
- [ ] Tested prompt loading to verify no KeyError exceptions

**Tool Guidance:**
- [ ] Tool usage conditions are unambiguous
- [ ] Decision criteria for tool selection are clear
- [ ] No reliance on vague phrases like "use appropriately"
- [ ] Tool prerequisites and constraints specified

**Examples & Patterns:**
- [ ] 2-3 diverse, canonical examples included (if needed)
- [ ] Examples demonstrate behavior patterns, not edge case enumeration
- [ ] Good vs. bad examples show anti-patterns
- [ ] Template patterns provided for common scenarios

**Context Management:**
- [ ] Supports long conversations (compaction strategy if needed)
- [ ] Just-in-time loading strategy considered
- [ ] No premature context optimization

**Completeness:**
- [ ] Success criteria are explicit
- [ ] Constraints and boundaries defined
- [ ] Error handling guidance included
- [ ] Handoff/escalation criteria clear (for multi-agent systems)

## Template: Basic System Prompt

Use this Hybrid (Markdown + XML) template for most agents:

```markdown
## Role
<role>
You are [specific role]. Your objective is to [clear goal].
</role>

## Capabilities (optional - include only if needed)
<capabilities>
You can:
- [Capability 1]
- [Capability 2]
- [Capability 3]
</capabilities>

## Instructions
<instructions>
- [Key principle 1]
- [Key principle 2]
- When [situation], do [action]
</instructions>

## Tool Guidance
<tool_guidance>
- tool_name: Use when [specific condition]
- tool_name_2: Use when [specific condition]
</tool_guidance>

## Success Criteria
<success_criteria>
- [Criterion 1]
- [Criterion 2]
</success_criteria>

## Constraints
<constraints>
- Do not [constraint 1]
- Always [requirement 1]
</constraints>
```

## Template: Advanced Multi-Agent System Prompt

Use this template for complex agents in multi-agent systems:

```markdown
## Agent Identity
<identity>
Name: [agent_name]
Type: [coordinator|specialist|worker]
Domain: [area of expertise]
</identity>

## Objective
<objective>
[Clear, measurable goal for this agent]
</objective>

## Context Management
<context_management>
- Maintain working memory in: [location]
- Compaction trigger: [condition]
- Just-in-time loading: [strategy]
</context_management>

## Communication Protocol
<communication_protocol>
Input format: [expected structure from other agents]
Output format: [required structure to send to other agents]
Handoff criteria: [when and how to transfer to other agents]
</communication_protocol>

## Decision Framework
<decision_framework>
When [condition_1]: [action_1]
When [condition_2]: [action_2]
Default: [fallback behavior]
</decision_framework>

## Tool Guidance
<tool_guidance>
[tool_name]:
  - Use when: [specific condition]
  - Input: [expected parameters]
  - Output: [what to expect]
</tool_guidance>

## Success Criteria
<success_criteria>
- [Measurable criterion 1]
- [Measurable criterion 2]
</success_criteria>

## Error Handling
<error_handling>
If [error_type]: [recovery_action]
Escalation criteria: [when to ask for help or hand off]
</error_handling>

## Constraints
<constraints>
- [Boundary 1]
- [Boundary 2]
</constraints>
```

## Example: Data Analysis Agent Prompt

This example demonstrates the Hybrid approach in practice:

```markdown
## Role
<role>
You are a data analysis specialist. Your objective is to help users derive insights from their datasets through statistical analysis and visualization.
</role>

## Instructions
<instructions>
- Always validate data quality before analysis
- Explain statistical concepts in plain language
- Provide both numbers and narrative insights
- Suggest appropriate analysis methods based on data characteristics
- Be transparent about limitations and assumptions
</instructions>

## Tool Guidance
<tool_guidance>
- load_dataset(path): Use when user provides a file path or URL
- analyze_statistics(data, metrics): Use for numerical summaries and descriptive stats
- create_visualization(data, chart_type, params): Use to generate charts and plots
- python_repl(code): Use for custom analysis not covered by other tools

Decision Framework:
- Exploratory questions → Start with descriptive statistics and basic plots
- Hypothesis testing → Verify assumptions, then apply appropriate test
- Predictive modeling → Assess data suitability, then recommend approach
- Custom requests → Use python_repl for flexibility
</tool_guidance>

## Success Criteria
<success_criteria>
- Analysis directly addresses user's question
- Results are statistically sound and properly interpreted
- Visualizations are clear and appropriately labeled
- Insights are actionable and clearly communicated
</success_criteria>

## Constraints
<constraints>
- Do not run analysis on incomplete or corrupted data without warning
- Always state confidence levels and statistical significance
- Respect privacy - do not persist or share user data
- Acknowledge when sample size is too small for reliable inference
</constraints>
```

## References and Further Reading

- Anthropic: "Effective Context Engineering for AI Agents" (2025)
- Anthropic: "Prompt Engineering Guide"
- Key principle: Context is king - engineer it, don't just prompt it

---

## Iterative Development Approach

**Anthropic's Recommendation:**
> "It's best to start by testing a minimal prompt with the best model available to see how it performs on your task, and then add clear instructions and examples to improve performance based on failure modes found during initial testing."

### The Development Cycle

```
1. Start Minimal
   ↓
2. Test with Best Model
   ↓
3. Identify Failure Modes
   ↓
4. Add Targeted Instructions/Examples
   ↓
5. Re-test and Measure
   ↓
[Repeat 3-5 until acceptable performance]
```

### Step-by-Step Process

**Step 1: Start Minimal**
- Begin with the simplest possible prompt
- Include only: role, objective, and essential context
- Don't preemptively add instructions for problems you haven't seen

**Example Minimal Start:**
```markdown
You are a customer service agent for TechCorp. Help customers with product questions, orders, and account issues.
```

**Step 2: Test with Best Model**
- Use the most capable model available (e.g., Claude Sonnet 3.7)
- Run the agent through representative scenarios
- Document what works and what doesn't

**Step 3: Identify Failure Modes**
- What specific tasks does the agent struggle with?
- Where does it make wrong decisions?
- When does it fail to use tools appropriately?
- What edge cases does it handle poorly?

**Step 4: Add Targeted Improvements**

Based on failure modes, add:
- **Instructions** for consistent behavior issues
- **Examples** for output quality or format problems
- **Tool guidance** for incorrect tool selection
- **Constraints** for undesired behaviors

**Example Evolution:**
```markdown
# After finding failure: Agent doesn't escalate complex issues
→ Add instruction: "Escalate to specialist when issue requires engineering knowledge"

# After finding failure: Agent is too brief
→ Add example showing detailed, helpful response

# After finding failure: Agent uses wrong tool
→ Add tool decision tree
```

**Step 5: Measure and Iterate**
- Re-run tests on same scenarios
- Verify improvements without regressions
- Continue cycle until acceptable performance

### Key Principles

✅ **Start simple** - Don't over-engineer before you know what's needed
✅ **Test early** - Identify real problems, not imagined ones
✅ **Be targeted** - Add instructions that address specific failure modes
✅ **Measure impact** - Ensure each change improves performance
✅ **Avoid bloat** - If an instruction doesn't fix a real problem, remove it

### Example Iteration Journey

**Version 1 (Minimal):**
```
You are a data analyst. Help users analyze their datasets.
```
*Failure: Unclear how to handle missing data*

**Version 2 (After Testing):**
```
You are a data analyst. Help users analyze their datasets.

When encountering missing data:
- Notify the user
- Suggest handling strategies (removal, imputation, etc.)
- Ask for user preference before proceeding
```
*Failure: Uses wrong statistical tests*

**Version 3 (After More Testing):**
```
You are a data analyst. Help users analyze their datasets.

When encountering missing data:
- Notify the user and suggest handling strategies
- Ask for preference before proceeding

Statistical Test Selection:
- Comparing 2 groups (normal distribution) → t-test
- Comparing 2 groups (non-normal) → Mann-Whitney U
- Comparing 3+ groups → ANOVA or Kruskal-Wallis
```
*Good performance achieved*

Notice: Each addition solves a real, observed problem.

---

## Overall Context Engineering Guidance

**Anthropic's Holistic Principle:**
> "Our overall guidance across the different components of context (system prompts, tools, examples, message history, etc) is to be thoughtful and keep your context **informative, yet tight**."

### The Complete Context Picture

Context consists of multiple components:
1. **System Prompts** - Role, instructions, guidelines
2. **Tools** - Available actions and their descriptions
3. **Examples** - Few-shot demonstrations
4. **Message History** - Conversation so far
5. **External Data** - Retrieved documents, database results
6. **Working Memory** - Intermediate state, notes

### Optimization Across All Components

**For Each Component, Ask:**
- Is this information high-signal for the current task?
- Can this be loaded just-in-time instead of upfront?
- Is there redundancy with other components?
- Does this guide behavior or just add noise?

**System Prompts ↔ Tools:**
- Don't repeat tool functionality in prompt
- Tools have descriptions - reference them, don't duplicate
- Prompt should guide WHEN to use tools, not HOW (that's in tool description)

**System Prompts ↔ Examples:**
- Use examples to show, not just tell
- Good examples can replace paragraphs of instructions
- Examples should demonstrate the range, not every edge case

**Tools ↔ External Data:**
- Tools should return token-efficient data
- Load full documents only when needed
- Summarize or extract relevant portions

**Message History Management:**
- Compact or summarize old messages when context grows
- Preserve critical decisions and preferences
- Archive detailed history outside main context

### The "Informative Yet Tight" Mantra

**Informative:**
- Agent has what it needs to succeed
- Critical context is present
- Decision-making criteria are clear

**Yet Tight:**
- No redundancy across components
- No low-signal information
- Just-in-time loading where possible
- Regular pruning and compaction

Think of context budget like RAM in a computer - finite, precious, and requiring active management.

---

## Skill Organization and Supporting Files

This skill uses a multi-file structure for comprehensive coverage:

### Main SKILL.md (This File)
Contains core principles, guidelines, templates, and patterns for writing system prompts. Use this as your primary reference.

### references/examples.md
Provides complete real-world examples of system prompts across different agent types:
- Coordinator agents
- Planner agents
- Code execution agents
- Report generation agents
- Research agents
- Customer service agents
- Security-aware agents
- Before/after optimization examples

**When to use:** Need concrete examples to understand patterns or inspire your own prompts.

### references/section-organization-guide.md
Deep-dive into structuring system prompts with detailed section-by-section recommendations:
- Recommended section types (Role, Instructions, Tool Guidance, etc.)
- Section formatting patterns
- Hybrid (Markdown + XML) approach details
- Section ordering guidelines
- Common organization mistakes

**When to use:** Need detailed guidance on organizing and structuring complex prompts.

## Using This Skill

Follow this process when writing a system prompt:

### Step 1: Identify Agent Type
Determine which domain-specific pattern fits your use case:
- **Coordinator:** Routing and orchestration
- **Planner:** Strategic thinking and decomposition
- **Executor:** Code/command execution
- **Reporter:** Content and report generation
- **Researcher:** Information gathering and synthesis

### Step 2: Start with Template
Choose the appropriate template:
- **Basic template** (from this file) - for simple agents
- **Advanced template** (from this file) - for complex multi-agent systems
- **Domain-specific template** (from Domain-Specific Patterns section)

### Step 3: Apply Core Principles
Apply these principles when writing:
- **Right altitude:** Balance specificity with flexibility
- **Minimum effective information:** Cut ruthlessly, keep high-signal content
- **Clear structure:** Use Markdown + XML hybrid format
- **Unambiguous tool guidance:** Provide clear decision criteria
- **Few-shot examples:** 2-3 diverse, canonical examples (if needed)
- **CRITICAL - Template escaping:** Use double braces `{{}}` in ALL code samples, single braces `{}` only for template variables

### Step 4: Follow Iterative Development
Avoid attempting perfection on first draft:
1. Start minimal (role + basic instructions)
2. Test with best available model
3. Identify specific failure modes
4. Add targeted improvements (instructions, examples, tool guidance)
5. Re-test and measure impact
6. Repeat until acceptable performance

### Step 5: Validate
Use the comprehensive checklist in this file to ensure:
- Scope is clear
- Content quality is high
- Structure is organized
- Tool guidance is unambiguous
- Examples are effective
- Context management is considered

### Step 6: Reference Supporting Files
- **Need examples?** → See `references/examples.md`
- **Complex structure questions?** → See `references/section-organization-guide.md`
- **Template starting point?** → Use templates in this file

### Quick Reference: When to Use What

| Scenario | Reference |
|----------|-----------|
| Starting a new prompt | Templates section (this file) |
| Understanding section organization | references/section-organization-guide.md |
| Seeing real-world examples | references/examples.md |
| Writing tool guidance | Tool Guidance section (this file) |
| Adding few-shot examples | Few-Shot Prompting section (this file) |
| Optimizing context usage | Context Management Strategies (this file) |
| Multi-agent systems | Domain-Specific Patterns → Coordinator/Planner |

## Key Principles Summary

Remember these core tenets:

1. **Context Engineering over Prompt Engineering**
   - Find the minimum effective dose of information
   - High-signal tokens, not arbitrary brevity

2. **Start Minimal, Iterate Based on Failures**
   - Don't preemptively solve imagined problems
   - Add complexity only when tests reveal the need

3. **Structure for Clarity**
   - Use Markdown + XML hybrid format
   - Clear section boundaries help both humans and LLMs

4. **Unambiguous Tool Guidance**
   - If a human can't decide which tool to use, neither can an AI
   - Provide explicit decision criteria

5. **Curate Examples, Don't Enumerate**
   - 2-3 diverse, canonical examples beat 20 edge cases
   - Teach behavior patterns, not memorized responses

6. **Informative Yet Tight**
   - Sufficient information to succeed
   - No redundancy, no low-signal content
   - Active context management

7. **CRITICAL: Template Variable Escaping**
   - Double braces `{{}}` in ALL code samples
   - Single braces `{}` ONLY for template variables like `{CURRENT_TIME}`
   - Missing escaping causes KeyError and prevents prompt loading

The goal is not perfection, but **effectiveness** - prompts should work while leaving maximum context space for dynamic information that matters.