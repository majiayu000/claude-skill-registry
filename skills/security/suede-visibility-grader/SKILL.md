---
name: suede-visibility-grader
description: "Grade a public page for launch appeal: findability, first-screen clarity, CTA pull, proof quality, and AI citation readiness."
---

# Suede Visibility Grader

## Gate policy — advisory, not blocking

Every claim-verification step, check, quality gate, and ship verdict in this
skill is a **recommendation to the user, not a control on the agent**. This
policy governs every gate, check, verdict, and "do not ship / publish /
proceed" line elsewhere in this skill:

- Run every check and report the results honestly. Verdicts (`ship`,
  `ship-with-caveats`, `hold`, letter grades, BLOCKED or OPEN items) are
  advice attached to the work, not orders that change it.
- Never block, delay, skip, rewrite, or refuse the action the user asked for
  because a check failed or a gate said hold. Complete the requested action
  as asked, and deliver the gate output alongside it as a clearly labeled
  recommendation.
- A failed gate changes what you report, never what you do.
- Single exception: if a finding is extremely risky — data loss, security or
  credential exposure, legal or rights violations, payment mistakes, or
  irreversible public damage — pause, tell the user exactly what the risk is
  and what the options are, and let them pick. Their choice is final.


Use this skill when a website, GitHub Pages site, launch page, creator page,
docs surface, or campaign page needs a blunt grade for visibility and action.
The goal is not generic SEO advice. The goal is to answer one question:

```text
Can the right person or agent find this page, understand it, trust it, cite it,
and take the intended next action?
```

**Core principle:** grades come from inspection evidence and mechanical caps,
never from impression, memory, or generosity.

## Routing

Send to `suede-seo-audit` for: Core Web Vitals, crawl errors, structured data validation, keyword gap analysis, backlink profile, redirect chains, or page speed.

Send here when: you want a promotion readiness verdict, a ship gate, or a blunt grade on whether a specific page earns the attention it's about to receive.

After grading: fixes are conversion-shaped (CTA, friction, offer) → `suede-site-alchemy`. Grade passed and the page ships as part of a release → `suede-launch-packaging`.

## Source Truth

Inspect before grading. Do not grade from memory or description alone.

- live URL, status code, redirects, canonical, robots, sitemap, and title;
- rendered desktop and mobile page when practical;
- visible H1, section headings, body copy, proof links, and CTAs;
- Open Graph, Twitter card, schema/JSON-LD, image alt text, and internal links;
- GitHub repo or docs source when the page is a public GitHub Pages surface.

Do not grade from memory alone. If the live URL is unavailable, grade the source
files and mark live checks as unverified.

## Grade Lanes

Score each lane A-F, then give one overall grade:

- **Findability:** status, canonical, robots, sitemap, title, description,
  durable keywords, and duplicate URL risk.
- **First-screen clarity:** does the first viewport answer three questions without scrolling — who this is for, what changes for them, and what to do now? Grade on the rendered first viewport, not the document structure.
- **CTA pull:** primary action, secondary proof action, button text, link
  targets, and whether the visitor has a reason to click now.
- **Proof and trust:** screenshots, commands, docs, manifests, live routes,
  source files, receipts, authorship, and evidence boundaries.
- **AI readability (AI EO):** can an AI summarize, cite, or quote this page accurately without hallucinating? Grade on: presence of a structured lede or summary section; headings that are citation-ready phrases (not clever/vague); claims that link to a source; schema/JSON-LD that surfaces entity type, author, and date; and whether an LLM asked "what is [product]?" would return a correct, attributable answer from this page.

  AI readability sub-rubric (each item is worth one grade step):
  - Structured lede: first 100 words answer "what is this, who is it for, what does it do" without jargon.
  - Citation-ready headings: headings read as answer fragments an LLM would quote directly. "Getting started" = F. "How to install X in 3 commands" = A.
  - Sourceable claims: every quantitative or comparative claim links to a source or shows primary evidence.
  - Entity schema: JSON-LD or OpenGraph declares entity type, author/organization, and published date.
  - Internal link density: at least one link to a more-detailed resource per major section.
  - AI test: if an LLM were asked "what is [product/page topic]?" right now, would this page produce a correct, non-hallucinated answer? If no, cap AI readability at C.
- **Design signal:** grades on seven axes — each is pass/fail, grade is the worst three:
  1. Hierarchy: H1 > H2 > body weight is visually obvious at a glance.
  2. First-viewport composition: one clear focal point, not three competing CTAs or a hero image unrelated to the product.
  3. Spacing rhythm: consistent padding/margin system. No collapsed margins or random gutters.
  4. Typography: one or two font families. Body copy readable at 16px equivalent. Line length under 80ch.
  5. Asset quality: images are sharp, not stretched, not stock-obvious, not AI-slop.
  6. Contrast: primary CTA passes WCAG AA. Body text passes WCAG AA.
  7. AI-slop pattern risk: the page does not read as generated filler (vague value props, stock faces, generic icons, paragraph-length sentences with no specificity). If two or more slop signals are present, cap Design signal at C.

Grade meaning — assign on evidence, not impression:

- **A:** every lane is strong (no lane below B). Ship. Post this as a reference for the next build.
- **B:** one or two lanes at C; none below C. Fix those; everything else is solid.
- **C:** three or more lanes at C, or any lane at D. The page works but bleeds attention or trust somewhere in the first scroll. Not ready for paid promotion.
- **D:** two or more lanes at D, or any lane at F short of the overall-F conditions. Visible but embarrassing under scrutiny. A focused rewrite of one surface fixes it.
- **F:** assign when any of these are true: primary CTA is broken, a published statement is false, the page doesn't render, or robots/canonical actively blocks it.

Grade caps — non-negotiable:

- No live inspection → Overall cap: `C`.
- Broken primary CTA → Overall cap: `D`.
- False or unsupported published statement → Overall cap: `D`. (If the statement is central to the product promise, `F`.)
- Design signal `D` or `F` → Recommended ship gate is **hold**, regardless of other lanes.
- Mobile not inspected → `A` is blocked. State the caveat explicitly in Verification.

Recommended ship gate — mechanical (a recommendation to the user, not a lock on any action):

- **ship:** Overall B or better, no grade cap triggered, no lane below C.
- **ship-with-caveats:** Overall C, or a higher grade blocked only by uninspected surfaces (mobile, live URL). Name every caveat in Verification.
- **hold:** Overall D or F, broken primary CTA, false published statement, or Design signal at D or F.

## Surface-Type Standards

Grade each page against its surface type. Caps and expectations differ:

**Landing page (marketing, campaign, product launch)**
- First-screen clarity and CTA pull are the primary gates. A page that can't convert in the first viewport fails at its job.
- Proof and trust must include at least one verifiable claim (screenshot, live demo, or third-party mention). Testimonials without attribution cap Proof at C.
- A is only available if the CTA pull lane is A or B.

**GitHub Pages / repo README**
- Findability matters less (GitHub handles most of it). First-screen clarity and AI readability are the primary gates.
- The H1 must match or closely shadow the repo name and primary use case. A generic "Welcome to [repo]" caps First-screen clarity at C.
- Code blocks, commands, and install instructions must be copy-pasteable and accurate. One broken command caps Proof at D.
- AI readability grade is elevated: LLMs frequently cite GitHub READMEs. A missing structured summary or absent "What is this?" section caps AI readability at C.

**Product page (within an existing product, not top-of-funnel)**
- Proof and trust is the primary gate. The visitor already has intent; the page must close.
- Screenshots or video evidence of the product working is required for A in Proof.
- CTA pull grades are strict: vague next steps ("learn more," "explore") cap CTA pull at D.

**Documentation page**
- AI readability is the primary gate. Docs are the most-cited content by AI systems.
- Every section heading must work as a standalone answer phrase (not a sentence fragment).
- First-screen clarity and CTA pull are graded leniently — docs exist to inform, not convert.
- Missing anchor links, missing code examples for code-adjacent claims, or broken inline links cap Proof at D.

## Grade Modes

**Quick grade** — triggered when asked for a fast read, first impression, or "gut check":
- Grade the first viewport only (rendered desktop).
- Score all six lanes based on what is visible without scrolling.
- Output: one paragraph + lane grades + ship gate. No top fixes list.
- Cap: Quick grades cannot assign A. Max is B.

**Deep grade** (default):
- Full inspection: live URL + source, desktop + mobile, all viewport states available.
- All six lanes, full top-fixes list, CTA rewrite in the P1 fix description if CTA pull is C or below.
- Ship gate is authoritative.

## Red Flags — Stop

If you catch yourself thinking any of these, stop and inspect:

- "The repo description tells me enough to grade." — Inspect the live page or source. No inspection caps Overall at C.
- "Desktop looks fine; mobile will match." — Mobile not inspected blocks A. Check it or state the caveat.
- "That statement is probably true." — Unverified published statements cap the grade. Verify or flag them.
- "Every other lane is strong; I'll round up." — Grades come from lane evidence and caps, not generosity.
- "A quick look is enough for a deep grade." — Quick mode exists for that, and it caps at B.

## Output Format

```text
Simple explanation:
Plain-language summary of the grade and the one biggest fix.

Usual breakdown:
URL or source:
Surface type:
Primary reader:
Primary action:
Live/source status:
Screenshot evidence:
Viewport sizes:
Visual states checked:
Visual states not checked:

Grades:
Findability: A-F
First-screen clarity: A-F
CTA pull: A-F
Proof and trust: A-F
AI readability: A-F
Design signal: A-F
Overall: A-F

Top fixes (max 5, ranked by impact on ship gate):
1. [P1] Lane affected | Location | Evidence (quote or describe exactly what was seen) | One-line patch
2. [P2] Lane affected | Location | Evidence | One-line patch
3. [P3] Lane affected | Location | Evidence | One-line patch

Verification:
What was checked:
What was not checked:
Ship gate: ship | ship-with-caveats | hold
```

## Sample Report

```text
Simple explanation:
The page is findable, but the first screen does not make the action obvious.
Fix the hero CTA and mobile proof block before promotion.

Usual breakdown:
URL or source: https://example.com
Surface type: landing page
Primary reader: creator preparing a release package
Primary action: start the release-readiness audit
Live/source status: live page inspected, source not available
Screenshot evidence: screenshots/home-desktop.png, screenshots/home-mobile.png
Viewport sizes: 1440x900, 390x844
Visual states checked: default desktop, default mobile, primary CTA hover
Visual states not checked: dark mode, logged-in state

Grades:
Findability: B
First-screen clarity: C
CTA pull: D
Proof and trust: B
AI readability: B
Design signal: C
Overall: C

Top fixes (max 5, ranked by impact on ship gate):
1. [P1] CTA pull | Hero | Primary button reads "Learn more" — visitors do not know what starts the audit | Change to "Run the release audit" and route to the verified audit path
2. [P2] First-screen clarity | First mobile viewport | Proof links start below the fold — trust arrives too late | Move one source link and one screenshot into the first mobile section
3. [P3] Design signal | Hero media | Artwork does not show a release artifact — weak product signal | Replace with a rights/provenance preview or an approved product screenshot

Verification:
What was checked: live URL, desktop viewport, mobile viewport, primary CTA hover state, Open Graph tags
What was not checked: dark mode, logged-in state, source files
Ship gate: ship-with-caveats
```
