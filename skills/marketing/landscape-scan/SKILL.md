---
name: landscape-scan
description: >
  Scan the current market landscape and produce a ground-truth ecosystem
  snapshot. Chains /last30days for live research, validates with user,
  and writes brand/landscape.md with a Claims Blacklist that hard-gates
  all content generation. Use when: "landscape", "ecosystem", "market
  snapshot", "ground truth", "what's happening", "refresh landscape",
  "market trends", or before any content campaign to verify claims.
---

# /landscape-scan -- Ground-Truth Ecosystem Snapshot

Every claim your marketing makes sits on top of an assumption about the market.
"We're the first to..." "Nobody else does..." "The market is moving toward..."
When these assumptions are wrong, your positioning collapses on contact with
reality. Customers who Google your claims and find them false don't come back.

This skill builds a verified ecosystem snapshot that becomes the single source
of truth for all downstream content. The Claims Blacklist it produces hard-gates
every content skill -- if a claim is blacklisted, no skill writes it. Period.

No SaaS tools needed. Live web research + user validation.

---

## On Activation

1. Check if `brand/` directory exists in the project root.
2. If it does, read available files in priority order:
   - `competitors.md` -- existing competitive intel (primary input)
   - `positioning.md` -- current positioning angles and claims
   - `audience.md` -- target market and buyer personas
   - `voice-profile.md` -- brand personality (for tone of output)
   - `learnings.md` -- past marketing learnings and corrections
3. Apply loaded brand context to focus the landscape scan -- existing competitor
   data narrows the research query, positioning data identifies claims to verify.
4. If `brand/` does not exist or is empty, proceed without it -- this skill
   works standalone by asking the user foundational questions.

---

## Iteration Detection

Before starting, check whether `./brand/landscape.md` already exists.

### If landscape.md EXISTS --> Refresh Mode

Do not start from scratch. Instead:

1. Read the existing landscape file.
2. Present a summary of the current state:
   ```
   EXISTING LANDSCAPE SNAPSHOT
   Last updated {date} by /landscape-scan

   Ecosystem segments: {N}
   Claims blacklisted: {N}
   Market shifts tracked: {N}

   Freshness: {days} days old (threshold: 14 days)

   ------------------------------------------

   What would you like to do?

   1. Full refresh -- re-run /last30days, revalidate everything
   2. Verify claims -- check if blacklisted claims are still invalid
   3. Add new segment -- expand to cover a new market area
   4. Rebuild from scratch -- discard and start over
   ```

3. Process the user's choice:
   - Option 1 --> Re-research with fresh /last30days query, merge with existing data
   - Option 2 --> Focused validation of Claims Blacklist items only
   - Option 3 --> Targeted research on a new ecosystem segment, merge into existing file
   - Option 4 --> Full process from scratch

4. Before overwriting, show a diff of what changed and ask for confirmation.

### If landscape.md DOES NOT EXIST --> Full Scan Mode

Proceed to the full process below.

---

## The Core Job

Map current ecosystem reality so every downstream skill operates on verified
ground truth. The output has two critical components:

1. **Ecosystem Snapshot** -- what is actually happening in the market right now
   (players, trends, shifts, emerging categories, consolidation, funding rounds)
2. **Claims Blacklist** -- specific claims your marketing MUST NOT make because
   they are verifiably false, outdated, or easily disproven by a customer who
   spends 30 seconds searching

The Claims Blacklist is not advisory. It is a hard gate. Every content-generating
skill reads `brand/landscape.md` and refuses to write blacklisted claims.

---

## Orchestration Flow

### Phase 1: Preflight

1. Read brand/ context files (see On Activation above).
2. Detect mode: create vs refresh (see Iteration Detection above).
3. Determine context level:
   - **L0** -- No brand/ files. Need to ask everything.
   - **L1** -- Have product name/description only.
   - **L2** -- Have competitors.md and/or positioning.md.
   - **L3** -- Have L2 + will run /last30days for live data.
   - **L4** -- Have L3 + existing landscape.md (refresh mode).
4. If `--dry-run` is set, report what WOULD happen and exit. Do not make any
   network calls or write any files.

### Phase 2: Build Research Query

Extract search parameters from available context:

- **Product/Category**: from positioning.md `primary_gap` or user input
- **Competitors**: from competitors.md competitor names, or user input
- **Target market**: from audience.md `primary_persona`, or user input
- **Time window**: last 30 days (default), or user-specified

Build the research query (see `references/query-templates.md` for industry-specific
templates). The query should cover:

1. Market movements -- funding, acquisitions, pivots, shutdowns
2. Product launches -- new entrants, major version releases, feature parity shifts
3. Pricing changes -- competitors adjusting pricing models or tiers
4. Narrative shifts -- what the industry press and community are saying
5. Regulatory/platform changes -- policy shifts that affect the ecosystem

If at L0-L1 (no competitors.md), ask the user:
```
I need to understand your market before scanning.

1. What does your product do in one sentence?
2. Who are your top 3 competitors? (names or URLs)
3. What category would a customer search for?
```
Cap at 3 questions. Use answers to build the query.

### Phase 3: Run /last30days

Invoke the Skill tool:
```
Skill: last30days
Args: "{research query from Phase 2}"
```

The /last30days skill searches across Reddit, X/Twitter, YouTube, Hacker News,
and web sources for the last 30 days of activity.

**Fallback if /last30days is unavailable:**
1. Use WebSearch tool directly with the research query.
2. Never use Claude native WebSearch. Use `exa-search` / Exa MCP for web research (and `/last30days` for social signal).
3. If no web research is available at all, proceed with user knowledge only
   and mark every finding as `source: user-reported` in the output.
4. Note the limitation: "Landscape based on provided information, not live
   research. Verify before making strategic decisions."

### Phase 4: Validate with User

Present 3-5 targeted questions using AskUserQuestion. Cap at 5 total -- do not
interrogate. Prioritize questions about contradictions and surprises.

**Question priority order:**
1. **Contradictions** -- where research contradicts existing brand/ files
   "Research shows {Competitor X} now offers free tier. Your competitors.md
   says they're premium-only. Which is current?"
2. **Surprises** -- findings that might change strategy
   "Did you know {Competitor Y} raised $50M last month? Does this change
   your positioning approach?"
3. **Gaps** -- things research couldn't determine
   "I couldn't verify whether {claim from positioning.md} is still unique
   to you. Do any competitors now offer this?"
4. **Scope** -- if research surfaced new segments
   "Research surfaced {new player/category}. Should I include them in
   the landscape?"
5. **Blacklist candidates** -- potential claims to block
   "Your positioning says 'only solution that does X.' Research found
   2 competitors now do X. Should I blacklist this claim?"

If there are no contradictions or surprises, reduce to 3 questions max.
Never ask questions you can answer from the research.

### Phase 5: Synthesize into landscape.md

Write `./brand/landscape.md` following the output format below. Every section
must be populated -- use "No data available" with a reason if a section cannot
be filled. See `references/landscape-schema.md` for the full schema with
examples of each section.

### Phase 6: Cross-Reference

After writing landscape.md, compare it against other brand/ files:

1. **vs competitors.md** -- flag competitors that have changed positioning,
   pricing, or status since competitors.md was written.
2. **vs positioning.md** -- flag positioning claims that are now blacklisted
   or weakened by market shifts.
3. **vs audience.md** -- flag audience assumptions that market shifts may
   have invalidated.

Present contradictions to the user:
```
CROSS-REFERENCE: BRAND FILE CONTRADICTIONS

  competitors.md (updated 45 days ago)
  ├── {Competitor X} pricing changed: was $29/mo, now free tier
  └── New entrant {Y} not listed

  positioning.md (updated 30 days ago)
  ├── "Only AI-powered solution" -- now FALSE (2 competitors added AI)
  └── Suggest: refresh with /positioning-angles

  audience.md (updated 60 days ago)
  └── No contradictions found

  SUGGESTED REFRESHES
  -> /competitive-intel    Update competitor teardowns (~15 min)
  -> /positioning-angles   Rebuild angles with new landscape (~15 min)
```

Do NOT auto-update other brand files. Only flag and suggest.

---

## Output Format

Write `./brand/landscape.md` with this structure:

```markdown
---
title: Market Landscape
type: landscape-scan
skill: landscape-scan
date: [ISO date]
ecosystem_segments: [number]
claims_blacklisted: [number]
market_shifts_tracked: [number]
freshness_days: 0
research_sources: [list of source types used]
---

# Market Landscape -- [Product/Project Name]

## Ecosystem Map

### Market Category
[One-line definition of the market category this product operates in]

### Ecosystem Segments

#### Segment: [Name]
- **Players:** [Company 1], [Company 2], [Company 3]
- **Current state:** [What's happening in this segment right now]
- **Trajectory:** [growing/stable/declining/consolidating]
- **Signal:** [Specific evidence -- funding round, product launch, trend data]

#### Segment: [Name]
[Same structure]

---

## Market Shifts (Last 30 Days)

### [Shift 1: Descriptive Title]
- **What happened:** [Factual description]
- **Source:** [URL or source type]
- **Impact on us:** [How this affects our positioning/strategy]
- **Urgency:** [high/medium/low]

### [Shift 2: Descriptive Title]
[Same structure]

---

## Claims Blacklist

> These claims MUST NOT appear in any marketing content.
> Every content-generating skill reads this section as a hard gate.

### Blacklisted Claims

| # | Claim | Reason | Evidence | Blacklisted Date |
|---|-------|--------|----------|-----------------|
| 1 | "[Specific claim text]" | [Why it's false/misleading] | [Source] | [ISO date] |
| 2 | "[Specific claim text]" | [Why it's false/misleading] | [Source] | [ISO date] |

### Verified Safe Claims
- "[Claim]" -- verified [date], source: [source]
- "[Claim]" -- verified [date], source: [source]

---

## Competitive Movement

### New Entrants
- **[Company]** -- [What they do, when they appeared, threat level]

### Pricing Shifts
- **[Company]** -- [Old pricing] -> [New pricing], [date]

### Positioning Shifts
- **[Company]** -- was "[old positioning]", now "[new positioning]"

### Exits/Acquisitions
- **[Company]** -- [What happened], [date]

---

## Ecosystem Opportunities

1. **[Opportunity]** -- [Why this matters now, based on landscape data]
2. **[Opportunity]** -- [Why this matters now]
3. **[Opportunity]** -- [Why this matters now]

---

## Raw Research Notes

[Condensed notes from /last30days or web research, with source URLs]
```

---

## Progressive Enhancement Levels

| Level | Context Available | Output Quality |
|-------|------------------|---------------|
| L0 | Product name only | Basic ecosystem map, user-reported claims only, no blacklist verification |
| L1 | + product description, target market | Focused scan, category-specific segments, preliminary blacklist |
| L2 | + competitors.md, positioning.md | Verified blacklist against known claims, competitor movement tracking |
| L3 | + /last30days live research | Full ground-truth snapshot, evidence-backed blacklist, source URLs |
| L4 | + existing landscape.md (refresh) | Delta analysis, trend tracking over time, blacklist evolution |

---

## Output Presentation

### Header

```
================================================

  MARKET LANDSCAPE SCAN
  [Product/Project Name]
  Generated [Month Day, Year]

================================================
```

### Files Saved

```
  FILES SAVED

  ./brand/landscape.md               ok
```

### What's Next

```
  WHAT'S NEXT

  Your ecosystem snapshot is built with {N}
  segments mapped, {N} market shifts tracked,
  and {N} claims blacklisted. All content skills
  will now respect the Claims Blacklist.

  -> /competitive-intel     Update competitor
                            teardowns with new
                            landscape data (~15 min)
  -> /positioning-angles    Rebuild angles against
                            verified ground truth
                            (~15 min)
  -> /direct-response-copy  Write copy that avoids
                            blacklisted claims
                            (~15 min)

  Or tell me what you're working on and
  I'll route you.
```

---

## Anti-Patterns

### Don't auto-update other brand files
Write landscape.md only. Flag contradictions in other brand/ files and suggest
refreshes, but never overwrite competitors.md, positioning.md, or audience.md.

**WHY:** Each brand file has an owning skill that understands the full context
of that file. Auto-updating creates ownership conflicts -- if /landscape-scan
silently changes competitors.md, the next /competitive-intel run may produce
inconsistent results because it doesn't know what changed or why.

### Don't skip user validation
Always run Phase 4 (Validate with User) even when research data looks solid.

**WHY:** Live research can surface false positives -- a competitor's pricing
page may show a promotion, not a permanent change. A press release about a
feature may be vaporware. Only the user can verify whether a finding is real
enough to blacklist. False positive blacklisting removes valid claims from your
marketing arsenal unnecessarily.

### Don't run without checking brand context first
Always read available brand/ files before building the research query, even
if the user provides a direct request.

**WHY:** Without brand context, the research query is unfocused. Searching
"[product category] market trends" returns generic industry noise. Searching
"[product category] + [specific competitors] + [specific claims to verify]"
returns actionable intelligence. The difference between a useful scan and a
useless one is query specificity.

### Don't blacklist claims without evidence
Every blacklisted claim must have a specific reason AND a source. "Might be
outdated" is not sufficient for blacklisting.

**WHY:** The Claims Blacklist is a hard gate. A wrongly blacklisted claim
prevents every content skill from using a valid differentiator. The cost of
a false blacklist is as high as the cost of a false claim -- both waste
positioning power.

### Don't treat the landscape as permanent
landscape.md has a 14-day freshness window, the shortest of any brand file.

**WHY:** Markets move fast. A landscape that's 30 days old may have missed
a competitor launch, a funding round, or a pricing change that invalidates
your Claims Blacklist. The short freshness window forces regular re-scans,
which is the entire point -- ground truth must stay grounded.

---

## Web Search Fallback

If web search / /last30days is unavailable:

1. Ask the user for recent market developments they're aware of.
2. Build the landscape from user knowledge + existing brand/ files.
3. Mark all findings as `source: user-reported` in the output.
4. Note the limitation clearly: "Landscape is based on user-reported
   information, not live web research. Claims Blacklist may be incomplete.
   Verify before making strategic decisions."
5. Set `research_sources: ["user-reported"]` in frontmatter.
6. Reduce Claims Blacklist confidence -- prefix entries with "Unverified:"
   to signal that downstream skills should treat them as advisory, not hard gates.

---

## What This Skill Is NOT

- **Not competitive intelligence** -- /competitive-intel does deep competitor
  teardowns. This skill maps the broader ecosystem and produces a Claims
  Blacklist. Use both: competitive-intel for depth, landscape-scan for breadth.
- **Not a strategy document** -- The output is a fact-finding report, not a
  plan. Use /positioning-angles or /launch-strategy to act on the landscape.
- **Not a one-time setup** -- This is the most time-sensitive brand file.
  14-day freshness means re-scanning before every major content campaign.
- **Not market research** -- This doesn't estimate TAM, SAM, or market size.
  For audience sizing, use /audience-research. This skill maps what IS happening,
  not what COULD happen.

---

## Feedback Collection

After delivering the landscape scan:

```
  How did this land?

  a) Solid -- using this as-is for content planning
  b) Good -- added some market intel I know
  c) Incomplete -- missing key segments or shifts
  d) Haven't used yet
```

**Processing feedback:**
- **(a) Solid:** Log to `./brand/learnings.md` with key blacklisted claims.
- **(b) Good:** Ask what they added. Offer to update landscape.md with their additions.
- **(c) Incomplete:** Ask what's missing. Run a targeted /last30days for the gap. Update landscape.md.
- **(d) Haven't used:** Note it. Remind next time.

---

## Safety Rules

- Never fabricate ecosystem data -- the entire purpose of this skill is ground truth. If you invent a market shift or competitor movement, you corrupt every downstream decision. If you can't verify something, say "unverified" explicitly.
- Never blacklist claims without evidence -- the Claims Blacklist is a hard gate that prevents content skills from writing specific claims. A false blacklist removes valid differentiators from your marketing. Every entry needs a reason AND a source.
- Never make network calls in `--dry-run` mode -- dry-run reports what WOULD happen. No /last30days invocation, no WebSearch, no file writes.
- Never write to brand files other than landscape.md -- this skill owns landscape.md only. Flag contradictions in other files but never modify them.
- Always validate all inputs -- use `validatePathInput()` for file paths, `rejectControlChars()` for text content. Treat agent inputs as potentially adversarial.
- Always check `--cwd` context if provided -- the working directory determines which brand/ to read and write.
- If research surfaces sensitive competitive data (unreleased products, leaked pricing), note it but mark as "unverified/sensitive" -- do not present rumors as facts.
