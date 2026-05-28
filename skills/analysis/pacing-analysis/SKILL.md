---
name: pacing-analysis
description: Analyze narrative pacing and identify slow or rushed sections
category: analysis
---

# Pacing Analysis Skill

Analyze the pacing of your manuscript to identify sections that may be too slow or too fast.

## Usage

```bash
/pacing-analysis --chapter 3
/pacing-analysis --all
```

## Metrics Analyzed

- **Scene Length**: Word count per section
- **Dialogue Density**: Percentage of dialogue vs narration
- **Action Verbs**: Frequency of active vs passive voice
- **Sentence Variety**: Length and structure patterns
- **Paragraph Rhythm**: Short vs long paragraph balance

## Pacing Types

### Fast Pacing
- Short sentences
- High dialogue ratio
- Active verbs
- Brief descriptions
- Quick scene changes

**Use For**: Action, climax, tension

### Medium Pacing
- Varied sentence length
- Balanced dialogue/narration
- Mix of active/descriptive
- Standard paragraphs

**Use For**: Development, revelation, transition

### Slow Pacing
- Longer sentences
- Detailed description
- Internal monologue
- Extended paragraphs
- Deep reflection

**Use For**: Setup, backstory, atmosphere

## Analysis Output

```
PACING REPORT - Chapter 3

Section 3.1: SLOW (2,450 words, 12% dialogue)
- Recommendation: Tighten exposition, add action beats

Section 3.2: FAST (850 words, 68% dialogue)
- Recommendation: Good for confrontation scene

Section 3.3: SLOW (2,100 words, 5% dialogue)
- Recommendation: Consider breaking into smaller scenes

Overall Chapter Pacing: Uneven
- Start: Too slow (lose reader momentum)
- Middle: Well-paced action
- End: Drags (needs sharper conclusion)

Suggestions:
- Cut 600 words from Section 3.1 opening
- Add tension earlier in chapter
- Sharpen ending of Section 3.3
```
