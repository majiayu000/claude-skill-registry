# Guide Structure — NamingGuide Reference

Naming system patterns, tier structures, and how to match them to company type.

---

## Naming System Patterns

### Pattern 1: Standalone Brand (Apple model)

Each product is a standalone brand. Features are descriptive. No prefix.

**Structure:**
- Company: Apple
- Products: iPhone, iPad, Mac, Apple Watch (note: Apple prefix added late, after brand confusion)
- Features: FaceTime, Siri, AirDrop — branded features get their own names
- Releases: codenames internally, version numbers publicly

**When to use:**
- Company with multiple distinct product lines
- Each product serves a different audience or category
- Company brand is strong enough to confer trust without prefix

**Naming rule:** Products need standalone strength. Features deserve names only when users will talk about them by name.

---

### Pattern 2: Brand-Prefix Constellation (Stripe model)

Products expand outward from core brand with compound names.

**Structure:**
- Core: Stripe
- Products: Stripe Atlas, Stripe Radar, Stripe Issuing, Stripe Treasury
- Features: unnamed or described within the product

**When to use:**
- Company with one core product and expanding platform features
- B2B / enterprise context where brand authority matters in sales
- Products that are genuinely distinct but serve the same audience

**Naming rule:** Second word should be a strong standalone word (Atlas, Radar) not a descriptor (StripeAnalytics = bad).

**Pitfall:** Prefix exhaustion. If every product is [Brand] + [word], the brand becomes noise. Limit to 5-7 products before reconsidering.

---

### Pattern 3: Ecosystem Umbrella (Notion model)

Everything lives under one brand. Features are described, not named. Consistency over personality.

**Structure:**
- Core: Notion
- Features: Notion AI, Notion Calendar, Notion Forms — functional compounds
- No sub-brands or standalone product names

**When to use:**
- Single-product company with expanding features
- Audience expects consistency and predictability
- Brand equity is strong enough that sub-branding would dilute it

**Naming rule:** Functional clarity over brand personality at the feature level. Reserve branded names for major platform pivots.

---

### Pattern 4: Codename Releases (macOS model)

Releases get creative codenames. Products stay clean.

**Structure:**
- Product: macOS
- Releases: Ventura, Monterey, Sonoma — geographic/thematic codenames
- Features: Stage Manager, Focus Mode — descriptive

**When to use:**
- Regular release cadence that needs narrative (annual releases, major versions)
- Team culture values the ritual of naming releases
- Audience will remember releases by name (enthusiast community)

**Naming rule:** Codenames should come from a consistent theme (Apple: California locations). Pick the theme and commit to it for 5+ releases minimum.

---

### Pattern 5: Open Tier (GitHub / Linear model)

Minimal naming system. Brand + product descriptions. Let the work speak.

**Structure:**
- GitHub: Issues, Pull Requests, Actions, Copilot (the one exception — AI gets a name)
- Linear: Issues, Projects, Cycles, Roadmaps — all descriptive

**When to use:**
- Developer tools where users value precision over brand personality
- Products where descriptive names aid discoverability and onboarding
- Teams that want to ship fast without naming debates

**Naming rule:** Only name something when it's genuinely new — when no existing word captures it. Default to the best descriptive name.

---

## Tier Definition Reference

### Product Tier
The highest-level named thing. Carries full brand weight.
- Naming intensity: HIGH — invest time here
- Style: invented or modified real word preferred
- Length: 4-8 characters ideal
- Domain: should own the domain

### Feature Tier
A capability within a product. Named only when users will refer to it by name.
**The question to ask:** "Will a user say 'I used [feature name] to do X' or will they say 'I used the [description] in [product]'?"
- Named features: Siri, AirDrop, FaceTime, Stripe Radar
- Unnamed features: file export, user permissions, notification settings
- Naming intensity: SELECTIVE — only when the feature has brand moment potential
- Style: can be more descriptive than product names; concept/metaphor works well

### Release Tier
Time-based versions. Named only if release cadence is regular and team culture supports it.
- Naming intensity: LOW-MEDIUM — fun but not mission-critical
- Style: pick a theme and commit (geography, mythology, animals, etc.)
- Number: always also use a version number; codenames are supplementary

### Sub-brand Tier
A distinct product that serves a meaningfully different audience or market.
- Naming intensity: HIGH — treat like a new brand
- Must pass the standalone test: would this name work without the parent brand?
- Visual identity: can deviate from parent, but should be related

---

## Audience-Specific Naming Conventions

**Developer audience:**
- Short, lowercase-friendly names work (bun, nx, vite)
- Technical precision valued over warmth
- GitHub org name as important as domain
- Feature names can be more technical

**Consumer audience:**
- Warmth and approachability required
- Avoid jargon, acronyms, or overly technical constructions
- Names should work as verbs ("I'll [name] it")
- Feature names should feel intuitive, not technical

**Enterprise audience:**
- Clarity and credibility over cleverness
- Avoid names that sound like consumer apps
- Sub-brands and product families need clear hierarchy
- Acronyms acceptable at enterprise scale (but risky pre-scale)

**SMB / prosumer audience:**
- Balance of approachability and professionalism
- Avoid names that are too consumer (feels unserious) or too enterprise (feels intimidating)
- Feature names should be self-explanatory on first encounter
