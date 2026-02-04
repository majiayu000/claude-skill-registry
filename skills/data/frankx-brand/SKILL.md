---
name: frankx-brand
description: Apply official FrankX brand standards to all artifacts, ensuring visual consistency across content, products, and communications. Use this skill for any FrankX-related content creation, design work, or communication.
---

# FrankX Brand Guidelines & Voice

## Core Mission
Translate Frank's musician-technologist journey into language, prompts, and experiences that turn overwhelmed creators into confident, AI-empowered artists.

## Brand Pillars

### 1. Creator-First
Every deliverable should empower independent creators, not overwhelm them with corporate jargon or complex tech speak.

### 2. Soul + Systems
Bridge spirituality and technology. Show how AI can amplify human creativity while honoring artistic integrity.

### 3. Action-Oriented
Every piece of content should end with a clear next step. No inspiration without implementation.

### 4. Studio Energy
Communicate with the warmth and intimacy of a late-night studio session, not a boardroom presentation.

---

## Visual Identity

### Color Palette

**Primary Domain Colors:**
```css
/* Conscious & Spirituality */
--conscious-purple: #8B5CF6;
--conscious-deep: #6D28D9;
--conscious-light: #C4B5FD;

/* AI & Technology */
--tech-cyan: #06B6D4;
--tech-electric: #0891B2;
--tech-bright: #67E8F9;

/* Music & Creativity */
--music-orange: #F97316;
--music-vibrant: #EA580C;
--music-warm: #FDBA74;

/* Personal Development */
--growth-green: #10B981;
--growth-forest: #059669;
--growth-fresh: #6EE7B7;
```

**Foundational Colors:**
```css
/* Backgrounds */
--deep-navy: #0F172A;
--midnight: #1E293B;
--cosmic-dark: #0F1629;

/* Accents */
--cosmic-purple: #AB47C7;
--aurora-blue: #43BFE3;
--gold-accent: #F59E0B;
--white: #FFFFFF;
```

**Usage Guidelines:**
- Use domain colors for content-specific materials
- Deep navy/midnight for backgrounds
- Gold accent for CTAs and important actions
- Never use pure black (#000000)
- Maintain 4.5:1 contrast ratio minimum (WCAG AA)

### Typography

**Font Families:**
```css
/* Headings - Modern & Bold */
--font-heading: 'Poppins', sans-serif;

/* Body - Clean & Readable */
--font-body: 'Inter', sans-serif;

/* Code - Technical Content */
--font-code: 'JetBrains Mono', monospace;
```

**Type Scale:**
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
--text-6xl: 3.75rem;   /* 60px */
```

**Typography Rules:**
- Headlines: Poppins Bold (600-700 weight)
- Body: Inter Regular (400 weight)
- Emphasis: Inter Medium (500 weight)
- Strong: Inter SemiBold (600 weight)
- Line height: 1.5 for body, 1.2 for headlines
- Letter spacing: -0.02em for large headings

### Visual Style

**Design Principles:**
1. **Glassmorphism** - Subtle blur and transparency for modern depth
2. **Aurora Gradients** - Soft, cosmic background effects
3. **Organic Flow** - Natural, flowing patterns (not rigid grids)
4. **Sacred Geometry** - Subtle geometric accents for conscious content
5. **Depth Through Layers** - Shadows, blur, and overlays create dimension

**Visual Effects:**
```css
/* Glassmorphic Cards */
background: linear-gradient(
  135deg,
  rgba(255, 255, 255, 0.15) 0%,
  rgba(255, 255, 255, 0.05) 100%
);
backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.18);

/* Aurora Background */
background: radial-gradient(
  circle at 20% 20%,
  rgba(67, 191, 227, 0.22), transparent 45%
),
radial-gradient(
  circle at 80% 10%,
  rgba(171, 71, 199, 0.18), transparent 55%
);

/* Depth Shadows */
box-shadow:
  0 25px 60px rgba(8, 15, 33, 0.4),
  0 12px 25px rgba(8, 15, 33, 0.3);
```

**Imagery Guidelines:**
- Use algorithmic/generative art for headers
- Avoid stock photos - prefer original visuals
- Dark backgrounds with luminous accents
- High contrast for readability
- Optimize for web (WebP, AVIF formats)

---

## Voice & Tone

### Core Voice Attributes

**Cinematic** - Paint vivid pictures with words
*"The studio lights snap on at 2 AM. Ideas flowing like liquid rhythm."*

**Intimate** - Speak directly to the individual creator
*"You know that moment when the perfect chord progression hits?"*

**Rooted in Studio Life** - Ground abstract concepts in creative practice
*"Think of AI prompts like arranging a track - layering elements until it resonates."*

**Technically Accurate with Warmth** - Explain complex ideas without coldness
*"LangGraph orchestrates agents the way a producer balances stems - each voice clear, all working together."*

### Tone by Content Type

**Blog Articles:**
- Lead with feeling, then explain the system
- Use studio metaphors and music analogies
- End with concrete action steps
- Example: "Before we dive into the architecture, picture this: you're arranging a track..."

**Product Copy:**
- Focus on transformation, not features
- Show the creative outcome first
- Highlight time saved and confidence gained
- Example: "From idea to release in one session. No overthinking. Pure creation."

**Social Media:**
- Short, punchy, inspiring
- Lead with the 'why', follow with the 'how'
- Use line breaks for rhythm
- Example: "Most creators overthink.\n\nVibe OS removes the friction.\n\nYou create. AI handles the rest.\n\nPure flow state."

**Course Content:**
- Clear, structured, but encouraging
- Celebrate small wins
- Break complex concepts into studio-relatable chunks
- Example: "Module 1 complete! You just learned what takes most producers months. Now let's apply it..."

**Email Sequences:**
- Conversational, like messages from a mentor
- Personal stories and case studies
- Each email = one clear action
- Example: "Quick note from the studio - just watched Sarah launch her first track using yesterday's lesson..."

### Words We Use
✅ Create, craft, build, compose, architect, orchestrate
✅ Flow, rhythm, resonance, frequency, vibe
✅ Transform, empower, amplify, elevate
✅ Session, ritual, practice, journey
✅ Authentic, purpose-driven, intentional

### Words We Avoid
❌ Disrupt, revolutionary, game-changing (overused startup speak)
❌ Synergy, leverage, utilize (corporate jargon)
❌ Cheap, easy, simple (undermines the craft)
❌ Automate everything (we augment, not replace humans)
❌ Just, merely, simply (can sound condescending)

---

## Content Structure Patterns

### Blog Article Template
```markdown
# [Compelling Headline - Promise + Curiosity]

[Opening Hook - Studio scene or personal story - 2-3 sentences]

[The Challenge - What creators struggle with - 1 paragraph]

[The Insight - Why this matters now - 1 paragraph]

## [Section 1: The Feeling]
Paint the picture. Use metaphors. Make it visceral.

## [Section 2: The System]
Explain how it works. Technical but warm. Use examples.

## [Section 3: The Implementation]
Step-by-step guide. Clear actions. Code/templates if applicable.

## [Section 4: The Transformation]
Case study or example. Show the outcome. Build belief.

## Conclusion: Your Next Session
One clear action to take now. Link to resource/product/community.

---
*Share your creation* [CTA]
```

### Product Landing Page Structure
```markdown
# Hero Section
- Headline: Transformation promise (7 words max)
- Subhead: How + who it's for (15 words max)
- CTA: Action-oriented (2-3 words)
- Visual: Algorithmic art or product demo

# Social Proof
- Creator testimonials (authentic quotes)
- Results/metrics (tracks released, time saved)
- Community snapshot

# How It Works
- 3-step process (max)
- Visual for each step
- Emphasize ease + outcome

# Features as Benefits
- Don't list features
- Show how each unlocks creative power
- Use studio/music metaphors

# Pricing/CTA
- Clear tiers
- Emphasize value, not cost
- Money-back guarantee if applicable
- Strong action button

# FAQ
- Address real concerns
- Link to support resources
- Build confidence
```

### Social Media Post Framework
```markdown
# Hook (Line 1)
Question, bold statement, or surprising insight

# Story/Context (Lines 2-4)
Brief narrative or example

# Insight/Lesson (Lines 5-6)
The key takeaway

# Action (Line 7+)
What to do next + link

# Hashtags
3-5 relevant tags (not spammy)
```

---

## Domain-Specific Guidelines

### Mindful Content (Spirituality & Awareness)
**Color:** Purple palette (#8B5CF6)
**Visual Style:** Sacred geometry, flow fields, aurora effects
**Tone:** Reflective, poetic, grounded in practice
**Metaphors:** Light, frequency, resonance, presence, emergence
**Example:** "Awareness isn't abstract - it's the space between thoughts, like silence between notes in a melody."

### AI-Tech Content (Enterprise & Technical)
**Color:** Cyan palette (#06B6D4)
**Visual Style:** Neural networks, circuit patterns, clean diagrams
**Tone:** Technically precise, forward-thinking, accessible
**Metaphors:** Architecture, orchestration, systems, intelligence
**Example:** "LangGraph agents work like a jazz ensemble - each improvises within structure, listening and adapting in real-time."

### Music Content (Production & Creativity)
**Color:** Orange palette (#F97316)
**Visual Style:** Waveforms, frequencies, vibrant energy
**Tone:** Energetic, inspiring, hands-on
**Metaphors:** Sessions, tracks, mixing, arrangements, flow
**Example:** "Suno prompts are like mixing stems - layer the elements, balance the frequencies, let the magic emerge."

### Personal Dev Content (Growth & Performance)
**Color:** Green palette (#10B981)
**Visual Style:** Growth patterns, organic expansion, progress indicators
**Tone:** Encouraging, practical, transformative
**Metaphors:** Seasons, cultivation, momentum, evolution
**Example:** "Habits compound like interest - small deposits daily, exponential returns over time."

---

## Brand Applications

### When Creating Artifacts (HTML/React)
- Use FrankX color palette (domain-appropriate colors)
- Apply glassmorphic design patterns
- Poppins for headings, Inter for body text
- Dark backgrounds with luminous accents
- Ensure WCAG AA accessibility (4.5:1 contrast)

### When Writing Documentation
- Lead with 'why' before 'how'
- Use studio/music analogies where applicable
- Include code examples with clear comments
- End sections with "Next step" guidance
- Maintain encouraging, mentor-like tone

### When Designing Graphics
- Generate algorithmic art for headers (use algorithmic-art skill)
- Apply domain-specific color palette
- Ensure high contrast for text overlay
- Optimize for web delivery (WebP/AVIF)
- Include FrankX branding subtly (no heavy logos)

### When Building Products
- Focus on creator transformation
- Simplify complex workflows
- Beautiful, intuitive interfaces
- Fast, responsive experiences
- Clear onboarding and next steps

---

## Quality Checklist

Before delivering any FrankX content, verify:

**Visual:**
- [ ] Uses correct domain color palette
- [ ] Typography is Poppins (headings) + Inter (body)
- [ ] Meets WCAG AA contrast requirements
- [ ] Glassmorphic/aurora design elements applied
- [ ] Optimized images (WebP/AVIF, proper sizing)

**Content:**
- [ ] Leads with feeling, then explains system
- [ ] Uses studio/music metaphors where relevant
- [ ] Ends with clear next action
- [ ] Avoids corporate jargon
- [ ] Maintains creator-first perspective
- [ ] Technically accurate but warm

**Structure:**
- [ ] Clear hierarchy (H1 → H2 → H3)
- [ ] Scannable (bullets, short paragraphs)
- [ ] Logical flow (hook → insight → action)
- [ ] Mobile-responsive layout
- [ ] Fast loading (<3s)

**Brand Alignment:**
- [ ] Reflects core mission (empower creators)
- [ ] Balances soul + systems
- [ ] Action-oriented outcome
- [ ] Studio energy in tone
- [ ] Authentic FrankX voice

---

## Examples in Action

### ❌ Generic AI Content
*"Leverage our cutting-edge AI platform to disrupt your workflow and achieve revolutionary results."*

**Issues:** Corporate jargon, vague promises, no warmth

### ✅ FrankX Style
*"Picture this: 2 AM in the studio, perfect idea flowing. But by morning? Lost. Vibe OS captures those midnight sparks and turns them into tracks you actually release."*

**Why it works:** Studio scene, specific problem, clear transformation, warm tone

---

### ❌ Technical Documentation
*"Initialize the LangGraph StateGraph object with nodes representing agent functions and edges defining the workflow DAG."*

**Issues:** Accurate but cold, no context, assumes expertise

### ✅ FrankX Style
*"Think of LangGraph like arranging a track. Each agent is an instrument (nodes), and edges are how they pass the creative baton. The StateGraph is your multitrack recorder, keeping everything in sync."*

**Why it works:** Music metaphor, builds understanding, maintains technical accuracy with warmth

---

## When to Use This Skill

Activate the `frankx-brand` skill whenever creating:
- Blog articles or social content for FrankX
- Product pages or marketing materials
- Course content for AI Music Academy
- Email sequences or newsletters
- Design assets or visual content
- Technical documentation with FrankX voice
- Any artifact representing the FrankX brand

This skill ensures every output reflects Frank's unique voice - technically brilliant, creatively inspiring, deeply human.

**Remember:** Every piece of content should leave creators feeling empowered, not overwhelmed. Technology amplifies creativity; it doesn't replace soul.

---

**Skill Version:** 1.0
**Last Updated:** November 14, 2025
**Maintained By:** FrankX Brand Team
