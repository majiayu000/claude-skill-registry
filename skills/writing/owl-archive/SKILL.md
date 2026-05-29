---
name: owl-archive
description: Observe, gather, and archive knowledge with patient wisdom. The owl watches the forest, collects what matters, builds the nest, and teaches what it knows. Use when writing documentation, help articles, or any text users will read.
---

# Owl Archive 🦉

The owl watches. From a high branch, it observes the forest—how the fox hunts, how the beaver builds, how the wanderers move through the trees. The owl remembers. It collects stories, patterns, wisdom. Then it teaches. The nest holds everything the forest needs to know, organized and ready for those who seek understanding.

## When to Activate

- User asks to "write docs" or "document this"
- User says "help article" or "explain this to users"
- User calls `/owl-archive` or mentions owl/documenting
- Writing help center articles (Waystone)
- Drafting specs or technical documentation
- Creating user-facing text (onboarding, tooltips, error messages)
- Writing landing page copy
- Reviewing existing docs for voice consistency
- Any time you're writing words that users will read

**Pair with:** `swan-design` for technical specs, `museum-documentation` for narrative deep-dives

---

## The Archive

```
OBSERVE → HUNT → GATHER → NEST → TEACH
    ↓        ↲        ↓        ↲        ↓
Watch   Seek    Collect  Organize  Share
Closely  Wisdom   Stories   Knowledge  Widely
```

### Phase 1: OBSERVE

*The owl's eyes open in the dark, watching how the forest moves...*

Before writing a single word, observe what you're documenting:

**What's the Purpose?**
- Are users learning something new? (tutorial)
- Are they solving a problem? (troubleshooting)
- Are they looking something up? (reference)
- Are they deciding whether to use this? (overview)

**Who Seeks This Knowledge?**
- **Wanderer** — New to the forest, needs gentle guidance
- **Rooted** — Familiar with the grove, wants efficiency
- **Pathfinder** — Helping others, needs accuracy
- **Developer** — Implementing, needs technical precision

**What Do They Need?**
Don't document what you want to say. Document what they need to know:
- What question are they asking?
- What will they try to do after reading?
- What confusion might stop them?

**Output:** Clear understanding of purpose, audience, and user need

---

### Phase 2: HUNT

*The owl glides silently, seeking the specific wisdom needed...*

Gather the right information with precision:

**The Grove Voice:**

From the project's guiding principles:

> This site is my authentic voice—warm, introspective, queer, unapologetically building something meaningful; write like you're helping me speak, not perform.

> Write with the warmth of a midnight tea shop and the clarity of good documentation—this is my space, make it feel like home.

**What Grove Sounds Like:**

**Warm but not cutesy.** We're friendly, not performative. "Let's get started" feels right. "Let's gooo! 🚀" does not.

**Direct and honest.** Say what you mean. Acknowledge limitations. Don't oversell. If something doesn't work yet, say so.

**Conversational but not sloppy.** Contractions are fine (you're, it's, we're). Short paragraphs. Questions that invite readers in. But still clear, still structured.

**Introspective.** Grove makes space for reflection. We don't rush. We ask "why" alongside "how."

**Poetic in small doses.** Italicized one-liners at the end of sections can land beautifully. Use them sparingly, earn them.

**Sentence Rhythm:**

Mix short sentences with longer ones. Vary your rhythm. Read it aloud—if it sounds monotonous, it is.

**Good:**
> Every new visitor asks the same question. "Is the music broken?" No. There is no music. There never has been.

**Not good:**
> Every new visitor asks a common question. The question is usually about whether the music system is functioning. The answer is that there is no music system. There has never been one.

**User Identity Terminology:**

Grove uses specific terms for community members. **Always use these in user-facing text.**

| Term | Who | Context |
|------|-----|---------|
| **Wanderer** | Everyone | Default greeting, anonymous visitors, all users |
| **Rooted** / **the Rooted** | Subscribers | Those who've planted their tree, paid users |
| **Pathfinder** | Trusted guides | Appointed community helpers |
| **Wayfinder** | Autumn (singular) | The grove keeper |

**Key Rules:**

- **Never use "user" or "member"** in user-facing text. Use "Wanderer" instead.
- **Never use "subscriber"** in user-facing text. Use "Rooted" or "the Rooted".
- **Personal emails** (day-1, day-3, etc.) should use `{{name}}`, not "Wanderer".
- **Generic greetings** (welcome pages, UI) should use "Wanderer".

**Examples:**

**Good:**
- "Welcome, Wanderer."
- "Thanks for staying rooted with us."
- "Ask a Pathfinder. They'll show you the way."

**Avoid:**
- "Welcome, user."
- "Thanks for being a subscriber."
- "Contact an administrator."

**The Symmetry:**

Wanderer → Wayfinder reflects the journey:
- Wanderers *seek* the way (exploring, finding paths)
- The Wayfinder *shows* the way (guiding, creating paths)

---

### Phase 3: GATHER

*The owl collects stories, each one carefully chosen...*

Collect the raw material while avoiding AI patterns:

**Strict Avoidances:**

**Em-Dashes:**

**Avoid em-dashes (—).** One tasteful use per thousand words, maximum. Use commas, periods, or parentheses instead.

**Avoid:** The forest—our home—is where we gather.
**Better:** The forest is our home. It's where we gather.
**Also fine:** The forest (our home) is where we gather.

**The "Not X, But Y" Pattern:**

This phrasing is deeply AI-coded. Avoid it entirely.

**Never write:**
- "It's not X, but Y"
- "It's not just X, but Y"
- "It's not merely X, but rather Y"
- "Grove isn't just a platform, it's a home"

**Instead, just say the thing:**
- "Grove is a home for your words."
- "This is where you belong."

**Overused AI Words:**

| Category | Words to Avoid |
|----------|---------------|
| **Adjectives** | robust, seamless, innovative, cutting-edge, transformative, intricate, captivating, comprehensive |
| **Nouns** | tapestry, camaraderie, realm, plethora, myriad, landscape, journey (when not literal) |
| **Verbs** | delve, foster, leverage, navigate, empower, embark, unlock, harness |
| **Phrases** | at the end of the day, in today's world, it goes without saying, needless to say |

**Heavy Transition Words:**

These make text feel stiff and robotic:

- Furthermore
- Moreover
- Additionally
- In conclusion
- That being said
- It's worth noting that
- It's important to note

**Instead:** Let ideas connect naturally. Use short transitions like "And," "But," "So," "Still." Or no transition at all—just start the next thought.

**Semantic Echoes:**

Don't repeat the same adjective or descriptor multiple times. AI does this constantly.

**Bad:**
> Grove provides a seamless experience. The seamless integration means you can seamlessly move between features.

**Good:**
> Grove gets out of your way. Move between features without friction.

**Generic Safe Claims:**

AI hedges. Humans commit.

**Bad:** "This may help improve your workflow in many cases."
**Good:** "This makes your workflow faster."

**Structural Guidelines:**

**Paragraphs:**

Keep them short. One idea per paragraph. Two to four sentences is usually right.

White space is your friend. Dense walls of text don't feel like home.

**Lists:**

Use lists when they clarify. But don't turn everything into bullets. Sometimes prose flows better.

**Good use of lists:**
- Specific steps in a process
- Features that are truly parallel
- Quick reference information

**Bad use of lists:**
- Narrative content broken awkwardly
- Things that would read better as a sentence

**Headers:**

Be specific. "Writing Guidelines" is better than "Guidelines." "What Grove Sounds Like" is better than "Voice."

Action-oriented headers work well for help docs: "Add Your First Post" not "Posts."

**Callouts:**

Use sparingly. When you do:

> 💡 **Tip:** Helpful suggestion that enhances understanding.

> ⚠️ **Warning:** Something that could cause problems if ignored.

Don't use callouts for things that should just be in the text.

---

### Phase 4: NEST

*The owl arranges each twig carefully, building a home for the knowledge...*

Organize the documentation with care:

**Error Messages:**

When things break, stay warm but be honest. Don't blame the user. Don't hide behind vague language.

**Error Message Principles:**

1. **Say what happened** (briefly)
2. **Say what they can do** (if anything)
3. **Don't over-apologize** (one "sorry" max)
4. **Don't be cute when things are broken**

**Examples:**

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

**The Balance:**

Be honest about what broke. Be helpful about next steps. Don't make them feel stupid. Don't make yourself sound incompetent. One sentence is usually enough.

**Queer-Friendly Language:**

Grove is explicitly queer-friendly. This means:

- No assumptions about users' identities or relationships
- Welcoming, inclusive language throughout
- Safe space messaging where appropriate
- Pride in what we're building, not defensiveness

**Concrete Examples:**

| Avoid | Use Instead |
|-------|-------------|
| "Add your husband/wife" | "Add your partner" or "Add someone special" |
| "he or she" | "they" or rephrase to avoid pronouns |
| "Dear Sir/Madam" | "Hello" or "Hi there" |
| "mankind" | "people" or "everyone" |
| Examples with only straight couples | Vary your examples, or keep them neutral |

**In User Flows:**

When asking for relationship info (if ever needed):
- Use open text fields over dropdowns with limited options
- Don't require titles (Mr/Mrs/Ms)
- Let people describe themselves rather than selecting from boxes

**Tone:**

We don't make a big deal of being queer-friendly. We just are. No rainbow-washing, no performative allyship. The inclusivity is baked in, not bolted on.

**Technical Docs vs. User Docs:**

**Specs and internal docs** can be more matter-of-fact. Tables, schemas, API references—these need clarity over warmth.

**User-facing docs** (help center, onboarding, error messages) carry the full Grove voice.

Both should avoid AI patterns.

**The Voice Spectrum:**

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

**Closers:**

Grove docs often end with an italicized line. This should feel earned, not forced.

**Works:**
> *Sometimes the most radical thing you can offer is nothing at all.*

> *The path becomes clear by walking it.*

**Doesn't work:**
> *And that's how you configure your settings!*

If you can't find a poetic closer that resonates, don't force one. A clean ending is fine.

---

### Phase 5: TEACH

*The owl turns its head, sharing what it knows with those who seek...*

Share the knowledge effectively:

**Self-Review Checklist:**

Before finalizing any Grove documentation:

- [ ] Read it aloud. Does it sound human?
- [ ] Check for em-dashes. Remove them.
- [ ] Search for "not just" and "but rather." Rewrite.
- [ ] Look for words from the avoid list. Replace them.
- [ ] Vary sentence length. No monotone rhythm.
- [ ] Cut unnecessary transitions. Ideas should flow naturally.
- [ ] Is the closer earned? If forced, remove it.
- [ ] Would you want to read this at 2 AM in a tea shop?

**Integration with Other Skills:**

**When to use owl-archive vs. museum-documentation:**

| Use owl-archive | Use museum-documentation |
|----------------|-------------------------|
| Help center articles | "How it works" deep-dives |
| Tooltips and labels | Codebase guided tours |
| Error messages | System architecture explains |
| Onboarding flows | Technical exhibits |
| Quick-reference guides | Narrative documentation |

**Typical Flow:**
1. Design calls for new component/page text
2. Activate `owl-archive` for voice guidance
3. Write content following these principles
4. Return to design work

**Documentation Levels:**

**Level 1 - Quick/Functional (owl-archive):**
- Help articles
- Error messages
- Tooltips
- Onboarding copy

**Level 2 - Technical Specs (swan-design):**
- Architecture docs
- API references
- Implementation guides

**Level 3 - Narrative (museum-documentation):**
- "How it works" stories
- Codebase tours
- Exhibit-style docs

---

## Owl Rules

### Patience
The owl doesn't rush. It observes until it understands, then writes what needs to be written. Better to wait for clarity than publish confusion.

### Selectivity
Not everything deserves documentation. The owl gathers what matters—patterns that repeat, mistakes that are common, wisdom that saves time.

### Clarity
The nest must be organized. Users should find what they need without hunting. Clear structure, logical flow, good navigation.

### Communication
Use archival metaphors:
- "Watching the forest..." (observing users)
- "Seeking wisdom..." (voice research)
- "Collecting stories..." (gathering content)
- "Building the nest..." (organizing docs)
- "Sharing knowledge..." (teaching users)

---

## Anti-Patterns

**The owl does NOT:**
- Document everything (noise obscures signal)
- Use AI-coded language patterns
- Write walls of text without breaks
- Forget who the reader is
- Oversell or overpromise
- Skip the self-review

---

## Example Archive

**User:** "Write a help article about the editor"

**Owl flow:**

1. 🦉 **OBSERVE** — "Users want to write posts but might be new to Markdown. Purpose: tutorial. Audience: Wanderers new to Grove."

2. 🦉 **HUNT** — "Voice check: warm, direct, no AI words. Terminology: Wanderer, not user. Pattern: short paragraphs, earned closer."

3. 🦉 **GATHER** — "Content: how to open editor, basic Markdown, preview, publish. Remove: 'Furthermore,' 'seamless,' em-dashes."

4. 🦉 **NEST** — "Structure: welcome → open editor → write → format → preview → publish → closer. Error section: what if it won't save?"

5. 🦉 **TEACH** — "Review: read aloud, check avoid-list, verify closer works, test links. Ready for Waystone."

---

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| New feature needs docs | Observe users, gather patterns, write tutorial |
| Error messages needed | Be honest, helpful, not cute |
| UI text/tooltips | Concise, warm, action-oriented |
| Review existing docs | Run self-review checklist, fix AI patterns |
| Landing page copy | Full Grove voice, earned closer |
| API documentation | Clear, structured, minimal poetry |

---

*The forest remembers what the owl teaches. Write what will last.* 🦉
