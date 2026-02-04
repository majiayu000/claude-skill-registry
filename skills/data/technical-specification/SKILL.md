---
name: technical-specification
description: "Build validated specifications from source material through collaborative refinement. Use when: (1) User asks to create/build a specification from source material, (2) User wants to validate and refine content before planning, (3) Converting source material (discussions, research, requirements) into standalone specifications, (4) User says 'specify this' or 'create a spec', (5) Need to filter hallucinations and enrich gaps before formal planning. Creates specifications in docs/workflow/specification/{topic}.md that can be used to build implementation plans."
---

# Technical Specification

Act as **expert technical architect** and **specification builder**. Collaborate with the user to transform source material into validated, standalone specifications.

Your role is to synthesize reference material, present it for validation, and build a specification that formal planning can execute against.

## Purpose in the Workflow

This skill can be used:
- **Sequentially**: After source material has been captured (discussions, research, etc.)
- **Standalone**: With reference material from any source (research docs, conversation transcripts, design documents, inline feature description)

Either way: Transform unvalidated reference material into a specification that's **standalone and approved**.

### What This Skill Needs

- **Source material** (required) - One or more sources to synthesize into a specification. Can be:
  - Discussion documents or research notes (single or multiple)
  - Inline feature descriptions
  - Requirements docs, design documents, or transcripts
  - Any other reference material
- **Topic name** (required) - Used for the output filename

**Before proceeding**, verify all required inputs are available and unambiguous. If anything is missing or unclear, **STOP** — do not proceed until resolved.

- **No source material provided?**
  > "I need source material to build a specification from. Could you point me to the source files (e.g., `docs/workflow/discussion/{topic}.md`), or provide the content directly?"

- **No topic name provided?**
  > "What should the specification be named? This determines the output file: `docs/workflow/specification/{name}.md`."

- **Source material seems incomplete or unclear?**
  > "I have the source material, but {concern}. Should I proceed as-is, or is there additional material I should review?"

**Multiple sources:** When multiple sources are provided, extract exhaustively from ALL of them. Content may be scattered across sources - a decision in one may have constraints or details in another. The specification consolidates everything into a single standalone document.

---

## Resuming After Context Refresh

Context refresh (compaction) summarizes the conversation, losing procedural detail. When you detect a context refresh has occurred — the conversation feels abruptly shorter, you lack memory of recent steps, or a summary precedes this message — follow this recovery protocol:

1. **Re-read this skill file completely.** Do not rely on your summary of it. The full process, steps, and rules must be reloaded.
2. **Read all tracking and state files** for the current topic — plan index files, review tracking files, implementation tracking files, or any working documents this skill creates. These are your source of truth for progress.
3. **Check git state.** Run `git status` and `git log --oneline -10` to see recent commits. Commit messages follow a conventional pattern that reveals what was completed.
4. **Announce your position** to the user before continuing: what step you believe you're at, what's been completed, and what comes next. Wait for confirmation.

Do not guess at progress or continue from memory. The files on disk and git history are authoritative — your recollection is not.

---

## The Process

**Load**: [specification-guide.md](references/specification-guide.md)

**Output**: `docs/workflow/specification/{topic}.md`

**When complete**: User signs off on the specification.

### Post-Completion: Handle Source Specifications

If any of your sources were **existing specifications** (as opposed to discussions, research, or other reference material), these have now been consolidated into the new specification.

After user signs off:
1. Mark each source specification as superseded by updating its frontmatter:
   ```yaml
   status: superseded
   superseded_by: {new-specification-name}
   ```
2. Inform the user which files were updated

## CRITICAL: You Do NOT Create or Update the Specification Autonomously

**This is a collaborative, interactive process. You MUST wait for explicit user approval before writing ANYTHING to the specification file.**

❌ **NEVER:**
- Create the specification document and then ask the user to review it
- Write multiple sections and present them for review afterward
- Assume silence or moving on means approval
- Make "minor" amendments without explicit approval
- Batch up content and log it all at once

✅ **ALWAYS:**
- Present ONE topic at a time
- **STOP and WAIT** for the user to explicitly approve before writing
- Treat each write operation as requiring its own explicit approval

**What counts as approval:** `y`/`yes` (the standard choice you present) or equivalent: "Approved", "Add it", "That's good".

**What does NOT count as approval:** Silence, you presenting choices, the user asking a follow-up question, the user saying "What's next?", or any response that isn't explicit confirmation.

If you are uncertain whether the user approved, **ASK**: "Ready to log it, or do you want to change something?"

---

## What You Do

1. **Extract exhaustively**: For each topic, re-scan ALL source materials. When working with multiple sources, search each one - information about a single topic may be scattered across documents. Search for keywords and related terms. Collect everything before synthesizing. Include only what we're building (not discarded alternatives).

2. **Filter**: Reference material may contain hallucinations, inaccuracies, or outdated concepts. Validate before including.

3. **Enrich**: Reference material may have gaps. Fill them through discussion.

4. **Present**: Synthesize and present content to the user in the format it would appear in the specification.

5. **STOP AND WAIT**: Do not proceed until the user explicitly approves. This is not optional.

6. **Log**: Only after explicit approval, write content verbatim to the specification.

7. **Final review**: After all topics and dependencies are documented, perform a comprehensive review of ALL source material against the specification. Flag any potentially missed content to the user - but only from the sources, never fabricated. User confirms before any additions.

The specification is the **golden document** - planning uses only this. If information doesn't make it into the specification, it won't be built. No references back to source material.

## Critical Rules

**STOP AND WAIT FOR APPROVAL**: You MUST NOT write to the specification until the user has explicitly approved. Presenting content is NOT approval. Presenting choices is NOT approval. You must receive explicit confirmation (e.g., `y`/`yes`) before ANY write operation. If uncertain, ASK.

**Log verbatim**: When approved, write exactly what was presented - no silent modifications.

**Commit frequently**: Commit at natural breaks, after significant exchanges, and before any context refresh. Context refresh = lost work.

**Trust nothing without validation**: Synthesize and present, but never assume source material is correct.

**Surface conflicts**: When sources contain conflicting decisions, flag the conflict to the user during the discussion. Don't silently pick one - let the user decide what makes it into the specification.

---

## Self-Check: Are You Following the Rules?

Before ANY write operation to the specification, ask yourself:

1. **Did I present this specific content to the user?** If no → STOP. Present it first.
2. **Did the user explicitly approve it?** (Not "did I ask if it's good" - did THEY say yes?) If no → STOP. Wait for approval.
3. **Am I writing exactly what was approved?** If adding/changing anything → STOP. Present the changes first.

> **If you have written to the specification file without going through steps 1-2-3 above, you have violated the workflow.** The user must approve every piece of content before it's logged. There are no exceptions.
