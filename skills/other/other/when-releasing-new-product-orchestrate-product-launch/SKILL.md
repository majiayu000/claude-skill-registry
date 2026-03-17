---
name: when-releasing-new-product-orchestrate-product-launch
type: sop-workflow
description: |
  Use when launching a new product end-to-end from market research through post-launch monitoring.
  Orchestrates 15+ specialist agents across 5 phases in a 10-week coordinated workflow including
  research, development, marketing, sales preparation, launch execution, and ongoing optimization.
  Employs hierarchical coordination with parallel execution for efficiency and comprehensive coverage.
agents:
  - market-researcher
  - business-analyst
  - product-manager
  - backend-developer
  - frontend-developer
  - mobile-developer
  - database-architect
  - security-specialist
  - qa-engineer
  - marketing-specialist
  - sales-specialist
  - content-creator
  - seo-specialist
  - devops-engineer
  - production-validator
  - performance-monitor
  - customer-support-specialist
phases: 5
memory_pattern: "product-launch/{launch-id}/phase-{N}/{agent}/{deliverable}"
---

# Product Launch Orchestration Workflow

Complete end-to-end product launch workflow orchestrating 15+ specialist agents across research, development, marketing, launch execution, and post-launch monitoring. Designed for comprehensive product launches requiring coordination across technical, marketing, sales, and operations teams.

## Overview

This SOP orchestrates a complete 10-week product launch using multi-agent coordination with hierarchical topology. The workflow balances sequential dependencies with parallel execution to optimize both speed and quality. Each phase produces specific deliverables stored in memory for subsequent phases to consume, ensuring continuity and context preservation.

## Trigger Conditions

Use this workflow when:
- Launching a new product or major feature requiring comprehensive go-to-market
- Coordinating across multiple teams (engineering, marketing, sales, support)
- Need systematic approach covering all launch aspects from research to post-launch
- Timeline spans multiple weeks with clear phases and deliverables
- Require coordination between development, marketing campaigns, and sales enablement
- Post-launch monitoring and optimization are critical to success

## Orchestrated Agents (15 Total)

### Research & Planning Agents
- **`market-researcher`** - Market analysis, competitive research, customer insights, trend identification
- **`business-analyst`** - SWOT analysis, business model validation, revenue projections, risk assessment
- **`product-manager`** - Product strategy, feature prioritization, positioning, go-to-market planning

### Development & Engineering Agents
- **`backend-developer`** - REST/GraphQL API development, server-side logic, business layer implementation
- **`frontend-developer`** - Web UI development, React/Vue components, state management, client integration
- **`mobile-developer`** - iOS/Android applications, React Native, cross-platform, offline sync
- **`database-architect`** - Schema design, query optimization, indexing strategy, data modeling
- **`security-specialist`** - Security audits, vulnerability scanning, compliance validation, penetration testing
- **`qa-engineer`** - Test suite creation, integration testing, E2E testing, performance validation

### Marketing & Sales Agents
- **`marketing-specialist`** - Campaign creation, audience segmentation, multi-channel strategy, KPI tracking
- **`sales-specialist`** - Sales enablement, pipeline setup, lead qualification, revenue forecasting
- **`content-creator`** - Blog posts, social media content, email sequences, video scripts, landing pages
- **`seo-specialist`** - Keyword research, on-page SEO, link building, search optimization

### Launch & Operations Agents
- **`devops-engineer`** - CI/CD pipelines, Docker/K8s deployment, infrastructure setup, monitoring configuration
- **`production-validator`** - Production readiness assessment, go/no-go decision, deployment validation
- **`performance-monitor`** - Metrics collection, alert configuration, anomaly detection, dashboard setup
- **`customer-support-specialist`** - Support infrastructure, knowledge base, ticket workflows, team training

## Workflow Phases

### Phase 1: Research & Planning (Week 1-2, Sequential → Parallel)

**Duration**: 2 weeks
**Execution Mode**: Sequential analysis then parallel strategy
**Agents**: `market-researcher`, `business-analyst`, `product-manager`

**Process**:

1. **Conduct Comprehensive Market Analysis** (Day 1-3)
   ```bash
   npx claude-flow hooks pre-task --description "Product launch: ${PRODUCT_NAME}"
   npx claude-flow swarm init --topology hierarchical --max-agents 15
   npx claude-flow agent spawn --type researcher
   ```

   Spawn `market-researcher` agent to:
   - Analyze target market size, demographics, and segmentation
   - Research competitors (features, pricing, positioning, market share)
   - Identify market trends, opportunities, and threats
   - Document customer pain points and unmet needs
   - Validate product-market fit hypotheses

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "product-launch/${LAUNCH_ID}/phase-1/market-researcher/analysis" \
     --value "${MARKET_ANALYSIS_JSON}"
   ```

2. **Perform Business Analysis** (Day 4-6)

   Retrieve market analysis and spawn `business-analyst` agent:
   ```bash
   npx claude-flow memory retrieve --key "product-launch/${LAUNCH_ID}/phase-1/market-researcher/analysis"
   npx claude-flow agent spawn --type analyst
   ```

   Conduct:
   - SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
   - Business model validation and monetization strategy
   - Revenue projections and financial modeling (3-year forecast)
   - Risk assessment and mitigation strategies
   - Competitive differentiation analysis

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "product-launch/${LAUNCH_ID}/phase-1/business-analyst/strategy"
   ```

3. **Define Product Strategy** (Day 7-10)

   Retrieve market and business analysis, spawn `product-manager` agent:
   ```bash
   npx claude-flow memory retrieve --pattern "product-launch/${LAUNCH_ID}/phase-1/*/analysis"
   npx claude-flow agent spawn --type planner
   ```

   Define:
   - Product positioning statement and value proposition
   - Feature prioritization (MVP vs future roadmap)
   - Pricing strategy (tiers, packaging, discounts)
   - Go-to-market strategy and launch timeline
   - Success metrics and KPIs

   **Memory Storage**:
   ```bash
   npx claude-flow memory store --key "product-launch/${LAUNCH_ID}/phase-1/product-manager/plan"
   npx claude-flow hooks post-task --task-id "phase-1-planning"
   ```

**Outputs**:
- Market analysis report with competitive landscape
- SWOT analysis and business validation
- Product strategy document with positioning and pricing
- Launch timeline with milestones

**Success Criteria**:
- [ ] Market opportunity clearly quantified (TAM, SAM, SOM)
- [ ] Competitive differentiation documented
- [ ] Business model validated with financial projections
- [ ] Product strategy approved by stakeholders
- [ ] Phase 1 deliverables stored in memory

---

### Phase 2: Product Development (Week 3-8, Parallel Execution)

**Duration**: 6 weeks
**Execution Mode**: Parallel with mesh coordination
**Agents**: `backend-developer`, `frontend-developer`, `mobile-developer`, `database-architect`, `security-specialist`, `qa-engineer`

**Process**:

1. **Initialize Development Swarm** (Day 1)
   ```bash
   npx claude-flow swarm init --topology mesh --max-agents 6 --strategy adaptive
   npx claude-flow memory retrieve --key "product-launch/${LAUNCH_ID}/phase-1/product-manager/plan"
   ```

2. **Parallel Development Execution** (Week 3-6)

   Spawn all development agents concurrently:
   ```bash
   # Backend development
   npx claude-flow agent spawn --type backend-dev --capabilities "api,authentication,database"

   # Frontend development
   npx claude-flow agent spawn --type coder --capabilities "react,ui,state-management"

   # Mobile development
   npx claude-flow agent spawn --type mobile-dev --capabilities "react-native,ios,android"

   # Database architecture
   npx claude-flow agent spawn --type code-analyzer --capabilities "database,schema,optimization"

   # Security implementation
   npx claude-flow agent spawn --type reviewer --capabilities "security,audit,compliance"

   # QA and testing
   npx claude-flow agent spawn --type tester --capabilities "testing,automation,coverage"
   ```

   **Backend Developer** builds:
   - REST/GraphQL API with comprehensive endpoints
   - Authentication system (OAuth 2.0, JWT)
   - Business logic layer with validation
   - Payment gateway integration
   - Database integration and ORM setup

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-2/backend-developer/{api-spec,schema,implementation}`

   **Frontend Developer** builds:
   - React/Vue web application with responsive design
   - Component library following design system
   - State management (Redux/Context/Zustand)
   - API integration layer with error handling
   - Progressive Web App (PWA) capabilities

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-2/frontend-developer/{components,architecture}`

   **Mobile Developer** builds:
   - React Native applications (iOS + Android)
   - Native modules for device features
   - Offline-first architecture with sync
   - Push notifications integration
   - Deep linking and analytics

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-2/mobile-developer/{builds,native-modules}`

   **Database Architect** designs:
   - Optimized schema for scalability
   - Indexing strategy for performance
   - Query optimization and stored procedures
   - Data migration strategy
   - Backup, recovery, and disaster recovery plans

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-2/database-architect/{schema,indexes,migrations}`

   **Security Specialist** implements:
   - OAuth 2.0 + JWT authentication
   - Role-based access control (RBAC)
   - Data encryption (at rest and in transit)
   - Security audit and penetration testing
   - Compliance validation (GDPR, CCPA, SOC2)

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-2/security-specialist/{audit,compliance}`

   **QA Engineer** creates:
   - Unit test suite (target: 90%+ coverage)
   - Integration test scenarios
   - End-to-end test workflows
   - Performance benchmarks
   - Automated test pipeline

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-2/qa-engineer/{test-plan,coverage-report}`

3. **Integration & Testing** (Week 7-8)

   Sequential integration after parallel development:
   ```bash
   npx claude-flow task orchestrate --strategy sequential --task "system-integration"
   ```

   - Integrate all components (backend + frontend + mobile)
   - Run full integration test suite
   - Performance optimization (< 200ms API response, < 2s page load)
   - Final security audit

   **Coordination Scripts**:
   ```bash
   npx claude-flow hooks post-edit --file "src/**/*.{ts,tsx}" \
     --memory-key "product-launch/${LAUNCH_ID}/phase-2/integration/status"
   npx claude-flow hooks notify --message "Phase 2 development complete"
   ```

**Outputs**:
- Production-ready web application
- Native mobile applications (iOS + Android)
- API documentation (OpenAPI spec)
- Security audit report
- Performance benchmark results
- Test coverage report (>90%)

**Success Criteria**:
- [ ] All applications functional and integrated
- [ ] Test coverage exceeds 90%
- [ ] Security audit passed with no critical issues
- [ ] Performance benchmarks met (API < 200ms, UI < 2s)
- [ ] All deliverables stored in memory for next phase

---

### Phase 3: Marketing & Sales Preparation (Week 5-9, Parallel Execution)

**Duration**: 4-5 weeks (overlaps with development)
**Execution Mode**: Parallel marketing campaigns
**Agents**: `marketing-specialist`, `sales-specialist`, `content-creator`, `seo-specialist`

**Process**:

1. **Initialize Marketing Swarm** (Week 5)
   ```bash
   npx claude-flow swarm init --topology star --max-agents 4 --strategy specialized
   npx claude-flow memory retrieve --key "product-launch/${LAUNCH_ID}/phase-1/product-manager/plan"
   ```

2. **Parallel Campaign Creation** (Week 5-7)

   Spawn all marketing agents concurrently:
   ```bash
   npx claude-flow task orchestrate --strategy parallel --priority high
   ```

   **Marketing Specialist** creates:
   - Multi-channel campaign strategy (email, social, paid ads, PR)
   - Audience segmentation and targeting
   - Campaign timeline aligned with launch date
   - Budget allocation across channels
   - KPI tracking and analytics setup

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-3/marketing-specialist/{campaign,metrics}`

   **Content Creator** produces:
   - Product landing page copy (hero, features, testimonials, CTA)
   - Blog posts (3-5 pre-launch, 10+ post-launch schedule)
   - Social media content calendar (50+ posts across platforms)
   - Email sequences (welcome, onboarding, nurture, re-engagement)
   - Video demos, tutorials, and explainer videos

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-3/content-creator/{landing-page,blog,social,email}`

   **SEO Specialist** optimizes:
   - Keyword research and mapping (primary, secondary, long-tail)
   - On-page SEO (meta tags, headers, schema markup)
   - Content optimization for search intent
   - Link building strategy and outreach plan
   - Technical SEO audit and fixes

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-3/seo-specialist/{keywords,seo-plan}`

3. **Sales Enablement** (Week 7-9)

   **Sales Specialist** prepares:
   - Product demo scripts and presentation decks
   - Sales playbook with objection handling
   - Pricing calculator and proposal templates
   - CRM configuration and automation workflows
   - Sales pipeline stages and conversion targets

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-3/sales-specialist/{enablement,pipeline}`

4. **Support Infrastructure** (Week 8-9)

   **Customer Support Specialist** sets up:
   - Help desk software and ticket workflows
   - Knowledge base articles (50+ FAQ entries)
   - Support team training materials
   - Escalation procedures and SLAs
   - Self-service resources (docs, videos, troubleshooting)

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-3/customer-support-specialist/{knowledge-base,workflows}`

   **Coordination**:
   ```bash
   npx claude-flow hooks post-task --task-id "phase-3-marketing-prep"
   npx claude-flow memory retrieve --pattern "product-launch/${LAUNCH_ID}/phase-3/*"
   ```

**Outputs**:
- Multi-channel marketing campaign (ready to execute)
- Complete content library (landing page, blog, social, email)
- SEO optimization plan with keyword targeting
- Sales enablement kit with playbooks and tools
- Support infrastructure and knowledge base

**Success Criteria**:
- [ ] Marketing campaigns ready for launch day
- [ ] Content calendar planned for 3 months post-launch
- [ ] SEO foundation established (technical + content)
- [ ] Sales team trained and equipped with materials
- [ ] Support infrastructure tested and operational

---

### Phase 4: Launch Execution (Week 10, Sequential + Parallel)

**Duration**: 1 week
**Execution Mode**: Sequential validation, parallel launch activities
**Agents**: `production-validator`, `devops-engineer`, `marketing-specialist`, `sales-specialist`

**Process**:

1. **Pre-Launch Validation** (Day 1-2)
   ```bash
   npx claude-flow hooks pre-task --description "Final production validation"
   npx claude-flow agent spawn --type production-validator
   ```

   **Production Validator** verifies:
   - All tests passing (unit, integration, E2E)
   - Security audit complete with zero critical issues
   - Performance benchmarks met or exceeded
   - Monitoring and alerting systems active
   - Backup and recovery procedures tested
   - Rollback plan documented and rehearsed

   Generate go/no-go report:
   ```bash
   npx claude-flow memory store --key "product-launch/${LAUNCH_ID}/phase-4/production-validator/final-check"
   ```

2. **Production Deployment** (Day 2-3)
   ```bash
   npx claude-flow agent spawn --type cicd-engineer
   ```

   **DevOps Engineer** executes:
   - Blue-green deployment to production
   - Frontend deployment to CDN (global distribution)
   - Mobile app submission (App Store + Google Play)
   - Production database configuration and migration
   - Monitoring, logging, and alerting activation

   **Deployment Script**:
   ```bash
   npx claude-flow workflow create --name "production-deployment" \
     --steps '["backend","frontend","mobile","monitoring"]'
   npx claude-flow workflow execute --workflow-id "prod-deploy-${LAUNCH_ID}"
   ```

   **Memory Pattern**: `product-launch/${LAUNCH_ID}/phase-4/devops-engineer/{deployment-log,status}`

3. **Launch Day Marketing Blitz** (Day 3-5, Parallel)
   ```bash
   npx claude-flow task orchestrate --strategy parallel --max-agents 4
   ```

   Parallel campaign execution:
   - **Email Marketing**: Launch announcement to existing list, automated sequences
   - **Social Media**: Coordinated posts across all platforms, engagement monitoring
   - **Paid Advertising**: Google Ads, Facebook/Instagram, LinkedIn campaigns live
   - **PR Outreach**: Press releases, influencer partnerships, Product Hunt launch

   **Marketing Coordination**:
   ```bash
   npx claude-flow hooks notify --message "Launch campaigns live"
   npx claude-flow memory store --key "product-launch/${LAUNCH_ID}/phase-4/marketing/campaign-metrics"
   ```

4. **Real-Time Monitoring** (Day 3-7)
   ```bash
   npx claude-flow agent spawn --type performance-monitor
   ```

   **Performance Monitor** tracks:
   - Application uptime and performance metrics
   - User signups, activation, and conversion rates
   - Marketing campaign ROI across all channels
   - Support ticket volume and response times
   - Revenue and transaction tracking

   Generate hourly reports during launch week:
   ```bash
   npx claude-flow hooks post-task --task-id "launch-monitoring" --export-metrics true
   ```

**Outputs**:
- Live production application (web + mobile)
- Active marketing campaigns across all channels
- Sales team actively engaging leads
- Support team handling customer inquiries
- Real-time monitoring dashboards

**Success Criteria**:
- [ ] Production deployment successful with zero downtime
- [ ] All marketing campaigns launched on schedule
- [ ] Monitoring shows healthy system metrics
- [ ] First customer conversions recorded
- [ ] Support team responding within SLA

---

### Phase 5: Post-Launch Monitoring & Optimization (Week 11+, Continuous)

**Duration**: Ongoing
**Execution Mode**: Weekly reviews with adaptive optimization
**Agents**: `performance-monitor`, `business-analyst`, Various optimization agents

**Process**:

1. **Weekly Performance Review** (Every Monday)
   ```bash
   npx claude-flow hooks session-restore --session-id "launch-${LAUNCH_ID}"
   npx claude-flow agent spawn --type analyst
   ```

   **Business Analyst** aggregates:
   - User acquisition metrics (signups, activations, churn)
   - Marketing performance (campaigns, channels, ROI)
   - Sales pipeline progress (leads, opportunities, revenue)
   - Support metrics (tickets, resolution time, satisfaction)
   - Product usage analytics (features, engagement, retention)

   Retrieve all metrics:
   ```bash
   npx claude-flow memory retrieve --pattern "product-launch/${LAUNCH_ID}/phase-5/week-${WEEK_NUM}/*"
   ```

   Generate insights and recommendations:
   ```bash
   npx claude-flow memory store --key "product-launch/${LAUNCH_ID}/phase-5/weekly-report/week-${WEEK_NUM}"
   ```

2. **Adaptive Optimization** (Continuous)

   Based on weekly insights, spawn specialist agents for targeted improvements:

   **If conversion rate is low**:
   ```bash
   npx claude-flow agent spawn --type optimizer --focus "conversion-optimization"
   ```
   - A/B testing on landing page elements
   - Funnel analysis and friction point identification
   - Pricing experiment variations
   - Checkout flow optimization

   **If support volume is high**:
   ```bash
   npx claude-flow agent spawn --type planner --focus "support-optimization"
   ```
   - Identify common issues and root causes
   - Create self-service solutions and documentation
   - Proactive user education (tooltips, guides, videos)
   - Product improvements to prevent issues

   **If marketing ROI is below target**:
   ```bash
   npx claude-flow agent spawn --type researcher --focus "marketing-optimization"
   ```
   - Channel performance analysis
   - Audience segment refinement
   - Ad creative and copy testing
   - Budget reallocation to high-performing channels

3. **Continuous Improvement Cycle**
   ```bash
   npx claude-flow hooks post-task --task-id "weekly-optimization-${WEEK_NUM}"
   npx claude-flow hooks session-end --export-metrics true
   ```

   Store learnings for future launches:
   ```bash
   npx claude-flow memory store --key "product-launch/learnings/${LAUNCH_ID}" \
     --value "${LESSONS_LEARNED_JSON}"
   ```

**Outputs**:
- Weekly performance reports with trends
- Continuous product improvements and iterations
- Optimized marketing campaigns (improved ROI)
- Enhanced customer experience (reduced friction)
- Documented learnings for future launches

**Success Criteria**:
- [ ] Weekly reports delivered on schedule
- [ ] Key metrics trending positively week-over-week
- [ ] Customer satisfaction scores improving
- [ ] Product-market fit validated through usage data
- [ ] Launch learnings documented for knowledge sharing

---

## Memory Coordination

### Namespace Convention

All workflow data follows this hierarchical pattern:

```
product-launch/{launch-id}/phase-{N}/{agent-type}/{deliverable-type}
```

**Examples**:
- `product-launch/saas-app-v1/phase-1/market-researcher/analysis`
- `product-launch/saas-app-v1/phase-2/backend-developer/api-spec`
- `product-launch/saas-app-v1/phase-3/marketing-specialist/campaign`
- `product-launch/saas-app-v1/phase-4/devops-engineer/deployment-log`
- `product-launch/saas-app-v1/phase-5/weekly-report/week-1`

### Cross-Phase Data Flow

**Phase 1 → Phase 2**:
```bash
# Phase 2 agents retrieve Phase 1 strategy
npx claude-flow memory retrieve --key "product-launch/${LAUNCH_ID}/phase-1/product-manager/plan"
```

**Phase 2 → Phase 3**:
```bash
# Marketing agents retrieve product specs
npx claude-flow memory retrieve --key "product-launch/${LAUNCH_ID}/phase-2/backend-developer/api-spec"
```

**Phase 3 → Phase 4**:
```bash
# Deployment retrieves marketing timeline
npx claude-flow memory retrieve --key "product-launch/${LAUNCH_ID}/phase-3/marketing-specialist/campaign"
```

**Phase 4 → Phase 5**:
```bash
# Monitoring retrieves launch metrics baseline
npx claude-flow memory retrieve --pattern "product-launch/${LAUNCH_ID}/phase-4/*/metrics"
```

---

## Scripts & Automation

### Pre-Workflow Initialization

```bash
#!/bin/bash
# Initialize product launch workflow

PRODUCT_NAME="$1"
LAUNCH_ID="${PRODUCT_NAME}-$(date +%Y%m%d)"

# Setup coordination
npx claude-flow hooks pre-task --description "Product launch: ${PRODUCT_NAME}"

# Initialize hierarchical swarm
npx claude-flow swarm init --topology hierarchical --max-agents 15 --strategy adaptive

# Store launch metadata
npx claude-flow memory store --key "product-launch/${LAUNCH_ID}/metadata" --value '{
  "product_name": "'"${PRODUCT_NAME}"'",
  "launch_id": "'"${LAUNCH_ID}"'",
  "start_date": "'"$(date -I)"'",
  "timeline_weeks": 10,
  "phases": 5
}'

echo "✅ Product launch initialized: ${LAUNCH_ID}"
```

### Per-Phase Coordination

```bash
#!/bin/bash
# Execute specific phase

LAUNCH_ID="$1"
PHASE="$2"

# Restore session context
npx claude-flow hooks session-restore --session-id "launch-${LAUNCH_ID}"

# Retrieve prior phase outputs
if [ "$PHASE" -gt 1 ]; then
  PREV_PHASE=$((PHASE - 1))
  npx claude-flow memory retrieve --pattern "product-launch/${LAUNCH_ID}/phase-${PREV_PHASE}/*"
fi

# Execute phase-specific workflow
case $PHASE in
  1)
    echo "🔬 Executing Phase 1: Research & Planning"
    npx claude-flow task orchestrate --strategy sequential --task "market-research"
    ;;
  2)
    echo "⚙️ Executing Phase 2: Product Development"
    npx claude-flow task orchestrate --strategy parallel --max-agents 6
    ;;
  3)
    echo "📢 Executing Phase 3: Marketing & Sales Prep"
    npx claude-flow task orchestrate --strategy parallel --max-agents 4
    ;;
  4)
    echo "🚀 Executing Phase 4: Launch Execution"
    npx claude-flow task orchestrate --strategy sequential --priority critical
    ;;
  5)
    echo "📊 Executing Phase 5: Post-Launch Monitoring"
    npx claude-flow task orchestrate --strategy adaptive
    ;;
esac

# Store phase completion
npx claude-flow hooks post-task --task-id "phase-${PHASE}-complete"
```

### Post-Workflow Summary

```bash
#!/bin/bash
# Generate launch summary report

LAUNCH_ID="$1"

# Retrieve all phase data
npx claude-flow memory retrieve --pattern "product-launch/${LAUNCH_ID}/*" > "/tmp/${LAUNCH_ID}-data.json"

# Generate summary
npx claude-flow hooks post-task --task-id "launch-${LAUNCH_ID}" --export-metrics true

# Export workflow for future reference
npx claude-flow hooks session-end --export-workflow "/tmp/${LAUNCH_ID}-workflow.json"

echo "✅ Product launch complete: ${LAUNCH_ID}"
echo "📊 Summary report: /tmp/${LAUNCH_ID}-data.json"
echo "📈 Workflow export: /tmp/${LAUNCH_ID}-workflow.json"
```

---

## Success Metrics

### Technical Metrics (Phase 2 & 4)
- **Uptime**: 99.9%+ during launch week
- **API Response Time**: < 200ms (p95)
- **Page Load Time**: < 2 seconds
- **Error Rate**: < 0.1%
- **Test Coverage**: > 90%
- **Mobile App Ratings**: > 4.0 stars

### Business Metrics (Phase 5)
- **User Signups**: Target defined in Phase 1 strategy
- **Activation Rate**: > 40% (activated within 7 days)
- **Conversion Rate**: > 2.5% (free to paid)
- **Customer Acquisition Cost (CAC)**: Within budget
- **Monthly Recurring Revenue (MRR)**: Target growth trajectory
- **Churn Rate**: < 5% monthly
- **Net Promoter Score (NPS)**: > 50

### Marketing Metrics (Phase 3 & 4)
- **Campaign ROI**: > 3:1 across all channels
- **Email Open Rate**: > 25%
- **Social Engagement**: > 5% (likes, comments, shares)
- **Paid Ad CTR**: > 2%
- **Organic Traffic Growth**: > 20% month-over-month
- **Press Coverage**: 5+ publications

### Support Metrics (Phase 5)
- **First Response Time**: < 2 hours
- **Resolution Time**: < 24 hours
- **Customer Satisfaction (CSAT)**: > 4.5/5
- **Self-Service Rate**: > 60% (resolved without ticket)
- **Ticket Volume**: Declining trend

---

## Usage Examples

### Example 1: SaaS Product Launch

```bash
# Initialize launch
PRODUCT="TaskFlow AI"
LAUNCH_ID="taskflow-ai-20250101"

# Phase 1: Market Research (Week 1-2)
npx claude-flow agent spawn --type researcher
# Output: Market size $2B TAM, 50k potential customers identified

# Phase 2: Development (Week 3-8)
npx claude-flow swarm init --topology mesh --max-agents 6
# Output: Web app + mobile apps + API complete with 93% test coverage

# Phase 3: Marketing (Week 5-9)
npx claude-flow task orchestrate --strategy parallel
# Output: Campaign across 5 channels, 100+ content pieces created

# Phase 4: Launch (Week 10)
npx claude-flow workflow execute --workflow-id "prod-deploy-${LAUNCH_ID}"
# Output: Deployed successfully, 1,000 signups in first week

# Phase 5: Optimization (Week 11+)
npx claude-flow hooks session-restore --session-id "launch-${LAUNCH_ID}"
# Output: Weekly reports, 15% improvement in conversion rate
```

### Example 2: Mobile App Launch

```bash
# Focus on mobile-first approach
LAUNCH_ID="fitness-tracker-20250201"

# Phase 2: Prioritize mobile development
npx claude-flow agent spawn --type mobile-dev --priority high
npx claude-flow agent spawn --type backend-dev --priority high
# Output: React Native app (iOS + Android) with offline-first architecture

# Phase 3: App store optimization
npx claude-flow agent spawn --type seo-specialist --focus "app-store-optimization"
# Output: ASO strategy, 50+ keywords, compelling app store listings

# Phase 4: Soft launch to beta users
npx claude-flow workflow execute --workflow-id "beta-deploy-${LAUNCH_ID}"
# Output: 500 beta users, 4.8 star rating, feedback incorporated
```

### Example 3: Enterprise B2B Launch

```bash
# Enterprise focus with sales-led approach
LAUNCH_ID="enterprise-analytics-20250301"

# Phase 1: Enterprise market research
npx claude-flow agent spawn --type researcher --focus "enterprise-b2b"
# Output: Target 500 enterprise accounts, decision-maker personas

# Phase 3: Sales enablement priority
npx claude-flow agent spawn --type sales-specialist --priority critical
# Output: Enterprise sales playbook, ROI calculator, case studies

# Phase 4: Account-based marketing launch
npx claude-flow task orchestrate --strategy "account-based-marketing"
# Output: 50 target accounts engaged, 10 pilot customers secured
```

---

## GraphViz Process Diagram

See `when-releasing-new-product-orchestrate-product-launch-process.dot` for visual workflow representation showing:
- 5 phases with sequential and parallel execution patterns
- 15+ agent interactions and data flows
- Memory coordination points between phases
- Decision gates and validation checkpoints
- Optimization loops in Phase 5

---

## Quality Checklist

Before considering launch complete, verify:

- [ ] **Phase 1**: Market validated, strategy approved, business case solid
- [ ] **Phase 2**: All applications deployed, tests passing, security audited
- [ ] **Phase 3**: Marketing campaigns ready, sales team trained, support operational
- [ ] **Phase 4**: Production stable, first customers acquired, monitoring active
- [ ] **Phase 5**: Metrics tracking positively, optimization loops running

**All phase deliverables stored in memory following namespace convention**:
- [ ] `product-launch/${LAUNCH_ID}/phase-1/*` - Research and strategy
- [ ] `product-launch/${LAUNCH_ID}/phase-2/*` - Development artifacts
- [ ] `product-launch/${LAUNCH_ID}/phase-3/*` - Marketing materials
- [ ] `product-launch/${LAUNCH_ID}/phase-4/*` - Launch metrics
- [ ] `product-launch/${LAUNCH_ID}/phase-5/*` - Weekly reports

---

**Workflow Complexity**: High (15+ agents, 10 weeks, 5 phases)
**Coordination Pattern**: Hierarchical with adaptive parallel execution
**Memory Footprint**: ~50-100 memory entries per launch
**Typical Use Case**: Major product launches requiring comprehensive coordination
