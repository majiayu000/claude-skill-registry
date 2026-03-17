---
name: agent-design
description: Guidelines for designing tools and action spaces for AI agents. Use when building agent harnesses, designing tool interfaces, creating elicitation mechanisms, or optimizing agent-tool interactions. Covers progressive disclosure, tool design patterns, and lessons from Claude Code development.

---

# Agent Design Guidelines

## Overview

Designing tools for AI agents is as much art as science. The key principle: **give agents tools shaped to their own abilities** — which you discover by paying attention to their outputs.

### The Mental Model

Imagine being given a difficult math problem. What tools would you want?

| Tool | Limitation |
|------|------------|
| Paper only | Limited by manual calculations |
| Calculator | Better, but requires knowledge to operate |
| Computer | Most powerful, but requires coding skills |

The right tool depends on **your own abilities**. Same for agents — design tools that match what the model can actually do well.

## Core Principles

### 1. Claude Must "Like" Calling the Tool

Even the best designed tool doesn't work if Claude doesn't understand how to call it.

- Test if the model naturally uses the tool
- Read outputs to see if it's confused
- Iterate on the interface until it "clicks"

### 2. Tools That Were Necessary Can Become Constraints

As models improve:
- Old workarounds become unnecessary
- Previous "helps" become limitations
- Constantly revisit assumptions

**Example:** TodoWrite reminders helped older models but made newer ones think they couldn't modify the list.

### 3. Progressive Disclosure Over Context Bloat

Instead of stuffing everything in the system prompt:
- Give agents tools to discover context themselves
- Let them search, read, and explore recursively
- Skills can reference other files for nested discovery

### 4. High Bar for New Tools

More tools = more options to think about = cognitive overhead.

- Claude Code has ~20 tools
- Consider: can this be a subagent? A skill? Progressive disclosure?
- Only add tools when truly necessary

## Design Patterns

### Pattern: Structured Elicitation (AskUserQuestion)

**Problem:** Claude asking questions in plain text was slow and unstructured.

**Failed Attempts:**
1. Adding questions to another tool's output → confused the model
2. Modified markdown format → unreliable output

**Solution:** Dedicated tool with:
- Structured input (question + options)
- Modal UI that blocks until answered
- Clear prompt about when to call it

**Key insight:** Claude "liked" calling this tool — the interface matched how it naturally thinks about asking questions.

### Pattern: Task Coordination (Task Tool)

**Evolution from TodoWrite:**
- TodoWrite was for keeping the model on track
- Task Tool is for subagent coordination
- Tasks have dependencies, can be shared, modified, deleted

**When to use:** When multiple agents need to coordinate on shared state.

### Pattern: Context Building (Search Tools)

**Evolution:**
1. RAG → fast but fragile, context was given not found
2. Grep tool → let Claude search directly
3. Skills → progressive disclosure through file references

**Key insight:** As models get smarter, they become better at building their own context if given the right tools.

### Pattern: Capability Without Tools (Subagents)

**Problem:** Claude didn't know about itself (MCP, slash commands, etc.)

**Failed approach:** Put docs in system prompt → context rot

**Solution:** Claude Code Guide subagent
- Prompted to call when users ask about Claude Code
- Has extensive instructions on searching docs
- Adds capability without adding a tool

## Tool Design Checklist

Before adding a tool, ask:

1. **Can this be progressive disclosure?**
   - A skill that references files?
   - A subagent with specialized instructions?

2. **Does Claude naturally want to call this?**
   - Test with real scenarios
   - Read the outputs carefully

3. **Is this solving a real problem?**
   - Or is it a workaround for model limitations that may improve?

4. **How many tools will this make?**
   - Is the cognitive overhead worth it?

5. **Will this age well?**
   - As models improve, will this still be useful?
   - Or will it become a constraint?

## Anti-Patterns

### Anti-Pattern: Overloading Tool Purpose

```markdown
# BAD: Asking for plan AND questions in same tool
ExitPlanTool(plan: string, questions: Question[])

# GOOD: Separate tools for separate purposes
ExitPlanTool(plan: string)
AskUserQuestion(questions: Question[])
```

### Anti-Pattern: Relying on Output Format

```markdown
# BAD: Hoping model outputs specific format
"Output questions in this format: - Question [Option A | Option B]"

# GOOD: Structured tool input
AskUserQuestionTool({
  questions: [{
    question: "...",
    options: ["A", "B"]
  }]
})
```

### Anti-Pattern: Static Context

```markdown
# BAD: Everything in system prompt
"You have access to MCP servers, here's how to configure them..."

# GOOD: Progressive disclosure
"You can call the claude-code-guide agent to learn about Claude Code features"
```

## Practical Tips

### See Like an Agent

1. **Read the outputs** — What confused the model? What did it do naturally?
2. **Experiment often** — Try different tool shapes
3. **Watch for patterns** — Is the model working around your tools?

### Iterate on Tool Interfaces

The first design rarely works. Expect:
- 2-3 iterations minimum
- Testing with real use cases
- Adjusting based on model behavior

### Model Capabilities Change

What works for Claude 3.5 may not work for Claude 4:
- Revisit tool designs with new models
- Remove tools that are no longer needed
- Don't optimize for old model limitations

## Reference

**Source:** [Claude Code Team Learnings](https://x.com/trq212/status/2027463795355095314)

**Related Concepts:**
- Tool calling / Function calling
- Progressive disclosure
- Subagent coordination
- Context building
- Elicitation patterns
