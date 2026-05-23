---
name: skill-editor
description: Use when drafting or revising an agent skill spec in an environment that already has a general skill creator. Apply user-specific preferences to tighten triggers, reduce redundancy, keep scope safe, and keep the spec compact and consistent.
metadata:
  short-description: Refine skill specs
---


# Skill Editor

Refine an agent skill specification by applying user-specific preferences on top of an existing skill-creation workflow. Improve trigger precision, internal consistency, and compactness without expanding scope.

## Activation

Use this skill only when the task is to write, revise, or review an agent skill spec.

## Metadata First

* Put trigger conditions and the goal in the header metadata.
* Do not restate the trigger in the body.
* Keep the body focused on execution rules and constraints.

## Scope Control

* Default to localized edits unless a full rewrite is explicitly requested.
* Avoid adding new features, categories, or policies not implied by the user’s request.
* If information is missing, make safe progress and ask only the smallest clarification needed to avoid incorrect constraints.

## Redundancy Control

* Remove repeated statements across sections.
* Replace explanatory prose with concise definitions when possible.
* Keep examples minimal and only when they clarify an otherwise ambiguous rule.

## Neutral Examples

* Use generic examples that do not imply a specific organization, product, or domain.
* Examples should demonstrate the rule, not introduce new conventions.

## Consistency Checks

Before finalizing a spec, ensure:

* Metadata and body have distinct roles and do not duplicate content.
* Terms are used consistently and defined once.
* Rules do not conflict; when tradeoffs exist, the priority is explicit.
* Output expectations are clear and bounded.
