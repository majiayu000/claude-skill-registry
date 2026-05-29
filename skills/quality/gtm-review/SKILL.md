---
name: gtm-review
description: Run a comprehensive Go-to-Market and launch readiness review for a project phase. Combines marketing content audit, code quality review, performance audit, accessibility audit, infrastructure readiness, and business review with council evaluation. Use before phase launches or when GTM review issues are ready.
user-invokable: true
---

# GTM Review Workflow

Run a comprehensive Go-to-Market and launch readiness review for a project phase. This skill audits marketing content accuracy, code quality, performance, accessibility, infrastructure readiness, and business positioning, then activates the GTM Council for a consolidated launch readiness verdict.

## Scope

| Does                                     | Does NOT do                                   |
| ---------------------------------------- | --------------------------------------------- |
| Comprehensive phase readiness audit      | Write application code or fix bugs            |
| Marketing content accuracy review        | Push to remote or create PRs                  |
| Code quality review via Review Council   | Modify the project board schedule             |
| Performance and accessibility audit      | Re-plan features (that's `/plan-feature`)     |
| Business and competitive analysis        | Run security audit (that's `/security-audit`) |
| Generate GTM report in `docs/decisions/` |                                               |
| Update GTM issue with findings           |                                               |

> [!IMPORTANT]
> This skill does NOT replace the `/security-audit` gate. Security audit is a separate gate item that runs after the GTM review. This skill delegates security concerns to that skill rather than duplicating its work.

## Step 0: Verify Clean Working Tree

This skill commits a report file in Step 10. Ensure the working tree is clean before starting:

```bash
git status --porcelain
```

If there are uncommitted changes, warn the user and ask whether to stash them (`git stash push -m "gtm-review: stash before review"`) or abort.

## Step 1: Identify Phase Scope

Accept input from the user:

- **GTM issue number** (e.g., `#132`) — primary input
- **Phase identifier** (e.g., `M1`) — alternative input

If given a GTM issue number:

```bash
gh issue view <number> --json title,body,labels,milestone
```

If given a phase identifier, find the GTM issue for that phase:

```bash
gh issue list --state open --label "gtm-review" --json number,title,milestone
```

### Build the Phase Inventory

1. **List all issues in the milestone** — shipped (closed), in-progress, open:

   ```bash
   gh issue list --milestone "<milestone-title>" --state all --json number,title,state,labels --limit 100
   ```

2. **Categorize features**:
   - **Shipped** (closed issues): features that are complete and available
   - **In-progress** (issues with `in-progress` label): features being built in tandem
   - **Planned** (open issues without `in-progress`): features not yet started

3. **Build a capabilities matrix**: For each shipped feature, summarize what the product can now do. For each in-progress feature, note what it will add. This matrix is the ground truth for the content audit — every marketing claim will be validated against it.

4. **Identify gaps**: Features described in the GTM issue's Phase Summary that are NOT yet shipped.

## Step 2: Run Automated Quality Checks

Run all checks in parallel:

```bash
pnpm lint
pnpm format:check
pnpm type-check
pnpm test --coverage
pnpm build
```

Capture and record:

- **Lint**: pass/fail, number of warnings
- **Format**: pass/fail, files needing formatting
- **Type-check**: pass/fail, error count
- **Tests**: pass/fail, total tests, coverage percentage by package
- **Build**: pass/fail, bundle sizes from build output

These results feed into later steps. Do not checkpoint here.

## Step 3: Performance Audit

Activate the **Performance Analyst** agent. Read the agent definition from `.claude/agents/performance-analyst.md` and use the model specified in the `## Model` section.

Invoke the following plugins for guidance:

- `application-performance` for application profiling and optimization patterns
- `performance-testing-review` for performance testing methodology and coverage analysis

### Frontend Performance

Using the build output from Step 2:

- **Bundle size analysis**: Total bundle size, largest chunks, opportunities for code splitting
- **Lazy loading**: Are route-level components lazy loaded? Are heavy libraries deferred?
- **Image optimization**: Are images served in modern formats (WebP, AVIF)? Are they properly sized?
- **Render performance**: Are there render-blocking resources? Large initial payloads?
- **Core Web Vitals risk assessment** (from code patterns):
  - **LCP**: Large hero images without preloading? Blocking fonts? Slow server response patterns?
  - **INP**: Heavy JavaScript on the main thread? Missing `React.memo` or `useMemo` for expensive renders?
  - **CLS**: Dynamic content insertion without reserved space? Font swap without fallback sizing?

### Backend Performance

- **API endpoint patterns**: Are there endpoints that fetch excessive data? Missing pagination?
- **N+1 queries**: Review Prisma queries for `.include()` patterns that could cause N+1
- **Database index coverage**: Do frequently queried fields have indexes?
- **Connection pooling**: Is the database connection pool configured?
- **Caching**: Is there a caching strategy for frequently accessed data?

Record all findings for the council evaluation. Do not checkpoint here.

## Step 4: Accessibility Audit

Invoke the following plugins:

- `accessibility-compliance:wcag-audit-patterns` for comprehensive WCAG 2.1 AA compliance audit
- `accessibility-compliance:screen-reader-testing` for assistive technology compatibility
- `ui-design:accessibility-audit` for component-level accessibility checks

Audit areas:

- **Color contrast**: Do all text/background combinations meet WCAG AA ratios (4.5:1 normal, 3:1 large)?
- **Keyboard navigation**: Can all interactive elements be reached and activated via keyboard?
- **ARIA attributes**: Are ARIA roles, labels, and live regions used correctly?
- **Focus management**: Is focus trapped in modals? Does focus move logically between steps?
- **Semantic HTML**: Are headings hierarchical? Are form labels associated? Are landmarks present?
- **Touch targets**: Are interactive elements at least 44x44px on mobile?
- **Responsive design**: Does the layout work across common breakpoints?
- **Motion/animation**: Is `prefers-reduced-motion` respected?

Record all findings for the council evaluation. Do not checkpoint here.

## Step 5: Content & Marketing Audit

Activate the **Content Reviewer** agent. Read the agent definition from `.claude/agents/content-reviewer.md` and use the model specified in the `## Model` section (Claude Opus 4.6).

Invoke the following plugins for guidance:

- `seo-technical-optimization` for meta tags, structured data, schema markup audit
- `seo-content-creation` for content quality and E-E-A-T assessment

### Marketing Page Audit

For each section of the landing page (Hero, Features, How It Works, Pricing, Social Proof, FAQ, Footer):

1. **Read the actual component file** to see the exact copy users will see
2. **Compare each claim against the capabilities matrix** from Step 1
3. **Flag any discrepancies**: features mentioned but not shipped, inflated descriptions, misleading comparisons

### Content Consistency Audit

Compare copy across all surfaces:

- **Landing page** vs. **in-app copy** (onboarding, dashboard, profiles)
- **Landing page** vs. **email templates** (invite, welcome)
- **Pricing claims** vs. **actual billing implementation**
- **"How it works" flow** vs. **actual user experience**

### SEO Audit

- **Meta tags**: Are title, description, and keywords accurate for current product state?
- **Structured data** (JSON-LD): Does it match the actual product (type, price, features)?
- **Open Graph tags**: Are og:title, og:description, og:image correct?
- **Aggregate ratings**: Are they real or fabricated?

### Legal Link Verification

- Do `/privacy`, `/terms`, `/contact` (or equivalent) links resolve to actual pages?
- Are legal pages complete and accurate?

### Content Style Compliance

Check all user-facing copy against the **User-Facing Content Style** rules in `AGENTS.md`:

- **No em dashes** (`—` or `&mdash;`)
- **No AI-slop vocabulary**: delve, tapestry, landscape, leverage, seamless, cutting-edge, groundbreaking, etc.
- **No hollow transitions**: moreover, furthermore, additionally
- **No promotional inflation**: stunning, breathtaking, world-class, game-changer
- **No rule-of-three defaults**
- **No superficial -ing closers**

### Testimonial and Social Proof Review

- Are testimonials real or placeholder?
- Is scale language appropriate? (e.g., "Join thousands" for an invite-only beta is misleading)
- Are star ratings backed by actual data?

Produce a **line-item content accuracy report** with specific file paths, the problematic text, and recommended corrections.

### CHECKPOINT: Present the automated findings summary from Steps 2-5 to the user.

Organize as:

1. **Quality Checks** (Step 2): pass/fail status, coverage numbers, bundle sizes
2. **Performance** (Step 3): key findings, risk areas
3. **Accessibility** (Step 4): WCAG compliance status, issues found
4. **Content Accuracy** (Step 5): line-item accuracy report, SEO audit results, style violations

Wait for user review before proceeding to council evaluations. The user may want to address critical issues before the council sees them.

## Step 6: Code Quality Review

Invoke `code-review-ai:architect-review` for architecture analysis of the phase's codebase.

> **Model Selection**: See the [Model Selection](../../README.md#model-selection) section in README.md for mapping agent model specs to Task tool parameters.

Activate the **Review Council** (4 members from `.claude/councils/review-council.md`):

### Security Engineer (Lead) — consult: security-scanning

- Review codebase security posture (this is a high-level review, not the full `/security-audit`)
- Validate authentication and authorization patterns
- Check OWASP Top 10 at a surface level
- Flag any critical issues that should block launch
- **Vote**: Approve / Concern / Block
- **Assessment**: [Findings and recommendations]

### QA Lead — consult: unit-testing

- Assess test coverage against >80% target for phase code
- Identify gaps in critical user paths (auth, onboarding, core features)
- Evaluate test quality (are tests meaningful or just hitting line counts?)
- **Vote**: Approve / Concern / Block
- **Assessment**: [Findings and recommendations]

### DevX Engineer — consult: documentation-generation

- Is README.md accurate for a fresh developer setup?
- Does `docs/DEVELOPMENT.md` match current setup steps?
- Is `docs/INDEX.md` up to date with all docs files?
- Are API endpoints documented?
- **Vote**: Approve / Concern / Block
- **Assessment**: [Findings and recommendations]

### Frontend Specialist and/or Backend Specialist — consult: frontend-mobile-development or backend-development

Based on what the phase touches:

- Domain-specific code quality and patterns consistency
- Architecture adherence (folder structure, module organization)
- Component reuse and DRY principles
- **Vote**: Approve / Concern / Block
- **Assessment**: [Findings and recommendations]

Record the council vote tally and any blocking issues. Do not checkpoint here — results feed into the GTM Council.

## Step 7: Infrastructure & Documentation Readiness

Invoke the following plugins for guidance:

- `deployment-validation` for pre-deployment configuration checks
- `observability-monitoring` for monitoring and observability readiness

### Platform Engineer — consult: cloud-infrastructure

Read the agent definition from `.claude/agents/platform-engineer.md` and use the specified model.

- **Docker**: Does `docker compose up` produce a working environment for a fresh clone?
- **CI/CD**: Are all checks passing on the main branch?
- **Environment variables**: Is `.env.example` complete and accurate? Are all required vars documented?
- **Database**: Are all Prisma migrations applied cleanly? Is the seed script current?
- **Monitoring**: Is error tracking or logging in place?
- **Health checks**: Does the API have a health endpoint that validates dependencies?

### DevX Engineer — consult: documentation-generation

Read the agent definition from `.claude/agents/devx-engineer.md` and use the specified model.

- Is README.md accurate for a fresh developer clone-to-running experience?
- Is `docs/DEVELOPMENT.md` current with all prerequisites and setup steps?
- Is `docs/INDEX.md` up to date with all documentation files?
- Are all new docs files from this phase indexed?

Record all findings for the GTM Council. Do not checkpoint here.

## Step 8: Activate GTM Council

Invoke the following plugins for input:

- `business-analytics` for KPI framework, metrics guidance, and financial analysis patterns
- `content-marketing` for content strategy and competitive research

> **Model Selection**: See the [Model Selection](../../README.md#model-selection) section in README.md for mapping agent model specs to Task tool parameters.

Activate the **GTM Council** (5 members from `.claude/councils/gtm-council.md`). Provide all findings from Steps 2-7 as input to each council member.

### Product Strategist (Lead) — consult: content-marketing

- Market positioning accuracy for this phase's capabilities
- Messaging effectiveness and clarity
- Launch tactics: channels, timing, sequencing
- Competitive differentiation given current feature set
- **Vote**: Approve / Concern / Block
- **Rationale**: [Explanation]

### Business Ops Lead — consult: business-analytics

- Pricing validation: is the price justified by the current feature set?
- Revenue impact: what conversion path exists?
- Competitive positioning: how does pricing compare?
- Risk assessment: what could go wrong at launch?
- **Vote**: Approve / Concern / Block
- **Rationale**: [Explanation]

### Content Reviewer — consult: seo-technical-optimization, seo-content-creation

- Final content accuracy verdict based on Step 5 findings
- SEO readiness score
- Style compliance summary
- Are there any claims that could erode user trust?
- **Vote**: Approve / Concern / Block
- **Rationale**: [Explanation]

### Design Lead — consult: ui-design

- Brand consistency across all surfaces (marketing, app, emails)
- Visual polish: is the UI production-ready?
- UX coherence: does the product experience match marketing promises?
- **Vote**: Approve / Concern / Block
- **Rationale**: [Explanation]

### Lean Delivery Lead

- MVP completeness: are all planned features for this phase shipped?
- Feature flags: are unfinished features properly gated?
- Shipped vs. promised: gap analysis between marketing and reality
- Launch timeline: is the timing realistic?
- **Vote**: Approve / Concern / Block
- **Rationale**: [Explanation]

### Council Verdict

Tally votes and produce a consolidated verdict using the consensus rules from `.claude/councils/gtm-council.md`:

- **Approved**: All members vote Approve or Concern (no Blocks)
- **Needs Changes**: One or more Concern votes on blocking items, implement recommendations
- **Blocked**: One or more Block votes, fundamental issues must be resolved before launch

List all blocking issues identified across the council.

### CHECKPOINT: Present the GTM Council results to the user.

Show:

1. Each member's vote and rationale
2. The consolidated verdict (Approved / Needs Changes / Blocked)
3. Blocking issues list
4. Non-blocking recommendations

Wait for user approval of the assessment before generating the final report.

## Step 9: Generate Consolidated Report

Synthesize all findings from Steps 2-8 into a comprehensive GTM report document.

### Report File

Use the template at `.claude/skills/gtm-review/GTM-REPORT-TEMPLATE.md` as the structure for the report. Write the completed report to `docs/decisions/` using the next available decision number:

1. **Determine the next decision number**: Read `docs/decisions/INDEX.md` and find the highest existing decision number. Increment by 1, zero-padded to 3 digits.

2. **File name**: `docs/decisions/NNN-<phase>-gtm-review.md` (e.g., `021-m1-gtm-review.md`)

3. **Fill in all template sections** with real data from Steps 2-8. Replace all placeholder text. Remove sections that are not applicable to this phase, but keep the overall structure intact.

4. **Frontmatter**: Update the `description` field to summarize the phase and verdict:
   ```yaml
   ---
   type: reference
   description: GTM launch readiness report for M1 -- [Approved/Needs Changes/Blocked]. Covers marketing, code quality, performance, accessibility, infrastructure, and business positioning.
   ---
   ```

### Report Sections

The template covers all required sections. Ensure each is populated with findings from the corresponding step:

- **Executive Summary** — Phase overview and council vote tallies
- **Phase Inventory** — Capabilities matrix and gap analysis from Step 1
- **Blocking / High / Medium / Low Priority Issues** — Categorized findings from all steps
- **Automated Quality Checks** — Results from Step 2
- **Performance Readiness** — Frontend and backend findings from Step 3
- **Accessibility Compliance** — WCAG audit results from Step 4
- **Content & Marketing Audit** — Content accuracy, SEO, style compliance from Step 5
- **Code Quality Summary** — Review Council votes from Step 6
- **Infrastructure Readiness** — Platform and docs findings from Step 7
- **GTM Council Votes** — Each member's vote, rationale, and strategic recommendations from Step 8
- **Success Metrics** — Validation of GTM issue metrics
- **Action Items and Next Steps** — Consolidated from all findings

### CHECKPOINT: Present the full consolidated report to the user. Wait for approval before writing the file and posting to GitHub.

## Step 10: Write Report, Update GTM Issue & Hand Off

### Write the Report File and Commit

Write the completed report to `docs/decisions/NNN-<phase>-gtm-review.md`.

After writing the report file and updating the decisions index (below), commit the artifacts:

```bash
git add docs/decisions/
git commit -m "docs(gtm): add GTM review report for <phase>"
```

### Update the Decisions Index

Add a row to `docs/decisions/INDEX.md` in the decisions table. Insert the new row at the top of the table (after the header), following the existing format:

```markdown
| NNN | [Phase GTM Review](NNN-<phase>-gtm-review.md) | YYYY-MM-DD | Review + GTM | Approved / Needs Changes / Blocked | gtm, launch readiness, <phase>, marketing, performance, accessibility |
```

Use the verdict as the Status column value (e.g., "Approved", "Needs Changes", "Blocked").

### Post the Report to GitHub

Post the consolidated report as a comment on the GTM issue:

```bash
gh issue comment <issue-number> --body "<report>"
```

> [!TIP]
> Use a HEREDOC for the report body to preserve formatting:
>
> ```bash
> gh issue comment <number> --body "$(cat <<'EOF'
> ## GTM Review Results
> ...report content...
> EOF
> )"
> ```

### Update Checklist Items

If the GTM issue body contains checklists, update them based on findings:

- Check items that pass: `- [x] Item`
- Add notes to items that need work: `- [ ] Item -- [GTM Review: needs attention because...]`

Use `gh issue edit` to update the body if needed.

### Close GTM Issue (Conditional)

If the GTM review verdict is **Approved** and the user approved the report:

1. **CHECKPOINT**: Ask the user whether to close the GTM issue now that the review is complete. Present the issue number and title for confirmation.
2. If approved, close the issue:
   ```bash
   gh issue close <number> --reason completed
   ```

If the verdict is **Needs Changes** or **Blocked**, do not offer to close the issue.

### Hand Off

> [!IMPORTANT]
> This skill does NOT replace the `/security-audit` gate item. The security audit is the final gate in every milestone and must be run separately after the GTM review.

Present to the user:

- **GTM Issue**: Link to the updated issue
- **Report File**: Path to the decision record (e.g., `docs/decisions/021-m1-gtm-review.md`)
- **Verdict**: The consolidated readiness verdict
- **Blocking Issues Count**: How many must-fix items remain
- **Next Steps**:
  - If blocking issues remain: "Fix blocking issues, then re-run `/gtm-review`"
  - If ready: "Run `/security-audit` to complete the final gate item for this phase"

**Stop** — do not proceed to the security audit or any other skill automatically.
