---
name: clip-extraction
description: Identify best clips from raw video footage by transcribing with timestamps, identifying high-emotion moments, and scoring clips for ad potential. Use when processing founder interviews, UGC footage, or any raw video to extract usable ad components.
---

# Clip Extraction

Extract and catalog best moments from raw footage.

## Process

### Step 1: Transcribe with Timestamps

**Transcription Methods:**
- AI transcription (Claude, Whisper, Descript)
- Manual review for accuracy
- Include timestamps every 10-30 seconds

**Format:**
```
[00:00] Opening small talk
[00:45] "The reason I started this company was..."
[01:23] Gets emotional about customer story
[02:15] Explains unique mechanism
...
```

### Step 2: Identify High-Emotion Moments

**Emotion Markers:**
- Voice changes (gets louder, softer, cracks)
- Pauses before important statements
- Laughing or crying
- Passionate explanations
- Authentic frustration
- Surprise or excitement

**Flag These Moments:**
- Real reactions (not scripted)
- Vulnerable admissions
- Powerful stories
- "Aha" moments
- Customer impact stories

### Step 3: Tag by Content Type

**HOOK Clips**
- Attention-grabbing statements
- Provocative claims
- Curiosity-inducing openers
- Pattern interrupts

**SOCIAL PROOF Clips**
- Customer stories
- Results mentions
- Testimonial moments
- Endorsements

**NARRATIVE Clips**
- Origin story pieces
- Problem explanations
- Solution discoveries
- Transformation arcs

**CTA Clips**
- Direct calls to action
- Recommendation statements
- "You should try this" moments
- Risk reversal mentions

**OBJECTION HANDLING Clips**
- Skeptic responses
- Trust building
- "Why us" explanations
- Price justification

### Step 4: Score for Ad Potential

**Scoring Criteria (1-10):**

| Factor | Weight | Score |
|--------|--------|-------|
| Authenticity | 25% | X |
| Emotion | 25% | X |
| Clarity | 20% | X |
| Relevance | 20% | X |
| Technical Quality | 10% | X |

**Authenticity:** Does it feel real, unscripted?
**Emotion:** Does it evoke feeling?
**Clarity:** Is the message clear?
**Relevance:** Does it serve an ad purpose?
**Technical:** Is audio/video usable?

### Step 5: Output Clip List

```
## CLIP EXTRACTION: [Video Source]
Total Duration: [X:XX]
Clips Identified: [#]
High-Value Clips: [#]

---

### HOOK CLIPS (Score 8+)

**CLIP H1** [02:34 - 02:41]
- Quote: "I never thought I'd be the one to..."
- Emotion: Vulnerability
- Score: 9/10
- Usage: Top of funnel hook
- Notes: Great pause before revelation

**CLIP H2** [05:12 - 05:18]
...

---

### SOCIAL PROOF CLIPS

**CLIP SP1** [08:45 - 09:12]
- Quote: "A customer told me she cried when..."
- Emotion: Pride/Joy
- Score: 9/10
- Usage: Testimonial body section
- Notes: Genuine tears, very powerful

**CLIP SP2** [12:30 - 12:55]
...

---

### NARRATIVE CLIPS

**CLIP N1** [00:45 - 01:30]
- Content: Origin story - why started company
- Emotion: Determination
- Score: 7/10
- Usage: Story-based ad body
- Notes: Good but could be tighter

---

### CTA CLIPS

**CLIP C1** [18:20 - 18:35]
- Quote: "If you're struggling with X, just try it"
- Emotion: Confidence
- Score: 8/10
- Usage: End of ad CTA
- Notes: Direct, authentic recommendation

---

### OBJECTION HANDLING CLIPS

**CLIP O1** [14:55 - 15:20]
- Objection addressed: Price concerns
- Quote: "I know it seems expensive but..."
- Score: 7/10
- Usage: Middle/bottom funnel

---

### TOP 10 CLIPS (Ranked)

| Rank | Clip ID | Timestamp | Type | Score | Primary Use |
|------|---------|-----------|------|-------|-------------|
| 1 | SP1 | 08:45 | Social Proof | 9 | Body |
| 2 | H1 | 02:34 | Hook | 9 | Opening |
| 3 | ... | ... | ... | ... | ... |

---

### AD COMBINATIONS

**Combo 1: Full Story Arc**
- Hook: H1 (02:34)
- Body: N1 (00:45) + SP1 (08:45)
- CTA: C1 (18:20)
- Est. length: 60s

**Combo 2: Quick Proof**
- Hook: H2 (05:12)
- Body: SP1 (08:45)
- CTA: C1 (18:20)
- Est. length: 30s

---

### CLIPS NEEDING RE-SHOOT
[List any moments worth capturing again with better setup]

### MISSING CONTENT
[Content types not captured that should be]
```

## Extraction Tips (Kamal FounderAds)

**What to Look For:**
- Pain in their eyes when telling real stories
- Moments they haven't rehearsed
- Stories > Statements (22x more memorable)
- Authentic emotional responses

**Technical Considerations:**
- Good audio is essential (external mic)
- Lighting can be imperfect (authenticity)
- iPhone quality is fine
- Background should be interesting

**Organization System:**
- Folder per video source
- Subfolders by clip type
- Clear naming convention
- Timestamp in filename

Source: Kamal FounderAds, LeadsIcon
