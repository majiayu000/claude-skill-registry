---
name: cover-letter-generator
description: Generate professional cover letter from career data. Use when creating a narrative-style introduction that tells your career story with personality and passion.
allowed-tools: Read, Write, Glob
context: fork
---

# Cover Letter Generator Skill

## Purpose
Create a **compelling cover letter** that tells your career story in a narrative format, showing personality, passion, and the "why" behind your technical achievements.

## Task
Generate `COVER_LETTER.md` by synthesizing:
- `my_thoughts_*.md` files (learnings, reflections, growth)
- `what_i_did_*.md` files (accomplishments context)
- `performance_*.md` files (impact validation)
- `basic_info.md` (personal background)

## Instructions

### Step 1: Read Source Data

Read all available files:
- All `my_thoughts_*.md` files (all years) - This is your primary source
- All `what_i_did_*.md` files (context for achievements)
- All `performance_*.md` files (metrics to back up claims)
- `basic_info.md` (personal background, education, career)

### Step 2: Understand the Narrative Arc

A great cover letter tells a story with:
- **Hook**: What drives you? Why software engineering?
- **Journey**: How did you grow? Key turning points?
- **Impact**: What have you accomplished? Why does it matter?
- **Vision**: Where are you headed? What excites you?

### Step 3: Extract Story Elements

From `my_thoughts_*.md` files, identify:
- **Pivotal learnings**: Moments that changed how you think
- **Challenges overcome**: Hard problems you solved, how you grew
- **Passions and interests**: What excites you about technology
- **Growth trajectory**: How you evolved from year to year
- **Values**: What matters to you in your work

From `what_i_did_*.md` and `performance_*.md`:
- **Concrete examples**: Stories that illustrate your points
- **Impact metrics**: Numbers that validate your achievements

### Step 4: Structure the Cover Letter

#### Opening (1-2 paragraphs)
- **Hook**: Start with something engaging
  - A pivotal moment in your career
  - What drives your passion for technology
  - A unique perspective or insight
- **Current state**: Who you are today

**Example**:
> I still remember the moment I deployed my first real-time streaming system to production. Watching 10,000+ CCTV streams flow through the architecture I'd designed, processing at 99.9% uptime—that's when I truly understood the power of distributed systems. Over the past 6 years, I've channeled that excitement into building scalable AI/ML infrastructure that serves millions of users, always driven by the question: "How can we make this better?"

#### Body (3-5 paragraphs)
Tell your story chronologically or thematically:

**Option A - Chronological**:
- Early career: How you started, initial learnings
- Growth phase: Key projects, expanding expertise
- Current focus: What you're working on now, where you excel

**Option B - Thematic**:
- Technical depth: Your expertise evolution
- Impact focus: How you create business value
- Leadership growth: How you've grown beyond code

Each paragraph should:
- Start with a theme or insight
- Provide concrete example from your career data
- Include metrics when relevant
- Show personal growth or learning

**Example paragraph**:
> My approach to backend engineering evolved significantly through 2023-2024. What started as a routine database migration became a masterclass in distributed systems design. Leading the PostgreSQL-to-MongoDB transition, I learned that performance optimization isn't just about choosing the right tool—it's about understanding data access patterns, query characteristics, and system bottlenecks. The 40% latency reduction we achieved validated months of careful analysis and iterative refinement. More importantly, this project taught me to balance technical excellence with pragmatic delivery, a lesson I've applied to every project since.

#### Closing (1-2 paragraphs)
- **Current focus**: What you're passionate about now
- **Future vision**: Where you want to go, what you want to build
- **Value proposition**: What makes you unique
- **Call to action**: How to learn more / get in touch

**Example**:
> Today, I'm focused on pushing the boundaries of AI/ML infrastructure at OGQ, where I'm working on systems that make intelligent capabilities accessible and reliable at scale. I'm particularly excited about the intersection of LLMs and production systems—building the infrastructure that makes AI useful, not just impressive.
>
> If you're interested in learning more about my work or discussing opportunities, check out my detailed [RESUME](./RESUME.md) or explore my [career data repository](./). I'm always open to conversations about distributed systems, AI infrastructure, or the art of building reliable software at scale.

### Step 5: Apply Storytelling Principles

**Voice and Tone**:
- First person ("I", not "He/She")
- Conversational but professional
- Show personality and passion
- Be authentic, not generic

**Show, Don't Tell**:
- ❌ "I'm a hard worker and team player"
- ✅ "I mentored 3 junior engineers through their first distributed systems project, meeting weekly to pair-program and review architecture decisions"

**Use Specific Details**:
- ❌ "I improved system performance"
- ✅ "I reduced query latency by 40% through careful data modeling and index optimization"

**Connect the Dots**:
- Link learnings to outcomes
- Show how challenges led to growth
- Demonstrate continuous improvement

### Step 6: Language Considerations

**For Korean**:
- Professional but warm tone (존댓말 appropriate level)
- Balance humility with confidence
- Technical terms can stay in English
- Natural conversational flow

**For English**:
- Active voice, strong verbs
- Concise but not terse
- Professional yet personable

### Step 7: Quality Checks

Before writing output:
- ✅ Tells a coherent story (not just list of facts)
- ✅ Shows personality and passion
- ✅ Includes concrete examples with metrics
- ✅ Demonstrates growth over time
- ✅ Connects learnings from my_thoughts files to impact
- ✅ Authentic voice (not generic template)
- ✅ Proper grammar and flow
- ✅ Appropriate length (800-1200 words for general, 400-600 for specific)

### Step 8: Write Output

Write to `COVER_LETTER.md` in the base directory.

## Example Structure

```markdown
# Cover Letter

## About Me

[Opening hook - what drives you, pivotal moment, passion]

[Current state - who you are today]

## My Journey

[Story paragraph 1 - early career or key theme]

[Story paragraph 2 - growth phase or technical depth]

[Story paragraph 3 - current focus or leadership evolution]

[Optional: Story paragraph 4 - additional theme]

## What Drives Me

[Your passions, values, what excites you about technology]

## Looking Forward

[Current focus, future vision, where you want to go]

[Value proposition - what makes you unique]

## Let's Connect

[How to learn more, get in touch]

---

**Quick Links:**
- 📄 [Detailed Resume](./RESUME.md)
- 💼 [GitHub Profile](https://github.com/ufxpri)
- 📊 [Career Data](./2024/)
```

## Customization Options

You may receive instructions like:
- "For a startup role" → Emphasize scrappiness, versatility, 0-to-1 building
- "For a senior/staff position" → Focus on technical leadership, architecture decisions
- "For a specific company" → Tailor to company values, tech stack, culture
- "Keep it concise" → Shorter version (400-600 words)
- "More technical depth" → Include more architecture details, design decisions

Adapt accordingly using your LLM judgment.

## General vs. Targeted Cover Letters

**General (GitHub profile)**:
- Broad overview of career and passions
- Multiple themes and achievements
- Open-ended vision
- 800-1200 words

**Targeted (specific application)**:
- Focus on relevant experience for that role
- Address company's needs/challenges
- Explain why you're interested in *that* company
- 400-600 words
- Modify opening and closing to be company-specific

## Success Criteria
- Reads like a compelling story, not a resume in prose
- Shows personality and authentic voice
- Backed by concrete examples and metrics
- Demonstrates growth and learning over time
- Appropriate tone (professional but personable)
- Proper structure and flow
- Correct grammar and formatting
