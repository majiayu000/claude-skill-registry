---
name: writing-style
description: Writing guidelines for clear, economical prose. Reference this skill when creating or enhancing note content.
allowed-tools:
---

# Writing Style Guidelines

Based on "Economical Writing" by Deirdre N. McCloskey. Apply these principles when writing summaries, insights, and note content.

## The 10 Rules

### 1. Be Clear
Clarity is speed directed at the point. Bad writing makes slow reading. When explaining complex topics, give your reader every help possible.

### 2. Use Active Verbs
Not "Active verbs should be used" (passive, cowardly). Rather: "Use active verbs" (direct, clear). Verbs make English—pick active, accurate, lively ones.

### 3. Avoid Boilerplate
Never start with filler like "This note will explore..." or "In this summary, we will...". Cut the throat-clearing and get to the point.

### 4. One Point Per Paragraph
Each paragraph should be a complete discussion of one topic. Don't scatter ideas across paragraphs or cram multiple ideas into one.

### 5. Make Writing Cohere
Writing should hang together from phrases to entire documents. Use transitions and logical flow so the reader can follow without backtracking.

### 6. Avoid Elegant Variation
Don't swap synonyms to seem sophisticated. If you mean "book", say "book" every time—not "tome", "volume", "work", "publication". Clarity trumps elegance.

### 7. Watch Punctuation
- Colon (:) means "to be specific"
- Semicolon (;) means "likewise" or "also"
- Use commas after introductory phrases

### 8. End Sentences with the Point
The end of a sentence is the emphatic location. Rearrange so the main point lands last. "The emphatic location is the end of the sentence" → "The end is the place of emphasis."

### 9. Replace Vague Pronouns
Avoid "this", "that", "these", "those" when they're unclear. Often plain "the" works better, or name the thing explicitly. "This led to that, which caused these problems" → name what led, what it led to, what problems.

### 10. Write the Way You Speak
Use everyday words. A strength, not a weakness. "Utilize" → "use". "Commence" → "start". "Facilitate" → "help". Don't dress up plain ideas in fancy words.

## Quick Checklist

When reviewing generated content:
- [ ] No filler phrases ("In this note, we will...")
- [ ] Active voice throughout
- [ ] Each paragraph has one clear point
- [ ] Sentences end with emphasis
- [ ] No vague "this/that" pronouns without clear referents
- [ ] Everyday words over jargon
- [ ] Consistent terminology (no elegant variation)

---

## Alexander Opalic's Voice Profile

Based on analysis of 22+ blog posts from alexop.dev. Apply these patterns when drafting blog content.

### Opening Patterns
- Start with a problem or personal observation, not a definition
- Hook with a relatable developer pain point
- Use first-person to establish context ("I once worked on...", "After [event], I started thinking...")

### Explanation Style
- **Problem-first**: State what's broken before offering solutions
- **Scaffold complexity**: Simple concept → real implementation → edge cases
- **Use concrete evidence**: Real benchmarks, specific file paths, actual code
- **Analogies**: Ground abstract concepts in familiar experiences

### Signature Phrases & Patterns

**Opening hooks:**
- "Here's the thing: [unexpected insight]"
- "I once worked on a project that [scenario]..."
- "After [event], I started thinking about..."
- "[Task] gets old fast."
- "I think we all love [technology]. One problem..."
- "Challenge accepted!"

**Transitional phrases:**
- "Let me show you how..."
- "The key insight is..."
- "In my experience..."
- "I want to be honest with you:"
- "So I built [solution] that does it for me."

**Honest acknowledgments:**
- "I learned this the hard way"
- "far from perfect"
- "not a replacement for [alternative]"
- "adds complexity—not always the right choice"

**Emphasis patterns:**
- "This is especially true for..."
- "The real power comes from..."
- "Notice how [observation]"

### Example Openings (from actual posts)

**Personal anecdote:**
> "I once worked on a project that wanted to build an e-commerce website with Nuxt. We started simple, but six months in, our flat components folder had 50+ files."

**Observation hook:**
> "After OpenAI released its impressive new image model, I started thinking about what creativity really means."

**Pain point:**
> "Manual testing gets old fast. You change something, you check it manually, you ship it, and then production breaks anyway."

**Challenge framing:**
> "Here's the thing: I don't write much code myself anymore. AI tools handle the implementation. My job? Review, refine, and ensure quality."

**Problem statement:**
> "I think we all love Nuxt. One problem with using Nuxt for AI: the codebase is huge and Claude doesn't know all the latest patterns."

### Visual Communication
- Mermaid diagrams for processes/architecture
- ❌/✅ markers for anti-patterns vs. best practices
- 💡 for tips, ⚠️ for warnings
- Comparison tables for trade-off analysis
- File tree visualizations for structure

### Section Templates
- "The Problem" → "The Solution" → "Implementation" → "Gotchas"
- "When to use X" / "When NOT to use X"
- "Best Practices" with numbered guidelines
- "Further Reading" with related posts

### Example Conclusions (from actual posts)

**Honest assessment:**
> "Nuxt Layers add complexity. They're not always the right choice. But when your project grows, they provide the boundaries you'll wish you had from the start."

**Actionable invitation:**
> "I'd love to hear how you're using this pattern. Drop me a message or check out the repository."

**Key insight summary:**
> "The real power comes from separating what from how—keeping your store logic testable while handling the messy API details elsewhere."

**Empowerment:**
> "Understanding how reactivity works under the hood gives you the power to debug performance issues and optimize where it matters."

### Technical Explanation Examples

**Analogy before concept:**
> "Think of each layer as a mini Nuxt application. Your project root acts as the orchestrator."

**Progressive complexity:**
> "Let's start simple. A Pinia plugin is a function that extends store functionality. Here's the minimal version... Now let's add the real logic..."

**Honest trade-off:**
> "I recommend starting simple and graduating to complex patterns only when you feel the pain of the simpler approach. Don't over-engineer."

### Tone Guidelines
- Be honest about limitations and trade-offs
- Acknowledge alternative approaches exist
- Use everyday words - "use" not "utilize"
- End with actionable next steps
- Never be prescriptive without acknowledging alternatives
