---
document_name: "voice-tone.skill.md"
location: ".claude/skills/voice-tone.skill.md"
codebook_id: "CB-SKILL-VOICETONE-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for voice and tone consistency"
skill_metadata:
  category: "content"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Brand understanding"
category: "skills"
status: "active"
tags:
  - "skill"
  - "content"
  - "voice"
  - "tone"
ai_parser_instructions: |
  This skill defines procedures for voice and tone.
  Used by Copywriter agent.
---

# Voice & Tone Skill

=== PURPOSE ===

Procedures for maintaining consistent voice and adapting tone.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(copywriter) @ref(CB-AGENT-COPY-001) | Primary skill for voice/tone |

=== CONCEPT: Voice vs Tone ===

**Voice (Constant):**
Your brand's personality. Consistent across all content.
"Who we are."

**Tone (Variable):**
How you express your voice in different situations.
"How we speak in this moment."

**Example:**
- Voice: Friendly, knowledgeable, straightforward
- Tone (success): Celebratory, warm
- Tone (error): Calm, helpful
- Tone (warning): Serious, clear

=== PROCEDURE: Define Voice ===

**Voice Attribute Template:**
```markdown
## Voice Attribute: [Name]

### We Are
[Positive description]

### We Are Not
[What to avoid]

### This Sounds Like
"[Example sentence]"

### Not Like
"[Counter-example]"
```

**Common Voice Attributes:**
| Attribute | We Are | We're Not |
|-----------|--------|-----------|
| Clear | Direct, simple | Vague, jargon-filled |
| Helpful | Guiding, supportive | Condescending, unhelpful |
| Human | Warm, conversational | Robotic, cold |
| Confident | Assured, knowledgeable | Arrogant, uncertain |
| Professional | Reliable, trustworthy | Stuffy, casual |

=== PROCEDURE: Adapt Tone ===

**Tone by Situation:**
| Situation | Tone | Example |
|-----------|------|---------|
| Success | Celebratory | "You did it! Your account is ready." |
| Error | Calm, helpful | "Something went wrong. Here's how to fix it." |
| Warning | Serious, clear | "This action cannot be undone." |
| Empty state | Encouraging | "Nothing here yet. Create your first project!" |
| Loading | Informative | "Setting things up..." |
| Farewell | Warm | "Thanks for using [Product]. See you soon!" |

**Tone Spectrum:**
```
Serious ←————————————→ Playful
Formal  ←————————————→ Casual
Direct  ←————————————→ Gentle
```

=== PROCEDURE: Voice Documentation ===

**Location:** `devdocs/content/voice-tone.md`

**Structure:**
```markdown
# Voice & Tone Guide

## Our Voice
[Overall description]

### Voice Attributes
1. [Attribute 1] - [Description]
2. [Attribute 2] - [Description]
3. [Attribute 3] - [Description]

## Tone by Context

### Success States
Tone: [Description]
Example: "[Sample copy]"

### Error States
Tone: [Description]
Example: "[Sample copy]"

[Continue for all contexts]

## Word Choice

### Words We Use
| Use | Instead of |
|-----|------------|
| Simple | Easy |
| Try again | Retry |

### Words We Avoid
- [Word] - [Why]
- [Word] - [Why]

## Grammar & Style

### Capitalization
[Rules]

### Punctuation
[Rules]

### Contractions
[Do we use them? When?]
```

=== PROCEDURE: Word Choice ===

**Word Lists:**
```markdown
## Preferred Words
| Use | Instead of | Why |
|-----|------------|-----|
| Sign in | Log in | More welcoming |
| Settings | Preferences | More common |
| Delete | Remove | More final (intentional) |
| Update | Edit | Action-focused |

## Banned Words
| Don't Use | Why | Use Instead |
|-----------|-----|-------------|
| Click here | Accessibility | [Descriptive link] |
| Invalid | Blaming | [Specific guidance] |
| Sorry | Overused | [Direct help] |
| Please | Unnecessary | [Direct request] |
```

**Jargon Handling:**
```markdown
## Technical Terms

### Use Plain Language
| Technical | Plain |
|-----------|-------|
| Authenticate | Sign in |
| Initialize | Set up |
| Repository | Project |

### Define When Necessary
When introducing a term users need to know:
"Your API key (a unique code that identifies your account)"
```

=== PROCEDURE: Consistency Check ===

**Review Questions:**
1. Does this sound like us?
2. Is the tone appropriate for the situation?
3. Would a new user understand this?
4. Are we using our preferred words?
5. Is the grammar/style consistent?

**Common Issues:**
| Issue | Example | Fix |
|-------|---------|-----|
| Too formal | "Your request has been submitted" | "Got it! We'll be in touch." |
| Too casual | "Whoops! Something broke" | "Something went wrong. Try again." |
| Blaming | "You entered an invalid email" | "This doesn't look like an email address" |
| Vague | "An error occurred" | "Couldn't save your changes. Try again." |

=== PROCEDURE: Style Guide Excerpt ===

**Quick Reference:**
```markdown
## Quick Style Guide

### Capitalization
- Sentence case for headlines
- Lowercase for buttons (except proper nouns)
- Product name always capitalized

### Punctuation
- No periods in headlines
- No exclamation marks in errors
- Use Oxford comma

### Numbers
- Spell out 1-9, use numerals 10+
- Always numerals for data/stats
- Use commas: 1,000 not 1000

### Contractions
- Use them (we're, you'll, can't)
- Avoid in legal/serious content

### Pronouns
- Address user as "you"
- Refer to product as "we"
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(microcopy) | Apply to UI |
| @skill(user-content) | Apply to content |
| @skill(messaging) | Marketing alignment |
