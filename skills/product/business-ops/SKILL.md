---
name: business-ops
description: "Business operations: strategy, technology, growth, competitive intelligence, support, finance, HR, legal, operations, sales, productivity, product management."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    # Strategy/CEO
    - "should we"
    - "evaluate opportunity"
    - "trade-off"
    - "worth it"
    - "invest in"
    - "strategy"
    # Technology/CTO
    - "build vs buy"
    - "vendor evaluation"
    - "adopt"
    - "technology choice"
    - "tech stack"
    # Growth/CMO
    - "grow audience"
    - "growth"
    - "brand"
    - "positioning"
    - "community building"
    # Competitive
    - "competitive analysis"
    - "market landscape"
    - "differentiation"
    # Evaluation
    - "feasibility"
    - "effort estimate"
    - "ROI"
    - "priority"
    - "project evaluation"
    - "go no go"
    - "viability"
    # Customer Support
    - "customer support"
    - "ticket triage"
    - "support response"
    - "knowledge base"
    - "KB article"
    - "escalation"
    - "customer research"
    # Finance
    - "finance"
    - "journal entry"
    - "reconciliation"
    - "variance analysis"
    - "financial statements"
    - "financial audit"
    - "month-end close"
    - "SOX"
    # HR
    - "HR"
    - "human resources"
    - "recruiting"
    - "performance review"
    - "compensation"
    - "hiring"
    - "onboarding"
    - "org planning"
    # Legal
    - "legal"
    - "contract review"
    - "compliance check"
    - "NDA"
    - "legal risk"
    - "legal brief"
    - "vendor check"
    - "german compliance"
    - "DSGVO"
    - "GoBD"
    - "TDDDG"
    - "AI Act compliance"
    - "eIDAS"
    # Operations
    - "operations"
    - "vendor review"
    - "runbook"
    - "process documentation"
    - "risk assessment"
    - "capacity plan"
    - "change management"
    - "compliance tracking"
    # Sales
    - "sales"
    - "call prep"
    - "pipeline review"
    - "forecast"
    - "draft outreach"
    - "prospect research"
    - "competitive intelligence"
    # Productivity
    - "productivity"
    - "task management"
    - "daily plan"
    - "weekly review"
    - "meeting agenda"
    - "focus time"
    - "goal setting"
    - "status update"
    - "time management"
    - "prioritize tasks"
    - "standup"
    - "retrospective"
    # Product Management
    - "product management"
    - "feature spec"
    - "PRD"
    - "roadmap"
    - "stakeholder update"
    - "user research"
    - "sprint planning"
    - "product metrics"
  not_for: "micro library choices (use decision-helper), writing content, SEO of specific posts, or tactical marketing competitive analysis (use marketing) — this is executive strategy, not campaign execution. Code security audits, vulnerability scanning, or auth-flow reviews (use security-review) — only financial/accounting audit and SOX compliance. Code performance review (use reviewer-code) — this covers people performance reviews and HR operations. Software task specs, requirements, or plan-lifecycle management (use planning) — this skill prioritizes and tracks work, not specs. UX design methodology, wireframes, or accessibility audits (use design) — this handles product strategy, roadmaps, user research for feature prioritization."
  complexity: Medium
  category: decision-support
  pairs_with:
    - marketing
    - data-analysis
---

# Business Operations

Umbrella skill for all business functions: executive strategy (CEO/CTO/CMO), competitive intelligence, project evaluation, customer support, finance, HR, legal, operations, sales, productivity, and product management. Each domain loads its own reference files on demand — this skill detects the mode, loads the right references, and executes the appropriate framework.

**Scope**: Business decisions and operational workflows. Use decision-helper for technical architecture micro-choices, domain agents for code, voice-writer for content, and systematic-debugging for debugging.

---

## Mode Detection

Classify the user's request into exactly one mode before proceeding. If the request spans multiple modes, choose the primary one and note the secondary.

| Mode | Signal Phrases | Reference |
|------|---------------|-----------|
| **STRATEGY** | Market entry, partnerships, resource allocation, opportunity, "should I/we", strategic pivots, investment | `references/csuite.md` |
| **TECHNOLOGY** | Build vs buy, vendor, SaaS, tech stack, architecture, adopt, technology choice | `references/csuite.md` |
| **GROWTH** | Content strategy, audience, SEO, marketing, brand, community, positioning, channel | `references/csuite.md` |
| **COMPETITIVE** | Competitor, competition, market landscape, differentiation, positioning against, market share | `references/csuite.md` |
| **EVALUATION** | Feasibility, effort estimate, ROI, priority, go/no-go, viability, "is it worth it" | `references/csuite.md` |
| **SUPPORT** | Customer support, ticket triage, support response, knowledge base, KB article, escalation | `references/customer-support.md` |
| **FINANCE** | Finance, journal entry, reconciliation, variance analysis, financial statements, audit, SOX, month-end close | `references/finance.md` |
| **HR** | HR, recruiting, performance review, compensation, hiring, onboarding, org planning | `references/hr.md` |
| **LEGAL** | Legal, contract review, compliance check, NDA, legal risk, legal brief, vendor check, DSGVO, GoBD | `references/legal.md` |
| **OPERATIONS** | Operations, vendor review, runbook, process documentation, risk assessment, capacity plan, change management | `references/operations.md` |
| **SALES** | Sales, call prep, pipeline review, forecast, draft outreach, prospect research, competitive intelligence | `references/sales.md` |
| **PRODUCTIVITY** | Productivity, task management, daily plan, weekly review, meeting agenda, focus time, goal setting, standup | `references/productivity.md` |
| **PRODUCT** | Product management, feature spec, PRD, roadmap, stakeholder update, user research, sprint planning, metrics | `references/product-management.md` |

---

## Reference Loading Table

Load references based on the detected mode. Load only the references required by the mode.

| Signal | Mode | Reference |
|--------|------|-----------|
| Market entry, partnerships, resource allocation, opportunity | STRATEGY | `references/strategic-frameworks.md`, `references/decision-matrices.md` |
| Build vs buy, vendor, SaaS, tech stack, architecture | TECHNOLOGY | `references/tco-framework.md`, `references/vendor-evaluation.md` |
| Content, audience, SEO, marketing, brand, community | GROWTH | `references/audience-segmentation.md`, `references/channel-evaluation.md` |
| Competitor, market landscape, positioning, differentiation | COMPETITIVE | `references/competitive-mapping.md`, `references/market-positioning.md` |
| Feasibility, effort, ROI, priority, go/no-go | EVALUATION | `references/feasibility-scoring.md`, `references/roi-frameworks.md` |
| Ticket triage, support response, KB article, escalation, customer research | SUPPORT | `references/customer-support.md` |
| Journal entry, reconciliation, variance, financial statements, audit, SOX | FINANCE | `references/finance.md` |
| Recruiting, performance review, compensation, hiring, onboarding, org planning | HR | `references/hr.md` |
| Contract review, compliance check, NDA, legal risk, legal brief, DSGVO, GoBD | LEGAL | `references/legal.md` |
| Vendor review, runbook, process documentation, risk assessment, capacity plan, change management | OPERATIONS | `references/operations.md` |
| Call prep, pipeline review, forecast, draft outreach, prospect research | SALES | `references/sales.md` |
| Task management, daily plan, weekly review, meeting agenda, goal setting, standup | PRODUCTIVITY | `references/productivity.md` |
| Feature spec, PRD, roadmap, stakeholder update, user research, sprint planning, metrics | PRODUCT | `references/product-management.md` |

---

## Instructions

For each mode, load the corresponding reference file for the full framework and instructions:

- **STRATEGY, TECHNOLOGY, GROWTH, COMPETITIVE, EVALUATION**: Load `references/csuite.md`
- **SUPPORT**: Load `references/customer-support.md`
- **FINANCE**: Load `references/finance.md`
- **HR**: Load `references/hr.md`
- **LEGAL**: Load `references/legal.md`
- **OPERATIONS**: Load `references/operations.md`
- **SALES**: Load `references/sales.md`
- **PRODUCTIVITY**: Load `references/productivity.md`
- **PRODUCT**: Load `references/product-management.md`

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Too many options | 5+ options creating paralysis | Eliminate obviously inferior options first. Get to 2-4 before running full framework. |
| Not enough information | User cannot answer framing questions | Identify 2-3 critical unknowns. Recommend time-boxed research sprint before deciding. |
| Analysis paralysis | Keeps adding criteria or second-guessing | Apply reversibility test. If reversible, recommend best current option with checkpoint. |
| Emotional attachment | User has already decided, wants validation | Name the pattern directly. Ask: stress-test the choice, or genuinely evaluate all options? |

---

## References

| Reference | When to Load | Content |
|-----------|-------------|---------|
| `references/csuite.md` | Any executive strategy mode | Full C-suite decision support frameworks: STRATEGY, TECHNOLOGY, GROWTH, COMPETITIVE, EVALUATION |
| `references/strategic-frameworks.md` | STRATEGY mode | Porter's Five Forces, SWOT scoring, OKR alignment matrices |
| `references/decision-matrices.md` | STRATEGY mode | Weighted decision matrices, ICE/RICE scoring, pre-mortem templates |
| `references/tco-framework.md` | TECHNOLOGY mode | TCO templates, hidden cost checklists, migration cost models |
| `references/vendor-evaluation.md` | TECHNOLOGY mode | Vendor scorecards, RFP criteria, red flag detection, contract checklist |
| `references/audience-segmentation.md` | GROWTH mode | ICP scoring matrix, persona templates, segmentation frameworks |
| `references/channel-evaluation.md` | GROWTH mode | Channel scoring matrices, CAC/LTV models, funnel stage mapping |
| `references/competitive-mapping.md` | COMPETITIVE mode | Landscape map templates, feature matrices, activity tracker |
| `references/market-positioning.md` | COMPETITIVE mode | Positioning maps, differentiation scoring, win/loss frameworks |
| `references/feasibility-scoring.md` | EVALUATION mode | Three-dimension feasibility model, confidence calibration, decision tree |
| `references/roi-frameworks.md` | EVALUATION mode | T-shirt sizing, three-point estimation, risk-adjusted NPV |
| `references/customer-support.md` | SUPPORT mode | Triage, response drafting, KB articles, escalation, customer research |
| `references/finance.md` | FINANCE mode | Journal entries, reconciliation, variance analysis, financial statements, audit/SOX |
| `references/hr.md` | HR mode | Recruiting, performance management, compensation, org planning, people analytics |
| `references/legal.md` | LEGAL mode | Contract review, compliance, NDA triage, risk assessment, legal writing |
| `references/operations.md` | OPERATIONS mode | Runbooks, risk assessment, vendor management, process docs, change management, compliance |
| `references/sales.md` | SALES mode | Call prep, pipeline analysis, outreach, competitive intelligence, forecasting |
| `references/productivity.md` | PRODUCTIVITY mode | Task management, daily/weekly planning, meeting optimization, status updates, goals |
| `references/product-management.md` | PRODUCT mode | Feature specs, roadmaps, stakeholder updates, research synthesis, metrics, sprint planning |
