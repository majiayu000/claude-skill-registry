---
name: social-writer
description: "Create engaging content for social media platforms: X posts and threads, LinkedIn, Threads, Instagram, Facebook. Includes writing styles, AI-avoidance patterns, hooks catalog, and macOS Notes integration. Keywords: social media, X, X, LinkedIn, threads, posts, hooks, content strategy, AI writing avoidance."
---

# Social Writer

Create platform-optimized social media content that sounds human, drives engagement, and builds audience.

## Quick Navigation

| Topic                 | Reference                                               |
| --------------------- | ------------------------------------------------------- |
| X Single Posts        | [x-posts.md](references/x-posts.md)                     |
| X Threads             | [x-threads.md](references/x-threads.md)                 |
| X Content Strategy    | [x-strategy.md](references/x-strategy.md)               |
| Hook Patterns         | [hooks.md](references/hooks.md)                         |
| LinkedIn              | [linkedin.md](references/linkedin.md)                   |
| Threads & Instagram   | [threads-instagram.md](references/threads-instagram.md) |
| Facebook              | [facebook.md](references/facebook.md)                   |
| AI Writing Avoidance  | [ai-avoidance.md](references/ai-avoidance.md)           |
| Style Guide           | [style-guide.md](references/style-guide.md)             |
| Technical Blog Styles | [technical-styles.md](references/technical-styles.md)   |

## Platform Quick Reference

| Platform      | Limit       | Best Length | Hashtags | Key Rule                           |
| ------------- | ----------- | ----------- | -------- | ---------------------------------- |
| **X**         | 280 chars   | 230-280     | 1-2 max  | Hook in first line, use full space |
| **LinkedIn**  | 3,000 chars | 1,300       | 3-5      | Hook before "see more"             |
| **Threads**   | 500 chars   | 400-500     | None     | Conversational, no hashtags        |
| **Instagram** | 2,200 chars | Varies      | 5-15     | Visual-first, line breaks          |
| **Facebook**  | Unlimited   | <250        | 2-3      | Community, engagement              |

## Content Type Router

```
What are you creating?
│
├─ X?
│   ├─ Single insight/observation → x-posts.md
│   ├─ Multi-part story/tutorial → x-threads.md
│   └─ Content planning → x-strategy.md
│
├─ LinkedIn → linkedin.md
│   └─ Professional, B2B, thought leadership
│
├─ Threads/Instagram → threads-instagram.md
│   └─ Conversational, authentic, visual
│
├─ Facebook → facebook.md
│   └─ Community, engagement, events
│
└─ Technical blog → technical-styles.md
    ├─ Karpathy style (conversational, personal)
    └─ Deep technical (opinion-forward, contrarian)
```

## Writing Workflow

### 1. Select Platform & Format

Choose based on:

- **Audience**: Where do they spend time?
- **Content depth**: Quick insight vs deep dive
- **Goal**: Engagement, education, announcement

### 2. Load Style Reference

Before writing:

1. Read platform-specific guide
2. Read [ai-avoidance.md](references/ai-avoidance.md) — critical for human voice
3. Read [style-guide.md](references/style-guide.md) for tone

### 3. Draft Content

Apply platform constraints from start. Style informs structure.

### 4. Quality Check

Run through checklist below before posting.

## Universal Quality Checklist

### Voice

- [ ] Sounds like a person, not AI?
- [ ] Zero banned words (delve, unleash, harness, leverage)?
- [ ] Zero em-dashes (—)?
- [ ] Contractions used naturally?

### Specificity

- [ ] Includes names, numbers, tools, dates?
- [ ] Concrete examples, not hypotheticals?
- [ ] Would I bookmark this if someone else wrote?

### Structure

- [ ] Hook in first line?
- [ ] Sentence lengths vary (5-40 words)?
- [ ] Each paragraph/tweet can stand alone?

### Value

- [ ] Teaches something specific?
- [ ] Actionable today?
- [ ] From real experience?

## X Quick Start

### Single Post Pattern

```
[Hook - stop the scroll]

[Context or specific detail]

[Insight or learning]

[Optional: engagement question]
```

**Example:**

```
Shipped curation v1 for agents.foo today.

Discovery is way harder than app stores. Agents are conversations, not static features.

Had to rebuild around context matching instead of keyword search.
```

### Thread Pattern

```
1/N [Bold hook - main insight] 👇

2/N [Context or setup]

3-N/N [Key points, one per tweet]

N/N [Summary + CTA]
```

**Rules:**

- First tweet MUST end with 👇 or 🧵 to signal thread
- Use N/M numbering (1/7, 2/7... 7/7)
- Each tweet must stand alone
- Max 5-7 tweets (longer = blog post)

## High-Engagement Content Patterns

| Pattern                  | Structure                                    | Best For           |
| ------------------------ | -------------------------------------------- | ------------------ |
| **Shipped X, Learned Y** | What shipped + key learning + why it matters | Project updates    |
| **How to X**             | Problem + steps + key insight                | Tutorials          |
| **Problem → Solution**   | Problem + failed attempts + what worked      | Case studies       |
| **Contrarian**           | Popular belief + why wrong + your evidence   | Thought leadership |
| **Tool Recommendation**  | Tool + specific benefit + real example       | Resources          |

## Content Selection: What to Share

### Always Share ✓

- Shipped work + learnings
- Non-obvious insights
- Tool recommendations with specifics
- Solutions to common problems

### Skip ✗

- Generic progress updates
- Plans before execution
- Obvious observations
- Engagement bait ("RT if you agree")
- Vague hype

## Critical Prohibitions

- Do not use words: delve, unleash, harness, leverage, robust, seamless, game-changer, unlock
- Do not use em-dashes (—) anywhere
- Do not use "It's not X, it's Y" pattern
- Do not ask for engagement ("RT if you agree", "What do you think?")
- Do not use formal transitions (Furthermore, Moreover, Additionally)
- Do not write uniform sentence lengths
- Do not skip the hook

## Links

- [ai-avoidance.md](references/ai-avoidance.md) — Most important, read first
- [hooks.md](references/hooks.md) — Hook patterns with examples
- [x-strategy.md](references/x-strategy.md) — What to share
