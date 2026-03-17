---
name: audiobook-production
description: "Master ACX-compliant audiobook production using Audible's technical standards and Richard Mayer's multimedia learning principles for engaging, professional audio. Use when: Producing an audiobook for Audible/ACX distribution; Creating audio versions of courses or written content; Setting up narration workflow for long-form content; Ensuring audio meets professional distribution standards; Self-producing an audiobook as an author"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Audiobook Production

> Master ACX-compliant audiobook production using Audible's technical standards and Richard Mayer's multimedia learning principles for engaging, professional audio.

## When to Use This Skill

- Producing an audiobook for Audible/ACX distribution
- Creating audio versions of courses or written content
- Setting up narration workflow for long-form content
- Ensuring audio meets professional distribution standards
- Self-producing an audiobook as an author
- Managing audiobook production projects

## Methodology Foundation

**Source**: ACX (Audiobook Creation Exchange) + Richard Mayer (Multimedia Learning)

**Core Principle**: Professional audiobook production balances technical excellence (meeting strict ACX standards) with engaging delivery (applying learning science principles). As Mayer's research shows: "People learn better from friendly human voice than machine voice" (Voice Principle).

**Why This Matters**: ACX/Audible rejects audiobooks that don't meet technical specifications, wasting production time and money. Beyond technical compliance, understanding how listeners process audio enables production choices that maximize engagement and retention.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Ensures ACX technical compliance** - Specs for bit rate, sample rate, RMS, peaks, and noise floor
2. **Structures audiobook projects** - Chapter organization, credits, retail samples
3. **Applies learning principles** - Pacing, tone, and delivery that aid comprehension
4. **Manages production workflow** - From script to final master
5. **Handles proofing and QC** - Catching errors before submission

## How to Use

### Check ACX Compliance
```
Help me verify this audiobook meets ACX submission requirements.
[provide audio specs or describe setup]
```

### Plan Audiobook Structure
```
Help me structure an audiobook from this manuscript:
Total word count: [X]
Chapters: [Y]
Type: [Fiction/Non-fiction]
```

### Create Production Workflow
```
Create a production plan for my audiobook project:
Book length: [word count]
Narrator: [self/hired]
Deadline: [date]
```

## Instructions

When producing audiobooks, follow this methodology:

### Step 1: Understand ACX Technical Requirements

ACX has strict specifications that must be met for acceptance.

```
## ACX Audio Specifications (2026)

### File Format
- MP3, 192 kbps or higher (constant bit rate)
- 44.1 kHz sample rate
- Mono (single channel)

### Audio Levels
- RMS: -23dB to -18dB
- Peak values: -3dB maximum (no clipping)
- Noise floor: -60dB or lower

### File Naming
- Chapter files: [BookTitle]_[ChapterNumber].mp3
- Opening credits: [BookTitle]_Opening_Credits.mp3
- Closing credits: [BookTitle]_Closing_Credits.mp3

### Content Requirements
- Opening credits (first file): Title, author, narrator
- Closing credits (last file): "This has been [title] by [author], narrated by [narrator]"
- Each chapter file is standalone (no cross-file audio)
- Consistent room tone throughout

### Quality Requirements
- No extraneous sounds (mouth clicks, pops, page turns)
- Consistent audio quality across all files
- Retail sample: ~5 minutes of representative content
```

**Critical**: Run ACX Check tool on every file before submission.

---

### Step 2: Prepare the Manuscript

Before recording, optimize the text for audio delivery.

```
## Manuscript Preparation Checklist

### Structure
□ Chapter breaks clearly marked
□ Section breaks identified (longer pause points)
□ Footnotes converted to in-text explanations or removed
□ Visual content (charts, tables) adapted for audio or noted for skip

### Pronunciation Guide
□ Character names with phonetic spelling
□ Foreign words and phrases
□ Technical terms and jargon
□ Place names and proper nouns
□ Acronyms expanded or spelled out

### Narrator Notes
□ Tone shifts marked
□ Character voice cues (if fiction)
□ Emphasis suggestions (minimal)
□ "As shown in Figure X" → adapted for audio
□ Author asides or commentary identified

### Timing Estimate
□ Word count per chapter
□ Total word count
□ Estimated runtime: words ÷ 9,300 = hours (approx)
   - 50,000 words ≈ 5-6 hours
   - 80,000 words ≈ 8-9 hours
```

---

### Step 3: Set Up Recording Environment

Consistent, quality recording requires proper setup.

```
## Home Studio Essentials

### Minimum Equipment
- **Microphone**: USB condenser (AT2020, Blue Yeti) or XLR setup
- **Pop filter**: Essential for plosives
- **Mic stand**: Stable positioning
- **Headphones**: Closed-back, wired

### Room Treatment
- Record in smallest, most furnished room available
- Hang blankets on hard surfaces
- Use reflection filter behind mic
- Close windows, turn off HVAC
- Eliminate electronic hum (fridges, computers)

### Recording Software (DAW)
- Free: Audacity, GarageBand
- Professional: Adobe Audition, Reaper, Pro Tools
- ACX-specific: Hindenburg Pro (audiobook workflow)

### Test Recording Checklist
□ Record 30 seconds of room tone
□ Record test passage
□ Check RMS levels (-23 to -18 dB)
□ Check peak levels (below -3 dB)
□ Check noise floor (below -60 dB)
□ Listen for room echo or hum
□ Verify consistent mic positioning
```

---

### Step 4: Apply Mayer's Multimedia Learning Principles

Science-backed techniques for engaging audio.

```
## Mayer's Principles for Audiobook Delivery

### Voice Principle
"People learn better from human voice than machine voice."
→ Warm, conversational delivery beats polished broadcast voice
→ Let personality come through
→ Avoid monotone "reading" voice

### Personalization Principle
"People learn better when words are conversational rather than formal."
→ Write/deliver as if talking to one person
→ Use "you" and "we"
→ Contractions are encouraged

### Segmenting Principle
"People learn better when content is in learner-paced segments."
→ Clear chapter breaks
→ Section pauses for complex material
→ Chapter summaries for dense non-fiction

### Redundancy Principle (for video/slides)
"People learn better from graphics and narration than graphics + narration + text."
→ For audiobooks: don't describe visual elements you can't show
→ Adapt visual content or acknowledge it's omitted

### Coherence Principle
"People learn better when extraneous material is excluded."
→ Cut verbal filler
→ Remove tangents that don't serve the chapter
→ Every word earns its place
```

---

### Step 5: Production Workflow

Systematic process from script to master.

```
## Audiobook Production Pipeline

### Phase 1: Pre-Production (Week 1-2)
□ Manuscript finalized and proofread
□ Pronunciation guide complete
□ Chapter structure confirmed
□ Recording schedule created
□ Test recordings approved

### Phase 2: Recording (Weeks 2-6, varies by length)
□ Opening credits recorded first
□ Chapters recorded in order (usually)
□ Room tone captured each session
□ Daily backup of raw files
□ Notes logged for pickups needed

### Phase 3: Editing (Concurrent or following)
□ Remove mistakes and restart takes
□ Remove excessive breaths (keep natural ones)
□ Eliminate mouth clicks and pops
□ Smooth edits (crossfade)
□ Consistent pacing throughout

### Phase 4: Mastering
□ Noise reduction applied (light touch)
□ Compression for consistent levels
□ Limiting to prevent peaks
□ Final RMS check (-23 to -18 dB)
□ Export to ACX specs (192 kbps MP3, 44.1kHz, mono)

### Phase 5: Quality Control
□ Listen to every file start to finish
□ Check first/last 5 seconds of each file
□ Verify file naming convention
□ Run ACX Check or similar tool
□ Create retail sample (5 min)
```

---

### Step 6: Credits and Sample

Specific requirements for opening, closing, and retail sample.

```
## Opening Credits Script
(Must be first audio file)

"[Book Title]"
Written by [Author Name]
Narrated by [Narrator Name]

[Optional: Publisher name]
[Optional: Copyright year]

---

## Closing Credits Script
(Must be last audio file)

"This has been [Book Title], written by [Author Name],
narrated by [Narrator Name]."

[Optional: "Visit [website] for more" or other approved callout]
[Optional: "Audiobook production by [producer]"]

---

## Retail Sample Guidelines

**Length**: Approximately 5 minutes
**Content**: Representative excerpt that hooks listeners
**Selection criteria**:
- Showcases narrator's ability
- Engages interest without major spoilers
- Demonstrates the book's voice/style
- Often from early chapters (context not required)

**Do NOT include**: Credits or chapter announcements in sample
```

## Examples

### Example 1: Self-Published Non-Fiction Audiobook

**Context**: An author is self-narrating their business book.

**Input**:
> Help me plan audiobook production for my 55,000-word business book. I'm self-narrating. I have a Blue Yeti mic and record in my home office.

**Output**:

## Production Plan: Business Book Audiobook

### Project Specifications
- **Word count**: 55,000 words
- **Estimated runtime**: 5.5-6 hours
- **Narrator**: Author (self-narrated)
- **Equipment**: Blue Yeti USB mic (adequate for ACX)

### Pre-Production (Days 1-3)

**Manuscript Prep**
- Review all 12 chapters for audio adaptation
- Convert/adapt 8 figures referenced in text
- Create pronunciation guide for industry terms
- Mark chapter breaks and section pauses
- Estimate 4,500 words/chapter average = ~29 min/chapter

**Room Preparation**
- Assess home office acoustics
- Add blanket on wall behind recording position
- Use closet with clothes as recording booth alternative
- Test recordings at 3 different times of day (HVAC, traffic noise)

**Sample Script**:
"As shown in Figure 3" → "Here's how it works: imagine a funnel with three stages..."

### Recording Schedule (Weeks 1-3)

**Daily recording block**: 2 hours max (voice fatigue)
**Target per session**: 1.5-2 chapters (8,000 words)
**Total sessions needed**: ~8-10

**Schedule**:
- Day 1: Opening credits + Chapter 1
- Day 2: Chapters 2-3
- Day 3: Chapters 4-5
- [continue pattern]
- Day 8: Chapter 12 + Closing credits
- Days 9-10: Pickups and problem sections

**Session Ritual**:
1. Hydrate 30 min before (room temp water)
2. Vocal warmup (5 min)
3. Record room tone (10 sec)
4. Test recording, check levels
5. Record chapter(s)
6. Log pickup notes

### Post-Production (Week 4)

**Editing workflow per chapter**:
1. Import raw audio
2. Remove mistakes and alternate takes
3. Clean up breaths and mouth clicks
4. Apply light noise reduction
5. Normalize RMS to -20 dB
6. Check peaks (below -3 dB)
7. Export as MP3 (192 kbps, 44.1 kHz, mono)

**File naming**:
- BusinessBookTitle_Opening_Credits.mp3
- BusinessBookTitle_001.mp3
- BusinessBookTitle_002.mp3
- ...
- BusinessBookTitle_012.mp3
- BusinessBookTitle_Closing_Credits.mp3

### Quality Control (Days 1-2)

- Listen through every file with checklist
- Run ACX Check on all files
- Create 5-minute retail sample from Chapter 2
- Verify consistent sound across all chapters
- Final review of opening/closing credits

### Technical Settings

**Recording**:
- 44.1 kHz, 24-bit WAV (edit in high quality)
- Mono input
- Gain set for peaks at -12 dB

**Export (ACX compliant)**:
- MP3, 192 kbps CBR
- 44.1 kHz
- Mono
- RMS: -20 dB (within -23 to -18)
- Peak: -3 dB max

---

### Example 2: ACX Troubleshooting

**Context**: Audiobook files are being rejected by ACX.

**Input**:
> My audiobook submission was rejected. ACX says "RMS levels out of spec" and "noise floor too high." How do I fix this?

**Output**:

## ACX Rejection Fix: RMS and Noise Floor

### Diagnosis

**RMS out of spec**: Your audio is either too quiet (below -23 dB) or too loud (above -18 dB)

**Noise floor too high**: Background hiss or hum is above -60 dB

### Step-by-Step Fix

**Fix 1: RMS Levels**

In Audacity:
1. Select all audio (Ctrl+A)
2. Effect → Loudness Normalization
3. Set to: -20 dB RMS (middle of ACX range)
4. Apply

In Adobe Audition:
1. Select all
2. Effects → Amplitude → Match Loudness
3. Set Target Loudness to -20 LUFS
4. Process

**Fix 2: Noise Floor**

*If noise is mild (just room tone)*:
1. Find 2-3 seconds of "silence" (room tone only)
2. Select it as noise profile
3. Apply noise reduction to full track
4. Use minimal settings (6-12 dB reduction) to avoid artifacts

In Audacity:
- Effect → Noise Reduction → Get Noise Profile
- Select all → Noise Reduction → 6-12 dB, 6 Sensitivity

*If noise is significant*:
- Re-record in quieter environment
- Use noise gate (removes sound below threshold)
- Consider iZotope RX for professional repair

**Fix 3: Verify Peaks**

After RMS adjustment, peaks may exceed -3 dB:
1. Effect → Limiter
2. Set ceiling to -3.0 dB
3. Apply

### Verification Workflow

1. Make fixes to one chapter first
2. Run ACX Check plugin or online tool
3. Verify all specs pass:
   - RMS: -23 to -18 dB ✓
   - Peak: -3 dB or lower ✓
   - Noise floor: -60 dB or lower ✓
4. Apply same process to all files
5. Re-check each file before resubmitting

### Prevention for Future

**Recording checklist**:
- Noise floor below -60 dB before recording
- Gain set so peaks hit -12 dB when speaking
- Room tone recorded each session
- Test file checked before full session

## Checklists & Templates

### ACX Pre-Submission Checklist

```
## Technical Compliance

□ All files are 192 kbps MP3, 44.1 kHz, mono
□ RMS levels between -23 and -18 dB
□ Peak values at or below -3 dB
□ Noise floor at or below -60 dB
□ No clipping or distortion
□ Consistent levels across all chapters

## File Structure

□ Opening credits file present
□ Closing credits file present
□ Files named correctly: [Title]_[Number].mp3
□ Chapter numbers are sequential
□ No missing chapters
□ Retail sample created (≈5 minutes)

## Content Quality

□ First/last 5 seconds of each file are clean (room tone or fade)
□ No extraneous sounds (clicks, pops, breaths)
□ No room echo or reverb issues
□ Consistent voice quality throughout
□ All pickups and corrections completed
□ Credits read correctly (title, author, narrator)

## Final Review

□ Listened to complete audiobook
□ Spot-checked transitions between chapters
□ Verified retail sample is representative
□ Cover art meets ACX specs (if applicable)
□ All metadata entered correctly
```

---

### Production Schedule Template

```
## Audiobook Production Schedule

**Title**: ________________________________
**Word count**: ___________ | **Est. runtime**: ___________
**Narrator**: _____________________________
**Target completion**: ____________________

### Pre-Production: Week ___

| Task | Due | Done |
|------|-----|------|
| Manuscript finalized | | □ |
| Pronunciation guide | | □ |
| Room/equipment tested | | □ |
| Opening credits scripted | | □ |

### Recording: Weeks ___ - ___

| Session | Chapters | Words | Est. Time | Done |
|---------|----------|-------|-----------|------|
| 1 | Credits + Ch 1 | | | □ |
| 2 | Ch 2-3 | | | □ |
| 3 | Ch 4-5 | | | □ |
| ... | | | | □ |

### Post-Production: Week ___

| Task | Due | Done |
|------|-----|------|
| Editing complete | | □ |
| Mastering complete | | □ |
| ACX specs verified | | □ |
| QC listen-through | | □ |
| Retail sample created | | □ |

### Submission: ___________
```

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- ACX. "Audio Submission Requirements" - Official technical specifications
- Richard Mayer. "Multimedia Learning" (2009) - Scientific principles for audio learning
- iZotope. "Professional Voice Over Recording Tips" - Technical recording guidance
- Audacity Team. "Audacity Manual" - Free editing software

## Related Skills

- [voiceover-direction](../voiceover-direction/) - Directing talent for quality delivery
- [audio-editing](../audio-editing/) - Post-production fundamentals
- [voice-design](../voice-design/) - AI voice alternatives for narration
- [transcription-to-content](../transcription-to-content/) - Repurposing audiobook content

---

## Skill Metadata (Internal Use)

```yaml
name: audiobook-production
category: audio
subcategory: voiceover
version: 1.0
author: MKTG Skills
source_expert: ACX, Richard Mayer
source_work: ACX Submission Requirements, Multimedia Learning
difficulty: intermediate
estimated_value: $500-2,000 per audiobook (equivalent production management)
tags: [audiobook, acx, audible, narration, production]
created: 2026-01-26
updated: 2026-01-26
```
