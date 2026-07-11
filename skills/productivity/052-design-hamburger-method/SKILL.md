---
name: 052-design-hamburger-method
description: Use when a large feature, story, plan, or spec idea needs to be split into small vertical slices with the Hamburger Method. This should trigger for requests such as Split this oversized story; Find the smallest useful slice; Break this feature into vertical slices; Apply the Hamburger Method; Turn this broad plan into tracked slices. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.17.0
---
# Hamburger Method Design

Guide Java teams through the Hamburger Method for splitting oversized work into small, valuable, end-to-end vertical slices. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Recognizing oversized feature, story, plan, or spec work
- Identifying 3-6 functional or workflow layers that participate in delivering value
- Generating 4-5 implementation or quality options per layer
- Challenging scope with the smallest useful version question
- Filtering options that are too costly, redundant, irreversible, or unnecessary for early learning
- Composing one first vertical slice and follow-up slices
- Self-checking value, size, testability, deliverability, and issue-tracking suitability
- Routing plan, OpenSpec, GitHub issue, and Jira follow-up through the existing planning skills

## Constraints

Split oversized work into vertical slices that deliver observable value, not isolated horizontal technical tasks.

- **MUST** read `references/052-design-hamburger-method.md` before applying the method
- **MUST** identify 3-6 functional or workflow layers before selecting a slice
- **MUST** generate 4-5 options per layer, ordered from simplest acceptable option to richer options
- **MUST** challenge scope with the smallest-useful-version question before recommending a first slice
- **MUST** filter costly, redundant, irreversible, or unnecessary options before composing the first slice
- **MUST** keep recommended work as vertical slices that deliver observable value
- **MUST NOT** present isolated technical layers as independently shippable stories

## When to use this skill

- Apply the Hamburger Method
- Split this oversized story
- Find the smallest useful slice
- Break this feature into vertical slices
- Turn this broad plan into tracked slices
- This feature is too large

## Workflow

1. **Recognize Oversized Work**

Read `references/052-design-hamburger-method.md`, then restate the large feature, story, plan, or spec idea and why ordinary implementation task decomposition would be too broad, risky, or horizontal.

2. **Map Layers and Options**

Identify 3-6 functional or workflow layers needed for observable value. For each layer, generate 4-5 implementation or quality options ordered from the simplest acceptable choice to richer choices.

3. **Challenge Scope**

Ask: "If this had to ship tomorrow, what would be the smallest useful version?" Use the answer to remove options that are too costly, redundant, irreversible, or unnecessary for early learning.

4. **Compose the First Slice**

Select one option from each relevant layer to create the smallest useful end-to-end vertical slice. Explain the user-visible value, validation signal, and why rejected layer options wait for later slices.

5. **Plan Follow-Up Slices**

Propose follow-up vertical slices that incrementally improve quality, automation, robustness, reach, observability, operational behavior, or supported workflows without turning them into isolated technical layers.

6. **Self-Check and Route Follow-Up**

Check every slice for value, size, testability, deliverability, and issue-tracking suitability. Route implementation planning through `041-planning-plan-mode`, spec-level changes through `042-planning-openspec`, GitHub issue work through `043-planning-github-issues`, Jira work through `044-planning-jira`, and Azure DevOps work through `045-planning-azure-devops`.

## Reference

For detailed guidance, examples, and constraints, see [references/052-design-hamburger-method.md](references/052-design-hamburger-method.md).
