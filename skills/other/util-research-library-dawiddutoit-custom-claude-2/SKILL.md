---
name: util-research-library
description: Provides Systematic library evaluation with emphasis on readability, actionable insights, and informed decision-making. Use when asked "should we use X", "is there a better library", during security audits, or making migration decisions. Produces concise, scannable reports that drive adoption decisions - not walls of text.
allowed-tools:
  - Read
  - mcp__context7__get-library-docs
  - mcp__context7__resolve-library-id
  - WebSearch
  - mcp__project-watch-mcp__search_code
  - mcp__memory__create_entities
---

# Library Research & Evaluation

## Purpose

Systematic library evaluation framework that produces readable, actionable decision briefs for library adoption, migration, and upgrade decisions using a 6-dimension research methodology.

## Quick Start

**Create readable, actionable research that drives informed decisions.**

This skill is about **research methodology** - knowing what to look for, where to find it, how to synthesize it, and how to present it. The goal is NOT to dump data, but to **accelerate time to adoption** through clear, confident recommendations.

**Most common use case:**
```
User: "Should we use Pydantic v2?"

→ Research 6 dimensions (docs, updates, alternatives, security, community, codebase)
→ Score each with evidence
→ Deliver decision brief with clear ADOPT/MIGRATE/STAY/AVOID recommendation

Result: 40 minutes (vs 2-4 hours ad-hoc research)
```

## Table of Contents

1. [When to Use This Skill](#when-to-use-this-skill)
2. [What This Skill Does](#what-this-skill-does)
3. [Instructions](#instructions)
4. [Research Framework (6 Dimensions)](#research-framework-6-dimensions)
5. [Output Format: Decision Brief](#output-format-decision-brief)
6. [Usage Examples](#usage-examples)
7. [Expected Outcomes](#expected-outcomes)
8. [Integration Points](#integration-points)
9. [Expected Benefits](#expected-benefits)
10. [Success Metrics](#success-metrics)
11. [Requirements](#requirements)
12. [Troubleshooting](#troubleshooting)
13. [Red Flags to Avoid](#red-flags-to-avoid)

---

## When to Use This Skill

Use this skill when:
- **Adoption decisions:** "Should we use library X?"
- **Migration decisions:** "Should we switch from X to Y?"
- **Upgrade decisions:** "Should we upgrade to version Z?"
- **Security audits:** "Are our dependencies safe?"
- **Performance optimization:** "Is there a faster alternative?"
- **Technology evaluation:** "What's the best tool for this job?"

---

## What This Skill Does

This skill provides systematic library evaluation through:

1. **Research 6 dimensions** - Official docs, recent updates, alternatives, security, community, codebase usage
2. **Score with evidence** - Each dimension rated 1-10 with specific supporting data
3. **Synthesize decision** - Clear ADOPT/MIGRATE/UPGRADE/STAY/AVOID recommendation
4. **Deliver decision brief** - Scannable report with TL;DR, decision matrix, action items
5. **Time-boxed process** - Complete research in ~40 minutes (vs 2-4 hours ad-hoc)

See Instructions section below for detailed step-by-step workflow.

---

## Instructions

### Phase 1: Gather (15 minutes)

**Goal:** Collect evidence across 6 research dimensions

**Steps:**

1. **Context**: Read `pyproject.toml` for existing libraries and Context7 IDs
2. **Docs**: Get official docs (check pyproject.toml first, then resolve-library-id)
3. **Updates**: WebSearch for recent changes, changelogs
4. **Alternatives**: WebSearch for comparisons, discussions
5. **Security**: WebSearch for CVEs, advisories
6. **Community**: WebSearch on reddit, HN, GitHub, StackOverflow
7. **Codebase**: Search current usage patterns

### Phase 2: Synthesize (10 minutes)

**Goal:** Transform evidence into clear decision

**Steps:**

1. **Score each dimension** (1-10) with specific evidence
2. **Identify decision driver** (what matters most?)
3. **Determine recommendation** (ADOPT/MIGRATE/UPGRADE/STAY/AVOID)
4. **Assess confidence** (High/Medium/Low)
5. **List action items** (what happens next?)

### Phase 3: Write (15 minutes)

**Goal:** Create scannable decision brief

**Steps:**

1. **TL;DR**: Write last, summarize the decision
2. **Decision Matrix**: Fill in scores and evidence
3. **Recommendation**: State decision and rationale
4. **Action Items**: Specific, assignable tasks
5. **Supporting Evidence**: Details for skeptics
6. **References**: Links for deep dive

**Total time: ~40 minutes** (vs 1-2 hours of ad-hoc research)

---

## Core Principles

### 1. **Readability First**
- ❌ Walls of text, data dumps, exhaustive lists
- ✅ Scannable sections, bullet points, clear structure
- ✅ Executive summary fits in one screen
- ✅ Each section answers ONE question

### 2. **Decision-Focused**
- Every fact must support a decision
- If it doesn't change the recommendation, cut it
- Lead with "SO WHAT?" not "WHAT?"
- Clear action items, not observations

### 3. **Confidence Over Completeness**
- Better to be 80% confident with 6 sources than 60% with 20 sources
- Quality of sources > quantity
- Synthesize, don't concatenate

### 4. **Time to Value**
- Reader should know the recommendation in 30 seconds
- Supporting evidence in 3 minutes
- Full context in 10 minutes
- Everything else is noise

---

## Usage Examples

### Example 1: Adoption Decision

**Scenario:** User asks: "Should we use Pydantic v2 for data validation?"

**Process:**
1. Research 6 dimensions: docs, updates, alternatives, security, community, codebase
2. Score each dimension with evidence
3. Synthesize into decision brief

**Outcome:**
```
📋 TL;DR
Recommendation: ✅ ADOPT
Confidence: High (8/10)
Key insight: Production-ready, 20x faster, easy migration

🎯 Decision Matrix: 8.2/10 overall
🚀 Action Items: POC this week, migrate next month
```

**Time:** ~40 minutes (vs 2-4 hours ad-hoc research)

---

### Example 2: Migration Decision

**Scenario:** User asks: "Should we migrate from Neo4j to Memgraph?"

**Outcome:**
```markdown
📋 TL;DR
Recommendation: ❌ STAY
Confidence: High (8/10)
Key insight: Neo4j meets needs, migration cost high, unclear benefit

🎯 Decision Matrix:
| Dimension | Neo4j | Memgraph | Winner |
|-----------|-------|----------|--------|
| Functionality | 9/10 | 8/10 | Neo4j |
| Performance | 8/10 | 9/10 | Memgraph |
| Maturity | 10/10 | 6/10 | Neo4j |
| Migration Cost | N/A | 3/10 | Neo4j |

🚀 When to Reconsider: If query performance drops below SLA
```

---

### Example 3: Security Audit

**Scenario:** User asks: "Audit our dependencies for security issues"

**Outcome:** Security report for each dependency with:
- CVE status (none found / issues identified)
- Latest version check
- Upgrade recommendations
- Priority ranking (critical/high/medium/low)

---

## Research Framework (6 Dimensions)

### 1. **Official Documentation** (Context7)
**Question:** Does it do what we need?

- Check `pyproject.toml [tool.context7]` FIRST for existing library ID
- If not found, use `resolve-library-id`
- Focus search on specific use case (e.g., "async patterns", "performance tuning")
- Extract: capabilities, limitations, best practices

### 2. **Recent Developments** (WebSearch)
**Question:** Is it actively maintained and improving?

- Last 6 months of updates (use current year from env)
- Changelog, release notes, roadmap
- Breaking changes, deprecations
- Extract: momentum, stability, future-proofing

### 3. **Alternatives** (WebSearch)
**Question:** Is this the best tool for the job?

**Sources:**
- General: `best {category} 2025 comparison benchmark`
- Head-to-head: `{lib} vs {alternative} 2025` (db-engines.com, github.com)
- Community: `{lib} vs {alternative} discussion` (reddit.com, news.ycombinator.com)

Extract: competitive positioning, trade-offs, deal-breakers

### 4. **Security** (WebSearch)
**Question:** Is it safe to use?

**Sources:**
- CVEs: `{lib} CVE vulnerability 2025` (nvd.nist.gov, snyk.io)
- Advisories: `{lib} security advisory 2025` (github.com)

Extract: known vulnerabilities, security track record, response time

### 5. **Community Health** (WebSearch)
**Question:** Will we get support when we need it?

**Trusted sources:**
- **reddit.com**: Real-world experiences, gotchas, war stories
- **news.ycombinator.com**: Technical discourse, deep dives
- **github.com**: Issues, PRs, responsiveness, contributor activity
- **stackoverflow.com**: Common problems, solutions, adoption

**Searches:**
- Adoption: `{lib} adoption trends 2025`
- Experiences: `{lib} experiences 2025` (reddit.com)
- Discussion: `{lib} discussion 2025` (news.ycombinator.com)
- Issues: `{lib} problems issues 2025` (github.com, stackoverflow.com)

Extract: community size, responsiveness, common pain points, maturity

### 6. **Current Usage** (Codebase)
**Question:** How does this fit with what we already have?

- Semantic search: `{lib} usage patterns`
- Import count: How widely used?
- Migration effort: What needs to change?

Extract: integration complexity, migration cost, team familiarity

---

## Output Format: Decision Brief

### Template Structure

```markdown
# Library Evaluation: {Name}

## 📋 TL;DR (30-second read)

**Recommendation:** [ADOPT / MIGRATE / UPGRADE / STAY / AVOID]
**Confidence:** [High/Medium/Low] (8/10)
**Priority:** [Critical/High/Medium/Low]
**Time to Adopt:** [Days/Weeks/Months]

**One-sentence summary:** {What it is and why it matters}

**Key insight:** {The one thing that drives the recommendation}

---

## 🎯 Decision Matrix (3-minute read)

| Dimension | Score | Evidence | Impact |
|-----------|-------|----------|--------|
| **Functionality** | ⭐⭐⭐⭐⭐ 9/10 | Does X, Y, Z | ✅ Meets all requirements |
| **Performance** | ⭐⭐⭐⭐ 8/10 | 20% faster than current | ✅ Significant improvement |
| **Security** | ⭐⭐⭐⭐⭐ 10/10 | No CVEs, active patches | ✅ Production-ready |
| **Community** | ⭐⭐⭐⭐ 8/10 | 50K GitHub stars, active | ✅ Strong support |
| **Maturity** | ⭐⭐⭐ 6/10 | v2.0, 3 years old | ⚠️ Some rough edges |
| **Migration** | ⭐⭐⭐⭐ 8/10 | 2-3 days effort | ✅ Low risk |

**Overall:** 8.2/10 - **Strong recommendation**

---

## ✅ Recommendation

**{DECISION}**: {Clear action statement}

**Why:**
1. {Primary reason - the deal-maker}
2. {Secondary reason - supporting evidence}
3. {Tertiary reason - nice-to-have}

**Why not alternatives:**
- {Alt 1}: {Specific disqualifying reason}
- {Alt 2}: {Specific disqualifying reason}

**Risks & Mitigations:**
- ⚠️ {Risk}: {Mitigation strategy}
- ⚠️ {Risk}: {Mitigation strategy}

---

## 🚀 Action Items

**Immediate (this week):**
1. [ ] {Specific action with owner}
2. [ ] {Specific action with owner}

**Short-term (this month):**
1. [ ] {Specific action}
2. [ ] {Specific action}

**Long-term (this quarter):**
1. [ ] {Specific action}

---

## 📊 Supporting Evidence (10-minute read)

### What We Found

#### ✅ Strengths
- {Specific strength with evidence}
- {Specific strength with evidence}

#### ⚠️ Limitations
- {Specific limitation with workaround}
- {Specific limitation with impact}

#### 🔴 Deal-breakers (if any)
- {What would disqualify this library}

### Community Insights

**From Reddit/HN:**
- {Key insight from real users}
- {Common gotcha or pain point}

**From GitHub:**
- {Issue responsiveness}
- {Active development indicators}

### Alternatives Considered

| Alternative | Why Not? | When to Reconsider |
|-------------|----------|-------------------|
| {Alt 1} | {Disqualifying reason} | {Condition} |
| {Alt 2} | {Disqualifying reason} | {Condition} |

---

## 📚 References

- Official docs: {Context7 library ID}
- GitHub: {URL}
- Key discussions: {URLs to reddit/HN threads}
- Benchmarks: {URLs}
- Security: {CVE/advisory links}

---

## 🔄 Next Review

**When to revisit:**
- {Specific trigger, e.g., "v3.0 release"}
- {Time-based, e.g., "6 months from now"}
- {Condition-based, e.g., "if performance degrades"}
```

---

## Synthesis Guidelines

### What to Include

**Include if:**
- ✅ Directly impacts the decision
- ✅ User will ask "what about X?"
- ✅ Reveals a non-obvious trade-off
- ✅ Prevents a future mistake

**Exclude if:**
- ❌ Common knowledge or easily Googled
- ❌ Doesn't differentiate from alternatives
- ❌ Historical context without current relevance
- ❌ Marketing fluff or hype

### How to Synthesize

1. **Find the signal in the noise**
   - Look for consensus across sources
   - Weight trusted sources (docs, GitHub) > marketing
   - Real user experiences > benchmarks

2. **Identify the decision driver**
   - What's the ONE thing that matters most?
   - What's the deal-maker or deal-breaker?
   - What's the non-obvious insight?

3. **Quantify when possible**
   - "20% faster" > "fast"
   - "50K GitHub stars" > "popular"
   - "v3.0, 5 years old" > "mature"

4. **Be honest about gaps**
   - "No benchmark data available" > assume/guess
   - "Limited community feedback" > extrapolate
   - "Confidence: Medium (6/10)" > overstate

---

## Research Workflow

### Phase 1: Gather (15 minutes)

1. **Context**: Read `pyproject.toml` for existing libraries and Context7 IDs
2. **Docs**: Get official docs (check pyproject.toml first, then resolve-library-id)
3. **Updates**: WebSearch for recent changes, changelogs
4. **Alternatives**: WebSearch for comparisons, discussions
5. **Security**: WebSearch for CVEs, advisories
6. **Community**: WebSearch on reddit, HN, GitHub, StackOverflow
7. **Codebase**: Search current usage patterns

### Phase 2: Synthesize (10 minutes)

1. **Score each dimension** (1-10) with specific evidence
2. **Identify decision driver** (what matters most?)
3. **Determine recommendation** (ADOPT/MIGRATE/UPGRADE/STAY/AVOID)
4. **Assess confidence** (High/Medium/Low)
5. **List action items** (what happens next?)

### Phase 3: Write (15 minutes)

1. **TL;DR**: Write last, summarize the decision
2. **Decision Matrix**: Fill in scores and evidence
3. **Recommendation**: State decision and rationale
4. **Action Items**: Specific, assignable tasks
5. **Supporting Evidence**: Details for skeptics
6. **References**: Links for deep dive

**Total time: ~40 minutes** (vs 1-2 hours of ad-hoc research)

---

## Quality Checklist

Before delivering the report:

- [ ] Can user make decision from TL;DR alone? (30 seconds)
- [ ] Is recommendation clear and confident? (not "it depends")
- [ ] Are scores backed by specific evidence? (not gut feel)
- [ ] Are action items specific and assignable? (not vague)
- [ ] Are risks identified with mitigations? (not ignored)
- [ ] Is it scannable? (bullets, tables, sections)
- [ ] Is it < 2 pages for main content? (not a wall of text)
- [ ] Would you read this if someone else wrote it? (readability test)

---

## Integration Points

### With @researcher Agent
@researcher delegates library research to this skill, focusing on broader architectural questions.

### With ADR Creation
Use this skill's output to populate the "Alternatives Considered" section of ADRs.

### With Security Audits
Run this skill on all dependencies periodically to catch security issues early.

### With pyproject.toml
When researching NEW library (not in `[tool.context7]`):
- **ALWAYS suggest** adding library ID to `pyproject.toml [tool.context7]`
- Format: `{lib} = { id = "{id}", trust = {score}, snippets = {count}, desc = "{desc}" }`
- Creates single source of truth for future research

---

## Success Metrics

### Adoption Metrics
- **Time to decision**: < 1 hour (vs 2-4 hours ad-hoc)
- **Decision confidence**: 8+/10 consistently
- **Decision accuracy**: Right call 90%+ of the time
- **Time to adoption**: Days (vs weeks of analysis paralysis)

### Quality Metrics
- **Readability**: User can scan and understand in < 5 minutes
- **Actionability**: Clear next steps, not open questions
- **Completeness**: All 6 dimensions covered with evidence
- **Reproducibility**: Different researchers reach same conclusion

### Impact Metrics
- **Avoided mistakes**: Caught security issues, performance problems before adoption
- **Faster adoption**: Evidence-based decisions reduce bike-shedding
- **Better outcomes**: Right tool for job, not latest hype

---

## Common Pitfalls

### ❌ Don't:
- Dump all search results into report
- List features without context
- Ignore migration cost
- Assume newer = better
- Skip security checks
- Write for yourself (write for tired, busy reader)

### ✅ Do:
- Synthesize findings into insights
- Explain WHY features matter
- Quantify migration effort
- Evaluate maturity and stability
- Always check CVEs
- Write for skimmers (bullets, tables, sections)

---

## Expected Outcomes

### Successful Research Completion

```
✅ Research Complete

Library: pydantic
Time: 38 minutes
Confidence: High (8/10)

Decision Brief Delivered:
  ✅ TL;DR (30-second read) - Clear recommendation
  ✅ Decision Matrix - 6 dimensions scored with evidence
  ✅ Action Items - Specific, assignable tasks
  ✅ Supporting Evidence - Detailed rationale
  ✅ References - All sources documented

Quality Checks:
  ✅ Can user make decision from TL;DR alone?
  ✅ Is recommendation clear and confident?
  ✅ Are scores backed by specific evidence?
  ✅ Are action items specific and assignable?
  ✅ Are risks identified with mitigations?
  ✅ Is it scannable? (bullets, tables, sections)
  ✅ Is it < 2 pages for main content?

Next Steps:
  1. User reviews decision brief
  2. Team discusses action items
  3. Decision documented in ADR (if adoption)
```

### Insufficient Evidence

```
⚠️  Research Incomplete

Library: obscure-lib
Confidence: Low (4/10)

Issues Found:
  - No official documentation found
  - Limited community feedback (< 10 GitHub stars)
  - No security audit data available
  - No alternatives comparison possible

Recommendation:
  ❌ AVOID - Insufficient evidence for production use

When to Reconsider:
  - If library reaches 1000+ GitHub stars
  - If official documentation published
  - If security audit completed
```

---

## Requirements

**Tools needed:**
- Read - Access pyproject.toml and codebase files
- WebSearch - Research updates, alternatives, security, community
- mcp__context7__get-library-docs - Fetch official documentation
- mcp__context7__resolve-library-id - Resolve library identifiers
- mcp__project-watch-mcp__search_code - Search codebase usage
- mcp__memory__create_entities - Store research findings

**Environment:**
- Context7 configured in pyproject.toml
- Internet access for WebSearch
- Neo4j running (for codebase search)

**Knowledge:**
- Understanding of decision brief format
- Ability to synthesize technical information
- Familiarity with project architecture
- Knowledge of Context7 library registry

**Optional:**
- pyproject.toml management experience
- ADR creation workflow familiarity

---

## Troubleshooting

### Issue: Context7 library ID not found

**Symptom:** `resolve-library-id` returns no results

**Solutions:**
1. Check library name spelling (exact match required)
2. Search Context7 registry manually: `mcp__context7__search-libraries`
3. Use WebSearch as fallback for official docs
4. **ALWAYS suggest** adding library ID to `pyproject.toml [tool.context7]` after resolving

**Example:**
```toml
[tool.context7]
pydantic = { id = "pydantic_pydantic", trust = 90, snippets = 20, desc = "Data validation" }
```

---

### Issue: Conflicting recommendations from sources

**Symptom:** Reddit says "avoid", GitHub shows active development, docs look professional

**Solutions:**
1. **Weight trusted sources higher** - Official docs, GitHub > Reddit opinions
2. **Look for recency** - 2025 opinions > 2023 opinions
3. **Identify context** - Reddit complaint about v1, you're researching v2
4. **Be honest about conflict** - Note in decision brief: "Mixed community feedback"
5. **Adjust confidence score** - Lower from High to Medium if significant conflict

---

### Issue: No recent updates found

**Symptom:** Last release was 2+ years ago

**Questions to ask:**
1. Is library mature/stable (intentionally low churn)?
2. Is library abandoned (no issue responses, PRs ignored)?
3. Check GitHub: Last commit date, issue response time
4. Check alternatives: Are competitors more active?

**Decision impact:**
- If mature: ✅ May still be good choice
- If abandoned: ❌ AVOID or MIGRATE away

---

### Issue: Decision brief too long (> 2 pages)

**Symptom:** Supporting Evidence section has walls of text

**Solutions:**
1. **Ruthlessly cut** - If it doesn't change the decision, remove it
2. **Move to references** - Create `research-{lib}.md` in session workspace
3. **Use bullets** - Convert paragraphs to scannable bullet points
4. **Focus on signal** - What's the ONE thing that matters most?

**Target length:**
- TL;DR: 1 screen
- Decision Matrix: 1 screen
- Full brief: < 2 pages

---

## Red Flags to Avoid

### Research Process

1. **Dumping raw data** - Synthesize findings, don't copy-paste search results
2. **No clear recommendation** - Always have ADOPT/MIGRATE/UPGRADE/STAY/AVOID decision
3. **Vague action items** - "Consider using" → "POC this week with John on auth module"
4. **Ignoring security** - Always check CVEs, even if library looks safe
5. **Assuming newer = better** - Maturity and stability matter
6. **Skipping migration cost** - Easy adoption ≠ easy migration
7. **Cherry-picking evidence** - Include both strengths and limitations
8. **Writing for yourself** - Write for tired, busy reader who skims

### Decision Brief Quality

9. **Walls of text** - Use bullets, tables, sections for scannability
10. **Missing confidence score** - Always include High/Medium/Low with /10 rating
11. **No "when to reconsider"** - Document conditions for revisiting decision
12. **Broken references** - Verify all links work before delivering
13. **Marketing fluff** - Focus on evidence, not hype
14. **No time estimate** - Include adoption/migration time estimate

### Integration

15. **Not updating pyproject.toml** - Always suggest adding new library IDs to Context7 config
16. **Skipping ADR creation** - Major adoption decisions should have ADRs
17. **No memory storage** - Store research findings in mcp__memory for future reference

---

## Evolution & Improvement

This skill should improve over time:

1. **Track decisions**: Did we make the right call?
2. **Refine criteria**: What dimensions matter most?
3. **Improve synthesis**: What signal did we miss?
4. **Optimize sources**: Which sources had best signal/noise?
5. **Update templates**: What format worked best?

**Feedback loop:** After 6 months, review decisions and update methodology.

---

## Expected Benefits

| Metric | Without Skill | With Skill | Improvement |
|--------|--------------|------------|-------------|
| **Research Time** | 2-4 hours | 40 minutes | 75% faster |
| **Decision Confidence** | 60% (guesswork) | 90% (evidence-based) | 50% increase |
| **Adoption Mistakes** | 30% (wrong library) | 5% (vetted choices) | 83% reduction |
| **Security Issues Caught** | 20% (manual checks) | 95% (systematic CVE search) | 75% improvement |
| **Time to Value** | Days (analysis paralysis) | Hours (clear decision) | 90% faster |
| **Documentation Quality** | Ad-hoc notes | Structured decision brief | 100% coverage |

## Validation Process

### Step 1: Research Validation
```bash
# Verify all 6 dimensions covered
✓ Official Documentation (Context7)
✓ Recent Developments (WebSearch)
✓ Alternatives (WebSearch comparisons)
✓ Security (CVE search)
✓ Community Health (Reddit, HN, GitHub)
✓ Current Usage (codebase search)
```

### Step 2: Decision Matrix Validation
```bash
# Each dimension scored 1-10 with evidence
# Overall score calculated
# Confidence level assigned (High/Medium/Low)
```

### Step 3: Recommendation Validation
```bash
# Clear ADOPT/MIGRATE/UPGRADE/STAY/AVOID decision
# Rationale documented
# Action items specific and assignable
```

### Step 4: Quality Checklist
```bash
# Can user make decision from TL;DR alone? (30 seconds)
# Is recommendation clear and confident?
# Are scores backed by specific evidence?
# Are action items specific and assignable?
# Are risks identified with mitigations?
# Is it scannable? (bullets, tables, sections)
```

### Step 5: Report Delivery
```bash
# Decision brief < 2 pages
# Supporting evidence documented
# References included
# Next review conditions specified
```

## See Also

- [references/date-aware-search.md](./references/date-aware-search.md) - WebSearch strategies for current, relevant information
- [references/research-checklist.md](./references/research-checklist.md) - Comprehensive checklist for all 6 dimensions
- [templates/decision-matrix-template.md](./templates/decision-matrix-template.md) - Copy-paste template for evaluations

---

**Last Updated:** 2025-10-16
**Version:** 2.0 (Renamed from research-sota-library, refocused on methodology)
