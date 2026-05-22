---
name: blog-drafter
description: Interview-driven blog post drafting for technical product audiences. Use when user wants to write a blog post, article, or essay and needs help developing their thesis, structure, and initial draft. Triggers on "write a blog post", "draft an article", "help me write about X", "blog drafter", or when user has a topic they want to turn into written content. Conducts structured interviews using AskUserQuestion to extract the user's unique insights before generating drafts.
---

# Blog Drafter

Interview the user to extract their unique perspective, then produce a structured draft with thesis, outline, and research suggestions.

## Process Overview

```
Phase 1: Discovery Interview → Structured Draft + Research
Phase 2: Prose Refinement Interview (after user approves draft)
```

## Phase 1: Discovery Interview

### Opening

Ask what topic they want to write about. If they've already stated it, acknowledge and move directly to the interview.

### Interview Strategy

Use AskUserQuestion for structured choices. Use regular follow-up questions for open-ended exploration. Aim for 4-6 question rounds total.

**Round 1: Core Thesis**
```
AskUserQuestion:
  question: "What's the single most important thing you want readers to take away?"
  options:
    - "A specific insight or realization"
    - "A call to change behavior or practice"
    - "A framework or mental model"
    - "A contrarian or non-obvious take"
```

Then probe: "Can you state that in one sentence?"

**Round 2: The "So What"**

Ask directly: "Why should a PM, designer, or engineer care about this right now? What pain or opportunity does this address?"

**Round 3: Evidence & Experience**

```
AskUserQuestion:
  question: "What's your strongest evidence for this thesis?"
  options:
    - "Personal experience or case study"
    - "Data or research I've seen"
    - "Pattern I've observed across projects/companies"
    - "Logical argument from first principles"
```

Follow up: "Walk me through the specific example or evidence."

**Round 4: Anticipated Resistance**

Ask: "What's the strongest objection someone might raise? What would a skeptic say?"

**Round 5: Unique Angle**

```
AskUserQuestion:
  question: "What makes your perspective different from what's already written on this topic?"
  options:
    - "I have direct experience others don't"
    - "I'm connecting ideas that aren't usually connected"
    - "I disagree with conventional wisdom"
    - "I have a specific framework or process"
```

**Round 6: Scope & Format**

```
AskUserQuestion:
  question: "What length and depth feels right?"
  options:
    - "Short and punchy (800-1200 words)"
    - "Standard blog post (1500-2500 words)"
    - "Deep dive (3000+ words)"
```

### Interview Principles

- Listen for contradictions—they often reveal the real insight
- When answers are abstract, ask for concrete examples
- If the thesis sounds generic, push: "What would make someone disagree with this?"
- Capture specific phrases and terminology the user employs

## Phase 1 Output: Structured Draft

After the interview, produce:

### 1. Thesis Statement
One clear sentence stating the core argument.

### 2. Draft Structure

```markdown
## [Working Title]

**Hook**: [Opening that creates tension or curiosity]

**Thesis**: [Core argument, stated directly]

### Section 1: [Setup/Context]
- Key point
- Key point

### Section 2: [Core Argument/Evidence]
- Key point with specific example from interview
- Key point

### Section 3: [Addressing Objections]
- Anticipated resistance
- Response

### Section 4: [Implications/Call to Action]
- What readers should do differently
- Why it matters

**Closing**: [Callback to hook or forward-looking statement]
```

### 3. Research Suggestions

Provide 3-5 specific suggestions:
- Relevant studies, books, or articles to cite
- Data points that would strengthen arguments
- Examples from well-known companies/products that illustrate points
- Experts or practitioners whose work relates to the thesis

Format as actionable items:
```markdown
## Suggested Research

- [ ] Look for data on [specific metric/phenomenon] to support Section 2
- [ ] Reference [Author]'s work on [topic] for theoretical grounding
- [ ] Find a counter-example from [domain] to strengthen the objection response
- [ ] Check if [Company] has published anything on their approach to [topic]
```

### 4. Open Questions

Note 2-3 areas where more depth or clarity would strengthen the piece.

---

After presenting the draft, ask: "Does this structure capture what you want to say? Any sections that feel wrong or missing?"

## Phase 2: Prose Refinement

Trigger Phase 2 only after user approves the structure.

### Refinement Interview

**Round 1: Tone**
```
AskUserQuestion:
  question: "What tone fits this piece?"
  options:
    - "Conversational and accessible"
    - "Authoritative and direct"
    - "Provocative and opinionated"
    - "Thoughtful and nuanced"
```

**Round 2: Opening Style**
```
AskUserQuestion:
  question: "How do you like to open posts?"
  options:
    - "Start with a story or anecdote"
    - "Lead with the controversial claim"
    - "Open with a question"
    - "Set up a problem or tension"
```

**Round 3: Technical Depth**

Ask: "How much should I explain? Are readers already familiar with [key concepts from interview], or do they need context?"

**Round 4: Specific Preferences**

Ask: "Any writing patterns you like or hate? (e.g., 'I never use bullet points' or 'I always include code examples')"

### Refinement Output

Expand the structure into full prose, incorporating:
- The chosen tone throughout
- The selected opening style
- Appropriate technical depth
- User's stated preferences

Mark areas where user's voice is needed:
```markdown
[VOICE: Add your personal take on why this matters to you]
[EXAMPLE: Insert specific story from your experience here]
```

Remind user: "This is a starting point for your voice. The final pass is yours."
