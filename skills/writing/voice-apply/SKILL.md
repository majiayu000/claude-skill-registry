---
name: voice-apply
description: Applies a voice profile to transform content. Use when user asks to write in a specific voice, match a tone, apply a style, or transform content to sound like a particular voice profile.
version: 1.0.0
---

# Voice Apply Skill

## Purpose

Transform content to match a specified voice profile. This skill loads voice profiles and applies their characteristics (tone, vocabulary, structure, perspective) to new or existing content.

## When This Skill Applies

- User asks to "write in X voice" or "use Y tone"
- User wants to "make this sound more [casual/formal/technical/etc.]"
- User provides content and asks to transform its style
- User references a voice profile by name
- User wants content to match a specific audience or context

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Write this in technical voice" | Apply technical-authority profile |
| "Make it more casual" | Apply casual-conversational or calibrate toward casual |
| "This needs to sound executive" | Apply executive-brief profile |
| "Explain like I'm a beginner" | Apply friendly-explainer profile |
| "Use the [profile-name] voice" | Load and apply named profile |
| "Transform this to match [example]" | Analyze example, apply derived voice |

## Voice Profile Locations

Skill checks these locations (in order):
1. Project: `.aiwg/voices/`
2. User: `~/.config/aiwg/voices/`
3. Built-in: `voice-framework/voices/templates/`

## Built-in Voice Profiles

| Profile | Description | Best For |
|---------|-------------|----------|
| `technical-authority` | Direct, precise, confident | Docs, architecture, engineering |
| `friendly-explainer` | Approachable, encouraging | Tutorials, onboarding, education |
| `executive-brief` | Concise, outcome-focused | Business cases, stakeholder comms |
| `casual-conversational` | Relaxed, personal | Blog posts, social, newsletters |

## Application Process

### 1. Load Voice Profile

```python
# Load from YAML
profile = load_voice_profile("technical-authority")
```

### 2. Analyze Source Content (if transforming)

- Current tone characteristics
- Vocabulary patterns
- Structure patterns
- Gap analysis vs target voice

### 3. Apply Voice Characteristics

**Tone Calibration**:
- Adjust formality level (word choice, contractions)
- Calibrate confidence (hedging vs assertion)
- Set warmth (clinical vs personable)
- Tune energy (measured vs enthusiastic)

**Vocabulary Transformation**:
- Replace words per `prefer`/`avoid` guidance
- Introduce domain terminology naturally
- Weave in signature phrases where appropriate

**Structure Adjustment**:
- Modify sentence length distribution
- Adjust paragraph breaks
- Add/remove lists, examples, analogies as specified

**Perspective Shift**:
- Adjust narrative person (I, we, you, they)
- Calibrate opinion expression
- Set reader relationship tone

### 4. Verify Authenticity Markers

Ensure output includes profile's authenticity characteristics:
- Acknowledges uncertainty (if specified)
- Shows tradeoffs (if specified)
- Uses specific numbers (if specified)
- References constraints (if specified)

## Usage Examples

### Apply Named Voice

```
User: "Write release notes in technical-authority voice"

Process:
1. Load technical-authority.yaml
2. Generate release notes with:
   - Precise technical terminology
   - Specific version numbers
   - Direct, confident statements
   - Tradeoff acknowledgments where relevant
```

### Transform Existing Content

```
User: "Make this documentation more friendly for beginners"

Input: "The API endpoint accepts a JSON payload containing the requisite parameters..."

Process:
1. Load friendly-explainer.yaml
2. Analyze: formal, technical, passive
3. Transform to: casual, accessible, active

Output: "To use this endpoint, send it some JSON with the info it needs..."
```

### Calibrate Voice

```
User: "This is too formal, dial it back 30%"

Process:
1. Identify current formality (~0.8)
2. Calculate target (0.8 - 0.3 = 0.5)
3. Adjust vocabulary and structure for medium formality
```

## Voice Blending

Combine multiple profiles:

```
User: "Write this with 70% technical-authority and 30% friendly-explainer"

Process:
1. Load both profiles
2. Weighted merge:
   - tone.formality: 0.7 * 0.7 + 0.3 * 0.3 = 0.58
   - tone.warmth: 0.7 * 0.3 + 0.3 * 0.8 = 0.45
   - etc.
3. Apply merged profile
```

## Script Reference

### voice_loader.py
Load and validate voice profiles:
```bash
python scripts/voice_loader.py --profile technical-authority
```

### voice_analyzer.py
Analyze content against voice profile:
```bash
python scripts/voice_analyzer.py --content input.md --profile technical-authority
```

## Integration

Works with:
- `/voice-apply` command for explicit invocation
- `/voice-create` command for generating new profiles
- SDLC templates (apply appropriate voice per artifact type)
- Marketing templates (brand voice consistency)

## Output Format

When reporting voice application:

```
Voice Applied: technical-authority

Transformations:
- Formality: 0.4 → 0.7 (increased)
- Confidence: 0.5 → 0.9 (increased)
- Vocabulary: 12 replacements
- Structure: Added 2 examples, removed 1 rhetorical question

Authenticity Check:
✓ Acknowledges tradeoffs
✓ Uses specific numbers
✓ References constraints
```
