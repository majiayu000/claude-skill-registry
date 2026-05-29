---
name: writing-agents-md
description: Teach an agent how to create a high-quality AGENTS.md file for a code project, including structure, rules, conventions, and examples. Use when the user requests guidance or generation of an AGENTS.md file.
license: MIT
metadata:
  author: Ron Dekker <rondekker.nl>
---

# Writing AGENTS.md

## When to use this skill
Use this skill when the user explicitly requests:
1. Generation of a new AGENTS.md file for a repository.
2. Review or improvement of an existing AGENTS.md.
3. Conversion of project conventions into agent-actionable guidance.

Base the output on best practices for agent guidance, project conventions,
explicit rules, and examples.

## Objective
Produce an AGENTS.md that:
1. Is **clear and unambiguous** about agent behavior expectations.
2. Includes **explicit rules, boundaries, and escalation points**.
3. Is **actionable and machine-readable** (do not rely on narrative prose alone).
4. Provides **commands, conventions, and examples** the agent can follow.
5. Contains **sections relevant to the user’s project context**.

## Structure to output
1. Title and purpose
  - One sentence summarizing the role of the AGENTS.md file for this project.
2. Scope
  - Which agents the file governs (AI assistants, bots, CI tools).
  - Which parts of the project are *in scope* vs *restricted*.
3. Non-negotiable rules
  - Explicit statements of `MUST`, `MUST NOT`, `SHOULD`, or `SHOULD NOT`.
  - Example:
    ```
    MUST NOT modify database schema migrations.
    MUST run tests before proposing a patch.
    ```
4. Project architecture summary
  - A short, bullet list description of the main code boundaries (e.g., frontend/backend layers, APIs, core modules).
5. Coding and workflow conventions
  - Toolchain commands (e.g. build/test/lint) with exact flags the agent should use.
  - Formatting, error handling, commit conventions.
6. Testing and validation requirements
  - Explicit instructions on when tests must be added or updated.
  - Expected test commands to run and criteria to meet.
7. Change and escalation policies
  - When the agent **must stop and ask for human approval**.
    Example: “If a breaking API change is required, prompt for approval.”
8. Examples
  - Minimal examples showing correct application of key rules.
9. Safety, security, and sensitive areas
  - List areas where modifications are high-risk and require explicit verification.
10. Final checklist
  - A bullet list of items the agent should ensure before submitting changes.

## Output guidelines
- Use **clear, short commands** (no narrative prose) in rules and conventions.
- Avoid generalities; prefer **specific examples or exact commands**.
- Do not assume project context; **ask clarifying questions** if needed.
- Do not generate hypothetical rules; ensure each rule is **relevant to the target repository**.

## Example prompt
When the user asks:
> “Write an AGENTS.md for my TypeScript web app using React and Vitest”
You should prompt:
1. “What are the test, lint, and build commands?”
2. “Which parts of the project should not be modified by an agent?”

Use their answers to tailor the output.

## Edge cases to include
- If the project has *multiple services* (monorepo), clarify **scope by directory**.
- If there are *security-relevant config files*, include explicit error-prevention rules.
- If no explicit test suite exists, generate fallback instructions for test scaffolding.

## Important notes
- The agent should treat **AGENTS.md not as optional commentary, but as a normative contract** for autonomous behaviors.
- Output must be usable by other agent products that understand AGENTS.md semantics (avoid product-specific jargon).
