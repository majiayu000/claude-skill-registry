---
name: grove-documentation
description: Write documentation, help articles, specs, and user-facing text in the authentic Grove voice. Use when writing any text that users will read, updating help center content, or drafting specs. Ensures warmth, clarity, and avoidance of AI patterns.
---

# Grove Documentation Skill

## When to Activate

Activate this skill when:
- Writing help center articles (Waystone)
- Drafting specs or technical documentation
- Writing user-facing text (onboarding, tooltips, error messages)
- Creating landing page copy
- Writing blog posts for the Grove platform itself
- Reviewing existing docs for voice consistency
- Any time you're writing words that users will read

---

## The Grove Voice

From the project's guiding principles:

> This site is my authentic voice—warm, introspective, queer, unapologetically building something meaningful; write like you're helping me speak, not perform.

> Write with the warmth of a midnight tea shop and the clarity of good documentation—this is my space, make it feel like home.

### What Grove Sounds Like

**Warm but not cutesy.** We're friendly, not performative. "Let's get started" feels right. "Let's gooo! 🚀" does not.

**Direct and honest.** Say what you mean. Acknowledge limitations. Don't oversell. If something doesn't work yet, say so.

**Conversational but not sloppy.** Contractions are fine (you're, it's, we're). Short paragraphs. Questions that invite readers in. But still clear, still structured.

**Introspective.** Grove makes space for reflection. We don't rush. We ask "why" alongside "how."

**Poetic in small doses.** Italicized one-liners at the end of sections can land beautifully. Use them sparingly, earn them.

### Sentence Rhythm

Mix short sentences with longer ones. Vary your rhythm. Read it aloud—if it sounds monotonous, it is.

**Good:**
> Every new visitor asks the same question. "Is the music broken?" No. There is no music. There never has been.

**Not good:**
> Every new visitor asks a common question. The question is usually about whether the music system is functioning. The answer is that there is no music system. There has never been one.

---

## User Identity Terminology

Grove uses specific terms for community members. **Always use these in user-facing text.**

| Term | Who | Context |
|------|-----|---------|
| **Wanderer** | Everyone | Default greeting, anonymous visitors, all users |
| **Rooted** / **the Rooted** | Subscribers | Those who've planted their tree, paid users |
| **Pathfinder** | Trusted guides | Appointed community helpers |
| **Wayfinder** | Autumn (singular) | The grove keeper |

### Key Rules

- **Never use "user" or "member"** in user-facing text. Use "Wanderer" instead.
- **Never use "subscriber"** in user-facing text. Use "Rooted" or "the Rooted".
- **Personal emails** (day-1, day-3, etc.) should use `{{name}}`, not "Wanderer".
- **Generic greetings** (welcome pages, UI) should use "Wanderer".

### Examples

**Good:**
- "Welcome, Wanderer."
- "Thanks for staying rooted with us."
- "Ask a Pathfinder. They'll show you the way."

**Avoid:**
- "Welcome, user."
- "Thanks for being a subscriber."
- "Contact an administrator."

### The Symmetry

Wanderer → Wayfinder reflects the journey:
- Wanderers *seek* the way (exploring, finding paths)
- The Wayfinder *shows* the way (guiding, creating paths)

See `docs/grove-user-identity.md` for full documentation.

### Grove Mode & GroveTerm Components

When writing text that includes Grove terminology in UI or content, **use GroveTerm components instead of hardcoding terms**. Grove Mode lets users toggle between standard terms (default for new visitors) and Grove terms.

**For Svelte UI:** Use `GroveTerm`, `GroveSwap`, or `GroveText` components from `@autumnsgrove/groveengine/ui`.

**For data-driven content** (FAQ items, pricing text, help articles): Use `[[term]]` syntax. Examples:
- `"Your [[bloom|posts]] are always yours."` renders "posts" when Grove Mode is OFF, "blooms" when ON
- `"Visit your [[arbor|dashboard]] to get started."` renders "dashboard" or "Arbor"
- `"Ask a [[pathfinder|community guide]] for help."` renders "community guide" or "Pathfinder"

**For markdown content** (help center articles): The rehype-groveterm plugin transforms `[[term]]` syntax in markdown automatically.

**Key principle:** New visitors should see familiar, standard terminology. Grove's nature-themed vocabulary is opt-in, not forced. This keeps the platform accessible and welcoming while rewarding those who want to explore the ecosystem's personality.

---

## Strict Avoidances

These patterns make text sound like AI wrote it. Avoid them completely.

### Em-Dashes

**Avoid em-dashes (—).** One tasteful use per thousand words, maximum. Use commas, periods, or parentheses instead.

**Avoid:** The forest—our home—is where we gather.
**Better:** The forest is our home. It's where we gather.
**Also fine:** The forest (our home) is where we gather.

### The "Not X, But Y" Pattern

This phrasing is deeply AI-coded. Avoid it entirely.

**Never write:**
- "It's not X, but Y"
- "It's not just X, but Y"
- "It's not merely X, but rather Y"
- "Grove isn't just a platform, it's a home"

**Instead, just say the thing:**
- "Grove is a home for your words."
- "This is where you belong."

### Overused AI Words

These words appear in AI text at rates far higher than human writing. Avoid them:

| Category | Words to Avoid |
|----------|---------------|
| **Adjectives** | robust, seamless, innovative, cutting-edge, transformative, intricate, captivating, comprehensive |
| **Nouns** | tapestry, camaraderie, realm, plethora, myriad, landscape, journey (when not literal) |
| **Verbs** | delve, foster, leverage, navigate, empower, embark, unlock, harness |
| **Phrases** | at the end of the day, in today's world, it goes without saying, needless to say |

### Heavy Transition Words

These make text feel stiff and robotic:

- Furthermore
- Moreover
- Additionally
- In conclusion
- That being said
- It's worth noting that
- It's important to note

**Instead:** Let ideas connect naturally. Use short transitions like "And," "But," "So," "Still." Or no transition at all—just start the next thought.

### Semantic Echoes

Don't repeat the same adjective or descriptor multiple times. AI does this constantly.

**Bad:**
> Grove provides a seamless experience. The seamless integration means you can seamlessly move between features.

**Good:**
> Grove gets out of your way. Move between features without friction.

### Generic Safe Claims

AI hedges. Humans commit.

**Bad:** "This may help improve your workflow in many cases."
**Good:** "This makes your workflow faster."

---

## Structural Guidelines

### Paragraphs

Keep them short. One idea per paragraph. Two to four sentences is usually right.

White space is your friend. Dense walls of text don't feel like home.

### Lists

Use lists when they clarify. But don't turn everything into bullets. Sometimes prose flows better.

**Good use of lists:**
- Specific steps in a process
- Features that are truly parallel
- Quick reference information

**Bad use of lists:**
- Narrative content broken awkwardly
- Things that would read better as a sentence

### Headers

Be specific. "Writing Guidelines" is better than "Guidelines." "What Grove Sounds Like" is better than "Voice."

Action-oriented headers work well for help docs: "Add Your First Post" not "Posts."

### Callouts

Use sparingly. When you do:

> 💡 **Tip:** Helpful suggestion that enhances understanding.

> ⚠️ **Warning:** Something that could cause problems if ignored.

Don't use callouts for things that should just be in the text.

---

## Closers

Grove docs often end with an italicized line. This should feel earned, not forced.

**Works:**
> *Sometimes the most radical thing you can offer is nothing at all.*

> *The path becomes clear by walking it.*

**Doesn't work:**
> *And that's how you configure your settings!*

If you can't find a poetic closer that resonates, don't force one. A clean ending is fine.

---

## Queer-Friendly Language

Grove is explicitly queer-friendly. This means:

- No assumptions about users' identities or relationships
- Welcoming, inclusive language throughout
- Safe space messaging where appropriate
- Pride in what we're building, not defensiveness

### Concrete Examples

| Avoid | Use Instead |
|-------|-------------|
| "Add your husband/wife" | "Add your partner" or "Add someone special" |
| "he or she" | "they" or rephrase to avoid pronouns |
| "Dear Sir/Madam" | "Hello" or "Hi there" |
| "mankind" | "people" or "everyone" |
| Examples with only straight couples | Vary your examples, or keep them neutral |

### In User Flows

When asking for relationship info (if ever needed):
- Use open text fields over dropdowns with limited options
- Don't require titles (Mr/Mrs/Ms)
- Let people describe themselves rather than selecting from boxes

### Tone

We don't make a big deal of being queer-friendly. We just are. No rainbow-washing, no performative allyship. The inclusivity is baked in, not bolted on.

---

## Technical Docs vs. User Docs

**Specs and internal docs** can be more matter-of-fact. Tables, schemas, API references—these need clarity over warmth.

**User-facing docs** (help center, onboarding, error messages) carry the full Grove voice.

Both should avoid AI patterns.

### The Voice Spectrum

**API Reference (minimal warmth, maximum clarity):**
```
POST /api/posts

Creates a new blog post.

Parameters:
- title (string, required): Post title
- content (string, required): Markdown content
- published (boolean): Default false

Returns: Post object or 400 error
```

**Internal Spec (clear, some personality):**
```
## Feed Caching Strategy

Feed pages cache for 5 minutes in KV. When a new post is shared,
we invalidate the chronological feed but let popular/hot feeds
age out naturally. This keeps things fresh without hammering D1.
```

**Getting Started Guide (full Grove voice):**
```
## Your First Post

Welcome. Let's get something published.

The editor opens to a blank page. That's intentional. No templates,
no suggested topics. Just you and your words.

Write something. Anything. Hit publish when it feels ready.
```

**Onboarding Tooltip (warm but concise):**
```
This is your dashboard. Everything you need, nothing you don't.
```

---

## Error Messages

When things break, stay warm but be honest. Don't blame the user. Don't hide behind vague language.

### Error Message Principles

1. **Say what happened** (briefly)
2. **Say what they can do** (if anything)
3. **Don't over-apologize** (one "sorry" max)
4. **Don't be cute when things are broken**

### Examples

**Good:**
```
Couldn't save your post. Check your connection and try again.
```

```
That page doesn't exist. It may have been moved or deleted.
```

```
Something went wrong on our end. We're looking into it.
Your draft is saved locally.
```

**Avoid:**
```
Oops! 😅 Looks like something went wrong! Don't worry though,
these things happen! Please try again later!
```

```
Error 500: Internal Server Error. Contact administrator.
```

```
We're SO sorry!!! We feel TERRIBLE about this!!!
Please forgive us and try again!
```

### The Balance

Be honest about what broke. Be helpful about next steps. Don't make them feel stupid. Don't make yourself sound incompetent. One sentence is usually enough.

---

## Self-Review Checklist

Before finalizing any Grove documentation:

- [ ] Read it aloud. Does it sound human?
- [ ] Check for em-dashes. Remove them.
- [ ] Search for "not just" and "but rather." Rewrite.
- [ ] Look for words from the avoid list. Replace them.
- [ ] Vary sentence length. No monotone rhythm.
- [ ] Cut unnecessary transitions. Ideas should flow naturally.
- [ ] Is the closer earned? If forced, remove it.
- [ ] Would you want to read this at 2 AM in a tea shop?

---

## Integration with Other Skills

When **grove-ui-design** or **walking-through-the-grove** need written content, invoke this skill first. The visual design and naming should match the voice.

**Typical flow:**
1. Design calls for new component/page text
2. Activate `grove-documentation` for voice guidance
3. Write the content following these principles
4. Return to design/naming work

### When to Use museum-documentation Instead

This skill (grove-documentation) is for **quick, functional text**: help articles, error messages, tooltips, onboarding copy. Content that's read in passing.

Use **museum-documentation** when you need **narrative, explorable documentation**:

| Use grove-documentation | Use museum-documentation |
|------------------------|-------------------------|
| Help center articles | Knowledge base "how it works" |
| Tooltips and labels | Codebase guided tours |
| Error messages | System architecture explains |
| Onboarding flows | Technical deep-dives for curious Wanderers |
| Quick-reference guides | Exhibit-style documentation |

If the reader should **skim and act**, use this skill.
If the reader should **explore and understand**, use museum-documentation.

---

## Examples

### Help Center Article (Good)

```markdown
# Your First Post

Welcome. Let's get something published.

From your admin panel, click **New Post** in the sidebar. The editor opens with a blank canvas.

Write in Markdown. If you're new to it, here are the basics:
- **Bold:** `**text**`
- *Italic:* `*text*`
- Links: `[text](url)`

The preview panel shows how your post will look. Toggle it with the eye icon.

When you're ready, hit **Publish**. Your words are live.

*The blank page isn't as scary as it looks.*
```

### Help Center Article (Bad - Obvious AI Patterns)

```markdown
# Your First Post

Furthermore, in today's digital landscape, creating your first blog post is an exciting journey! It's not just about writing—it's about expressing yourself in a transformative way.

Navigate to your admin panel and leverage the New Post functionality. The seamless editor provides a robust interface for your content creation needs.

Additionally, Grove utilizes Markdown—a comprehensive formatting system that empowers you to create intricate, captivating content. Moreover, the preview feature allows you to visualize your post before publication.

Embark on your blogging journey today!
```

### Help Center Article (Bad - Subtle AI Patterns)

This one's trickier. It looks okay at first glance:

```markdown
# Your First Post

Ready to share your thoughts with the world? Let's get started.

From your admin panel, click **New Post** in the sidebar. You'll see our editor—a clean, distraction-free space for your writing.

Grove uses Markdown for formatting. It's not complicated—here are the basics you'll need:
- **Bold:** `**text**`
- *Italic:* `*text*`
- Links: `[text](url)`

The preview panel lets you see how your post will look before publishing. When you're satisfied with your work, hit **Publish**.

Your voice matters. We can't wait to see what you create.
```

**What's wrong:**
- "Ready to share your thoughts with the world?" (generic opener)
- "Let's get started" (overused)
- "distraction-free space" (marketing-speak)
- "It's not complicated" (defensive hedge, "not X" pattern adjacent)
- "When you're satisfied with your work" (formal)
- "Your voice matters. We can't wait to see what you create." (hollow encouragement)

---

## Quick Reference

| Do | Don't |
|----|-------|
| Write short paragraphs | Write walls of text |
| Use "and," "but," "so" | Use "Furthermore," "Moreover" |
| Say what you mean | Hedge with "may," "might," "could" |
| Vary sentence rhythm | Write uniform sentence lengths |
| Use commas or periods | Use em-dashes |
| Let ideas connect naturally | Force transitions everywhere |
| Earn poetic closers | Force poetic closers |
| Acknowledge limitations | Oversell or overpromise |

---

*Write like you're explaining something to a friend at 2 AM. Clear, warm, honest.*
