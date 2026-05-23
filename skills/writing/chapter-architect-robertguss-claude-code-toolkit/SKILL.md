---
name: chapter-architect
description: Plan and architect a single chapter at beat-level granularity. Use when you have a chapter from the Architecture Document and need to create a detailed outline before drafting. Produces a Chapter Outline Document for use by draft-coach or ghostwriter.
---

# Chapter Architect

Transform a chapter's high-level specification (from book-architect) into a beat-level outline that guides drafting while preserving creative freedom.

## Core Philosophy

1. **Reader-first, always.** Every beat exists to move the reader toward the chapter's destination—intellectually and emotionally.

2. **Compass, not GPS.** The outline points direction and marks waypoints. It does not dictate every turn. The ghostwriter has creative freedom within the structure.

3. **Collaborative partnership.** Claude contributes ideas, challenges weak thinking, and advocates for what serves the reader. The author has final approval on all decisions.

4. **Intent over prescription.** Each beat captures _why_ it exists, not just _what_ it contains. This enables intelligent adaptation during drafting.

5. **Emotional arc matters.** Track not just where the reader is intellectually, but how they _feel_ at each stage of the journey.

## Session Flow

This skill is session-flexible. Simple chapters may complete in one session. Complex chapters may need natural pause points with thinking time between.

### Session Start

1. **Identify context:**
   - New chapter or continuing a previous session?
   - If continuing, request the latest working draft.

2. **Gather inputs:**
   - Architecture Document (chapter specification)
   - Research Dossier (chapter's section)
   - Book Concept Document (reader, promise, voice)
   - Any author notes on this chapter

3. **Confirm which chapter** we're architecting and surface the key specs:
   - Chapter number and working title
   - Chapter's job
   - Reader entry state
   - Reader exit state
   - Key concepts to cover
   - Bridge from previous / to next chapter

### Phase 1: Orient

Review inputs together. Surface any tensions, questions, or issues.

**Key questions to explore:**

- Is this a standard chapter or special type? (introduction, conclusion, case-study, etc.)
  - _If special type, read `references/special-chapter-types.md`_
- Is the research sufficient? Any gaps?
- Are there competing ways to approach this chapter?
- What's the emotional shape of this chapter? (tension→release, confusion→clarity, etc.)
  - _Reference `references/emotional-arc-patterns.md` as needed_

**Claude's role:** Surface concerns, ask probing questions, identify what's unclear or underdeveloped.

**Pause point:** If significant unresolved questions emerge, pause here to resolve them before proceeding.

### Phase 2: Brainstorm Beats

Generate candidate beats without worrying about sequence yet.

**Process:**

1. Review the beat vocabulary together
   - _Read `references/beat-vocabulary.md`_
2. Generate possible beats—both author and Claude contribute
3. Consider opening options
   - _Reference `references/opening-strategies.md`_
4. Consider closing options
   - _Reference `references/closing-strategies.md`_
5. Capture all candidates without judging yet

**Claude's role:** Actively contribute beat ideas, not just record. Suggest moves the author might not have considered. Ask "what about a beat that does X?"

### Phase 3: Sequence and Debate

Put the beats in order. This is where real collaboration happens.

**Process:**

1. Propose an initial sequence
2. Walk through the reader's experience: "They arrive here, then this happens, now they feel..."
3. Debate ordering decisions:
   - Does the counterargument come before or after the main case?
   - Where does the reader need relief or breathing room?
   - What must be established before something else can land?
4. Identify which beats are load-bearing (structural, can't move) vs. flexible
5. Cut beats that aren't earning their place
6. Add beats if gaps emerge

**Claude's role:** Advocate for what serves the reader. Push back when a sequence feels off. Offer alternatives with reasoning.

**Pause point:** If the sequence isn't clicking, pause here. Complex chapters may need marinating time.

### Phase 4: Flesh Out Beats

For each beat in the final sequence, define:

- **Beat name and type** (from vocabulary)
- **What happens** (loosely described—compass, not GPS)
- **Reader destination** (intellectual and emotional—this is non-negotiable)
- **Key material** (specific pointers to research, quotes, examples)
- **Load-bearing flag** (yes/no—can this beat be moved or cut?)
- **Notes** (anything the ghostwriter should know)

**Special attention:** Opening and closing beats get deeper treatment.

- _Reference `references/opening-strategies.md` and `references/closing-strategies.md`_
- Articulate _why_ this opening/closing works
- Note what to avoid
- Identify specific hooks, callbacks, or images to consider

### Phase 5: Review and Finalize

Stress-test the complete arc before producing the document.

**Process:**

1. Claude walks through the reader's experience aloud—beat by beat, tracking intellectual and emotional state
2. Check against common problems
   - _Read `references/common-chapter-problems.md`_
3. Verify the chapter delivers on its job and reaches the exit state
4. Confirm the bridge to the next chapter works
5. Final author approval

**Only after approval:** Produce the Chapter Outline Document using the template.

- _Use `assets/templates/chapter-outline-template.md`_

### Session End

1. Produce the versioned Chapter Outline Document (v1, v2, etc.)
2. Summarize any open questions or flags for the ghostwriter
3. Confirm next steps:
   - Ready for drafting? → Handoff to draft-coach or ghostwriter
   - Need another session? → Note where to resume

## Inputs

| Document              | Source               | Purpose                                                 |
| --------------------- | -------------------- | ------------------------------------------------------- |
| Architecture Document | `book-architect`     | Chapter's job, entry/exit states, key concepts, bridges |
| Research Dossier      | `research-assistant` | Evidence, examples, quotes organized by chapter         |
| Book Concept Document | `book-ideation`      | Reader, promise, thesis, voice, author angle            |
| Author notes          | Author               | Any existing thoughts, fragments, or constraints        |

## Outputs

**Chapter Outline Document** containing:

1. Chapter Context (job, entry/exit states, connections, emotional arc, tone notes)
2. Reader Journey Walkthrough (prose narrative of the experience)
3. Beat Sequence (detailed breakdown of each beat)
4. Opening and Closing Deep Dives (expanded treatment)

See `assets/templates/chapter-outline-template.md` for exact format.

## Readiness Criteria

Before handoff, confirm:

- [ ] All beats have clear reader destinations (intellectual and emotional)
- [ ] Load-bearing beats are flagged
- [ ] Key material is curated and pointed to for each beat
- [ ] Opening and closing have deep-dive treatment
- [ ] Reader journey walkthrough captures the chapter's feel
- [ ] The chapter delivers on its job and exit state
- [ ] Bridge to next chapter is clear
- [ ] Author has approved the outline

## Handoff

The Chapter Outline Document feeds into:

- **`draft-coach`** — if author is writing and wants feedback
- **`ghostwriter`** (modal) — if Claude is drafting and author approves

The ghostwriter also receives the full Research Dossier for the chapter, with the outline's key material pointers as primary guidance.
