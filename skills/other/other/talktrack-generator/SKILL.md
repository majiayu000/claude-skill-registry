---
name: talktrack-generator
description: Generate natural, ElevenLabs-ready talk tracks for physician course lectures using Ralph-style iterative architecture with fresh subagent context per slide.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
user_invocable: true
argument-hint: <lecture-path> [--transcript PATH] [--words-per-minute N] [--max-retries N]
---

# Talk Track Generator

Generate natural, ElevenLabs-ready voiceover scripts for physician course lectures. Uses Claude Opus 4.5 with closed feedback loops and fresh subagent context per slide to produce high-quality talk tracks that can be pasted directly into text-to-speech systems.

## Overview

This skill processes lecture JSON files and generates spoken narration that:
- Covers all slide content naturally
- Uses natural verbal bridges between slides (no markers)
- Matches the educator's voice if a transcript is provided
- Is ready to paste directly into ElevenLabs

**Key Principles:**
- **Iterative**: Each slide is generated, validated, and refined before moving on
- **Fresh Context**: Each slide uses a fresh subagent to prevent context bloat
- **Validated**: Every segment passes timing, coverage, flow, and transition checks
- **Audited**: Full changelog of generation decisions and iterations

## Invocation

```bash
/talktrack-generator <lecture-path> [options]
```

**Arguments:**
- `<lecture-path>` - Path to lecture JSON or shorthand (e.g., `dr-robin-rose/gut-microbiome/lecture-1`)
- `--transcript PATH` - Voice sample transcript for style matching (optional)
- `--words-per-minute N` - Target speaking pace (default: 150)
- `--max-retries N` - Max retries per slide before blocking (default: 2)

**Examples:**
```bash
# Generate from lecture JSON path
/talktrack-generator content/physician-courses/dr-robin-rose/gut-microbiome/lecture-1.json

# With voice transcript for style matching
/talktrack-generator dr-robin-rose/gut-microbiome/lecture-1 --transcript ./voice-samples/dr-rose-transcript.txt

# Custom speaking pace (slower for complex content)
/talktrack-generator dr-robin-rose/gut-microbiome/lecture-1 --words-per-minute 140

# Resume interrupted generation
/talktrack-generator --resume
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    /talktrack-generator                      │
│                                                              │
│  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐│
│  │  PHASE 1       │   │  PHASE 2       │   │  PHASE 3       ││
│  │  Planning      │──▶│  Iterative     │──▶│  Assembly      ││
│  │                │   │  Generation    │   │                ││
│  └────────────────┘   └────────────────┘   └────────────────┘│
│         │                    │                    │          │
│         ▼                    ▼                    ▼          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    STATE FILES                          │ │
│  │  .talktrack-gen/prd.json, progress.txt, segments/       │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Quick Start

1. **Provide lecture** - Point to lecture JSON file
2. **Optional transcript** - Provide educator voice sample for style matching
3. **Monitor generation** - Skill generates slide by slide with validation
4. **Get output** - Final script ready for ElevenLabs

---

## Phase 1: Planning

### Step 1.1: Load Lecture JSON

Resolve the lecture path and load the JSON structure:

```javascript
// Supported path formats:
// 1. Full path: content/physician-courses/dr-robin-rose/gut-microbiome/lecture-1.json
// 2. Shorthand: dr-robin-rose/gut-microbiome/lecture-1
// 3. Relative: ./lecture-1.json

const lecture = JSON.parse(Read({ file_path: lecturePath }));
```

**Lecture structure expected:**
```json
{
  "id": "lecture-id",
  "title": "Lecture Title",
  "module": "Module Name",
  "duration": 60,
  "slides": [...],
  "keyTakeaways": [...],
  "references": [...]
}
```

### Step 1.2: Extract Voice Profile (Optional)

If `--transcript` is provided, analyze it for voice patterns:

**Voice extraction analyzes:**
- Tone (formal vs. conversational)
- Sentence length patterns (short, medium, long rhythm)
- Transition phrases used
- Rhetorical devices (questions, analogies, stories)
- Vocabulary level
- Use of first person vs. third person

**Output:**
```json
{
  "voiceProfile": {
    "tone": "warm, conversational with authority",
    "sentenceRhythm": "medium-short-long pattern",
    "transitionStyle": "uses rhetorical questions and 'Here's what's fascinating...'",
    "vocabulary": "clinical terms explained simply",
    "personalization": "first person plural ('we', 'let's')",
    "samplePhrases": [
      "Here's what makes this different...",
      "Let me show you what this looks like in practice...",
      "This is where it gets interesting for your clinic..."
    ]
  }
}
```

If no transcript provided, Claude Opus 4.5 will determine optimal voice based on:
- Physician persona (from course metadata)
- Content type (clinical, business, research)
- Target audience expectations

### Step 1.3: Generate PRD (Slide Segments)

Create a segment for each slide with target metrics:

```json
{
  "sessionId": "talktrack-2026-01-16-dr-robin-rose-gut-microbiome-1",
  "lecture": {
    "id": "long-covid-gut-microbiome-robin-rose",
    "title": "Long COVID and the Gut Microbiome",
    "slideCount": 16
  },
  "config": {
    "wordsPerMinute": 150,
    "maxRetries": 2,
    "model": "claude-opus-4-5-20250514"
  },
  "voiceProfile": { ... },
  "segments": [
    {
      "segmentId": "SEG-001",
      "slideId": "learning-objectives",
      "slideTitle": "Learning Objectives",
      "targetDuration": 90,
      "targetWordCount": 225,
      "status": "pending",
      "attempts": 0,
      "contentElements": {
        "paragraphs": 1,
        "bullets": 0,
        "numbered": 4,
        "callouts": 1,
        "hasDiagram": false
      }
    },
    // ... more segments
  ],
  "summary": {
    "totalSegments": 16,
    "pending": 16,
    "completed": 0,
    "blocked": 0,
    "estimatedTotalDuration": 60
  }
}
```

### Step 1.4: Initialize State Files

Create the `.talktrack-gen/` directory structure:

```
.talktrack-gen/
├── prd.json              # Segment definitions + status
├── progress.json         # Iteration history (machine-readable)
├── progress.txt          # Human-readable progress log
├── segments/             # Individual slide scripts
│   └── (created during execution)
└── output/               # Final assembled output
    └── (created during assembly)
```

### Step 1.5: Present Planning Summary

```
TALK TRACK PLANNING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lecture: Long COVID and the Gut Microbiome
Physician: Dr. Robin Rose
Slides: 16

Voice Profile: 
  - Tone: Warm, conversational with clinical authority
  - Style: First-person plural, rhetorical questions
  - Source: Extracted from provided transcript

Target Metrics:
  - Speaking pace: 150 words/minute
  - Estimated duration: ~60 minutes
  - Max retries per slide: 2

Ready to begin generation. Proceed?
```

---

## Phase 2: Iterative Slide Generation

### The Generation Loop

For each slide segment, execute a **Plan → Generate → Validate → Complete/Retry** cycle:

```
┌─────────────────────────────────────────────────────────────┐
│                  PER-SLIDE GENERATION LOOP                   │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Load    │──▶│ Generate │──▶│ Validate │──▶│ Complete │ │
│  │  Context │   │  Script  │   │  Quality │   │ or Retry │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       │              │              │              │        │
│       │              │              │              │        │
│  Fresh context   Opus 4.5      4 criteria    Save or       │
│  per iteration   generation    checked       iterate       │
└─────────────────────────────────────────────────────────────┘
```

### Step 2.1: Load Slide Context

For each slide, prepare the generation context:

```javascript
const slideContext = {
  // Current slide content
  slide: lecture.slides[segmentIndex],
  
  // Voice profile for style matching
  voiceProfile: prd.voiceProfile,
  
  // Previous slide ending (for transition continuity)
  previousSlideEnding: segments[segmentIndex - 1]?.lastParagraph || null,
  
  // Next slide preview (for forward transitions)
  nextSlideTitle: lecture.slides[segmentIndex + 1]?.title || null,
  
  // Learnings from previous iterations
  learnings: progress.patterns || [],
  
  // Target metrics
  targetWordCount: segment.targetWordCount,
  wordsPerMinute: prd.config.wordsPerMinute
};
```

### Step 2.2: Generate Script Segment

Use the Task tool to spawn a fresh subagent with the slide generation prompt:

**Key generation requirements:**
1. Cover ALL content from the slide (paragraphs, bullets, definitions, callouts)
2. Verbally describe diagrams if present
3. Use natural transitions (no "[SLIDE]" markers)
4. Match voice profile tone and rhythm
5. Hit target word count within ±15%

**Output format:** Plain text, no headers, no formatting.

### Step 2.3: Validate Generated Script

Run four validation checks:

#### Check 1: Timing Validation
```javascript
const wordCount = script.split(/\s+/).length;
const targetMin = segment.targetWordCount * 0.85;
const targetMax = segment.targetWordCount * 1.15;
const timingPass = wordCount >= targetMin && wordCount <= targetMax;
```

#### Check 2: Content Coverage
```javascript
// Extract key terms from slide content
const keyTerms = extractKeyTerms(slide);
const mentionedTerms = keyTerms.filter(term => 
  script.toLowerCase().includes(term.toLowerCase())
);
const coveragePercent = mentionedTerms.length / keyTerms.length;
const coveragePass = coveragePercent >= 0.85; // 85% coverage required
```

#### Check 3: Flow Analysis
```javascript
// Check for run-on sentences
const sentences = script.split(/[.!?]+/);
const longSentences = sentences.filter(s => s.split(/\s+/).length > 40);
const flowPass = longSentences.length === 0;

// Check for varied rhythm
const sentenceLengths = sentences.map(s => s.split(/\s+/).length);
const hasVariation = standardDeviation(sentenceLengths) > 5;
```

#### Check 4: Transition Quality
```javascript
// Check for natural transition at end (if not last slide)
const transitionPhrases = [
  "let's", "now", "this brings us", "building on",
  "moving", "next", "consider", "turn to"
];
const lastParagraph = script.split('\n\n').pop();
const hasTransition = transitionPhrases.some(phrase =>
  lastParagraph.toLowerCase().includes(phrase)
);
const transitionPass = isLastSlide || hasTransition;
```

### Step 2.4: Handle Validation Results

**If ALL checks pass:**
```javascript
// Save segment
Write({
  file_path: `.talktrack-gen/segments/slide-${padNumber(index)}.txt`,
  content: script
});

// Update PRD
segment.status = 'completed';
segment.wordCount = wordCount;
segment.completedAt = new Date().toISOString();

// Log success
appendToProgress(`SEG-${index}: PASSED (${wordCount} words)`);
```

**If ANY check fails:**
```javascript
segment.attempts += 1;

if (segment.attempts >= prd.config.maxRetries) {
  segment.status = 'blocked';
  segment.blockedReason = failedChecks.join(', ');
  // Continue to next segment
} else {
  // Retry with feedback about what failed
  const retryContext = {
    ...slideContext,
    previousAttempt: script,
    failedChecks: failedChecks,
    feedback: generateRetryFeedback(failedChecks)
  };
  // Loop back to Step 2.2
}
```

### Step 2.5: Progress Tracking

After each segment, update TodoWrite and log progress:

```
SEGMENT PROGRESS
━━━━━━━━━━━━━━━━

SEG-001: Learning Objectives ✓ (225 words, 1 attempt)
SEG-002: Pathophysiological Mechanisms ✓ (380 words, 2 attempts)
SEG-003: The Gut-Lung Axis → IN PROGRESS
SEG-004: Microbiome Alterations ○ PENDING
...

Progress: 2/16 complete (12.5%)
Estimated remaining: ~45 minutes
```

---

## Phase 3: Assembly

### Step 3.1: Collect All Segments

Read all completed segment files in order:

```javascript
const segments = [];
for (let i = 1; i <= slideCount; i++) {
  const segmentPath = `.talktrack-gen/segments/slide-${padNumber(i)}.txt`;
  if (fileExists(segmentPath)) {
    segments.push(Read({ file_path: segmentPath }));
  } else {
    segments.push(`[BLOCKED: Slide ${i} could not be generated]`);
  }
}
```

### Step 3.2: Coherence Pass

Run a final coherence check on the assembled script:

**Coherence checks:**
1. Transition flow between segments
2. Consistent terminology throughout
3. No repetitive phrasing across segments
4. Natural overall rhythm
5. Proper opening hook and closing summary

**Minor adjustments allowed:**
- Smoothing transitions between segments
- Removing accidental repetition
- Ensuring consistent name/term usage

### Step 3.3: Generate Final Output

Write the assembled, polished script:

```javascript
Write({
  file_path: '.talktrack-gen/output/talktrack-final.txt',
  content: assembledScript
});
```

**Output characteristics:**
- Plain text only
- Natural paragraph breaks for pacing
- No headers, formatting, or markdown
- Ready to paste directly into ElevenLabs

### Step 3.4: Generate Summary Report

```
TALK TRACK GENERATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lecture: Long COVID and the Gut Microbiome
Physician: Dr. Robin Rose

Results:
  - Segments completed: 15/16
  - Segments blocked: 1
  - Total iterations: 22
  - Final word count: 9,450
  - Estimated duration: 63 minutes

Output:
  .talktrack-gen/output/talktrack-final.txt

Quality Metrics:
  - Average coverage: 94%
  - Transition quality: All natural bridges
  - Flow score: Good (varied rhythm)

Blocked Segments:
  - SEG-012: Exceeded retry limit (timing validation failed)
    Recommendation: Manually review slide 12 content density

Changelog:
  .talktrack-gen/changelogs/talktrack-2026-01-16-183000.md

Next Steps:
  1. Review output at .talktrack-gen/output/talktrack-final.txt
  2. Address any blocked segments manually
  3. Upload to ElevenLabs for voice generation
```

---

## Validation Criteria Reference

| Criterion | What It Checks | Pass Condition | Retry Feedback |
|-----------|----------------|----------------|----------------|
| **Timing** | Word count vs. target | Within ±15% | "Too long/short by X words" |
| **Coverage** | Key terms mentioned | ≥85% terms covered | "Missing: [terms]" |
| **Flow** | Sentence structure | No sentences >40 words | "Break up long sentences" |
| **Transitions** | Natural bridges | Transition phrase at end | "Add natural bridge to next topic" |

---

## State Files Reference

### prd.json

```json
{
  "sessionId": "talktrack-YYYY-MM-DD-physician-course-lecture",
  "createdAt": "ISO timestamp",
  "updatedAt": "ISO timestamp",
  "lecture": {
    "path": "content/physician-courses/...",
    "id": "lecture-id",
    "title": "Lecture Title",
    "slideCount": 16
  },
  "config": {
    "wordsPerMinute": 150,
    "maxRetries": 2,
    "model": "claude-opus-4-5-20250514"
  },
  "voiceProfile": {
    "source": "transcript" | "auto",
    "tone": "...",
    "sentenceRhythm": "...",
    "transitionStyle": "...",
    "samplePhrases": [...]
  },
  "segments": [
    {
      "segmentId": "SEG-001",
      "slideId": "slide-id",
      "slideTitle": "Slide Title",
      "targetWordCount": 225,
      "status": "pending" | "in_progress" | "completed" | "blocked",
      "attempts": 0,
      "wordCount": null,
      "completedAt": null,
      "blockedReason": null
    }
  ],
  "summary": {
    "totalSegments": 16,
    "pending": 16,
    "completed": 0,
    "blocked": 0
  }
}
```

### progress.txt

Human-readable log of all iterations and decisions:

```
================================================================================
TALK TRACK GENERATOR - PROGRESS LOG
================================================================================

Session: talktrack-2026-01-16-dr-robin-rose-gut-microbiome-1
Started: 2026-01-16T18:30:00.000Z
Lecture: Long COVID and the Gut Microbiome

================================================================================
VOICE PROFILE
================================================================================

Source: Provided transcript (./voice-samples/dr-rose.txt)
Tone: Warm, conversational with clinical authority
Style: First-person plural, uses rhetorical questions
Sample phrases:
  - "Here's what makes this different..."
  - "Let me show you what this looks like..."

================================================================================
GENERATION LOG
================================================================================

--- SEG-001 | Learning Objectives | Attempt 1 ---
Timestamp: 2026-01-16T18:31:15.000Z
Status: PASSED

Validation:
  ✓ Timing: 228 words (target: 225, within ±15%)
  ✓ Coverage: 100% (4/4 key terms)
  ✓ Flow: No long sentences
  ✓ Transitions: Natural bridge present

---

--- SEG-002 | Pathophysiological Mechanisms | Attempt 1 ---
Timestamp: 2026-01-16T18:32:45.000Z
Status: FAILED

Validation:
  ✓ Timing: 395 words (target: 380)
  ✗ Coverage: 71% (5/7 key terms missing: "EBV", "HHV-6")
  ✓ Flow: OK
  ✓ Transitions: OK

Retry feedback: Missing key terms. Ensure these are mentioned: EBV, HHV-6

---

--- SEG-002 | Pathophysiological Mechanisms | Attempt 2 ---
Timestamp: 2026-01-16T18:34:00.000Z
Status: PASSED

Validation:
  ✓ Timing: 388 words
  ✓ Coverage: 100% (7/7 key terms)
  ✓ Flow: OK
  ✓ Transitions: OK

---
```

---

## When to Use This Skill

**Use `/talktrack-generator` when:**
- You have a completed lecture JSON and need voiceover narration
- You want to generate audio via ElevenLabs or similar TTS
- You need consistent, high-quality spoken scripts
- You have a voice sample to match (optional)

**Do NOT use when:**
- Creating lectures from scratch (use `/physician-course-builder`)
- Iterating on lecture content (use `/lecture-iterator`)
- Just need a quick summary (manual is faster)

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `/lecture-iterator` | Iterate on lecture content based on feedback |
| `/physician-course-builder` | Create new lectures from scratch |
| `/generate-lectures` | Generate lectures from outline |

---

## Troubleshooting

### Segment blocked after retries

1. Check `.talktrack-gen/progress.txt` for failure reasons
2. Review the slide content - may be too dense
3. Options:
   - Manually write that segment
   - Split the slide in the source lecture
   - Increase `--max-retries`

### Voice doesn't match transcript

1. Verify transcript is clean text (no timestamps, speaker labels)
2. Provide longer transcript sample (>500 words recommended)
3. Check extracted voice profile in prd.json

### Output too long/short

1. Adjust `--words-per-minute` (lower = longer output)
2. Review slide content density
3. Consider splitting dense slides

### Resuming interrupted generation

```bash
/talktrack-generator --resume
```

This will:
1. Load existing state from `.talktrack-gen/`
2. Continue from the last pending segment
3. Preserve all completed work

---

## Example Output

Here's an example of generated output for the first slide of Dr. Robin Rose's gut microbiome lecture:

```
The gut is ground zero for understanding Long COVID. In this lecture, 
we're going to explore something that fundamentally changes how we 
think about post-acute COVID syndrome—and it starts with a surprising 
discovery about SARS-CoV-2.

Here's what makes this different from anything you've learned before: 
this virus doesn't just infect your cells. It infects the bacteria 
living inside you. It's acting as a bacteriophage, hijacking your gut 
microbiome to produce toxin-like peptides that explain many of the 
mysterious symptoms our patients are experiencing.

By the end of this lecture, you'll understand four critical concepts. 
First, the gut-lung axis and how SARS-CoV-2 directly affects the 
gastrointestinal tract through ACE2 receptors. Second, the virus's 
bacteriophage behavior and the production of these toxin-like peptides. 
Third, how to identify clinical symptom correlations with specific 
microbiome signatures. And fourth, a three-phase therapeutic protocol 
that I've developed: detox, restoration, and repair.

The key takeaway I want you to hold onto is this: the gut microbiome 
is both a mechanistic link in Long COVID pathogenesis and a therapeutic 
target. If you treat the gut first, everything else becomes easier.

Let's start with the mechanisms that drive Long COVID...
```

Notice:
- No headers or formatting
- Natural paragraph breaks
- All learning objectives covered
- Smooth transition to next topic
- Matches warm, authoritative voice style
