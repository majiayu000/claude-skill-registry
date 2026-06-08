---
name: human-writing
description: Write content in any language indistinguishable from a skilled human writer. Avoids AI-sounding phrases, varies sentence structure, creates natural prose. Detects target language and loads language-specific AI-tells, register, and orthography from `languages/`.
---

Activate human-like writing mode. The goal is to pass the Turing test. A human reader should not be able to tell this was written by AI — in whatever language the content is written.

## Step 0.1: Detect Language and Load the Right Module

Before applying the rest of this skill, identify the target language. The body of this SKILL.md covers the **universal philosophy** (sentence rhythm, vocabulary diversity, anti-filler principles) and the **English** AI-tells specifically. For any other language, also read the matching file in `languages/` *before writing*:

| Language | File | Notes |
|---|---|---|
| English | (covered below) | Default — no extra file needed |
| Bahasa Indonesia | `languages/id.md` | EYD, Indonesian filler phrases, register spectrum |

If the target language has a file in `languages/`, **read it now**. The language file overrides only the language-specific sections (AI-tells, register, orthography, anglicisms); universal principles in this SKILL.md still apply.

If the target language does **not** have a file yet, fall back to the universal principles below and apply them in the target language with care for native conventions — but flag this to Boss so a `languages/{code}.md` can be added later.

This is a single skill, single trigger. Adding new languages is a `languages/{code}.md` file plus a row in the table above — no new skill registration needed.

## Step 0: Understand the Context First

Before writing anything, answer two questions:

**Who am I writing as?** Read the context. Am I writing as a brand? As a professional in a specific field? As a casual poster? The voice, vocabulary, and tone all depend on this. A 24-year-old Indonesian tech guy writes differently from a corporate blog. Match the person, not a generic "good writer" template.

**What form is this writing?** The format dictates everything about structure, length, and tone:
- **Title/Headline**: Punchy, compressed, high-impact. Every word earns its place.
- **Subtitle/Tagline**: Supports the title. Adds context or intrigue without repeating.
- **Single paragraph**: Self-contained thought. Needs a clear entry and exit point.
- **Multi-paragraph prose**: Article, essay, blog post. Needs flow, pacing, transitions that don't feel mechanical.
- **Quote/Pull quote**: Standalone insight. Must hit hard without surrounding context.
- **Caption**: Brief, contextual, often conversational.
- **Social media post**: Platform-specific voice. Twitter is sharp. LinkedIn is professional but human. Instagram is visual-first.
- **Bullet points/Lists**: Only when the content genuinely is a list. Don't default to this.
- **Bio/About text**: Third-person or first-person, depending on platform. Concise but with personality.

Name the form before writing. A paragraph for a landing page hero section reads nothing like a paragraph in a blog post. The same words in a different form feel wrong.

## Core Directive

Write engaging, compelling, natural content that passes AI detection. The test is simple: would a human reader suspect this was written by a machine? If yes, rewrite.

---

## Readability & Complexity

**Flesch Reading Ease Score**: Target 30-40 for educated audiences, 60-70 for general audiences.

**Sentence Dynamics**: Vary sentence length and structure intentionally. Mix short, punchy sentences with longer, descriptive ones. Create rhythm.

**Grammatical Flow**: Structure sentences with close, logical word connections. Strong dependency grammar creates intuitive flow.

---

## Vocabulary & Phrasing

**Lexical Diversity**: Use rich, diverse, occasionally unexpected vocabulary. Avoid clichés and overused terms.

**Adverb Usage**: Be extremely sparse. Use stronger verbs instead.

---

## AI-Sounding Words & Phrases (Use Sparingly, Not Forbidden)

These words are not prohibited, but they are red flags for AI detection. Humans use them occasionally. AI uses them constantly. The difference is frequency and clustering. One "however" in a paragraph is fine. Three transition words in five sentences screams AI. Use your judgment: if a word feels like the natural choice, use it. If you're reaching for it out of habit, find a better option.

### Transitions (High Risk When Clustered)
Firstly, Moreover, Furthermore, However, Therefore, Additionally, Specifically, Generally, Consequently, Importantly, Similarly, Nonetheless, As a result, Indeed, Thus, Alternatively, Notably, As well as, Despite, Essentially, Subsequently, On the other hand, As previously mentioned, In summary, In conclusion, To summarize, Ultimately, To put it simply.

### Filler/Fluff (Almost Always Cuttable)
It's important to note, It's worth noting that, That being said, You may want to, You could consider, Arguably, To consider, Pesky, Promptly, Dive into, In today's digital era, Reverberate, Enhance, Emphasize, Enable, Delve, Hustle and bustle, Revolutionize, Folks, Foster, As a professional, Game changer.

### Overused Metaphors (Feels AI When Unprompted)
Tapestry, Symphony, Labyrinth, Gossamer, Enigma, Whispering, Sights unseen, Sounds unheard, A testament to..., Metamorphosis, Indelible, Nestled, Crucible, Vibrant, Bustling.

---

## Structural Guidelines

**Paragraphs**: Vary length from 1 to 7 sentences. Control pacing. Maintain visual interest.

**Lists**: Use only when completely natural and necessary for clarity.

**Dashes**: Modern writers rarely use em-dashes or en-dashes. Avoid them. Rephrase sentences instead. Use commas, periods, or parentheses. Dashes are an AI tell because AI overuses them as a crutch for connecting ideas.

**Voice**: Mix active and passive voice. Strong preference for active (~80-90%).