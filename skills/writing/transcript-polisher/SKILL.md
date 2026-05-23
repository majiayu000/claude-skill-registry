---
name: transcript-polisher
description: Transform raw podcast transcripts into polished, readable documents. This skill removes filler words, fixes grammar, adds structure, and preserves authentic voice. Use when processing podcast transcripts, interview recordings, video captions, or any spoken content that needs cleanup while maintaining 100% fidelity to meaning.
---

# Transcript Polisher

Transform raw podcast or interview transcripts into polished, professional documents that maintain authentic voice while dramatically improving readability.

## Purpose

Raw transcripts from automated services are often unreadable - filled with filler words, incomplete sentences, and poor formatting. This skill cleans them up while preserving what was actually said.

**Core Philosophy:** Balance authenticity with clarity. Remove everything that doesn't add meaning while preserving what was actually said. Create the "ideal version" of what the speaker wanted to communicate - without changing their words or ideas.

**Target:** 25-35% length reduction while maintaining 100% fidelity to meaning.

## When to Use This Skill

- Processing raw transcripts from Rev, Otter, Descript, YouTube auto-captions
- Cleaning up interview recordings or video transcripts
- Preparing spoken content for publication as articles or show notes
- Converting conversational content into readable written format

**Not for:** Written content that wasn't originally spoken, pre-polished articles, or scripts that are already edited.

---

## Workflow

### Step 1: Add Document Structure

Create proper header with:

```markdown
# [Guest Name]: [Compelling Episode Title]

*[Podcast Name] Episode - [Host Names]*

---

## Timestamped Outline
[Add 10 chapters maximum - see guidelines below]

---

## [Time] Chapter Title
[Content starts here]
```

**Timestamped Outline Rules:**
- Format: `**MM:SS** - Descriptive Chapter Title`
- 10 chapters maximum for 45-60 minute episodes
- Focus on major topic changes, not minute-by-minute
- Use compelling, specific titles (not generic descriptions)

**Good Examples:**
- ✅ **12:25** - The Turnaround: From Struggling to Thriving
- ✅ **29:08** - Why Successful Strategies Don't Spread

**Poor Examples:**
- ❌ **12:25** - Guest talks about their experience
- ❌ **29:08** - Discussion about the industry

### Step 2: Identify and Label Speakers

Replace generic speaker markers (>>, Speaker 1, etc.) with actual names:
- **Bold all speaker names**: `**Isaac:** Content here`
- Use first names for casual podcasts, full names for professional interviews
- Be consistent throughout

### Step 3: Aggressive Editing Pass

Apply aggressive polishing while maintaining 100% fidelity.

**Remove ALL filler words:**
- "um," "uh," "ah," "er," "hmm"
- "you know," "I mean," "like" (when used as filler)
- "so," "well," "basically," "literally" (when empty)
- "kind of," "sort of" (when hedging unnecessarily)

**Consolidate restarts:**
- ❌ "I think that... well, what I think is... the main thing is..."
- ✅ "The main thing is..."

**Pick the clearest version when speakers repeat:**
- If they say the same thing 3 ways, keep only the best one
- Combine fragments into complete thoughts

**Fix awkward grammar:**
- Complete sentence fragments
- Fix subject-verb agreement
- Repair run-on sentences

**Keep only the strongest examples:**
- If speaker gives 5+ examples, keep 1-2 best ones
- Remove redundant illustrations of the same point

**Add clarity to vague pronouns:**
- Use minimal bracketed additions: "they [the teachers] decided..."
- Only when meaning would be unclear otherwise

### Step 4: Preserve What Matters

**Never edit:**
- Unique voice and natural rhythm
- Exact wording of powerful statements
- Emotional moments and authenticity
- Specialized terminology
- Cultural references that reveal personality
- Natural dialogue patterns
- Humor and personality
- Memorable phrases

**The 100% Fidelity Rule:**
- ❌ Never paraphrase or change meaning
- ❌ Never add ideas not present in original
- ❌ Never remove key insights or stories
- ✅ Only remove redundancy and inefficiency
- ✅ Preserve exact wording of powerful statements
- ✅ Keep all substantive content

### Step 5: Quality Check

Before finishing:
- [ ] Length reduced by 25-35%
- [ ] All filler words removed
- [ ] Speakers properly identified and bolded
- [ ] Chapter breaks added with compelling titles
- [ ] Grammar fixed but voice preserved
- [ ] Key insights and stories intact
- [ ] No meaning changed or paraphrased
- [ ] Reads naturally when spoken aloud

---

## Editing Guidelines

### What TO Edit (Aggressively)

**1. Filler Words**
Remove ALL instances unless part of signature style:
- um, uh, ah, er, hmm
- you know, I mean, like
- so, well, basically, literally, actually
- kind of, sort of, I think, probably, maybe

**2. False Starts and Restarts**
```
Before: "I think that... well, what I was trying to say is... the main thing is that we need to focus"
After: "The main thing is that we need to focus"
```

**3. Redundant Explanations**
When the same point is made multiple ways, keep only the clearest version.

**4. Verbal Hedging (when excessive)**
```
Before: "I think it's probably maybe kind of important to sort of consider..."
After: "It's important to consider..."
```

**5. Conversational Detours**
Remove tangents that don't serve the narrative or provide insight.

**6. Grammar Issues**
- Incomplete sentences → complete
- Subject-verb disagreement → fix
- Run-on sentences → break up

**7. Excessive Examples**
If 5+ examples are given for one point, keep 1-2 strongest.

**8. Vague Pronouns (minimal intervention)**
Only add bracketed clarity when meaning is genuinely unclear:
```
"They [the board members] decided to..."
```

### What NOT to Edit

**1. Unique Voice and Natural Rhythm**
Keep the speaker's distinctive patterns, even if informal.

**2. Powerful Statements**
Preserve exact wording of quotable moments.

**3. Emotional Moments**
Don't sanitize authentic expressions:
- ✅ Keep: "That bugged the crap out of me"
- ❌ Don't change to: "That bothered me significantly"

**4. Specialized Terminology**
Keep industry/domain-specific language even if uncommon.

**5. Cultural References**
Preserve references that reveal personality and context.

**6. Natural Dialogue Patterns**
Keep the back-and-forth feel of conversation.

---

## Common Transcription Errors to Fix

### Auto-Caption Issues
- OCR errors (e.g., "quad code" → "Claude Code")
- Homophone mistakes ("their" vs "there")
- Missing punctuation
- Run-on sentences
- Mis-identified technical terms

### Audio Transcription Issues
- Speaker confusion
- Overlapping dialogue
- Background noise artifacts
- Timestamp errors

---

## Output Format

Final polished transcript should be:
- Markdown formatted
- Properly sectioned with timestamps
- Speaker names bold and consistent
- 25-35% shorter than original
- Grammar perfect but voice authentic
- Ready for publication or repurposing

---

## Before/After Examples

### Example 1: Filler Removal

**Before:**
> "So, um, I think that, you know, what we really need to focus on is, like, the fact that, you know, students are, um, actually learning better when, you know, they have more autonomy."

**After:**
> "Students learn better when they have more autonomy."

(15 words → 8 words = 47% reduction)

### Example 2: Consolidating Restarts

**Before:**
> "The thing about... what I'm trying to say is... the main point here is that we need to rethink how we approach this. We need to rethink our approach. What I mean is, the whole system needs to be reconsidered."

**After:**
> "The whole system needs to be reconsidered."

(Kept only the clearest expression of the idea)

### Example 3: Voice Preservation

**Before:**
> "Look, this bugged the crap out of me for years. Nobody wanted to talk about it. Like, everyone knew, but nobody would say anything."

**After:**
> "Look, this bugged the crap out of me for years. Nobody wanted to talk about it. Everyone knew, but nobody would say anything."

(Only removed the filler "like" - preserved the authentic voice and expression)

---

## Bundled Resources

- `references/editing-guidelines.md` - Detailed editing rules with examples
- `references/structure-template.md` - Header format and chapter guidelines

---

## Related Skills

- **anti-ai-writing** - Further humanize and polish the output
- **social-content-creation** - Repurpose transcript insights to social posts
- **hook-and-headline-writing** - Create compelling chapter titles

---

*Remember: 100% fidelity to meaning, 25-35% reduction in length. Remove what doesn't add meaning. Preserve what makes it authentic.*
