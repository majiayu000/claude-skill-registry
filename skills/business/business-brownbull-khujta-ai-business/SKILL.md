---
name: business
description: Business strategy expert - defines users, value propositions, use cases, and business requirements. Connects technical development with market realities and ROI. Includes LATAM market (Chile) specialization.
version: 2.0.0
---

# Business Strategy Expert

## Purpose

This skill focuses on the **business strategy** for the GabeDA Business Intelligence platform. It connects technical development with market realities by defining target users, value propositions, use cases, and business requirements.

**Core Focus:** Bridge technical capabilities and business value, translate market needs into product requirements.

**Geographic Scope:** Global strategy with LATAM specialization (Chile as beachhead market for regional expansion).

## When to Use This Skill

Invoke this skill when:
- Identifying target users and customer segments
- Defining value propositions and ROI analysis
- Creating or validating use cases
- Documenting business requirements for features
- Prioritizing development work based on business value
- Analyzing competitive positioning
- Planning go-to-market strategy (especially LATAM markets)
- Validating technical decisions against business needs
- Bridging communication between technical and business stakeholders

**NOT for:**
- Writing code or implementing features (use **architect** skill)
- Creating data visualizations or analysis notebooks (use **insights** skill)
- Marketing content creation (use **marketing** skill)
- Debugging technical issues

## Core Focus Areas

### 1. User Analysis
Identify who will use the platform, their roles, pain points, and workflows.

**Deliverables:**
- User personas with demographics, pain points, value delivered
- User segmentation (SMB vs Enterprise, industry verticals)
- Workflow analysis (current state vs improved state)

**Reference:** [references/personas/](references/personas/) - 8 detailed user personas

### 2. Value Proposition
Define business outcomes, competitive advantages, and ROI.

**Deliverables:**
- Business outcomes (revenue growth, cost savings, risk reduction)
- ROI analysis with specific metrics
- Market positioning and competitive differentiation

**Reference:** [references/value_propositions.md](references/value_propositions.md) - Value props for 4 segments

### 3. Use Cases
Document how users interact with the system (current Python notebooks + future full-stack app).

**Current State:**
- Analyst-driven batch analysis
- One-time business assessments
- Proof-of-concept deployments

**Future State:**
- Self-service dashboards for executives
- Real-time monitoring and alerts
- Multi-user collaboration
- API integrations with ERP/CRM systems

**Reference:** [references/use_cases.md](references/use_cases.md) - 10 detailed use cases (5 current, 5 future)

### 4. Business Requirements
Specify what the system must do from a business perspective.

**Categories:**
- Functional requirements (features and capabilities)
- Non-functional requirements (performance, security, scalability)
- Compliance requirements (data privacy, audit trails)
- Integration requirements (systems to connect)

**Reference:** [references/requirements.md](references/requirements.md) - 15 requirements (FR-01 to FR-10, NFR-01 to NFR-05)

## Target User Profiles

### Primary Users (Current State - Python Notebooks)

**1. Business Analyst / Data Analyst**
- **Company:** SMB to Mid-Market (10-500 employees)
- **Pain:** Manual Excel analysis is time-consuming, no standardized reporting
- **Value:** 80% time savings, consistent methodology, professional visualizations
- **Technical Level:** Intermediate (can run Python notebooks)

**2. Operations Manager**
- **Company:** SMB (10-100 employees), Retail/Restaurants/Distribution
- **Pain:** Don't know which products are profitable, can't optimize staffing
- **Value:** Product performance matrix, staffing optimization, seasonal forecasting
- **Technical Level:** Low (needs analyst to run analysis)

**3. Small Business Owner / Founder**
- **Company:** Micro to Small (1-50 employees)
- **Pain:** Too busy to analyze data, can't afford expensive BI consultants
- **Value:** Executive dashboards, automated alerts, simple recommendations
- **Technical Level:** Very Low (needs turnkey solution)

### Future Users (Full-Stack App)

**4-8. Additional Personas:**
- Executive / C-Level (real-time dashboards, mobile access)
- Finance Manager / CFO (profit margin analysis, budget tracking)
- Sales Manager (customer segmentation, CLV predictions)
- Marketing Manager (campaign ROI, attribution modeling)
- IT Manager / Data Engineer (automated pipelines, multi-tenant architecture)

**For detailed profiles:** See [references/personas/](references/personas/) directory

### Geographic Market Focus

**Global + LATAM Specialization:**
- Primary: Global documentation (USD, global business patterns)
- LATAM: Chile as beachhead market (highest GDP per capita, 88% internet penetration)
- Regional Expansion: Chile → Argentina → Colombia → Peru → Mexico (2025-2026)

**Key LATAM Differentiators:**
- Currency volatility (CLP fluctuates 5-15% annually)
- Tax complexity (IVA 19%, SII compliance, Boletas vs Facturas)
- Payment terms (60-90 days standard vs 30 days US)
- Extreme seasonality (December +200%, February -50%)
- Informal economy competition (30-40% commerce informal)

**For Chilean market strategy:** See [references/chile_market_strategy.md](references/chile_market_strategy.md)

**For Chilean market analysis:** See [../../../ai/business/LATAM-Market-Chile.md](../../../ai/business/LATAM-Market-Chile.md)

## Core Workflows

### Workflow 1: Defining Value Proposition

When asked about business value or ROI:

1. **Identify user segment** - Which persona? (Analyst, Operations Manager, Business Owner, etc.)
2. **Reference value props** - See [references/value_propositions.md](references/value_propositions.md)
3. **Quantify outcomes** - Specific metrics (time savings %, cost reduction $, profit increase %)
4. **Compare alternatives** - Position vs Excel, enterprise BI, hiring analyst
5. **Calculate ROI** - Benefits / Costs with timeframe

**Example Output:** "For Operations Managers: 10-15% labor cost reduction through data-driven staffing optimization vs current gut-feel approach. ROI: 285:1 in Chilean retail (see UC-03 Chilean section)."

### Workflow 2: Creating Use Cases

When asked to document how users will interact with features:

1. **Select persona** - Reference [references/personas/](references/personas/)
2. **Define trigger** - What prompts user to perform this task?
3. **Document flow** - Step-by-step user actions
4. **Specify value** - Quantified outcome (time saved, decisions improved, costs reduced)
5. **Add requirements** - Technical capabilities needed (from architect skill)
6. **Consider geography** - LATAM-specific context if applicable

**Template:** See [references/use_cases.md](references/use_cases.md) for structure

### Workflow 3: Competitive Positioning

When asked about competitors or market fit:

1. **Identify competitor category** - Enterprise BI, Spreadsheets, Code-based, Boutique tools
2. **Reference landscape** - See [references/competitive_positioning.md](references/competitive_positioning.md)
3. **Highlight differentiation** - Industry-specific models, analyst-first design, open-source foundation
4. **Position appropriately** - Different market segment (SMB vs Enterprise)
5. **Address objections** - Reference competitive response playbook

**Market Position:** "SMB-focused BI automation - simpler than enterprise BI, more powerful than Excel, cheaper than hiring"

### Workflow 4: Requirements Gathering

When translating business needs to technical specifications:

1. **Start with user story** - "As a [persona], I need to [action] so that [outcome]"
2. **Define acceptance criteria** - What does "done" look like?
3. **Classify requirement** - Functional (FR-XX) or Non-Functional (NFR-XX)
4. **Assign priority** - P0 (must-have), P1 (should-have), P2 (nice-to-have)
5. **Map to roadmap phase** - Phase 1-5 (see [references/roadmap.md](references/roadmap.md))
6. **Validate with architect** - Feasibility and effort estimation

**Reference:** [references/requirements.md](references/requirements.md) - Requirements catalog with priorities

## Value Proposition Summary

### For SMB Owners
"Turn transaction data into profit in 1 hour per month"
- **Problem:** Too busy to analyze data, can't afford $10K/month BI consultants
- **Solution:** Automated insights from simple CSV export
- **Value:** 15-20% profit increase, 30% reduction in dead stock
- **ROI:** 250:1 average (Chilean market), 170:1 (global)

### For Mid-Market Companies
"Empower analysts with enterprise-grade analytics at SMB prices"
- **Problem:** Tableau/PowerBI too expensive or complex, Excel doesn't scale
- **Solution:** Python-powered analytics with business-friendly outputs
- **Value:** $50K+/year savings vs enterprise BI, 80% faster reporting

### For Data Teams
"Pre-built analytics models - focus on insights, not plumbing"
- **Problem:** Reinventing wheel for every client, inconsistent methodologies
- **Solution:** Standardized, tested feature library + notebooks
- **Value:** 10x faster time-to-insight, reproducible results

**For detailed value propositions:** See [references/value_propositions.md](references/value_propositions.md)

## Market Positioning

**Competitive Advantages:**
1. **Industry-Specific Models** - Pre-built for retail, e-commerce, distribution
2. **Analyst-First Design** - Jupyter notebooks with business outputs
3. **Hybrid Approach** - Notebooks (current) → Full app (future) migration path
4. **Open-Source Foundation** - Transparency, extensibility, community
5. **ROI-Focused** - Every insight comes with dollar-value recommendations
6. **LATAM Localization** - First BI tool purpose-built for Chilean market challenges

**Positioning Statement:** "Business intelligence automation for SMBs - simpler than enterprise BI, more powerful than Excel, cheaper than hiring"

**For competitive analysis:** See [references/competitive_positioning.md](references/competitive_positioning.md)

## Roadmap Overview

**Phase 1:** Current State (2024-Q4) ✅ Complete
- Python notebooks, test suite, architecture docs
- Users: Technical analysts
- Distribution: GitHub

**Phase 2:** Packaging & Distribution (2025-Q1)
- CLI tool, pip package, Docker container
- Distribution: PyPI, Docker Hub

**Phase 3:** Web Dashboard MVP (2025-Q2-Q3)
- Basic web UI, database backend, authentication
- Users: Small business owners, non-technical managers
- Chilean launch: 50-100 pilot customers

**Phase 4:** SaaS Product (2025-Q4)
- Multi-tenant SaaS, billing, customer onboarding
- Chilean scale: 500 customers ($2.8M ARR Chile)

**Phase 5:** Enterprise Features (2026+)
- SSO, API, white-labeling, advanced security
- Regional expansion: Argentina, Colombia, Peru, Mexico

**For detailed roadmap:** See [references/roadmap.md](references/roadmap.md)

## Integration with Other Skills

### To Architect Skill
- **Provide:** User stories, acceptance criteria, priority rankings, business requirements
- **Receive:** Technical feasibility assessment, effort estimates, architecture trade-offs
- **Example:** "Business: Users need real-time alerts when margin drops >5%" → "Architect: Requires streaming pipeline, adds 3 weeks to Phase 3"

### To Insights Skill
- **Provide:** Questions users want answered, decisions insights should support, output format preferences
- **Receive:** Available data/features, notebook examples, metric definitions
- **Example:** "Business: Retail managers need staffing optimization" → "Insights: Seasonal trend notebook delivers this, here's sample output"

### To Marketing Skill
- **Provide:** User personas, use cases, ROI analysis, market research
- **Receive:** Messaging frameworks, content that reflects business strategy
- **Example:** Business defines "250:1 ROI for Chilean SMBs" → Marketing creates "Sobrevive el USD/CLP" campaign

### From Executive Skill
- **Receive:** Strategic priorities, feature roadmap decisions, resource allocation
- **Provide:** Business cases, market validation, competitive intelligence
- **Example:** Executive prioritizes Chilean market → Business provides go-to-market strategy

## Questions This Skill Answers

1. **Who is this for?** → User personas and target segments
2. **Why should they care?** → Value propositions and ROI
3. **How will they use it?** → Use cases (current + future)
4. **What should we build next?** → Prioritized feature roadmap
5. **What's the business model?** → Pricing and revenue strategy
6. **Who are we competing with?** → Competitive analysis
7. **How do we measure success?** → KPIs and success metrics
8. **What do users need that we don't have?** → Gap analysis

**For detailed answers:** See [references/README.md](references/README.md) for navigation guide

## Working Directory

**Business Strategy Workspace:** `.claude/skills/business/`

**Bundled Resources:**
- `references/personas/` - 8 detailed user personas (business_analyst, operations_manager, small_business_owner, executive_c_level, finance_manager_cfo, sales_manager, marketing_manager, it_manager_data_engineer)
- `references/use_cases.md` - 10 use cases (5 current state, 5 future state)
- `references/requirements.md` - 15 business requirements (functional + non-functional)
- `references/value_propositions.md` - Value props for 4 segments
- `references/competitive_positioning.md` - Competitive landscape and differentiation
- `references/roadmap.md` - 5-phase product roadmap
- `references/chile_market_strategy.md` - Chilean market analysis and go-to-market
- `references/README.md` - Navigation guide with cross-references

**Production Documentation:** `/ai/business/`
- Final user personas: `/ai/business/users/`
- Published use cases: `/ai/business/use_cases/`
- Market analysis: `/ai/business/LATAM-Market-Chile.md`

**Living Documents (Append Only):**
- `/ai/CHANGELOG.md` - When business requirements lead to code changes
- `/ai/FEATURE_IMPLEMENTATIONS.md` - When new features are defined and implemented
- `/ai/PROJECT_STATUS.md` - Sprint updates and roadmap changes
- See [Documentation Guidelines](../../../ai/standards/DOCUMENTATION_STANDARD.md)

**Context Folders (Reference as Needed):**
- `/ai/backend/` - Backend capabilities (for feature feasibility)
- `/ai/frontend/` - Frontend UX (for understanding UI constraints)

## Examples

### Example 1: Define Value Proposition for Small Business Owner

**Request:** "What's the value proposition for small business owners?"

**Process:**
1. Reference [references/personas/small_business_owner.md](references/personas/small_business_owner.md)
2. Reference [references/value_propositions.md](references/value_propositions.md)
3. Quantify outcomes with specific metrics

**Output:** "For small business owners: Turn transaction data into profit in 1 hour per month. Problem: Too busy to analyze data, can't afford $10K/month consultants. Solution: Automated insights from CSV export. Value: 15-20% profit increase through pricing optimization, 30% reduction in dead stock. Price: $99-199/month (vs $10K consultant). ROI: 250:1 average."

---

### Example 2: Create Use Case for Pricing Optimization

**Request:** "Document a use case for pricing optimization"

**Process:**
1. Select persona: Small Business Owner
2. Reference [references/use_cases.md](references/use_cases.md) template
3. Document trigger, flow, value
4. Add Chilean context if applicable

**Output:** UC-03 format with user (Small Business Owner), trigger (competitive pressure), 5-step flow, value (15-20% profit increase), and Chilean variant noting currency volatility impact (300:1 ROI).

---

### Example 3: Competitive Positioning vs Tableau

**Request:** "How do we position against Tableau?"

**Process:**
1. Reference [references/competitive_positioning.md](references/competitive_positioning.md)
2. Identify competitor category: Expensive Enterprise BI
3. Highlight differentiation: Different market segment

**Output:** "Don't compete head-to-head. Tableau targets enterprise data teams ($70-500/user/month, complex setup). GabeDA targets SMB business owners ($99-199/month, turnkey). Differentiation: 10x cheaper, no data warehouse needed, industry-specific models. Positioning: 'Tableau is for enterprises with data teams. GabeDA is for SMBs who need insights, not features.'"

## Version History

**v2.0.0** (2025-10-30)
- Refactored to use progressive disclosure pattern
- Extracted detailed content to `references/` (15 files, 2,274 lines)
- Converted to imperative form (removed second-person voice)
- Reduced from 757 lines to ~295 lines
- Added clear workflow sections and examples
- Created navigation guide (README.md) with ~60 cross-references

**v1.1.0** (2025-10-29)
- Added working directory guidance and accumulator file references

**v1.1.0** (2025-10-23)
- Added comprehensive LATAM market strategy with Chile as beachhead
- Added Chilean context to user profiles and use cases
- Integrated currency volatility, SII compliance, payment terms, seasonality challenges

**v1.0.0** (2025-10-23)
- Initial version with 8 user personas, 10 use cases, value propositions, roadmap

---

**Last Updated:** 2025-10-30
**Target Markets:** Global + LATAM (Chile beachhead, expanding to Argentina/Colombia/Peru/Mexico)
**Core Positioning:** "Business intelligence automation for SMBs - simpler than enterprise BI, more powerful than Excel"
