---
name: generate-variant
description: Generate job-targeted CV variants with built-in quality gates. Queries knowledge base, customizes content, runs eval/redteam pipeline.
---

# Generate Variant

<purpose>
Generate personalized portfolio variants for specific job opportunities, with full traceability and quality verification through a 9-phase pipeline.
</purpose>

<when_to_activate>
Activate when the user:
- Provides a job description or job URL
- Asks to create a variant for a specific company/role
- Says "generate variant", "create variant", "tailor CV for [company]"
- Wants to apply for a specific position

**Trigger phrases:** "variant", "tailor", "customize CV", "apply for [company]", "job application"
</when_to_activate>

<critical_principles>
## Critical Design Principles

**From Galaxy Variant Exercise:**
1. **Signature headline stays** — "Building at the edge of trust" is the brand
2. **companyAccent is REQUIRED** — Add inline company name (`— with {Company}`)
3. **Existing connections are gold** — Lead with what you've already proven
4. **Stats must be verifiable** — Every metric traced to knowledge base
5. **Pause between phases** — Get user approval before proceeding
</critical_principles>

---

## Phase 1: JD Analysis & Must-Have Extraction

**Goal:** Extract NON-GENERIC requirements using the deterministic `analyze:jd` script.

### Step 1.1: Save JD to File

If user provides JD text, save it first:
```bash
# Save JD to source-data/jd-{company}.txt
echo "[JD TEXT]" > source-data/jd-{company}.txt
```

### Step 1.2: Run Deterministic JD Analysis

**USE THE SCRIPT** — it automatically filters 47+ generic phrases and extracts specific requirements:

```bash
npm run analyze:jd -- --file source-data/jd-{company}.txt --save
```

This outputs to `capstone/develop/jd-analysis/{slug}.yaml` with:
- `extracted.company`, `extracted.role`, `extracted.yearsRequired`
- `mustHaves[]` with category and specificity (high/medium/low)
- `niceToHaves[]`
- `ignoredGeneric[]` — what was filtered out
- `domainKeywords[]` — crypto, fintech, developer_tools, etc.
- `searchTerms[]` — ready for knowledge base search

**What the script filters automatically:**
- "Team player", "excellent communicator", "fast-paced environment"
- "Passionate about [X]", "self-starter", "attention to detail"
- "Proven track record", "data-driven", "results-oriented"
- 40+ more generic phrases (see `scripts/analyze-jd.ts:GENERIC_PHRASES`)

### Step 1.3: Review Analysis Output

```bash
# Read the generated analysis
cat capstone/develop/jd-analysis/{slug}.yaml
```

Check for:
- Correct company/role extraction
- Meaningful must-haves (not generic)
- Appropriate domain keywords

### Step 1.4: Check for Existing Variants

```bash
ls content/variants/ | grep -i {company}
```

**Output:** JD analysis summary to user for confirmation before proceeding.

---

## Phase 1.5: Alignment Gate (GO/NO-GO)

**Goal:** Score alignment BEFORE investing time in content generation using the `search:evidence` script.

### Run Evidence Search

**USE THE SCRIPT** — it searches the knowledge base and generates an alignment report:

```bash
npm run search:evidence -- --jd-analysis capstone/develop/jd-analysis/{slug}.yaml --save
```

This outputs to `capstone/develop/alignment/{slug}.yaml` with:
- `summary.alignmentScore` — 0.0 to 1.0
- `summary.recommendation` — PROCEED | REVIEW | SKIP
- `summary.strongMatches` — count of high-relevance matches (≥70%)
- `summary.moderateMatches` — count of medium-relevance matches (40-70%)
- `matches[]` — sorted by relevance with evidence snippets
- `gaps[]` — search terms with no matches

### Alternative: Manual Search Terms

If you have specific terms not from JD analysis:

```bash
npm run search:evidence -- --terms "crypto,staking,infrastructure,api" --threshold 0.5 --save
```

### Review Alignment Report

```bash
cat capstone/develop/alignment/{slug}.yaml
```

### Decision Framework

| Score | Recommendation | Action |
|-------|----------------|--------|
| ≥ 0.50 + 2 strong | **PROCEED** | Generate variant |
| ≥ 0.30 or 1 strong | **REVIEW** | Show gaps, ask user if worth pursuing |
| < 0.30 and 0 strong | **SKIP** | Recommend not applying, show why |

### Honesty Check

For REVIEW/SKIP cases, the script surfaces:
- `gaps[]` — terms with no matching evidence
- Low relevance matches that may be stretches

Surface honestly:
- Which must-haves have no evidence
- Whether gaps are addressable (transferable skills) or hard blockers
- Honest assessment: "This role requires X, which isn't in your background"

**PAUSE:** Show alignment score and recommendation. Get explicit GO/NO-GO from user.

---

## Phase 2: Knowledge Base Query

**Goal:** Find matching achievements and stories.

1. Search achievements:
   ```bash
   ls content/knowledge/achievements/
   ```

2. Read relevant achievement files matching JD requirements

3. Look for existing client relationships:
   - Search for company name in achievements/stories
   - Example: Galaxy was already an Anchorage client (ETH staking)

4. Rank matches by relevance (0.0-1.0):
   - Direct skill match: 0.9-1.0
   - Related experience: 0.7-0.9
   - Transferable skills: 0.5-0.7

**Output:** List of relevant achievements with relevance scores.

---

## Phase 2.5: Bullet Coverage Check

**Goal:** Ensure experience highlights cover all 7 PM competency bundles using the `check:coverage` script.

### Run Coverage Check

**USE THE SCRIPT** — it automatically categorizes bullets into the 7 PM competency bundles:

```bash
npm run check:coverage
```

For JSON output (easier to process):
```bash
npm run check:coverage -- --json
```

To save report:
```bash
npm run check:coverage -- --save
```

### The 7 Competency Bundles (Automated)

The script categorizes based on keywords (see `scripts/check-coverage.ts:BUNDLES`):

| Bundle | Keywords Detected |
|--------|-------------------|
| **1. Product Design** | shipped, launched, built, designed, UX, prototyped, improved |
| **2. Leadership** | led, managed, coordinated, E2E, cross-functional, stakeholders |
| **3. Strategy** | strategy, vision, roadmap, prioritized, market analysis |
| **4. Business** | revenue, ARR, GTM, partnerships, growth, B2B, pricing |
| **5. Project Mgmt** | delivered, timeline, Agile, risk, milestones, on-time |
| **6. Technical** | architecture, API, SDK, data, metrics, trade-offs, system |
| **7. Communication** | presented, documented, collaborated, aligned, storytelling |

### Review Coverage Output

The script outputs:
- Count per bundle
- Examples of bullets in each bundle
- `gaps[]` — bundles with <2 bullets
- `overweight[]` — bundles with 5+ bullets
- Overall balance assessment

### Interpretation

| Gap Level | Action |
|-----------|--------|
| 0 gaps | Proceed — well-rounded |
| 1-2 gaps | Surface gaps to user — may want to emphasize in bio/tagline |
| 3+ gaps | Warning — resume may appear unbalanced |

### Using Coverage for This Variant

Cross-reference gaps with JD must-haves:
1. Does this role care about the gap? (Check Phase 1 analysis)
2. Can the bio/tagline emphasize this competency?
3. Are there achievements in knowledge base that weren't surfaced?

**Note:** Not all variants need all 7 bundles. A technical PM role may not care about "Business & Marketing." Use the JD must-haves to determine which gaps matter.

---

## Phase 3: Content Generation

**IMPORTANT:** Invoke `dmitrii-writing-style` skill before writing bio content.

### Hero Section

```yaml
hero:
  status: "Open to Product Roles"  # Keep simple
  headline:
    - text: "Building"
      style: "italic"
    - text: "at the edge of"
      style: "muted"
    - text: "trust"
      style: "accent"
  companyAccent:  # REQUIRED
    - text: "with"
      style: "muted"
    - text: "{Company}"
      style: "accent"
  subheadline: >
    [Tailored elevator pitch mentioning company connection]
```

### About Section

```yaml
about:
  tagline: >
    [One-line positioning statement]
  bio:
    - >
      [Paragraph 1: Recent experience, relevant achievements, company connection]
    - >
      [Paragraph 2: Career arc leading to this opportunity + vision]
  stats:
    - value: "[X]+"
      label: "[Relevant metric]"
    - value: "[Y]"
      label: "[Relevant metric]"
    - value: "[Z]"
      label: "[Relevant metric]"
```

### Relevance Scoring

```yaml
relevance:
  caseStudies:
    - slug: "[most-relevant]"
      relevanceScore: 1.0
      reasoning: "[Why this matches JD]"
    # ... ranked list
  skills:
    - category: "[Top category]"
      relevanceScore: 1.0
    # ... ranked list
```

**PAUSE:** Show generated content to user for review before proceeding.

---

## Phase 4: Variant File Creation

1. Create variant YAML:
   ```bash
   # Write to content/variants/{slug}.yaml
   ```

2. Sync to JSON:
   ```bash
   npm run variants:sync -- --slug {slug}
   ```

3. Verify JSON created:
   ```bash
   ls content/variants/{slug}.json
   ```

---

## Phase 5: Evaluation Pipeline

1. Run evaluation:
   ```bash
   npm run eval:variant -- --slug {slug}
   ```

2. Review extracted claims (metrics with anchors)

3. For each unverified claim, verify against knowledge base:
   ```bash
   npm run eval:variant -- --slug {slug} --verify {claim-id}={source-path}
   ```

4. Target: **100% claims verified**

**PAUSE:** Show claims status to user before proceeding.

---

## Phase 6: Red Team Pipeline

1. Run red team scan:
   ```bash
   npm run redteam:variant -- --slug {slug}
   ```

2. Review findings:
   - **FAIL** — Must fix before publishing
   - **WARN** — Review and decide

3. Common issues and fixes:
   | Check | Issue | Fix |
   |-------|-------|-----|
   | RT-ACC-CLAIMS | Unverified claims | Run Phase 5 verification |
   | RT-SEC-SECRETS | Tokens in content | Remove sensitive data |
   | RT-TONE-SYCOPHANCY | Flattery detected | Rewrite objectively |
   | RT-PRIV-JD | Long JD exposed | Truncate in YAML |

**PAUSE:** Show redteam results to user for approval.

---

## Phase 7: Final Review

1. Start dev server if not running:
   ```bash
   npm run dev
   ```

2. Open variant in browser:
   ```
   http://localhost:5173/{company}/{role}
   ```

3. Visual checklist:
   - [ ] companyAccent renders inline after "trust"
   - [ ] Stats are visible and accurate
   - [ ] Bio reads naturally
   - [ ] Case studies are relevant

4. Offer to commit if approved.

---

## Phase 8: Resume Generation

**Goal:** Generate a variant-specific resume PDF and link it to the variant.

1. Generate variant resume:
   ```bash
   npm run generate:resume -- --variant {slug}
   ```

   This will:
   - Render the resume at `/{company}/{role}/resume`
   - Output PDF to `public/resumes/{slug}.pdf`
   - Auto-update variant YAML with `resumePath: /resumes/{slug}.pdf`

2. Sync the updated variant:
   ```bash
   npm run variants:sync -- --slug {slug}
   ```

3. Verify resume was generated:
   ```bash
   ls -la public/resumes/{slug}.pdf
   ```

**Note:** The variant resume uses the merged profile/experience data, so it reflects the tailored content (bio, stats, tagline) specific to this role.

---

## Phase 9: Dashboard Update

**Goal:** Regenerate the CV dashboard to include the new variant.

1. Regenerate dashboard HTML:
   ```bash
   DASHBOARD_PASSWORD=<password> npm run generate:dashboard
   ```

   Or use the combined command (syncs variants AND regenerates dashboard):
   ```bash
   DASHBOARD_PASSWORD=<password> npm run variants:sync:dashboard
   ```

2. Verify the new variant appears in the dashboard output:
   - Check the console shows the new variant in the list
   - Dashboard HTML is updated at `public/cv-dashboard/index.html`

3. Commit the updated dashboard:
   ```bash
   git add public/cv-dashboard/index.html
   ```

**Note:** The dashboard is password-protected. The `DASHBOARD_PASSWORD` env var is required. Check `.env.local` or ask the user for the password.

---

## Quality Checklist

Before marking variant complete:

- [ ] All claims verified against knowledge base
- [ ] No hallucinated achievements
- [ ] Company connection established (existing client? industry overlap?)
- [ ] Signature headline preserved with companyAccent (REQUIRED)
- [ ] Stats are verifiable and impactful
- [ ] Red team passes (0 FAIL, minimal WARN)
- [ ] Would defend every claim in an interview
- [ ] Writing style matches dmitrii-writing-style
- [ ] Resume PDF generated and linked (`resumePath` in variant metadata)
- [ ] Dashboard regenerated with new variant visible

---

## File Locations Reference

| File | Purpose |
|------|---------|
| `content/variants/{slug}.yaml` | Variant source (canonical) |
| `content/variants/{slug}.json` | Runtime artifact |
| `content/variants/_template.yaml` | Template reference |
| `capstone/develop/evals/{slug}.claims.yaml` | Claims ledger |
| `capstone/develop/evals/{slug}.eval.md` | Eval report |
| `capstone/develop/redteam/{slug}.redteam.md` | Redteam report |
| `content/knowledge/achievements/*.yaml` | Achievement sources |
| `content/knowledge/stories/*.yaml` | Story sources |
| `public/resumes/{slug}.pdf` | Variant-specific resume PDF |
| `public/cv-dashboard/index.html` | Dashboard HTML (password-protected) |
| `public/cv-dashboard/variants-manifest.json` | Dashboard data source |

---

## Commands Reference

```bash
# ═══════════════════════════════════════════════════════════════
# PHASE 1: JD Analysis (deterministic)
# ═══════════════════════════════════════════════════════════════
npm run analyze:jd -- --file source-data/jd-{company}.txt --save
npm run analyze:jd -- --file jd.txt --json  # JSON output

# ═══════════════════════════════════════════════════════════════
# PHASE 1.5: Evidence Search (deterministic)
# ═══════════════════════════════════════════════════════════════
npm run search:evidence -- --jd-analysis capstone/develop/jd-analysis/{slug}.yaml --save
npm run search:evidence -- --terms "crypto,staking,api" --threshold 0.5

# ═══════════════════════════════════════════════════════════════
# PHASE 2.5: Coverage Check (deterministic)
# ═══════════════════════════════════════════════════════════════
npm run check:coverage
npm run check:coverage -- --json
npm run check:coverage -- --save

# ═══════════════════════════════════════════════════════════════
# PHASE 4-6: Variant Pipeline
# ═══════════════════════════════════════════════════════════════
npm run variants:sync -- --slug {slug}
npm run eval:variant -- --slug {slug}
npm run eval:variant -- --slug {slug} --verify {id}={path}
npm run redteam:variant -- --slug {slug}

# ═══════════════════════════════════════════════════════════════
# PHASE 8: Resume Generation
# ═══════════════════════════════════════════════════════════════
npm run generate:resume -- --variant {slug}
npm run variants:sync -- --slug {slug}  # Sync after resume path update

# ═══════════════════════════════════════════════════════════════
# PHASE 9: Dashboard Update
# ═══════════════════════════════════════════════════════════════
DASHBOARD_PASSWORD=<password> npm run generate:dashboard
# Or combined sync + dashboard:
DASHBOARD_PASSWORD=<password> npm run variants:sync:dashboard

# ═══════════════════════════════════════════════════════════════
# PREVIEW
# ═══════════════════════════════════════════════════════════════
npm run dev
open "http://localhost:5173/{company}/{role}"
open "http://localhost:5173/{company}/{role}/resume"  # Preview resume page
```

---

## Example: Galaxy PM Variant

**Job:** Director, Technical Program Manager at Galaxy

**Key Learnings Applied:**
1. Found existing connection: Galaxy was already an Anchorage client (ETH staking)
2. Matched L2 integration framework to "cross-functional" TPM requirement
3. Used punchy stats: "8+", "7+", "Zero" (all verified)
4. companyAccent: `trust — with Galaxy` (inline, subtle)
5. Status: "Open to Product Roles" (simple, not desperate)

**Result:** All 6 claims verified, redteam passed, variant shipped.

<quality_gate>
## Quality Gate

See [Quality Gate Template](../_shared/quality-gate.md) for universal checks.

**Variant-specific:**
- [ ] All claims verified against knowledge base
- [ ] companyAccent is set (REQUIRED)
- [ ] Red team passes (0 FAIL findings)
- [ ] Would defend every claim in an interview
</quality_gate>

<skill_compositions>
## Works Well With

- **dmitrii-writing-style** — MUST invoke before writing bio content
- **cv-knowledge-query** — Search evidence before generating
- **ultrathink** — For complex alignment decisions
- **generate-resume** — Generate variant-specific resume after variant
</skill_compositions>
