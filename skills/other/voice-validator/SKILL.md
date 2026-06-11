---
name: voice-validator
description: "Critique-and-rewrite loop for voice fidelity validation."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
  - Skill
routing:
  triggers:
    - "validate voice"
    - "check voice fidelity"
    - "voice critique"
    - "voice fidelity"
    - "writing style check"
  category: voice
  pairs_with:
    - voice-writer
    - anti-ai-editor
    - joy-check
---

# Voice Validator Skill

## Overview

This skill operates a rigorous critique-and-rewrite enforcement loop for voice fidelity. It scans content against voice-specific negative prompt checklists, documents violations with evidence, fixes them while preserving intent, and rescans to confirm the revision passes — up to 3 iterations maximum.

The workflow implements the **Iterative Refinement** pattern: scan → document violations → revise → rescan. This ensures voice violations are caught systematically and fixed methodically without over-engineering or changing meaning.

**CRITICAL CONSTRAINT**: Never revise content without first scanning against the full checklist. Every violation must cite a specific quote. After 3 failed iterations, output with flagged concerns rather than continuing indefinitely.

---

## Instructions

### Phase 1: IDENTIFY TARGET

**Goal**: Determine the voice, mode, and content to validate.

**Step 1: Identify voice target**
- Determine target voice from context or user instruction
- Identify mode if applicable — casual modes may have additional specific checks
- Reference the target voice's checklist (contact user if unclear)

**Step 2: Load content**
- Read the content to validate
- Note content length — longer content is more prone to drift

**Gate**: Voice target and mode identified. Content loaded. Proceed only when gate passes.

### Phase 2: SCAN

**Goal**: Run full checklist against content and identify all violations with evidence.

**Step 1: Run negative prompt checklist**

Check all categories against the target voice's checklist. Standard categories include:

- **Tone**: Does the tone match the voice profile? (e.g., too polished, too corporate, missing warmth)
- **Structure**: Does the structure match? (e.g., front-loaded constraints, clean outlines, wrap-ups)
- **Sentences**: Do sentence patterns match? (e.g., dramatic short sentences, rhetorical flourishes, symmetrical structure)
- **Language**: Any banned words? (amazing, terrible, revolutionary, perfect, game-changing, transformative, incredible, outstanding, exceptional, groundbreaking), marketing/hype, inspirational, unnecessary superlatives
- **Emotion**: Does emotion handling match? (e.g., explicitly named emotions, venting/ranting, moralizing)
- **Questions**: Do question patterns match? (e.g., open-ended brainstorming, vague curiosity)
- **Metaphors**: Do metaphor patterns match? (e.g., journey/path, biological/growth, narrative/story)
- **Narrative** (500+ words only; full 13-check rubric in `references/narrative-patterns.md`):
  - Evidence speaks for itself, or narrator over-explains the point?
  - Emotional registers mixed (named feelings + behavioral cues + sensation)?
  - Secondary threads present that enrich the main argument?
  - Reader's experience acknowledged?
  - Temporal structure varied (callbacks, non-linear points)?
  - References specific (named people, works, sources)?
  - Room for uncertainty and loose ends, or subject has every answer?
  - Intensity varies (peaks and valleys), or flat throughout?
  - Event types diverse, or every paragraph does the same thing?
  - Ending carries forward motion, or defaults to tidy realization epilogue?

**Step 2: Check pass conditions**

Verify the content matches the target voice's positive identity markers. Common pass conditions include:

- Feels like the person actually wrote it
- Voice-specific patterns are present (thinking out loud, warmth, precision, etc.)
- Could NOT be posted on LinkedIn without edits (for casual voices) — this heuristic catches ~80% of voice violations
- Does NOT sound like AI wrote it
- Narrative structure shows variety — secondary threads, temporal variation, forward-motion ending
- Mode-specific patterns are present (casual modes: no preamble, no wrap-up; formal modes: structured flow)

**Step 3: Document violations**

For each violation, record:
1. Category (tone, structure, sentence, language, emotion, question, metaphor, narrative)
2. Quoted text from the content
3. Specific fix recommendation

**Key constraint**: Only scan at this stage; save revisions for the next phase. Subjective assessment without a checklist misses specific violations.

**Gate**: Full checklist scanned. All violations documented with evidence. Proceed only when gate passes.

### Phase 3: REVISE

**Goal**: Fix all violations while preserving content intent and substance.

**Step 1: Apply fixes**
- Address each violation with the smallest change that resolves it
- Preserve the original meaning and information
- Maintain natural flow — fixes should not create new violations

**Step 2: Verify no overcorrection**
- Ensure revisions did not strip necessary content
- Confirm the substance and technical accuracy remain intact
- Keep the revision to voice-level changes only; leave paragraphs and arguments intact

**Key constraint**: Make the smallest change that resolves each violation. Preserve all meaning. Changing substance is scope creep.

**Gate**: All documented violations addressed. Intent preserved. Proceed only when gate passes.

### Phase 4: VERIFY

**Goal**: Confirm revised content passes all checks.

**Step 1: Rescan revised content**

Run the full checklist from Phase 2 against the revised version.

**Step 2: Evaluate result**
- If PASS: Output final content with validation report
- If FAIL and iteration < 3: Return to Phase 3 with new violations
- If FAIL and iteration = 3: Output content with flagged remaining concerns

**Key constraint**: Always rescan. "Should be fine" is a rationalization. Fixes can introduce new violations.

**Step 3: Output validation report**

```
VOICE VALIDATION: [Voice Name] Mode [mode]
SCAN RESULT: [PASS/FAIL]
VIOLATIONS DETECTED: [N]
ITERATION: [1-3]

[If violations:]
1. [Category]: "[quoted violation]"
   Fix: [specific correction]

2. [Category]: "[quoted violation]"
   Fix: [specific correction]

REVISED OUTPUT:
[Corrected content]

RESCAN RESULT: [PASS/FAIL]
```

**Gate**: Content passes all checks, or maximum iterations reached with flagged concerns. Validation complete.

---

## Examples

### Example 1: Technical Voice Validation
User says: "Validate this draft is in the right voice"

Actions:
1. Identify target voice from context, determine mode from content style (IDENTIFY TARGET)
2. Run full 8-category checklist (Tone, Structure, Sentences, Language, Emotion, Questions, Metaphors, Narrative), find 2 violations (SCAN)
3. Fix "I'm excited to share" (named emotion) and "This changes everything" (dramatic short sentence) (REVISE)
4. Rescan revised content, confirm PASS (VERIFY)

Result: Clean content with validation report

### Example 2: Community Voice Validation
User says: "Does this sound like the right voice?"

Actions:
1. Identify target voice from context (IDENTIFY TARGET)
2. Scan against voice checklist, find missing warmth and no sensory details (SCAN)
3. Add experiential language and warmth while preserving substance (REVISE)
4. Rescan, confirm warmth and sensory details present, PASS (VERIFY)

Result: Content matches voice profile

---

## Error Handling

### Error: "Voice Target Unclear"
Cause: Content doesn't specify which voice to validate against, or context is ambiguous

Solution:
1. Check conversation context for voice mentions
2. Look for voice-specific patterns to infer target
3. If still unclear, ask user to specify voice name and mode

### Error: "Violations Persist After 3 Iterations"
Cause: Fundamental mismatch between content substance and voice requirements, or conflicting checklist items

Solution:
1. Output content with clearly flagged remaining violations
2. List specific checklist items that resist correction
3. Suggest the content may need to be regenerated from scratch with the correct voice skill

### Error: "Revision Introduced New Violations"
Cause: Fixing one category created violations in another (e.g., removing dramatic sentences introduced polished phrasing)

Solution:
1. Address new violations in next iteration
2. If oscillating between two violation types, fix both simultaneously
3. Prioritize tone and language violations over structural ones

---

## References

### Related Skills
- `voice-{name}` - Generates content in a specific voice (validate output with this skill)
- `anti-ai-editor` - Complementary anti-AI pattern detection
- `voice-writer` - Unified voice content generation pipeline that invokes this skill
