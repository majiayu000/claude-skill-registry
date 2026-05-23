---
name: groom
description: |
  Comprehensive backlog grooming. Orchestrates issue-creator skills and agents.
  Creates prioritized GitHub issues across all domains.
  Uses Gemini, Kimi, Codex, and Thinktank to flesh out issues with research,
  implementation recommendations, and multi-perspective validation.
  No flags. Always comprehensive.
---

# /groom

Orchestrate comprehensive backlog grooming. Create prioritized issues across all domains.

## Philosophy

**Orchestrator pattern.** /groom invokes skills, doesn't reimplement logic.

**Unix philosophy.** Small, focused skills that compose. Investigate ≠ Fix.

**AI-augmented analysis.** External AI tools provide specialized capabilities:
- **Gemini** — Web-grounded research, current best practices, huge context
- **Kimi** — Frontend/visual expertise, Agent Swarm for parallel analysis
- **Codex** — Implementation recommendations, concrete code suggestions
- **Thinktank** — Multi-model consensus, diverse expert perspectives

**No flags.** Always runs full audit. Always creates issues.

## What This Does

1. **Load or gather vision** — Check vision.md or ask about product direction
2. **Capture what's on your mind** — Bugs, UX friction, nitpicks from using the app
3. **Audit existing backlog** — Validate, reprioritize, close stale issues
4. **Run issue-creator skills** — Each domain gets audited, issues created
5. **AI-assisted enrichment** — Gemini, Kimi, Codex, Thinktank flesh out issues
6. **Adaptive agent analysis** — Based on backlog size, run specialized agents
7. **Dedupe & consolidate** — Merge duplicates, finalize issue set
8. **Summarize** — Report P0/P1/P2/P3 counts and recommended focus

## Priority System

```
🔴 P0: CRITICAL PRODUCTION BUGS
   └─ Errors actively breaking production
   └─ Critical security vulnerabilities

🟠 P1: FUNDAMENTALS (Foundation)
   ├─ Testing (coverage, quality gates)
   ├─ Documentation (README, architecture)
   ├─ Quality gates (hooks, CI/CD)
   ├─ Observability (logging, error tracking)
   ├─ Product standards (version, attribution, contact)
   └─ Working prototype (not stubs)

🟡 P2: LAUNCH READINESS
   ├─ Compelling landing page
   ├─ Boutique onboarding
   ├─ Stripe monetization
   ├─ Viral growth infrastructure
   └─ Marketing readiness (demo video, brand profile, analytics, distribution prep)

**Marketing Readiness checks:**
- Demo video exists (30-60s screen recording)
- brand-profile.yaml configured
- PostHog events defined (signup, activation, [core_action])
- Distribution drafts prepared (Twitter, Reddit, HN)

🟢 P3+: EVERYTHING ELSE
   └─ Innovation, polish, strategic improvements

⚠️  SECURITY: Own severity scale
   Critical → P0, High → P1, Medium → P2, Low → P3
```

## Process

### Step 1: Load or Gather Vision

Vision should persist across sessions. Check for `vision.md` in project root:

```bash
[ -f "vision.md" ] && echo "Vision found" || echo "No vision.md"
```

**If vision.md exists:**
1. Read and display current vision
2. Ask: "Is this still accurate? Any updates?"
3. If updates provided, rewrite vision.md

**If vision.md doesn't exist:**
1. Ask open-ended question:
   ```
   What's your vision for this product? Where should it go?
   ```
2. Write response to `vision.md`

**vision.md format:**
```markdown
# Vision

## One-Liner
[Single sentence: what this product is and who it's for]

## North Star
[The dream state - what does success look like in 2 years?]

## Key Differentiators
[What makes this different from alternatives?]

## Target User
[Who specifically is this for? Be concrete.]

## Current Focus
[What's the immediate priority this quarter?]

---
*Last updated: YYYY-MM-DD*
*Updated during: /groom session*
```

Store content as `{vision}` for agent context throughout session.

**Why persist vision?**
- Vision shouldn't change dramatically between sessions
- Agents get consistent context
- Creates documentation artifact
- Enables other skills to reference it

### Step 2: Capture What's On Your Mind

Before structured analysis, ask:

```
Anything on your mind? Bugs you've noticed, UX friction, missing features,
nitpicks while using the app? These become issues alongside the automated findings.

(Skip if nothing comes to mind)
```

**What this captures:**
- Bugs encountered during manual testing
- UX friction points noticed while using the app
- Missing features that became obvious
- "Why doesn't this..." observations
- Quality-of-life improvements
- Things that annoyed you today

**For each item provided:**
1. Clarify if needed (one follow-up max)
2. Assign tentative priority based on description
3. Create as GitHub issue with `source: user-observation` tag
4. Include in final summary

**Why this step matters:**
- User has context automation doesn't (how it *feels* to use the app)
- Catches issues that slip through automated checks
- Captures the "I keep meaning to file this" backlog
- Makes groom feel collaborative, not just audit

**Format for user-submitted issues:**

```markdown
## Title
[P{0-3}] {user's description, cleaned up}

## Labels
- priority/p{n}
- domain/{best-fit}
- source/user-observation

## Body
### Problem
{user's observation}

### Context
Reported during /groom session

---
Created by `/groom` (user observation)
```

### Step 3: Audit Existing Backlog

**Critical:** Existing issues are not sacred. They may be stale, irrelevant, misprioritized, or duplicative. Every issue must be validated.

```bash
gh issue list --state open --limit 100 --json number,title,labels,body,createdAt,updatedAt
```

**For each existing issue, evaluate:**

1. **Still relevant?** Does this issue still matter given current vision and codebase state?
   - If NO → Close with explanation
   - If UNCERTAIN → Flag for user confirmation

2. **Priority correct?** Given current vision.md focus, is the priority right?
   - Re-prioritize if focus has shifted
   - P0 from 6 months ago may be P3 now

3. **Description accurate?** Does the issue still describe the actual problem?
   - Update if codebase has changed
   - Flesh out if too vague to act on

4. **Duplicate?** Is this covered by another issue or will be covered by new findings?
   - Consolidate into single issue
   - Close duplicate with link to canonical

5. **Actionable?** Can someone pick this up and know what to do?
   - Add concrete next steps if missing
   - Break down if too large

**Actions to take:**

```bash
# Close irrelevant issue
gh issue close 123 --comment "Closing: no longer relevant. [reason]"

# Update priority
gh issue edit 123 --remove-label "priority/p1" --add-label "priority/p3"

# Update description
gh issue edit 123 --body "Updated description..."

# Close as duplicate
gh issue close 123 --comment "Duplicate of #456"
```

**Output from this step:**
- List of issues kept (with any priority/description changes)
- List of issues closed (with reasons)
- List of issues to consolidate with new findings

This prevents backlog bloat and ensures the backlog reflects current reality.

### Step 4: Run Issue-Creator Skills

Invoke in sequence (each creates GitHub issues):

| Skill | Domain | Priority Range |
|-------|--------|----------------|
| `/log-production-issues` | Production health | P0-P3 |
| `/log-quality-issues` | Tests, CI/CD, hooks | P0-P3 |
| `/log-doc-issues` | Documentation | P0-P3 |
| `/log-observability-issues` | Monitoring, logging | P0-P3 |
| `/log-product-standards-issues` | Version, attribution, contact | P1 |
| `/log-stripe-issues` | Stripe payments | P0-P3 |
| `/log-bitcoin-issues` | Bitcoin on-chain | P0-P3 |
| `/log-lightning-issues` | Lightning Network | P0-P3 |
| `/log-virality-issues` | Sharing, referrals | P0-P3 |
| `/log-landing-issues` | Landing page | P0-P3 |
| `/log-onboarding-issues` | New user experience | P0-P3 |

**Why invoke skills, not reimplement?**
- Each skill has deep domain knowledge
- Consistent output format
- Can be run independently
- Easy to update without changing groom

### Step 5: AI-Assisted Issue Enrichment

After basic issue creation, use external AI tools to flesh out issues with deeper analysis.

**Why external tools?**
- **Gemini**: Web-grounded research for current best practices, framework docs
- **Kimi**: Frontend/visual expertise, can coordinate sub-agents for UI issues
- **Codex**: Implementation recommendations, concrete code suggestions
- **Thinktank**: Multi-model consensus for architecture/design decisions

**Run enrichment by domain:**

```bash
# 1. Gemini: Research current best practices for flagged issues
gemini "Review these issues and research current best practices:
$(gh issue list --label domain/quality --state open --json title,number --jq '.[] | "#\(.number): \(.title)"')

For each issue, provide:
- Current industry best practices (2024-2025)
- Recommended tools/libraries
- Common pitfalls to avoid

Be specific and cite sources."

# 2. Kimi: Analyze frontend/visual issues with Agent Swarm
kimi "Analyze the UI/UX issues in this codebase:
$(gh issue list --label domain/landing,domain/onboarding --state open --json title,number --jq '.[] | "#\(.number): \(.title)"')

For each issue:
- Assess current implementation quality
- Suggest specific visual improvements
- Recommend component patterns" --thinking

# 3. Codex: Generate implementation recommendations
codex "For these technical issues, provide concrete implementation steps:
$(gh issue list --label priority/p0,priority/p1 --state open --json title,number,body --jq '.[:5] | .[] | "### #\(.number): \(.title)\n\(.body)\n"')

For each:
- Specific files to modify
- Code patterns to follow
- Test cases needed" --full-auto

# 4. Thinktank: Multi-perspective validation for architecture issues
thinktank "Evaluate these architecture decisions:
$(gh issue list --label domain/architecture --state open --json title,body --jq '.[] | "## \(.title)\n\(.body)\n"')

Provide:
- Consensus recommendation
- Dissenting opinions worth considering
- Risk assessment" ./src --synthesis
```

**Update issues with findings:**

```bash
# Append Gemini research to issue body
gh issue edit {number} --body "$(gh issue view {number} --json body --jq .body)

---
## Research (Gemini)
{gemini_findings}"

# Add implementation notes from Codex
gh issue comment {number} --body "## Implementation Recommendations (Codex)
{codex_recommendations}"

# Add architecture review from Thinktank
gh issue comment {number} --body "## Architecture Review (Thinktank)
{thinktank_synthesis}"
```

**When to run which tool:**

| Issue Domain | Primary Tool | Why |
|--------------|--------------|-----|
| Quality, Docs, Observability | Gemini | Needs current best practices research |
| Landing, Onboarding, Design | Kimi | Visual/frontend expertise |
| Security, Architecture | Thinktank | Needs multi-perspective validation |
| All P0/P1 technical issues | Codex | Implementation recommendations |

### Step 6: Adaptive Agent Analysis

After issue enrichment, count by priority:

```bash
p0_count=$(gh issue list --label priority/p0 --state open --json number | jq length)
p1_count=$(gh issue list --label priority/p1 --state open --json number | jq length)
total=$((p0_count + p1_count))
```

**Heavy backlog (P0+P1 > 15):**
Run only core agents:
- `security-sentinel` — Security vulnerabilities
- `architecture-guardian` — Structural issues

**Medium backlog (P0+P1 = 5-15):**
Add creative agents:
- `aesthetician` — Visual excellence
- `pioneer` — Innovation opportunities
- `visionary` — Vision acceleration (receives `{vision}`)

**Light backlog (P0+P1 < 5):**
Full suite:
- `product-visionary` — Feature opportunities
- `user-experience-advocate` — UX improvements

Each agent receives `{vision}` context and creates additional issues.

### Step 7: Dedupe & Consolidate

**Three sources of duplicates:**
1. User observations (Step 2) may overlap with automated findings
2. New issues from Steps 4-5 that overlap with each other
3. New issues that overlap with existing issues kept from Step 3

**Find duplicates:**

```bash
# Find potential duplicates (similar titles)
gh issue list --state open --json number,title,labels | jq '.[] | .title' | sort | uniq -d

# Review issues flagged for consolidation in Step 3
# These were marked as "consolidate with new findings"
```

**For each duplicate set:**
- Keep the most comprehensive issue
- Close others with link to canonical: `gh issue close 123 --comment "Consolidated into #456"`
- Merge unique details from closed issues into the kept issue

**For issues to consolidate from Step 3:**
- If new findings cover the same ground → close old, reference new
- If new findings add to old → update old issue with new details
- If old issue is more comprehensive → close new, reference old

**Final pass:**
- Verify all open issues have correct priority labels
- Verify all open issues have domain labels
- Verify no orphaned issues (no priority, no domain)

### Step 8: Summarize

Output final report:

```
GROOM SUMMARY
=============

Issues by Priority:
- P0 (Critical): 2
- P1 (Essential): 8
- P2 (Important): 12
- P3 (Nice to Have): 5

Issues by Domain:
- Production: 2
- Quality: 3
- Docs: 2
- Observability: 3
- Stripe: 2
- Virality: 4
- Landing: 3
- Onboarding: 3
- Security: 2 (from agents)
- Other: 3 (from agents)

Recommended Focus Order:
1. [P0] Fix production payment failures
2. [P0] Patch security vulnerability
3. [P1] Add test coverage
4. [P1] Configure Sentry
...

View all: gh issue list --state open
View P0: gh issue list --label priority/p0
```

## Agent Prompts

### Security (Always Run)

```
Audit for security vulnerabilities: OWASP top 10, auth gaps,
data exposure, injection points, secrets management.
Include file:line. Output: prioritized security issues as GitHub issues.
```

### Architect (Always Run)

```
Audit system design: coupling, cohesion, module depth,
abstraction quality, dependency direction.
Include file:line. Output: prioritized architecture issues as GitHub issues.
```

### Aesthetician (Medium+ Backlog)

```
Audit visual design: distinctiveness, craft, trends, typography,
color sophistication, motion quality.
Focus: "Does this make people gasp?"
Output: prioritized design issues as GitHub issues.
```

### Pioneer (Medium+ Backlog)

```
Explore innovation opportunities: AI/LLM integration, Gordian knot
solutions, emerging tech, pattern modernization.
Output: prioritized R&D opportunities as GitHub issues.
```

### Visionary (Medium+ Backlog)

```
Read vision.md for the user's product vision.

Accelerate this vision. Find gaps, blockers, accelerators.
100% aligned with stated goals.
Output: prioritized vision-alignment actions as GitHub issues.
```

## Issue Format

All issues created by /groom (via skills or agents):

```markdown
## Title
[P{0-3}] Clear, actionable description

## Labels
- priority/p0|p1|p2|p3
- domain/production|quality|docs|observability|product-standards|stripe|bitcoin|lightning|payments|virality|landing|onboarding|security|architecture|design|innovation
- type/bug|enhancement|chore

## Body
### Problem
What's wrong or missing

### Impact
Why this matters (user impact, risk, blocked work)

### Suggested Fix
Concrete next steps or skill to run

### Source
Which skill or agent identified this

---
Created by `/groom`
```

## What You Get

After running /groom:
- Complete issue backlog in GitHub
- Issues prioritized P0-P3
- Issues labeled by domain
- Issues with actionable next steps
- Duplicates removed
- Summary of recommended focus

User can:
- See all work in GitHub Issues
- Filter by priority: `label:priority/p0`
- Filter by domain: `label:domain/stripe`
- Assign and track progress
- Run `/fix-*` skills to address issues

## Related Skills

### Primitives (Investigate)
- `/check-production`, `/check-docs`, `/check-quality`, `/check-observability`
- `/check-product-standards` (version, attribution, contact)
- `/check-stripe`, `/check-bitcoin`, `/check-lightning`, `/check-btcpay`, `/check-payments`
- `/check-virality`, `/check-landing`, `/check-onboarding`

### Issue Creators (Document)
- `/log-production-issues`, `/log-doc-issues`, `/log-quality-issues`
- `/log-observability-issues`, `/log-product-standards-issues`
- `/log-stripe-issues`, `/log-bitcoin-issues`, `/log-lightning-issues`
- `/log-virality-issues`, `/log-landing-issues`, `/log-onboarding-issues`

### Fixers (Act)
- `/triage`, `/fix-docs`, `/fix-quality`, `/fix-observability`
- `/fix-stripe`, `/fix-bitcoin`, `/fix-lightning`
- `/fix-virality`, `/fix-landing`, `/fix-onboarding`

## Running Individual Domains

Don't want full groom? Run specific skills:

```bash
/check-production     # Audit only, no issues
/log-production-issues # Create issues, no fixes
/triage              # Fix highest priority

/check-stripe        # Audit only
/log-stripe-issues   # Create issues
/fix-stripe          # Fix highest priority
```
