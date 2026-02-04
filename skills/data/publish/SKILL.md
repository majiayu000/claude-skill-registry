---
name: publish
description: Draft email and tweet for a new blog post. Reads the latest post from campedersen.com, generates Kit.com broadcast copy and a tweet, ready to paste.
allowed-tools: Read, Glob, Bash
---

# Publish

Drafts promotional content for a new blog post.

## Usage

- `/publish` - Draft for most recent post
- `/publish [slug]` - Draft for specific post

## Workflow

1. Find the post in `~/Developer/campedersen.com/src/posts/`
2. Read it fully to understand the hook
3. Generate email + tweet using voice from `/blog` skill
4. Output both in copy-pasteable format

## Email Format

```
Subject: [Post Title]

[1-2 sentence hook - the problem or revelation]

[Optional: 1 sentence context]

Read it here: https://campedersen.com/[slug]

- Cam
```

## Tweet Format

```
[hook that stands alone - lowercase, casual]

https://campedersen.com/[slug]
```

Max 280 chars. No hashtags. No emojis.

## Voice Quick Reference

See `/blog` for full guidelines. Key points:

- Lead with the problem solved or a weird specific detail
- Lowercase for tweets, casual punctuation
- Short sentences, dashes over semicolons
- One exclamation max
- "shipped" not "launched", "wrote" not "published"
- End email with "- Cam"

**Never say:**
- "We're excited to announce..."
- "Check out this amazing..."
- "I'm thrilled to share..."

## Examples

**Debugging post:**

Email:
```
Subject: Hung by a Thread

My robot froze at 2am. Same iteration every time - 1,615. Took 8 hours to find a 2-line fix.

Wrote about rayon deadlocks and why you should never call into a library while holding a mutex.

Read it here: https://campedersen.com/rayon-mutex-deadlock

- Cam
```

Tweet:
```
my robot froze at 2am. 8 hours of debugging. the fix was 2 lines.

https://campedersen.com/rayon-mutex-deadlock
```

**Technical explainer:**

Email:
```
Subject: Cutting Up Curved Things

Your GPU doesn't know what a cylinder is. It only knows triangles.

Wrote about how CAD geometry becomes something a graphics card can actually draw.

Read it here: https://campedersen.com/tessellation

- Cam
```

Tweet:
```
your GPU doesn't know what a cylinder is. it only knows triangles.

wrote about tessellation - with a pizza you can eat.

https://campedersen.com/tessellation
```
