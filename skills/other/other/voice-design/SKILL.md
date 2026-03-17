---
name: voice-design
description: "Select and create the perfect AI voice for your content using ElevenLabs, Qwen3-TTS, and other platforms—matching voice characteristics to brand personality and audience. Use when: Choosing an AI voice for video narration; Creating a consistent brand voice across content; Cloning a voice for scalable production; Comparing voice synthesis platforms; Designing voice characteristics by description"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# AI Voice Design

> Select and create the perfect AI voice for your content using ElevenLabs, Qwen3-TTS, and other platforms—matching voice characteristics to brand personality and audience.

## When to Use This Skill

- Choosing an AI voice for video narration
- Creating a consistent brand voice across content
- Cloning a voice for scalable production
- Comparing voice synthesis platforms
- Designing voice characteristics by description
- Casting multiple voices for different characters/uses

## Methodology Foundation

**Source**: ElevenLabs + Qwen3-TTS + Voice Design Best Practices

**Core Principle**: "La voix est 50% de l'impact d'une vidéo"—a poorly chosen or generated voice breaks the illusion. The best AI voice is one listeners don't notice is AI. This requires matching voice characteristics (age, gender, tone, pace) to content type and audience expectations.

**Why This Matters**: AI voice synthesis has reached human-level quality for most use cases, enabling content creation at scale. But the technology is only as good as the voice selection. A mismatched voice undermines content regardless of how natural it sounds.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Matches voice to brand** - Translates brand attributes into voice characteristics
2. **Selects optimal platform** - ElevenLabs vs Qwen3-TTS vs alternatives based on needs
3. **Designs voices by description** - Creates custom voices from text prompts
4. **Manages voice consistency** - Maintains the same voice across projects
5. **Casts multi-voice projects** - Selects complementary voices for dialogues/characters

## How to Use

### Select AI Voice
```
Help me choose an AI voice for [content type].
Brand: [personality]
Audience: [who]
Content: [describe]
Platform preference: [if any]
```

### Design Custom Voice
```
Design a voice for my brand:
Brand personality: [traits]
Target audience: [who]
Use cases: [where voice will be used]
```

### Compare Platforms
```
Compare voice platforms for my needs:
Volume: [how much content]
Languages: [which]
Budget: [range]
Features needed: [cloning, real-time, etc.]
```

## Instructions

When designing AI voices, follow this methodology:

### Step 1: Define Voice Requirements

Before choosing a platform or voice, document what you need.

```
## Voice Requirements Worksheet

### Brand Alignment
**Brand personality** (3-5 traits):
**Tone of voice** (formal/casual/playful/etc.):
**Existing brand sounds** (if any):

### Audience Match
**Primary audience** (age, context):
**What voice would they trust?**
**What voice would feel authentic to them?**

### Technical Requirements
**Languages needed**:
**Monthly volume** (minutes/hours):
**Real-time needed?** (yes/no):
**Voice cloning needed?** (yes/no):
**Budget** (monthly):

### Content Types
□ Long-form narration (courses, audiobooks)
□ Short-form video (social, ads)
□ Conversational (chatbots, assistants)
□ Character voices (multiple speakers)
□ Localization (same voice, multiple languages)
```

---

### Step 2: Choose Your Platform

Match platform to requirements.

```
## Platform Decision Matrix (2026)

### ElevenLabs
**Best for**: Premium quality, voice cloning, multilingual
**Pricing**: $5-330/mo
**Languages**: 29+
**Voice cloning**: Yes (from $22/mo)
**Latency**: 75ms (Flash v2.5)

**Choose if**:
- Quality is top priority
- Need professional voice cloning
- Require many languages with same voice
- Budget allows $20+/mo

### Qwen3-TTS (Open Source)
**Best for**: Self-hosted, zero marginal cost, privacy
**Pricing**: Free (+ GPU costs)
**Languages**: 10
**Voice cloning**: Yes (zero-shot from 3 seconds)
**Latency**: 97ms streaming

**Choose if**:
- Processing sensitive data locally
- High volume (cost per minute matters)
- Technical capability to self-host
- Need real-time streaming

### Murf.ai
**Best for**: Professional voiceover, video workflow
**Pricing**: $19-99/mo
**Languages**: 45+
**Voice cloning**: Limited
**Special**: "Say It My Way" intonation control

**Choose if**:
- Need studio voiceover quality
- Video production workflow
- Team collaboration needed
- Want precise pronunciation control

### OpenAI TTS
**Best for**: Simple integration, developer-focused
**Pricing**: $15/M characters
**Languages**: Limited
**Voices**: 6 presets (alloy, echo, fable, onyx, nova, shimmer)

**Choose if**:
- Already using OpenAI ecosystem
- Simple API integration needed
- Don't need customization
- Light usage

### Budget Decision

| Budget | Recommendation |
|--------|----------------|
| $0 | Qwen3-TTS (self-hosted) |
| $5-20/mo | ElevenLabs Starter |
| $20-50/mo | ElevenLabs Creator (with cloning) |
| $100+/mo | ElevenLabs Pro or Murf Pro |
| High volume | Self-hosted Qwen3-TTS |
```

---

### Step 3: Translate Brand to Voice

Convert brand attributes into voice parameters.

```
## Brand-to-Voice Translation

### Voice Attributes

| Brand Trait | Voice Translation |
|-------------|-------------------|
| Professional | Lower pitch, measured pace, clear articulation |
| Friendly | Mid-pitch, warm tone, slight smile quality |
| Authoritative | Deep, resonant, slower pace, confident pauses |
| Energetic | Higher pitch variation, faster pace, dynamic range |
| Trustworthy | Steady, consistent, neutral accent, clear |
| Innovative | Modern quality, subtle processing, distinctive |
| Warm | Rich mid-tones, soft consonants, unhurried |
| Premium | Controlled, polished, slight reverb/space |

### Voice Parameter Guide

**Pitch Range**:
- Low: Authority, seriousness, gravitas
- Mid: Versatility, approachability
- High: Energy, youth, friendliness

**Pace**:
- Slow: Premium, thoughtful, serious content
- Medium: Most content, versatile
- Fast: Energetic, urgent, young audience

**Accent**:
- Neutral: Universal appeal, no specific region
- Regional: Authenticity for specific markets
- International: European/British for sophistication (to US ears)
```

---

### Step 4: Design by Description (ElevenLabs)

ElevenLabs allows voice design via text description.

```
## Voice Design Prompts

### Template
"A [gender] voice in their [age range], with a [accent] accent.
The voice is [tone qualities] with [delivery characteristics].
[Additional characteristics or limitations]."

### Examples

**Corporate Explainer**:
"A male voice in his late 30s, with a neutral American accent.
The voice is warm and professional with clear articulation and
measured pacing. Sounds like a trusted advisor, not a salesman."

**E-learning Instructor**:
"A female voice in her early 40s, with a slight British accent.
The voice is encouraging and patient with a natural, conversational
delivery. Sounds like a supportive teacher who makes complex
topics accessible."

**Tech Product Demo**:
"A young male voice in his late 20s, with a West Coast American accent.
The voice is confident and energetic with a modern, casual delivery.
Sounds knowledgeable but not condescending, like explaining to a
friend who's also into tech."

**Luxury Brand**:
"A female voice in her 30s, with a subtle French accent.
The voice is sophisticated and understated with elegant pacing
and restrained emotion. Sounds exclusive but welcoming, never rushed."

### Tips for Better Results
- Be specific about age (not just "young" but "late 20s")
- Describe the feeling, not just mechanics
- Reference the context/listener relationship
- Iterate: try 3-5 variations, pick the best
```

---

### Step 5: Multi-Voice Casting

When content requires multiple speakers.

```
## Voice Casting for Multi-Speaker Content

### Dialogue Principles

**Contrast**:
- Different pitches (one higher, one lower)
- Different timbres (one warm, one bright)
- Different energies (one measured, one dynamic)

**Cohesion**:
- Similar quality level
- Compatible accents
- Both feel "from the same world"

### Example Cast

**Corporate Training Video (3 voices)**:

| Role | Voice Type | Platform Choice |
|------|-----------|-----------------|
| Narrator | Authoritative female, 40s | ElevenLabs "Charlotte" |
| Employee A | Friendly male, 30s | ElevenLabs "Daniel" |
| Employee B | Energetic female, 20s | ElevenLabs "Elli" |

**Podcast-Style Explainer (2 voices)**:

| Role | Voice Type | Characteristics |
|------|-----------|-----------------|
| Host | Warm male, mid-30s | Conversational, asks questions |
| Expert | Authoritative female, 40s | Knowledgeable, explains |

### Casting Checklist

□ Voices are clearly distinguishable by ear
□ Voices complement (not clash)
□ Power dynamic appropriate for content
□ All voices pass the "would I trust this person?" test
□ Consistent quality/processing across all voices
```

---

### Step 6: Voice Consistency Management

Maintaining the same voice across projects.

```
## Voice Consistency System

### Documentation

Create a Voice ID Card for each brand voice:

```markdown
## Voice ID: [Brand Name] Primary

**Platform**: ElevenLabs
**Voice ID/Name**: [voice identifier]
**Created**: [date]

### Specifications
- Base voice: [name or description]
- Stability: 0.7 (or setting used)
- Clarity: 0.8 (or setting used)
- Style exaggeration: 0 (or setting used)

### Usage Guidelines
- Primary use: [main content types]
- Never use for: [inappropriate contexts]
- Pair with: [complementary voices]

### Reference Sample
[Link to audio sample]
[Link to key content using this voice]

### Settings History
- v1.0 (date): Initial settings
- v1.1 (date): Adjusted clarity for better consonants
```

### Quality Control

□ Sample new content against reference
□ Check for drift if using cloned voice
□ Verify processing/effects are consistent
□ Test on multiple playback devices
□ Get external ear check periodically
```

## Examples

### Example 1: SaaS Product Demo Voice

**Context**: Choosing an AI voice for product demo videos.

**Input**:
> Help me choose an AI voice for our SaaS product demos. Brand is professional but friendly, audience is B2B decision makers (30-50 years old), and we produce 4-5 videos per month.

**Output**:

## Voice Selection: SaaS Demo Videos

### Requirements Analysis
- **Brand**: Professional + friendly (approachable authority)
- **Audience**: B2B decision makers, 30-50
- **Volume**: 4-5 videos/month (~30-60 min total)
- **Implicit needs**: Trustworthy, clear, not salesy

### Platform Recommendation: ElevenLabs Creator ($22/mo)

**Why**:
- Quality matches professional B2B expectations
- Volume fits within plan limits
- Professional voice library
- Room to clone founder voice later if desired

### Voice Selection

**Primary Voice**: Rachel (ElevenLabs)
- Female, American, mid-30s sound
- Professional warmth, clear articulation
- Works for both feature demos and testimonial reads
- Doesn't sound "AI" to most ears

**Alternative**: Josh (ElevenLabs)
- Male, American, early 40s sound
- Authority without stuffiness
- Good for technical deep-dives

### Settings

```
Voice: Rachel
Stability: 0.75 (natural variation)
Clarity + Similarity: 0.80 (prioritize clarity)
Style: 0 (neutral, professional)
```

### Sample Script Test

Before committing, test with representative content:

"DataFlow integrates with your existing tools in minutes,
not months. Here's how: Simply connect your Salesforce instance
using our secure OAuth flow, and we'll automatically map your
custom fields. No IT tickets required."

→ Listen for: Natural flow, clear tech terms, appropriate pace

---

### Example 2: Multi-Language Brand Voice

**Context**: Expanding content to multiple markets with consistent voice.

**Input**:
> We need to create content in English, French, and Spanish with a consistent brand voice. Same "person" across all languages. Budget is flexible for the right solution.

**Output**:

## Multi-Language Voice Strategy

### Challenge
Maintain consistent brand "character" across languages—not just translation, but the same perceived person speaking.

### Recommended Platform: ElevenLabs Pro ($99/mo)

**Why ElevenLabs for multilingual**:
- Same voice can speak 29+ languages natively
- Preserves tone and character across languages
- Better than separate native voices for brand consistency
- Dubbing feature maintains lip-sync

### Implementation Approach

**Option 1: Design Voice, Use Across Languages**

1. Create perfect English voice using Voice Design
2. Use that exact voice for French and Spanish
3. ElevenLabs handles accent authentically per language

**Voice Design Prompt**:
"A warm, confident voice in the early 30s. Gender-neutral leaning
slightly feminine. Clear, professional articulation with a modern,
international quality. Should sound equally at home in New York,
Paris, or Madrid. Approachable expert energy."

**Option 2: Clone Founder/Spokesperson**

If you have a real person who embodies the brand:
1. Clone their voice (30+ min sample)
2. Use clone for all languages
3. Their "essence" transfers, accent adapts

### Language-Specific Notes

| Language | Consideration |
|----------|--------------|
| English | Base voice, primary development |
| French | Slightly slower pace, French pronunciation patterns |
| Spanish | Choose Castilian vs Latin American variant |

### Quality Control

- Native speaker review for each language
- Check for unnatural pronunciation of brand terms
- Verify numbers and dates sound correct
- Test technical vocabulary

## Checklists & Templates

### Voice Selection Checklist

```
## Before Selecting

□ Brand personality documented
□ Audience defined
□ Content types listed
□ Volume estimated
□ Budget confirmed
□ Languages needed identified

## Selection Process

□ Shortlist 3-5 candidate voices
□ Test with real script content
□ Listen on target devices (phone, laptop)
□ Get team feedback
□ Test for ear fatigue (listen to 5+ minutes)
□ Verify consistency across sample content

## After Selection

□ Document voice settings
□ Save reference samples
□ Create usage guidelines
□ Test with production content
□ Plan for localization if needed
```

---

### Voice Platform Comparison

```
## Quick Reference

| Need | Best Choice |
|------|-------------|
| Premium quality | ElevenLabs |
| Zero cost | Qwen3-TTS (self-hosted) |
| Voice cloning | ElevenLabs Creator+ |
| 29+ languages | ElevenLabs |
| Video workflow | Murf.ai |
| OpenAI ecosystem | OpenAI TTS |
| Real-time | Qwen3-TTS or ElevenLabs Flash |
| Data privacy | Qwen3-TTS (self-hosted) |
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

- ElevenLabs Documentation - Voice design and cloning guides
- Qwen3-TTS vs ElevenLabs Comparison - ByteIota
- Best Text-to-Speech AI 2026 - AIML API review
- Murf AI Review - Voice design workflows

## Related Skills

- [voice-localization](../voice-localization/) - Same voice across languages
- [voiceover-direction](../voiceover-direction/) - Working with human talent
- [sonic-branding](../sonic-branding/) - Brand audio identity
- [video-testimonial](../video-testimonial/) - Customer video content

---

## Skill Metadata (Internal Use)

```yaml
name: voice-design
category: audio
subcategory: voice
version: 1.0
author: MKTG Skills
source_expert: ElevenLabs, Qwen3-TTS
source_work: Platform Documentation, Industry Comparisons
difficulty: intermediate
estimated_value: $200-1,000 per voice design project
tags: [ai-voice, tts, elevenlabs, voice-synthesis, brand-voice]
created: 2026-01-26
updated: 2026-01-26
```
