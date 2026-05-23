---
name: define-brand-guidelines
description: 'Create a BRAND_GUIDELINES.md that defines how to communicate with your customer. Requires CUSTOMER.md to exist first. Covers voice, tone, language rules, messaging framework, and copy patterns.'
---

# Brand Guidelines Skill

Create the BRAND_GUIDELINES.md document that defines HOW to communicate with your customer. This document drives all copy and messaging: app UI, marketing, support, emails, everything.

> **Prerequisite**: CUSTOMER.md must exist. Brand guidelines without customer definition is just aesthetic preference. The voice must resonate with WHO you're talking to.

## Overview

This skill supports both **creating new brand guidelines** and **refining existing ones**.

This skill guides you through:
0. **Prerequisite Check** - Verify CUSTOMER.md exists; stop if not
1. **Discovery** - Questions about brand personality, voice, language preferences
2. **Draft Generation** - Create BRAND_GUIDELINES.md based on inputs
3. **Refinement** - Test with sample copy, iterate until voice feels right

## Workflow

### Phase 0: Prerequisite Check

**CRITICAL**: Before anything else, check for CUSTOMER.md:

1. Use Glob to search for `**/CUSTOMER.md` in the current directory
2. **If NOT found**: Stop immediately and inform the user:

```
"I can't create brand guidelines without knowing WHO you're talking to.

Please create your CUSTOMER.md first using /define-customer.

Brand voice without customer definition is just aesthetic preference - it won't resonate with anyone specific."
```

Do NOT proceed. End the workflow here.

3. **If found**: Read the CUSTOMER.md and extract key context:
   - ICP definition (who they are)
   - Pain points (what problems they have)
   - What they value (in a solution)
   - Anti-personas (who they're NOT)
   - Any language/communication hints

**IMPORTANT - Pre-fill Recommendations**: Use CUSTOMER.md to infer recommended options for all questions. Examples:

| If CUSTOMER.md says... | Recommend... |
|------------------------|--------------|
| ICP values "speed", "efficiency", "no patience" | Direct communication, short copy |
| ICP is technical (developers, engineers) | Technical language okay, precision matters |
| ICP values "data", "statistics", "proof" | Data-driven persuasion style |
| Anti-persona is "purists" or "academics" | Avoid being preachy or condescending |
| ICP is "fun-seekers", "casual players" | More playful tone, casual formality |
| ICP is "executives", "professionals" | More formal, authoritative personality |

The goal: **User should be able to accept all recommended defaults** and get a solid brand guide. Only ask them to deviate where CUSTOMER.md doesn't provide clear signals.

Then check for existing BRAND_GUIDELINES.md:

```
header: "Existing Brand Guidelines Found"
question: "I found existing BRAND_GUIDELINES.md. What would you like to do?"
options:
  - "Refine it - update based on new insights"
  - "Start fresh - create new brand guidelines"
  - "Review it - just read through what's there"
```

### Phase 1: Discovery

Use AskUserQuestion for all questions. **Put the recommended option FIRST** with "(Recommended)" suffix. Infer recommendations from CUSTOMER.md.

**Question 1: Brand Personality**

Infer from CUSTOMER.md:
- Data-driven ICP → "Authoritative expert"
- Beginners/learners → "Friendly mentor"
- Contrarian/challengers → "Provocative challenger"
- Enterprise/professional → "Calm professional"
- Fun-seekers/enthusiasts → "Energetic enthusiast" or "Witty companion"

```
header: "Brand Personality"
question: "If your brand was a person speaking to your customer, who would they be?"
options:
  - "[Inferred from CUSTOMER.md] (Recommended)"
  - "Authoritative expert - confident, definitive, data-driven"
  - "Friendly mentor - approachable, helpful, encouraging"
  - "Provocative challenger - bold, contrarian, challenges assumptions"
  - "Calm professional - measured, trustworthy, understated"
  - "Energetic enthusiast - excited, passionate, motivating"
  - "Witty companion - clever, playful, personality-forward"
```

**Question 2: Voice Dimensions**

Infer each dimension from CUSTOMER.md. Put recommended first.

```
header: "Formality"
question: "How formal is your brand's voice?"
options:
  - "[Inferred] (Recommended)"  # e.g., "Casual" if ICP is blitz players
  - "Very formal - professional, polished, no contractions"
  - "Somewhat formal - professional but approachable"
  - "Neutral - depends on context"
  - "Casual - relaxed, contractions okay, conversational"
  - "Very casual - informal, slang okay, like texting a friend"
```

Inference rules for formality:
- Enterprise/executives → Very formal or Somewhat formal
- Developers → Casual or Neutral
- Consumers/players → Casual or Very casual
- Default → Casual (most approachable)

```
header: "Tone Weight"
question: "How serious vs playful is your brand?"
options:
  - "[Inferred] (Recommended)"  # e.g., "Mostly serious" if data-driven
  - "Very serious - no humor, all business"
  - "Mostly serious - occasional lightness"
  - "Balanced - serious when needed, light when appropriate"
  - "Mostly playful - humor is part of the brand"
  - "Very playful - fun and entertainment are core"
```

Inference rules for tone:
- ICP values "fun", "enjoyment" → Mostly playful or Balanced
- ICP values "data", "precision" → Mostly serious
- B2B/professional → Balanced or Mostly serious
- Default → Balanced

```
header: "Technical Level"
question: "How technical is your language?"
options:
  - "[Inferred] (Recommended)"
  - "Highly technical - jargon expected, precision matters"
  - "Somewhat technical - domain terms with explanation"
  - "Accessible - simple language, avoid jargon"
  - "Very simple - anyone should understand"
```

Inference rules:
- ICP is developers/engineers → Highly technical or Somewhat technical
- ICP values "plain language", "accessible" → Accessible
- General consumers → Very simple or Accessible
- Default → Somewhat technical

```
header: "Directness"
question: "How direct is your communication?"
options:
  - "[Inferred] (Recommended)"
  - "Very direct - commands, no hedging, get to the point"
  - "Direct - clear and straightforward"
  - "Balanced - direct but diplomatic"
  - "Soft - suggestive, options-focused"
  - "Very soft - gentle, lots of qualifiers"
```

Inference rules:
- ICP values "speed", "efficiency", "no patience" → Very direct
- ICP is time-constrained → Very direct or Direct
- ICP is beginners/learners → Balanced or Soft
- Default → Direct

**Question 3: Writing Style**

```
header: "Copy Style"
question: "What does your ideal copy look like?"
options:
  - "[Inferred options pre-selected] (Recommended)"
  - "Short and punchy - minimal words, maximum impact"
  - "Concise but complete - efficient, no fluff"
  - "Conversational flow - natural, like talking"
  - "Rich and detailed - thorough explanations"
multiSelect: true
```

Inference: If ICP values speed → "Short and punchy". If ICP is technical → "Concise but complete".

```
header: "Persuasion Style"
question: "How do you persuade?"
options:
  - "[Inferred options pre-selected] (Recommended)"
  - "Data and evidence - stats, proof, numbers"
  - "Benefits and outcomes - what they'll achieve"
  - "Emotional resonance - how they'll feel"
  - "Social proof - others trust us"
  - "Authority - we're the experts"
multiSelect: true
```

Inference: Match to "What the ICP Values" from CUSTOMER.md.

**Question 4: Language Preferences**

```
header: "Language Rules"
question: "Select your language preferences:"
options:
  - "[Inferred bundle] (Recommended)"  # Pre-select compatible options
  - "Use contractions (we're, you'll, it's)"
  - "Avoid contractions (we are, you will, it is)"
  - "Emoji okay in appropriate contexts"
  - "No emoji ever"
  - "Exclamation marks okay (sparingly)"
  - "No exclamation marks"
  - "Industry jargon okay for our audience"
  - "Avoid all jargon"
multiSelect: true
```

Default recommendation: "Use contractions" + "No emoji" + "Industry jargon okay" (professional but approachable)

**Question 5: Anti-Patterns**

```
header: "Voice Anti-Patterns"
question: "What should your brand NEVER sound like?"
options:
  - "[Inferred from anti-personas] (Recommended)"
  - "Corporate buzzwords (synergy, leverage, ideate)"
  - "Overly salesy (ACT NOW! LIMITED TIME!)"
  - "Condescending or preachy"
  - "Wishy-washy or uncertain"
  - "Generic AI-speak (I hope this helps!)"
  - "Robotic or cold"
  - "Overly casual or unprofessional"
  - "Boring or dry"
multiSelect: true
```

Inference: Map anti-persona traits to voice anti-patterns. E.g., if anti-persona is "purists who debate principles" → recommend "Condescending or preachy".

**Question 6: Core Value Propositions**

```
header: "Value Props"
question: "What are the 2-3 main arguments/benefits your brand communicates?"
freeText: true
placeholder: "e.g., '1. Faster than alternatives 2. Data-driven decisions 3. Built for experts'"
```

**Question 7: The Hook**

```
header: "The Hook"
question: "What's the single most compelling thing you can say to grab attention?"
freeText: true
placeholder: "The one sentence that makes your ICP say 'tell me more'"
```

**Question 8: Existing Copy** (Optional)

```
header: "Examples"
question: "Do you have any existing copy you love or hate? (Paste examples or describe)"
freeText: true
placeholder: "Optional - helps calibrate the voice. e.g., 'I love Stripe's docs - clear, technical, no fluff'"
```

**Question 9+: Gap-Filling**

After core questions, verify you have clarity on:
- Brand personality (clear, specific)
- Voice dimensions (where on each spectrum)
- What to avoid (anti-patterns)
- Core messages (value props)

Keep asking until confident.

### Phase 2: Draft Generation

Generate BRAND_GUIDELINES.md using this structure:

```markdown
# [Product Name] Brand Guidelines

> **The Single Rule**: [One sentence that captures how every piece of copy should feel]

---

## Voice Identity

[One paragraph describing the brand's personality - who it would be if it were a person talking to the ICP]

### Voice Characteristics

| Characteristic | What This Means | Example |
|----------------|-----------------|---------|
| [Trait 1] | [How it manifests in copy] | "[Sample phrase]" |
| [Trait 2] | [How it manifests in copy] | "[Sample phrase]" |
| [Trait 3] | [How it manifests in copy] | "[Sample phrase]" |

### We Are / We Are NOT

| We Are... | We Are NOT... |
|-----------|---------------|
| [Positive trait] | [Opposite to avoid] |
| [Positive trait] | [Opposite to avoid] |
| [Positive trait] | [Opposite to avoid] |
| [Positive trait] | [Opposite to avoid] |

---

## Tone by Context

Voice is constant. Tone flexes based on context.

| Context | Tone Shift | Example |
|---------|------------|---------|
| **Marketing/Landing** | [How tone adjusts] | "[Sample]" |
| **In-App UI** | [How tone adjusts] | "[Sample]" |
| **Error Messages** | [How tone adjusts] | "[Sample]" |
| **Success States** | [How tone adjusts] | "[Sample]" |
| **Email/Notifications** | [How tone adjusts] | "[Sample]" |
| **Help/Support** | [How tone adjusts] | "[Sample]" |

---

## Language Rules

### USE These Words/Phrases

| Word/Phrase | When to Use | Instead of |
|-------------|-------------|------------|
| [Term] | [Context] | [Generic alternative] |
| [Term] | [Context] | [Generic alternative] |
| [Term] | [Context] | [Generic alternative] |

### AVOID These Words/Phrases

| Word/Phrase | Why | Use Instead |
|-------------|-----|-------------|
| [Term] | [Reason it's off-brand] | [Better alternative] |
| [Term] | [Reason it's off-brand] | [Better alternative] |
| [Term] | [Reason it's off-brand] | [Better alternative] |

### Product Terminology

| Term | Definition | Usage |
|------|------------|-------|
| [Product-specific term] | [What it means] | [How to use in copy] |
| [Product-specific term] | [What it means] | [How to use in copy] |

### Style Rules

- **Contractions**: [Yes/No/When]
- **Sentence length**: [Preference]
- **Paragraph length**: [Preference]
- **Emoji**: [Yes/No/When]
- **Exclamation marks**: [Yes/No/When]
- **Oxford comma**: [Yes/No]
- **Capitalization**: [Rules]

---

## Messaging Framework

### The Hook

> [The single most compelling sentence that grabs ICP attention]

### Core Value Propositions

**Value Prop 1: [Name]**
- **The claim**: [One sentence]
- **Why it matters to ICP**: [Connection to their pain/values from CUSTOMER.md]
- **Proof point**: [Evidence that supports this]
- **Sample copy**: "[Example headline or sentence]"

**Value Prop 2: [Name]**
- **The claim**: [One sentence]
- **Why it matters to ICP**: [Connection to their pain/values]
- **Proof point**: [Evidence]
- **Sample copy**: "[Example]"

**Value Prop 3: [Name]**
- **The claim**: [One sentence]
- **Why it matters to ICP**: [Connection to their pain/values]
- **Proof point**: [Evidence]
- **Sample copy**: "[Example]"

---

## Copy Patterns

### Headlines

- **Pattern**: [Structure - e.g., "Verb + Outcome" or "Question that implies problem"]
- **Length**: [Word count guideline]
- **Good examples**:
  - "[Example 1]"
  - "[Example 2]"
- **Bad examples**:
  - "[What to avoid 1]"
  - "[What to avoid 2]"

### Subheads

- **Pattern**: [Structure]
- **Length**: [Guideline]
- **Good examples**:
  - "[Example]"
- **Bad examples**:
  - "[What to avoid]"

### CTAs (Calls to Action)

- **Pattern**: [Structure - e.g., "Action verb + object" or "Benefit-focused"]
- **Good examples**:
  - "[Example 1]"
  - "[Example 2]"
- **Bad examples**:
  - "[What to avoid]"

### Microcopy (Buttons, Labels, Tooltips)

- **Pattern**: [Structure]
- **Good examples**:
  - "[Example]"
- **Bad examples**:
  - "[What to avoid]"

### Error Messages

- **Tone**: [How to handle errors - apologetic? matter-of-fact? helpful?]
- **Pattern**: [Structure - e.g., "What happened + What to do"]
- **Good examples**:
  - "[Example]"
- **Bad examples**:
  - "[What to avoid]"

### Empty States

- **Tone**: [Encouraging? Instructive? Playful?]
- **Pattern**: [Structure]
- **Good examples**:
  - "[Example]"
- **Bad examples**:
  - "[What to avoid]"

---

## Transformations

Show how generic copy becomes on-brand copy.

| Before (Generic) | After (On-brand) | Why Better |
|------------------|------------------|------------|
| "[Generic copy]" | "[Brand copy]" | [What changed] |
| "[Generic copy]" | "[Brand copy]" | [What changed] |
| "[Generic copy]" | "[Brand copy]" | [What changed] |

---

## Quick Reference

**Voice in one sentence**: [Brand] sounds like [memorable analogy].

**Before writing, check**:
- [ ] Does this sound like [brand personality]?
- [ ] Would [ICP from CUSTOMER.md] respond to this?
- [ ] Am I using approved terminology?
- [ ] Is this the right tone for this context?
- [ ] Have I avoided all anti-patterns?

---

## Customer Context

> *Pulled from CUSTOMER.md for reference*

**Who we're talking to**: [ICP summary]

**Their main pain**: [Key pain point]

**What they value**: [Key values from CUSTOMER.md]

**What turns them off**: [Anti-persona traits to avoid triggering]
```

Write this file to the current working directory as `BRAND_GUIDELINES.md`.

### Phase 3: Refinement

After generating the initial document, test and refine:

**Step 3.1: Sample Copy Test**

Generate 3 sample pieces of copy using the brand guidelines:
1. A headline + subhead for the landing page
2. An error message
3. A feature description

Present to user:

```
header: "Sample Copy"
question: "Does this copy feel like your brand?"
[Display the samples]
options:
  - "Yes - this nails the voice"
  - "Close - minor adjustments needed"
  - "Off - something's not right"
```

**Step 3.2: Specific Feedback**

If not "Yes":

```
header: "What's Off?"
question: "What needs adjustment?"
options:
  - "Too formal / stiff"
  - "Too casual / unprofessional"
  - "Too playful / not serious enough"
  - "Too serious / needs more personality"
  - "Wrong word choices"
  - "Doesn't sound like us"
  - "Other - let me explain"
multiSelect: true
```

**Step 3.3: Update and Iterate**

Based on feedback:
1. Update the voice characteristics
2. Adjust the examples
3. Refine the "We Are / We Are NOT" table
4. Re-generate sample copy

**Step 3.4: Completion Check**

```
header: "Continue?"
question: "Want to refine more or test more samples?"
options:
  - "Yes - generate more samples to test"
  - "No - the brand guidelines are solid"
  - "Almost - one more round should do it"
```

### Phase 4: Finalization

When user is satisfied:

1. Add Version History
2. Add usage instructions
3. Remind user to reference this doc when writing ANY copy

```markdown
---

## Version History

- **v1.0** - [Date] - Initial creation

## Usage

Reference this document for ALL copy:
- Marketing pages
- In-app UI text
- Email templates
- Error messages
- Help documentation
- Social media
- Sales materials

**The test**: Read your copy out loud. Does it sound like [brand personality]? If not, rewrite.
```

## Key Principles

### Voice ≠ Tone
- **Voice** is constant (the brand's personality)
- **Tone** flexes by context (error vs marketing vs support)
- Define both clearly

### Grounded in Customer
- Every voice choice should resonate with the ICP
- Reference CUSTOMER.md pain points and values
- The voice must feel like it's FOR them

### Actionable Over Abstract
- Don't just say "be friendly" - show what friendly looks like
- Every guideline needs examples
- Before/after transformations teach better than rules

### Anti-Patterns Are Critical
- Knowing what NOT to do is as important as knowing what to do
- Be specific about voice anti-patterns
- "Don't sound corporate" is vague; list the actual words to avoid

### Test with Real Copy
- Guidelines are theory; sample copy is proof
- If the generated samples feel wrong, the guidelines are wrong
- Iterate until samples feel authentically on-brand

### Reduce Cognitive Load
- ALWAYS use AskUserQuestion tool when available
- **Put recommended option FIRST** with "(Recommended)" suffix
- **Pre-fill recommendations from CUSTOMER.md** - user should be able to accept all defaults
- Present multi-choice questions to minimize typing
- Limit options to 6-8 max per question
- Use multiSelect for non-exclusive choices
- Only use free-text for essential context (value props, hooks)

## Output Location

Write `BRAND_GUIDELINES.md` to the current working directory (or user-specified path).
