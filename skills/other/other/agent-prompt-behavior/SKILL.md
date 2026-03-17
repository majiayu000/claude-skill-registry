---
name: agent-prompt-behavior
description: |
  Design agent system prompts with explicit behavior rules and cognitive control.
  This skill should be used when users need to define agent instructions,
  create intent-to-tool mappings, establish confirmation policies, or prevent
  hallucinated actions in AI agents.
---

# Agent Prompt & Behavior

Build system prompts that provide deterministic cognitive control over AI agents.

## What This Skill Does

- Design agent system instructions with explicit behavior rules
- Create intent-to-tool mapping tables (what user says → what agent does)
- Define confirmation policies (when to ask before acting)
- Establish error handling behaviors
- Prevent hallucinated actions through grounding rules
- Generate complete, production-ready system prompts

## What This Skill Does NOT Do

- Implement the agent runtime/executor
- Handle conversation state management
- Define API contracts or schemas
- Deploy or test agents

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Available tools, existing prompts, agent framework |
| **Conversation** | Agent's purpose, domain, user types |
| **Skill References** | Prompt patterns, mapping rules, safety policies |
| **User Guidelines** | Tone, brand voice, compliance requirements |

---

## Core Principle: Cognitive Control

**The system prompt is the agent's brain.** It determines:

```
┌─────────────────────────────────────────────────────────────┐
│                    COGNITIVE CONTROL                        │
├─────────────────────────────────────────────────────────────┤
│  IDENTITY      │ Who am I? What's my purpose?              │
│  CAPABILITIES  │ What tools can I use? What can't I do?    │
│  BEHAVIOR      │ How do I respond? When do I confirm?      │
│  GROUNDING     │ What prevents me from hallucinating?      │
│  ERRORS        │ How do I handle failures gracefully?      │
└─────────────────────────────────────────────────────────────┘
```

---

## Required Clarifications

Before building the system prompt, clarify:

### 1. Agent Identity
- **Purpose**: What is this agent for? (task assistant, customer support, code helper)
- **Domain**: What domain knowledge is needed?
- **Persona**: Any personality traits or tone requirements?

### 2. Available Tools
- **Tool list**: What tools/functions can the agent call?
- **Tool descriptions**: What does each tool do?
- **Tool constraints**: Any usage limits or conditions?

### 3. Safety Requirements
- **Destructive actions**: Which actions need confirmation?
- **Forbidden actions**: What must the agent never do?
- **Scope limits**: What's out of scope?

### 4. Error Policy
- **Failure modes**: How should the agent handle tool failures?
- **Ambiguity**: What if user intent is unclear?
- **Escalation**: When should agent defer to human?

---

## System Prompt Architecture

A complete system prompt has 6 sections:

```
┌─────────────────────────────────────────┐
│ 1. IDENTITY & PURPOSE                   │
│    Who you are, what you do             │
├─────────────────────────────────────────┤
│ 2. CAPABILITIES & TOOLS                 │
│    What you CAN do (explicit list)      │
├─────────────────────────────────────────┤
│ 3. BOUNDARIES & CONSTRAINTS             │
│    What you CANNOT do (explicit list)   │
├─────────────────────────────────────────┤
│ 4. INTENT → TOOL MAPPING                │
│    How to interpret user requests       │
├─────────────────────────────────────────┤
│ 5. CONFIRMATION POLICY                  │
│    When to ask before acting            │
├─────────────────────────────────────────┤
│ 6. ERROR HANDLING                       │
│    How to handle failures gracefully    │
└─────────────────────────────────────────┘
```

See `assets/system-prompt-template.md` for complete template.

---

## Intent-to-Tool Mapping

The most critical section. Maps natural language → deterministic action.

### Mapping Table Format

```markdown
## Intent Mapping

| User Says (Intent) | Tool to Call | Parameters | Confirmation |
|--------------------|--------------|------------|--------------|
| "create a task" | create_task | title, description | No |
| "delete task X" | delete_task | task_id | Yes |
| "show my tasks" | list_tasks | user_id | No |
| "mark X as done" | update_task | task_id, completed=true | No |
```

### Mapping Rules

1. **Be exhaustive**: List ALL supported intents
2. **Be specific**: Avoid ambiguous mappings
3. **Include variations**: "delete", "remove", "get rid of" → same tool
4. **Mark confirmations**: Destructive actions need confirmation

See `references/intent-mapping.md` for patterns and examples.

---

## Confirmation Policy

### Actions Requiring Confirmation

| Category | Examples | Why Confirm |
|----------|----------|-------------|
| **Destructive** | Delete, remove, cancel | Irreversible |
| **Financial** | Purchase, transfer, refund | Real money |
| **External** | Send email, post message | Visible to others |
| **Bulk** | Delete all, update all | Large impact |

### Confirmation Format

```
Before I [action], let me confirm:
- [Detail 1]
- [Detail 2]

Proceed? (yes/no)
```

See `references/confirmation-policy.md` for implementation.

---

## Grounding Rules (Prevent Hallucination)

**Critical**: The agent must ONLY use tools it actually has.

### Grounding Principles

```markdown
## Grounding Rules

1. ONLY call tools listed in your capabilities
2. NEVER invent tool names or parameters
3. If no tool matches the request, say so clearly
4. NEVER claim to have done something you didn't do
5. If a tool call fails, report the failure honestly
```

### Unknown Intent Handling

```markdown
When you receive a request you cannot fulfill:

1. Acknowledge the request
2. Explain what you CAN do instead
3. Offer alternatives if available
4. Never pretend or hallucinate capabilities
```

---

## Error Handling Behavior

### Error Response Pattern

```markdown
## When Tools Fail

If a tool returns an error:
1. Do NOT retry automatically (unless specified)
2. Explain what happened in plain language
3. Suggest what the user can do
4. Offer to try an alternative approach

Example:
"I tried to create the task, but the database returned an error.
This might be a temporary issue. Would you like me to try again,
or would you prefer to wait a few minutes?"
```

### Graceful Degradation

```markdown
## Graceful Degradation

If you cannot complete a request:
1. Complete as much as possible
2. Clearly state what succeeded and what failed
3. Provide partial results if available
4. Suggest next steps
```

See `references/error-handling.md` for patterns.

---

## Workflow: Building a System Prompt

```
1. CLARIFY
   └─→ Gather identity, tools, safety requirements

2. ENUMERATE TOOLS
   └─→ List all available tools with descriptions

3. MAP INTENTS
   └─→ Create intent → tool mapping table

4. DEFINE BOUNDARIES
   └─→ List forbidden actions and scope limits

5. SET CONFIRMATION POLICY
   └─→ Mark which actions need confirmation

6. ADD ERROR HANDLING
   └─→ Define failure responses

7. ASSEMBLE PROMPT
   └─→ Use template to create complete prompt

8. VALIDATE
   └─→ Check for gaps, ambiguities, conflicts
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Vague capabilities | "Help with tasks" | List specific tools |
| Missing boundaries | Agent tries anything | Explicit "do not" list |
| No confirmation | Destroys data silently | Confirm destructive actions |
| Silent failures | User thinks it worked | Always report errors |
| Invented tools | Hallucinated actions | Grounding rules |
| Ambiguous mapping | Wrong tool called | Specific intent patterns |

---

## Output Checklist

Before delivering a system prompt:

- [ ] Identity section defines purpose clearly
- [ ] All available tools listed with descriptions
- [ ] Intent → tool mapping is exhaustive
- [ ] Boundaries and forbidden actions explicit
- [ ] Confirmation policy covers destructive actions
- [ ] Error handling defined for all failure modes
- [ ] Grounding rules prevent hallucination
- [ ] Unknown intent handling specified
- [ ] Tone and persona consistent throughout

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/system-prompt-patterns.md` | Prompt structure and examples |
| `references/intent-mapping.md` | Intent recognition and mapping rules |
| `references/confirmation-policy.md` | When and how to confirm actions |
| `references/error-handling.md` | Failure modes and responses |
| `assets/system-prompt-template.md` | Complete template to fill in |
