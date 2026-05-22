---
name: system-prompt-engineering
description: Design effective system prompts for custom agents. Use when creating agent system prompts, defining agent identity and rules, or designing high-impact prompts that shape agent behavior.
allowed-tools: Read, Grep, Glob
---

# System Prompt Engineering Skill

Design effective system prompts for custom agents that establish identity, rules, and behavior.

## Purpose

Create system prompts that shape agent behavior across all conversations. System prompts are orders of magnitude more important than user prompts.

## When to Use

- Creating new custom agents
- Establishing agent expertise
- Defining persistent rules
- Building specialized assistants

## System Prompt vs User Prompt

| Aspect | System Prompt | User Prompt |
| --- | --- | --- |
| Scope | All conversations | Single task |
| Persistence | Affects everything | Per-request |
| Impact | Orders of magnitude higher | Lower blast radius |
| Sections | Purpose, Instructions, Examples | All sections |

## Key Sections

### Purpose (Required)

Define who the agent is and what it does.

```markdown
## Purpose

You are a security expert specializing in code review.
Your role is to identify vulnerabilities and suggest fixes.
You focus on OWASP Top 10 and secure coding practices.
```

**Guidelines:**

- Direct, clear identity statement
- Specific expertise area
- What the agent DOES

### Instructions (Recommended)

Establish rules, constraints, and boundaries.

```markdown
## Instructions

- Focus only on security concerns
- Always explain the reasoning behind findings
- Prioritize issues by severity (Critical, High, Medium, Low)
- Do not modify code without explicit permission
- When uncertain, ask clarifying questions
```

**Guidelines:**

- Bullet points for clarity
- Positive and negative rules
- Edge case handling
- Boundary definition

### Examples (Critical)

Shape behavior through concrete examples.

```markdown
## Examples

### Example 1: SQL Injection Finding
**Input:** "Review this login function"
**Output:** "Found SQL injection vulnerability at line 42. The user input is directly concatenated into the query string. Recommendation: Use parameterized queries instead."

### Example 2: Out of Scope Request
**Input:** "Fix this CSS styling issue"
**Output:** "That's outside my security focus. I specialize in security vulnerabilities, not styling. Consider consulting a frontend expert for CSS issues."

### Example 3: Clean Code
**Input:** "Check this authentication module"
**Output:** "Reviewed the authentication module. No security vulnerabilities found. The code follows secure practices: uses parameterized queries, hashes passwords with bcrypt, and implements rate limiting."
```

**Guidelines:**

- 2-4 diverse examples
- Cover common cases
- Include edge cases
- Show desired output format

## Design Process

### Step 1: Define Agent Identity

Answer:

- What expertise does this agent have?
- What domain does it operate in?
- What is its primary purpose?
- What tone should it use?

### Step 2: Establish Boundaries

Answer:

- What should the agent do?
- What should the agent NOT do?
- When should it ask for clarification?
- What are its limitations?

### Step 3: Create Examples

For each key scenario:

- What's a typical input?
- What's the ideal output?
- How should edge cases be handled?

### Step 4: Validate Design

Check:

- [ ] Purpose is clear and specific
- [ ] Instructions are unambiguous
- [ ] Examples cover key scenarios
- [ ] Boundaries are well-defined
- [ ] Tone is consistent

## What to Avoid

| Avoid | Why | Instead |
| --- | --- | --- |
| Detailed workflows | Reduces autonomy | High-level guidelines |
| Dynamic variables | System prompt is static | Use user prompts |
| Prescriptive formats | Over-constrains | Flexible guidelines |
| Everything "just in case" | Context bloat | Only essentials |

## System Prompt Architecture

```markdown
---
name: agent-name
description: When to use this agent (for auto-delegation)
tools: [minimal tool set]
model: sonnet
color: blue
---

# Agent Name

## Purpose
[Identity and role definition]

## Instructions
[Rules and constraints]

## Examples

### Example 1: [Scenario]
**Input:** [typical input]
**Output:** [ideal output]

### Example 2: [Edge Case]
**Input:** [edge case input]
**Output:** [handling output]

### Example 3: [Boundary]
**Input:** [out-of-scope request]
**Output:** [how to decline/redirect]
```

## Output Format

When designing a system prompt:

```markdown
## System Prompt Design

**Agent Name:** [name]
**Domain:** [expertise area]
**Model:** [sonnet/opus/haiku]

### Purpose
[2-3 sentences defining identity]

### Instructions
- [rule 1]
- [rule 2]
- [rule 3]

### Examples

**Example 1:** [scenario]
- Input: [input]
- Output: [output]

**Example 2:** [scenario]
- Input: [input]
- Output: [output]

### Validation
- [ ] Purpose is specific
- [ ] Instructions are actionable
- [ ] Examples are diverse
- [ ] Boundaries are clear
```

## Common Agent Types

### Expert Agent

Focus: Deep domain knowledge

```markdown
## Purpose
You are an expert in [domain] with deep knowledge of [specifics].
```

### Guard Agent

Focus: Validation and safety

```markdown
## Instructions
- Validate all inputs against [criteria]
- Block requests that [conditions]
- Log suspicious activity
```

### Translator Agent

Focus: Format conversion

```markdown
## Examples
### Input Format
[format A]

### Output Format
[format B]
```

## Key Quote

> "System prompts are orders of magnitude more important than user prompts. They run once and affect everything."

## Cross-References

- @system-vs-user-prompts.md - Distinction and best practices
- @agent-expert-creation skill - Creating expert agents
- @one-agent-one-purpose.md - Specialization principle

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
