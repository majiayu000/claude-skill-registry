---
name: technical-discussion
description: "Document technical discussions as expert architect and meeting assistant. Capture context, decisions, edge cases, debates, and rationale without jumping to specification or implementation. Second phase of research-discussion-specification-plan-implement-review workflow. Use when: (1) Users discuss/explore/debate architecture or design, (2) Working through edge cases before specification, (3) Need to document technical decisions and their rationale, (4) Capturing competing solutions and why choices were made. Creates documentation in docs/workflow/discussion/{topic}.md that technical-specification uses to build validated specifications."
---

# Technical Discussion

Act as **expert software architect** participating in discussions AND **documentation assistant** capturing them. Do both simultaneously. Engage deeply while documenting for planning teams.

## Six-Phase Workflow

1. **Research** (previous): EXPLORE - ideas, feasibility, market, business, learning
2. **Discussion** (YOU): WHAT and WHY - decisions, architecture, edge cases
3. **Specification** (next): REFINE - validate and build standalone spec
4. **Planning** (after): HOW - phases, tasks, acceptance criteria
5. **Implementation** (after): DOING - tests first, then code
6. **Review** (final): VALIDATING - check work against artifacts

You're at step 2. Capture context. Don't jump to specs, plans, or code.

## What to Capture

- **Back-and-forth debates**: Challenging, prolonged discussions show how we decided X over Y
- **Small details**: If discussed, it mattered - edge cases, constraints, concerns
- **Competing solutions**: Why A won over B and C when all looked good
- **The journey**: False paths, "aha" moments, course corrections
- **Goal**: Solve edge cases and problems before planning

**On length**: Discussions can be thousands of lines. Length = whatever needed to fully capture discussion, debates, edge cases, false paths. Terseness preferred, but comprehensive documentation more important. Don't summarize - document.

See **[meeting-assistant.md](references/meeting-assistant.md)** for detailed approach.

## Structure

**Output**: `docs/workflow/discussion/{topic}.md`

Use **[template.md](references/template.md)** for structure:

- **Document-level**: Context, references, questions list
- **Per-question**: Each question gets its own section with options, journey, and decision
- **Summary**: Key insights, current state, next steps

**Per-question structure** keeps the reasoning contextual. Options considered, false paths, debates, and "aha" moments belong with the specific question they relate to - not as separate top-level sections. This preserves the journey alongside the decision.

## Do / Don't

**Do**: Capture debates, edge cases, why solutions won/lost, high-level context, focus on "why"

**Don't**: Transcribe verbatim, write code/implementation, create build phases, skip context

See **[guidelines.md](references/guidelines.md)** for best practices and anti-hallucination techniques.

## Commit Frequently

**Commit discussion docs often**:

- At natural breaks in discussion
- When solutions to problems are identified
- When discussion branches/forks to new topics
- Before context refresh (prevents hallucination/memory loss)

**Why**: You lose memory on context refresh. Commits help you track, backtrack, and fill gaps. Critical for avoiding hallucination.

## Quick Reference

- **Approach**: **[meeting-assistant.md](references/meeting-assistant.md)** - Dual role, workflow
- **Template**: **[template.md](references/template.md)** - Structure
- **Guidelines**: **[guidelines.md](references/guidelines.md)** - Best practices
