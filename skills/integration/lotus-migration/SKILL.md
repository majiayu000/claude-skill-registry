---
name: lotus-migration
description: |
  Analyze and plan migrations of Lotus Notes applications to modern platforms.
  Use when understanding Lotus Notes architecture, analyzing NSF databases,
  identifying integration points, planning migration strategies, or translating
  Notes concepts to modern equivalents. Covers Forms, Views, Agents, Script Libraries,
  Formula Language, LotusScript, direct database writes, ODBC connections, and
  replacement architecture decision frameworks.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

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

Each integration pattern has optimal replacement strategies:

#### Direct Database Writes (Highest Priority)

**Why This Matters:** Direct DB writes represent the tightest coupling and are highest priority for migration because they:
- Create schema dependencies
- Make testing difficult
- Provide poor error visibility
- Create change coordination challenges

**Option A: REST API Integration** ⭐ Recommended for most cases
- Source app calls API endpoint instead of writing database
- Target system owns database changes
- Clear error handling and versioning
- Easier to monitor and debug
- Overhead: Requires API development, network latency

**Option B: Message Queue Integration** ⭐ Best for asynchronous, high-volume
- Source app publishes message (incident/charge data)
- Target system subscribes and processes
- Decoupled, scalable, replay capability
- Better for high-volume scenarios
- Overhead: Queue infrastructure, eventual consistency, monitoring

**Option C: Shared Staging Table** - Transitional approach
- Source app writes to staging table
- Target system polls and processes
- Maintains existing database connectivity
- Simple atomic transactions
- Downside: Maintains coupling, less modern

**Option D: Event Sourcing** - Strategic long-term
- Apps emit domain events (IncidentCreated, ViolationDetected)
- Event store captures all changes
- Subscribers react to events
- Full audit trail, replay capability
- Overhead: Complex, requires event infrastructure

**Decision Matrix:**
```
Integration Type          | Volume | Latency | Best Fit | Alternative
--------------------------|--------|---------|----------|-------------
Direct DB Write (sync)   | Low    | <1s     | API      | Staging Table
Direct DB Write (batch)  | High   | Hours   | API+Queue| Batch API
ODBC Read (reference)    | Low    | Seconds | API      | Cache Layer
ODBC Read (transactional)| Medium | <1s     | API/Query| Cached API
File Export              | Medium | Minutes | Scheduled Job | Event Stream
Email Notification       | Low    | Minutes | Message/Event | Direct Service
```

#### ODBC Connections

**Replacement Strategy:**
1. **If reading reference data:** Create API endpoint, cache results, sunset ODBC
2. **If reading transactional data:** Refactor to direct SQL or service API
3. **If writing data:** Replace with API or message-based approach
4. **Mainframe dependencies:** Prioritize API layer to abstract mainframe

**Example:** Mainframe DB2 ODBC queries in VRS validation
- Current: VRS agents query DB2 via ODBC for product validation
- Problem: Tight coupling, network latency, hard to troubleshoot
- Solution: Create API wrapper around DB2 data, migrate VRS to call API, decommission ODBC

#### File-Based Integrations

**Current Usage in B&O:** Oracle Finance exports, PDP feeds

**Replacement Strategy:**
1. **For exports (outbound):** Keep file-based as intermediary, add API-first capability
2. **For imports (inbound):** Prefer file over API for compatibility
3. **For both:** Use file staging as transitional; move to API for new integrations
4. **Improve:** Standardize formats, add schema validation, improve error handling

#### Reference Data Integrations

**Critical Issue in B&O:** BDL feeds being decommissioned
- Current: Four reference databases (Assortment, Supplier Info, Buying Groups, Lookups) fed by BDL
- Problem: BDL decommissioning creates immediate risk
- Action: Identify alternative sources urgently

**Replacement Strategy:**
1. **Map data lineage:** Where does BDL data originate?
2. **Identify alternatives:** Which systems own this data?
3. **Design sync mechanism:** Periodic file-based? API? Real-time?
4. **Create migration path:** Batch initial load, incremental updates ongoing

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

### Example 1: Analyzing a Direct Database Integration

**Scenario:** Understand the Product Incidents → B&O integration

**Steps:**

1. **Gather details**
   ```
   Application: Product Incidents Lotus Notes
   Owner: Quality Assurance team
   Purpose: Track product quality issues, generate supplier charges
   Integration: Direct database write to B&O
   ```

2. **Map integration**
   ```
   Direction: Inbound (to B&O)
   Type: Direct database write
   Trigger: When incident is marked as billable
   Data: Supplier ID, charge amount, incident details
   Frequency: ~50 incidents per day
   Volume: Small (kilobytes per write)
   Criticality: HIGH (blocks supplier charge processing)
   ```

3. **Identify constraints**
   ```
   - Tight coupling to B&O database schema
   - No error handling visible to users
   - No retry mechanism
   - Schema changes in B&O break Product Incidents
   - Hard to test (requires B&O database)
   ```

4. **Recommend replacement**
   ```
   Strategy: REST API
   Reasoning:
     - Decouples Product Incidents from B&O schema
     - Enables proper error handling
     - Allows versioning and evolution
     - Easier testing (mock API)
     - Standard pattern (more maintainable)
   ```

5. **Design API specification**
   ```
   POST /api/v1/supplier-charges
   Request: { supplierId, amount, incidentId, description, ... }
   Response: { chargeId, status, createdAt, ... }
   Errors: 400 (validation), 409 (duplicate), 500 (server error)
   Idempotency: Via idempotency-key header
   ```

6. **Plan cutover**
   ```
   Phase 1 (Week 1): Deploy API, run parallel
   Phase 2 (Week 2): Validation, testing
   Phase 3 (Week 3): Cutover
     - Product Incidents app updated to call API
     - Monitor for errors
     - Rollback plan ready
   ```

### Example 2: Replacing ODBC with API Layer

**Scenario:** Mainframe DB2 ODBC queries for product validation

**Current State:**
```
VRS Agents → ODBC Query → Mainframe DB2 → Product validation data
```

**Problems:**
- Network latency for every transaction
- Hard to troubleshoot issues
- Tight coupling to mainframe database
- Performance bottleneck

**Replacement:**
```
Step 1: Create API wrapper around DB2
  - Query mainframe DB2 directly from new API
  - Cache results to reduce mainframe hits
  - Return consistent JSON format

Step 2: Update VRS to call API instead of ODBC
  - Replace ODBC connection string with API endpoint
  - Add error handling for API failures
  - Test fallback/retry logic

Step 3: Decommission ODBC driver
  - Remove from Notes agent
  - Clean up configuration
  - Remove from infrastructure
```

**Benefits:**
- Single API layer can be called from multiple systems
- Can add caching without touching mainframe
- Network calls visible and monitorable
- Easier to troubleshoot (API logs vs. ODBC traces)
- Path to decommissioning mainframe

### Example 3: Designing Multi-Integration Cutover Sequence

**Scenario:** B&O system has 10+ integrations, cannot migrate all at once

**Assessment:**
```
CRITICAL (Do First):
  - Reference databases (BDL decommissioning)
  - VRS configuration

HIGH (Early):
  - Product Incidents (direct DB write)
  - Delivery Standards (direct DB write)
  - Oracle Finance (business critical)

MEDIUM (Mid):
  - PDP (coordinate with their rework)
  - Mainframe ODBC

LOW (Later):
  - Email system
  - File uploads
```

**Sequence:**
```
Month 1 (Weeks 1-4):
  - Resolve BDL alternatives (URGENT)
  - Modernize reference database feeds
  - Design VRS replacement

Month 2 (Weeks 5-8):
  - Build API for Product Incidents
  - Build API for Delivery Standards
  - Parallel testing begins

Month 3 (Weeks 9-12):
  - Cutover Phase 1 (test environment)
  - Cutover Phase 2 (staging)
  - Production cutover

Month 4+ (Weeks 13+):
  - Optimize remaining integrations
  - Retire legacy Notes dependencies
  - Document lessons learned
```

**Risk Mitigation:**
- Parallel running reduces cutover risk
- Early focus on critical dependencies
- Clear communication with all teams
- Well-documented rollback procedures
- Dedicated testing environment

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
