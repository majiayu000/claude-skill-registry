---
name: blueprint
description: Transform verbose natural language requests into structured bilingual documentation (Korean for review + English for AI prompts). Use when you need to clarify and structure a complex request before implementation.
---

# Generate Request Blueprint Document

Transform ANY unstructured natural language request into clear, systematic markdown documentation: $ARGUMENTS

## Purpose of This Command

This command works for ALL types of requests - technical, non-technical, decision-making, planning, career advice, personal questions, brainstorming, etc. There is no "not technical enough" - if the user asks, generate the blueprint.

Analyze ANY unstructured user request and create:

1. **Korean Version**: Structured document for user review and confirmation
2. **English Version**: Optimized prompt document for AI agent consumption

This enables:

- Reduced AI hallucination
- Lower context costs
- Clear communication of request intent
- Concrete scope and constraints

## Types of Requests Supported

- ✅ Software development and coding tasks
- ✅ Career decisions and job transitions
- ✅ Personal advice and life consultations
- ✅ Business strategy and planning
- ✅ Research and analysis questions
- ✅ Decision-making dilemmas
- ✅ Creative and design projects
- ✅ Financial planning discussions
- ✅ Any other topics requiring structured thinking

## Output Principles

Structure flexibly based on context. Adapt sections to the request - forcing unnecessary sections reduces clarity.

### Core Principles

1. **Simple request → Simple document**: 3-4 sections sufficient
2. **Complex request → Detailed document**: Add only what's needed
3. **Non-technical request**: Skip technical environment, dependencies
4. **Core goal**: Reduce verbosity, structure essentials only

### Document Structure

Create markdown file in **root directory**:

```markdown
# [Request Title]

---

## 📋 Korean Version (For Review)

> Version for user to review and confirm request content

[Include only necessary sections based on context]

### Example Possible Sections (Optional)

- 🎯 Request Overview
- 📖 Purpose & Background
- ✅ Specific Requirements
- 🚫 Constraints & Warnings
- 🎨 Expected Outcomes
- 🛠️ Technical Environment (technical requests only)
- 📊 Priority (if needed)
- 📚 References (if available)
- 💬 Additional Context (if needed)

---

## 📋 English Version (For AI Prompt)

> **Language Requirement: All responses, conversations, and outputs should be in Korean (한글).**
>
> This section is optimized for AI agent consumption. The AI agent must communicate entirely in Korean regardless of the prompt language.

[Same structure as Korean version, written in English]
[Include same sections only, do not add unnecessary ones]

---

## 🔄 Next Steps

1. Review the Korean version
2. Modify if needed
3. Share the English version with the next AI agent
```

## File Naming Convention

Generated filename: `blueprint-[brief-title]-[timestamp].md`

Examples:

- `blueprint-user-auth-implementation-20250110-143022.md`
- `blueprint-api-refactoring-20250110-150530.md`

## Usage Examples

**Basic usage:**

```
/blueprint
```

**With specific focus:**

```
/blueprint focus on authentication system
```

**Complex request cleanup:**

```
/blueprint based on entire previous conversation
```

## Workflow

1. **User → Agent A**: Explain request verbosely in natural language
2. **Agent A**: Execute `/blueprint` to generate structured document (root path)
3. **User**: Review and modify Korean version
4. **User → Agent B**: Share English version prompt
5. **Agent B**: Perform work based on structured instructions (communicate in Korean)

## Key Features

### Bilingual Structure

- **Korean Section**: Intuitive review, quick understanding, Korean user-friendly
- **English Section**: Prompt engineering optimization, improved AI performance, clear instructions

### Language Policy

English version has **CRITICAL** notice stating "all communication in Korean" to ensure:

- AI agents respond in Korean even with English prompts
- Consistent user experience
- Communication efficiency

## Writing Guidelines

Document only what the user explicitly stated. This prevents hallucination and ensures the blueprint accurately represents the user's intent.

When generating documents:

### ✅ DO:

- **Record user's exact words** for ambiguous expressions
- **Keep vague terms vague** - don't interpret them
- **Only include explicitly mentioned** requirements, constraints, and context
- **Preserve user's original phrasing** when unclear
- **Ask clarifying questions** (mark as "Needs clarification:") rather than guessing

### ❌ DON'T:

- **DON'T extract "implicit" requirements** - only explicit ones
- **DON'T interpret vague expressions** like "tight circumstances" as specific problems
- **DON'T add details** the user didn't mention
- **DON'T expand abbreviations** or casual language into formal assumptions
- **DON'T infer user's situation** beyond what they stated

## Benefits

1. **Reduced Hallucination**: Clear structure and specific requirements minimize AI guessing
2. **Context Efficiency**: Remove unnecessary verbosity, deliver only core information
3. **Verifiability**: User can clearly confirm request content
4. **Reusability**: Use as template for similar tasks
5. **Enhanced Collaboration**: Clear communication when passing work between AI agents
