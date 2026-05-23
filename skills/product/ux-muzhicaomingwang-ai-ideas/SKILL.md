---
name: ux
description: Product management UX skill for designing user journeys, information architecture, interaction flows, wireframe-level specs, usability heuristics, and experiment-driven iteration. Use for tasks like refining PRDs with UX requirements, defining success metrics, writing microcopy, accessibility considerations, and conducting user testing plans.
---

# ux

Use this skill for PM 视角的 UX 设计与评审：从需求到体验闭环。

## Outputs (choose what the task needs)

- User journeys / storyboards
- Information architecture (IA) + navigation map
- Key flows (happy path + edge cases) with states
- Wireframe-level spec (components, behavior, copy)
- UX acceptance criteria (可测试的验收标准)
- Metrics and experiment plan (A/B, funnel, retention)

## Workflow

1) Clarify users and jobs
- ICPs, triggers, JTBD / Job Story.
- Define “success” in measurable outcomes.

2) Map journeys and flows
- Identify critical journeys; pick 1–2 primary flows first.
- Define states: empty/loading/error/success/permission denied.
- Define drop-off points and recovery paths.

3) Information architecture
- Group content by user mental model.
- Keep navigation shallow; avoid hidden complexity in MVP.
- Name things consistently with domain language.

4) Interaction design principles
- Reduce cognitive load: progressive disclosure, sensible defaults.
- Make system status visible (progress, confirmations, undo).
- Prevent errors; when errors happen, provide recovery.
- Keep copy short, specific, and action-oriented.

5) Accessibility & inclusivity
- Keyboard/gesture alternatives where applicable.
- Color contrast, dynamic text, screen reader labels.
- Avoid relying on color alone to convey meaning.

6) Metrics & experiments
- Define funnel events and North Star Metric.
- Prioritize experiments tied to a hypothesis with guardrails.

7) Usability testing plan
- Script tasks, success criteria, and note-taking template.
- Recruit target users; run quick iterative rounds (5–8 users).

## UX acceptance criteria template

- Given [context], when [user action], then [expected behavior].
- Empty state: [copy + CTA + example].
- Error state: [message + retry + fallback].
- Loading: [skeleton/spinner + timeout handling].

