---
name: shard-document
description: Break large documents into smaller, manageable shards with maintained relationships and navigation, improving document usability and maintenance for PRDs, specs, and technical documentation. Use when large documents (>5000 words) need splitting for better maintainability, navigation, or when documentation becomes difficult to navigate.
acceptance:
  - shards_created: "Document split into logical, focused shards"
  - navigation_provided: "Index/navigation document created for shard discovery"
  - relationships_maintained: "Cross-references and dependencies preserved"
  - metadata_complete: "Each shard includes metadata (title, purpose, dependencies)"
  - validation_passed: "All internal links verified, no broken references"
inputs:
  source_document:
    type: string
    required: true
    description: "Path to document to be sharded (absolute path)"
  sharding_strategy:
    type: string
    required: false
    description: "logical | size-based | semantic | custom (default: logical)"
    default: "logical"
  max_shard_size:
    type: number
    required: false
    description: "Maximum lines per shard (for size-based strategy, default: 500)"
    default: 500
  output_directory:
    type: string
    required: false
    description: "Directory for shard output (default: <source>-shards/)"
  preserve_original:
    type: boolean
    required: false
    description: "Keep original document alongside shards (default: true)"
    default: true
outputs:
  sharding_complete:
    type: boolean
    description: "Whether sharding completed successfully"
  shard_count:
    type: number
    description: "Number of shards created"
  output_location:
    type: string
    description: "Directory path containing shards and index"
  index_file:
    type: string
    description: "Path to navigation index file"
  broken_references:
    type: array
    description: "List of broken cross-references found during validation"
telemetry:
  emit: "skill.shard-document.completed"
  track:
    - source_document
    - sharding_strategy
    - shard_count
    - output_location
    - broken_references_count
    - duration_ms
---

# Shard Document Skill

## Purpose

Break large, monolithic documents into smaller, manageable shards that are easier to navigate, maintain, and understand. Particularly valuable for lengthy PRDs, technical specifications, architecture docs, and API documentation.

**Core Principles:**
- Logical boundaries (shard by topic/section, not arbitrary size)
- Relationship preservation (maintain cross-references)
- Navigation clarity (create clear index and links)
- Metadata richness (each shard self-describes purpose)
- Validation rigor (verify all references work)

---

## Prerequisites

- Source document exists and is readable
- Document has clear structure (headings, sections)
- Output directory is writable
- workspace/ directory available for shard storage

---

## Workflow

### Step 1: Analyze Document Structure

**Action:** Parse document to understand structure, identify logical boundaries, and assess sharding approach.

**Key Activities:**

1. **Parse Document Hierarchy**
   ```markdown
   Example document structure:

   # Product Requirements Document
   ## 1. Executive Summary (200 lines)
   ## 2. Vision & Objectives (150 lines)
   ## 3. User Personas (400 lines)
   ### 3.1 Persona: Sarah (SaaS Admin)
   ### 3.2 Persona: Mike (End User)
   ### 3.3 Persona: Lisa (Manager)
   ## 4. Market Analysis (600 lines)
   ### 4.1 Competitive Landscape
   ### 4.2 Market Segmentation
   ### 4.3 Differentiation Strategy
   ## 5. Feature Specifications (1200 lines) ⚠️ Large
   ### 5.1 Feature: Authentication
   ### 5.2 Feature: Dashboard
   ### 5.3 Feature: Reporting
   ### ... (20 more features)
   ## 6. Technical Requirements (800 lines)
   ## 7. Success Metrics (300 lines)

   Total: ~3,650 lines (too large for single document)
   ```

2. **Identify Shard Boundaries**

   **Logical Strategy (Recommended):**
   - Shard by major sections (Executive Summary, Personas, Market Analysis, etc.)
   - Break large sections into sub-shards (e.g., Features → one shard per feature)
   - Keep related content together (don't split mid-topic)

   **Size-Based Strategy:**
   - Split when section exceeds max_shard_size (default 500 lines)
   - Find nearest heading boundary
   - Create shard at logical break point

   **Semantic Strategy:**
   - Analyze content similarity
   - Group related topics even if in different sections
   - Advanced: requires NLP analysis

3. **Assess Cross-References**
   ```markdown
   Scan for internal links:
   - [See Market Analysis](#market-analysis)
   - [Feature dependencies in Technical Requirements](#technical-requirements)
   - [Success metrics for Dashboard feature](#feature-dashboard)

   Catalog all cross-references for later validation
   ```

4. **Determine Sharding Plan**
   ```
   Proposed Shards:
   1. index.md - Navigation hub (50 lines)
   2. executive-summary.md - Overview (200 lines)
   3. vision-objectives.md - Goals and vision (150 lines)
   4. personas.md - All user personas (400 lines)
   5. market-analysis.md - Competitive & market insights (600 lines)
   6. features/ - Directory with one file per feature (20 files)
      - authentication.md
      - dashboard.md
      - reporting.md
      - ... (17 more)
   7. technical-requirements.md - Tech specs (800 lines)
   8. success-metrics.md - KPIs and metrics (300 lines)

   Total: 8 top-level files + 20 feature shards = 28 shards
   Reduction: 3,650 lines → avg 130 lines per shard ✅
   ```

**Output:** Sharding plan with boundaries, file names, and relationships

**See:** `references/sharding-strategies.md` for strategy selection guidance

---

### Step 2: Extract Shards with Metadata

**Action:** Create individual shard files with proper metadata, navigation links, and content.

**Key Activities:**

1. **Create Shard Template**
   ```markdown
   ---
   shard_id: feature-authentication
   shard_type: feature-specification
   parent: prd-main
   created_from: product-requirements-document.md
   section: 5.1 Feature: Authentication
   related:
     - technical-requirements.md#authentication
     - success-metrics.md#auth-metrics
   dependencies:
     - feature-user-management
   tags:
     - authentication
     - security
     - core-feature
   ---

   # Feature: Authentication

   [◄ Back to PRD Index](index.md) | [Next: Dashboard ►](feature-dashboard.md)

   ## Feature Overview
   [Content from original section 5.1...]

   ## Related Documents
   - [Technical Requirements: Authentication](technical-requirements.md#authentication)
   - [Success Metrics: Auth Metrics](success-metrics.md#auth-metrics)
   - [User Persona: Sarah (SaaS Admin)](personas.md#sarah-saas-admin)

   ---

   **Shard Navigation:**
   - Previous: [Vision & Objectives](vision-objectives.md)
   - Up: [PRD Index](index.md)
   - Next: [Feature: Dashboard](feature-dashboard.md)
   ```

2. **Extract Content**
   - Copy section content from original document
   - Preserve heading hierarchy (adjust if needed)
   - Maintain formatting (code blocks, tables, lists)
   - Keep internal structure intact

3. **Update Internal Links**
   ```markdown
   Original document:
   See [Market Analysis](#market-analysis) for details.

   Sharded version (from feature-authentication.md):
   See [Market Analysis](market-analysis.md) for details.

   Update format:
   #section-name → filename.md
   #parent-section-name → filename.md#section-name
   ```

4. **Add Contextual Navigation**
   - Breadcrumbs (Parent document → Current section)
   - Previous/Next links (Sequential reading)
   - Related documents (Cross-references)
   - Back to index link (Always available)

5. **Enrich with Metadata**
   ```yaml
   Metadata includes:
   - shard_id: Unique identifier
   - shard_type: Category (feature, persona, analysis, technical, etc.)
   - parent: Original source document
   - section: Original section path
   - related: Cross-referenced shards
   - dependencies: Other shards this depends on
   - tags: Keywords for discovery
   - created_from: Source file path
   - created_at: Timestamp
   ```

**Output:** Individual shard files with complete metadata and navigation

**See:** `references/shard-metadata-guide.md` for metadata standards

---

### Step 3: Create Navigation Index

**Action:** Build master index document that provides overview and navigation to all shards.

**Key Activities:**

1. **Create Index Structure**
   ```markdown
   ---
   document_type: shard-index
   original_document: product-requirements-document.md
   shard_count: 28
   sharding_date: 2025-01-04
   sharding_strategy: logical
   ---

   # PRD: Product Requirements Document (Sharded)

   This document has been split into 28 focused shards for easier navigation and maintenance.

   **Original Document:** `product-requirements-document.md` (3,650 lines)
   **Sharded Version:** 28 documents (avg 130 lines each)

   ---

   ## Quick Navigation

   ### Core Documents
   1. [Executive Summary](executive-summary.md) - Product overview and key findings
   2. [Vision & Objectives](vision-objectives.md) - Product vision and goals
   3. [User Personas](personas.md) - Target user profiles
   4. [Market Analysis](market-analysis.md) - Competitive landscape
   5. [Technical Requirements](technical-requirements.md) - Technical specifications
   6. [Success Metrics](success-metrics.md) - KPIs and measurement

   ### Features (20 total)

   **Core Features:**
   - [Authentication](features/authentication.md) - User login and security
   - [Dashboard](features/dashboard.md) - Main user interface
   - [Reporting](features/reporting.md) - Analytics and reports

   **Secondary Features:**
   - [Notifications](features/notifications.md) - Email and in-app alerts
   - [User Profile](features/user-profile.md) - Profile management
   - ... [View all features](features/README.md)

   ---

   ## Reading Paths

   ### Path 1: Executive Overview (15 min read)
   1. [Executive Summary](executive-summary.md)
   2. [Vision & Objectives](vision-objectives.md)
   3. [User Personas](personas.md)
   4. [Market Analysis](market-analysis.md)

   ### Path 2: Feature Deep Dive (45 min read)
   1. [Feature Overview](features/README.md)
   2. Core features (Authentication, Dashboard, Reporting)
   3. [Technical Requirements](technical-requirements.md)
   4. [Success Metrics](success-metrics.md)

   ### Path 3: Complete Read (2 hour read)
   Follow sequential navigation links in each document.

   ---

   ## Shard Organization

   ```
   prd-shards/
   ├── index.md (this file)
   ├── executive-summary.md
   ├── vision-objectives.md
   ├── personas.md
   ├── market-analysis.md
   ├── technical-requirements.md
   ├── success-metrics.md
   └── features/
       ├── README.md
       ├── authentication.md
       ├── dashboard.md
       ├── reporting.md
       └── ... (17 more)
   ```

   ---

   ## Search by Tag

   **#core-feature:** Authentication, Dashboard, Reporting
   **#security:** Authentication, Data Encryption, Access Control
   **#analytics:** Dashboard, Reporting, Success Metrics
   **#user-facing:** All features under features/

   ---

   ## Original Document

   The original, unshard document is preserved at:
   [`product-requirements-document.md`](../product-requirements-document.md)
   ```

2. **Create Directory README Files**

   For subdirectories (like features/), create README.md:
   ```markdown
   # Features Directory

   This directory contains detailed specifications for all 20 product features.

   ## Core Features (Must Have)
   1. [Authentication](authentication.md) - User login and security
   2. [Dashboard](dashboard.md) - Main user interface
   3. [Reporting](reporting.md) - Analytics and reports

   ## Secondary Features (Should Have)
   4. [Notifications](notifications.md) - Email and in-app alerts
   5. [User Profile](user-profile.md) - Profile management
   ...

   ## Legacy Features (Won't Have v1)
   18. [Old Admin Panel](old-admin-panel.md) - Deprecated interface

   [◄ Back to PRD Index](../index.md)
   ```

3. **Generate Metadata Summary**
   ```markdown
   ## Shard Metadata

   | Shard | Type | Lines | Dependencies | Tags |
   |-------|------|-------|--------------|------|
   | executive-summary.md | overview | 200 | - | #summary #overview |
   | authentication.md | feature | 85 | user-management | #core #security |
   | dashboard.md | feature | 120 | authentication, reporting | #core #ui |
   ...

   Total Shards: 28
   Total Lines: 3,650 (across all shards)
   Average Shard Size: 130 lines
   ```

**Output:** Comprehensive index with multiple navigation paths

**See:** `references/navigation-patterns.md` for index design patterns

---

### Step 4: Validate Relationships

**Action:** Verify all cross-references, dependencies, and links work correctly.

**Key Activities:**

1. **Validate Internal Links**
   ```bash
   # Scan all shards for markdown links
   for file in *.md; do
     grep -o '\[.*\](.*\.md[^)]*)' "$file"
   done

   # Check each link target exists
   # Report broken links
   ```

2. **Verify Dependencies**
   ```markdown
   For each shard with dependencies:
   - Check dependency shards exist
   - Verify dependency sections referenced exist
   - Ensure no circular dependencies

   Example:
   authentication.md depends on user-management.md
   → Check: user-management.md exists ✅
   → Check: No circular dependency (user-management depends on authentication) ✅
   ```

3. **Check Cross-References**
   ```markdown
   From authentication.md:
   "See [Success Metrics: Auth Metrics](success-metrics.md#auth-metrics)"

   Validation:
   → success-metrics.md exists? ✅
   → Section #auth-metrics exists in success-metrics.md? ✅
   → Link format correct? ✅
   ```

4. **Verify Metadata Completeness**
   ```yaml
   For each shard, check:
   - shard_id present and unique ✅
   - shard_type defined ✅
   - parent specified ✅
   - tags include at least one tag ✅
   - related docs list is valid ✅
   ```

5. **Test Navigation Paths**
   ```markdown
   Test reading paths from index:

   Path 1: Executive Overview
   1. Index → Executive Summary ✅
   2. Executive Summary → Vision & Objectives ✅
   3. Vision & Objectives → User Personas ✅
   4. User Personas → Market Analysis ✅
   5. All "Back to Index" links work ✅
   ```

6. **Generate Validation Report**
   ```markdown
   # Shard Validation Report

   **Total Shards:** 28
   **Validation Status:** ✅ PASSED

   ## Validation Results

   ✅ Internal Links: 142/142 valid (0 broken)
   ✅ Dependencies: 35/35 resolved
   ✅ Cross-References: 89/89 valid
   ✅ Metadata: 28/28 complete
   ✅ Navigation Paths: 3/3 working

   ## Issues Found

   None ✅

   ---

   ## Recommendations

   - Consider adding more tags to personas.md (currently only 1 tag)
   - Feature shards could benefit from examples section
   - Add glossary shard for technical terms
   ```

**Output:** Validation report with broken link list and recommendations

**See:** `references/validation-checklist.md` for comprehensive validation

---

## Common Scenarios

### Scenario 1: Large PRD (3,000+ lines)

**Context:** Single PRD file too large to navigate

**Approach:**
- Strategy: Logical sharding
- Shard by major sections (Executive, Personas, Features, etc.)
- Create features/ subdirectory (one shard per feature)
- Result: 20-30 shards, avg 100-150 lines each

**Example Structure:**
```
prd-shards/
├── index.md
├── executive-summary.md
├── personas.md
├── market-analysis.md
├── features/
│   ├── README.md
│   ├── feature-1.md
│   └── ... (19 more)
├── technical-requirements.md
└── success-metrics.md
```

---

### Scenario 2: API Documentation (5,000+ lines)

**Context:** Comprehensive API docs with 100+ endpoints

**Approach:**
- Strategy: Logical + hierarchical
- Shard by API resource (Users, Products, Orders, etc.)
- Group endpoints within each resource shard
- Create separate authentication.md and errors.md shards

**Example Structure:**
```
api-docs-shards/
├── index.md
├── getting-started.md
├── authentication.md
├── errors.md
├── resources/
│   ├── users.md (GET/POST/PUT/DELETE /users)
│   ├── products.md (GET/POST/PUT/DELETE /products)
│   └── ... (20 more)
└── webhooks.md
```

---

### Scenario 3: Architecture Documentation (2,000+ lines)

**Context:** System architecture doc with multiple components

**Approach:**
- Strategy: Logical by component
- Shard by system component (Frontend, Backend, Database, etc.)
- Create separate decision-records/ directory for ADRs
- Maintain architecture-overview.md as entry point

**Example Structure:**
```
architecture-shards/
├── index.md
├── architecture-overview.md
├── components/
│   ├── frontend.md
│   ├── backend.md
│   ├── database.md
│   └── ... (5 more)
├── decision-records/
│   ├── adr-001-framework-choice.md
│   └── ... (10 more)
└── deployment.md
```

---

### Scenario 4: Size-Based Sharding (Any large document)

**Context:** Document with no clear logical structure

**Approach:**
- Strategy: Size-based (max_shard_size: 500 lines)
- Split at nearest heading when size exceeded
- Number shards sequentially (part-01.md, part-02.md, etc.)
- Maintain reading order with prev/next links

**Example Structure:**
```
document-shards/
├── index.md
├── part-01-introduction.md
├── part-02-methodology.md
├── part-03-findings-1.md
├── part-04-findings-2.md
└── part-05-conclusion.md
```

---

## Best Practices

1. **Prefer Logical over Size-Based** - Shard by topic/section, not arbitrary size
2. **Keep Related Content Together** - Don't split mid-topic for size constraints
3. **Use Descriptive File Names** - `authentication.md` not `feature-1.md`
4. **Add Rich Metadata** - Tags, dependencies, relationships for discovery
5. **Provide Multiple Navigation Paths** - Index, sequential, topic-based
6. **Validate Thoroughly** - Check all links, dependencies, cross-references
7. **Preserve Original** - Keep unshard document as backup/reference
8. **Document Shard Structure** - Clear README explaining organization
9. **Use Consistent Naming** - Follow conventions (kebab-case, descriptive)
10. **Version Control Friendly** - Smaller files = better diffs, easier reviews

---

## When to Escalate

**Escalate to stakeholders when:**
- Document structure unclear (no clear shard boundaries)
- Multiple valid sharding approaches (need decision)
- Critical cross-references can't be preserved
- Original document has no clear hierarchy

**Escalate to authors when:**
- Content organization illogical
- Sections heavily interdependent (can't cleanly separate)
- Terminology inconsistent across sections

**Use alternative skill when:**
- Creating new document → Use `create-prd` or `create-brownfield-prd`
- Document already well-structured → No sharding needed
- Interactive navigation required → Use `interactive-checklist` skill

---

## Reference Files

- `references/sharding-strategies.md` - Strategy selection and comparison
- `references/shard-metadata-guide.md` - Metadata standards and examples
- `references/navigation-patterns.md` - Index and navigation design
- `references/validation-checklist.md` - Comprehensive validation steps
- `references/naming-conventions.md` - File and directory naming standards

---

*Part of BMAD Enhanced Planning Suite*
