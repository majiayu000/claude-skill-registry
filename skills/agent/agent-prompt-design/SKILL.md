---
name: agent-prompt-design
description: Create well-structured prompts for AI agents using proven architecture patterns. Use when users ask to write agent prompts, system prompts, or agent instructions, or want to improve existing prompts that aren't working.
---

# Agent Prompt Design

## Process

### Phase 1: Gather Requirements

Collect the following before drafting:

**Required:**
- Agent's purpose and role (what it does)
- Available tools and their capabilities
- Primary tasks the agent should perform

**If improving an existing prompt:**
- Current prompt text
- Specific failures or problems observed
- Example queries that don't work well

### Phase 2: Draft the Prompt Structure

Build the prompt with these five components in order:

#### 2.1 Role Definition
Write 1-2 sentences establishing identity and function.

```
You are a [role] that [primary function]. Your goal is to [main objective].
```

#### 2.2 Dynamic Content Section
Add placeholders for context that will be injected at runtime. Focus on domain-specific data the framework won't provide automatically:

```
## Current Context
- User: {{user_name}}
- Account type: {{account_tier}}
- Permissions: {{user_permissions}}
```

Note: Conversation history and tool definitions are typically handled by the framework—don't include them unless the system requires manual injection.

#### 2.3 Detailed Instructions
Write step-by-step behavioral guidance. Be specific about:
- What to do first when receiving a request
- How to handle common scenarios
- When to use which tools
- What format to use for responses

#### 2.4 Examples (Optional)
Include only if the task has non-obvious output formats. Keep examples minimal—frontier models don't need extensive few-shot demonstrations.

#### 2.5 Critical Reminders
For prompts longer than ~500 words, repeat the most important rules at the end. Models pay more attention to the beginning and end of prompts.

### Phase 3: Add Explicit Heuristics

Identify domain-specific decisions the agent must make and write explicit rules for each.

**Questions to answer:**
- What actions are irreversible? → Add confirmation requirements
- What does "good enough" mean? → Define stopping conditions
- What are the resource limits? → Set budgets (API calls, searches, time)
- What happens when goals conflict? → Define priority order
- When should the agent ask vs. decide? → Set autonomy boundaries

**Transform vague instructions into explicit rules:**

| Vague | Explicit |
|-------|----------|
| "Search for relevant documents" | "Search up to 3 times. If no relevant results after 3 searches, ask the user to clarify." |
| "Make sure the data is accurate" | "Cross-reference data from at least 2 sources before presenting to user." |
| "Be thorough" | "For simple questions, use 1-2 tool calls. For complex analysis, use up to 10." |

### Phase 4: Handle Tool Usage

Add guidance for how the agent should use its tools.

**For agents with MCP servers or dynamic tools:**
Tools are loaded automatically with their own descriptions. Focus on:
- When to prefer one category of tools over another
- Sequencing guidance (e.g., "read before write", "search before create")
- Domain-specific tool workflows

```
## Tool Usage Guidelines
- Always read existing data before attempting modifications
- Prefer search tools over list tools when looking for specific items
- Use creation tools only after confirming the item doesn't exist
```

**For agents with custom/static tools:**
If tools have overlapping functions or ambiguous names, add explicit selection rules:

```
## When to Use Each Tool
- Use `search_docs` for internal knowledge base queries
- Use `search_web` only when docs don't have the answer
- Use `ask_user` when the query is ambiguous after one search attempt
```

### Phase 5: Add Safety Guardrails

Address potential failure modes in the prompt:

**Loops:** Add stopping conditions
```
If you've attempted the same action 3 times without progress, stop and ask the user for guidance.
```

**Excessive tool use:** Set budgets
```
Limit to 5 tool calls per user request unless explicitly asked for deeper research.
```

**Irreversible actions:** Require confirmation
```
Before deleting, modifying, or sending anything, show the user what will happen and ask for confirmation.
```

**Perfectionism:** Allow "good enough"
```
If perfect information isn't available after reasonable effort, provide the best answer with caveats rather than continuing indefinitely.
```

### Phase 6: Validate the Prompt

Before delivering, verify:

1. **Empathy test:** Read the prompt as if you were the agent with only the described tools and context. Could you follow every instruction unambiguously?

2. **Heuristics check:** Are all domain-specific decisions explicit? No "use your judgment" without criteria.

3. **Architecture check:** All five components present (role, dynamic content, instructions, examples if needed, critical reminders if long)?

4. **Side effects check:** Are irreversible actions, loops, and resource limits addressed?

If any check fails, revise the relevant section.

## Failure Modes to Avoid

**Overcomplicating:** Start simple. Add complexity only when testing reveals gaps.

**Implicit knowledge:** Don't assume the agent knows domain rules. If humans in the field would need training, the agent needs explicit instructions.

**Rigid reasoning:** Don't prescribe exact thought patterns ("First think X, then think Y"). Let the model reason flexibly between tool calls.

**Vague stopping conditions:** "Keep searching until you find it" causes loops. Always define when to stop.
