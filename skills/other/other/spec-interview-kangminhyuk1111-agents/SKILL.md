---
name: spec-interview
description: Conducts a deep, multi-round interview to clarify ambiguous requirements and produces a structured specification document. Automatically discovers requirement files and asks probing, non-obvious questions across technical implementation, UX/UI, trade-offs, edge cases, and architectural decisions.
---

# Spec Interview

## Overview
This skill transforms vague or incomplete requirements into a comprehensive, actionable specification through structured interviewing. It reads existing requirement documents in the project, identifies gaps and ambiguities, then conducts a rigorous multi-round interview using the AskUserQuestion tool. The interview continues until all critical dimensions are clarified. Upon completion, it produces a structured markdown specification file.

## Instructions

### Phase 1: Discovery & Analysis
1. Scan the project for requirement-related files. Search patterns include:
   - `**/SPEC.md`, `**/spec.md`, `**/SPEC*.md`
   - `**/PRD.md`, `**/prd.md`
   - `**/REQUIREMENTS.md`, `**/requirements.md`
   - `**/README.md` (if it contains requirement-like content)
   - `**/docs/requirements/**`, `**/docs/specs/**`
   - Any file passed as an argument to the skill invocation
2. Read and deeply analyze all discovered files.
3. Before starting the interview, internally identify:
   - What is explicitly stated vs. what is assumed
   - Logical contradictions or inconsistencies
   - Missing technical details that would block implementation
   - Unstated constraints (performance, scale, compatibility)
   - Ambiguous terms that could be interpreted multiple ways

### Phase 2: Interview Execution
4. Conduct the interview using `AskUserQuestion`. Follow these principles:

   **Question Quality Rules:**
   - NEVER ask questions whose answers are already in the document
   - NEVER ask generic questions like "What's the target audience?" unless genuinely unclear
   - Each question must be derived from a specific gap, contradiction, or ambiguity found in the requirement document
   - Questions should reveal hidden assumptions and force the user to think about scenarios they haven't considered
   - Prefer questions that expose trade-offs ("If X and Y conflict, which takes priority?") over simple information gathering
   - Ask "what happens when..." questions for edge cases the document doesn't address
   - Challenge stated requirements when they seem contradictory or technically infeasible

   **Interview Dimensions (cover all that are relevant):**
   - **Core Intent**: What problem is actually being solved? Is the stated solution the right approach?
   - **Technical Architecture**: Data models, state management, API contracts, system boundaries
   - **UX/UI Decisions**: Interaction patterns, error states the user sees, loading states, empty states, accessibility
   - **Edge Cases & Failure Modes**: What breaks? What's the degraded experience? Concurrency issues?
   - **Trade-offs & Constraints**: Performance vs. correctness, speed-to-market vs. quality, flexibility vs. simplicity
   - **Security & Privacy**: Data exposure, authentication boundaries, input validation
   - **Scale & Performance**: Expected load, data volume growth, bottleneck scenarios
   - **Integration & Dependencies**: External system contracts, version compatibility, fallback behavior
   - **Migration & Rollout**: How to get from current state to target state, backward compatibility

   **Interview Flow:**
   - Start with the most critical ambiguities first (things that would fundamentally change the implementation)
   - Group related questions together (max 3-4 questions per round using AskUserQuestion's multi-question capability)
   - After each round, synthesize the answers and identify new questions that emerge from the responses
   - If an answer reveals a new area of ambiguity, explore it before moving on
   - Track which dimensions have been sufficiently covered and which remain open

5. Continue the interview until:
   - All critical implementation decisions have clear answers
   - No logical contradictions remain
   - Edge cases have defined behavior
   - Trade-offs have explicit priorities
   - The specification is implementable without further clarification

### Phase 3: Specification Output
6. When the interview is complete, inform the user that the interview is finished and write the specification file.
7. Output file location: Same directory as the discovered requirement file, named `SPEC.md` (or update the existing file if the user prefers).
8. The specification must follow this structure:

```markdown
# [Project/Feature Name] Specification

## 1. Overview
- Problem statement
- Solution summary
- Key goals and success criteria

## 2. Functional Requirements
### 2.1 Core Features
- Feature descriptions with acceptance criteria
### 2.2 User Flows
- Step-by-step user interactions
### 2.3 Edge Cases & Error Handling
- Defined behavior for exceptional scenarios

## 3. Technical Architecture
### 3.1 System Design
- High-level architecture decisions
- Component boundaries
### 3.2 Data Model
- Key entities and relationships
### 3.3 API Design
- Endpoints, contracts, error responses
### 3.4 State Management
- Client/server state boundaries

## 4. UX/UI Specification
### 4.1 Interaction Patterns
- Key interactions and feedback
### 4.2 States
- Loading, empty, error, success states
### 4.3 Accessibility
- Requirements and standards

## 5. Non-Functional Requirements
### 5.1 Performance
- Targets and constraints
### 5.2 Security
- Authentication, authorization, data protection
### 5.3 Scalability
- Growth expectations and limits

## 6. Constraints & Trade-offs
- Explicit decisions made and their rationale
- What was deliberately excluded and why

## 7. Open Questions
- Any remaining items that need future clarification
```

9. Sections that are not relevant to the project should be omitted (don't include empty sections).
10. Every statement in the spec must be traceable to either the original document or an interview answer. Do not invent requirements.

## Examples

### Input
```
/spec-interview
```
(With a SPEC.md file in the project containing: "Build a notification system for the app")

### Interview Round 1
```
Questions asked:
1. "The document mentions 'notifications' but doesn't specify the delivery channels.
    Are we talking about in-app only, or also push/email/SMS? If multiple, which is
    the primary channel and which are fallbacks?"
2. "What triggers a notification? Is it purely event-driven from backend actions,
    or can other users trigger notifications (e.g., mentions, shares)?"
3. "Should notifications be real-time (WebSocket/SSE) or is polling acceptable?
    What's the maximum acceptable delay between event and notification?"
```

### Interview Round 2 (after user answers)
```
Questions asked:
1. "You mentioned push notifications are needed. If the user has denied push
    permissions, should the system fall back to email, show an in-app prompt to
    re-enable, or silently degrade?"
2. "For real-time delivery: if the WebSocket connection drops, should queued
    notifications be delivered on reconnect, or only show new ones from that point?"
3. "You said 'mentions' trigger notifications. In a thread with 50 participants,
    does @all notify everyone? Is there a rate limit to prevent notification storms?"
```

### Output
A structured SPEC.md file with all ambiguities resolved, containing specific implementation details derived from the interview.

## Guidelines
- The interview is the primary value of this skill. Spend more effort on asking the right questions than on formatting the output.
- Never rush the interview. It's better to ask one more round of questions than to produce a spec with assumptions.
- When the user's answer is vague, follow up. Don't accept "it should just work" as a specification.
- Respect the user's domain expertise. Ask "how" and "what if" questions, not "what is" questions about their own domain.
- If the requirement document is well-specified in certain areas, acknowledge that and focus interview time on the gaps.
- Keep each interview round focused. Don't mix architectural questions with UX details in the same round.
- Use the user's own terminology from the requirement document. Don't introduce new jargon.
- If the project has existing code, reference actual file structures or patterns when asking technical questions to ground the discussion in reality.
- The final spec should be immediately actionable by a developer who hasn't seen the interview. All context must be captured in the document.
