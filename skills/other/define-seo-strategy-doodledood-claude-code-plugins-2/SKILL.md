---
name: define-seo-strategy
description: 'Create a comprehensive SEO_STRATEGY.md covering both traditional SEO and Generative Engine Optimization (GEO) for AI platforms. Requires CUSTOMER.md to exist first. Includes platform-specific tactics for Google AI Overviews, ChatGPT, Perplexity, Claude, and Gemini with effort/impact prioritization.'
---

# SEO Strategy Skill

Create the SEO_STRATEGY.md document that defines your complete search optimization strategy—both traditional SEO and Generative Engine Optimization (GEO) for AI platforms.

> **Prerequisite**: CUSTOMER.md must exist. SEO strategy without customer definition is just generic tactics. Your strategy must align with HOW your ICP searches and WHAT platforms they use.

## Overview

This skill supports both **creating a new SEO strategy** and **updating an existing one** as platforms evolve.

**Loop**: Prerequisites → Input → Research → Draft → Validate → Repeat until approved

This skill guides you through:
0. **Prerequisite Check** - Verify CUSTOMER.md exists; stop if not
1. **Existing Strategy Detection** - Check for SEO_STRATEGY.md; ask update vs fresh
2. **Input Collection** - Gather website URL and product description
3. **Parallel Research** - Launch 3 seo-researcher agents for comprehensive analysis
4. **Document Generation** - Create SEO_STRATEGY.md with prioritized recommendations
5. **Validation Loop** - Review sections with user, incorporate feedback
6. **Finalization** - Add version history once approved

**Research log**: `/tmp/seo-research-{YYYYMMDD-HHMMSS}.md` - external memory updated after each step.

## Core Concepts

### Traditional SEO vs GEO

**Traditional SEO**: Optimizing for clicks from search engine results pages (SERPs). Focus on rankings, click-through rates, and organic traffic.

**GEO (Generative Engine Optimization)**: Optimizing for citations in AI-generated responses. Focus on being the source that ChatGPT, Perplexity, Google AI Overviews, Claude, and Gemini cite when answering questions.

**Key difference**: SEO optimizes for clicks. GEO optimizes for citations. Both matter, but they require different tactics.

### Platform Landscape (2025)

| Platform | Citation Style | Key Preferences |
|----------|---------------|-----------------|
| **Google AI Overviews** | Integrated with organic results | Structured content, schema markup, top 10 ranking |
| **ChatGPT** | Reference-heavy | Wikipedia, authoritative sources, E-E-A-T |
| **Perplexity** | Transparent citations | UGC (Reddit), clear structure, comparisons |
| **Claude** | Authoritative sources | Well-structured, information-dense content |
| **Gemini** | Knowledge graph integration | Similar to Google AI Overviews |

## Workflow

### Initial Setup (create todos immediately)

**Create todo list** - areas to research/validate, not fixed steps.

**Starter todos**:
```
- [ ] Prerequisite check (CUSTOMER.md); done when CUSTOMER.md read or created
- [ ] Existing strategy detection→log; done when existing strategy assessed
- [ ] Input collection→log; done when user inputs captured
- [ ] Research→log; done when keyword/competitor research complete
- [ ] Generate initial draft; done when draft created
- [ ] Validation→log; done when user approves direction
- [ ] Refresh: read full research log
- [ ] Finalize document; done when SEO_STRATEGY.md written
```

**Create research log** at `/tmp/seo-research-{YYYYMMDD-HHMMSS}.md`:

```markdown
# SEO Research Log
Started: {timestamp}

## Customer Context
(from CUSTOMER.md)

## Research Findings
(populated by agents)

## Validation Feedback
(populated during review)

## Decisions Made
(populated incrementally)
```

### Phase 0: Prerequisite Check

**Mark "Prerequisite check" todo `in_progress`.**

**CRITICAL**: Before anything else, check for CUSTOMER.md:

1. Use Glob to search for `**/CUSTOMER.md` in the current directory
2. **If NOT found**: Stop immediately and inform the user:

```
I can't create an SEO strategy without knowing WHO you're targeting.

Please create your CUSTOMER.md first using /define-customer.

SEO strategy without customer definition is just generic tactics—it won't resonate with anyone specific or help you prioritize.
```

Do NOT proceed. End the workflow here.

3. **If found**: Read the CUSTOMER.md and extract key context:
   - ICP definition (who they are)
   - Pain points (what problems they have)
   - Current state (what they do today)
   - Triggers (what makes them search)
   - What they value in a solution

Also check for BRAND_GUIDELINES.md:
- Use Glob to search for `**/BRAND_GUIDELINES.md`
- If found, read it for voice/tone context to align content recommendations

**Append to research log**:
```markdown
## Customer Context
**ICP**: {summary from CUSTOMER.md}
**Pain points**: {key pain points}
**Triggers**: {what makes them search}
**Brand voice**: {from BRAND_GUIDELINES.md if found}
```

**Mark "Prerequisite check" todo `completed`.**

### Phase 1: Existing Strategy Detection

**Mark "Existing strategy detection" todo `in_progress`.**

Check for existing SEO_STRATEGY.md:

1. Use Glob to search for `**/SEO_STRATEGY.md`
2. **If found**: Ask user what to do:

```
header: "Existing SEO Strategy Found"
question: "I found an existing SEO_STRATEGY.md. What would you like to do?"
options:
  - "Update it - refresh with latest platform data and recommendations (Recommended)"
  - "Start fresh - create a new strategy from scratch"
  - "Review it - just read through what's there"
```

**If "Update it"**: Read existing strategy, note what's implemented vs pending, focus research on platform changes and gaps.

**If "Start fresh"**: Proceed to Phase 2 (will overwrite existing).

**If "Review it"**: Display the strategy, then ask what to do next.

3. **If NOT found**: Proceed directly to Phase 2.

**Mark "Existing strategy detection" todo `completed`.**

### Phase 2: Input Collection

**Mark "Input collection" todo `in_progress`.**

Collect required inputs via AskUserQuestion.

**Question 1: Website URL** (Required)

```
header: "Website URL"
question: "What's the URL of the website/product you want to optimize?"
freeText: true
placeholder: "e.g., https://myproduct.com"
```

**Question 2: Product Description** (If not clear from CUSTOMER.md)

```
header: "Product Description"
question: "Briefly describe what your product/service does (if not already clear from CUSTOMER.md)"
freeText: true
placeholder: "e.g., 'AI-powered code review tool for Python developers'"
```

**Question 3: Top Competitors** (Optional, helps focus research)

```
header: "Competitors"
question: "Who are your top 2-3 competitors? (Optional - helps focus research)"
freeText: true
placeholder: "e.g., 'Competitor A (competitor-a.com), Competitor B (competitor-b.com)'"
```

**Question 4: Current SEO Status**

```
header: "Current SEO Status"
question: "What's your current SEO situation?"
options:
  - "Starting from scratch - no SEO work done yet (Recommended for new products)"
  - "Some basics - have content but not optimized"
  - "Intermediate - doing traditional SEO, want to add GEO"
  - "Advanced - strong SEO, need cutting-edge GEO tactics"
```

**After input collection, append to research log**:
```markdown
## Inputs Collected
**Website**: {URL}
**Product**: {description}
**Competitors**: {list}
**Current status**: {level}
```

**Mark "Input collection" todo `completed`.**

### Phase 3: Parallel Research

**Mark "Research" todo `in_progress`.**

Launch 3 seo-researcher agents in parallel. Send all three agent invocations in a single message.

**IMPORTANT**: Use the `seo-researcher` agent for each research task.

**Agent 1: Industry Analysis**

```
Launch Task agent (subagent_type: seo-researcher) with prompt:

"Research SEO and GEO best practices for [industry from CUSTOMER.md].

Context:
- Product: [product description]
- ICP: [from CUSTOMER.md]
- Competitors: [if provided]

Focus on:
1. Industry-specific SEO patterns that work
2. Content formats that perform well in this vertical
3. Authority signals and trust factors for this industry
4. Common search queries and keywords
5. Industry-specific schema markup recommendations

Return structured findings with confidence levels."
```

**Agent 2: Competitor Structure Analysis**

```
Launch Task agent (subagent_type: seo-researcher) with prompt:

"Analyze competitor content structure and SEO patterns.

Competitors to analyze: [competitor URLs if provided, or research top competitors in the space]
Industry: [from CUSTOMER.md]

Focus on:
1. Content structure patterns (headings, lists, tables, answer capsules)
2. Schema markup usage
3. Third-party presence (Reddit mentions, review sites, listicles)
4. Content freshness and update patterns
5. Gaps and opportunities they're missing

Return structured findings with specific observations."
```

**Agent 3: Platform Requirements Analysis**

```
Launch Task agent (subagent_type: seo-researcher) with prompt:

"Research current citation requirements and patterns for each AI platform.

Context:
- Industry: [from CUSTOMER.md]
- Product type: [product description]

For EACH platform (Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini), research:
1. How the platform selects sources to cite
2. Content format preferences
3. Authority signals that matter
4. Specific optimization tactics
5. Anti-patterns to avoid

Use 2025+ data only. Return structured findings per platform."
```

**Research Synthesis**

After all agents complete:

1. Combine findings into a unified research summary
2. Identify patterns across all three research streams
3. Note any conflicts or uncertainties
4. Present summary to user:

```
header: "Research Summary"
question: "Here's what the research found. Does this align with your understanding?"
[Display: Key findings across industry, competitors, and platforms]
options:
  - "Yes - this matches my understanding (Recommended)"
  - "Mostly - some insights are new or surprising"
  - "No - this doesn't match my market"
```

If "Mostly" or "No": Ask what's different and incorporate adjustments.

**Append to research log**:
```markdown
## Research Findings
### Industry Analysis
{summary from Agent 1}

### Competitor Analysis
{summary from Agent 2}

### Platform Requirements
{summary from Agent 3}

### User validation
{matches/differs from user understanding}
```

**Mark "Research" todo `completed`.**

### Phase 4: Document Generation

**Mark "Generate initial draft" todo `in_progress`.**

Generate SEO_STRATEGY.md based on research and user context.

**Document Structure:**

```markdown
# SEO & GEO Strategy: [Product Name]

Generated: [Date]
Last Updated: [Date]

> **TL;DR**: [3-5 priority actions with expected impact]

---

## Executive Summary

### Current State Assessment
[Based on website URL analysis and user input]

### Top Priority Actions

| Priority | Action | Effort | Impact | Platform |
|----------|--------|--------|--------|----------|
| 1 | [Specific action] | Low/Med/High | Low/Med/High | [Which platforms] |
| 2 | [Specific action] | Low/Med/High | Low/Med/High | [Which platforms] |
| 3 | [Specific action] | Low/Med/High | Low/Med/High | [Which platforms] |
| 4 | [Specific action] | Low/Med/High | Low/Med/High | [Which platforms] |
| 5 | [Specific action] | Low/Med/High | Low/Med/High | [Which platforms] |

### Expected Outcomes
[What success looks like - specific metrics or indicators]

---

## Customer-Aligned Strategy

### How Your ICP Searches
[Based on CUSTOMER.md - questions they ask, platforms they use, language they use]

### Content Topics That Resonate
[Topics aligned with ICP pain points and triggers]

### Authority Signals Your ICP Trusts
[What makes sources credible to your specific ICP]

---

## Traditional SEO Foundation

### Technical SEO Requirements

**Schema Markup:**
- [Specific schema types to implement]
- [Priority order]

**Site Structure:**
- [URL structure recommendations]
- [Internal linking strategy]

**Performance:**
- [Core Web Vitals targets]
- [Mobile optimization requirements]

### Content Strategy

**Topic Priorities:**
| Topic | ICP Alignment | Search Volume Signal | Priority |
|-------|--------------|---------------------|----------|
| [Topic 1] | [Why it matters to ICP] | [High/Med/Low] | [1-5] |

**Content Formats:**
- [Format 1]: [Why it works for this industry]
- [Format 2]: [Why it works for this industry]

**Publishing Cadence:**
[Recommended frequency with rationale]

### Authority Building

**Backlink Opportunities:**
- [Specific targets based on industry research]

**Citation Targets:**
- [Publications, directories, aggregators]

**Third-Party Presence:**
- [Reddit strategy]
- [Industry publications]
- [Review sites]

---

## Platform-Specific GEO

### Google AI Overviews

**How It Selects Sources:**
[Current understanding from research]

**Content Format Preferences:**
- [Specific formats that get cited]
- [Structure recommendations]

**Optimization Tactics:**
1. [Tactic with implementation details]
2. [Tactic with implementation details]

**Anti-Patterns to Avoid:**
- [What hurts citation chances]

---

### ChatGPT

**How It Selects Sources:**
[Current understanding from research]

**Content Format Preferences:**
- [Specific formats that get cited]
- [Structure recommendations]

**Optimization Tactics:**
1. [Tactic with implementation details]
2. [Tactic with implementation details]

**Anti-Patterns to Avoid:**
- [What hurts citation chances]

---

### Perplexity

**How It Selects Sources:**
[Current understanding from research]

**Content Format Preferences:**
- [Specific formats that get cited]
- [Structure recommendations]

**Optimization Tactics:**
1. [Tactic with implementation details]
2. [Tactic with implementation details]

**Anti-Patterns to Avoid:**
- [What hurts citation chances]

---

### Claude

**How It Selects Sources:**
[Current understanding from research]

**Content Format Preferences:**
- [Specific formats that get cited]
- [Structure recommendations]

**Optimization Tactics:**
1. [Tactic with implementation details]
2. [Tactic with implementation details]

**Anti-Patterns to Avoid:**
- [What hurts citation chances]

---

### Gemini

**How It Selects Sources:**
[Current understanding from research]

**Content Format Preferences:**
- [Specific formats that get cited]
- [Structure recommendations]

**Optimization Tactics:**
1. [Tactic with implementation details]
2. [Tactic with implementation details]

**Anti-Patterns to Avoid:**
- [What hurts citation chances]

---

## Content Recommendations

### High-Priority Content Pieces

| Content Piece | Type | Effort | Impact | Platforms Served |
|---------------|------|--------|--------|------------------|
| [Title/Topic] | [Blog/FAQ/Comparison/etc] | L/M/H | L/M/H | [Platforms] |

### Content Structure Templates

**Answer Capsule Format:**
```
[Question as H2]
[2-3 sentence direct answer - this is what AI cites]
[Expanded explanation with details]
[Supporting data/examples]
```

**FAQ Structure:**
```
## Frequently Asked Questions

### [Question 1]
[Direct answer in first sentence]
[Supporting details]

### [Question 2]
...
```

**Comparison Table Format:**
```
| Feature | [Option A] | [Option B] | [Your Product] |
|---------|-----------|-----------|----------------|
| [Feature 1] | [Value] | [Value] | [Value] |
```

### Schema Markup Recommendations

**Priority Schema Types:**
1. [Schema type] - [Why/Where to use]
2. [Schema type] - [Why/Where to use]

---

## Third-Party Presence Strategy

### Platforms to Prioritize

| Platform | Why It Matters | Strategy | Effort |
|----------|---------------|----------|--------|
| Reddit | [AI platforms cite Reddit heavily] | [Specific subreddits, approach] | [L/M/H] |
| [Platform 2] | [Reason] | [Strategy] | [L/M/H] |

### Wikipedia / Knowledge Panel
[If applicable - strategy for establishing presence]

### Listicle and Review Opportunities
[Specific targets for getting mentioned in roundups]

---

## Implementation Roadmap

### Quick Wins (Low Effort, High Impact)
Start here - these deliver results fastest.

1. **[Action]** - [Why it's high impact, low effort]
2. **[Action]** - [Why it's high impact, low effort]
3. **[Action]** - [Why it's high impact, low effort]

### Strategic Investments (High Effort, High Impact)
Plan these into your roadmap.

1. **[Action]** - [Why it's worth the effort]
2. **[Action]** - [Why it's worth the effort]

### Maintenance (Low Effort, Low Impact)
Do these after the above are done.

1. **[Action]**
2. **[Action]**

### Skip These (High Effort, Low Impact)
Not worth prioritizing now.

1. **[Action]** - [Why to skip]

---

## Anti-Patterns

### What NOT to Do

| Anti-Pattern | Why It Hurts | What to Do Instead |
|--------------|-------------|-------------------|
| [Bad practice] | [Consequence] | [Better approach] |

### Platform-Specific Pitfalls

- **Google AI Overviews**: [Specific pitfall]
- **ChatGPT**: [Specific pitfall]
- **Perplexity**: [Specific pitfall]

---

## Refresh Cadence

AI platforms evolve rapidly. This strategy should be refreshed quarterly.

**Next Review**: [Date + 3 months]

**Signals to refresh sooner:**
- Major platform algorithm changes announced
- Significant drop in AI-referred traffic
- New AI search platforms gain traction
- Industry landscape shifts

---

## Version History

- **v1.0** - [Date] - Initial creation

---

## Quick Reference

**One-liner**: [Core strategy in one sentence]

**Decision checklist for new content:**
- [ ] Does this serve our ICP's search intent?
- [ ] Is it structured for AI citation (answer capsule, FAQ, etc.)?
- [ ] Does it include appropriate schema markup?
- [ ] Is it published on a page with strong internal linking?
- [ ] Have we considered third-party distribution?
```

**Effort/Impact Definitions:**

| Level | Effort Definition | Impact Definition |
|-------|------------------|-------------------|
| **Low** | < 1 day of work | Marginal visibility improvement |
| **Medium** | 1-5 days of work | Noticeable improvement in citations/traffic |
| **High** | > 5 days of work | Significant citation/traffic increase |

Write the document to the current working directory as `SEO_STRATEGY.md`.

**Mark "Generate initial draft" todo `completed`.**

### Phase 5: Validation Loop

**Mark "Validation" todo `in_progress`.**

After generating the initial document, validate major sections with the user.

### Validation Loop

For each validation section:
1. Mark current section validation `in_progress`
2. Ask validation question (AskUserQuestion)
3. **Write feedback immediately** to research log
4. If not "Yes": add todo for that section's revision
5. Update SEO_STRATEGY.md
6. Mark section `completed`
7. Repeat until user approves

**NEVER proceed without writing feedback to log** — research log is external memory.

**Section 1: Executive Summary**

```
header: "Executive Summary"
question: "Do these priority actions feel right for your situation?"
[Display: Top 5 priority actions with effort/impact]
options:
  - "Yes - these priorities make sense (Recommended)"
  - "Mostly - but some adjustments needed"
  - "No - priorities are off"
```

If not "Yes": Ask what to adjust and update.

**Section 2: Platform-Specific Sections**

```
header: "Platform Strategy"
question: "Do the platform-specific recommendations make sense?"
[Display: Summary of each platform's key tactics]
options:
  - "Yes - these look actionable (Recommended)"
  - "Mostly - some platforms need adjustment"
  - "No - need to rethink platform approach"
```

If not "Yes": Ask which platforms need adjustment and why.

**Section 3: Implementation Roadmap**

```
header: "Implementation Roadmap"
question: "Is this roadmap helpful for planning your work?"
[Display: Quick Wins and Strategic Investments]
options:
  - "Yes - clear path forward (Recommended)"
  - "Mostly - need to reprioritize some items"
  - "No - roadmap doesn't fit my constraints"
```

If not "Yes": Ask about constraints and reprioritize.

**Completion Check:**

```
header: "Finalize Strategy?"
question: "Ready to finalize the SEO strategy?"
options:
  - "Yes - strategy is complete (Recommended)"
  - "No - let's review another section"
```

If "No": Return to relevant section review.

**After each section validation, append to research log**:
```markdown
### Validation: {section name}
**Feedback**: {user's response}
**Adjustments requested**: {if any}
**Changes made**: {summary}
```

**Mark "Validation" todo `completed`.**

### Phase 6: Finalization

**Mark "Finalize document" todo `in_progress`.**

When user approves:

1. Read the full research log file to restore all findings, decisions, and rationale into context
2. Update version history with creation date
3. Set next review date (3 months out)
4. Display completion summary:

```
## SEO Strategy Complete

Your SEO_STRATEGY.md has been created with:
- [X] priority actions identified
- [X] platform-specific tactics for [platforms]
- [X] effort/impact scoring for prioritization

**Start with Quick Wins:**
1. [First quick win]
2. [Second quick win]
3. [Third quick win]

**Next review**: [Date]

Run /define-seo-strategy again to update the strategy as platforms evolve.
```

**Append to research log**:
```markdown
## Completion
Finished: {timestamp} | Research agents: 3 | Validation cycles: {count}
## Summary
{Brief summary of SEO strategy creation}
```

**Mark "Finalize document" todo `completed`. Mark all todos complete.**

## Key Principles

| Principle | Rule |
|-----------|------|
| **Write before proceed** | Write findings to research log BEFORE next step; every validation feedback → log; update after EACH phase |
| **Todo-driven** | Create todos for phases; expand when validation reveals issues; never keep mental notes |
| **Customer-aligned** | Every recommendation ties to ICP searches; content matches pain points; authority signals ICP trusts |
| **Actionable** | No generic advice; every tactic has implementation details; effort/impact scoring |
| **Platform-aware** | Each AI platform has unique patterns; tactics tailored per platform; anti-patterns explicit |
| **Current data** | 2025+ research only; platforms evolve rapidly; strategy includes refresh cadence |
| **Reduce cognitive load** | Recommended option first; multi-choice over free-text; limit questions to essentials |

### Never Do

- Proceed without writing findings to research log
- Keep discoveries as mental notes instead of todos
- Skip todo list
- Finalize with unvalidated sections
- Skip research phase (it's the core value)
- Forget to expand todos when validation reveals issues

## Output Location

Write `SEO_STRATEGY.md` to the current working directory (or user-specified path).
