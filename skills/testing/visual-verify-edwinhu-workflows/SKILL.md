---
name: visual-verify
version: 2.3
description: "This skill should be used when the user asks to 'verify visual output', 'check how it looks', 'render and review', 'visual verify', 'check the slide', 'does this look right', or when any task produces rendered visual output (slides, charts, documents, UI). Starts a render-vision-fix loop using Gemini vision."
user-invocable: false
---

**Announce:** "I'm using visual-verify to set up a render-vision-fix loop."

<EXTREMELY-IMPORTANT>
## The Iron Law

**NO VISUAL TASK IS COMPLETE WITHOUT RENDERING, SCORING, AND MEETING THE THRESHOLD.**

Source code correctness does NOT imply visual correctness. You MUST render to PNG, score with context-enriched Gemini vision (0-10), and iterate until score >= 9.5. Claiming "done" with a score below threshold delivers broken visuals to the user.

**Skipping the score check is NOT HELPFUL — the user gets a visual artifact with defects you didn't verify.**
</EXTREMELY-IMPORTANT>

## Agentic Vision Routing

**Route based on image complexity, not source language.**

Agentic vision (`--agentic`) enables Gemini's Think-Act-Observe loop: it can crop, zoom, annotate, and re-examine regions of the image autonomously. This catches fine-grained defects that full-image viewing misses.

| Image characteristic | `--agentic`? | Why |
|---|---|---|
| Dense diagram (5+ nodes, many arrows/labels) | YES | Can crop individual arrow paths, zoom into small labels to check connections |
| Small text or labels near container edges | YES | Implicit zoom catches clipping that full-image view misses |
| Side-by-side or before/after comparison | YES | Can crop matching regions and annotate differences |
| Simple layout (2-3 large elements) | NO | Full image is sufficient; agentic adds latency for no gain |
| Single chart with large text | NO | No fine-grained details to investigate |

**Decision rule:** If the image has details that are easy to miss at full resolution, use `--agentic`. If you can see everything clearly at a glance, skip it.

## The Loop

```
0. PAGE MAP -> If Typst + Touying: Skill("teaching:find-slide-page")
       |      Returns heading → physical page mapping
       |      Skip if: single-page file, non-Typst, or page already known
       |
1. CHANGE  -> Modify source code (Task agent)
       |
2. RENDER  -> Produce PNG (see references/render-commands.md)
       |      Render fails? -> fix source, back to step 1
       |
3. VISION  -> Two-part check:
       |      a) INTENT — Does the render match the design intent?
       |         (Does the visual structure argue what it should?)
       |      b) DEFECTS — Scan for the 9 visual defect categories:
       |         1. Text clipped by or overflowing its container
       |         2. Text or shapes overlapping other elements
       |         3. Arrows crossing through elements instead of routing around
       |         4. Arrows landing on wrong element or pointing into empty space
       |         5. Labels floating ambiguously (not anchored to what they describe)
       |         6. Labels squeezed between adjacent elements without clearance
       |         7. Uneven spacing (cramped sections next to spacious ones)
       |         8. Text too small to read at rendered size
       |         9. Parallel sub-diagrams with inconsistent layout
       |      Complexity-routed look-at call with SCORING:
       |      Dense/fine-grained? -> --agentic (Gemini crops/zooms/annotates)
       |      Simple/large elements? -> vision-only (structured pixel feedback)
       |      → Score 0-10 against checklist items
       |      → Record in SCORES.md
       |
4. DECIDE  -> Score >= 9.5 AND exit criteria met? → DONE
              Score < 9.5 OR defects remain?      → extract fixes, back to step 1
```

### When to Stop

The loop is done when ALL of these hold:
- Score >= 9.5
- The rendered output matches the design intent (not just defect-free but *correct*)
- No text is clipped, overlapping, or unreadable
- All arrows/lines connect to the right elements and route cleanly
- Spacing is consistent and composition is balanced
- You'd show it to someone without caveats

**Don't stop after one clean pass just because there are no critical bugs — if the composition could be better, improve it.** Conversely, don't loop forever on cosmetics — 5 iterations max before escalating to the user.

### Invocation

```
Skill(skill="ralph-loop:ralph-loop", args="Visual Task N: [TASK NAME] --max-iterations 5 --completion-promise VTASKN_9_5")
```

### Score Tracking

Initialize SCORES.md before the first iteration:

```markdown
# Visual Verify Scores

| Iteration | Score | Threshold | BLOCKING | COSMETIC | Delta |
|-----------|-------|-----------|----------|----------|-------|
```

Each vision call must score the output 0-10:
- 10.0 = all checklist items pass, zero issues
- 9.5 = 95% pass, 1-2 cosmetic issues remain (default threshold)
- < 9.0 = BLOCKING issues present

The score reflects the fraction of checklist items that pass. Gemini counts BLOCKING and COSMETIC issues against the domain-specific checklist, and the score = (items passing / total items) * 10.

### Vision Calls

**Agentic** (dense diagrams, fine-grained details, comparisons):
```bash
LOOK_AT=$(${CLAUDE_SKILL_DIR}/../../skills/look-at/scripts/look_at.py) && python3 "$LOOK_AT" \
    --file "/tmp/visual-verify.png" \
    --goal "[CONTEXT-ENRICHED GOAL]" \
    --agentic
```

Gemini will autonomously crop, zoom, and annotate regions it wants to inspect more closely. This is most valuable for:
- Verifying arrow connections in dense node diagrams
- Checking whether small labels are fully visible (not clipped)
- Comparing spatial consistency across sub-diagrams

**Vision-only** (simple layouts, large elements):
```bash
LOOK_AT=$(${CLAUDE_SKILL_DIR}/../../skills/look-at/scripts/look_at.py) && python3 "$LOOK_AT" \
    --file "/tmp/visual-verify.png" \
    --goal "[CONTEXT-ENRICHED GOAL]"
```

### Goal Assembly

**NEVER call look-at with a generic goal.** Goals must reference the spec, checklist items, and prior feedback.

| Context Piece | Source |
|---------------|--------|
| `spec_text` | SPEC.md, PLAN.md task, or user request |
| `checklist_items` | Domain + task specific |
| `previous_feedback` | Gemini's output from prior iteration |

**For diagrams (fletcher, CeTZ): use describe-first strategy**, NOT judgment prompts.
- Step 1: Ask Gemini to transcribe all text elements with `[FULL | PARTIAL]` annotations
- Step 2: Claude diffs transcription against expected elements from source code
- Step 3 (optional): Run spatial/overlap check for non-clipping issues
- **Why:** Judgment prompts ("is X visible?") invite yes-man answers. Transcription forces the model to report what it actually sees — clipping becomes objectively detectable via text mismatches.

See `references/goal-templates.md` for full copy-paste templates per domain.

### Translating Non-Python Feedback

**Before editing Typst source to apply fixes, load the tinymist skill:** `Skill(skill="tinymist:typst")`
It has Fletcher/CeTZ reference docs with correct parameter names (label-side, label-pos, spacing, inset). Without it, you will guess at parameter names and waste iterations.

Gemini returns structured pixel measurements. Claude translates to source code:

| Gemini says | Claude translates to (Typst example) |
|-------------|--------------------------------------|
| "Move label 15px left" | Adjust `label-pos` or node coordinates by ~0.5em |
| "Text clipped at right edge" | Increase `inset` or reduce `scale()` percentage |
| "Node/diagram cut off at edge" | Reduce canvas `length`, node `inset`, or `spacing`; or shift coordinates toward center |
| "Elements overlap vertically" | Increase `spacing` parameter |
| "Font too small to read" | Increase `#set text(Npt)` value |

### Complex Diagrams (3+ Failed Iterations)

If the same spatial issue persists after 3 iterations, escalate to the reference sketch approach: have Gemini draw an ideal layout in matplotlib and translate coordinates.

See `references/complex-diagram-strategy.md` for the full approach.

## Quick Render Reference

| Domain | Command |
|--------|---------|
| Typst | `tinymist compile input.typ /tmp/visual-verify.png --pages N --ppi 144` (use `/find-slide-page` to get N) |
| Python | `python3 script.py` (script saves to known path) |
| Screenshot | `screencapture -x /tmp/visual-verify.png` |

See `references/render-commands.md` for the full reference.

## When NOT to Use

- **One-off visual checks**: Use `look-at` directly, not the full loop
- **Text-only verification**: Use standard dev-verify
- **Compilation checks only**: Just run the compile command

## Reference Files

- `references/goal-templates.md` -- copy-paste goal templates per domain
- `references/render-commands.md` -- render commands for all supported domains
- `references/rationalization-prevention.md` -- excuses, red flags, honesty framing, drive-aligned consequences
- `references/complex-diagram-strategy.md` -- reference sketch approach for persistent layout failures
- `references/examples.md` -- worked examples (Typst slide, matplotlib chart, diagram escalation)
