---
name: spec-writer
description: Generate Product Requirements Document with EARS syntax and structured ambiguity clarification
triggers: [spec, PRD, feature, requirements, product requirements, write spec, new feature]
context_cost: medium
---

# Spec Writer Skill

## Goal
Transform a user goal or feature request into a structured PRD using EARS syntax. Before generating requirements, invoke the ambiguity layer to clarify unclear aspects. Human approval required before proceeding to implementation.

## Steps

1. **Receive and understand the goal**
   - First, check for `Step 0` strategic context in `docs/strategic/` (e.g., `BUSINESS_CASE.md`, `EMPATHY_MAP.md`, `PROBLEM_STATEMENT.md`). If present, read them.
   - Ask the user: "Describe what you want to build in plain language"
   - Identify: Who is the user? What problem does it solve? What does success look like? (using the strategic docs if available)

2. **Ambiguity Layer — ask clarifying questions**
   Identify and ask about ALL ambiguous aspects before writing requirements:
   ```
   Questions to ask (examples):
   - "Who are the users of this feature? (roles, permissions, guest vs authenticated)"
   - "What happens if [edge case] occurs?"
   - "What are the performance expectations? (response time, concurrent users)"
   - "Is there an existing system this integrates with? What are its constraints?"
   - "What is explicitly out of scope for this version?"
   - "Are there any regulatory requirements? (GDPR, HIPAA, PCI-DSS)"
   - "What devices/browsers must be supported?"
   ```
   Wait for answers before proceeding.

3. **Generate the PRD** using templates/product/PRD_TEMPLATE.md

4. **Write EARS requirements** — use all 5 patterns as appropriate:

   **Ubiquitous** (always applies):
   ```
   THE SYSTEM SHALL encrypt all data in transit using TLS 1.3 or higher.
   ```

   **Event-Driven** (triggered by an event):
   ```
   WHEN a user submits a login form with incorrect credentials 3 consecutive times
   THE SYSTEM SHALL lock the account for 15 minutes and send an email notification.
   ```

   **State-Driven** (while in a state):
   ```
   WHILE the payment processing service is unavailable
   THE SYSTEM SHALL queue requests and retry with exponential backoff up to 3 times.
   ```

   **Optional Feature** (feature flag / conditional):
   ```
   WHERE two-factor authentication is enabled for the account
   THE SYSTEM SHALL require a TOTP code on each login attempt.
   ```

   **Unwanted Behavior** (negative requirements):
   ```
   THE SYSTEM SHALL NOT store plaintext passwords in any medium.
   THE SYSTEM SHALL NOT expose internal stack traces in HTTP responses.
   ```

5. **Write acceptance criteria**
   Each requirement needs 1+ verifiable acceptance criteria:
   ```
   Given [precondition]
   When [action]
   Then [expected outcome with measurable result]
   ```

6. **Non-functional requirements**
   Always include:
   - Performance: expected response time, throughput
   - Security: data classification, access control requirements
   - Accessibility: WCAG level (if UI feature)
   - Scalability: expected load, growth projections

7. **Out of scope section**
   Explicitly list what this feature does NOT include. This prevents scope creep.

8. **Present PRD to human for approval**
   Say: "Here is the PRD. Please review and approve before I proceed to architecture/planning."

9. **After approval: create SDLC checkpoint S01**
   - Invoke sdlc-checkpoint.skill → creates SESSION_SNAPSHOT/S01_requirements.md
   - Updates PROJECT_STATE.md → current phase: S02_DESIGN

## Constraints
- NEVER skip the ambiguity layer — unresolved ambiguity is the #1 cause of rework
- NEVER start planning or implementation without human approval of the PRD
- All requirements must be EARS-formatted and verifiable (not vague like "fast" or "user-friendly")
- Use the PRD template in templates/product/PRD_TEMPLATE.md

## Output Format
Completed PRD.md file at project root (or docs/) using templates/product/PRD_TEMPLATE.md structure.
