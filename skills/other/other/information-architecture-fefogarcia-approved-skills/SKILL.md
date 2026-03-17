---
name: information-architecture
description: Use when organizing content for digital products, designing navigation systems, restructuring information hierarchies, improving findability, creating taxonomies or metadata schemas, or when users mention information architecture, IA, sitemap, navigation design, content structure, card sorting, tree testing, taxonomy, findability, or need help making information discoverable and usable.
---

# Information Architecture

## Purpose

Information architecture (IA) is the practice of organizing, structuring, and labeling content to help users find and manage information effectively. Good IA makes complex information navigable, discoverable, and understandable.

Use this skill when:
- **Designing navigation** for websites, apps, documentation, or knowledge bases
- **Restructuring content** that users can't find or understand
- **Creating taxonomies** for classification, tagging, or metadata
- **Organizing information** at scale (hundreds or thousands of items)
- **Improving findability** when search and browse both fail
- **Designing mental models** that match how users think about content

Information architecture bridges user mental models and system structure. The goal: users can predict where information lives and find it quickly.

---

## Common Patterns

### Pattern 1: Content Audit → Card Sort → Sitemap

**When**: Redesigning existing site/app with lots of content

**Process**:
1. **Content audit**: Inventory all existing content (URLs, titles, metadata)
2. **Card sorting**: Users group content cards into categories
3. **Analyze patterns**: What categories emerge? What's grouped together?
4. **Create sitemap**: Translate patterns into hierarchical structure
5. **Validate with tree testing**: Can users find content in new structure?

**Example**: E-commerce site with 500 products. Audit products → Card sort with 15 users → Patterns show users group by "occasion" not "product type" → New navigation: "Daily Essentials", "Special Occasions", "Gifts" instead of "Electronics", "Clothing", "Home Goods"

### Pattern 2: Taxonomy Design (Faceted Navigation)

**When**: Users need multiple ways to slice/filter information

**Structure**: Orthogonal facets (dimensions) that combine
- **Facet 1**: Category (e.g., "Shoes", "Shirts", "Pants")
- **Facet 2**: Brand (e.g., "Nike", "Adidas", "Puma")
- **Facet 3**: Price range (e.g., "$0-50", "$50-100", "$100+")
- **Facet 4**: Color, Size, etc.

**Principle**: Facets are independent. Users can filter by any combination.

**Example**: Amazon product browse. Filter by Category AND Brand AND Price simultaneously. Each facet narrows results without breaking others.

### Pattern 3: Progressive Disclosure (Hub-and-Spoke)

**When**: Content hierarchy is deep, users need overview before details

**Structure**:
- **Hub page**: High-level overview with clear labels
- **Spoke pages**: Detailed content, linked from hub
- **Breadcrumbs**: Show path back to hub

**Principle**: Don't overwhelm with everything at once. Start simple, reveal complexity on-demand.

**Example**: Documentation site. Hub: "Getting Started" with 5 clear options (Install, Configure, First App, Tutorials, Troubleshooting). Each option links to detailed spoke. Users scan hub, pick entry point, dive deep, return to hub if stuck.

### Pattern 4: Flat vs. Deep Navigation

**When**: Deciding navigation depth (breadth vs. depth tradeoff)

**Flat navigation** (broad, shallow):
- **Structure**: Many top-level categories, few sub-levels (e.g., 10 categories, 2 levels deep)
- **Pros**: Less clicking, everything visible
- **Cons**: Overwhelming choice, hard to scan 10+ options

**Deep navigation** (narrow, tall):
- **Structure**: Few top-level categories, many sub-levels (e.g., 5 categories, 5 levels deep)
- **Pros**: Manageable choices at each level (5-7 items)
- **Cons**: Many clicks to reach content, users get lost in depth

**Optimal**: **3-4 levels deep, 5-9 items per level** (Hick's Law: more choices = longer decision time)

**Example**: Software docs. Flat: All 50 API methods visible at once (overwhelming). Deep: APIs → Authentication → Methods → JWT → jwt.sign() (5 clicks, frustrating). Optimal: APIs (8 categories) → Authentication (6 methods) → jwt.sign() (3 clicks).

### Pattern 5: Mental Model Alignment (Card Sorting)

**When**: You don't know how users think about content

**Process**:
1. **Open card sort**: Users create their own categories (exploratory)
2. **Closed card sort**: Users fit content into your categories (validation)
3. **Hybrid card sort**: Users use your categories OR create new ones (refinement)
4. **Analyze**: What labels do users use? What groupings emerge? What's confusing?

**Example**: SaaS product features. Company calls them "Widgets", "Modules", "Components" (technical terms). Card sort reveals users think "Reports", "Dashboards", "Alerts" (task-based terms). **Insight**: Label by user tasks, not internal architecture.

### Pattern 6: Tree Testing (Reverse Card Sort)

**When**: Validating navigation structure before building

**Process**:
1. **Create text-based tree** (sitemap without visuals)
2. **Give users tasks**: "Where would you find X?"
3. **Track paths**: What route did they take? Did they succeed?
4. **Measure**: Success rate, directness (fewest clicks), time

**Example**: Navigation tree with "Services → Web Development → E-commerce". Task: "Find information about building an online store". 80% success = good. 40% success = users don't understand "E-commerce" label or "Services" category. Iterate.

---

## Workflow

Use this structured approach when designing or auditing information architecture:

```
□ Step 1: Understand context and users
□ Step 2: Audit existing content (if any)
□ Step 3: Conduct user research (card sorting, interviews)
□ Step 4: Design taxonomy and navigation
□ Step 5: Create sitemap and wireframes
□ Step 6: Validate with tree testing
□ Step 7: Implement and iterate
□ Step 8: Monitor findability metrics
```

**Step 1: Understand context and users** ([details](#1-understand-context-and-users))
Identify content volume, user goals, mental models, and success metrics (time to find, search queries, bounce rate).

**Step 2: Audit existing content** ([details](#2-audit-existing-content))
Inventory all content (URLs, titles, metadata). Identify duplicates, gaps, outdated items. Measure current performance (analytics, heatmaps).

**Step 3: Conduct user research** ([details](#3-conduct-user-research))
Run card sorting (open, closed, or hybrid) with 15-30 users. Analyze clustering patterns, category labels, outliers. Conduct user interviews to understand mental models.

**Step 4: Design taxonomy and navigation** ([details](#4-design-taxonomy-and-navigation))
Create hierarchical structure (3-4 levels, 5-9 items per level). Design facets for filtering. Choose labeling system (task-based, audience-based, or alphabetical). Define metadata schema.

**Step 5: Create sitemap and wireframes** ([details](#5-create-sitemap-and-wireframes))
Document structure visually (sitemap diagram). Create low-fidelity wireframes showing navigation, breadcrumbs, filters. Get stakeholder feedback.

**Step 6: Validate with tree testing** ([details](#6-validate-with-tree-testing))
Test navigation with text-based tree (no visuals). Measure success rate (≥70%), directness (≤1.5× optimal path), time. Identify problem areas, iterate.

**Step 7: Implement and iterate** ([details](#7-implement-and-iterate))
Build high-fidelity designs and implement. Launch incrementally (pilot → rollout). Gather feedback from real users.

**Step 8: Monitor findability metrics** ([details](#8-monitor-findability-metrics))
Track time to find, search success rate, navigation abandonment, bounce rate, user feedback. Refine taxonomy based on data.

---

## Critical Guardrails

### 1. Test with Real Users, Not Assumptions

**Danger**: Designing based on stakeholder opinions or personal preferences

**Guardrail**: Always validate with user research (card sorting, tree testing, usability testing). Minimum 15 participants for statistical significance.

**Red flag**: "I think users will understand 'Synergistic Solutions'..." — If you're guessing, you're wrong.

### 2. Avoid Org Chart Navigation

**Danger**: Structuring navigation by internal org structure (Sales, Marketing, Engineering)

**Guardrail**: Structure by user mental models and tasks, not company departments

**Example**: Bad: "About Us → Departments → Engineering → APIs". Good: "For Developers → APIs"

### 3. Keep Navigation Shallow (3-4 Levels Max)

**Danger**: Deep hierarchies (5+ levels) where users get lost

**Guardrail**: Aim for 3-4 levels deep, 5-9 items per level. If deeper needed, add search, filtering, or multiple entry points.

**Rule of thumb**: If users need >4 clicks from homepage to content, rethink structure.

### 4. Use Clear, Specific Labels (Not Jargon)

**Danger**: Vague labels ("Resources", "Solutions") or internal jargon ("SKU Management")

**Guardrail**: Labels must be specific, action-oriented, and match user vocabulary. Test labels in card sorts and tree tests.

**Test**: Could a new user predict what's under this label? If not, clarify.

### 5. Ensure Single, Predictable Location

**Danger**: Content lives in multiple places, or users can't predict location

**Guardrail**: Each content type should have ONE canonical location. If cross-category, use clear primary location + links from secondary.

**Principle**: "Principle of least astonishment" — content is where users expect it.

### 6. Design for Scale

**Danger**: Structure works for 50 items but breaks at 500

**Guardrail**: Think ahead. If you have 50 products now but expect 500, design faceted navigation from start. Don't force retrofitting later.

**Test**: What happens if this category grows 10×? Will structure still work?

### 7. Provide Multiple Access Paths

**Danger**: Only one way to find content (e.g., only browse, no search)

**Guardrail**: Offer browse (navigation), search, filters, related links, breadcrumbs, tags. Different users have different strategies.

**Principle**: Some users are "searchers" (know what they want), others are "browsers" (exploring). Support both.

### 8. Validate Before Building

**Danger**: Building full site/app before testing structure

**Guardrail**: Use tree testing (text-based navigation) to validate structure before expensive design/dev work

**ROI**: 1 day of tree testing saves weeks of rework after launch.

---

## Quick Reference

### IA Methods Comparison

| Method | When to Use | Participants | Deliverable |
|--------|-------------|--------------|-------------|
| **Open card sort** | Exploratory, unknown categories | 15-30 users | Category labels, groupings |
| **Closed card sort** | Validation of existing categories | 15-30 users | Fit quality, confusion points |
| **Tree testing** | Validate navigation structure | 20-50 users | Success rate, directness, problem areas |
| **Content audit** | Understand existing content | 1-2 analysts | Inventory spreadsheet, gaps, duplicates |
| **User interviews** | Understand mental models | 5-10 users | Mental model diagrams, quotes |

### Navigation Depth Guidelines

| Content Size | Recommended Structure | Example |
|--------------|----------------------|---------|
| <50 items | Flat (1-2 levels) | Blog, small product catalog |
| 50-500 items | Moderate (2-3 levels) | Documentation, medium e-commerce |
| 500-5000 items | Deep with facets (3-4 levels + filters) | Large e-commerce, knowledge base |
| 5000+ items | Hybrid (browse + search + facets) | Amazon, Wikipedia |

### Labeling Systems

| System | When to Use | Example |
|--------|-------------|---------|
| **Task-based** | Users have clear goals | "Book a Flight", "Track Order", "Pay Invoice" |
| **Audience-based** | Different user types | "For Students", "For Teachers", "For Parents" |
| **Topic-based** | Reference/learning content | "History", "Science", "Mathematics" |
| **Format-based** | Media libraries | "Videos", "PDFs", "Podcasts" |
| **Alphabetical** | No clear grouping, lookup-heavy | "A-Z Directory", "Glossary" |

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Tree test success rate** | ≥70% | Users find correct destination |
| **Directness** | ≤1.5× optimal path | Clicks taken / optimal clicks |
| **Time to find** | <30 sec (simple), <2 min (complex) | Task completion time |
| **Search success** | ≥60% find without search | % completing task without search |
| **Bounce rate** | <40% | % leaving immediately from landing page |

---

## Resources

### Navigation to Resources

- [**Templates**](resources/template.md): Content audit template, card sorting template, sitemap template, tree testing script
- [**Methodology**](resources/methodology.md): Card sorting analysis, taxonomy design, navigation patterns, findability optimization
- [**Rubric**](resources/evaluators/rubric_information_architecture.json): Evaluation criteria for IA quality (10 criteria)

### Related Skills

- **data-schema-knowledge-modeling**: For database schema and knowledge graphs
- **mapping-visualization-scaffolds**: For visualizing information structure
- **discovery-interviews-surveys**: For user research methods
- **evaluation-rubrics**: For creating IA evaluation criteria
- **communication-storytelling**: For explaining IA decisions to stakeholders

---

## Examples in Context

### Example 1: E-commerce Navigation Redesign

**Context**: Bookstore with 10,000 books organized by publisher (internal logic)

**Approach**: Content audit → Open card sort (20 users: genre-based, not publisher) → Faceted navigation: Genre × Format × Price × Rating → Tree test (75% success) → **Result**: Time to find -40%, conversion +15%

### Example 2: SaaS Documentation IA

**Context**: Developer docs, high abandonment after 2 pages

**Approach**: User interviews (mental model = tasks not features) → Taxonomy shift: feature-based to task-based ("Get Started", "Store Data") → Progressive disclosure (hub-and-spoke) → Tree test (68% → 82% success) → **Result**: Engagement +50%, support tickets -25%

### Example 3: Internal Knowledge Base

**Context**: Company wiki with 2,000 articles, employees can't find policies

**Approach**: Content audit (40% outdated, 15% duplicates) → Closed card sort (25 employees) → Hybrid: browse (known needs) + search (unknown) + metadata schema → Search best bets → **Result**: Search success 45% → 72%, time to find 5min → 1.5min
