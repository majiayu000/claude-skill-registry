---
name: campaign-orchestrator
description: Orchestrates the full crowdfunding workflow phase-by-phase, ensuring each Skill runs in sequence with proper handoffs and validation gates.
---

# Crowdfunding Campaign Orchestrator

This Skill coordinates all other Skills into a structured, sequenced process from market understanding to continual interest. It enforces inputs/outputs, validates handoffs, and ensures clean progression.

## When to Use
Use this when launching or retrofitting a full campaign and you want a repeatable, end-to-end workflow that executes each phase in order with quality checks.

## Inputs
- [PRODUCT_INPUTS]: Name, price, overview
- [ALLOWED_SKILLS]: List of enabled Skills names

## Global Conventions
- All phase outputs must include a JSON handoff block with minimal keys: `meta`, `tokens`, or `handoff`.
- Output files should be created in their respective `templates/` folder defined by each Skill.
- The `raw-templates/` directory contains archived reference/inspiration materials only. Do not invoke those skills or use their outputs in the orchestrated flow.

## The Phases

### Part 1: Understanding the Market
1. Buyer Persona (`buyer-persona-generator`)
   - Output: `Buyer Persona/templates/persona-dossier.md`
   - JSON: `meta_project.persona_name`, `voice_samples`, `emotional_drivers`
   - Gate: If persona lists < 20 wants / < 20 anti-goals, iterate.
2. Competitor Summary (`competitor-analysis`)
   - Output: `competitor-analysis/templates/competitor-intelligence.md`
   - JSON: `weaknesses[]`, `specs{}`
   - Gate: Must include direct quotes for 1-star reviews.

### Part 2: Product Detailing
3. Detailed Product Description (`detailed-product-description`)
   - Output: `detailed-product-description/templates/detailed-product-description.md`
   - JSON: `product{ name, price }`, `specs{ dimensions, materials }`
4. Product Positioning Summary (`product-positioning-summary`)
   - Output: `product-positioning-summary/templates/product-positioning-summary.md`
   - JSON: `cbbe{ salience, performance, imagery, judgments, feelings, resonance }`
5. MDS (`mds-messaging-direction-summary`)
   - Output: `mds-messaging-direction-summary/templates/mds.md`
   - JSON: `handoff{ pitch, usp, objections, emotions }`
6. Voice and Tone (`voice-and-tone`)
   - Output: `voice-and-tone/templates/voice-and-tone.md`
   - JSON: `voice{ tones[], persona, culture, lingo, emotions[] }`

### Part 3: Crafting Compelling Copy
7. Campaign Page Copy (`campaign-page-copy`)
   - Output: `campaign-page-copy/templates/campaign-page-copy.md`
   - Gate: Must include all 30 persuasion steps.
8. Pre-Launch Ads Copy (`pre-launch-ads`)
   - Output: `pre-launch-ads/templates/ad-campaign-dossier.md`

### Part 4: Email Strategy
9. Welcome Email Sequence (`welcome-email-sequence`)
   - Output: `welcome-email-sequence/templates/welcome-email-sequence.md`
10. Pre-Launch Email Sequence (`pre-launch-email-sequence`)
   - Output: `pre-launch-email-sequence/templates/pre-launch-email-sequence.md`
11. Launch Email Sequence (`launch-email-sequence`)
   - Output: `launch-email-sequence/templates/launch-email-sequence.md`

### Part 5: Campaign Messaging
12. Campaign Page Copy (`campaign-page-copy`)
   - Output: `campaign-page-copy/templates/campaign-page-copy.md`
13. Campaign Video Script (`campaign-video-script`)
   - Output: `campaign-video-script/templates/campaign-video-script.md`

### Part 6: Continual Interest
14. Live Campaign Ads Copy (`live-campaign-ads`)
   - Output: `live-campaign-ads/templates/live-campaign-ads.md`
15. Press Release Copy (`press-release-copy`)
   - Output: `press-release-copy/templates/press-release-copy.md`

## Validation Gates
- Each phase verifies the presence of prior JSON keys before proceeding.
- If a gate fails, iterate the producing Skill with added constraints.
  - Part 1 requires:
    - Persona: `meta_project.persona_name`, `voice_samples[]`, `emotional_drivers[]`
    - Competitor: `market_gaps[]`, `verified_anxieties[]`
  - Part 2 requires:
    - Detailed Product: `product{ name, price }`, `specs{ dimensions, materials }`
    - Positioning: `cbbe{ salience, performance, imagery, judgments, feelings, resonance }`
    - MDS: `handoff{ pitch, usp, objections, emotions }`
    - Voice & Tone: `voice{ tones[], persona, culture, lingo, emotions[] }`
  - Part 3 requires:
    - Campaign Page: `meta{ product, brand }`
    - Pre-Launch Ads: presence of full sections in `ad-campaign-dossier.md`
  - Part 4 requires:
    - Welcome: `meta{ brand, product, founder }`, `links{ vip_group, preview }`
    - Pre-Launch: `schedule{ announcement, reminder, launch }`, `segments[]`, `links{ preview }`
    - Launch: `schedule{ day1_morning, day1_evening, day2_morning, day3_morning, day5_morning, day7_morning }`
  - Part 5 requires:
    - Campaign Page: `meta{ product, brand }`
    - Video Script: `timing.total_seconds`, `cta`
  - Part 6 requires:
    - Live Ads: `tokens{ funding_percent, backers, end_date, hours_left }`

## Output
Produce a phase-by-phase status in `templates/orchestrator.md` including links to completed outputs and a final JSON index for programmatic consumption.


## Integration & Technical Specs

### API Specification
- **ID**: `campaign-orchestrator`
- **Path**: `skills/campaign-orchestrator/templates/orchestrator.md`
- **Context**: Part of *Strategy & Management*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `orchestrator.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate campaign-orchestrator
```
