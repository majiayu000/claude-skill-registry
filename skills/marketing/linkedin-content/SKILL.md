---
name: linkedin-content
description: Design LinkedIn posts, banners, and profile content. Creates text posts with hooks, visual banners as React components, and profile optimization.
disable-model-invocation: true
---

# LinkedIn Content Creation

Create LinkedIn posts, visual content, banners, and profile optimization for AEO brand positioning.

## Target Audience

**30+ year old founders and business owners** who:
- Run premium/high-ticket businesses
- Are starting to worry about AI visibility
- Don't know what AEO is yet
- Are active on LinkedIn for business development

## Brand Voice

- Direct, confident, not salesy
- Data-driven (specific numbers: 0% to 90%, 7/10, $10M)
- Origin story anchored (Porsche/BMW story)
- Contrarian without being aggressive
- Short sentences. Punchy. No fluff.
- No em dashes. No corporate speak.

## Origin Story (Use in Hooks)

> "ChatGPT convinced me to buy a Porsche instead of a BMW. 50K purchase. Mind completely changed by AI. If it can influence ME - a marketer who scaled a brand to $10M - what's it doing to YOUR customers?"

## Key Proof Points

| Proof | Detail |
|-------|--------|
| FueGenix scale | $0 to $10M (first $5M Meta ads, next $5M AI) |
| AI visibility | 0/10 to 7/10 Gemini mentions in 30 days |
| Global ranking | #1 for "artistic perfection" globally |
| ChatGPT consistency | 50% to 90% with direct citations |
| Pricing fix | ChatGPT went from citing $25K (wrong) to $50K (correct) |
| Protocol name | AEO Protocol |
| Website | aeoprotocol.ai |

---

## Post Types

### 1. Hook Posts (Pattern Interrupt)

Open with something unexpected, then connect to AEO.

**Hook formulas:**
- "I [unexpected personal story]. Here's what that taught me about [business insight]."
- "[Controversial statement]. Here's why."
- "I asked ChatGPT [question]. The answer terrified me."
- "[Specific number] that changed how I think about [topic]."
- "Your competitors are doing [thing] and you don't even know it."

### 2. Data Posts (Proof/Authority)

Share specific audit results, consistency test data, or client outcomes.

**Structure:**
```
[Surprising data point]

[Context - why this matters]

[What I did about it]

[Result with specific numbers]

[Takeaway for the reader]

---
[Soft CTA or question]
```

### 3. Framework Posts (Education)

Teach one AEO concept in a digestible format.

**Topics:**
- First 50 Words rule
- 10-Run Consistency Test
- Discovery vs branded queries
- Why SEO rankings don't equal AI visibility
- Google shows 10 results, ChatGPT gives 1 answer

### 4. Story Posts (Engagement)

Tell a narrative with a business lesson.

**Structure:**
- Line 1-2: Hook (pattern interrupt)
- Lines 3-8: Story setup (tension)
- Lines 9-12: The turning point
- Lines 13-16: The result/lesson
- Line 17: CTA or question

### 5. Carousel/Visual Posts

Created as React components in the aeo-landing project at `/banner` route or similar.

---

## Post Formatting Rules

1. **First line is everything** - Pattern interrupt or curiosity gap
2. **One idea per line** - Short sentences, lots of white space
3. **No walls of text** - Max 2-3 lines per paragraph
4. **Use line breaks aggressively** - LinkedIn rewards scannability
5. **End with engagement** - Question, CTA, or provocative statement
6. **No hashtags in body** - Add 3-5 at the very end if needed
7. **No emojis** unless specifically requested
8. **No em dashes** - Use periods or commas instead

---

## Tournament Method for Posts

When writing multiple post options, use tournament-style selection:

1. **Generate 4-6 hooks** for the same topic
2. **Score each** on:
   - Pattern Interrupt (35%) - Does it stop the scroll?
   - Curiosity Gap (25%) - Does it make them want to read more?
   - Authenticity (25%) - Does it sound like the brand voice?
   - Shareability (15%) - Would someone tag a friend?
3. **Eliminate** to top 2, then pick winner
4. **Write full post** from winning hook

---

## Visual Content (React Banners)

Banners and visual content are built as React components in the aeo-landing project.

### Location
`/Users/sohaib/Downloads/aeo/aeo-landing/src/pages/LinkedInBanner.tsx`

### Route
Accessible at `/banner` in the dev server for screenshot.

### Design System
Uses the aeo-landing design tokens:
- **Background:** #0a0a0f (near-black)
- **Primary:** #00d4ff (cyan)
- **Secondary:** #3b82f6 (blue)
- **Accent:** #8b5cf6 (purple)
- **Text:** #f8fafc (near-white)
- **Heading font:** Syne (font-heading)
- **Body font:** Space Grotesk (font-sans)

### Banner Structure (Ty Frankel Model)
- Left side: Data visualization (chart/graph with dots, grid lines, glow)
- Center: Bold headline text + URL pill
- Right side: Tangible visual (chat mockup, UI element)
- Background: Subtle gradient orbs for depth

### Key Principles
- Graph should have volatility (zigzag /\/\/) not smooth curves
- 10-20 data points max with dots on each
- Chart fades into background via CSS mask
- Right-side element should be tangible (chat UI, not abstract blobs)
- No neural networks, no abstract orbs as main elements
- Background orbs are subtle (blur-[80px-100px], low opacity)
- Fonts match website exactly (Syne headings, Space Grotesk body)
- text-gradient class available for cyan-to-purple gradient text

---

## Profile Optimization

### Headline Formula
```
[Origin hook] | [Specific result] | [Mechanism name]
```

Current:
```
ChatGPT convinced me to buy a Porsche. Now I make AI recommend YOUR brand | 0% to 90% AI visibility in 30 days | Scaled FueGenix $0-$10M | AEO Protocol
```

### About Section Structure (Ty Model)
1. Origin story (2-3 lines, pattern interrupt)
2. The question it raised (1 line)
3. What you built (mechanism name)
4. Timeline ("Started X. Mastered by Y.")
5. Named client results (add as you get them)
6. The belief statement ("Google shows 10. ChatGPT gives 1.")
7. Who it's for (qualification)
8. CTA (DM "AUDIT")

---

## Content Calendar Themes

| Day | Theme | Post Type |
|-----|-------|-----------|
| Mon | Data/Proof | Audit results, consistency tests |
| Tue | Education | AEO framework, one concept |
| Wed | Story | Client case study, personal insight |
| Thu | Contrarian | Challenge SEO orthodoxy |
| Fri | Engagement | Question, poll, hot take |

---

## CTA Options

- "DM me 'AUDIT' to see what ChatGPT says about your brand"
- "Comment 'INVISIBLE' and I'll check your brand's AI visibility"
- "Save this for when you realize your SEO isn't enough"
- "Follow for more on how AI is changing buying decisions"
- No CTA (let the content speak, build authority)

---

## Output Format

```markdown
# LinkedIn Post: [Topic]

**Type:** [Hook/Data/Framework/Story]
**Goal:** [What this achieves]

---

## Hook Tournament

1. [Hook option 1]
2. [Hook option 2]
3. [Hook option 3]
4. [Hook option 4]

**Winner:** [Which and why]

---

## Final Post

[The complete post, formatted for LinkedIn]

---

## Notes
- [Any context on timing, audience, follow-up]
```
