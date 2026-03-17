---
name: aico-pm-brainstorming
description: |
  Guide users through structured dialogue to transform vague ideas into clear, actionable product concepts. Uses one-question-at-a-time approach with multiple choice options.

  Use this skill when:
  - User says "I have an idea", "I want to build", "let me think about"
  - User mentions "brainstorm", "explore ideas", "think through"
  - Requirements are vague, incomplete, or user seems unsure what they want
  - Need to explore problem space before jumping to solutions
  - Running /pm.plan but requirements are unclear or missing context
  - User asks "what should I build?", "how should this work?"

  Process: Ask ONE question at a time, prefer multiple choice, explore 2-3 approaches before settling.
---

# Brainstorming

## ⚠️ CRITICAL RULES - READ FIRST

1. **READ CONSTITUTION**: Always read `docs/reference/pm/constitution.md` first for product context
2. **ONE QUESTION AT A TIME**: Never ask multiple questions in one message
3. **USE MULTIPLE CHOICE**: Prefer AskUserQuestion tool with 2-4 options

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Check context**: Scan `docs/reference/pm/` for existing product context
2. **Understand problem**: Ask clarifying questions one at a time
3. **Explore alternatives**: Propose 2-3 approaches with trade-offs
4. **Validate concept**: Present ideas in small sections (200-300 words), confirm each
5. **Document outcome**: Save validated concept for next steps

## Core Pattern

| Phase      | Action                                 | Output            |
| ---------- | -------------------------------------- | ----------------- |
| Understand | Ask clarifying questions one at a time | Problem statement |
| Explore    | Propose 2-3 approaches with trade-offs | Selected approach |
| Validate   | Present concept in small sections      | Validated concept |

## Key Rules

- ALWAYS ask ONE question per message - never overwhelm with multiple questions
- MUST prefer multiple choice over open-ended questions when possible
- ALWAYS explore 2-3 alternative approaches before settling on one
- Present ideas incrementally in 200-300 word sections, confirm each before continuing

## Question Examples

- "What problem are you trying to solve for users?"
- "Who is the primary user for this feature?"
- "What does success look like? (A) metric improvement (B) user satisfaction (C) both"

## Common Mistakes

- ❌ Ask multiple questions at once → ✅ One question per message
- ❌ Jump to solutions immediately → ✅ Understand problem first
- ❌ Skip alternatives → ✅ Always explore 2-3 approaches

---

## Iron Law

**NO IMPLEMENTATION DISCUSSION DURING BRAINSTORMING**

This rule is non-negotiable. During brainstorming:

1. Focus only on WHAT, never HOW
2. No code, no architecture, no technical details
3. Capture all ideas without judgment
4. Defer feasibility analysis to later phases

### Rationalization Defense

| Excuse                                       | Reality                                        |
| -------------------------------------------- | ---------------------------------------------- |
| "I already know what to build"               | Unvalidated assumptions cause 3x rework        |
| "Let's save time and discuss implementation" | Premature optimization kills innovation        |
| "The solution is obvious"                    | Obvious solutions often miss edge cases        |
| "We don't have time for this"                | 1 hour of brainstorming saves 3 days of rework |
