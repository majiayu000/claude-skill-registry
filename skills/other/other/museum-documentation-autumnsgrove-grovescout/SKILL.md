---
name: museum-documentation
description: Write elegant, narrative-driven documentation that treats codebases and systems as exhibits worth exploring. Use when creating documentation for Wanderers and visitors who want to understand how Grove works. This is the "fancy" documentation style—warm, inviting, meant to be read and enjoyed.
---

# Museum Documentation

> *Documentation as hospitality. Code as curated collection.*

The art of transforming technical systems into welcoming guided tours. Museum documentation positions the writer as a guide walking alongside readers through "why" questions before diving into implementation specifics.

This is Grove's elegant documentation style—meant for Wanderers of any experience level who want to understand the technologies, patterns, and decisions that make Grove what it is.

## When to Activate

- Creating documentation meant to be **read by Wanderers**, not developers
- Writing knowledge base articles that explain how systems work
- Documenting a codebase, feature, or system for curious visitors
- Creating "how it works" content for the help center
- Writing technical content that should feel inviting, not intimidating
- Building exhibits for future knowledge base sections
- Onboarding documentation that walks through architecture

**Not for:**
- API references (use grove-documentation)
- Technical specs (use grove-spec-writing)
- Quick-reference guides

---

## Core Philosophy

Documentation should function as **hospitality**.

When readers enter a codebase or system, they're visitors unfamiliar with its architecture and design decisions. Museum-style documentation positions the writer as a guide rather than a reference compiler, walking alongside readers through "why" questions before diving into implementation.

### The Museum Metaphor

```
             🌲  Welcome  🌲
          ╭─────────────────────╮
          │                     │
          │   ╭─────────────╮   │
          │   │  EXHIBIT A  │   │
          │   │             │   │
          │   │  How Login  │   │
          │   │    Works    │   │
          │   │             │   │
          │   ╰─────────────╯   │
          │         │           │
          │    ═════╪═════      │
          │         │           │
          │   ╭─────────────╮   │
          │   │  EXHIBIT B  │   │
          │   ╰─────────────╯   │
          │                     │
          ╰─────────────────────╯

    Walk through. Take your time.
    Every exhibit tells a story.
```

A museum doesn't hand you a catalog and wish you luck. It **guides** you through a curated experience, placing context before complexity, stories before specifications.

---

## Key Principles

### Orient Before Explaining

Start exhibits by establishing context. Before showing code or architecture, tell readers:
- What they're looking at
- Why it exists
- Who benefits from it

**Instead of:**
> The TokenRefreshMap stores active refresh operations keyed by user ID.

**Write:**
> When someone's login expires, we need to refresh their credentials without logging them out. This map coordinates that process—preventing duplicate refresh attempts when multiple tabs are open.

### Explain Reasoning Over Facts

Code shows *what*. Documentation explains *why*.

Rather than stating that a Map stores token refresh operations, describe the coordination problem it solves. Connect the abstraction to the experience it creates.

### Use Accessible Metaphors

Connect technical concepts to familiar experiences:

| Technical Concept | Museum Metaphor |
|-------------------|-----------------|
| Database | A filing cabinet with organized drawers |
| Cache | A quick-lookup shelf by the door |
| Middleware | A security checkpoint you pass through |
| Queue | A line where requests wait their turn |
| Worker | A helpful assistant handling tasks in the background |
| Webhook | A doorbell that rings when something happens |

### Show Real Code, Then Analyze

Present actual code snippets followed by clear explanation of their significance:

```typescript
const pending = this.refreshInProgress.get(userId);
if (pending) return pending;
```

*If a refresh is already happening for this person, we wait for that one instead of starting another. One kitchen, one cook.*

---

## Structural Framework

Museum exhibits follow consistent anatomy:

### 1. Title with Tagline

```markdown
# The Authentication Exhibit

> Where login happens. Where trust begins.
```

### 2. "What You're Looking At" Section

Orient the reader immediately:

```markdown
## What You're Looking At

This is where login happens. When someone proves they own an email
address, this code decides what they can access and how long that
access lasts.

You'll see OAuth flows, session management, and token refresh logic.
Nothing scary—just careful choreography.
```

### 3. Organized Tour Structure

Use galleries, parts, or sections to organize the journey:

```markdown
## The Tour

### Gallery 1: The Front Door
How visitors arrive and prove who they are.

### Gallery 2: The Memory Room
How we remember who's logged in.

### Gallery 3: The Renewal Office
How sessions stay fresh without interrupting work.
```

### 4. "Patterns Worth Stealing"

Highlight transferable lessons:

```markdown
## Patterns Worth Stealing

**The "already in progress" check.** Before starting an expensive
operation, check if it's already running. Simple, but easy to forget.

**Centralized error handling.** All auth failures flow through one
function. One place to fix, one place to log.
```

### 5. "Lessons Learned"

Offer honest reflection:

```markdown
## Lessons Learned

We tried stateless JWTs first. Simpler, they said. Scalable, they
promised. But logout was impossible—tokens couldn't be revoked.

Session-based auth is older, but it works. Sometimes boring is right.
```

### 6. "Continue Your Tour"

Link to related exhibits:

```markdown
## Continue Your Tour

- **[The Database Exhibit](./database.md)** — Where sessions are stored
- **[The API Exhibit](./api.md)** — How protected routes check access
- **[The Security Exhibit](./security.md)** — Rate limiting and protection
```

### 7. Meaningful Closing Signature

```markdown
---

*— Autumn, January 2026*
```

Or a poetic one-liner:

```markdown
---

*Trust is built one verified request at a time.*
```

---

## Visual Elements

### ASCII Flow Diagrams

Show processes and relationships:

```
  Visitor                    Grove                     Google
     │                         │                          │
     │   "Log me in"           │                          │
     │ ───────────────────────>│                          │
     │                         │   "Who is this?"         │
     │                         │ ────────────────────────>│
     │                         │                          │
     │                         │   "It's autumn@..."      │
     │                         │ <────────────────────────│
     │                         │                          │
     │   "Welcome back"        │                          │
     │ <───────────────────────│                          │
     │                         │                          │
```

### Tables for Quick Reference

```markdown
| File | What It Does | Why It Matters |
|------|--------------|----------------|
| `auth.ts` | Handles OAuth flow | The front door |
| `session.ts` | Manages login state | The memory |
| `middleware.ts` | Checks every request | The bouncer |
```

### Code Blocks with Context

Never show code in isolation. Always explain before or after:

```typescript
// Every request passes through this checkpoint
export async function authGuard(request: Request): Promise<Response | null> {
  const session = await getSession(request);
  if (!session) {
    return redirect('/login');
  }
  return null; // Continue to the page
}
```

*If you're not logged in, you go to login. If you are, you continue. Simple checkpoint logic.*

---

## Voice and Tone

### Do

- Write conversationally using "you" and "we" naturally
- Acknowledge imperfections ("We tried X first. It didn't work.")
- Include personal touches ("This took three attempts to get right.")
- Use short paragraphs (2-4 sentences)
- Vary sentence rhythm

### Avoid

- Em-dashes (use periods, commas, or parentheses)
- Corporate jargon ("robust," "seamless," "leverage")
- Heavy transitions ("Furthermore," "Moreover," "Additionally")
- Passive voice when active is clearer
- Hedging language ("This may potentially help...")

### The Distinction

**Generic (avoid):**
> This module provides robust functionality for handling authentication flows in a seamless manner, leveraging industry-standard OAuth protocols.

**Museum style (use):**
> This is where login happens. When someone proves they own an email address, this code decides what they can access.

---

## Organization Patterns

### Full Codebase: MUSEUM.md

For documenting an entire codebase, create a central `MUSEUM.md` that serves as the entrance:

```markdown
# Welcome to the Grove Museum

> A guided tour of how this forest grows.

## The Wings

- **[The Architecture Wing](./docs/exhibits/architecture.md)** — The big picture
- **[The Authentication Exhibit](./docs/exhibits/auth.md)** — Trust and identity
- **[The Database Galleries](./docs/exhibits/database.md)** — Where data lives
```

### Single Directory: EXHIBIT.md

For a single complex feature or directory:

```markdown
# The Editor Exhibit

> Where words become posts.

This directory contains everything that powers the writing experience...
```

### Complex Features: Gallery Structure

For multi-part systems, use galleries:

```markdown
## Gallery 1: Data Layer
How posts are stored and retrieved.

## Gallery 2: API Endpoints
The doors visitors knock on.

## Gallery 3: The Editor Component
Where the magic happens in the browser.

## Gallery 4: Security Considerations
Keeping things safe.
```

---

## Validation Checklist

Before finalizing any museum documentation:

### Structure
- [ ] Title includes tagline
- [ ] "What You're Looking At" orients the reader
- [ ] Organized into logical galleries/sections
- [ ] "Patterns Worth Stealing" highlights transferable lessons
- [ ] "Continue Your Tour" links to related content
- [ ] Meaningful closing (signature or poetic line)

### Visual Variety
- [ ] At least one ASCII diagram or flow
- [ ] Tables where comparison helps
- [ ] Code blocks with explanatory context
- [ ] No walls of text longer than 4-5 paragraphs

### Voice (refer to grove-documentation)
- [ ] No em-dashes
- [ ] No corporate jargon
- [ ] Direct tone explaining motivations
- [ ] Acknowledged imperfections where honest
- [ ] Clear connections between system parts

### Reader Experience
- [ ] A newcomer could follow the tour
- [ ] "Why" is answered before "how"
- [ ] Technical details are contextualized
- [ ] The path feels logical and navigable

---

## Integration with Other Skills

### Before Writing

1. **walking-through-the-grove** — If the exhibit needs a name
2. **grove-documentation** — Review voice guidelines, especially the "avoid" lists

### While Writing

3. **grove-spec-writing** — Borrow ASCII art techniques for diagrams
4. **grove-documentation** — Check terminology (Wanderer, Rooted, etc.)

### After Writing

5. **Read as a newcomer** — Traverse the documentation as if you've never seen it
6. Does the path feel logical? Would you want to explore further?

---

## Example: A Complete Exhibit

```markdown
# The Session Exhibit

> How Grove remembers who you are.

## What You're Looking At

When you log in, Grove needs to remember you. Not forever—just long
enough for your visit. This exhibit shows how that memory works.

You'll see cookies, database tables, and the careful dance of
"who are you?" that happens with every page load.

---

## Gallery 1: The Cookie Jar

A session starts with a cookie. Not the chocolate chip kind—a small
piece of text your browser holds onto.

```typescript
const SESSION_COOKIE = 'grove_session';
const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000; // 7 days
```

*Seven days. Long enough to be convenient, short enough to stay secure.*

When you log in, we generate a random ID and store it in this cookie.
The ID itself means nothing—it's just a key to look you up.

---

## Gallery 2: The Memory Book

The actual session data lives in the database:

| Column | What It Holds |
|--------|---------------|
| `id` | The random key from the cookie |
| `user_id` | Who this session belongs to |
| `created_at` | When you logged in |
| `expires_at` | When this session ends |

Every time you load a page, we look up your cookie's ID in this table.
If we find it (and it hasn't expired), you're still logged in.

---

## Gallery 3: The Refresh Dance

Sessions expire. But logging in every week is annoying.

So we do a quiet refresh: when your session is more than halfway
through its life, we extend it. You never notice. You just stay
logged in while you're active.

```typescript
if (session.expiresAt < Date.now() + SESSION_DURATION / 2) {
  await extendSession(session.id);
}
```

*Active visitors stay. Abandoned sessions expire.*

---

## Patterns Worth Stealing

**The "halfway refresh" pattern.** Don't wait until expiration to
extend sessions. Extend them while the visitor is active.

**Random IDs over sequential.** Session IDs should be unpredictable.
Never use auto-incrementing numbers for security tokens.

---

## Lessons Learned

We used to store session data in the cookie itself (JWTs). Simpler,
we thought. But then we couldn't revoke sessions—if someone's token
leaked, we had no way to invalidate it.

Database sessions are older technology. Sometimes older is wiser.

---

## Continue Your Tour

- **[The Authentication Exhibit](./auth.md)** — How login happens
- **[The Security Exhibit](./security.md)** — Rate limiting and protection

---

*— Autumn, January 2026*
```

---

## The Underlying Purpose

Museum documentation respects readers' time and intelligence while acknowledging that code is knowledge deserving careful stewardship.

Wanderers who read these exhibits should leave understanding not just *what* Grove does, but *why* it does it that way. They should feel like they've been welcomed into the workshop, not handed a manual.

*Every codebase has stories. Museum documentation tells them.*
