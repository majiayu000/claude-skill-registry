---
name: automation-language-selection
description: Choose between Shell and Python for generated automation code based on task traits. Use when automation language selection guidance is required.
---
## Purpose

Given a task description and basic characteristics (complexity, data handling, orchestration requirements), suggest Shell vs Python (or hybrid) in a way that is consistent with the governance rule-block and easy for agents to act on.

## IO Semantics

Input: Task description, automation requirements, and high-level complexity indicators.
Output: Language selection decision plus a short rationale suitable for logging or plan text.
Side Effects: May cause agents to load `skill:language-python` or `skill:language-shell` according to the decision.
