---
name: 021-problem-framing
description: Use when a problem or issue needs explicit framing before deeper analysis begins — establishing the Problem statement, Current state, Desired state, Stakeholders, and Success criteria. This should trigger when an issue's Problem Framing point of view needs evaluation, or when a maintainer directly asks to frame a problem before root-cause analysis, design, or planning begins. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.18.0
---
# Problem Framing

Guide production of a Problem statement, Current state, Desired state, Stakeholders, and Success criteria for a problem or issue under exploration. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Stating the problem independently of any specific solution
- Describing the current state using observable facts
- Describing the desired state as an outcome, not an implementation mechanism
- Identifying stakeholders affected by, accountable for, or informed about the problem
- Defining success criteria that make problem resolution verifiable
- Feeding a clarified problem frame into `022-root-cause-analysis` and the remaining Functional Specification lenses

## Constraints

Frame the problem before any deeper analysis. When this technique is orchestrated by another workflow, the orchestrator owns clarifying-question sequencing; when applied standalone, ask directly.

- **MUST** read `references/021-problem-framing.md` before applying Problem Framing guidance
- **MUST** state the problem independently of any specific solution, technology, or implementation
- **MUST** describe the current state using observable facts, not opinions or assumed causes
- **MUST** describe the desired state as an outcome or capability, not a specific mechanism
- **MUST** identify stakeholders affected by, accountable for, or informed about the problem, not only the requester
- **MUST** define success criteria that are observable or measurable
- **MUST NOT** invent a problem statement, state, stakeholder, or success criterion when the available content is vague or ambiguous; flag the gap for a clarifying question instead

## When to use this skill

- Frame this problem before deeper analysis
- Apply problem framing to this issue
- Establish the problem statement, current state, and desired state
- Identify stakeholders and success criteria for this problem
- Draft the Problem Framing section of a Functional Specification

## Workflow

1. **Read the Reference**

Read `references/021-problem-framing.md`, then identify what evidence is already available for the problem statement, current state, desired state, stakeholders, and success criteria.

2. **Separate the Problem from any Solution**

Strip out wording that already assumes a fix, technology, or implementation, and restate the gap in observable terms.

3. **Describe Current and Desired State**

Describe the current state as observable facts and the desired state as a target outcome or capability.

4. **Identify Stakeholders and Success Criteria**

List stakeholders affected by, accountable for, or informed about the problem, then define observable or measurable success criteria.

5. **Report the Problem Frame**

Report the Problem statement, Current state, Desired state, Stakeholders, and Success criteria, and flag any field left open pending a clarifying answer.

## Reference

For detailed guidance, examples, and constraints, see [references/021-problem-framing.md](references/021-problem-framing.md).
