---
name: shipflow-audit-gtm
description: Professional go-to-market review — single page (with argument) or full project audit (no argument)
disable-model-invocation: true
argument-hint: [file-path | "global"] (omit for full project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -100 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- All pages: !`find src/pages src/app -name "*.astro" -o -name "*.tsx" -o -name "*.vue" 2>/dev/null | grep -v node_modules | sort`
- Analytics: !`grep -ri "analytics\|gtag\|plausible\|umami\|posthog\|vercel/analytics" src/ 2>/dev/null | head -10 || echo "no analytics found"`
- Auth/payment: !`grep -ri "clerk\|stripe\|lemonsqueezy\|paddle\|auth" package.json 2>/dev/null | head -5 || echo "none"`
- Environment hints: !`grep -ri "STRIPE\|CLERK\|PAYMENT\|PRICE" .env.example .env.local 2>/dev/null | head -10 || echo "none"`

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: audit ALL commercial projects in the workspace.
- **`$ARGUMENTS` is a file path** → PAGE MODE: GTM review of that single page.
- **`$ARGUMENTS` is empty** → PROJECT MODE: full go-to-market audit. Think like a CMO reviewing before launch.

---

## GLOBAL MODE

Audit ALL commercial projects in the workspace for go-to-market readiness.

1. Read `/home/claude/shipflow_data/PROJECTS.md` — check the **Domain Applicability** table. Identify projects with ✓ in the GTM column.

2. Use **AskUserQuestion** to let the user choose:
   - Question: "Which projects should I audit for go-to-market?"
   - `multiSelect: true`
   - One option per applicable project: label = project name, description = stack from PROJECTS.md
   - All applicable projects pre-listed as options

3. Use the **Task tool** to launch one agent per **selected** project — ALL IN A SINGLE MESSAGE (parallel). Each agent: `subagent_type: "general-purpose"`.

   Agent prompt must include:
   - `cd [path]` then read `CLAUDE.md` for project context
   - The complete **PROJECT MODE** section from this skill (all 8 phases: Positioning Map → Conversion Funnel Map → Page-by-Page GTM → Trust Architecture → Analytics & Measurement → Launch Readiness → Fix → Report)
   - The **Tracking** section from this skill
   - Rule: **read-only analysis** — no code fixes, only update AUDIT_LOG.md and TASKS.md

4. After all agents return, compile a **cross-project GTM report**:

   ```
   GLOBAL GTM AUDIT — [date]
   ═══════════════════════════════════════
   PROJECT SCORES
     [project]    [A/B/C/D]  —  summary
     ...
   CROSS-PROJECT PATTERNS
     [Systemic GTM issues in 2+ projects]
   ALL ISSUES BY SEVERITY
     🔴 [project] file:line — description
     🟠 [project] file:line — description
     🟡 [project] file:line — description
   Total: X critical, Y high, Z medium across N projects
   ═══════════════════════════════════════
   ```

5. Update `/home/claude/shipflow_data/AUDIT_LOG.md` (one row per project, GTM column) and `/home/claude/shipflow_data/TASKS.md` (each project's `### Audit: GTM` subsection).

6. Ask: **"Which projects should I fix?"** — list projects with scores. Fix only approved projects, one at a time.

---

## PAGE MODE

### Step 1: Gather the page

1. Read the target file (`$ARGUMENTS`).
2. Read the site navigation to understand where this page sits in the funnel.
3. Read the homepage/landing page to understand overall positioning.
4. Read pricing page if it exists.

### Step 2: Audit against this checklist

Score each category **A/B/C/D**. Be strict — growth/marketing professional standard.

#### 1. Positioning & Differentiation
- [ ] Immediately clear what this product/service does (5-second test)
- [ ] Unique value proposition is explicit, not implied
- [ ] Competitive differentiation is visible
- [ ] Target audience is obvious from language, imagery, examples
- [ ] Positioning is specific, not vague

#### 2. Conversion Architecture
- [ ] Clear single goal (one primary conversion action)
- [ ] Conversion path has minimal friction
- [ ] CTA visible without scrolling
- [ ] CTA repeated at logical intervals
- [ ] Exit intent or secondary capture exists
- [ ] Pricing is transparent

#### 3. Trust & Credibility
- [ ] Social proof is present and specific
- [ ] Testimonials include name, role, photo, or company
- [ ] Trust badges where appropriate
- [ ] Case studies or results with real data
- [ ] Professional design
- [ ] Contact information visible

#### 4. Objection Handling
- [ ] FAQ addresses top 3-5 objections
- [ ] Pricing objections handled
- [ ] "Who is this for / not for" clarity
- [ ] Setup complexity addressed
- [ ] Data/privacy concerns addressed if relevant

#### 5. Funnel Alignment
- [ ] Page matches traffic source intent
- [ ] Internal links guide deeper into funnel
- [ ] Blog/content links back to product pages
- [ ] Navigation doesn't distract from conversion goal
- [ ] Post-conversion flow exists

#### 6. Analytics & Tracking
- [ ] Analytics tool installed and loading
- [ ] Key conversion events tracked
- [ ] UTM parameters preserved
- [ ] A/B testing infrastructure exists or easy to add
- [ ] Core Web Vitals monitored

#### 7. Market Readiness
- [ ] Legal pages exist (privacy, terms, mentions légales for FR)
- [ ] Cookie consent if EU-targeted
- [ ] Accessibility meets minimum legal requirements
- [ ] Contact/support channel functional
- [ ] Mobile experience equal to desktop

### Step 3: Fix

For each issue rated B or worse:
1. Explain the business impact.
2. Fix code-level issues directly.
3. For strategic decisions, provide specific recommendations.

### Step 4: Report

```
GTM REVIEW: [page name] — funnel stage: [awareness/consideration/conversion/retention]
─────────────────────────────────────
Positioning        [A/B/C/D] — one-line summary
Conversion         [A/B/C/D] — one-line summary
Trust & Proof      [A/B/C/D] — one-line summary
Objection Handling [A/B/C/D] — one-line summary
Funnel Alignment   [A/B/C/D] — one-line summary
Analytics          [A/B/C/D] — one-line summary
Market Readiness   [A/B/C/D] — one-line summary
─────────────────────────────────────
OVERALL            [A/B/C/D]

Fixed: X issues | Strategic recommendations: Y
```

---

## PROJECT MODE

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `src/` dir) BUT contains multiple project subdirectories — you are at the **workspace root**, not inside a project.

Use **AskUserQuestion**:
- Question: "You're at the workspace root. Which project(s) should I audit for go-to-market?"
- `multiSelect: true`
- Options:
  - **All projects** — "Run GTM audit across every commercial project" (Recommended)
  - One option per commercial project from `/home/claude/shipflow_data/PROJECTS.md`: label = project name, description = stack

Then proceed to **GLOBAL MODE** with the selected projects.

### Phase 1: Positioning Map

Read homepage, about, pricing, and key landing pages. Document:

1. **Core value proposition**: Explicit or implied?
2. **Target audience**: Specific enough?
3. **Competitive angle**: Communicated?
4. **Pricing model**: Aligned with value prop?
5. **Brand promise**: Kept throughout?

Deliver a **one-sentence positioning statement**: "[Product] helps [audience] [achieve outcome] by [unique mechanism], unlike [alternatives]."

### Phase 2: Conversion Funnel Map

Trace every conversion path:
```
Traffic Source → Landing → Consideration → Conversion → Post-Conversion
```

For each path:
- [ ] Entry point matches traffic intent
- [ ] Each step has a clear next action
- [ ] No dead ends
- [ ] Friction minimized
- [ ] Fallback capture for non-converters

### Phase 3: Page-by-Page GTM Audit

Classify each page by funnel role and audit:

**Awareness** (blog, content, landing):
- [ ] Strong hook, links to conversion pages, lead capture, shareable

**Consideration** (features, how-it-works, case studies):
- [ ] Addresses objections, relevant social proof, clear path to pricing

**Conversion** (pricing, signup, checkout):
- [ ] Price anchoring, risk reversal, minimal friction, trust signals near action

**Retention** (dashboard, settings, onboarding):
- [ ] Guides to first value moment, contextual upgrade prompts, accessible help

### Phase 4: Trust Architecture

- [ ] Testimonials: specific, credible
- [ ] Social proof: user counts, logos, media mentions
- [ ] Security signals: SSL, privacy policy
- [ ] Authority signals: team page, credentials
- [ ] Legal compliance: mentions légales (FR), privacy, CGV, cookie consent

### Phase 5: Analytics & Measurement

- [ ] Analytics on all pages
- [ ] Conversion events tracked (CTA clicks, form submissions, signups, pricing views)
- [ ] UTM parameters preserved
- [ ] Goal/conversion tracking configured

### Phase 6: Launch Readiness

- [ ] All pages load without errors
- [ ] Mobile experience complete
- [ ] Forms submit correctly
- [ ] Payment flow works (if applicable)
- [ ] Email templates branded
- [ ] 404 page helpful
- [ ] Social previews look good
- [ ] Legal pages complete
- [ ] Contact channel functional

### Phase 7: Fix

Fix all issues in code. Priority:
1. **Broken conversion paths**
2. **Missing trust signals**
3. **Missing analytics tracking**
4. **Legal compliance**
5. **Funnel leaks**

### Phase 8: Report

```
GTM AUDIT: [project name]
═══════════════════════════════════════

POSITIONING
  Value proposition:     [clear / vague / missing]
  Target audience:       [specific / generic]
  Differentiation:       [strong / weak / absent]
  One-liner: "[positioning statement]"

CONVERSION FUNNEL
  Primary path:          [description] — [A/B/C/D]
  Secondary paths:       [count] identified
  Dead ends:             [count]
  Friction:              [low / medium / high]

PAGE SCORES (by funnel role)
  Awareness
    /blog              [A/B/C/D]
  Consideration
    /features          [A/B/C/D]
  Conversion
    /pricing           [A/B/C/D]

TRUST ARCHITECTURE     [A/B/C/D]
ANALYTICS & TRACKING   [A/B/C/D]
LAUNCH READINESS       [A/B/C/D]
═══════════════════════════════════════
OVERALL                [A/B/C/D]

Fixed: X issues across Y files
Strategic recommendations: Z (detailed below)
```

---

## Tracking (all modes)

After generating the report and applying fixes:

### Log the audit

Append a row to two files:

1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`**: append a row filling only the GTM column, `—` for others.
2. **Project-local `./AUDIT_LOG.md`**: same without the Project column.

Create either file if missing.

### Update TASKS.md

1. **Local TASKS.md** (project root): add/replace an `### Audit: GTM` subsection with critical (🔴), high (🟠), and medium (🟡) issues as task rows.
2. **Master `/home/claude/shipflow_data/TASKS.md`**: find the project's section, add/replace an `### Audit: GTM` subsection with the same tasks.

---

## Important (all modes)

- Think like a growth lead, not a developer. Every recommendation ties to revenue or user acquisition.
- For French market: RGPD mandatory, mentions légales legally required, CGV for commercial transactions.
- Be specific with business impact estimates (use industry conversion benchmarks).
- Don't recommend building features that don't exist — optimize what's there. List "should build" items separately.
- If pre-launch, focus on launch readiness. If post-launch, focus on conversion optimization.
