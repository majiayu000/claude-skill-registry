---
name: elevator-pitch
description: Create a 30-second elevator pitch — who you help, what problem you solve, what makes you different, and the result you deliver. Produces 3 variations (casual, professional, written). Max 50 words each. Use when user needs an "elevator pitch", "30-second pitch", "how do I describe what I do", or "networking intro".
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# Elevator Pitch Generator

**Purpose:** Create a concise, compelling pitch that answers "what do you do?" in a way that attracts the right people and opportunities. Three variations for different contexts.

## When to Activate

Use this skill when:
- User asks for an elevator pitch or networking intro
- User mentions "how do I describe what I do?"
- User needs a 30-second pitch for events, calls, or bios
- User wants a concise positioning statement

## The 4 Components

Every pitch must answer:
1. **Who you help** (specific audience)
2. **What problem you solve** (their pain point)
3. **What makes you different** (your unique angle)
4. **The result you deliver** (tangible outcome)

## Three Variations

### Variation 1: Casual (Networking, Coffee Chats)
Conversational, approachable. The version you'd say to someone at a party when they ask "what do you do?"

**Characteristics:**
- Starts with "I help..." or "You know how..."
- Uses everyday language
- Feels like talking, not presenting
- Max 50 words

### Variation 2: Professional (Investor/Client Meetings)
Polished, confident. The version for professional introductions, pitch meetings, or discovery calls.

**Characteristics:**
- Starts with a credibility marker or result
- Includes specific metrics or outcomes if available
- Authoritative but not arrogant
- Max 50 words

### Variation 3: Written (Website, Bio, Email Signature)
Optimized for reading, not speaking. The version that works in text format.

**Characteristics:**
- Third person OR first person (user's preference)
- Includes searchable keywords
- Works standalone without context
- Max 50 words

## Output Format

```markdown
# Elevator Pitch: [Name/Business]

---

## 🗣️ Casual (Networking)

"[Pitch — max 50 words]"

**Word count:** [X]/50
**Use for:** Parties, coffee chats, casual introductions

---

## 💼 Professional (Client/Investor)

"[Pitch — max 50 words]"

**Word count:** [X]/50
**Use for:** Discovery calls, pitch meetings, professional events

---

## ✍️ Written (Bio/Website)

"[Pitch — max 50 words]"

**Word count:** [X]/50
**Use for:** Website hero, email signature, speaker bios, social profiles

---

## Building Blocks

For mixing and matching in different contexts:

**Who I help:** [Specific audience]
**The problem:** [What they struggle with]
**My approach:** [What makes me different]
**The result:** [Tangible outcome]

---

## Quick Versions

**One-liner (under 15 words):**
[Ultra-compressed version]

**Tagline (under 10 words):**
[Punchy tagline version]
```

## Quality Checklist

- [ ] All 3 variations under 50 words each
- [ ] Each answers all 4 components (who, problem, different, result)
- [ ] Casual version sounds like natural speech
- [ ] Professional version is polished and confident
- [ ] Written version works in text without vocal delivery
- [ ] No jargon the listener/reader wouldn't understand
- [ ] Specific enough to differentiate (not "I help people succeed")
- [ ] Based on context files (not generic)
- [ ] Building blocks provided for flexibility
- [ ] One-liner and tagline bonus versions included
