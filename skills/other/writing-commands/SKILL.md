---
name: writing-commands
description: Use when creating new commands, editing existing commands, or reviewing command quality. Triggers on "write command", "new command", "review command", "fix command"
---

# Writing Commands

**Announce:** "Using writing-commands skill for command creation, editing, or review."

<ROLE>
Command Architect. Your reputation depends on commands that agents execute correctly under pressure, not documentation that reads well but gets skipped. A command that an agent misinterprets or shortcuts is a failure, regardless of how polished it looks.
</ROLE>

<analysis>
Commands are direct prompts, not orchestrated workflows. They load into the agent's context in full and execute inline. This makes them fundamentally different from skills: commands must be self-contained, unambiguous, and structured so that an agent reading top-to-bottom knows exactly what to do at every step.
</analysis>

<reflection>
After completing any phase, verify:
- Does the command meet all Quality Checklist items?
- Are execution steps imperative, not suggestive?
- Does every conditional have both branches specified?
- Is the FORBIDDEN section specific enough to close real loopholes?
</reflection>

## Invariant Principles

1. **Commands are direct prompts**: A command loads entirely into context. No phases dispatch to subagents. No orchestration layer. The agent reads it and does the work.
2. **Structure enables scanning**: Agents under pressure skim. Sections, tables, and code blocks catch the eye. Prose paragraphs get skipped.
3. **FORBIDDEN closes loopholes**: Every command needs explicit negative constraints. Agents rationalize under pressure. Each excuse needs a counter.
4. **Reasoning tags force deliberation**: `<analysis>` before action, `<reflection>` after. Without these, agents skip straight to output.
5. **Paired commands share a contract**: If command A creates artifacts, command B must know exactly how to find and remove them. The manifest/contract is the interface.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Command purpose | Yes | What the command should accomplish when invoked |
| Trigger phrase | Yes | The `/command-name` that invokes it |
| Existing command | No | Path to command being reviewed or edited |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Command file | `commands/<name>.md` | Complete command following schema |
| Review report | Inline | Quality assessment against checklist (review mode) |

## Phase Overview

| Phase | Name | Purpose | Command |
|-------|------|---------|---------|
| 1 | Create | Schema, naming, required/optional sections, example, token efficiency | `/writing-commands-create` |
| 2 | Review | Quality checklist, anti-patterns, review protocol, testing protocol | `/writing-commands-review` |
| 3 | Paired | Paired command protocol, assessment framework integration | `/writing-commands-paired` |

---

## Phase 1: Create Command

Define command structure using the schema: file naming, frontmatter, required sections, optional sections, and token efficiency targets.

**Execute:** `/writing-commands-create`

**Outputs:** Command file at `commands/<name>.md`

**Self-Check:** Frontmatter present, all required sections included, imperative language used, token targets met.

---

## Phase 2: Review Command

Run the quality checklist against the command. Score structure, content quality, behavioral correctness, and anti-pattern avoidance. Follow the review and testing protocols.

**Execute:** `/writing-commands-review`

**Outputs:** Review report with score, passing/failing checks, critical issues.

**Self-Check:** All checklist items evaluated, score calculated, critical issues flagged.

---

## Phase 3: Paired Commands

When a command creates artifacts, ensure a paired removal command exists with proper manifest, discovery, safety, and verification contracts.

**Execute:** `/writing-commands-paired`

**Outputs:** Paired command file, cross-references in both commands.

**Self-Check:** Manifest format defined, both commands cross-reference each other, removal is safe.

---

<FORBIDDEN>
- Creating commands without a MISSION section
- Omitting FORBIDDEN section (every command needs explicit prohibitions)
- Writing execution steps as prose paragraphs instead of numbered steps
- Leaving conditional branches undefined ("if it works..." without "if it fails...")
- Creating artifact-producing commands without a paired removal command
- Putting workflow descriptions in the frontmatter description
- Using "consider", "you might", "perhaps" in execution steps (use imperatives)
- Omitting `<analysis>` or `<reflection>` tags
- Reviewing commands without running the full Quality Checklist
- Hardcoding project paths without discovery/detection steps
</FORBIDDEN>

## Self-Check

Before completing command creation or review:

- [ ] Frontmatter has `description` field with triggers, not workflow
- [ ] MISSION section is one clear paragraph
- [ ] ROLE tag has domain expert + stakes
- [ ] 3-5 Invariant Principles, each testable
- [ ] Execution steps are numbered and imperative
- [ ] Every step that can fail has a failure path
- [ ] Output section has concrete format
- [ ] FORBIDDEN section has 5+ specific prohibitions
- [ ] Analysis tag prompts pre-action reasoning
- [ ] Reflection tag asks specific verification questions
- [ ] If paired: partner command referenced, manifest format defined

If ANY unchecked: STOP and fix before declaring complete.

<FINAL_EMPHASIS>
Commands are the atomic unit of agent behavior. A well-written command is a contract between the author and every future agent that loads it. Ambiguity in that contract means agents will do the wrong thing under pressure. Precision in that contract means agents do the right thing even when rushed. Write for the agent under pressure, not the calm reviewer reading at leisure.
</FINAL_EMPHASIS>
