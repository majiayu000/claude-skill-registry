---
name: plan-cro
version: 1.0.0
description: '[Planning] Create a CRO plan for the given content'
disable-model-invocation: false
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

> **Skill Variant:** Variant of `/plan` — specialized for CRO (Conversion Rate Optimization) planning.

## Quick Summary

**Goal:** Create a CRO (Conversion Rate Optimization) plan for the given content or feature.

**Workflow:**

1. **Analyze** — Review current content/feature for conversion bottlenecks
2. **Research** — Identify CRO best practices and A/B test opportunities
3. **Plan** — Create actionable CRO improvement plan with measurable goals

**Key Rules:**

- PLANNING-ONLY: do not implement, only create CRO plan
- Focus on user behavior, conversion funnels, and measurable outcomes
- Always offer `/plan-review` after plan creation

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## PLANNING-ONLY — Collaboration Required

> **DO NOT** use the `EnterPlanMode` tool — you are ALREADY in a planning workflow.
> **DO NOT** implement or execute any code changes.
> **COLLABORATE** with the user: ask decision questions, present options with recommendations.
> After plan creation, ALWAYS run `/plan-review` to validate the plan.
> ASK user to confirm the plan before any next step.

You are an expert in conversion optimization. Analyze the content based on the given issues:
<issues>$ARGUMENTS</issues>

Activate `planning` skill.

**IMPORTANT:** Analyze the skills catalog and activate the skills that are needed for the task during the process.
**IMPORTANT:** Sacrifice grammar for the sake of concision when writing outputs.

## Conversion Optimization Framework

1. Headline 4-U Formula: **Useful, Unique, Urgent, Ultra-specific** (80% won't read past this)
2. Above-Fold Value Proposition: Customer problem focus, no company story, zero scroll required
3. CTA First-Person Psychology: "Get MY Guide" vs "Get YOUR Guide" (90% more clicks)
4. 5-Field Form Maximum: Every field kills conversions, progressive profiling for the rest
5. Message Match Precision: Ad copy, landing page headline, broken promises = bounce
6. Social Proof Near CTAs: Testimonials with faces/names, results, placed at decision points
7. Cognitive Bias Stack: Loss aversion (fear), social proof (FOMO), anchoring (pricing)
8. PAS Copy Framework: Problem > Agitate > Solve, emotion before logic
9. Genuine Urgency Only: Real deadlines, actual limits, fake timers destroy trust forever
10. Price Anchoring Display: Show expensive option first, make real price feel like relief
11. Trust Signal Clustering: Security badges, guarantees, policies all visible together
12. Visual Hierarchy F-Pattern: Eyes scan F-shape, put conversions in the path
13. Lead Magnet Hierarchy: Templates > Checklists > Guides (instant > delayed gratification)
14. Objection Preemption: Address top 3 concerns before they think them, FAQ near CTA
15. Mobile Thumb Zone: CTAs where thumbs naturally rest, not stretching required
16. One-Variable Testing: Change one thing, measure impact, compound wins over time
17. Post-Conversion Momentum: Thank you page sells next step while excitement peaks
18. Cart Recovery Sequence: Email in 1 hour, retarget in 4 hours, incentive at 24 hours
19. Reading Level Grade 6: Smart people prefer simple, 11-word sentences, short paragraphs
20. TOFU/MOFU/BOFU Logic: Awareness content ≠ decision content, match intent precisely
21. White Space = Focus: Empty space makes CTAs impossible to miss, crowded = confused
22. Benefit-First Language: Features tell, benefits sell, transformations compel
23. Micro-Commitment Ladder: Small yes leads to big yes, start with email only
24. Performance Tracking Stack: Heatmaps show problems, recordings show why, events show what
25. Weekly Optimization Ritual: Review metrics Monday, test Tuesday, iterate or scale

## Workflow

- If the user provides a screenshots or videos, use `ai-multimodal` skill to describe as detailed as possible the issue, make sure the CRO analyst can fully understand the issue easily based on the description.
- If the user provides a URL, use `web_fetch` tool to fetch the content of the URL and analyze the current issues.
- You can use screenshot capture tools along with `ai-multimodal` skill to capture screenshots of the exact parent container and analyze the current issues with the appropriate Gemini analysis skills (`ai-multimodal`, `gemini-video-understanding`, or `gemini-document-processing`).
- Use `/scout-ext` (preferred) or `/scout` (fallback) slash command to search the codebase for files needed to complete the task
- Use `planner` agent to create a comprehensive CRO plan following the progressive disclosure structure:
    - Create a directory using naming pattern from `## Naming` section.
    - Every `plan.md` MUST start with YAML frontmatter:

        ```yaml
        ---
        title: '{Brief title}'
        description: '{One sentence for card preview}'
        status: pending
        priority: P2
        effort: { sum of phases, e.g., 4h }
        branch: { current git branch }
        tags: [cro, conversion]
        created: { YYYY-MM-DD }
        ---
        ```

    - Save the overview access point at `plan.md`, keep it generic, under 80 lines, and list each phase with status/progress and links.
    - For each phase, add `phase-XX-phase-name.md` files containing sections (Context links, Overview with date/priority/statuses, Key Insights, Requirements, Architecture, Related code files, Implementation Steps, Todo list, Success Criteria, Risk Assessment, Security Considerations, Next steps).
    - Keep every research markdown report concise (≤150 lines) while covering all requested topics and citations.
      **IMPORTANT:** Sacrifice grammar for the sake of concision when writing reports.
      **IMPORTANT:** In reports, list any unresolved questions at the end, if any.

## **IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
- **MANDATORY FINAL TASKS:** After creating all planning todo tasks, ALWAYS add these two final tasks:
    1. **Task: "Run /plan-validate"** — Trigger `/plan-validate` skill to interview the user with critical questions and validate plan assumptions
    2. **Task: "Run /plan-review"** — Trigger `/plan-review` skill to auto-review plan for validity, correctness, and best practices

## REMINDER — Planning-Only Command

> **DO NOT** use `EnterPlanMode` tool.
> **DO NOT** start implementing.
> **ALWAYS** validate with `/plan-review` after plan creation.
> **ASK** user to confirm the plan before any implementation begins.
> **ASK** user decision questions with your recommendations when multiple approaches exist.
