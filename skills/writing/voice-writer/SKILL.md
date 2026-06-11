---
name: voice-writer
description: |
  Unified voice content generation pipeline with mandatory validation and
  joy-check. 13-phase pipeline: LOAD, GROUND, STATS-CHECKPOINT, GENERATE,
  HOOK-GATE, VALIDATE, REFINE, VARIETY-GATE, JOY-CHECK, ANTI-AI, CLOSE-GATE,
  OUTPUT, CLEANUP. Use when writing articles, blog posts, or any content that
  uses a voice profile. Use for "write article", "blog post", "write in voice",
  "generate content", "draft article", "write about".
user-invocable: true
argument-hint: "<topic or title>"
command: /voice-writer
context: fork
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
  force_route: true
  triggers:
    - "write article"
    - "blog post"
    - "write in voice"
    - "blog post voice"
    - "content pipeline"
    - "publish article"
    - "draft post"
    - "write about"
    - "blog post writer"
    - "/write"
    - "voice pipeline"
    - "voice-writer"
    - "voice writer"
    - "use voice-writer"
    - "use voice writer"
    - "rewrite article"
    - "rewrite this article"
    - "write blog post"
    - "full voice pipeline"
    - "run voice pipeline"
    - "use voice pipeline"
    - "write post"
    - "draft article"
    - "generate content"
    - "article about"
    - "write for blog"
    - "write for website"
    - "write essay"
    - "write piece"
    - "ghost write"
  not_for: "scheduling or calendaring a content series (use content-calendar). This skill generates one article from a voice profile."
  category: voice
  pairs_with:
    - voice-validator
    - anti-ai-editor
    - joy-check
---

# Voice Writer — 13-Phase Pipeline

> **Mandatory enforcement**: This pipeline is REQUIRED for all voice-profiled content. No article should be published without passing all 13 phase gates.

## Pipeline Overview

```
LOAD → GROUND → STATS-CHECKPOINT → GENERATE → HOOK-GATE → VALIDATE → REFINE → VARIETY-GATE → JOY-CHECK → ANTI-AI → CLOSE-GATE → OUTPUT → CLEANUP
```

## Execution Model (MANDATORY — DO NOT COLLAPSE PHASES)

**Each phase runs as a SEPARATE agent dispatch.** The orchestrator (parent session) dispatches one agent per phase sequentially. Each agent:
1. Reads the input artifact from the previous phase
2. Loads the selected voice profile and any phase-specific references
3. Executes the phase steps
4. Writes its output artifact to disk
5. Reports pass/fail on the phase gate

**No single agent runs multiple phases.** This ensures each phase gets a fresh context window with the full voice profile loaded, preventing context drift and ensuring the voice is the primary authority at every step. An orchestrator that attempts to combine phases or skip agent dispatches is violating this rule.

**Phase artifacts are files on disk**, not context passed between agents. Each phase reads and writes to well-known paths:

| Phase | Input Artifact | Output Artifact |
|-------|---------------|-----------------|
| 1. LOAD | User request + existing draft (if any) | `.voice-phase/01-load.json` (profile metadata, paths) |
| 2. GROUND | `.voice-phase/01-load.json` + source material | `.voice-phase/02-grounding.md` |
| 3. STATS-CHECKPOINT | `.voice-phase/01-load.json` | `.voice-phase/03-stats-baseline.json` |
| 4. GENERATE | `.voice-phase/02-grounding.md` + stats baseline | `.voice-phase/04-draft.md` |
| 5. HOOK-GATE | `.voice-phase/04-draft.md` | `.voice-phase/05-hook-score.json` + updated draft |
| 6. VALIDATE | `.voice-phase/04-draft.md` (or updated) | `.voice-phase/06-validation-report.json` |
| 7. REFINE | Draft + `.voice-phase/06-validation-report.json` | `.voice-phase/07-refined-draft.md` |
| 8. VARIETY-GATE | `.voice-phase/07-refined-draft.md` | `.voice-phase/08-variety-score.json` + updated draft |
| 9. JOY-CHECK | Latest draft | `.voice-phase/09-joy-report.json` + updated draft |
| 10. ANTI-AI | Latest draft | `.voice-phase/10-antiai-report.json` + updated draft |
| 11. CLOSE-GATE | Latest draft | `.voice-phase/11-close-score.json` + updated draft |
| 12. OUTPUT | Latest draft + all reports | Final file in `content/posts/` + `.voice-pipeline-complete` |
| 13. CLEANUP | All `.voice-phase/` artifacts | Summary report (artifacts cleaned up) |

**The orchestrator creates `.voice-phase/` directory at the start and each agent writes its artifact there. Phase N agent MUST verify Phase N-1 artifact exists before starting.**

**Every phase agent prompt MUST include:**
- "Read the selected voice profile's SKILL.md at `/home/feedgen/.claude/skills/{voice_profile}/skill/SKILL.md`"
- "Read the writing samples at `/home/feedgen/.claude/skills/{voice_profile}/references/samples/`"
- "Read `profile.json` at `/home/feedgen/.claude/skills/{voice_profile}/profile.json`"
- The specific phase instructions from this skill file
- "Write your output artifact to `.voice-phase/NN-name.ext`"

Where `{voice_profile}` is the voice skill selected in Phase 1 (e.g., `voice-myprofile`, `voice-myvoice`).

**Environment**: The orchestrator sets `VOICE_WRITER_ACTIVE=1` before dispatching any phase agent. This allows the pipeline-phase-gate hook to permit writes to `content/posts/`.

---

## Phase 1: LOAD

**Goal**: Load the correct voice profile and all reference materials.

**Steps**:
0. Set environment: `export VOICE_WRITER_ACTIVE=1` (allows pipeline-phase-gate to permit writes during pipeline execution)
1. Determine target voice from user context or explicit request. Available voice profiles:
   - Any `voice-*` skill in `~/.claude/skills/` — run `ls ~/.claude/skills/ | grep voice-` to see available profiles
2. Read the voice profile's `profile.json` and all files under `references/`
3. Read the target site's `CLAUDE.md` for structural conventions (front matter template, slug rules, tags)
4. If a topic-brainstormer outline exists, load it as structural input

**Gate**: Voice profile loaded and confirmed. Profile name echoed back. Proceed.

---

## Phase 2: GROUND

**Goal**: Anchor the article in lived experience, not abstraction.

**Steps**:
1. Identify the core problem or frustration the article solves
2. Find the specific personal experience: what happened, when, what went wrong
3. Extract the "vex" (frustration) and the "joy" (resolution) — these frame the narrative arc
4. List 3-5 concrete details from the experience (error messages, tool names, timestamps, measurements)
5. Determine the single insight the reader should carry away

**Gate**: Grounding document exists with: problem statement, personal experience, concrete details, single insight. All must be specific, not abstract.

---

## Phase 3: STATS-CHECKPOINT

**Goal**: Establish baseline metrics for the voice profile to validate against later.

**Steps**:
1. From the loaded voice profile, extract target ranges for:
   - Sentence length distribution
   - Paragraph length distribution
   - First-person pronoun density
   - Technical term density
   - Contraction rate
2. Record these as the validation targets for Phases 6 and 8
3. Note any voice-specific banned patterns (AI cliches, forbidden phrases)

**Gate**: Metrics targets recorded. Baseline established. Proceed.

---

## Phase 4: GENERATE

**Goal**: Produce the first complete draft using the loaded voice profile.

**Steps**:
1. Write the full article in the target voice, using grounding materials
2. Apply front matter template from site conventions
3. Ensure every section connects to the personal experience — no floating abstractions
4. Use the voice profile's modal register (teaching, casual, investigative, etc.) as appropriate
5. Include code examples if technical — they must be complete and tested
6. Target word count per user request or default 1200-2000 words
7. Apply narrative structure guidance (these counter the most durable AI fingerprints — narrative patterns survive stylistic editing):
   - Let evidence speak — present facts, quotes, and moments that carry the meaning. Trust readers to find the point.
   - Mix emotional registers: name feelings directly sometimes, use behavioral cues, alternate between sensation and plain statement.
   - Weave secondary threads: a tangent, counter-example, or aside that returns to enrich the main point.
   - Leave room for uncertainty: external factors, other people's decisions, and unresolved threads belong in the piece. Real situations have loose ends.
   - Reference specifically: name the person, the event, the source. Generic authority ("many experts") reads as evasion.
   - Vary intensity: build peaks and valleys. Flat escalation is a Claude fingerprint.
   - Include at least one event the reader would not predict from the opening: a surprising data point, unexpected reaction, or reversal.
   - Acknowledge the reader: address their likely experience, ask what they have noticed, speak to them.
   - Vary temporal structure: call back to an earlier point, open with the conclusion, break chronological order where it serves the piece.
   - Close with forward motion, a practical step, or an honest open question.
   - Subvert one expectation: lead with the counter-intuitive angle, challenge a convention, take a position the reader might push back on.
   - Use speculative departures where they serve the piece: "Imagine if..." or "What would happen if..." makes abstract points concrete.
   - Cut the epilogue unless it adds specific new information. General future-looking paragraphs weaken the final substantive point.

**Gate**: Complete draft exists with front matter, body, and closing. Draft is in the target voice. Proceed.

---

## Phase 5: HOOK-GATE

**Goal**: Ensure the opening paragraph arrests attention with specificity.

**Steps**:
1. Examine the opening paragraph (first 1-3 sentences)
2. Check for at least ONE of:
   - A concrete number ("20 headless sessions", "394 lines", "nine months")
   - A specific date or timeframe ("at 2 AM", "last Tuesday", "after six months")
   - An unexpected detail that raises a question ("and the results contradicted everything I expected")
3. Score the hook 1-10 on specificity and pull strength
4. If the opening is generic ("I kept noticing...", "I had a problem with...", "Recently I..."):
   - Scan the article body for the most surprising specific finding
   - Pull that concrete detail UP into the opening
   - Rewrite the opening to lead with the surprising specific
5. Re-score after rewrite

**Gate**: Hook score >= 8. If < 8, rewrite and re-score. Max 3 attempts. If still < 8 after 3 attempts, flag for human review but proceed.

---

## Phase 6: VALIDATE

**Goal**: Verify the draft matches the voice profile's statistical fingerprint.

**Steps**:
1. Invoke `voice-validator` skill
2. Measure actual metrics against Phase 3 targets:
   - Sentence length distribution
   - First-person pronoun density
   - Contraction rate
   - Technical term density
3. Flag any metric more than 1 standard deviation from target
4. Check for banned patterns and AI cliches
5. Produce a validation report with pass/fail per metric

**Gate**: All metrics within acceptable range OR deviations documented with justification. No banned patterns present.

---

## Phase 7: REFINE

**Goal**: Fix validation failures and polish prose quality.

**Steps**:
1. For each failed metric from Phase 6:
   - Rewrite affected sentences to bring metric into range
   - Preserve meaning and voice while adjusting structure
2. Tighten prose: cut filler words, redundant phrases, hedge stacking
3. Verify all code examples still compile/run after edits
4. Check that section transitions feel natural, not mechanical
5. Re-run validation on changed sections

**Gate**: All previously failed metrics now pass. Prose reads naturally. Proceed.

---

## Phase 8: VARIETY-GATE

**Goal**: Ensure sentence and paragraph rhythm creates natural reading texture.

**Steps**:
1. Measure sentence length distribution by word count per sentence:
   - Short (1-7 words): target 30-45%
   - Medium (8-20 words): target 35-50%
   - Long (21+ words): target 10-25%
2. Verify all three clusters appear at least 15% of the time
3. If any cluster is below 15%: rewrite sentences in the dominant cluster to redistribute
4. Check paragraph length (hard ceiling, enforces short paragraphs with spacing between thoughts):
   - Every paragraph holds 3 sentences or fewer. Count sentences per paragraph (split on blank lines).
   - Any paragraph of 4+ sentences fails the gate: split it at the thought boundary and insert a blank line.
   - At least 1 single-sentence paragraph per 500 words (single-sentence paragraphs are welcome whenever a thought stands alone).
   - This applies to ALL voices and modes. Walls of text read as AI output; short paragraphs with spacing read as a person thinking.
5. Calculate variety score: standard deviation of sentence word counts
6. If variety score < 8.0 words:
   - Inject longer exploratory sentences (complex thoughts, compound structures) while keeping each paragraph at 3 sentences or fewer
   - Inject shorter fragment punches (declarations, observations, reactions)
   - Recalculate until stddev >= 8.0

**Gate**: All three sentence clusters >= 15%. Every paragraph is 3 sentences or fewer (no walls of text), with at least 1 single-sentence paragraph per 500 words. Variety score (stddev of sentence lengths) >= 8.0. If any check fails, rewrite and re-measure. Max 3 attempts.

---

## Phase 9: JOY-CHECK

**Goal**: Verify the article frames its content on the joy side, not the grievance side.

**Steps**:
1. Invoke `joy-check` skill
2. Score the article on the joy-grievance spectrum
3. Ensure the article:
   - Celebrates problem-solving, not complaining about problems
   - Frames difficulties as interesting challenges, not injustices
   - Ends with satisfaction or forward motion, not bitterness
4. If the article scores too far toward grievance, reframe the problematic sections

**Gate**: Joy-check passes. Article is on the joy side of the spectrum.

---

## Phase 10: ANTI-AI

**Goal**: Strip all AI-sounding patterns from the content.

**Steps**:
1. Invoke `anti-ai-editor` skill (`/home/feedgen/.claude/skills/anti-ai-editor/SKILL.md`)
2. Scan for and remove:
   - Generic transitions ("Furthermore", "Moreover", "It's worth noting")
   - Hedge stacking ("It seems like it might potentially")
   - Summary-style conclusions
   - Bullet-point-as-prose formatting
   - Self-narrating structure ("In this article, we'll explore...")
   - Any pattern from the banned patterns list in the voice profile
3. Replace AI patterns with voice-authentic alternatives
4. Re-read the full article aloud (mentally) — does it sound like a person wrote it?

**CRITICAL: Voice profile overrides anti-AI rules.** When the anti-AI editor flags
a pattern that exists in the selected voice profile's corpus (writing samples, phrase bank,
or signature patterns), the voice profile wins. The anti-AI editor removes generic
AI patterns. It does NOT remove patterns that are documented in the voice profile
as authentic human writing, even if those patterns overlap with common AI tells.

Examples of voice-authentic patterns the anti-AI editor should preserve (do not remove):
- Repetition-for-emphasis ("X is Y. Z is Y. W is Y." — documented in voice profile samples)
- "This isn't X" flat dismissals (documented under "Direct Assessment" pattern)
- Short-then-long sentence pairs (documented structural pattern)
- Negation-then-reframe when framed as questions ("The question is not X. The question is Y.")

**Gate**: Anti-AI editor passes. Zero AI-flagged patterns remain. Voice-authentic patterns preserved.

---

## Phase 11: CLOSE-GATE

**Goal**: Ensure the closing avoids formulaic patterns and uses an authentic voice-profiled ending.

**Steps**:
1. Identify which closing pattern the article currently uses. The 5 closing modes (from the voice profile's closing patterns):
   - **Honest Uncertainty**: "I don't know if this generalizes", "But we'll see"
   - **Practical Trailing Observation**: "Save the work. Read the work."
   - **Self-Deprecating Admission**: "I may never be an influencer"
   - **Specific Next Step**: "I'm going to try X next week"
   - **Just Stops**: the last technical point IS the ending — no wrap-up at all
2. If the closing matches pattern #1 (Honest Uncertainty) AND it is the ONLY pattern considered:
   - Force a rewrite using pattern #2 (Practical Trailing Observation), #4 (Specific Next Step), or #5 (Just Stops)
3. Verify the close does NOT:
   - Summarize the article
   - Callback to the opening
   - Use "In conclusion", "To sum up", "At the end of the day", or equivalent
   - End with a grand statement or inspirational flourish
4. Score the closing 1-10 on authenticity and fit

**Gate**: Closing uses a pattern other than the lazy uncertainty default. Closing score >= 7. No summary, no callback, no grand statement. If < 7, rewrite using a different closing mode and re-score. Max 3 attempts.

---

## Phase 12: OUTPUT

**Goal**: Produce the final deliverable.

**Steps**:
1. Apply final formatting:
   - Correct front matter (title, date, draft status, tags, summary)
   - Proper Hugo markdown conventions
   - File named per convention: `YYYY-MM-DD-slug.md`
2. Write the file to `content/posts/`
3. Display the complete article to the user
4. Report all gate scores:
   - Hook score (Phase 5)
   - Validation pass/fail (Phase 6)
   - Variety score and cluster percentages (Phase 8)
   - Joy-check result (Phase 9)
   - Anti-AI result (Phase 10)
   - Close score (Phase 11)
5. Write pipeline completion marker:
   Write `.voice-pipeline-complete` in the project root with JSON:
   ```json
   {
     "pipeline": "voice-writer",
     "completed_at": "<ISO timestamp>",
     "target_file": "<relative path to the content/posts/ file>",
     "phases_passed": ["LOAD", "GROUND", "STATS-CHECKPOINT", "GENERATE", "HOOK-GATE", "VALIDATE", "REFINE", "VARIETY-GATE", "JOY-CHECK", "ANTI-AI", "CLOSE-GATE", "OUTPUT", "CLEANUP"]
   }
   ```

**Gate**: File written. All scores reported. Pipeline marker written. User can review.

---

## Phase 13: CLEANUP

**Goal**: Clear working state and summarize.

**Steps**:
1. Report final word count, reading time estimate
2. Provide the preview URL per CLAUDE.md conventions:
   - `http://<IP>:1313/posts/<slug-without-date>/`
3. Note any gates that required multiple attempts (potential voice drift indicators)
4. If any gate hit max attempts without passing, explicitly flag it

**Gate**: Summary delivered. Pipeline complete.
