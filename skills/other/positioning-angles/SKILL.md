---
name: positioning-angles
description: >
  Find the angle that makes something sell. Use this skill whenever the user
  mentions positioning, angles, differentiation, unique selling proposition,
  'how do I stand out', 'what makes us different', value proposition, messaging
  framework, or 'find the hook'. Also trigger when copy isn't converting (often
  a positioning problem), when marketing feels generic, when launching a product,
  creating a lead magnet, writing a landing page, or entering a crowded market.
  Even if the user is about to write copy without established positioning, run
  this first — the angle informs everything downstream. Generates 3-5 positioning
  angles with competitive web research and validation.
---


## On Activation

1. Check if `brand/` directory exists in the project root.
2. If it does, read available files: `voice-profile.md`, `positioning.md`, `audience.md`, `creative-kit.md`, `stack.md`, `learnings.md`.
3. Apply any loaded brand context to enhance output quality.
4. If `brand/` does not exist, proceed without it — this skill works standalone.
5. Read `brand/landscape.md` if it exists — check the Claims Blacklist before making ecosystem or competitive claims. If stale (>14 days) or missing, warn that market claims may be outdated.

> **Note:** Examples below use fictional brands (Acme, Lumi, Helm). Replace with your own brand context.

# Positioning & Angles

The same product can sell 100x better with a different angle. Not a different product. Not better features. Just a different way of framing what it already does.

This skill finds those angles.

---

## Brand memory integration

**Reads:** `audience.md`, `competitors.md`, `voice-profile.md` (if they exist)

On invocation, check for `./brand/` and load available context:

1. **Check for `./brand/positioning.md`** -- if it exists, this is an update session:
   - Read the existing positioning file
   - Display the current primary angle and any saved alternatives
   - Ask: "You already have positioning on file. Do you want to refine it with fresh data, or start from scratch?"
   - "Refine" -- load existing angles, run competitive search for new data, suggest adjustments to current positioning based on what has changed in the market
   - "Start fresh" -- run the full process below as if no positioning exists

2. **Load `audience.md`** (if exists):
   - Use audience segments, pain points, and language patterns to inform angle generation
   - Show: "I see your audience profile -- [brief summary]. Using that to shape angles."

3. **Load `competitors.md`** (if exists):
   - Use known competitors as starting seeds for the competitive web search step
   - Show: "I found [N] competitors in your brand memory. Starting search from there."

4. **Load `voice-profile.md`** (if exists):
   - Use voice DNA to ensure angle language matches brand tone
   - Show: "Your voice is [tone summary]. Angles will match that register."

5. **If `./brand/` does not exist:**
   - Skip brand loading entirely. Do not error.
   - Note in opening message: "No brand profile found — this skill works standalone. I'll ask what I need. You can run /cmo or /brand-voice later to unlock personalization."

---

## The core job

When someone asks about positioning or angles, the goal is not to find THE answer. It is to surface **multiple powerful options** they can choose from.

Every product has several valid angles. The question is which one resonates most with the specific audience at the specific moment.

Output format: **3-5 distinct angle options**, numbered with circled numbers, each with:
- Statement (one sentence positioning)
- Psychology (why this works with this audience)
- Headline direction (how it would sound in copy)
- Best for (market conditions, audience segments)
- One option marked with ★ recommended

---

## The angle-finding process

### Step 1: Identify what they are actually selling

Not the product. The transformation.

Ask: What does the customer's life look like AFTER? What pain disappears? What capability appears? What status changes?

A fitness program does not sell workouts. It sells "fit into your old jeans" or "keep up with your kids" or "look good naked."

A SaaS tool does not sell features. It sells "close your laptop at 5pm" or "never lose a lead" or "stop the spreadsheet chaos."

**The transformation is the raw material for angles.**

---

### Step 2: Map the competitive landscape

What would customers do if this did not exist? Not competitors -- alternatives.

- Do nothing (live with the problem)
- DIY (cobble together a solution)
- Hire someone (consultant, freelancer, agency)
- Buy a different category (different approach entirely)
- Buy a direct competitor

Each alternative has weaknesses. Those weaknesses become angle opportunities.

**Angle opportunity:** What is frustrating about each alternative that this solves?

---

### Step 2.5: Competitive web search (live data)

Before generating angles, search the web for real competitor messaging. This grounds the angle work in current market reality rather than assumptions.

**Search process:**

1. **Identify search targets:**
   - If `./brand/competitors.md` exists, start with those competitor names and URLs
   - If the user named competitors, search those
   - Otherwise, search for "[product category] + [target market]" to find the top players

2. **Pull messaging data from competitor sites:**
   - Homepage headlines and hero copy
   - Taglines and value propositions
   - Key claims on feature/pricing pages
   - Social proof framing (how they present testimonials)
   - CTA language

3. **Map the landscape:**
   - What claims appear on 3+ competitor sites (saturated territory)
   - What angles only 1 competitor uses (partially claimed)
   - What angles NO competitor uses (white space)
   - What proof/mechanism language dominates the space

4. **Present findings as a competitive landscape map:**

```
──────────────────────────────────────────────────

  COMPETITIVE MESSAGING LANDSCAPE

──────────────────────────────────────────────────

  Competitors Analyzed
  ├── [Competitor 1] -- "[their headline]"
  ├── [Competitor 2] -- "[their headline]"
  ├── [Competitor 3] -- "[their headline]"
  └── [Competitor 4] -- "[their headline]"

  ──────────────────────────────────────────────

  Saturated Claims (everyone says this)
  ├── "[Claim 1]"
  ├── "[Claim 2]"
  └── "[Claim 3]"

  Partially Claimed (1-2 competitors)
  ├── "[Claim]" -- used by [Competitor]
  └── "[Claim]" -- used by [Competitor]

  Underexploited Territory
  ├── Nobody is talking about [gap 1]
  ├── The [specific angle] is wide open
  └── [Niche audience] has no champion

──────────────────────────────────────────────────
```

**Why this matters:** Angles built on white space outperform angles that echo the market. If every competitor says "all-in-one platform," that phrase is dead. The competitive search reveals what NOT to say and where opportunity lives.

**If web search is unavailable:**
1. Use `./brand/competitors.md` if it exists — extract messaging data from previous competitive intel.
2. If no competitors.md exists, ask the user to name 2-3 competitors and describe their positioning.
3. If no competitor data is available at all, skip the competitive landscape map and note the limitation: "Angles are not competitively grounded. Run /competitive-intel first for stronger differentiation."
4. Proceed to Step 3 with whatever context is available — the skill still works without competitive data, just at a lower enhancement level.

---

### Step 3: Find the unique mechanism

The mechanism is HOW the product delivers results differently.

Not "we help you lose weight" (that is the promise).
"We help you lose weight through intermittent fasting optimized for your metabolic type" (that is the mechanism).

The mechanism makes the promise believable. It answers: "Why will this work when other things have not?"

**Questions to surface the mechanism:**
- What is the proprietary process, method, or system?
- What do you do differently than the obvious approach?
- What is the counterintuitive insight that makes this work?
- What is the "secret" ingredient, step, or element?

Even if nothing is truly proprietary, there is always a mechanism. Name it.

### Step 3.5: Require structural proof

Before accepting an angle, run the structural-proof, perception-gap, economic-case, and buyer-risk checks in `references/structural-proof.md`. Label unsupported angles as messaging hypotheses rather than competitive claims.

---

### Step 4: Assess market sophistication

Where is the market on Schwartz's awareness scale?

**Stage 1 (New category):** The market has not seen this before.
  Angle: Simple announcement. "Now you can [do thing]."

**Stage 2 (Growing awareness):** Competition exists, market is warming.
  Angle: Claim superiority. "The fastest/easiest/most complete way to [outcome]."

**Stage 3 (Crowded):** Many players, similar claims, skepticism rising.
  Angle: Explain the mechanism. "Here is WHY this works when others do not."

**Stage 4 (Jaded):** Market has seen everything, needs new frame.
  Angle: Identity and belonging. "For people who [identity marker]."

**Stage 5 (Iconic):** Established leaders, brand loyalty matters.
  Angle: Exclusive access. "Join the [tribe/movement]."

**The market stage determines which angle TYPE will work.**

---

### Step 5: Run the angle generators

Now generate options using multiple frameworks. Each generator is a lens -- run the product through several and keep the 3-5 strongest options.

#### The Contrarian Angle
What does everyone in this market believe that might not be true?
Challenge that assumption directly.

> "Everything you've been told about [topic] is wrong."
> "Stop [common practice]. Here's what actually works."

Works when: Market is frustrated with conventional approaches. Audience sees themselves as independent thinkers.

#### The Unique Mechanism Angle
Lead with the HOW, not just the WHAT.
Name the proprietary process or insight.

> "The [Named Method] that [specific result]"
> "How [mechanism] lets you [outcome] without [usual sacrifice]"

Works when: Market is sophisticated (Stage 3+). Similar promises exist. Need to differentiate.

#### The Transformation Angle
Before and after. The gap between current state and desired state.

> "From [painful current state] to [desired outcome]"
> "Go from [specific bad metric] to [specific good metric] in [timeframe]"

Works when: The transformation is dramatic and specific. Market is problem-aware.

#### The Enemy Angle
Position against a common enemy (not a competitor -- a problem, a mindset, an obstacle).

> "Stop letting [enemy] steal your [valuable thing]"
> "The [enemy] is lying to you. Here's the truth."

Works when: Audience has shared frustrations. There is a clear villain to rally against.

#### The Speed/Ease Angle
Compress the time or reduce the effort.

> "[Outcome] in [surprisingly short time]"
> "[Outcome] without [expected sacrifice]"

Works when: Alternatives require significant time or effort. Speed/ease is genuinely differentiated.

#### The Specificity Angle
Get hyper-specific about who it is for or what it delivers.

> "For [very specific avatar] who want [very specific outcome]"
> "The [specific number] [specific things] that [specific result]"

Works when: Competing with generic offerings. Want to signal "this is built for YOU."

#### The Social Proof Angle
Lead with evidence, not claims.

> "[Specific result] for [number] [type of people]"
> "How [credible person/company] achieved [specific outcome]"

Works when: Have strong proof. Market is skeptical. Trust is the primary barrier.

#### The Risk Reversal Angle
Make the guarantee the headline.

> "[Outcome] or [dramatic consequence for seller]"
> "Try it for [time period]. [Specific guarantee]."

Works when: Risk is the primary objection. Confidence in delivery is high.

---

## Worked Example

**Product:** Acme (verified meal delivery)
**Market awareness:** Stage 2 (Problem-Aware)

**Top 3 angles generated:**

1. **Unique Mechanism** — 'The only delivery app with on-site source inspectors' (differentiator: human verification vs. self-reported labels)
2. **Enemy** — 'DoorDash calls it verified. We actually check.' (names the villain: unverified-source claims)
3. **Transformation** — 'From ingredient-checking every order to ordering with your eyes closed' (before/after emotional state)

**Recommended:** Angle 2 (Enemy) — creates urgency, names a known frustration, and positions Acme as the trusted alternative.

---

## Progressive Enhancement Levels

| Level | Context Available | Output Quality |
|-------|------------------|---------------|
| L0 | Product description only, no web search | 3-5 angles from frameworks, no competitive grounding |
| L1 | + audience.md | Audience-aware angles, pain-point-driven psychology |
| L2 | + competitors.md | Competitively grounded angles, gap-exploiting positioning |
| L3 | + web search for live competitive messaging | Real-time white space identification, verified saturated claims |
| L4 | + existing positioning.md (refinement) | Evolved angles with market shift tracking |

---

## Output format

All output uses the four required sections: Header, Content, Files Saved, What's Next.

### Header

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  POSITIONING ANGLES
  [Product/Offer Name]
  Generated [Month Day, Year]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Content: Competitive Landscape Map

Present the competitive search findings first (see Step 2.5 format above).

### Content: Market Assessment

```
  MARKET ASSESSMENT

  Sophistication: Stage [N] -- [stage name]
  Transformation: [one sentence]
  Mechanism: [the unique how]
  Structural proof: [why the promise is defensible, or "unproven hypothesis"]
  Perception gap: [internal vs customer vs operational mismatch]
  Primary alternative: [what they do instead]
```

### Content: Angle Options

Present 3-5 numbered angle options using circled numbers (①②③④⑤). Each option includes: Statement (one sentence), Psychology (why it works), Headline (example), Best for (conditions). Mark the strongest with ★ recommended, then explain why in 1-2 sentences. Ask: "Which angle resonates? Pick a number, or tell me to combine elements from multiple."

### Files Saved

After the user selects an angle, write to `./brand/positioning.md`:

```
  FILES SAVED

  ./brand/positioning.md             ✓
```

If the file already existed and was updated:

```
  FILES SAVED

  ./brand/positioning.md             ✓ (updated)
```

### What's Next

```
  WHAT'S NEXT

  Your positioning is set. Every downstream
  skill will use this angle. Recommended moves:

  → /direct-response-copy  Write copy with your
                           winning angle (~15 min)
  → /lead-magnet           Build a lead gen
                           asset (~10 min)
  → /keyword-research      Map your content
                           territory (~15 min)

  Or tell me what you're working on and
  I'll route you.
```

---

## File output protocol

When the user selects an angle, write `./brand/positioning.md` with: Last Updated date, Primary Positioning (angle name, statement, psychology, headline direction, best for), Competitive Landscape Summary (sophistication stage, saturated claims, white space), and All Angles Explored (statement + headline for each generated angle, marking the selected one).

If `./brand/positioning.md` already exists, show what will change ("Your current positioning focuses on X, the new version shifts to Y"), ask for confirmation, and only overwrite after explicit approval.

---

## 12-ad matrix seed (optional)

After the user selects an angle, offer to generate a 12-ad testing matrix: 4 hooks (direct statement, question, proof, contrarian) across 3 formats (static image, video, carousel). Each cell gets a unique ID for performance tracking.

> See references/ad-matrix-and-examples.md for the full matrix template, cell structure, and the complete Claude Skills Pack worked example.

---

## How this skill gets invoked

This skill activates when:
- User asks "how should I position X"
- User asks "what's the angle for X"
- User asks "why isn't this selling"
- User asks to "find the hook" or "make this stand out"
- User is about to write copy/landing page but has not established positioning
- Direct-response-copy skill needs an angle to write from
- Landing-page skill needs a core positioning to build around

When another skill needs an angle, run this first. The angle informs everything downstream.

---

## What this skill is NOT

This skill finds positioning and angles. It does NOT:
- Write the actual copy (that is direct-response-copy)
- Build the landing page structure (that is landing-page)
- Research the audience from scratch (assumes you know who you are selling to, or loads audience.md)
- Pick a single "right" answer (it gives options to choose from)
- Replace deep competitive intelligence (that is competitive-intel -- this does a messaging-focused scan)

The output is strategic direction, not finished marketing.

---

## The test

Before delivering angles, verify each one:

1. **Is it specific?** Vague angles ("better results") fail. Specific angles ("20 lbs in 6 weeks") convert.

2. **Is it differentiated?** Could a competitor claim the same thing? If yes, sharpen it. Cross-reference against the competitive landscape map -- if a competitor already says it, it fails this test.

3. **Is it believable?** Does the mechanism or proof support the claim?

4. **Is it relevant to THIS audience?** An angle that works for beginners fails for experts. If audience.md is loaded, verify alignment with known segments and pain points.

5. **Does it lead somewhere?** Can you imagine the headline, the landing page, the copy? If not, it is too abstract.

---

## Iteration and update mode

This section adds detail to the iteration path described in "Brand memory integration" step 1. When `./brand/positioning.md` already exists, display current primary angle and offer: "Refine this, or start fresh?"

**Refine mode:** Load existing angles, run fresh competitive web search, compare new landscape to saved landscape, identify shifts (new competitors, new saturated claims, new white space), and suggest specific adjustments. Present 1-3 refined variations alongside the original. Let the user choose to keep, tweak, or replace.

**Start fresh mode:** Run the complete process from Step 1. Previous positioning.md is preserved until the user explicitly confirms the replacement.

---

## Feedback collection

After delivering the final angle selection and writing to positioning.md, run the 4-option feedback prompt in `references/feedback-collection.md` and log (a)/(b)/(c) outcomes to `./brand/learnings.md` as described there.

---

## References

For deeper frameworks, see the `references/` folder:
- `dunford-positioning.md` -- April Dunford's 5-component positioning methodology
- `schwartz-sophistication.md` -- Eugene Schwartz's market awareness levels
- `unique-mechanism.md` -- How to find and name your mechanism
- `angle-frameworks.md` -- Halbert, Ogilvy, Hopkins, Bencivenga, Kennedy approaches
- `hormozi-offer.md` -- Value equation and Grand Slam Offer thinking
- `ad-matrix-and-examples.md` -- 12-ad testing matrix template and full Claude Skills Pack worked example
- `feedback-collection.md` -- post-delivery feedback prompt and learnings.md logging rules
