---
name: authentic-product-representation
description: Product visuals — hero shots, demos, screenshots, landing-page panels — must reproduce the real product, not a stylised poster of it. Design with real content and real data, mirror the actual output the product generates, keep every label and number truthful, and refuse fabricated marketing chrome. Use when building landing pages, hero sections, product screenshots, demo panels, or any visual that stands in for the real thing.
metadata:
  priority: 7
  pathPatterns:
    - "app/**"
    - "src/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.html"
    - "**/page.tsx"
    - "**/hero*"
    - "marketing/**"
    - "landing/**"
  promptSignals:
    phrases:
      - "hero section"
      - "landing page"
      - "product screenshot"
      - "screenshot in the hero"
      - "product shot"
      - "mockup"
      - "demo panel"
      - "fake data"
      - "placeholder data"
      - "lorem ipsum"
      - "marketing visual"
      - "make it look impressive"
retrieval:
  aliases:
    - authentic product representation
    - honest product visuals
    - design with real data
    - real content not lorem ipsum
    - credible hero
    - product screenshot
    - anti AI-slop
    - show the real thing
  intents:
    - make this hero credible
    - show the real product output
    - replace the fake screenshot with something real
    - use real data in this mockup
    - this looks AI-generated, make it authentic
  examples:
    - this hero looks fake, make it credible
    - replace the lorem ipsum with real content
    - the demo panel should show what the product actually outputs
    - this screenshot is invented, base it on the real thing
    - the landing visual looks AI-generated
---

# Authentic Product Representation

The fastest way to lose a visitor's trust is a product visual that is obviously staged. People have seen thousands of landing pages; they recognise a fabricated dashboard, a screenshot full of lorem ipsum, or a "terminal" that prints things the real tool never would. The visual that converts is the one that looks like it was screenshotted straight out of the working product — because it was, or because it was built to be indistinguishable from it.

The principle is simple: **the visual is the product, not a poster of it.** Every shortcut away from that — invented data, decorative chrome, a capability shown that does not exist — is a small withdrawal from the trust account.

---

## Design With Real Content

Idealised placeholder content hides the problems your design will actually face.

- **No lorem ipsum.** Use real copy, or the closest draft of it. Real words have real lengths, real line-wraps, real awkward edge cases. Latin filler is uniformly tidy in a way your content never will be.
- **Real names, real numbers, real lengths.** "John Smith / $1,234" is a fantasy dataset. Use the longest realistic name, the account with 0 items, the title that wraps to three lines. If the design only looks good with perfect data, it is not finished.
- **Design the empty, loading, error, and overflow states too** — they are the product as much as the happy path. A screenshot that only ever shows the full, perfect state is selling a product that does not exist.

If you genuinely cannot use production data, generate the mock **from the real schema and the real renderer**, so its shape, formatting, and constraints match what ships.

---

## Mirror the Real Output

When a visual stands in for what the product produces — a CLI run, a generated file, a report, a chart, an editor — reproduce the **actual format**, not a prettier reinterpretation.

- Use the product's real output structure: the same labels, the same ordering, the same tree/log/table shape, the same truncation rules ("+4 more").
- Pull the values from a real run where possible. If the visual claims to process `yourdomain.com`, show what processing `yourdomain.com` actually yields — not another site's values relabelled.
- Reuse the real rendering component if one exists. A faithful embed beats a hand-built lookalike that drifts from reality the moment the product changes.
- Breadth is more convincing shown than claimed. Listing the real categories the tool already covers ("also: borders, shadows, motion, components") communicates scope truthfully; a "coming soon" teaser for things that already exist communicates the opposite.

A reinterpreted mock is a maintenance liability and a credibility risk: it looks like the product until someone compares it to the product.

---

## Keep It Truthful

The visual makes claims. Every one must hold.

- **Numbers reflect reality.** Stats, counts, and metrics are real or clearly illustrative — never inflated fiction presented as fact.
- **Labels match content.** Do not relabel one thing as another (a screenshot of system A captioned as system B; a domain in the command that does not match the results shown).
- **Show only real capabilities.** A demo that performs a feature the product does not have is a promise you will break on first use.
- **"Soon" means soon, and rarely earns its place.** A pending/soon badge on something that already ships is a lie; a pending badge on a real roadmap item is usually just noise in a product shot. Prefer showing what works.

---

## Refuse Fabricated Marketing Chrome

A recognisable visual dialect signals "generated to look impressive" rather than "screenshotted from a real product." It reads as AI-slop and erodes the authenticity you are trying to build.

Avoid:
- Invented dashboards, fake charts, and decorative "terminals" that print marketing copy
- Gradient-filled text, sparkle/star accents, aurora glows, and glassmorphism used as a substitute for substance
- Typewriter/rotator headlines and faux-AI chrome (scanning lines, "thinking" shimmers) with no real function
- Pill badges and ornaments that exist only to fill space, especially in places where they clash with the medium (e.g. a label chip dropped into monospace output)

The restraint test: if an element does not exist in the real product, it does not belong in a visual that represents the real product. Decoration that carries no information is the first thing to cut.

---

## When You Must Stage

Sometimes a literal screenshot is impossible (pre-launch, sensitive data, a composite view). Stage honestly:

- Build from the real schema, the real component, and realistic values.
- Match the product's real states and formatting, including the unglamorous ones.
- Keep claims conservative — under-promise in the visual, let the product over-deliver.
- Label clearly illustrative figures as such rather than passing them off as measured.

---

## Review Checklist

- [ ] Is there any lorem ipsum or obviously idealised placeholder content left? (There should be none.)
- [ ] Does the content use realistic lengths — the long name, the empty list, the three-line title?
- [ ] Are the empty, loading, error, and overflow states represented, not just the perfect state?
- [ ] When the visual stands in for product output, does it match the real format, ordering, and truncation?
- [ ] Do the values correspond to the input shown (right domain, right source), not another case relabelled?
- [ ] Is the real rendering component reused where one exists, instead of a hand-built lookalike?
- [ ] Are all numbers, labels, and capabilities truthful — nothing inflated, mislabelled, or not-yet-real?
- [ ] Is there any "coming soon" framing on things that already ship?
- [ ] Is there fabricated marketing chrome (fake dashboards, gradient text, sparkles, decorative terminals) that should be cut?
- [ ] Could a visitor screenshot the real product and get the same impression this visual gives? If not, why not?
