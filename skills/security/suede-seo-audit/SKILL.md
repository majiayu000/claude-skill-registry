---
name: suede-seo-audit
description: "Run a nine-lane evidence-based SEO and generative-search audit: access, intent, metadata, structure, supported schema, E-E-A-T, clusters, and exact rewrite fixes."
---

# Suede SEO Audit

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


This skill goes deeper than an inline copy audit. It inspects live page source,
validates schema, traces crawl access, checks whether content can be understood
and sourced accurately, and produces exact rewrites with a lane-by-lane grade.
Use suede-copy for writing new copy. Use this skill when the audit itself is the
deliverable.

**Core principle:** never audit from memory. Every finding cites what was
actually fetched, and every fix is written out literally, not described.

---

## 1. Source Truth

Do not audit from memory. Before writing a single finding, verify the live
surface.

### Required pre-audit checks

- HTTP status code (200, 301, 404, 503): note exact code
- Final URL after all redirects (is the canonical URL the destination?)
- `robots.txt`: is the path allowed? Is `Disallow: /` blocking indexers?
- `<meta name="robots">` or `<meta name="googlebot">`: noindex? nofollow?
- `<link rel="canonical">`: does it match the intended URL exactly?
- Sitemap evidence: if the site publishes sitemaps, is the URL present and is
  any `<lastmod>` value accurate? Absence is not an automatic indexing failure.
- `<title>` tag: exact text, character count
- `<meta name="description">`: exact text, character count
- Open Graph tags: og:title, og:description, og:image, og:url, og:type
- Twitter card tags: twitter:card, twitter:title, twitter:description,
  twitter:image
- JSON-LD presence: any `<script type="application/ld+json">` block present?
- Primary H1: exact text, position in document

If the URL is inaccessible, note that and audit from source files with caveats.
If the page is behind auth or a paywall, say so and limit the audit to what is
accessible.

---

## 2. Audit Lanes

Run all lanes. Score each A-F at the end. State explicitly when a check was
skipped and why. The detailed per-lane checklists live in this skill's
`references/` folder — read the relevant file when you run the lane:

| Lanes | Checklist file |
|---|---|
| Lane 0 (keyword research, optional) | `references/keyword-research.md` |
| Lanes 1–4, 6–9 | `references/lane-checklists.md` |
| Lane 5 (schema) | `references/schema-templates.md` |

Before applying Google-specific search, generative-search, title/snippet, or
structured-data rules, read `references/google-search-guidance.md`. It contains
the primary-source baseline verified on 2026-07-19 and tells you which volatile
rules to re-check before a ship decision.

### Lane 0: Keyword Research (optional mode)

Activate when keyword discovery is requested; skip for technical-only or
copy-only audits. When active, read `references/keyword-research.md` for the
full protocol: evidence-backed query themes, related topics and entities,
competitor content gaps, supported search-feature eligibility, and the content
brief. Numeric demand stays `unknown` unless a dated source provides it.

Lane 0 is informational only. It produces a keyword brief and content brief,
not a grade. Incorporate the brief into Lanes 2–7 findings where relevant.

### Lane 1: Technical Access

**Goal:** confirm that search crawlers and other explicitly tested clients can
reach and parse the page. Do not assume that one crawler's access policy or
behavior represents another's. Run the Lane 1 checklist in
`references/lane-checklists.md`: status, redirects, canonical, robots, sitemap,
JS-free rendering, and the Core Web Vitals measurement protocol. Measure CWV
when tooling allows (PageSpeed Insights at pagespeed.web.dev; `curl` time is a
server-response proxy only); otherwise report each vital as "not measurable"
with the reason plus observed risk factors. Do not invent scores; do report
observable risks. CWV never enters the A-F grade.

Lane 1 grade drops to C or below if: an actual indexability block is present,
the canonical is wrong, redirects fail, or primary content is absent from the
tested rendered result. JavaScript use alone is not a failure.

### Lane 2: Search and Answer Intent

**Goal:** confirm the page has a single coherent intent that matches real
queries and can earn a featured snippet or AI citation. Run the Lane 2
checklist in `references/lane-checklists.md`: primary reader, primary query
theme, the AI-answer-ready definition, one earned action, and cannibalization.
Treat the opening-section definition as a Suede editorial clarity diagnostic,
not a Google ranking requirement. If a concise answer cannot be constructed
from the opening section, report the ambiguity and its reader impact.

Lane 2 grade drops to C or below if: the page has no clear primary reader, the
intent conflicts with the title, or the opening section answers a different
question than the URL implies.

### Lane 3: Metadata

**Goal:** metadata is accurate, descriptive, and useful in search results and
social previews. Character counts are preview diagnostics because Google has
no fixed title or meta-description character limit and may generate different
title links or snippets. Run the Lane 3 checklist in
`references/lane-checklists.md`: title tag, meta description, Open Graph,
Twitter/X card, alt text, author entity, and durable entity names.

Lane 3 grade drops to D or below if: the title is missing or misleading, the
meta description is missing on a priority landing page, required social preview
assets are broken, or the page's entity cannot be identified from the title,
description, and H1 together. Length alone never causes a grade drop.

### Lane 4: Structure

**Goal:** the page's hierarchy, section order, internal links, and terminology
serve the reader's intent. Run the Lane 4 checklist in
`references/lane-checklists.md`: headings, reader-driven section coverage,
links, optional FAQ quality, and natural topic/entity coverage. Do not apply a
universal page template, word count, or keyword-density quota.

Lane 4 grade drops to C or below if: H1 is missing, the page omits information
required to satisfy its primary reader intent, or internal links use
non-descriptive anchor text throughout. Missing an exact-match phrase is not a
failure when the page clearly covers the subject with natural language.

### Lane 5: Schema Markup

**Goal:** decide whether structured data is warranted, then ensure every JSON-LD
block is valid, eligible for its stated search feature, and matches visible
content. Run the Lane 5 checklist in
`references/schema-templates.md`, which also holds the page-type → `@type`
mapping and minimum JSON-LD templates (Organization, SoftwareApplication,
FAQPage, Article).

When schema is missing or broken, provide the exact corrected JSON-LD block
inline in the findings. Do not describe it in prose.

Lane 5 grade drops to D or below if: markup is misleading, invalid, hidden from
users, or uses a type/property combination that is ineligible for the claimed
Google feature. A page does not fail merely because no schema is warranted.
FAQ markup never earns a visibility promise; Google generally limits FAQ rich
results to authoritative government and health sites.

### Lane 6: AI EO (Answer Engine Optimization)

**Goal:** help people and automated systems understand and source the page
accurately without inventing facts. Run the Lane 6 checklist in
`references/lane-checklists.md`: clear opening answer, plain definitions,
explicit subjects, verified entity signals, accessible primary content, source
links, and hallucination-risk claims. Google Search ignores `llms.txt`; record
one only when another named consumer documents support, and never grade its
presence as a search signal.

Lane 6 grade drops to C or below if: the opening section cannot state the
page's subject and answer clearly, material claims lack sources, or primary
content is inaccessible without JavaScript and has no crawlable fallback.

### Lane 7: Copy and Conversion Quality

**Goal:** copy earns action. Every sentence either moves the reader toward the
primary CTA or proves the claim that does. Run the Lane 7 checklist in
`references/lane-checklists.md`: directness, proof, claims, CTA, trust, and
filler removal.

Lane 7 grade drops to C or below if: the intended action is absent or
undiscoverable in the rendered task path, any published statement is unverifiable, or
the copy could belong to any competing product without changing a word.

### Lane 8: E-E-A-T Signals

**Goal:** use Experience, Expertise, Authoritativeness, and Trustworthiness as a
human quality/trust lens and verify the available evidence. E-E-A-T is not a
standalone ranking score exposed by Google. Run the Lane 8 checklist in
`references/lane-checklists.md` for what counts as evidence for each concept.

Grade: A (all four strong), B (3 strong), C (2 strong), D/F (1 or 0).

Lane 8 grade drops to C or below if: no real proof of experience or expertise
is visible, contact or privacy information is absent, or misleading UI patterns
are present.

### Lane 9: Topic Cluster Architecture

**Goal:** when a multi-page site benefits from a pillar/cluster strategy,
confirm that the selected topic ownership and internal paths are coherent.
Skip for single-page audits; mark N/A when that architecture does not serve the
site's user journeys. Run the Lane 9 audit questions and cluster-map output
format in `references/lane-checklists.md`.

When a cluster strategy is in scope, Lane 9 grade drops to C or below if: its
declared pillar is missing, important cluster pages are orphaned, or multiple
pages appear to compete for the same query intent without a clear owner.

---

## 3. Finding Format

Report every finding in this block. Do not describe findings in prose.

```
[HIGH|MEDIUM|LOW] Finding title
Location: <URL, selector, or file + line>
Issue: <what is wrong and why it matters>
Fix: <exact corrective action>
Suggested copy or code: <literal rewrite, JSON-LD block, or command>
Verification: <how to confirm the fix worked>
```

Severity guide:
- HIGH: blocks indexing, breaks CTA, contains a false published statement, schema invalid
- MEDIUM: may reduce result clarity, sourceability, or reader task success;
  missing a relevant recommended signal
- LOW: copy quality, filler, minor structural improvement

---

## 4. Scoring

Grade each lane A-F. Grades are mechanical — derived from finding counts, not
impression:

| Grade | Rule |
|-------|------|
| A | No HIGH or MEDIUM findings in the lane |
| B | No HIGH findings; one or two MEDIUM findings |
| C | Exactly one HIGH finding, or three or more MEDIUM findings |
| D | Two or three HIGH findings |
| F | Four or more HIGH findings, or the lane is absent or actively harmful |

Hard caps:
- Cannot earn A overall without verifying a live URL
- Cannot earn A if primary CTA is broken or absent
- Cannot earn A if any published statement is false, unverifiable, or invented
- Cannot earn A in Lane 5 if present or warranted schema does not validate
- Cannot earn A in Lane 6 if primary content was unavailable to the tested
  intended clients and the audit cannot evaluate it
- Cannot earn A in Lane 8 if contact, privacy policy, or HTTPS is absent
- Cannot earn A in an in-scope Lane 9 if material query-intent ownership
  conflicts remain unresolved

Overall grade: convert letter grades to points (A=4, B=3, C=2, D=1, F=0).
Lanes 1, 3, and 6 count 1.5x. Lanes 2, 4, 5, 7, 8, 9 count 1x. Lane 0
excluded. Max weighted score = (3 × 1.5 + 6 × 1) × 4 = 42. Overall letter:
≥38 = A, ≥30 = B, ≥22 = C, ≥14 = D, <14 = F.

---

## 5. Output Template

Produce this block at the end of every full audit. Fill every field. Write
"none found" or "not applicable" rather than leaving a field blank.

```
=== SEO AUDIT REPORT ===

Audited URL:
Audit date:
Source checked: [live URL | source file | both]

--- KEYWORD BRIEF (Lane 0 — omit if not requested) ---
Primary query theme: [query family] — [intent] — [evidence source/date]
Demand: [sourced value/range | unknown]
Supporting query themes: [query — observed/inferred — evidence]
Related topics and entities: [list grouped by reader need]
Content gaps: [subject — checked URL/source — reader value — priority]
Search-feature eligibility: [feature — eligible/validated/observed/not verified]
Content brief: [reader-first section, entity, link, and source plan]

--- METADATA ---
SEO title (suggested):
Meta description (suggested):
H1 (suggested):
Subhead (suggested):

--- CONVERSION ---
Primary CTA (text and destination):
Secondary CTA (text and destination):

--- CONTENT ADDITIONS ---
Content brief (from Lane 0 — omit if not requested):
  Length: [reader-driven scope; no universal word-count target]
  Required subjects: [list derived from intent and verified source gaps]
  Topic/entity coverage:
    Primary subject: [clear/unclear] — evidence: [locations]
    Supporting subjects: [covered/missing] — evidence: [locations]
FAQ additions:
  Q: [real reader/searcher question — cite observed wording when available]
  A: [complete answer in the length the reader needs; subject explicit]
Internal links to add (anchor text → destination URL):
External links to add (anchor text → destination URL):
Competitor content gap:
  Competitor: [URL or "derived from niche"]
  Missing sections: [H2 text — target query — priority: CRITICAL|IMPORTANT|INFORMATIONAL]

--- SCHEMA ---
Schema changes:
  [Paste corrected or new JSON-LD block here]

--- AI EO NOTES ---
Clear opening summary:
Machine-readable AI file: [named consumer and documented use | none warranted]
Google Search effect of llms.txt: none
Hallucination risk flags:

--- E-E-A-T NOTES ---
Experience proof present:
Expertise signals:
Authoritativeness signals:
Trustworthiness gaps:

--- TOPIC CLUSTER MAP (omit for single-page audits) ---
Pillar: [page] — [target keyword]
  Cluster: [page] — [sub-topic keyword]
Orphan pages:
Cannibalization risks:

--- CORE WEB VITALS (never part of the A-F grade) ---
LCP: [score or "not measurable" — reason]
CLS: [score or "not measurable" — reason]
INP: [score or "not measurable" — reason]
Lighthouse score (if available): Performance [N] | Accessibility [N] | Best Practices [N] | SEO [N]
CWV Risk: low / medium / high
CWV risk factors observed: [list or "none"]
Note: scores come only from PageSpeed Insights or Lighthouse. Do not invent scores; do report observable risks. curl time_total is a server-response proxy, not a CWV score.

--- SCORES ---
Copy score: /70
  Directness: /10
  Rhythm: /10
  Trust: /10
  Specificity: /10
  Authenticity: /10
  Density: /10
  Search/AI readability: /10

Lane grades:
  Lane 1 (Technical Access):
  Lane 2 (Search and Answer Intent):
  Lane 3 (Metadata):
  Lane 4 (Structure):
  Lane 5 (Schema Markup):
  Lane 6 (AI EO):
  Lane 7 (Copy and Conversion Quality):
  Lane 8 (E-E-A-T Signals):
  Lane 9 (Topic Cluster Architecture):

Overall grade:

--- EVIDENCE BOUNDARIES ---
Safe to publish:
Recommend holding until verified (user's call):
Remove entirely:

--- VERIFICATION CHECKLIST ---
[ ] Status code confirmed 200
[ ] Canonical URL confirmed
[ ] robots.txt allows path
[ ] Schema vocabulary/shape validates at schema.org/validator
[ ] Google feature eligibility validates in Rich Results Test when applicable
[ ] All internal links return 200
[ ] Primary CTA destination loads correctly
[ ] og:image loads at full resolution
[ ] JSON-LD blocks contain no fabricated content

--- SHIP GATE ---
ship | ship-with-caveats | hold

Reason:
```

---

## 6. Workflow Steps

Follow these steps in order. Do not skip to findings before completing steps 1
through 3.

1. **Read the target.** Fetch the live URL or open the source file. If both
   are available, check both and note any divergence between source and rendered
   output.

2. **Run the Source Truth checks** from Section 1. Record every field exactly as
   found. Do not paraphrase tag values.

3. **Check robots.txt and sitemap.** Fetch `<domain>/robots.txt` and any
   listed sitemap. Confirm the target URL is not blocked and is listed.

4. **Scan all active lanes.** Lane 0 activates only when keyword discovery is
   requested. Lanes 1–8 run on every audit. Lane 9 is N/A for single-page
   audits and sites where a cluster model is not warranted; note the reason.
   Read the lane's checklist file from `references/`
   and work through each item. Mark each item pass, fail, or N/A. Note the
   location of each failure.

5. **Write ranked findings.** Use the finding format from Section 3. Group by
   lane. Put HIGH findings first within each lane.

6. **Write exact rewrites.** For every HIGH and MEDIUM finding involving copy,
   metadata, or schema: provide the literal replacement text or JSON-LD block.
   Do not describe what the fix should say. Write it.

7. **Fill the output template** from Section 5. Every field must be filled.

8. **Score each lane** A-F using the rules from Section 4. Apply hard caps.

9. **Set the recommended ship gate.** Recommend `ship` only if no HIGH findings remain and all hard
   caps are met. `ship-with-caveats` if only MEDIUM or LOW findings remain and
   no claim is false. `hold` if any HIGH finding is unresolved, any claim is
   false, or the CTA destination is broken. Name any lane items that could not
   be verified and why (e.g., "Core Web Vitals: no field data access",
   "sitemap not publicly accessible").

---

## Red Flags — Stop

If you catch yourself thinking any of these, stop and run the check for real:

- "I know this page; I can grade it from memory." — Fetch it. Source Truth first.
- "curl was fast, that covers Core Web Vitals." — curl is a server-response proxy; CWV scores come only from PageSpeed Insights or Lighthouse, or they are "not measurable" with a reason.
- "I'll describe the schema fix; they can write the JSON." — Write the literal JSON-LD block.
- "The title or description crossed a magic character limit." — Count it for
  preview diagnostics, then judge accuracy and likely truncation in context.
  Google publishes no fixed character limit.
- "A traffic estimate will make this finding land harder." — Never invent traffic, rankings, or ROI.
- "The lane mostly passes; I'll skip the rest of the checklist." — Every item gets pass, fail, or N/A.

---

## 7. Boundaries

Do not invent traffic estimates, ranking positions, citation frequency, or ROI
from SEO changes. Do not present `llms.txt`, content chunking, exact-match term
density, word count, or unsupported schema as Google ranking requirements. Name
what was checked, which primary guidance was used, what was skipped, and what
requires additional tooling.

---

## Routing

- Need a fast A-F promotion-readiness verdict instead of a full audit → `suede-visibility-grader`.
- Findings point at conversion problems (CTA, friction, offer) → `suede-site-alchemy` for the rewrite pass.
- Findings require fresh copy, not fixes → `suede-copy`.
- Audit passed and the page is part of a release → `suede-launch-packaging` to package the launch.
