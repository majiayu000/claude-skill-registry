---
name: brainstorming-ideas
description: Turn ideas into designs through collaborative dialogue. Use when user wants to brainstorm, design features, explore approaches, or think through implementation before coding.
user-invocable: true
allowed-tools:
  - AskUserQuestion
  - Task
  - TodoWrite
  - Read
  - Grep
  - Glob
  - Write
  - mcp__perplexity-ask__perplexity_ask
  - WebFetch
  - Bash(git *)
argument-hint: "[<topic>]"
---

# Brainstorming Ideas Into Designs

Transform vague ideas into fully-formed designs through structured collaborative dialogue.

**Use TodoWrite** to track these 7 phases:

1. Understand the idea (dialogue first, no agents)
2. Explore requirements (Starbursting questions)
3. Checkpoint - offer exploration/research options
4. Research similar solutions (if requested)
5. Present approaches with recommendation
6. Validate design incrementally
7. Document and next steps

---

## Core Principles

- **Dialogue first** - Ask the user before spawning any agents
- **One question at a time** - Never batch multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended
- **"Other" always available** - Free text input for custom responses
- **YAGNI ruthlessly** - Challenge every feature's necessity
- **Incremental validation** - Present design in 200-300 word sections
- **Agents on request** - Only explore/research when user chooses it

---

## Phase 1: Understand the Idea

Start with dialogue, not agents. Ask the user directly.

### 1a. Initial Question

Use AskUserQuestion:

| Header    | Question                           | Options                                                                                                                                                                                       |
| --------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Idea type | What would you like to brainstorm? | 1. **New feature** - Add new functionality 2. **Modification** - Change existing behavior 3. **Integration** - Connect with external system 4. **Exploration** - Not sure yet, let's discover |

### 1b. Follow-up (based on response)

Ask clarifying questions using AskUserQuestion. Keep it conversational:

- "Can you describe this in a sentence or two?" (free text via "Other")
- "What triggered this idea?" with context-appropriate options
- "Is there an existing feature this builds on?"

---

## Phase 2: Explore Requirements (Starbursting)

Ask questions **one at a time** using AskUserQuestion. Adapt based on idea type.

### Question Framework (5WH)

| Question Type | When to Ask                    | Example AskUserQuestion                                                              |
| ------------- | ------------------------------ | ------------------------------------------------------------------------------------ |
| **WHO**       | Always first                   | "Who will use this?" → Options: Existing users, New segment, Internal, API consumers |
| **WHY**       | After WHO                      | "What problem does this solve?" → Options based on detected pain points              |
| **WHAT**      | After WHY is clear             | "What's the core capability?" → Open or options based on research                    |
| **WHERE**     | For integrations/modifications | "Where should this live?" → Options based on codebase exploration                    |
| **HOW**       | After approach research        | "How should we implement?" → Present 2-3 technical approaches                        |

### Adaptive Questioning

- Skip questions when answers are obvious from context
- If user seems certain, move faster to approaches
- If user seems uncertain, explore deeper with sub-questions
- Use "Other" option to allow custom responses

---

## Phase 3: Checkpoint - Gather More Context?

After understanding requirements, **ask before spawning any agents**:

| Header    | Question               | Options                                                                                                                                                                                                       |
| --------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Next step | How should we proceed? | 1. **Explore codebase** - Check existing patterns and tech stack 2. **Research solutions** - Look up how others solve this 3. **Both** - Explore then research 4. **Skip to approaches** - I know what I want |

### If user chooses "Explore codebase":

```
Task(
  subagent_type="Explore",
  prompt="Quick scan: project structure, tech stack, patterns relevant to [user's idea]",
  run_in_background=false
)
```

Then summarize findings and ask: "Based on this, should we also research external solutions?"

### If user chooses "Research solutions":

Proceed to Phase 4.

### If user chooses "Skip to approaches":

Jump directly to Phase 5 (Present Approaches).

---

## Phase 4: Research Similar Solutions (If Requested)

Only run when user explicitly chose research in Phase 3.

### 4a. Perplexity Query

```
mcp__perplexity-ask__perplexity_ask({
  messages: [{
    role: "user",
    content: "How do leading [industry] products implement [feature type]? Include architectural patterns, UX approaches, and trade-offs. Focus on [tech stack] implementations."
  }]
})
```

### 4b. Follow Citations

After Perplexity response, WebFetch top 2-3 relevant sources:

```
WebFetch(url="<citation-url>", prompt="Extract implementation details, code patterns, and lessons learned for [feature]")
```

### 4c. Synthesize Findings

Present research summary before asking approach preference:

```markdown
## Research Findings

**Common patterns:**

- [Pattern 1]: Used by X, Y. Trade-off: ...
- [Pattern 2]: Used by Z. Trade-off: ...

**Recommended for our context:** [Pattern] because [reasons]
```

---

## Phase 5: Present Approaches

Use AskUserQuestion with 2-4 options:

| Header   | Question                  | Options                                                                                                                              |
| -------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Approach | Which approach fits best? | 1. **[Recommended]** - Description + key trade-off 2. **[Alternative]** - Description + key trade-off 3. **Minimal** - YAGNI version |

### Approach Template

For each option, briefly cover:

- **What**: Core implementation
- **Trade-offs**: Complexity vs flexibility, Now vs later
- **Fits when**: Scenario where this shines

---

## Phase 6: Validate Design Incrementally

Present design in sections (~200-300 words each). After each section, use AskUserQuestion:

| Header   | Question                        | Options                                                                                                                    |
| -------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Validate | Does this [section] look right? | 1. **Yes, continue** - Move to next section 2. **Needs changes** - I'll explain 3. **Go back** - Revisit earlier decisions |

### Design Sections

1. **Architecture Overview** - Components, responsibilities, relationships
2. **Data Flow** - How information moves through the system
3. **API/Interface** - External contracts and user interactions
4. **Error Handling** - Failure modes and recovery strategies
5. **Testing Strategy** - How to verify it works

### YAGNI Checkpoints

At each section, actively challenge:

- "Do we need this now, or is it speculative?"
- "What's the simplest version that solves the problem?"
- "Can we defer this complexity?"

---

## Phase 7: Document and Next Steps

### 7a. Write Design Document

```
Write(
  file_path="docs/plans/YYYY-MM-DD-<topic>-design.md",
  content="# [Feature] Design\n\n## Problem\n...\n## Solution\n...\n## Architecture\n..."
)
```

### 7b. Commit Design

```bash
git add docs/plans/*.md && git commit -m "docs: add [feature] design document"
```

### 7c. Implementation Handoff

Use AskUserQuestion:

| Header     | Question                              | Options                                                                                                                                                           |
| ---------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Next steps | Ready to proceed with implementation? | 1. **Create worktree** - Isolated workspace via using-git-worktrees 2. **Create plan** - Detailed implementation steps 3. **Done for now** - Just save the design |

---

## Methodology Reference

This skill incorporates proven brainstorming techniques:

| Technique                 | How It's Used                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| **Starbursting (5WH)**    | Structured questions in Phase 2                                                             |
| **Design Thinking**       | Empathize (context) → Define (WHY) → Ideate → Prototype (design sections)                   |
| **SCAMPER**               | For modifications: Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse |
| **Reverse Brainstorming** | "How could this fail?" during validation                                                    |
| **Mind Mapping**          | Architecture section visualizes relationships                                               |

---

## Examples

```
/brainstorming-ideas                    # Start open-ended brainstorm
/brainstorming-ideas user notifications # Brainstorm notification feature
/brainstorming-ideas auth flow          # Brainstorm authentication changes
```

**Execute this collaborative brainstorming workflow now.**
