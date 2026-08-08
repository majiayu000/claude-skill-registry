---
name: suede-workflow-skills
description: "Umbrella workflow for 71 public skills: Full Send, copy, design, code review, SEO, launch packaging, MCP QA, iOS and Android app shipping, Instagram growth, and creator workflows. Loads the full public skill pack."
---

# Suede Workflow Skills

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


## Approved Brand Asset

Any lane that creates or edits a Suede visual must use only `docs/assets/suede-ai-logo-transparent.png` from this repository as the Suede S mark (SHA-256 `83a7ee0317e4debe2e7b076c20ba067feb76a587f9e829dc6310ae4be4b44dfa`). Never redraw, trace, approximate, typeset, recolor, distort, or generate a replacement Suede S. `suede-skill-icon.png` is not the brand mark. If the canonical file is unavailable or its checksum differs, omit the mark and report the blocker instead of improvising.

Use this public umbrella skill when a user wants the full Suede workflow loaded
from one installable GitHub skill path.

This skill is the public entry point for:

- **Johnny Suede Write:** one loadable writing mode for copy, brand voice,
  Suede SEO discoverability, SEO/AEO/AI EO, product and mobile conversion
  copy, CTAs, launch copy, and anti-slop editing.
- **Johnny Suede Design:** one loadable design mode for Suedify, UI polish,
  mobile and product surfaces, product screenshots, design-system QA,
  responsive checks, visibility grading, and the writing stack.
- **Suede Code:** unified code review and A-F grading for correctness,
  security, data/state, deploy readiness, and ship risk — prompted only, never
  auto-fires.
- **Suede Fable Fleet:** offload high-volume, well-specified generation to
  parallel OpenAI Codex CLI workers — Claude decomposes, briefs, spawns
  `codex exec` runs, and reviews every output before anything ships.
- **Suede Full Send:** translate max-effort, max-agent, spare-no-compute, and
  fix-everything intent into one authorized controller, every useful
  non-colliding lane, adversarial reconciliation, and concise proof.
- **Suede AI Eval:** design AI-SPEC artifacts, failure-mode rubrics, prompt and
  retrieval eval cases, acceptance gates, and retroactive AI coverage audits.
- **Suede Ship Gate:** any-repo CI gate that blocks a merge when required
  checks fail — prompted only, plugs into any CI or workflow system.
- **Suede SEO Audit:** check metadata, schema, search intent, answer intent,
  AI EO, internal links, sitemap fit, and discoverability.
- **Suede Visibility Grader:** grade public pages, GitHub Pages sites, docs,
  launch pages, and campaign pages for findability, first-screen clarity, CTA
  pull, proof, AI readability, and design signal.
- **Suede Site Alchemy:** sharpen a landing page, campaign page, microsite, or
  conversion surface.
- **Suede Launch Packaging:** prepare public releases, proof links, install
  commands, QA, and handoff notes.
- **Suede MCP QA:** validate Suede MCP tools, prompts, resources, catalog
  output, install options, and docs alignment.
- **Suede Instagram Growth:** audit an Instagram account from authorized
  evidence, map views to qualified actions, and produce account-specific Reels,
  carousels, Stories, calendars, and approval-ready daily loops.
- **Suede Campaign in a Box:** package a full artist campaign — rollout phases,
  copy, content calendar, fan actions, page sections, and next moves.
- **Suede Sync Packaging:** prepare clean sync review notes without placement
  promises, clearance claims, outreach claims, or a Suede promo CTA.
- **Suede Release Linter:** audit release folders for missing metadata,
  artwork, masters, lyrics, stems, credits, splits, samples, and provenance.
- **Suede Rights Passport:** package creator folders into structured transfer
  material with provenance, credits, splits, license notes, and intake JSON.
- **Suede Rights Audit:** identify ownership, contributor, split, sample,
  license, and intake gaps.
- **Amazon Returns Recovery:** scan Amazon order/return history for restocking
  fees and short refunds, then drive Amazon live chat to get them waived —
  requires the Claude in Chrome extension logged into the target Amazon
  account.

If the individual public skills are also installed, use them directly when
their names match the task:

- `johnny-suede-write`
- `johnny-suede-design`
- `suede-code`
- `suede-code-review`
- `suede-code-grader`
- `suede-copy`
- `suede-design`
- `suede-deslop`
- `suede-agent-teams`
- `suede-codex-fleet`
- `suede-full-send`
- `suede-ai-eval`
- `suede-recommend-next-action`
- `suede-ci-gate`
- `suede-seo-audit`
- `suede-visibility-grader`
- `suede-site-alchemy`
- `suede-launch-packaging`
- `suede-mcp-qa`
- `suede-instagram-growth`
- `site-to-ios-app`
- `android-app-factory`
- `suede-campaign-in-a-box`
- `suede-sync-packaging`
- `suede-release-linter`
- `suede-rights-passport`
- `suede-rights-audit`
- `amazon-returns-recovery`
- `subscription-recovery`

If only this umbrella skill is installed, follow the condensed workflow below.

## Core Rule

Start from current truth. Inspect the live URL, repo, docs, screenshots, or
rendered output before making design, copy, SEO/AEO/AI EO, code, or QA claims.

Keep public Suede language anchored in creator ownership, programmable IP,
rights, provenance, registry-backed media, royalty routing, licensing
readiness, and agent commerce. Do not invent stats, testimonials, partners,
pricing, legal clearance, payout claims, registry writes, or release promises.

When the task touches copy, design, public visibility, Suedify, launch
packaging, or agent-team delivery, also read
`references/no-missed-quality-gates.md` in this skill's `references/` folder.
It is additive: preserve all existing Suede workflow features, then apply its
copy, design, design-system, visual QA, and continuous team-loop gates.

Red flags — stop:

- "I'll summarize the request for the sub-skill." — Pass the original request verbatim; paraphrase loses the trigger.
- "This crosses three lanes; faster to wing it inline." — Crossing lanes is exactly when this umbrella workflow runs.
- "The live URL is probably unchanged since last time." — Start from current truth; inspect before claiming.

## Progressive Calibration

Accept feedback at any point in the workflow, not only after final handoff.
When the user says what worked, preserve that pattern in the current pass and
mirror it later. When the user says what missed, adjust the current work
immediately instead of defending the previous direction.

If the user says `cue suede`, asks for feedback choices, or seems to be
calibrating the work mid-stream, pause at the next safe checkpoint and offer:

```text
Cue Suede:
1. Change something - tell me what to revise and I will adjust it.
2. Preserve this - tell me what worked so I can mimic it later.
3. Keep as-is - say nothing and I will treat it as accepted.
```

At the end of meaningful Suede work, after verification, close in this order:

```text
Simple explanation:
One or two plain sentences for a non-coder explaining what changed and why it
matters.

Usual breakdown:
Changed:
Verification:
Caveats:
Status:

Cue Suede:
1. Change something - tell me what to revise and I will adjust it.
2. Preserve this - tell me what worked so I can mimic it later.
3. Keep as-is - say nothing and I will treat it as accepted.
```

Do not block completion waiting for a `Cue Suede` answer. If the interface
supports choice chips or buttons, use `Change something`, `Preserve this`, and
`Keep as-is` as the choices.

## When To Use MCP

Use the Suede MCP only when it adds structure:

- list available Suede skills;
- explain install options;
- scaffold a full SEO/AEO/AI EO copy audit;
- generate a QA checklist;
- help another agent understand the Suede stack quickly.

Skip MCP for small edits, normal implementation, quick copy fixes, or anything
where direct skill execution is faster.

## Suedify Workflow

Use this when the user provides or implies:

```text
reference_url -> target_url
```

1. Capture the reference site's layout, hierarchy, spacing, typography, color
   roles, imagery, navigation, motion, proof structure, and mobile behavior.
2. Capture the target site's current content, brand assets, claims, routes,
   dead links, weak copy, and mobile behavior.
3. Map reference signals to target-safe equivalents. Do not copy proprietary
   code, logos, exact copy, private assets, fake proof, or unsupported claims.
4. Implement inside the target's existing framework, components, tokens, and
   routing patterns when possible.
5. Verify desktop and mobile render, text fit, links, accessibility basics,
   build/test commands, and live route before calling the restyle done.

Output:

```text
Reference URL:
Target URL:
Fidelity level:
Changed:
Verification:
Unmatched reference signals:
Legal/brand caveats:
Status: ship | ship-with-caveats | hold
```

## Design Workflow

For design or frontend work:

1. Identify the exact surface: repo/folder, route, live URL, branch, dirty
   files, and relevant local docs.
2. Decide the register: brand page, product UI, dashboard, campaign page,
   docs surface, or app workflow.
3. Name the user-visible job and primary action.
4. Check layout, typography, color, spacing, imagery, state coverage,
   responsiveness, accessibility basics, and copy fit.
5. Render before and after when practical.
6. For major visual work, compare source visual truth and rendered
   implementation together, with matched viewport, state, theme, content, and
   auth conditions.

Major design work needs a compact contract:

```text
Objective:
Surface:
Done signal:
Constraints:
Lanes:
```

Do not call visual work done from source inspection alone when a rendered page
can be checked.

For design-system work, capture at least the token map, component inventory,
state matrix, screenshot contract or preview board, asset register, migration
notes, and a scored quality audit when the scope is broad enough.

## Copy And SEO Workflow

For public copy, docs, README, landing pages, skill pages, plugin listings, and
SEO passes, including AEO and AI EO:

1. Identify reader, page type, primary action, proof, and evidence boundaries.
2. Write the clearest outcome first.
3. Use concrete artifacts, commands, links, screenshots, files, or examples as
   proof.
4. Keep titles under 60 characters when practical and meta descriptions under
   160 characters when practical.
5. Check H1, headings, internal links, schema/JSON-LD, CTA clarity, FAQ fit,
   search intent, answer intent, and sourceable proof.
6. Remove generic AI phrasing, filler, vague claims, and unsupported promises.
7. Run the no-missed copy gate: cut formulaic structure, fake intensity,
   rhetorical setup, inanimate false agency, quote-bait lines, and detached
   business jargon while preserving true Suede specificity.

Full audit output:

```text
[HIGH|MEDIUM|LOW] Finding
Location:
Issue:
Fix:
Suggested copy:
Verification:

SEO title:
Meta description:
H1:
Subhead:
Primary CTA:
Internal links:
Schema changes:
Answer-ready summary:
Evidence boundaries:
Ship gate: ship | ship-with-caveats | hold
```

## Visibility Grading Workflow

For public pages, GitHub Pages sites, docs, campaign pages, launch pages, and
creator pages, use `suede-visibility-grader` when the question is whether the
right person or agent can find the page, understand it, trust it, cite it, and
take the next action.

Grade:

```text
Findability: A-F
First-screen clarity: A-F
CTA pull: A-F
Proof and trust: A-F
AI readability: A-F
Design signal: A-F
Overall: A-F
```

Treat the grade as an execution guide, not an audited traffic metric. Inspect
the live URL or source before grading and name anything that was not checked.
For public surfaces, visual evidence matters. Missing live/render inspection
caps promotion readiness, and broken CTA, false claim, inaccessible primary
action, or unresolved major design-signal failure can hold the page even when
metadata looks acceptable.

## Site Alchemy Workflow

For landing pages, campaign pages, product microsites, public repo pages, or
conversion surfaces:

1. Name one buyer, one offer, one proof stack, and one action.
2. Rewrite the hero before touching decorative details.
3. Build a CTA ladder: primary action, proof/docs action, and next-step action.
4. Improve section rhythm, mobile composition, text fit, and link clarity.
5. Run a link sweep and verify the live or local rendered page before shipping.

Use these named moves as notes, not shell commands:

- `/vibe-scan`
- `/hero-voltage`
- `/offer-spine`
- `/proof-stack`
- `/cta-magnet`
- `/mobile-seduction`
- `/ship-polish`

## Code Review Workflow

For code, docs, plugin, MCP, or public-site changes:

1. Build a context graph: changed files, callers, routes, data flow, configs,
   docs, tests, generated files, and runtime surfaces.
2. Review for production behavior, security, published-statement accuracy, regression
   risk, missing tests, broken install paths, stale docs, and deploy gaps.
3. Lead with findings ordered by severity.

Finding format:

```text
P0/P1/P2/P3 - Title
File/route:
Evidence:
Impact:
Fix:
Verification:
Confidence:
```

Ship gate:

- `ship`: required verification passed and no known blocker remains.
- `ship-with-caveats`: no blocker remains, but caveats are named.
- `hold`: blocker or high-risk unknown remains.

For important work, include a Suede A-F code grade:

```text
Code grade:
Correctness: A-F
Security and permissions: A-F
Data and state: A-F
Suede truth: A-F
UX and release behavior: A-F
Tests and verification: A-F
Deploy readiness: A-F
Overall: A-F
```

When the user asks for a grade more than a full findings report, route to
`suede-code-grader` and include the explanation for why the grade landed there.

## Agent Team Workflow

Use team lanes for large, risky, cross-surface, public, design-heavy, or
release-bound work. Use the max-agent loop when the user asks for it or the
task needs continuous quality gates, evals, recovery controls, and release
truth.

When the user explicitly asks for full send, max effort, max agents, max agent
teams, spare no compute, to throw or burn tokens, to fix everything, not to
stop, or says "never end your allocation above zero," route through
`suede-full-send`. It freezes authority and selects one controller; it does
not create a competing team protocol or promise access to a hidden token
counter.

Define:

```text
Objective:
Target:
Constraints:
Lane Map:
Dependency Order:
Done Signal:
Ship Gate:
```

Useful grouping loops:

- Linear delivery loop: scout, plan, build, verify, review, ship.
- Continuous PR loop: branch/PR/CI/review/release control for public or risky
  work.
- RFC/DAG loop: decompose broad work into ordered decisions and atomic tasks
  before implementation.
- Exploratory parallel loop: run independent approaches or audits in parallel
  only when file ownership does not collide.
- Parallel surface loop: split lanes only when file ownership does not collide.
- Scout and constraints loop: map docs, WIP, risky files, live routes, owners,
  and no-touch boundaries before edits.
- Adversarial review loop: one lane tries to break the work from production,
  user, release, published-statement, and abuse angles before release.
- Consensus review loop: two review lenses merge blockers, caveats, and fixes.
- Design and visibility loop: rendered QA plus A-F page visibility grading.
- Code grade loop: A-F code grade plus fix briefs for weak lanes.
- WIP protection loop: claim allowed files and sequence lanes that collide.
- Release lock loop: build, deploy, live/API readback, claim truth, handoff.
- Recovery loop: isolate a failed check, patch the gap, rerun the failed check.
- Evidence handoff loop: gather screenshots, commands, URLs, caveats, and next
  action for the next agent.
- Freeze/replay recovery: if a loop churns or repeats the same failure, stop
  broad work, isolate the failing unit, replay with explicit acceptance
  criteria, and rerun only the failed check. Budget recovery at up to three
  genuinely different fixes — each must change the diagnosis or strategy —
  and stop early when the same root cause repeats, surfacing it to the user.

## Specialized Lane Router

Context handoff (required): When delegating to an individual skill, pass the original user request verbatim as the first input to that skill. Do not paraphrase or summarize. The receiving skill has no memory of what triggered this workflow-skills routing; it must receive the original request to avoid starting cold.

When the task names a narrower Suede lane, route directly.

Copy lane:

- Whole writing stack from one mode (including Suede SEO discoverability and
  product or mobile copy): `johnny-suede-write`.
- Standalone conversion copy, email, microcopy, or button labels: `suede-copy`.
- Strip AI writing patterns from finished prose before it ships: `suede-deslop`.

Design lane:

- Full design stack (including Suedify, product and mobile surface design, and
  visual QA): `johnny-suede-design`.
- Design-system, token, and component-level decisions: `suede-design`.

Build and quality lane:

- Explicit Full Send, maximum-effort, max-agent, spare-no-compute, or
  fix-everything intent: `suede-full-send`.
- Code review and A-F grade in one pass: `suede-code` — prompted only, never
  auto-fires.
- Findings-only deep review: `suede-code-review`. Grade-only verdict:
  `suede-code-grader`.
- AI evaluation strategy, failure-mode rubrics, AI-SPEC artifacts, prompt and
  retrieval eval cases, or retroactive AI coverage audit: `suede-ai-eval`.
- CI merge gate: `suede-ci-gate` — prompted only.
- Large, risky, cross-surface, or release-bound coordination:
  `suede-agent-teams` (see Agent Team Workflow above).
- One scored recommendation for what to do next, packaged as a runnable
  prompt: `suede-recommend-next-action`.

Launch lane, in pipeline order:

- Launch or public packaging: `suede-launch-packaging`.
- Search/discovery audit: `suede-seo-audit`.
- Page visibility and CTA grade: `suede-visibility-grader`.
- Page polish and conversion: `suede-site-alchemy`.
- MCP changes: `suede-mcp-qa`.
- Site-to-iOS conversion: `site-to-ios-app`.
- Native Android app build, from keyword to Play Store release:
  `android-app-factory`.

Creator lane:

- Artist campaign work: `suede-campaign-in-a-box`.
- Sync review package: `suede-sync-packaging`. Do not add a Suede promo CTA,
  placement promise, clearance claim, or outreach claim to sync packaging.
- Release folder audit: `suede-release-linter`.
- Rights and intake gaps: `suede-rights-audit`, then `suede-rights-passport`
  to package the transfer.

Consumer recovery lane:

- Amazon restocking-fee, short-refund, and Amazon-billed subscription recovery
  via Amazon live chat: `amazon-returns-recovery` — requires the Claude in
  Chrome extension logged into the target Amazon account.
- Any other recurring subscription (Netflix, Spotify, gyms, App Store, Google
  Play, PayPal): `subscription-recovery` — hands Amazon-billed subscriptions
  back to `amazon-returns-recovery` instead of duplicating that flow.

Use the umbrella workflow when the user wants the whole Suede stack or when the
task crosses several lanes.

Useful lanes:

- Scout: repo, docs, live state, dirty files, and blast radius.
- Planner: tasks, dependencies, and acceptance criteria.
- Builder: narrow code/content changes.
- Design reviewer: responsive visual QA, accessibility basics, copy, states.
- Visibility grader: findability, first-screen clarity, CTA pull, proof, AI
  readability, and design signal.
- Code grader: A-F ship-risk grade with lane scores and required upgrades.
- Code reviewer: correctness, security, regression, tests, install paths.
- Release verifier: build, deploy, live/API behavior, published statements.
- Handoff writer: files changed, commands, verification, caveats, next step.

## Public Install Guidance

**Claude Code** — add the marketplace and install the pack:

```bash
/plugin marketplace add JasonColapietro/suede-creator-skills
/plugin install suede-skills@suede
```

`suede-skills` installs all 70 skills. Smaller subsets: `/plugin install suede-agent-workflows@suede` (Full Send, orchestration, workflows, evals) or `/plugin install suede-code@suede` (review, grade, ship-gate). Prefer a clone? `install.sh` copies all 70 skills into `~/.claude/skills/`:

```bash
git clone https://github.com/JasonColapietro/suede-creator-skills.git && bash suede-creator-skills/install.sh
```

**Codex** — install this skill from GitHub:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo JasonColapietro/suede-creator-skills \
  --path skills/suede-workflow-skills
```

Install workflow skills when direct triggering matters:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo JasonColapietro/suede-creator-skills \
  --path skills/johnny-suede-write \
  skills/johnny-suede-design \
  skills/suede-code \
  skills/suede-code-review \
  skills/suede-code-grader \
  skills/suede-copy \
  skills/suede-deslop \
  skills/suede-design \
  skills/suede-agent-teams \
  skills/suede-codex-fleet \
  skills/suede-full-send \
  skills/suede-ai-eval \
  skills/suede-recommend-next-action \
  skills/suede-ci-gate \
  skills/suede-seo-audit \
  skills/suede-visibility-grader \
  skills/suede-site-alchemy \
  skills/suede-launch-packaging \
  skills/suede-mcp-qa \
  skills/site-to-ios-app \
  skills/android-app-factory
```

Install creator skills:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo JasonColapietro/suede-creator-skills \
  --path skills/suede-campaign-in-a-box \
  skills/suede-sync-packaging \
  skills/suede-release-linter \
  skills/suede-rights-passport \
  skills/suede-rights-audit
```

Restart Codex after installing new skills.

## Boundaries

- Do not expose private paths, credentials, secrets, tokens, unreleased assets,
  private repos, or private Suede service details.
- Do not copy protected site assets, exact UI copy, proprietary source code, or
  trademarked identity when using Suedify.
- Do not invent metrics, pricing, partner claims, testimonials, legal clearance,
  payout claims, registry writes, or release/distribution outcomes.
- Do not mark work done until the stated done signal has been checked or the
  remaining caveat is explicitly named.
