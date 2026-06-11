---
name: create-voice
description: "Create voice profiles from writing samples."
user-invocable: false
argument-hint: "<voice-name> <sample-files...>"
command: /create-voice
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
    - create voice
    - new voice
    - build voice
    - voice from samples
    - calibrate voice
    - voice profile from scratch
    - make a voice
  pairs_with:
    - voice-validator
    - voice-writer
  complexity: Medium
  category: content
---

# Create Voice

Create a complete voice profile from writing samples through a 7-phase pipeline. This skill is the user-facing entry point for the voice system. It orchestrates existing tools (voice-analyzer.py, voice-validator.py, voice-calibrator template) into a guided, phase-gated workflow.

**Architecture**: This skill is a GUIDE and ORCHESTRATOR. It delegates all deterministic work to existing scripts and all template structure to the voice-calibrator skill. It does not duplicate or replace any existing component.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| errors, error handling | `error-handling.md` | Loads detailed guidance from `error-handling.md`. |
| extraction validation, pattern verdict, triple-validation | `extraction-validation.md` | Triple-validation rubric (recurrence, generative power, exclusivity) gating which patterns survive into the profile. |
| Steps 6-7: validation procedure and authorship matching | `iteration-guide.md` | Loads detailed guidance from `iteration-guide.md`. |
| Step 3: PATTERN — phrase fingerprints, thinking patterns, wabi-sabi markers | `pattern-identification.md` | Loads detailed guidance from `pattern-identification.md`. |
| reporting progress at phase gates | `phase-banners.md` | Loads detailed guidance from `phase-banners.md`. |
| locating exemplar voice skills and components | `reference-implementations.md` | Loads detailed guidance from `reference-implementations.md`. |
| Step 1 COLLECT: finding, vetting, and formatting samples | `sample-collection.md` | Loads detailed guidance from `sample-collection.md`. |
| Step 5 GENERATE: skill files, frontmatter, sample organization | `skill-generation.md` | Loads detailed guidance from `skill-generation.md`. |
| Step 4 RULE: writing positive and contrastive identity rules | `voice-rules-template.md` | Loads detailed guidance from `voice-rules-template.md`. |

## Instructions

### Overview

Read and follow the repository CLAUDE.md before starting any work.

The pipeline has 7 phases. Each phase produces artifacts saved to files (because context is ephemeral; files persist) and has a gate that must pass before proceeding. Report progress with phase status banners at each gate (templates in `references/phase-banners.md`). Be direct about what passed or failed, not congratulatory.

| Phase | Name | Artifact | Gate |
|-------|------|----------|------|
| 1 | COLLECT | `skills/voice-{name}/references/samples/*.md` | 50+ samples exist |
| 2 | EXTRACT | `skills/voice-{name}/profile.json` | Script exits 0, metrics present |
| 3 | PATTERN | Pattern analysis document | 10+ phrase fingerprints identified |
| 4 | RULE | Voice rules document | Rules have contrastive examples |
| 5 | GENERATE | `skills/voice-{name}/SKILL.md` + `config.json` | SKILL.md has 2000+ lines, samples section has 400+ lines |
| 6 | VALIDATE | Validation report | Score >= 70, no banned pattern violations |
| 7 | ITERATE | Final validated skill | 4/5 authorship match (or 3 iteration limit reached) |

---

### Step 1: COLLECT -- Gather 50+ Writing Samples

**Goal**: Build a corpus of real writing that captures the full range of the person's voice.

Stop and resolve before proceeding past this step without 50+ samples, because the system tried with 3-10 and FAILED. 50+ is where it starts working. LLMs are pattern matchers -- rules tell AI what to do but samples show AI what the voice looks like. V7-V9 had correct rules but failed authorship matching (0/5 roasters). V10 passed 5/5 because it had 100+ categorized samples.

See `references/sample-collection.md` for the "Where to Find Samples" table, "Sample Quality Guidelines", "Directory Setup", and "Sample File Format".

**GATE**: Count the samples. If fewer than 50 distinct writing samples exist across all files, STOP. Tell the user how many more are needed and where to find them. Stop and resolve before proceeding.

See `references/phase-banners.md` for the Phase 1 status banner template.

---

### Step 2: EXTRACT -- Run Deterministic Analysis

**Goal**: Extract quantitative voice metrics from the samples using `voice-analyzer.py`.

Always run script-based analysis before AI interpretation, because scripts produce reproducible, quantitative baselines. AI interpretation without data drifts toward "sounds like a normal person" rather than capturing what makes THIS person distinctive. The numbers ground everything that follows.

#### Run the Analyzer

```bash
python3 ~/.claude/scripts/voice-analyzer.py analyze \
  --samples skills/voice-{name}/references/samples/*.md \
  --output skills/voice-{name}/profile.json
```

#### Also Get the Text Report

```bash
python3 ~/.claude/scripts/voice-analyzer.py analyze \
  --samples skills/voice-{name}/references/samples/*.md \
  --format text
```

The text report gives a human-readable summary. Save it for reference during Steps 3-4.

#### What the Analyzer Extracts

| Category | Metrics | Why It Matters |
|----------|---------|---------------|
| Sentence metrics | Length distribution, average, variance | Rhythm fingerprint |
| Punctuation | Comma density, question rate, exclamation rate, em-dash count, semicolons | Punctuation signature |
| Word metrics | Contraction rate, first-person rate, second-person rate | Formality and perspective |
| Structure | Fragment rate, sentence starters by type | Structural patterns |
| Function words | Top 20 function word frequencies | Unconscious language fingerprint |

#### Verify the Output

Read `profile.json` and confirm it contains all expected sections. If the script exits non-zero, check Python 3 availability, sample file readability, and file paths (glob expansion can be tricky).

**GATE**: `profile.json` exists, is valid JSON, and contains `sentence_metrics`, `punctuation_metrics`, `word_metrics`, and `structure_metrics` sections. Script exit code was 0.

See `references/phase-banners.md` for the Phase 2 status banner template.

---

### Step 3: PATTERN -- Identify Voice Patterns (AI-Assisted)

**Goal**: Using the samples + profile.json, identify the distinctive patterns that make this voice THIS voice and not generic writing.

The script extracted WHAT (numbers). This step identifies WHY those numbers are what they are and what distinctive PATTERNS produce them. A high contraction rate is a number; "uses contractions even in technical explanations, creating casual authority" is a pattern.

See `references/pattern-identification.md` for detailed guidance on "Phrase Fingerprints", "Thinking Patterns", "Response Length Distribution", "Natural Typos", "Wabi-Sabi Markers", and all 4 "Linguistic Architectures" (Argument, Concession, Analogy, Bookend) with documentation templates.

#### Apply the Triple-Validation Rubric

Every candidate pattern (phrase fingerprint, thinking pattern, linguistic architecture) is run through the triple-validation rubric in `references/extraction-validation.md` before it is documented. Each documented pattern carries an explicit verdict (KEEP, FOOTNOTE, or DROP) with evidence for cross-domain recurrence, generative power, and distinguishing exclusivity. KEEP and FOOTNOTE patterns advance to Step 4; DROP patterns are recorded in working notes only and never reach the rules document. This rubric is mandatory because patterns that pass on intuition alone tend to be generic-writer features that produce hollow voice profiles downstream.

**GATE**: At least 10 phrase fingerprints documented with exact quotes AND triple-validation verdicts. At least 3 thinking patterns identified with verdicts. Response length distribution estimated. At least 5 natural typos found. Wabi-sabi markers identified. At least 2 of 4 linguistic architectures documented with evidence quotes and verdicts. Every documented pattern carries a KEEP or FOOTNOTE verdict (DROP-verdict patterns are excluded from the documented set).

See `references/phase-banners.md` for the Phase 3 status banner template.

---

### Step 4: RULE -- Build Voice Rules

**Goal**: Transform the patterns identified in Step 3 into actionable rules for the voice skill.

Rules set boundaries while samples show execution. You need both, but samples do the heavy lifting, because V7-V9 had detailed rules and failed 0/5 authorship matching -- V10 passed with samples. Rules prevent the worst failures (AI phrases, wrong structure). Samples guide the model toward authentic output.

See `references/voice-rules-template.md` for the full "What This Voice IS" positive identity format, the "What This Voice IS NOT" contrastive table template, "Hard Prohibitions" checklist, "Wabi-Sabi Rules", "Anti-Essay Patterns", and the "Architectural Patterns" template with all 4 rule sections (Argument Flow, Concessions, Analogy Domains, Bookends).

Build rules only from KEEP and FOOTNOTE patterns produced by Step 3's triple-validation rubric (`references/extraction-validation.md`). FOOTNOTE patterns are scoped to the domain or mode where the rubric verified them -- write the rule with the scope as a guard clause. DROP-verdict candidates are intentionally absent from the rules document.

**GATE**: Positive identity has 4+ traits with dampening adverbs, each traceable to a KEEP-verdict pattern from Step 3. Contrastive table covers 6+ aspects. At least 3 hard prohibitions defined. Wabi-sabi rules specify which imperfections to preserve. Anti-essay patterns documented. Architectural patterns documented for each architecture identified in Step 3 with a KEEP or FOOTNOTE verdict.

See `references/phase-banners.md` for the Phase 4 status banner template.

---

### Step 5: GENERATE -- Create the Voice Skill

**Goal**: Generate the complete voice skill files following the voice-calibrator template.

keep modifications out of scope — voice-analyzer.py, voice-validator.py, banned-patterns.json, voice-calibrator, voice-writer, or any existing skill/script, because the existing tools work. This skill only creates new files in `skills/voice-{name}/`.

Before generating, show users any existing voice implementation in `skills/voice-*/` as a concrete example of "done", because reference implementations ground expectations.

Follow the template structure from voice-calibrator (lines 1063-1512 of `skills/workflow/references/voice-calibrator.md`), because it was refined over 10 iterations and embeds prompt engineering best practices (attention anchoring, probability dampening, XML context tags, few-shot examples for prohibitions). Deviating from the template means losing those lessons.

See `references/skill-generation.md` for "Files to Create", the "SKILL.md Structure" table (sections by line count), "SKILL.md Frontmatter", "Sample Organization" (by length and by pattern type), "Voice Metrics Section" format, "Two-Layer Architecture", "Prompt Engineering Techniques" (5 validated techniques), and the `config.json` template.

**GATE**: `SKILL.md` exists with 2000+ lines. Samples section has 400+ lines. All template sections present (samples, metrics, rules, fingerprints, protocol, typos, contrastive examples, thinking patterns). `config.json` exists with valid JSON. Frontmatter has correct fields.

See `references/phase-banners.md` for the Phase 5 status banner template.

---

### Step 6: VALIDATE -- Test Against Profile

**Goal**: Generate test content using the new skill, then validate it against the profile using deterministic scripts.

Validate with scripts, not self-assessment, because self-assessment drifts. The model will convince itself the output sounds right. Scripts measure whether sentence length, punctuation density, and contraction rate actually match the targets. Objective measurement prevents rationalization.

Run both `voice-validator.py validate` and `voice-validator.py check-banned` during this step.

See `references/iteration-guide.md` for the "Generate Test Content" steps, full validation command blocks, the score interpretation table, the wabi-sabi check, and the "If Validation Fails" recovery procedure.

**GATE**: At least one test piece scores 60+ with 0 errors (script pass threshold is 60, calibrated against real human writing). No banned pattern violations. If failed after 3 iterations, proceed to Step 7 with best score and report issues.

See `references/phase-banners.md` for the Phase 6 status banner template.

---

### Step 7: ITERATE -- Refine Until Authentic

**Goal**: Test the voice against human judgment through authorship matching, because metrics measure surface features but humans detect deeper patterns -- the "feel" of a voice. A piece can pass all metrics and still feel synthetic. Treat validation as one gate among several.

Maximum 3 iterations in this step before escalating to user.

See `references/iteration-guide.md` for the "Authorship Matching Test" procedure, the "If Authorship Matching Fails" failure pattern table, "The V10 Lesson", and the "Wabi-Sabi Final Check" checklist.

**GATE**: 4/5 roasters say SAME AUTHOR. If roaster test is not feasible, use self-assessment checklist: Does the generated content feel like reading the original samples? Could you tell them apart? If yes (you can tell them apart), more work is needed.

See `references/phase-banners.md` for the Phase 7 status banner template.

---

### Final Output

See `references/phase-banners.md` for the "VOICE CREATION COMPLETE" final output template.

---

## Error Handling

See `references/error-handling.md` for the full error matrix (insufficient samples, voice-analyzer failures, validation score too low, authorship matching failures, SKILL.md too short, wabi-sabi violations).

---

## References

See `references/reference-implementations.md` for the "Reference Implementations" table (typical file sizes and what to learn from existing voice profiles) and the "Components This Skill Delegates To" table (scripts, data files, template references).
