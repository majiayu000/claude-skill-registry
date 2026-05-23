---
name: create-brownfield-prd
description: Generate Product Requirements Documents (PRD) for existing systems through systematic codebase analysis, feature extraction, and gap identification with confidence scoring for validation-needed areas. Use when documenting existing systems that lack requirements documentation or preparing for system modernization/migration.
acceptance:
  - prd_generated: "Brownfield PRD document created documenting current state"
  - features_extracted: "All major features identified and categorized (core/secondary/legacy)"
  - confidence_scored: "All extracted information includes confidence scores (High/Medium/Low)"
  - gaps_identified: "Known limitations, technical debt, and gaps documented"
  - modernization_roadmap: "Modernization opportunities and priorities identified"
inputs:
  project_root:
    type: string
    required: true
    description: "Absolute path to project root directory"
  existing_docs:
    type: string
    required: false
    description: "Path to existing documentation (README, wikis, etc.)"
  business_context:
    type: string
    required: false
    description: "Business context, target users, and objectives (if known)"
  tech_stack:
    type: string
    required: false
    description: "Known technology stack information"
  analysis_depth:
    type: string
    required: false
    description: "quick | standard | comprehensive (default: standard)"
    default: "standard"
outputs:
  prd_created:
    type: boolean
    description: "Whether brownfield PRD was successfully created"
  prd_location:
    type: string
    description: "File path to created PRD (docs/brownfield-prd.md)"
  feature_count:
    type: number
    description: "Number of features identified and documented"
  confidence_score:
    type: number
    description: "Overall confidence in analysis (0-100, weighted average)"
  validation_needed:
    type: array
    description: "List of areas requiring human validation"
telemetry:
  emit: "skill.create-brownfield-prd.completed"
  track:
    - project_root
    - analysis_depth
    - feature_count
    - confidence_score
    - validation_items_count
    - duration_ms
    - prd_location
---

# Create Brownfield PRD Skill

## Purpose

Generate Product Requirements Documents (PRD) for existing systems by analyzing codebases, extracting features, reconstructing user flows, and identifying modernization opportunities. Unlike greenfield PRDs (starting from scratch), brownfield PRDs document what exists today and plan evolution paths.

**Core Principles:**
- Evidence-based analysis (code is source of truth)
- Confidence scoring (highlight areas needing validation)
- Feature categorization (core/secondary/legacy)
- Gap identification (what's missing, what's broken)
- Modernization roadmap (prioritized improvements)

## Prerequisites

- Access to project codebase (read permissions)
- `document-project` skill available for architecture analysis
- Basic understanding of project's domain/purpose
- workspace/ directory exists for PRD storage

---

## Workflow

### Step 1: Codebase Analysis

**Action:** Analyze project structure, architecture, and technical implementation using systematic discovery.

**Key Activities:**

1. **Use document-project Skill**
   ```bash
   # Leverage existing brownfield analysis skill
   @bmad Use document-project skill to analyze [project_root]
   ```

   Extract from document-project output:
   - Project structure and organization
   - Technology stack details
   - Architecture patterns used
   - Data models and entities
   - API endpoints and routes
   - Integration points
   - Configuration and environment

2. **Supplement with Targeted Analysis**
   - **Entry Points:** Identify how users access the system (web routes, CLI commands, API endpoints)
   - **Core Workflows:** Map main user flows from routes/controllers
   - **Data Models:** Extract entities and relationships from database schemas
   - **Business Logic:** Identify key algorithms, calculations, validations
   - **External Dependencies:** Document third-party services, APIs, integrations
   - **Configuration:** Identify feature flags, environment variables, settings

3. **Scan for Documentation**
   - README files
   - API documentation
   - Code comments and docstrings
   - Wiki or docs/ directory
   - CHANGELOG or release notes
   - Issue tracker (if accessible)

**Confidence Scoring:**
```
HIGH (90-100%): Clear code, good naming, documented
MEDIUM (60-89%): Understandable code, decent structure, some gaps
LOW (0-59%): Unclear code, poor naming, no documentation
```

**Example Analysis:**
```
PROJECT: E-commerce Platform (Node.js/React)

STRUCTURE (Confidence: HIGH):
- Backend: Express.js API (src/api/)
- Frontend: React SPA (src/client/)
- Database: PostgreSQL (9 tables identified)
- Clear separation of concerns

FEATURES IDENTIFIED (Preliminary):
1. User Authentication (routes: /api/auth/*)
2. Product Catalog (routes: /api/products/*)
3. Shopping Cart (routes: /api/cart/*)
4. Checkout Process (routes: /api/checkout/*)
5. Order Management (routes: /api/orders/*)

CONFIDENCE: 85% overall (good structure, decent naming)
VALIDATION NEEDED: Business rules (need to understand pricing, taxes, shipping logic)
```

**Output:** Comprehensive technical analysis with confidence scores

**See:** `references/codebase-analysis-guide.md` for detailed analysis techniques

---

### Step 2: Feature Extraction

**Action:** Transform technical components into user-facing features with categorization.

**Key Activities:**

1. **Map Code to Features**
   ```
   Routes/Endpoints → User Capabilities

   Example:
   /api/auth/login, /api/auth/signup → "User Authentication"
   /api/products GET → "Browse Products"
   /api/products/:id GET → "View Product Details"
   /api/cart POST → "Add to Cart"
   /api/checkout POST → "Complete Purchase"
   ```

2. **Categorize Features**
   - **Core (Business-Critical):** Essential to product value, frequently used
   - **Secondary (Important):** Valuable but not critical, moderately used
   - **Legacy (Deprecated/Unused):** Old features, low usage, technical debt

3. **Infer User Value**
   - What problem does each feature solve?
   - What user goal does it enable?
   - How does it contribute to overall product value?

4. **Estimate Usage Patterns**
   - Frequency indicators (from code):
     - Many routes/components → Likely core feature
     - Complex logic → Important business capability
     - Simple CRUD → Possibly secondary feature
     - Dead code/commented out → Legacy feature

5. **Document Feature Details**
   ```markdown
   ### Feature: User Authentication

   **Category:** Core
   **Confidence:** High (95%)
   **Description:** Users can create accounts, log in, and manage sessions

   **Technical Implementation:**
   - Routes: /api/auth/signup, /api/auth/login, /api/auth/logout
   - Authentication: JWT tokens (stored in httpOnly cookies)
   - Password hashing: bcrypt
   - Session management: Redis cache

   **User Capabilities:**
   - Sign up with email/password
   - Log in with credentials
   - Log out (invalidate session)
   - Password reset (inferred from /forgot-password route)

   **Validation Needed:**
   - OAuth/social login support? (no code found, may be planned)
   - Two-factor authentication? (no implementation found)
   ```

**Categorization Criteria:**

```
CORE FEATURES:
- Directly enables primary user goals
- Frequently accessed routes/components
- Complex business logic
- Multiple database tables involved
- Recent updates/commits (actively maintained)

SECONDARY FEATURES:
- Enhances but doesn't enable core value
- Moderate route/component complexity
- Support/utility functions
- Less frequent updates

LEGACY FEATURES:
- Commented-out code
- Old routes with no recent changes
- Feature flags marked deprecated
- TODO comments suggesting removal
- No test coverage
```

**Output:** Categorized feature list with confidence scores

**See:** `references/feature-extraction-patterns.md` for extraction strategies

---

### Step 3: User Flow Reconstruction

**Action:** Reconstruct end-to-end user journeys from code structure.

**Key Activities:**

1. **Map User Journeys from Routes**
   ```
   Journey: New Customer Purchase

   1. Browse Products
      Route: GET /products
      Page: ProductListPage.jsx

   2. View Product Details
      Route: GET /products/:id
      Page: ProductDetailPage.jsx

   3. Add to Cart
      Route: POST /cart
      Action: addToCart() in CartService

   4. Proceed to Checkout
      Route: GET /checkout
      Page: CheckoutPage.jsx

   5. Enter Shipping Info
      Form: ShippingForm.jsx
      API: POST /checkout/shipping

   6. Enter Payment
      Form: PaymentForm.jsx
      API: POST /checkout/payment
      Integration: Stripe.js

   7. Confirm Order
      Route: POST /orders
      Email: sendOrderConfirmation()
   ```

2. **Identify User Personas (Inferred)**
   ```
   Based on features and flows, infer user types:

   PERSONA 1: Customer (End User)
   - Features used: Browse, Purchase, Order History
   - Entry points: Homepage, Product pages
   - Goals: Find and buy products

   PERSONA 2: Admin (Staff)
   - Features used: Product Management, Order Management
   - Entry points: /admin dashboard
   - Goals: Manage catalog, fulfill orders
   ```

3. **Document Integration Points**
   ```
   EXTERNAL INTEGRATIONS:
   - Stripe (Payment Processing)
   - SendGrid (Transactional Emails)
   - AWS S3 (Product Images)
   - Google Analytics (Tracking)

   INTERNAL INTEGRATIONS:
   - PostgreSQL Database
   - Redis Cache (Sessions)
   - Background Jobs (Bull Queue)
   ```

4. **Identify Authentication/Authorization Flows**
   ```
   AUTHENTICATION:
   - Method: JWT tokens (httpOnly cookies)
   - Flow: Login → Token → Protected Routes

   AUTHORIZATION:
   - Roles: customer, admin
   - Permissions: Role-based access to admin routes
   ```

5. **Note Edge Cases and Error Handling**
   ```
   EDGE CASES FOUND:
   - Out of stock products (handled: show "Unavailable" message)
   - Invalid payment (handled: error message, no order created)
   - Duplicate cart items (handled: increment quantity)

   GAPS IN ERROR HANDLING:
   - Network timeouts (no retry logic found)
   - Race conditions (concurrent cart updates not handled)
   - Session expiration (unclear behavior, validation needed)
   ```

**Confidence Scoring for Flows:**
```
HIGH: Complete flow with clear steps, well-documented
MEDIUM: Flow identifiable but some gaps or unclear logic
LOW: Incomplete flow, significant inference required
```

**Output:** Reconstructed user journeys with confidence scores

**See:** `references/user-flow-reconstruction.md` for reconstruction techniques

---

### Step 4: PRD Generation

**Action:** Compile analysis into comprehensive brownfield PRD document.

**Document Structure:**

#### Section 1: Executive Summary
```markdown
## Executive Summary

**Product:** [Product Name] (Existing System)
**Analysis Date:** [Date]
**Codebase Version:** [Git commit, version, or "current"]
**Overall Confidence:** [X%] (High/Medium/Low)

### Current State Overview
[1-2 paragraphs: What the product does today, who uses it, core value proposition]

### Key Findings
- X core features identified and documented
- Y secondary features catalogued
- Z legacy features marked for deprecation
- [Confidence: HIGH/MEDIUM/LOW areas highlighted]

### Modernization Priorities
[Top 3-5 improvement opportunities ranked by impact]
```

#### Section 2: Product Overview (As-Is)
```markdown
## Product Overview

### What It Does
[Clear description of product functionality based on code analysis]

### Current Users (Inferred)
[User personas reconstructed from features and flows]

### Technology Stack
[Extracted from codebase: languages, frameworks, databases, tools]

### System Architecture
[High-level architecture diagram and description from document-project]
```

#### Section 3: Feature Inventory
```markdown
## Feature Inventory

### Core Features (Business-Critical)
[List of core features with descriptions, confidence scores, technical details]

### Secondary Features
[List of secondary features]

### Legacy Features (Deprecated/Unused)
[Features marked for potential removal]

### Feature Details Template:
**Feature Name:** [Name]
**Category:** Core | Secondary | Legacy
**Confidence:** [%] - High | Medium | Low
**Description:** [What it does]
**User Value:** [Why users care]
**Technical Implementation:** [How it works]
**Usage Indicators:** [Evidence of usage/importance]
**Validation Needed:** [Areas requiring confirmation]
```

#### Section 4: User Flows
```markdown
## User Flows (Reconstructed)

[Document key user journeys with confidence scores]

### Flow 1: [Flow Name]
**Confidence:** [%]
**Steps:** [Numbered steps]
**Validation Needed:** [Unclear areas]
```

#### Section 5: Known Limitations & Technical Debt
```markdown
## Known Limitations & Technical Debt

### Functional Gaps
[Features that should exist but don't]

### Technical Debt
[Code quality issues, outdated dependencies, architectural problems]

### Performance Issues
[Identified bottlenecks or scalability concerns]

### Security Concerns
[Potential security issues observed]

### UX Issues
[User experience problems inferred from code]
```

#### Section 6: Modernization Opportunities
```markdown
## Modernization Opportunities

### Priority 1 (High Impact, High Confidence)
[Improvements with clear value and high certainty]

### Priority 2 (High Impact, Medium Confidence)
[Improvements requiring validation]

### Priority 3 (Medium Impact)
[Nice-to-have improvements]

### Technology Upgrades
[Outdated dependencies, framework versions]

### Feature Enhancements
[Existing features that could be improved]

### New Feature Opportunities
[Gaps that could become new features]
```

#### Section 7: Integration Map
```markdown
## Integration Map

### External Integrations
[Third-party services, APIs, SaaS tools]

### Internal Systems
[Databases, caches, message queues, microservices]

### Data Flows
[How data moves through the system]
```

#### Section 8: Validation Checklist
```markdown
## Validation Checklist

Areas requiring stakeholder/user validation:

**High Priority Validation:**
- [ ] [Unclear business rule or logic]
- [ ] [Assumed user persona/workflow]
- [ ] [Inferred feature purpose]

**Medium Priority Validation:**
- [ ] [Secondary feature usage]
- [ ] [Edge case handling]

**Low Priority Validation:**
- [ ] [Legacy feature status]
- [ ] [Nice-to-have clarifications]
```

#### Section 9: Recommendations
```markdown
## Recommendations

### Immediate Actions (0-3 months)
[Quick wins, critical fixes]

### Medium-Term (3-6 months)
[Important improvements, technical debt paydown]

### Long-Term (6-12 months)
[Major refactors, new capabilities]

### Do Not Invest
[Legacy features to deprecate or remove]
```

**File Location:** `docs/brownfield-prd.md`

**Validation:** Document includes confidence scores throughout, validation checklist for low-confidence areas

**Output:** Complete brownfield PRD document

**See:** `references/brownfield-prd-template.md` for complete template with examples

---

## Common Scenarios

### Scenario 1: Well-Documented Codebase

**Context:** Good code structure, naming, and documentation

**Approach:**
- Analysis quick and confident (High confidence scores)
- Focus on gaps and modernization
- Less validation needed
- Can identify subtle improvements

**Example:** Modern SaaS app with TypeScript, good tests, clear structure

---

### Scenario 2: Legacy Monolith

**Context:** Old codebase, poor structure, minimal documentation

**Approach:**
- Careful inference required (Medium/Low confidence)
- Extensive validation checklist
- Focus on understanding before modernizing
- Document assumptions clearly

**Example:** 10-year-old PHP application with mixed patterns

---

### Scenario 3: Microservices Architecture

**Context:** Multiple repositories, distributed system

**Approach:**
- Analyze each service separately
- Document inter-service communication
- Map data flows across services
- Identify redundancy and gaps

**Example:** Node.js microservices with message queues

---

### Scenario 4: Partial Documentation Exists

**Context:** Some docs available (README, wikis) but incomplete

**Approach:**
- Cross-reference code with docs
- Highlight discrepancies (code vs docs)
- Update PRD based on code reality
- Note documentation debt

**Example:** Startup product with outdated README

---

## Best Practices

1. **Code is Source of Truth** - When docs and code conflict, trust the code
2. **Score Confidence Honestly** - Don't over-claim certainty; flag uncertain areas
3. **Categorize Ruthlessly** - Not everything is core; identify true priorities
4. **Document Assumptions** - Make inference process transparent
5. **Flag Validation Needs** - Create checklist for stakeholder confirmation
6. **Focus on User Value** - Translate technical features to user benefits
7. **Identify Quick Wins** - Highlight easy modernization opportunities
8. **Respect Legacy** - Old code often has good reasons; understand before judging

---

## Reference Files

- `references/codebase-analysis-guide.md` - Systematic code analysis techniques
- `references/feature-extraction-patterns.md` - Mapping code to user features
- `references/user-flow-reconstruction.md` - Reconstructing journeys from code
- `references/gap-analysis-framework.md` - Identifying limitations and opportunities
- `references/modernization-strategies.md` - Prioritizing improvements
- `references/confidence-scoring-guide.md` - Assigning and interpreting confidence levels
- `references/brownfield-prd-template.md` - Complete PRD template with examples

---

## When to Escalate

**Escalate to stakeholders when:**
- Critical business logic unclear from code
- Multiple valid interpretations of feature purpose
- Major architectural decisions needed
- Regulatory/compliance requirements unclear
- Conflicting documentation and code

**Escalate to architects when:**
- Complex architecture patterns unclear
- Scalability/performance issues significant
- Major refactoring required
- Technology migration decisions needed

**Use alternative skill when:**
- Creating PRD for new product → Use `create-prd` skill
- Document too large/complex → Use `shard-document` skill after creation
- Need validation checklist execution → Use `interactive-checklist` skill

---

*Part of BMAD Enhanced Planning Suite*
