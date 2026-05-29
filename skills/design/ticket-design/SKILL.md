---
name: ticket-design
description: Create a design document with prototype placeholders for a feature. Includes agent review loop before user approval. Resumable - can commit and continue later.
---

# Task Design Creator

You are an **orchestrator agent** creating a design document with prototype code placeholders. You delegate heavy work to sub-agents while handling user interaction yourself.

**Architecture**: Thin orchestrator + sub-agents for maximum autonomy after user questions are answered.

## Output Location

Write designs to: `ai/tickets/`

Naming convention: `YYYY-MM-DD-feature-name.md` (e.g., `2026-01-28-user-authentication.md`)

## Design Document Structure

```markdown
---
status: created | description | explored | ready-for-review | changes-requested | ai-reviewed | approved
reviewer-iterations: 0
prototype-files: []
---

# User Description (Verbatim)

[User's description stays here unchanged]

# Design: [Feature Name]

## Problem Statement
[2-4 sentences: What problem are we solving? Why does it need to be solved?]

## Proposed Approach
[High-level description of the solution. 1-2 paragraphs. Include a diagram if helpful.]

## Key Decisions

| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| [Decision 1] | A) ..., B) ... | A | [Why A over B] |

## Trade-offs
- **Pro**: [Benefit of this approach]
- **Con**: [Drawback or limitation]
- **Mitigated by**: [How we handle the con]

## Affected Components

| File | Change Type | Description |
|------|-------------|-------------|
| `src/foo/bar.ts` | Modify | Add X parameter to Y function |
| `src/foo/new-file.ts` | Create | New module for Z |

## Technical Details
[Code examples, data structures, API contracts - enough detail for prototype placeholders]

## Edge Cases and Error Handling
[Document corner cases discovered during exploration]

## Test Cases

| Test Case | Type | Description |
|-----------|------|-------------|
| [Test name] | Unit / Integration | [What this test verifies] |

# Context

## Exploration Findings
[Summarize exploration findings and relevant context to drive design.]

## User Requirements & Answers
[Original requirement and all Q&A from clarification and implementation discussions - keep for documentation]

## AI Review Notes
[Filled by reviewer agent - issues found and how they were addressed]

## User Feedback
[Filled by orchestrator after user review - detailed feedback, questions, and discussion notes]
```

## Status Definitions

| Status | Meaning |
|--------|---------|
| `created` | Design document created with minimal scaffold |
| `description` | User provided feature description in the design doc |
| `explored` | Exploration completed and context written into the design doc |
| `ready-for-review` | Design document AND all prototype placeholders created |
| `changes-requested` | Review or user feedback requires updates |
| `ai-reviewed` | Passed agent review, ready for user approval |
| `approved` | User approved, ready for /ticket-plan |

## Prototype Placeholder Format

When creating prototype placeholders in code, ALWAYS include the design file reference:

### For new files:
```typescript
// ═══════════════════════════════════════════════════════════════════════════
// DESIGN PROTOTYPE: 2026-01-28-feature-name.md
// Do not use until implementation complete
// ═══════════════════════════════════════════════════════════════════════════
//
// This file will contain:
//
// export interface UserSession {
//   userId: string;
//   token: string;
//   expiresAt: Date;
// }
//
// export function createSession(userId: string): UserSession
// export function validateSession(token: string): boolean
//
// ═══════════════════════════════════════════════════════════════════════════
```

### For existing files (inline markers):
```typescript
// DESIGN PROTOTYPE: 2026-01-28-feature-name.md
// Add parameter → mappingType: MappingTypeName = "loinc"
export function generateConceptMapId(
  sender: SenderContext,
): string {
  // DESIGN PROTOTYPE: 2026-01-28-feature-name.md
  // Replace "-to-loinc" with → type.conceptMapSuffix
  return `hl7v2-${app}-${facility}-to-loinc`;
}
```

The design file reference (`DESIGN PROTOTYPE: <filename>.md`) allows multiple design processes to run in parallel without conflicts.

---

## Architecture: Orchestrator + Sub-Agents

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MAIN AGENT (Orchestrator)                       │
│                                                                         │
│  Responsibilities:                                                      │
│  - Check state & resume (Phase 0)                                       │
│  - Ask clarifying questions (Phase 1)                                   │
│  - Discuss implementation approach (Phase 3)                            │
│  - Ask user for approval (Phase 6)                                      │
│  - Orchestrate sub-agents                                               │
│  - Stay thin - minimal context accumulation                             │
└─────────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Explore Agent  │  │  Design Agent   │  │  Review Agent   │
│    (Phase 2)    │  │   (Phase 4)     │  │   (Phase 5)     │
│                 │  │                 │  │                 │
│ - Search code   │  │ - Create design │  │ - Critique      │
│ - Find patterns │  │ - Fix design    │  │ - Find issues   │
│ - Return summary│  │ - Add prototypes│  │ - Return verdict│
│                 │  │ - Commit        │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

**Benefits:**
- Main agent stays thin (just summaries and user dialogue)
- Each sub-agent has fresh context
- After Phase 3 (user discussion), runs autonomously through design → review loop
- User can focus on other tasks

---

## Your Process

### Phase 0: Check State & Resume

Before starting, check if a design file already exists for this feature.
If none exists, create it immediately with a minimal scaffold and `status: created`.
Minimal scaffold = frontmatter + all section headers from the template, with empty placeholders.

**State → Phase mapping:**

| Design File State | Start From |
|-------------------|------------|
| No design file exists | Create design file with `status: created`, then Phase 1 |
| `status: created` | Phase 1 |
| `status: description` | Phase 1 (use doc as feature description) |
| `status: explored` | Phase 4 via Design Agent |
| `status: ready-for-review` | Phase 5 (AI Review) |
| `status: changes-requested` | Phase 3 (Discuss with user before fixing) |
| `status: ai-reviewed` | Phase 6 (User Approval) |
| `status: approved` | **Automatically invoke /ticket-plan skill** - do not ask user |

If resuming from an existing file, briefly summarize the current state to the user before continuing.

---

### Phase 1: Clarify Requirements (if needed)

**You (orchestrator) handle this directly** - it requires user interaction.

If `status: description`, treat the document contents as the feature description and use it to drive Phase 1.

Before exploring code, ensure you understand WHAT to build. If the user's request is already clear and specific, skip to Phase 2.

Ask only questions that affect what you'll search for:
- "Should this feature be accessible to all users or require authentication?"
- "What should happen when [core operation] fails - retry, error message, or silent fallback?"
- "Does this need to work with [external system] or be standalone?"

After clarifying requirements, update the design document:
1. Write user requirements and answers to **# Context > ## User Requirements & Answers**
2. Commit the update

---

### Phase 2: Explore Codebase (Sub-Agent)

**Spawn an Explore agent** to search the codebase. This keeps exploration context separate.

**Explore agent prompt:**
```
Explore the codebase to understand how to implement [feature description].

Find:
1. Similar features or patterns that already exist
2. Architecture: How does data flow? What are the layers?
3. Files that will likely need changes
4. Testing patterns used in this codebase
5. Project conventions (check CLAUDE.md, README)
6. Libraries and established patterns

Return a summary with:
- Key files and their purposes
- Existing patterns that should be followed
- Constraints or limitations discovered
- Recommended approach based on codebase style
- Areas of uncertainty that need clarification from user
```

**After receiving exploration summary**, present findings to user:
- Key files and patterns discovered
- Existing approaches that could apply
- Constraints or limitations found
- Areas of uncertainty that need clarification

---

### Phase 3: Discuss Implementation Approach

**You (orchestrator) handle this directly** - it requires user interaction.

Now discuss HOW to build, grounded in the exploration summary. Use the AskUserQuestion tool.

1. **Validate assumptions**: "The exploration found X pattern in the codebase. Should we follow it for this feature?"
2. **Present options**: "Given the existing architecture, I see two approaches: A (pros/cons) or B (pros/cons). Which do you prefer?"
3. **Clarify ambiguities**: "The codebase uses Y for similar features, but the requirement mentions Z. Should we stick with Y or introduce Z?"
4. **Confirm scope**: "Based on exploration, this will require changes to [files]. Is there anything I'm missing?"
5. **Edge cases**: "How should we handle [specific scenario discovered during exploration]?"
6. **Testing strategy**: "Tests in this area use [pattern]. Should we continue with this approach?"

**Continue this discussion until you and the user have reached agreement on the approach.** Do not rush to the design phase. Ask follow-up questions, discuss trade-offs, and iterate until there are no open questions about the implementation approach.

**After this phase, you must have everything needed for the design process.**

After Phase 3 completes:
1. Update the design document with:
   - `status: explored`
   - Exploration findings in **# Context > ## Exploration Findings**
   - All Q&A and discussion in **# Context > ## User Requirements & Answers**
2. Commit the update:
   ```bash
   git add ai/tickets/YYYY-MM-DD-feature-name.md
   git commit -m "WIP: Design for [feature-name] - exploration context recorded"
   ```

---

### Phase 4: Create/Fix Design & Prototypes

Create the design document and prototype placeholders, OR spawn a sub-agent to fix an existing design based on feedback.

**Choose the prompt based on document status:**
- `status: explored` → Use **Create Design prompt**
- `status: changes-requested` → Spawn a sub-agent with the **Fix Design prompt**

---

#### Create Design prompt (status: explored)

```
Create a design document and prototype placeholders for [feature name]. Think hard.

## Design Document
Read: ai/tickets/YYYY-MM-DD-feature-name.md

The document contains context you need:
- **# Context > ## Exploration Findings**: Codebase analysis results
- **# Context > ## User Requirements & Answers**: Requirements and all Q&A from discussions

## Your Tasks

1. Fill out the Design sections of the document (everything ABOVE the "# Context" header):
   - **## Problem Statement**: 2-4 sentences on what problem we're solving
   - **## Proposed Approach**: High-level solution description
   - **## Key Decisions**: Table of decisions with options considered and rationale
   - **## Trade-offs**: Pros, cons, and mitigations
   - **## Affected Components**: Table of files with change types
   - **## Technical Details**: Code examples, data structures, API contracts
   - **## Edge Cases and Error Handling**: Corner cases and how to handle them
   - **## Test Cases**: Table listing test cases with type (Unit/Integration) and description

   Base all content on the Context sections.

2. Create prototype placeholders:
   - For NEW files: Create scaffold with `DESIGN PROTOTYPE: YYYY-MM-DD-feature-name.md` header
   - For EXISTING files: Add inline `// DESIGN PROTOTYPE: YYYY-MM-DD-feature-name.md` markers
   - Show types, function signatures, key logic locations - not full implementation

3. Update design document:
   - Add all prototype file paths to `prototype-files` in frontmatter
   - Set `status: ready-for-review`

4. Commit all changes:
    ```bash
    git add ai/tickets/YYYY-MM-DD-feature-name.md [prototype files...]
    git commit -m "WIP: Design for [feature-name] - ready for review"
    ```

## Return Summary

- Design document path
- List of prototype files created/modified
- Key decisions made
- Any concerns or alternatives considered
```

---

#### Fix Design prompt (status: changes-requested)

```
Fix the design based on feedback for [feature name]. Think hard.

## Design Document
Read: ai/tickets/YYYY-MM-DD-feature-name.md

The document contains feedback to address:
- **# Context > ## AI Review Notes**: Issues found by the reviewer
- **# Context > ## User Feedback**: User's change requests

## Your Tasks

1. Read the feedback in **## AI Review Notes** and/or **## User Feedback**

2. Address each issue:
   - Update Design sections as needed
   - Update prototype placeholders as needed
   - Document what was changed in **## AI Review Notes**

3. If you change the approach, update **## Key Decisions** with rationale

4. Set `status: ready-for-review`

5. Commit changes:
    ```bash
    git add [modified files]
    git commit -m "WIP: Design for [feature-name] - addressing feedback"
    ```

## Return Summary

- List of changes made
- Prototype files modified
- Key decisions changed (if any)
```

---

**After Design agent completes**, proceed immediately to Phase 5.

---

### Phase 5: AI Review (Sub-Agent)

**Spawn a Review agent** to critique the design.

```
 to review implementation of Task [N] from [current_task_document_path]. Think hard. The changes are uncommited. Return your review output as your response, do not change any files. 
```

**Review agent prompt:**
```
Use skill ai-review to review a software design for [feature name]. Think very hard.

## Design Document
Read: ai/tickets/YYYY-MM-DD-feature-name.md

## Prototype Files
[List files with DESIGN PROTOTYPE markers - include file paths]

## Output Format

Update the design document directly:
- Write review findings in **# Context > ## AI Review Notes** (issues + resolutions/notes)
- Set `status: changes-requested` if blockers found
- Set `status: ai-reviewed` if approved for user review
- Commit the design document changes

Return only one line, exactly:
- `BLOCKERS FOUND` (if blockers exist)
- `APPROVED FOR USER REVIEW` (if no blockers)
```

**Review loop logic (you orchestrate this):**

1. Run Review agent
2. Parse verdict from response
3. If `BLOCKERS FOUND`:
   - Increment `reviewer-iterations` in design doc
   - Spawn Design agent in FIX MODE
   - Run Review agent again (go to step 1)
4. If `APPROVED FOR USER REVIEW`:
   - Proceed to Phase 6

---

### Phase 6: User Approval

**You (orchestrator) handle this directly** - it requires user interaction.

Present the design to the user for approval:

**Summary to show:**
1. Problem statement (brief)
2. Chosen approach (1-2 sentences)
3. Key decisions made
4. Files that will be affected
5. Test cases planned (with unit/integration breakdown)
6. Number of review iterations it took

**Ask the user:**
- **Approve**: Set `status: approved`, commit, then automatically invoke /ticket-plan
- **Request changes / discuss**: Record feedback in **# Context > ## User Feedback**, set `status: changes-requested`, commit, **go back to Phase 3** to discuss the changes before fixing

**On approval:**

```bash
git add ai/tickets/YYYY-MM-DD-feature-name.md
git commit -m "Design approved: [feature-name]"
```

Then automatically invoke the /ticket-plan skill to create the implementation plan. Do not ask the user - proceed directly.
