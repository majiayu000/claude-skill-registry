---
name: language
description: Research and use customer language across Product and Marketing. Sales Safari methodology for finding watering holes, extracting pain language, and creating "OH YEAH!" resonance.
triggers:
  - sales safari
  - customer language
  - watering hole
  - audience language
  - voice of customer
  - how customers talk
  - resonance
  - product copy
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, AskUserQuestion
---

# Customer Language Mastery

Research how your customers actually talk, then use their exact language across Product and Marketing to create instant resonance.

## The Core Principle

**First Law of Customer Physics:** A customer at rest will remain at rest unless you provide a motivating, attention-grabbing force.

Language is that force. Your words must bypass the customer's natural filters by creating **resonance** — the "OH YEAH! THAT'S FOR ME!" reaction.

If your language is bland or tries to appeal to everyone, it exerts no gravitational force and gets ignored.

## Where Customer Language Applies

| Domain | Examples |
|--------|----------|
| **Product UI** | Button labels, error messages, empty states, onboarding |
| **Feature Naming** | What you call features determines if users understand them |
| **Documentation** | Guides, tooltips, help text |
| **Settings/Options** | How you frame choices affects decisions |
| **Notifications** | Push, email, in-app alerts |
| **Marketing** | Landing pages, emails, ads, social |

## Conversation Starter

Use `AskUserQuestion` to gather context:

1. **Who is your target audience?** (job title, industry, experience level)
2. **What problem does your product solve?**
3. **What copy needs work?** (Product UI, landing page, feature naming, etc.)
4. **Do you have existing customer conversations?** (support tickets, reviews, interviews)

---

## Part 1: Sales Safari — Finding Watering Holes

A **watering hole** is anywhere your target audience gathers to discuss problems, share advice, or seek help.

### Watering Hole Keywords

Combine audience terms with these keywords to find communities:

| Category | Keywords |
|----------|----------|
| **Community** | forum, community, group, mailing list, chat, Discord, Slack |
| **Help-Seeking** | help, problems, advice, questions, FAQs, support |
| **Learning** | tutorial, resources, guide, best practices, how to |
| **Evaluation** | reviews, comparison, best, vs, alternative |
| **Discussion** | discussions, sharing, experiences, stories |
| **Social** | Twitter/X chat, Facebook Group, subreddit, LinkedIn Group |

### Search Patterns

```
[audience term] + forum
[audience term] + community
[audience term] + "I'm struggling with"
[audience term] + "how do you handle"
[audience term] + site:reddit.com
[audience term] + site:news.ycombinator.com
[problem] + "anyone else"
[problem] + "is it just me"
```

### Platform-Specific Searches

| Platform | Search Pattern |
|----------|----------------|
| Reddit | `site:reddit.com [audience] [problem]` |
| Hacker News | `site:news.ycombinator.com [topic]` |
| Stack Overflow | `site:stackoverflow.com [technology] [problem]` |
| Product Hunt | `site:producthunt.com [category] discussions` |
| G2/Capterra | `site:g2.com [competitor] reviews` |
| Twitter/X | `[problem] filter:replies min_faves:10` |

---

## Part 2: Extracting Customer Language

Once you find watering holes, extract these language patterns:

### 1. Pain Language

Words and phrases expressing **frustration, anxiety, powerlessness, or uncertainty**.

**Listen for:**
- "I hate when..."
- "It drives me crazy that..."
- "I'm so frustrated with..."
- "Why can't I just..."
- "I've tried everything but..."
- "I'm worried about..."
- "I don't know how to..."

**Extract:** The exact phrases, not your interpretation.

### 2. Desire Language

Words expressing what they **want** but don't have.

**Listen for:**
- "I wish..."
- "If only..."
- "I just want to..."
- "It would be amazing if..."
- "My dream is..."

### 3. Jargon & Insider Terms

Every audience has vocabulary that signals belonging.

**Types of jargon:**
- **Technical terms** they use (not textbook definitions)
- **Abbreviations** unique to their world
- **Slang** that identifies insiders
- **Phrases** that have specific meaning in context

**Why it matters:** Using insider language creates instant trust. Wrong language signals "outsider."

### 4. Recommendation Patterns

How do they give each other advice?

**Listen for:**
- "You should try..."
- "What worked for me was..."
- "Read this..."
- "Check out..."
- "Think about it this way..."

**Use these structures** in your copy to feel like peer advice, not sales pitch.

---

## Part 3: Language Extraction Template

When researching, fill this out:

```markdown
## Language Research: [Audience]

### Watering Holes Found
- [Platform]: [Community name] - [Why relevant]
- [Platform]: [Community name] - [Why relevant]

### Pain Phrases (Exact Quotes)
| Quote | Emotion | Frequency |
|-------|---------|-----------|
| "[exact quote]" | frustrated/anxious/desperate | common/rare |

### Desire Phrases (Exact Quotes)
| Quote | What They Want |
|-------|----------------|
| "[exact quote]" | [interpretation] |

### Insider Jargon
| Term | What It Means to Them |
|------|----------------------|
| [term] | [contextual meaning] |

### Recommendation Patterns
- "[How they give advice]"
- "[Structure they use]"

### Words They NEVER Use
- [terms that signal outsider]
```

---

## Part 4: Worldview Resonance

Effective language expresses a **worldview** — shared beliefs and values.

### Take a Stand

Polarizing language **attracts** the right people and **repels** the wrong ones.

**Weak (appeals to everyone, resonates with no one):**
> "A better way to manage projects"

**Strong (takes a stand):**
> "Project management for teams who hate project management"

### Worldview Crossover

Find the overlap between YOUR worldview and your CUSTOMER'S worldview:

```
Your Beliefs          Customer's Beliefs
     \                    /
      \                  /
       \                /
        [CROSSOVER ZONE]
        This is where your
        messaging lives
```

### Positioning Through Language

| Audience Type | Language Signals |
|---------------|------------------|
| Professional/Enterprise | "controls", "governance", "compliance", "scalable" |
| Startup/Indie | "ship fast", "no bloat", "just works", "for builders" |
| Creative | "beautiful", "craft", "artisan", "curated" |
| Technical | "API-first", "extensible", "open source", "self-hosted" |
| Budget-conscious | "affordable", "free tier", "no hidden fees", "transparent" |

---

## Part 5: The "OH YEAH!" Test

Before shipping any copy, run this test:

### Does your language...

| Criterion | ✓/✗ |
|-----------|-----|
| Use words your customers actually use? | |
| Express a worldview they share? | |
| Address a pain they've expressed (in their words)? | |
| Feel like advice from a peer, not a pitch? | |
| Repel people who aren't your customer? | |
| Make the right person say "That's for me!"? | |

### Red Flags

- ❌ Afraid of offending anyone → too weak
- ❌ Using industry jargon they don't use → outsider signal
- ❌ Describing features, not outcomes → no resonance
- ❌ Corporate-speak when audience is casual → tone mismatch
- ❌ Casual when audience is professional → credibility loss

---

## Part 6: Application Examples

### Product UI

**Before (generic):**
> Error: Invalid input

**After (using customer language):**
> Hmm, that doesn't look right. Double-check the format?

---

**Before (feature-focused):**
> Enable notifications

**After (outcome-focused, using desire language):**
> Never miss an update from your team

### Feature Naming

**Before (technical):**
> Automated Workflow Engine

**After (using customer problem language):**
> "Set it and forget it" automation

### Empty States

**Before (bland):**
> No projects yet

**After (using desire language):**
> Ready to ship something? Create your first project.

### Error Messages

**Before (blame user):**
> Invalid email address

**After (helpful, peer tone):**
> That email looks incomplete — missing something after the @?

### Landing Page Headline

**Before (feature-focused):**
> All-in-one project management platform

**After (pain language + worldview):**
> Finally, project management that doesn't feel like a second job

---

## Output Format

When applying this skill, deliver:

```markdown
## Customer Language Analysis

### Research Summary
- **Watering holes searched:** [list]
- **Quotes extracted:** [count]
- **Key insight:** [one sentence]

### Language Patterns Discovered

**Pain phrases:**
- "[exact quote]" → Use for: [where to apply]

**Desire phrases:**
- "[exact quote]" → Use for: [where to apply]

**Insider jargon:**
- [term]: [meaning] → Use for: [where to apply]

### Recommended Copy Changes

| Location | Before | After | Why |
|----------|--------|-------|-----|
| [UI element/page] | [current] | [recommended] | [language pattern used] |

### "OH YEAH!" Test Results
[Run the test on recommended copy]
```

---

## When to Use This vs Other Skills

| Use `language` when... | Use other skills when... |
|------------------------|--------------------------|
| Researching how customers talk | Need emotional trigger words (`power-words`) |
| Writing product UI copy | Need full landing page (`landing-page-builder`) |
| Naming features | Need brand names (`namer` agent) |
| Improving resonance | Need SEO optimization (`seo-audit`) |
| Extracting voice of customer | Need to find communities (`customer-discovery`) |

## What This Skill Does NOT Do

- Replace user research interviews
- Guarantee conversion (testing required)
- Provide word lists (see `power-words` for that)
- Write full marketing campaigns
