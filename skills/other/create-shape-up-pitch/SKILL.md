---
name: create-shape-up-pitch
description: Write a Shape Up pitch with problem, appetite, solution sketch, rabbit holes, and no-gos when the user asks to pitch a feature, shape work, or write a Shape Up proposal
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[feature or problem to pitch]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: product, shape-up, planning
---

# Create Shape Up Pitch

## Overview

Generate a pitch following the Shape Up methodology (Ryan Singer / Basecamp). A pitch defines the problem, sets a fixed time budget (appetite), sketches a solution at the right level of abstraction, identifies rabbit holes to avoid, and declares explicit no-gos. This gives teams enough direction to build without over-specifying the solution.

## Workflow

1. **Read product context** -- Scan `.chalk/docs/product/` for the product profile, related PRDs, and JTBD docs. Check `.chalk/docs/engineering/` for architecture docs that inform feasibility. Understand the existing system before shaping new work.

2. **Parse the feature** -- Extract from `$ARGUMENTS` the problem or feature to pitch. If `$ARGUMENTS` describes a solution rather than a problem, dig back to the underlying need and reframe.

3. **Determine the next file number** -- Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

4. **Write the Problem section** -- Describe the problem from the user's perspective. Include: who has this problem, when they encounter it, and what the current workaround is. Ground it in specific scenarios, not abstract statements.

5. **Set the Appetite** -- Define the fixed time budget (typically 2 or 6 weeks in Shape Up). The appetite is a constraint, not an estimate. State what the team should be willing to spend and why that budget is appropriate for the value delivered.

6. **Sketch the Solution** -- Describe the solution at fat-marker sketch level: broad strokes, key affordances, critical flows. Do not specify UI details, exact copy, or implementation. Show enough that a team can start building but has room to make design decisions.

7. **Identify Rabbit Holes** -- List specific risks, technical unknowns, or scope traps that could consume the entire appetite. For each, explain why it is a risk and suggest how to avoid or de-risk it.

8. **Declare No-Gos** -- Explicitly list what is NOT included in this pitch, even if someone might reasonably expect it. These are intentional scope cuts that keep the work within the appetite.

9. **Write the file** -- Save to `.chalk/docs/product/<n>_pitch_<feature-slug>.md`.

10. **Confirm** -- Share the file path and highlight the biggest rabbit hole that needs attention before betting on this pitch.

## Output

- **File**: `.chalk/docs/product/<n>_pitch_<feature-slug>.md`
- **Format**: Plain markdown with Problem, Appetite, Solution, Rabbit Holes, and No-Gos sections
- **First line**: `# Pitch: <Feature Name>`

## Anti-patterns

- **Over-specified solution** -- Wireframes, pixel-perfect mockups, and detailed specs defeat the purpose. The solution should be at fat-marker level -- broad strokes that leave room for the building team to make decisions.
- **Appetite as estimate** -- "We estimate this will take 4 weeks" is not an appetite. An appetite is a deliberate constraint: "This problem is worth at most 6 weeks. If we cannot solve it in 6 weeks, we will not do it."
- **No rabbit holes section** -- Every pitch has risks. If the rabbit holes section is empty, the pitch has not been shaped thoroughly enough. Revisit and think about what could go wrong.
- **Problem described as absence of solution** -- "We do not have feature X" is not a problem. "Users cannot accomplish Y, so they do Z workaround which costs them time" is a problem.
- **No-gos that are obvious** -- "We will not rewrite the entire backend" is not a useful no-go. No-gos should be things a reasonable person might expect to be included but that are intentionally cut.
