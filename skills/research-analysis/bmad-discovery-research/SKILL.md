---
name: bmad-discovery-research
description: Brainstorms ideas and researches projects.
allowed-tools: ["Read", "Write", "Grep"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "I have an idea"
      - "What if we"
      - "Help me think"
      - "explore possibilities"
      - "I'm thinking about"
      - "brainstorm"
      - "research"
    keywords:
      - idea
      - brainstorm
      - explore
      - research
      - thinking
      - discovery
      - analyze
  capabilities:
    - brainstorming
    - research
    - competitive-analysis
    - discovery
    - problem-exploration
  prerequisites: []
  outputs:
    - discovery-brief
    - research-notes
    - problem-statement
---

# Discovery Analysis Skill

## When to Invoke

**Automatically activate this skill when the user:**
- Says "I have an idea...", "What if we...", "I'm thinking about..."
- Asks "Help me think through...", "Can you help me brainstorm...", "Let's explore..."
- Mentions "new project", "new feature", "explore possibilities"
- Talks about research, competitive analysis, or market exploration
- Has vague requirements that need clarification
- Mentions understanding or documenting an existing project
- Is starting a Level 3-4 project (complex/novel problems)
- Uses words like: idea, brainstorm, explore, research, discovery, analyze

**Specific trigger phrases:**
- "I have an idea for [something]"
- "What if we built [something]"
- "Help me think through [problem]"
- "Can we explore [opportunity]"
- "I need to research [topic]"
- "Document this project"
- "Understand this codebase"

**Do NOT invoke when:**
- User already has a detailed PRD (use bmad-product-planning instead)
- User is asking for implementation help (use bmad-development-execution instead)
- User has clear, well-defined requirements (skip to bmad-product-planning)
- User is asking about workflow status (use main-workflow-router)
- Project is Level 0-2 and requirements are clear (skip to bmad-product-planning)

## Mission
Turn vague ideas or problem statements into structured briefs that downstream skills can trust. Identify goals, constraints, risks, and unknowns to inform product planning.

## Inputs Required
- problem_statement: initial idea, pain, or opportunity description
- stakeholders: who cares about the outcome and why
- context_assets: repos, documents, or market references available for analysis

If essential context is missing, gather it before deeper synthesis.

## Outputs
- Discovery brief following patterns in `REFERENCE.md`
- **Brainstorm notes** (from `assets/brainstorm-template.md.template`)
- **Product brief** (from `assets/product-brief-template.md.template`)
- **Research dossier** (from `assets/research-dossier-template.md.template`)
- Prioritized questions and risk register captured for product-requirements skill
- Recommendation on readiness to progress or need for further discovery

**Template locations:** `.claude/skills/bmad-discovery-research/assets/*.template`

## Process
1. Validate entry criteria in `CHECKLIST.md` and classify project complexity.
2. Conduct desk research across provided assets; cite sources.
3. Frame insights into concise problem summary, goals, personas, and constraints (use templates in `assets/`).
4. Document open questions, assumptions, and risks with recommended owners.
5. Deliver summary plus links to created artifacts for the orchestrator and stakeholders.

**Note on automation:** This skill currently operates through collaborative conversation using templates. No automation scripts are required—artifacts are generated manually using Jinja2 templates from `assets/`. See `scripts/README.md` for future automation roadmap.

## Quality Gates
Confirm `CHECKLIST.md` is satisfied before signaling readiness for planning. Missing data or low confidence requires escalation.

## Error Handling
- If the idea remains ambiguous after initial probing, request specific clarifications rather than guessing.
- Flag conflicting stakeholder goals and recommend alignment conversations.
- When scope is too small (Level 0-1), suggest redirecting to lighter-weight workflows documented in `REFERENCE.md`.
