---
name: transcript-polisher
description: Transform raw podcast transcripts into polished, readable documents. Use when processing podcast transcripts, interview recordings, or any spoken content that needs cleanup. Removes filler words, fixes grammar, adds structure, while preserving authentic voice and key insights.
---

# Transcript Polisher

Transform raw podcast or interview transcripts into polished, professional documents that maintain authentic voice while dramatically improving readability and flow.

## When to Use This Skill

Use this skill when:
- Processing raw podcast transcripts from automated services (Rev, Otter, Descript, YouTube auto-captions)
- Cleaning up interview recordings or video transcripts
- Preparing spoken content for publication as articles or show notes
- Converting conversational content into readable written format

**Not for:** Written content that wasn't originally spoken, pre-polished articles, or scripts that are already edited.

## Core Philosophy

**Balance authenticity with clarity**: Remove everything that doesn't add meaning while preserving what was actually said. Create the "ideal version" of what the speaker wanted to communicate—without changing their words or ideas.

**Target**: 25-35% length reduction while maintaining 100% fidelity to meaning.

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

**Timestamped Outline Rules** (My First Million style):
- Format: `**MM:SS** - Descriptive Chapter Title`
- 10 chapters maximum for 45-60 minute episodes
- Focus on major topic changes, not minute-by-minute
- Use compelling, specific titles (not generic descriptions)

**Good Examples:**
- ✅ **12:25** - The 13th Percentile to Grade Level Miracle
- ✅ **29:08** - Why Successful Reforms Don't Spread

**Poor Examples:**
- ❌ **12:25** - Michelle talks about her students
- ❌ **29:08** - Discussion about education reform

### Step 2: Identify and Label Speakers

Replace generic speaker markers (>>, Speaker 1, etc.) with actual names:
- **Bold all speaker names**: `**Isaac:** Content here`
- Use first names for casual podcasts, full names for professional interviews
- Be consistent throughout

### Step 3: Aggressive Editing Pass

Apply aggressive polishing while maintaining 100% fidelity. See [Editing Guidelines](references/editing-guidelines.md) for detailed rules.

**Quick checklist:**
- Remove ALL filler words ("um," "uh," "you know," "like," "so," "I mean")
- Consolidate false starts and restarts
- Pick the clearest version when speakers repeat themselves
- Remove verbal hedging ("kind of," "sort of," "I think," "probably") when excessive
- Cut conversational detours that don't serve the narrative
- Fix awkward grammar and incomplete thoughts
- Keep only 1-2 strongest examples if speaker gives 5+
- Add clarity to vague pronouns (minimal bracketed additions)

### Step 4: Preserve What Matters

**Never edit:**
- Unique voice and natural rhythm
- Exact wording of powerful statements
- Emotional moments and authenticity
- Specialized terminology
- Cultural references that reveal personality
- Natural dialogue patterns

### Step 5: Quality Check

Before finishing:
- [ ] Length reduced by 25-35%
- [ ] All filler words removed
- [ ] Speakers properly identified
- [ ] Chapter breaks added with compelling titles
- [ ] Grammar fixed but voice preserved
- [ ] Key insights and stories intact
- [ ] No meaning changed or paraphrased

## Quick Reference

For detailed examples and transformation patterns, see:
- [Editing Guidelines](references/editing-guidelines.md) - Complete rules with before/after examples
- [Structure Template](references/structure-template.md) - Header format and chapter guidelines

## Common Transcription Errors to Fix

**Auto-caption issues:**
- OCR errors (e.g., "quad code" → "Claude Code")
- Homophone mistakes (e.g., "their" vs "there")
- Missing punctuation
- Run-on sentences
- Mis-identified technical terms

**Audio transcription issues:**
- Speaker confusion
- Overlapping dialogue
- Background noise artifacts
- Timestamp errors

## Output Format

Final polished transcript should be:
- Markdown formatted
- Properly sectioned with timestamps
- Speaker names bold and consistent
- 25-35% shorter than original
- Grammar perfect but voice authentic
- Ready for publication or repurposing

## Critical Reminders

**100% Fidelity Rule:**
❌ Never paraphrase or change meaning
❌ Never add ideas not present in original
❌ Never remove key insights or stories
✅ Only remove redundancy and inefficiency
✅ Preserve exact wording of powerful statements
✅ Keep all substantive content

**Aggressive Editing:**
❌ "So, um, I think that, you know, what we really need to focus on..."
✅ "What we really need to focus on..."

**Voice Preservation:**
❌ Removing authentic expressions like "bugged the crap out of me"
✅ Keeping natural language that shows personality
