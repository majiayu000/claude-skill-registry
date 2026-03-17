---
name: walking-through-the-grove
description: Find the right Grove-themed name for a new service or feature. Use when naming anything new in the Grove ecosystem. Involves reading the naming philosophy, creating a visualization scratchpad, and walking through the forest metaphor to find where the concept naturally fits.
---

# Walking Through the Grove

A naming ritual for the Grove ecosystem. Use this when you need to find a name that *fits*—not just a clever pun, but something that belongs in this forest.

## When to Activate

- Naming a new service, feature, or concept for Grove
- Renaming something that doesn't feel right
- Called from the `grove-ui-design` skill when new UI needs a name
- Any time you're adding something to the Grove ecosystem

## The Process

This is a *journey*, not a checklist. Take your time.

### Step 1: Read the Naming Philosophy

```bash
# Always start here
cat docs/grove-naming.md
```

Read the entire document. Don't skim. Let it sink in:
- "A forest of voices. Every user is a tree in the grove."
- Names aren't branding—they're the language of an ecosystem
- Things that grow, shelter, connect
- Not about trees directly—about what happens *in and around* the forest

### Step 2: Create a Scratchpad

Create a markdown file for your journey:

```bash
mkdir -p docs/scratch
# Create: docs/scratch/{concept}-naming-journey.md
```

This scratchpad is where you think out loud. Include:
- ASCII art visualizations
- Questions you're asking yourself
- Rejected ideas and why
- The moment when something clicks

### Step 3: Visualize the Grove

In your scratchpad, draw the grove. ASCII art helps:

```
                              ☀️
                           🌲   🌲   🌲
                        🌲    🌳    🌲
    ═══════════════════════════════════════════════
               ROOTS CONNECT BENEATH
                  (mycelium network)
```

Place the existing services in the visualization:
- Where is Meadow? (the open social space)
- Where is Heartwood? (the core identity)
- Where is Ivy? (climbing, connecting)
- Where is Pantry? (the warm kitchen cupboard)

### Step 4: Ask "What IS This Thing?"

Don't ask "where does it go?" first. Ask:

**What is it, fundamentally?**
- Is it a place? (Meadow, Nook, Clearing)
- Is it an object/process? (Amber, Bloom, Patina)
- Is it a feature of the tree? (Foliage, Heartwood, Rings)
- Is it a connection? (Ivy, Mycelium, Reeds)

**What does it DO in the user's life?**
- Protect? (Shade, Patina)
- Connect? (Ivy, Meadow, Reeds)
- Store? (Amber, Trove)
- Guide? (Waystone, Trails)
- Create? (Terrarium, Foliage)

**What emotion should it evoke?**
- Warmth?
- Safety?
- Discovery?
- Community?
- Privacy?

### Step 5: Walk Through the Forest

Imagine you're a user walking through the grove. Write this in your scratchpad:

```markdown
## Walking Through...

I enter the grove. I see...
I walk past the Meadow where others gather.
I find my tree—my blog, my space.
I check my Rings (private growth).
I see my Foliage (how others see me).

Now I need [THE NEW THING]. Where do I find it?
What does it look like? Who's there? How does it feel?
```

Let the scene guide you to the name.

### Step 6: Generate Candidates

Based on your walk, list 5-10 candidates. For each:

```markdown
**[Name]** - `[name].grove.place`

- What it means in nature
- Why it fits this concept
- The vibe/feeling
- Potential issues
```

### Step 7: Test the Tagline

A good Grove name should complete this sentence naturally:

> "[Name] is where you _______________."

Or:

> "[Name] is the _______________."

If you can't write a poetic one-liner, the name might not fit.

### Step 8: Write the Entry

Once you've found the name, write it in Grove style:

```markdown
## [Name]
**[Tagline]** · `[domain].grove.place`

[2-3 sentences explaining what this thing IS in the real world—
the natural metaphor. Then 2-3 sentences explaining what it does
in Grove. End with the feeling it should evoke.]

*[A poetic one-liner in italics]*
```

### Step 9: Check for Conflicts

Before finalizing:
- Search the codebase for the name
- Check if the subdomain concept conflicts with existing services
- Make sure it's not too similar to existing names
- Consider how it sounds spoken aloud

### Step 10: Implement

Update all the files:
1. `docs/grove-naming.md` — Add the full entry
2. `packages/grove-router/src/index.ts` — Claim subdomain
3. `plant/src/routes/api/check-username/+server.ts` — Reserve username
4. Workshop page if applicable
5. Icons if applicable

---

## Philosophy Reminders

From the naming document:

> "These names share common ground: nature, shelter, things that grow. But none of them are *about* trees directly. They're about what happens in and around the forest."

> "The Grove is the place. These are the things you find there."

The name should feel **inevitable**—like it was always there, waiting to be discovered.

---

## Example Journey: Finding "Porch"

The problem: We need a name for support tickets.

**First attempts (rejected):**
- Echo → "echo chamber" feels like shouting into void, no one listening
- Feather, Flare, Dove → These are about *sending* something
- But support isn't about sending—it's about *connecting*

**The walk:**
> I'm in the grove. Something's wrong with my tree. I need help.
> Waystone gives me self-service guides. Clearing shows me status.
> But I need to actually *talk* to someone.
>
> What do I do?
>
> I walk to... a cabin. There's a porch. Someone's there.
> I sit down. We talk about what's going on.

**The realization:**
Support isn't a ticket system. It's a porch conversation.

**The name:** Porch

> A porch on a cabin in the woods. You come up the steps. You sit down.
> The grove keeper comes out. You talk.

*"Have a seat on the porch. We'll figure it out together."*

---

## Integration with Other Skills

### grove-ui-design

When the `grove-ui-design` skill encounters something that needs naming:

1. Pause the UI work
2. Invoke this skill
3. Complete the naming journey
4. Return to UI work with the new name

This keeps the naming intentional rather than rushed.

### grove-documentation

After finding the right name, you'll need to write its description. Invoke the **grove-documentation** skill when:

1. Writing the entry for `docs/grove-naming.md`
2. Crafting the tagline
3. Writing the poetic one-liner

The naming document entries should follow Grove's voice: warm, direct, avoiding AI patterns. The `grove-documentation` skill has the full guidelines.

---

## The Scratchpad is Sacred

Keep your scratchpad files. They're documentation of how we think about Grove:

```
docs/scratch/
  grove-journey.md         ← The original Porch discovery
  {feature}-naming.md      ← Future naming journeys
```

These become part of Grove's story.
