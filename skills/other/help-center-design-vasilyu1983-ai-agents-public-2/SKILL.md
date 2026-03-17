---
name: help-center-design
description: Design or audit AI-first help centers/knowledge bases/FAQs, including taxonomy, article templates, analytics, and AI support (RAG, chatbot, escalation), using 2025-2026 best practices
---

# Help Center Design

Design AI-first help centers, knowledge bases, FAQs, and learning materials.

This skill reflects the shift from static help portals to AI-powered, embedded, personalized self-service systems.

## Workflow (Use As Default Order)

1. Define scope and constraints
   - Audience/personas, product area(s), product versioning, channels (web/in-app), compliance requirements, localization needs.
2. Inventory current knowledge
   - Top tickets, top searches, top articles, top escalation reasons, and known content owners.
3. Build information architecture
   - Category structure, tagging, navigation, URL strategy, and internal linking.
4. Standardize content
   - Article types, templates, AI-friendly writing rules, and visual standards.
5. Instrument and measure
   - KPIs, event tracking, dashboards, and search query logging.
6. Add AI support safely
   - Retrieval-first answers, citations, confidence thresholds, escalation rules, and transactional guardrails.
7. Run knowledge operations
   - Governance, freshness detection, release-driven updates, and continuous optimization.

Expected outputs (adapt to request):
- Help center taxonomy map + tag schema
- Top 20 article backlog (by impact) + templates
- Analytics spec (events + dashboard KPIs)
- AI support spec (RAG sources, escalation thresholds, safety rules)
- Operating cadence (owners + review schedule)

## Quick Reference

### Content Type Decision Matrix

| User Need | Content Type | Format | AI Role |
|-----------|--------------|--------|---------|
| "How do I..." | How-To | Step-by-step | Suggest next steps |
| "Why isn't..." | Troubleshooting | Problem -> Cause -> Fix | Diagnose & resolve |
| "What is..." | Conceptual | Explanation | Summarize context |
| "Quick answer" | FAQ | Q&A pairs | Instant response |
| "Full specs" | Reference | Tables, lists | Search & retrieve |
| "Learn feature" | Tutorial | Video + interactive | Personalized path |

### Platform Selection (Verify Pricing And Plan Limits)

| Company Stage | Platform | Monthly Cost | Best For |
|---------------|----------|--------------|----------|
| Enterprise | Zendesk | $55+/agent | Complex workflows, compliance |
| Growth/SaaS | Intercom | $29/seat + $0.99/resolution | Conversational, PLG |
| SMB/Startup | Freshdesk | $29-69/agent | Budget-friendly, native AI |
| Developer-focused | GitBook/Notion | $0-20/user | Docs-as-code |

See [references/platform-guides.md](references/platform-guides.md) for setup/migration notes and [data/sources.json](data/sources.json) for curated comparison sources.

## 2025-2026 Best Practices

### Key Shifts

| Aspect | Traditional (Pre-2024) | Modern (2025-2026) |
|--------|------------------------|---------------------|
| Support model | Separate help portal | Embedded in-app help |
| AI role | Search assistant | Higher automation with safe escalation |
| Search | Keyword matching | Semantic + RAG |
| Content | Text-heavy articles | Visual-first (video, GIF, screenshots) |
| Personalization | Same for all users | By role, version, behavior |
| Maintenance | Manual curation | AI-driven freshness detection |
| Navigation | Category browsing | Conversational + contextual |

Avoid quoting hard statistics without verification; refresh trends and benchmarks via [data/sources.json](data/sources.json) when needed.

### AI-First Principles

1. **Agentic Resolution** — AI executes tasks (refunds, bookings, updates), not just answers
2. **Semantic Understanding** — Intent-based search, not keyword matching
3. **Proactive Assistance** — Surface help before users ask
4. **Content Freshness** — Auto-detect stale content, suggest updates
5. **Multi-Source Synthesis** — Pull from docs, tickets, Slack, release notes
6. **Memory-Rich AI** — Retain context across sessions for personalized support

### Emerging Trends (2026)

| Trend | Description | Impact |
|-------|-------------|--------|
| **Voice Search** | Users speak instead of type to find information | Requires natural language KB content |
| **Proactive AI** | AI detects/resolves issues before users report | Reduces inbound support volume |
| **Embedded Help** | Help surfaces in-context, not separate portal | Higher engagement, lower friction |
| **AI Operations Lead** | New role supervising AI agent behavior | Shift from execution to oversight |
| **Hallucination Mitigation** | RAG grounding to reduce AI fabrication | Requires citation/source linking |

## Help Center Architecture

### Category Structure Rules

```
HIERARCHY LIMITS
- Maximum depth: 2-3 levels
- Top-level categories: 5-9 (cognitive load principle)
- Articles per category: 10-20 (scannable)
- Avoid: Deep nesting, internal org structure
```

### Recommended Top-Level Categories

```
STANDARD CATEGORIES (adapt to product)
1. Getting Started        — First-run, setup, quick wins
2. [Core Feature 1]       — Primary use case
3. [Core Feature 2]       — Secondary use case
4. Account & Billing      — Settings, payments, security
5. Integrations           — Third-party connections
6. Troubleshooting        — Common issues, error codes
7. API & Developers       — Technical documentation
8. What's New             — Changelog, releases
```

### Navigation Patterns

- **Breadcrumbs** — Always show location in hierarchy
- **Related Articles** — 3-5 contextually relevant links
- **Next Steps** — Guide to logical next action
- **Search Prominence** — Above fold, always visible
- **Popular Articles** — Surface high-traffic content

## Article Types (Keep The Set Small)

- How-To: task completion, 3-10 steps
- Troubleshooting: symptoms -> causes -> solutions
- FAQ: fast answers with links to deeper docs
- Conceptual: explain terms and mental models
- Reference: precise specs (tables, limits, error codes)

Use the copy-paste templates in [references/article-templates.md](references/article-templates.md).

## AI Integration Patterns

### Chatbot Architecture

```
MODERN AI SUPPORT FLOW (2025)

User query
  -> Intent detection (semantic understanding)
  -> RAG retrieval (KB + tickets + docs)
  -> Response and action (answer and/or execute task)
  -> Escalation check (confidence below threshold?)
  -> Human agent (if needed)
```

### Agentic AI Capabilities (2025-2026)

| Capability | Example | Platform |
|------------|---------|----------|
| Task execution | Process refund | Ada, Zendesk AI |
| Appointment booking | Schedule call | Chatbase, Calendly |
| Account updates | Change plan | Fin AI, custom |
| Ticket creation | Escalate to human | All platforms |
| Multi-system lookup | Check order + shipping | MCP integrations |

### Content for AI Consumption

```markdown
AI-FRIENDLY WRITING RULES

DO:
- Clear headings with keywords
- Structured data (tables, lists)
- Explicit step numbering
- Error messages verbatim
- Unique article titles

DON'T:
- Ambiguous pronouns
- Implicit assumptions
- Marketing fluff in support content
- Duplicate content across articles
```

See [references/ai-integration.md](references/ai-integration.md) for RAG setup, evaluation, and escalation patterns.

## Metrics & KPIs

### Core Metrics

| Metric | Definition | Benchmark |
|--------|------------|-----------|
| **Self-Service Rate** | % issues resolved without agent | 60-80% |
| **Deflection Rate** | Tickets avoided via KB | 30-50% |
| **Search Success** | % searches -> helpful result | >70% |
| **CSAT (KB)** | Article helpfulness rating | >80% positive |
| **Time to Resolution** | Self-service completion time | <3 min |
| **Zero-Result Rate** | Searches with no results | <5% |

### Content Health Metrics

```
FRESHNESS INDICATORS
- Last updated > 6 months -> Review required
- Last updated > 12 months -> Likely stale
- No views in 90 days -> Consider archive
- High bounce rate -> Content mismatch

QUALITY INDICATORS
- Thumbs down > 20% -> Rewrite needed
- Escalation after viewing -> Content gap
- Search -> immediate exit -> Title mismatch
```

### ROI Calculation

```
SELF-SERVICE ROI FORMULA

Monthly Savings = (Deflected Tickets x $13) - Platform Cost

Example:
- 1,000 deflected tickets/month
- $13 average agent cost
- $500 platform cost
- ROI = ($13,000 - $500) = $12,500/month
```

See [references/metrics-optimization.md](references/metrics-optimization.md) for instrumentation, dashboards, and optimization playbooks.

## Learning & Onboarding

### In-App Help Patterns

| Pattern | Use Case | Tools |
|---------|----------|-------|
| Tooltips | Field-level guidance | Native, Appcues |
| Hotspots | Feature discovery | UserPilot, Pendo |
| Checklists | Onboarding progress | Whatfix, Chameleon |
| Tours | New feature intro | Intercom, Appcues |
| Contextual Help | Error recovery | Custom, Zendesk |

### Tutorial Best Practices (2025)

```
VIDEO TUTORIALS
- Length: 2-4 minutes (40% higher completion)
- Format: Screen recording + voiceover
- Chapters: Clickable sections
- Captions: Always include (accessibility)

INTERACTIVE GUIDES
- Click-through walkthroughs
- Sandbox environments
- Progress saving
- Skip option for experienced users
```

See [references/learning-paths.md](references/learning-paths.md) for onboarding sequence design, accessibility, and measurement.

## Knowledge Operations (2026)

Operate the help center like a product:
- Assign owners per category and per top article; define review cadence and SLAs for updates.
- Use release notes, incident reports, and ticket trends as automatic triggers for content updates.
- Use freshness signals (search exits, escalation after article view, downvotes) to prioritize rewrites.

See [references/knowledge-ops.md](references/knowledge-ops.md) for governance, workflows, and checklists.

## Implementation Checklist

### Phase 1: Foundation (Week 1-2)

REQUIRED:
- Choose platform (Zendesk/Intercom/Freshdesk)
- Define category structure (5-9 top-level)
- Create article templates for each type
- Set up analytics tracking
- Configure search settings

### Phase 2: Content (Week 3-4)

REQUIRED:
- Audit existing documentation
- Migrate/rewrite top 20 articles
- Add visual content (screenshots, GIFs)
- Implement internal linking
- Set up redirects from old URLs

### Phase 3: AI Integration (Week 5-6)

REQUIRED:
- Enable AI chatbot
- Configure RAG/semantic search
- Set escalation thresholds
- Test common queries
- Monitor resolution rates

### Phase 4: Optimization (Ongoing)

REQUIRED:
- Review zero-result searches weekly
- Update stale content monthly
- A/B test article titles
- Analyze escalation patterns
- Expand based on ticket trends

## Resources

| Resource | Content |
|----------|---------|
| [article-templates.md](references/article-templates.md) | Complete templates for all 5 article types |
| [taxonomy-patterns.md](references/taxonomy-patterns.md) | Category structures, tagging, search optimization |
| [ai-integration.md](references/ai-integration.md) | RAG setup, chatbot config, platform integrations |
| [platform-guides.md](references/platform-guides.md) | Zendesk, Intercom, Freshdesk, GitBook setup |
| [learning-paths.md](references/learning-paths.md) | Onboarding sequences, tutorial design, courses |
| [metrics-optimization.md](references/metrics-optimization.md) | KPI tracking, analytics, A/B testing |
| [knowledge-ops.md](references/knowledge-ops.md) | Governance, workflows, and operating cadence |
| [sources.json](data/sources.json) | Curated sources with `add_as_web_search` flags |

## Trend Awareness Protocol

REQUIRED: When users ask recommendation questions about help centers, knowledge bases, or support platforms, run a quick web search to confirm current trends before answering. Prefer sources flagged `add_as_web_search: true` in [data/sources.json](data/sources.json), plus official docs for any platform you recommend.

### Trigger Conditions

- "What's the best help center platform?"
- "What should I use for [knowledge base/FAQ/support]?"
- "What's the latest in customer self-service?"
- "Current best practices for [AI support/chatbots]?"
- "Is [Zendesk/Intercom/Freshdesk] still relevant in 2026?"
- "[Zendesk] vs [Intercom] vs [other]?"
- "Best AI chatbot for customer support?"

### Required Searches

1. Search: `"help center best practices 2026"`
2. Search: `"[specific platform] vs alternatives 2026"`
3. Search: `"AI customer support trends January 2026"`
4. Search: `"knowledge base platforms 2026"`

### What to Report

After searching, provide:

- **Current landscape**: What support platforms/tools are popular NOW
- **Emerging trends**: New AI capabilities, patterns, or platforms gaining traction
- **Deprecated/declining**: Approaches or tools losing relevance
- **Recommendation**: Based on fresh data, not just static knowledge

If web search is unavailable, state that constraint and proceed with best-effort static guidance.

### Example Topics (verify with fresh search)

- Help center platforms (Zendesk, Intercom, Freshdesk)
- AI support agents (Fin AI, Ada, Forethought)
- Knowledge base tools (Document360, GitBook, Notion)
- In-app guidance (UserPilot, Pendo, Chameleon)
- Self-service AI capabilities and resolution rates
- Semantic search and RAG for support
