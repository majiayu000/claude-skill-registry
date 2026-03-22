---
name: pitch-experience-generator
description: Generate immersive, scrollytelling investor pitch experiences with glassmorphism UI, animated text effects, and parallel research agents. Use when users request pitch decks, investor presentations, business plan artifacts, or fundraising materials. Outputs IDE-ready project scaffolding (Overview.md, DesignSpec.md, Tasks.md) plus a React artifact preview. Leverages web search for market research and extended thinking for narrative strategy.
---

# Pitch Experience Generator

Create immersive, scrollytelling investor pitch experiences that transform static pitch decks into animated, narrative-driven web experiences.

## Outputs

### Primary: IDE Project Scaffolding
```
{company-name}-pitch/
├── Overview.md                    # Executive summary, narrative arc, emotional journey
├── DesignSpec.md                  # Complete design system, component specs, animations
├── Tasks.md                       # Step-by-step build checklist
├── research/
│   ├── market-intelligence.md    # TAM/SAM/SOM with sources
│   └── competitor-analysis.md    # Competitive landscape
├── content/
│   ├── narrative-arc.md          # Story structure
│   └── copy-blocks.md            # All text by section
└── design/
    └── tokens.css                # CSS variables
```

### Secondary: Interactive React Artifact
Simplified but functional preview viewable in Claude with hero, key sections, and animations.

## Workflow

### Step 1: Gather Inputs

**Required:**
- Company/Product name
- One-sentence pitch
- Problem being solved
- Target customer
- Stage: `idea | mvp | revenue | scaling`
- Traction highlights
- Funding ask + use of funds
- Team highlights

**Optional (from project knowledge):**
- Existing pitch materials
- Competitor names
- Target investor profile

### Step 2: Industry Detection

Analyze inputs and confirm with user:

| Industry | Signals | Focus |
|----------|---------|-------|
| B2B SaaS | "enterprise", "platform", "ARR" | CAC/LTV, NRR, logos |
| Consumer | "app", "users", "viral" | DAU/MAU, retention |
| Marketplace | "buyers", "sellers", "GMV" | Take rate, liquidity |
| Fintech | "payments", "lending" | Regulatory, trust |
| Hardware | "device", "units" | BOM, margins |
| DeepTech | "AI", "research", "patent" | IP, team, partnerships |
| Healthcare | "patients", "clinical" | Regulatory, outcomes |

**Confirm:** "This appears to be [Industry]. Optimize for [Industry] investors?"

### Step 3: Parallel Research

Execute three parallel research threads:

#### Thread 1: Market Intelligence (5 searches)
```
"[industry] market size TAM 2024"
"[industry] growth rate CAGR"
"[vertical] market trends"
"[industry] venture funding 2024"
"[geography] [industry] opportunity"
```
→ Output: `research/market-intelligence.md`

#### Thread 2: Competitive Landscape (5 searches)
```
"[competitor] funding valuation"
"[competitors] comparison"
"[industry] startup landscape"
"[problem] solutions comparison"
"[industry] competitive analysis"
```
→ Output: `research/competitor-analysis.md`

#### Thread 3: Narrative Strategy (Extended Thinking)
Synthesize without searching:
- Optimal story arc
- Emotional journey map
- Key proof points
- Objection rebuttals
→ Feeds into `Overview.md`

### Step 4: Generate Files

Follow templates in `references/output-templates.md`.
Apply design system from `references/design-system.md`.
Use components from `references/component-library.md`.

### Step 5: React Artifact Preview

Generate simplified artifact with:
- Hero (TextType + gradient background)
- 2-3 sections with GlassCards
- Animated metrics
- Scroll reveals

## Section Structure

10-section narrative journey:

| # | Section | Emotion | Components |
|---|---------|---------|------------|
| 1 | Hero | Intrigue | TextType, CircularText |
| 2 | Problem | Pain | GlassCards, stats |
| 3 | Solution | Relief | Product reveal |
| 4 | Traction | Trust | AnimatedCounter, logos |
| 5 | Market | Excitement | TAM circles, chart |
| 6 | Model | Confidence | Revenue viz |
| 7 | Competition | Clarity | Position matrix |
| 8 | Team | Credibility | Team cards |
| 9 | Roadmap | Belief | ProgressStepper |
| 10 | Ask | Action | Terms, CTA |

## IDE Build Spec

```yaml
package_manager: bun
framework: react (vite)
dependencies:
  - framer-motion
  - gsap  
  - lucide-react
  - recharts
  - tailwindcss
components: ReactBits patterns
```

## Quality Gates

- [ ] All 10 sections populated
- [ ] Market data has sources
- [ ] Financials reasonable for stage
- [ ] Design tokens exact
- [ ] Artifact renders clean
- [ ] Narrative has emotional arc
