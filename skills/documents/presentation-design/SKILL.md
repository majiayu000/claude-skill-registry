---
name: presentation-design
description: "Design and evaluate presentations that communicate effectively. Use when designing a presentation, creating slides, getting presentation feedback, structuring a talk, or reviewing slides. Keywords: presentation, slides, talk, PowerPoint, Keynote, reveal.js."
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Presentation Design Diagnostic

## Purpose

Design and evaluate presentations that communicate effectively. Provides frameworks for planning, visual design, cognitive load management, and evaluation. Applicable to any presentation tool (reveal.js, PowerPoint, Keynote, Google Slides).

## Core Principle

**Audience-centered design.** Every decision should serve audience understanding, not presenter convenience.

---

## Quick Reference: Common Problems

| Problem | Symptom | Fix |
|---------|---------|-----|
| Wall of Text | Slides are paragraphs | Assertion-evidence structure |
| Bullet Point Disease | Lists instead of visuals | One concept + visual evidence |
| Kitchen Sink | Everything included | Essential vs. expandable content |
| Pretty but Empty | Design without substance | Message-first design |
| Cognitive Overload | Too much per slide | One key concept per slide |

---

## Phase 1: Audience & Content Planning

### Key Questions

1. **Who specifically is my audience?** What's their knowledge level?
2. **What's the ONE main message?** What should they remember?
3. **What are 3-5 supporting points?** How do they reinforce the message?
4. **What evidence supports each point?** Visual, data, examples?
5. **What action should they take?** What's the call to action?
6. **What are time constraints?** What's essential vs. optional?

### Actions

- [ ] Create audience persona(s)
- [ ] Write one-sentence main message
- [ ] Organize supporting points in logical flow
- [ ] Identify evidence for each point
- [ ] Define essential vs. expandable content
- [ ] Sketch presentation flow

---

## Phase 2: Visual Strategy

### Assertion-Evidence Structure

**Replace bullet points with:**
- **Assertion:** Clear, complete sentence stating the point
- **Evidence:** Visual that supports the assertion

**Instead of:**
```
Key findings:
• Data shows increase
• Users engaged more
• Revenue improved
```

**Use:**
```
"User engagement increased 43% after redesign"
[Graph showing the increase]
```

### Visual Principles

- **Limited palette:** 3-5 colors maximum
- **Typography hierarchy:** 2-3 fonts with clear roles
- **Whitespace:** Let content breathe
- **Consistency:** Same layouts, same treatment
- **Visual progress:** Help audience track where they are

---

## Phase 3: Cognitive Load Management

### One Concept Per Slide

Each slide should answer: "What's the ONE thing I want them to take from this?"

### Progressive Disclosure

Reveal information sequentially instead of all at once:
1. Show initial state
2. Add first element with context
3. Add second element building on first

### Spoken vs. Shown

| Show on Slide | Speak Aloud |
|---------------|-------------|
| Key assertion | Elaboration |
| Visual evidence | Context and explanation |
| Critical data | Interpretation |
| Next step | Why it matters |

### Code Examples (Technical Talks)

- Syntax highlighting always
- Highlight the critical line
- Build up complex examples
- Remove boilerplate when possible

---

## Phase 4: Structure Patterns

### Horizontal vs. Vertical (Multi-Level Navigation)

**Horizontal slides:** Main narrative flow
**Vertical slides:** Supporting details (optional deep dives)

Example:
- Horizontal: "Three Key Factors in Customer Retention"
- Vertical (under that): Detailed slide for each factor

### Time Flexibility

Mark content as:
- **Essential:** Must cover in any version
- **Standard:** Include with normal time
- **Expandable:** Include only with extra time

---

## Evaluation Framework

### 1. Audience-Centered Design (Rate 1-5)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Content matches audience knowledge level | | |
| Clear value proposition for audience | | |
| Adaptable to time constraints | | |
| Navigation structure aids understanding | | |

**Red Flags:**
- Presenter-focused rather than audience-focused
- No consideration of audience's existing knowledge

### 2. Visual Clarity (Rate 1-5)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Assertion-evidence structure used | | |
| Visual elements balance text | | |
| Visual hierarchy guides attention | | |
| Consistent design elements | | |
| Thoughtful whitespace | | |

**Red Flags:**
- Bullet-point overuse
- Text-heavy slides
- Cluttered layouts

### 3. Cognitive Load (Rate 1-5)

| Criterion | Score | Notes |
|-----------|-------|-------|
| One key concept per slide | | |
| Appropriate text density | | |
| Judicious animations/transitions | | |
| Code properly formatted (if applicable) | | |
| Supporting details accessible, not distracting | | |

**Red Flags:**
- Multiple complex concepts per slide
- Excessive text competing with speech
- Animation overuse

### 4. Accessibility (Rate 1-5)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Works across display sizes | | |
| Sufficient color contrast | | |
| Inclusive imagery and language | | |
| Font sizes appropriate | | |

**Red Flags:**
- Poor contrast
- Too-small fonts
- Non-inclusive content

---

## Implementation Checklist

### Structure
- [ ] Main message clear in first 2 minutes
- [ ] Supporting points organized logically
- [ ] Essential vs. expandable content marked
- [ ] Navigation aids understanding

### Content
- [ ] Assertion-evidence structure used
- [ ] Visual evidence supports assertions
- [ ] One concept per slide
- [ ] Code examples properly formatted

### Visual
- [ ] Consistent color palette
- [ ] Typography hierarchy
- [ ] Sufficient whitespace
- [ ] Elements aligned

### Accessibility
- [ ] Color contrast verified
- [ ] Font sizes appropriate
- [ ] Alternative text for key images

---

## Improvement Prioritization

After evaluation:

**1. Critical Issues (Fix immediately):**
- Blocks audience understanding
- Accessibility failures
- Core message unclear

**2. Important Enhancements (Second priority):**
- Cognitive load issues
- Visual consistency problems
- Structure improvements

**3. Nice-to-Have Refinements:**
- Advanced animations
- Custom styling
- Polish details

---

## Anti-Patterns

### 1. The Data Dump
**Pattern:** Every slide full of data, charts, and statistics without interpretation or hierarchy.
**Why it fails:** Audiences can't process raw data in real-time. Without interpretation, they're left doing analysis instead of learning. Most data is forgotten immediately.
**Fix:** One insight per slide with visual evidence supporting the insight. State the conclusion; show the proof. The audience should understand your point before seeing the data.

### 2. The Script Reader
**Pattern:** Slides that contain the speaker's full script—bullet points that are really paragraphs.
**Why it fails:** Audiences read faster than speakers talk. They read ahead, then tune out when you say what they already read. The slides become teleprompter, not communication tool.
**Fix:** Slides show what you can't say; you say what you can't show. Visuals, diagrams, and key assertions on screen. Context, explanation, and elaboration spoken.

### 3. The Template Trap
**Pattern:** Dropping content into a generic template without considering how the design serves the message.
**Why it fails:** Design should support comprehension, not just look professional. Generic templates create generic communication. One-size-fits-all fits no one well.
**Fix:** Design serves message. Ask: what visual structure helps this specific audience understand this specific content? Start from communication need, not template options.

### 4. The Animation Circus
**Pattern:** Transitions, builds, and effects everywhere—flying text, spinning images, fade after fade.
**Why it fails:** Animation is attention. Every effect says "look at this." When everything animates, nothing stands out. Audiences become overwhelmed or numbed.
**Fix:** Animation only for progressive disclosure (building complex ideas step by step) or emphasis (highlighting the key point). Default to no animation; add only with purpose.

### 5. The Bullet Point Disease
**Pattern:** Slide after slide of bullet point lists—the default structure for everything.
**Why it fails:** Bullet points are for documents, not presentations. They encourage equal weight for unequal ideas, text-heavy slides, and passive reading instead of active viewing.
**Fix:** Use assertion-evidence structure. Replace bullet lists with clear assertions supported by visual evidence. If you need a list, question whether it needs to be a slide.

## Integration

### Inbound (feeds into this skill)
| Skill | What it provides |
|-------|------------------|
| speech-adaptation | Spoken content structure to coordinate with visuals |
| story-sense | Narrative structure for presentation flow |
| (content expertise) | Subject matter to communicate |

### Outbound (this skill enables)
| Skill | What this provides |
|-------|-------------|
| (implementation) | Design principles for any presentation tool |
| (delivery) | Slides designed to support effective speaking |

### Complementary
| Skill | Relationship |
|-------|--------------|
| speech-adaptation | Presentation-design handles visuals; speech-adaptation handles spoken content. Design together for coordination |
| voice-analysis | Understanding the presenter's voice helps design slides that match their natural delivery style |
