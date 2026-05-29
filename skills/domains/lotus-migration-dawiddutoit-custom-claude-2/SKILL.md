---
name: lotus-migration
description: |
  Analyzes and plans migrations of Lotus Notes applications to modern platforms.
  Use when understanding Lotus Notes architecture, analyzing NSF databases,
  identifying integration points, planning migration strategies, or translating
  Notes concepts to modern equivalents.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

Covers Forms, Views, Agents, Script Libraries, Formula Language, LotusScript, direct database writes, ODBC connections, and replacement architecture decision frameworks.
# Lotus Notes Migration Skill

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#examples)

**How to Implement** → [Step-by-Step](#instructions) | [Expected Outcomes](#quick-start)

**Reference** → [Requirements](#requirements) | [Related Skills](#see-also)

## Purpose

This skill helps architects, developers, and technical leads analyze Lotus Notes applications, understand their architecture and integration patterns, plan migration strategies, and design modern replacements. It provides frameworks for assessing complexity, identifying dependencies, translating legacy patterns to modern equivalents, and managing the organizational and technical challenges of large-scale Notes migrations.

## When to Use

Use this skill when you need to:

- **Understand Lotus Notes applications** - Analyze NSF structure, design elements, Forms, Views, Agents, and Script Libraries
- **Identify integration points** - Map all inbound/outbound integrations, ODBC connections, and data flows
- **Plan migration strategies** - Choose between API integration, message queues, file staging, or event sourcing
- **Translate Notes concepts** - Convert Formula Language, LotusScript, or Notes patterns to modern equivalents
- **Assess migration complexity** - Evaluate risks, dependencies, and effort required for migration
- **Design replacement architecture** - Create modern system designs that replace legacy Notes functionality
- **Manage stakeholder expectations** - Plan phased migrations with testing, rollback, and communication strategies

This skill provides comprehensive guidance for all aspects of Lotus Notes migration projects.

## Quick Start

Use this skill when you need to:

1. **Understand a Lotus Notes application** - Analyze NSF structure, design elements, and how they work
2. **Identify integrations** - Map all inbound/outbound integration points and data flows
3. **Choose a replacement strategy** - Evaluate API integration, message queues, file staging, event sourcing, or hybrid approaches
4. **Plan a migration** - Design phased approach with testing, rollback, and stakeholder management
5. **Translate Notes concepts** - Convert Formula Language, LotusScript, or Notes patterns to modern equivalents

**Example Use Cases:**
- "Analyze the Product Incidents Lotus Notes application to understand its database writes to B&O"
- "Identify all ODBC connections in the VRS configuration database and plan replacement"
- "Design an API specification to replace a direct database integration from Delivery Standards"
- "Extract rich text fields from reference database and plan data migration strategy"

## Instructions

### Step 1: Gather Application Details

Before planning any migration, establish baseline understanding:

1. **Identify the application**
   - Application name and primary purpose
   - Owner and technical maintainer
   - Users and usage volume
   - Strategic importance (critical path, legacy, sunset?)

2. **Document the NSF structure**
   - Database name and path
   - Design elements present:
     - Forms (data entry/display structures)
     - Views (how data is displayed/filtered)
     - Agents (scheduled or manual automation)
     - Script Libraries (reusable code)
     - Design resources (images, CSS, HTML)
   - Data volume and growth rate
   - User count and access patterns

3. **Review existing documentation**
   - Design documentation (if available)
   - Business process documentation
   - Known issues or workarounds
   - Technical debt areas

**Questions to Ask:**
- What business process does this application support?
- Who depends on this application?
- What data sensitivity/compliance requirements exist?
- When was the application last updated?
- Are there plans to replace or sunset it?

### Step 2: Map All Integration Points

Integration patterns are the primary concern in Notes migrations because they determine replacement complexity:

1. **Identify inbound integrations** (data flowing INTO the Notes app)
   - Direct database writes (from other apps)
   - File uploads (CSV, XML, Excel)
   - ODBC connections (reading external databases)
   - Email triggers
   - Web service calls
   - Message queue consumption
   - Replication from other Notes databases

2. **Identify outbound integrations** (data flowing OUT of Notes app)
   - Direct database writes (to other apps/databases)
   - File exports (Oracle Finance, PDP, data warehouses)
   - ODBC writes (to external databases)
   - Email notifications/reminders
   - API calls
   - Report generation
   - Replication to other Notes databases

3. **Document each integration**
   - **What:** What data is transferred?
   - **Where:** Source and destination systems
   - **How:** Technology/method used
   - **When:** Frequency, schedule, or trigger
   - **Volume:** Data volume, frequency, peak times
   - **Dependencies:** What breaks if this fails?
   - **Error Handling:** How are errors detected/resolved?

4. **Create integration map** using this format:
   ```
   | Integration | Direction | Type | Source/Dest | Frequency | Volume | Critical? |
   |-------------|-----------|------|------------|-----------|--------|-----------|
   | Direct DB Write | Inbound | Database | Product Incidents → B&O | On-demand | ~50/day | YES |
   | ODBC Lookup | Inbound | Query | VRS → Mainframe DB2 | Per transaction | ~1000/day | YES |
   | File Export | Outbound | File | B&O → Oracle Finance | Daily batch | ~2000 records | CRITICAL |
   ```

**See also:** Local documentation at `docs/B&O-Integrations-and-Touchpoints.md`

### Step 3: Analyze Data Structures and Fields

Lotus Notes' document-based, semi-structured approach is fundamentally different from relational databases:

1. **Document structure analysis**
   - What document types exist in the database?
   - What fields are mandatory vs. optional?
   - What is the actual data schema (may differ from design)?
   - Are there computed fields or formulas that generate data?
   - What validation formulas exist?

2. **Handle rich text fields**
   - Identify all rich text fields
   - Determine what they contain (formatted text, embedded objects, file attachments)
   - For migration, you'll likely need to:
     - Convert to HTML/Markdown for modern storage
     - Extract file attachments separately
     - Use tools like Genii AppsFidelity for complex conversions
     - Create test data with samples of rich text variations

3. **Address semi-structured data**
   - Document flexibility in schema is a feature, not a bug in Notes
   - For migration, you must decide:
     - Enforce stricter schema in target system?
     - Create flexible storage (JSONB columns, document stores)?
     - Map different document types to different tables?
   - Identify documents that don't fit the primary pattern

4. **Map to modern equivalents**
   - Notes Form → UI Form/API Input Schema
   - Notes View → SQL Query/GraphQL Resolver/API Endpoint
   - Rich Text → HTML + Attachments Storage
   - Formula Field → Computed Field/View/Trigger
   - Document → Database Record/Document in Document Store

### Step 4: Assess Integration Complexity

Not all integrations have equal migration complexity. Use this framework:

**Complexity Level 1: Simple (Low Risk)**
- Direct data consumption (read from file, API, ODBC)
- No write-back requirements
- Data is consistent and well-formed
- Few dependencies
- Example: Readonly reference data lookup

**Complexity Level 2: Moderate (Medium Risk)**
- Bidirectional sync with periodic reconciliation
- Some data transformation required
- Multiple data sources
- Example: VRS configuration sync with monitoring

**Complexity Level 3: Complex (High Risk)**
- Direct database writes (tight coupling)
- Real-time transaction flow
- Rich data transformations
- Multiple system dependencies
- Example: Product Incidents → B&O direct writes

**Complexity Level 4: Critical (Very High Risk)**
- Multiple levels of dependencies
- Business-critical process path
- Complex state management
- Difficult to test
- Example: Reference databases supporting all B&O transactions

**Assessment Dimensions:**
1. **Technical Coupling:** How tightly coupled is the integration?
2. **Data Complexity:** How complex is the data and transformations?
3. **Volume & Performance:** What are latency/throughput requirements?
4. **Dependencies:** How many systems depend on this?
5. **Testability:** How easy is it to test the integration?

### Step 5: Choose Replacement Strategy

Each integration pattern has optimal replacement strategies. See **[references/integration-strategies.md](references/integration-strategies.md)** for comprehensive details.

#### Quick Decision Guide

**Direct Database Writes (Highest Priority):**
- REST API Integration ⭐ (most cases)
- Message Queue ⭐ (high volume, async)
- Staging Table (transitional)
- Event Sourcing (strategic long-term)

**ODBC Connections:**
- Reference data → API with caching
- Transactional data → API or direct SQL
- Mainframe → API layer (path to retirement)

**File-Based Integrations:**
- Keep for batch exports/imports
- Add API capability for new consumers
- Standardize formats, add validation

**Reference Data:**
- Identify alternative sources
- Design sync mechanism (file/API/hybrid)
- Batch initial load, incremental updates

### Step 6: Design API Replacement Specifications

For direct database integrations, REST API is usually the right choice:

**API Specification Template:**

```yaml
# Example: Product Incidents to B&O Integration

API: POST /invoices/supplier-charges

Purpose: Create supplier charge invoice from incident or violation

Request Body:
  {
    "type": "incident|violation",
    "supplierId": "string (required)",
    "chargeAmount": "decimal (required)",
    "currency": "GBP|EUR|USD (default: GBP)",
    "description": "string (required)",
    "referenceNumber": "string (e.g., incident ID)",
    "dateOccurred": "ISO 8601 date",
    "metadata": {
      "source": "product-incidents|delivery-standards",
      "sourceId": "string",
      "category": "string (incident type or violation type)"
    }
  }

Response (Success):
  {
    "invoiceId": "string (UUID)",
    "status": "created",
    "supplierId": "string",
    "chargeAmount": "decimal",
    "createdAt": "ISO 8601 timestamp",
    "links": {
      "self": "/invoices/supplier-charges/{invoiceId}",
      "status": "/invoices/supplier-charges/{invoiceId}/status"
    }
  }

Error Responses:
  400 Bad Request:
    - Missing required fields
    - Invalid supplier ID
    - Invalid amount
  401 Unauthorized:
    - Missing/invalid API key
  409 Conflict:
    - Duplicate charge (idempotency key)
  500 Internal Server Error:
    - Database unavailable
    - Unexpected error

Idempotency:
  - Include idempotency-key header for safely retrying
  - Same idempotency-key returns same result

Authentication:
  - API key in Authorization header
  - OAuth 2.0 for interactive clients

Rate Limiting:
  - 1000 requests per minute
  - Backoff strategy: exponential with jitter
```

**Key Design Principles:**
1. **Idempotency:** Enable safe retries with idempotency keys
2. **Versioning:** Plan for API evolution (v1, v2)
3. **Error Handling:** Clear error codes and messages
4. **Documentation:** Swagger/OpenAPI specification
5. **Testing:** Contract tests between client and server

### Step 7: Plan Data Migration and Cutover

**Three-Phase Approach:**

**Phase 1: Parallel Running (2-4 weeks)**
- New system running in parallel with Notes
- Notes still active, source of truth
- New system receives copies of data
- Validate new system produces correct results
- Identify data mapping issues
- Users still working in Notes

**Phase 2: Validation (1-2 weeks)**
- Run reconciliation reports
- Compare old vs. new system outputs
- Fix any remaining mapping issues
- Test all integration points
- Train users on new system
- Prepare rollback procedures

**Phase 3: Cutover (1 day)**
- Final data sync from Notes to new system
- Stop Notes application writes
- Users switch to new system
- Monitor closely for issues
- Keep Notes in read-only for fallback

**Rollback Plan:**
- If critical issues: Revert to Notes as source
- Maintain reverse sync capability for 1-2 weeks
- Document all issues found
- Plan fixes for next iteration

### Step 8: Plan Migration Sequencing

For applications with multiple integrations (like the B&O system), sequence is critical:

**Priority Framework:**
1. **Criticality:** Business-critical path first
2. **Risk:** Reduce unknowns early
3. **Dependencies:** Resolve blocking items
4. **Resource availability:** Plan around team capacity

**B&O Example Sequencing:**
```
Phase 1 (Weeks 1-2): Foundation
  - Resolve BDL decommissioning (URGENT)
  - Design VRS API replacement
  - Clarify unclear integrations

Phase 2 (Weeks 3-4): High-Risk Integrations
  - Replace direct DB writes (Product Incidents, Delivery Standards)
  - Design Oracle Finance modernization
  - Plan mainframe ODBC replacement

Phase 3 (Weeks 5-6): Supporting Integrations
  - Modernize PDP integration
  - Coordinate with PDP team
  - Improve file upload handling

Phase 4 (Weeks 7+): Optimization
  - Retire MFT dependency
  - Event sourcing consideration
  - Performance tuning
```

### Step 9: Stakeholder and Change Management

Large migrations require careful stakeholder engagement:

**Stakeholder Identification:**
- **Business owners:** Who benefits from migration? Timeline preferences?
- **Application owners:** Product Incidents, Delivery Standards teams
- **Technical teams:** Database, integration, architecture
- **Operations:** Who runs the applications?
- **Users:** Who will be affected by changes?
- **Finance/Security:** Governance, compliance, risk

**Communication Plan:**
1. **Kickoff:** Explain why, what changes, timeline
2. **Weekly updates:** Progress, blockers, next steps
3. **Mid-phase review:** Validate assumptions, address concerns
4. **Pre-cutover:** Final prep, procedures, support
5. **Post-cutover:** Monitoring, issues, lessons learned

**Training and Support:**
- For new UI: Screenshot guides, video tutorials
- For new APIs: Developer documentation, examples
- For operations: Runbooks for monitoring, troubleshooting
- Support line: Who to contact for issues?

### Step 10: Testing Strategy

Migrations require extensive testing at multiple levels:

**Unit Tests:**
- Individual business logic
- Data transformations
- Validation rules

**Integration Tests:**
- API calls succeed and fail correctly
- Error handling works
- Data flows end-to-end
- External system calls work

**Data Migration Tests:**
- Historical data migrates correctly
- Rich text conversion works
- No data loss
- Reconciliation reports match

**UAT (User Acceptance Testing):**
- Business users validate
- All use cases work
- Performance acceptable
- No surprises

**Performance Tests:**
- Expected volume handled
- Latency acceptable
- Peak load testing
- Scalability validated

**Failover/Rollback Tests:**
- Rollback procedures work
- Data consistency maintained
- Communication channels clear

## Examples

**For comprehensive migration examples with complete analysis and implementation details**, see:

- **[references/detailed-examples.md](references/detailed-examples.md)** - Contains three complete examples:
  1. Analyzing a Direct Database Integration (Product Incidents → B&O)
  2. Replacing ODBC with API Layer (VRS Mainframe Integration)
  3. Designing Multi-Integration Cutover Sequence (B&O System)

Each example includes full requirements, technical specifications, API designs, cutover plans, and risk mitigation strategies.

## Requirements

- Access to Lotus Notes databases (NSF files) or administrator who can provide details
- Documentation of current integration architecture
- Stakeholder availability for interviews and decisions
- Technical team with database and integration expertise
- Project management discipline for phased implementation

## See Also

- **Local Documentation:** Review integration investigations at `docs/lotus-notes-apps/investigation.md` for context-specific details
- **Integration Overview:** `docs/B&O-Integrations-and-Touchpoints.md` for complete integration catalog
- **Technical Analysis:** `docs/Bonuses & Overriders - Analysis.md` for system architecture
- **Reference Databases:** `docs/reference-databases/investigation.md` for data lineage (critical: BDL decommissioning)
- **Project Context:** `CLAUDE.md` in project root for setup, dependencies, and Jira integration
