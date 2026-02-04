---
name: RecordsManager
description: Expert record keeping system with paperless-ngx integration, country-specific taxonomies, and intelligent document management. USE WHEN upload document, store file, organize records, find document, search papers, tag documents, delete records, retention check, archive documents, add entity, create trust, validate trust, workflow create, FTE check, connection test, system status, check status.
---

# Records Manager Skill

> Expert record keeping with paperless-ngx integration, country-specific taxonomies, and safe deletion practices

## Overview

The Records Manager Skill is a subject matter expert in record keeping and document management. It integrates with paperless-ngx to provide intelligent document organization, trust-specific expertise, automated workflow management, and safe deletion practices.

**Core Capabilities:**
- Intelligent document upload with automatic tagging
- **NEW: Trust document management** with ATO-compliant retention rules
- **NEW: Automated workflow creation** based on document patterns
- **NEW: Dynamic entity creation** for households, businesses, and trusts
- Country-specific record keeping taxonomies (AU, US, UK)
- Retention requirement checking
- Safe deletion with mandatory confirmation
- Search optimization for document discovery

**Key Safety Feature:**
Document deletion ALWAYS requires explicit approval through the DeleteConfirmation workflow. This prevents catastrophic data loss.

---

## Voice Notification

When executing workflows, send voice notification:

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the WORKFLOWNAME workflow from the Records Manager skill"}' \
  > /dev/null 2>&1 &
```

---

## Workflow Routing

| Trigger | Workflow | Purpose |
|---------|----------|---------|
| Upload intent | `Workflows/UploadWorkflow.md` | Add documents with intelligent tagging |
| Search intent | `Workflows/SearchWorkflow.md` | Find documents by tags, content, type |
| Organize intent | `Workflows/OrganizeWorkflow.md` | Suggest and apply taxonomy improvements |
| Tag intent | `Workflows/TagWorkflow.md` | Add or modify tags on documents |
| Delete intent | `Workflows/DeleteConfirmation.md` | **MANDATORY** approval workflow |
| Retention intent | `Workflows/RetentionWorkflow.md` | Check retention requirements |
| Info intent | `Workflows/InfoWorkflow.md` | Get document details and metadata |
| "Navigate taxonomy" | Use TaxonomyExpert hierarchical methods | Browse Function→Service→Activity→DocumentType |
| "Add new entity" | `Workflows/AddEntityWorkflow.md` | Create new entity interactively |
| "Create a workflow" | `Workflows/WorkflowCreator.md` | Analyze documents and recommend workflow |
| "Review workflow" | `Workflows/WorkflowReview.md` | Analyze workflow effectiveness |
| "Trust documents" | `Workflows/TrustValidation.md` | Validate trust document completeness |
| "FTE retention" | `Workflows/FTECheck.md` | Check Family Trust Election retention |
| "Update taxonomies" | `Workflows/TaxonomyUpdate.md` | Sync taxonomy changes from YAML to paperless-ngx |
| "Check status" | `Workflows/StatusCheck.md` | Test connection and verify system status |

---

## Examples

**Example 1: Upload a tax document**
```
User: "Store this medical receipt for tax"
→ Invokes Upload workflow
→ TaxonomyExpert suggests tags: medical, receipt, tax-deductible, 2024
→ Uploads to paperless-ngx with metadata
→ Returns: "Document uploaded as #1234 with tags: medical, receipt, tax-deductible"
```

**Example 2: Check retention before deletion**
```
User: "Can I delete my 2019 tax returns?"
→ Invokes Retention workflow
→ Checks ATO requirements: 5 years from lodgment
→ Returns: "⚠️ Retain until 2025-06-30. 2019 returns filed in 2020 must be kept 5 years."
```

**Example 3: Validate trust compliance**
```
User: "Validate Smith Family Trust documents"
→ Invokes TrustValidation workflow
→ Checks required documents against trust type checklist
→ Returns: "8/10 documents found. Missing: Beneficiary Declaration, 2024 Distribution Minutes"
```

---

## Workflows

### Upload Workflow

**Triggers:**
- "Upload this document"
- "Store this file"
- "Add to records"
- "Save this [document type]"

**Process:**
1. Ask for file path or document
2. Determine domain (household/corporate/projects) from context or user
3. Use TaxonomyExpert to suggest tags and document type
4. Get or create tags in paperless-ngx
5. Upload document with metadata
6. Confirm upload and show document ID

**CLI Command:**
```bash
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts upload <file> --domain <domain>
```

---

### Search Workflow

**Triggers:**
- "Find [document type]"
- "Search for [query]"
- "Show me [tag] documents"
- "Where are my [type] records?"

**Process:**
1. Parse search criteria from user request
2. Build search query with tags, types, dates
3. Execute search via PaperlessClient
4. Present results with document details
5. Offer to show more details or refine search

**CLI Command:**
```bash
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts search --query <text> --tags <tags> --type <type>
```

---

### Organize Workflow

**Triggers:**
- "Organize my records"
- "Clean up documents"
- "Improve document structure"
- "Suggest better tags"

**Process:**
1. Get untagged or poorly tagged documents
2. Use TaxonomyExpert to analyze and suggest improvements
3. Show suggested tags and types
4. Ask user approval before applying
5. Update document metadata in paperless-ngx
6. Report changes made

**CLI Command:**
```bash
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts organize --domain <domain> --apply
```

---

### Tag Workflow

**Triggers:**
- "Tag these documents"
- "Add [tag] to documents"
- "Change tags on [document]"

**Process:**
1. Get document IDs and tag names from user
2. Verify documents exist
3. Get or create tags in paperless-ngx
4. Apply tags to documents
5. Confirm changes

**CLI Command:**
```bash
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts tag <docIds> <tagNames>
```

---

### Delete Confirmation Workflow (CRITICAL)

**Triggers:**
- "Delete these documents"
- "Remove old records"
- "Purge [tag] documents"
- **ANY deletion intent**

**Process:**
1. Show documents that will be deleted (ID, title, date, tags)
2. Check retention requirements for each document
3. Warn if documents within retention period
4. Explain consequences (permanent, no undo)
5. Require EXACT confirmation phrase
6. Only after approval: Execute deletion
7. Log decision to audit trail

**MANDATORY APPROVAL PHRASE:**
```
I understand this cannot be undone and I want to proceed with deleting N documents
```

**Do NOT accept:**
- "yes"
- "do it"
- "proceed"
- "delete them"
- Any casual confirmation

**CLI Command:**
```bash
# This command REFUSES to delete and points to the workflow
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts delete <query>
```

**Why This Matters:**
Deleting records is catastrophic. Tax documents, legal papers, insurance policies - once deleted, they're gone forever. The confirmation workflow ensures:
- Principal sees exactly what will be deleted
- Retention warnings are surfaced
- Decision is intentional and understood
- Audit trail exists for compliance

---

### Retention Workflow

**Triggers:**
- "What can I shred?"
- "How long should I keep [type]?"
- "Retention requirements"
- "Can I delete old [documents]?"

**Process:**
1. Get document type or domain from user
2. Look up retention requirements for country and type
3. Show retention period and legal reason
4. Calculate keep-until date for documents
5. Advise what can be safely archived or deleted

**CLI Command:**
```bash
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts retention --domain <domain>
```

---

### Info Workflow

**Triggers:**
- "Show me document [ID]"
- "What do you know about [document]?"
- "Details for [document]"

**Process:**
1. Get document ID from user
2. Fetch document details from paperless-ngx
3. Show metadata: title, date, tags, type
4. Check retention requirements
5. Advise if document can be archived or deleted

**CLI Command:**
```bash
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts info <docId>
```

---

### Add Entity Workflow

**Triggers:**
- "Add a new entity"
- "Create a trust"
- "Set up a new business"
- "Add entity: [type]"

**Process:**
1. Ask entity type (household/corporate/unit-trust/discretionary-trust/family-trust/project)
2. Gather type-specific information (ABN, TFN, trustee, FTE date, etc.)
3. Create entity structure in paperless-ngx:
   - Entity tag for document identification
   - Required tags for entity-specific classification
   - Storage path for hierarchical organization
   - Custom fields for trust metadata
4. Register entity in local registry
5. Confirm entity creation with details

**Example:**
```
User: "Add a family trust for Smith family"
AI: "Creating Smith Family Trust entity..."
    "I'll need some information:"
    "  - Trustee name?"
    "  - ABN?"
    "  - Family Trust Election date?"
    "  - TFN (optional)?"
    [Creates entity tag, storage path, custom fields]
    "✅ Entity created: smith-family-trust-2024"
    "   Documents can now be tagged with 'entity:smith-family-trust'"
```

---

### Workflow Creator Workflow

**Triggers:**
- "Create a workflow for [documents]"
- "Automate tagging of [pattern]"
- "Recommend workflow for [entity]"

**Process:**
1. Get sample documents or describe pattern
2. Analyze document patterns (filename, content, tags)
3. Recommend workflow configuration:
   - Matching pattern
   - Tags to apply
   - Document type to assign
   - Storage path to use
   - Correspondent to assign
4. Show confidence and reasoning
5. Ask for approval
6. Create workflow in paperless-ngx
7. Test workflow on sample documents
8. Report effectiveness

**Example:**
```
User: "Recommend a workflow for Smith Family Trust documents"
AI: "Analyzing 47 documents tagged 'smith-family-trust'..."
    "Recommendation (high confidence):"
    "  Match: 'Smith.*Trust|Family.*Trust.*Smith'"
    "  Assign tag: entity:smith-family-trust"
    "  Assign storage path: /Trusts/Family/Smith Family Trust"
    "  Assign document type: Auto-detect from content"
    "  Reasoning: 45/47 documents match this pattern"
    "Approve? (yes/no)"
```

---

### Workflow Review Workflow

**Triggers:**
- "Review workflow performance"
- "Check workflow effectiveness"
- "Analyze workflow [name]"

**Process:**
1. Get workflow ID or name
2. Fetch workflow configuration from paperless-ngx
3. Test workflow against sample documents
4. Analyze match rate and accuracy
5. Identify false positives/negatives
6. Suggest improvements to matching rules
7. Report findings and recommendations

---

### Trust Validation Workflow

**Triggers:**
- "Validate trust documents"
- "Check trust completeness"
- "What documents am I missing for [trust]?"

**Process:**
1. Get trust type and trust name
2. Retrieve required document checklist for trust type
3. Search paperless-ngx for existing documents
4. Compare against checklist
5. Report:
   - Complete documents
   - Missing documents
   - Warnings (FTE retention, expired documents)
   - Retention compliance issues

**Example:**
```
User: "Validate Smith Family Trust documents"
AI: "Checking Smith Family Trust completeness..."
    "Required documents (10):"
    "  ✅ Trust Deed"
    "  ✅ Family Trust Election (FTE) - Retain until 2025-02-01"
    "  ✅ Trustee Appointment"
    "  ⚠️  Beneficiary Declaration - MISSING"
    "  ✅ ABN Registration"
    "  ❌ TFN Registration - NOT FOUND"
    "  ✅ Annual Financial Statements (2023)"
    "  ⚠️  Trustee Resolution (2024) - NOT YET CREATED"
    "  ⚠️  Distribution Minutes (2024) - NOT YET CREATED"
    "  ✅ Tax Return (2023)"
    ""
    "Action items:"
    "  1. Upload Beneficiary Declaration"
    "  2. Upload TFN Registration"
    "  3. Create pre-EOFY trustee resolution (before June 30)"
    "  4. Document beneficiary distributions for 2024"
```

---

### FTE Check Workflow

**Triggers:**
- "Check FTE retention"
- "When can I delete FTE document?"
- "Family Trust Election compliance"

**Process:**
1. Get FTE document ID or FTE date
2. Calculate retention period (5 years from FTE date, not EOFY)
3. Check if retention period has passed
4. Warn if document is still within retention period
5. Advise on retention requirements

**Example:**
```
User: "When can I delete my Family Trust Election document?"
AI: "Family Trust Election Date: 2020-02-01"
    "Retention Period: 5 years from FTE date"
    "Retain Until: 2025-02-01"
    ""
    "⚠️  DO NOT DELETE before 2025-02-01"
    "ATO Requirement: Section 272-80 ITAA 1936"
    "Reason: FTE must be retained for 5 years from lodgment date"
    ""
    "Current Date: 2025-01-17"
    "Days Remaining: 15 days"
    ""
    "After 2025-02-01, you may safely delete this document"
```

---

### Taxonomy Update Workflow

**Triggers:**
- "Update taxonomies"
- "Sync taxonomies"
- "Check for taxonomy updates"
- "Apply new retention rules"

**Process:**
1. Compare current paperless-ngx state with YAML taxonomy definitions
2. Detect new tags, document types, and retention rule changes
3. Display changes for user review
4. Require explicit approval for retention period changes (compliance safety)
5. Apply updates atomically with rollback on failure
6. Log all changes for audit trail

**CLI Commands (MANDATORY - DO NOT bypass):**
```bash
# Check for available updates (safe, read-only)
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts check-updates --country Australia

# Apply updates WITHOUT retention changes (safe)
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts sync-taxonomies --country Australia

# Apply updates WITH retention changes (requires approval)
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts sync-taxonomies --country Australia --approve-retention-changes

# View taxonomy version history
bun run $PAI_DIR/skills/RecordsManager/Tools/RecordManager.ts diff-taxonomies
```

**Example:**
```
User: "Sync taxonomies for Australia"
AI: "Checking for taxonomy updates..."
    "Changes detected:"
    "  NEW TAGS:"
    "    • trust-documents (category: legal)"
    "    • beneficiary-declaration (category: trust)"
    "  NEW DOCUMENT TYPES:"
    "    • Family Trust Election"
    "    • Distribution Minutes"
    "  RETENTION CHANGES:"
    "    ⚠️  Tax Return: 5 years → 7 years (requires approval)"
    ""
    "Apply non-retention changes? (yes/no)"
    [User: yes]
    "✅ Applied 2 new tags, 2 new document types"
    ""
    "⚠️  Retention change requires explicit approval:"
    "    Tax Return: 5 years → 7 years"
    "    Reason: ATO requirement update (Section 262A ITAA 1936)"
    "    Impact: Affects 47 documents currently tagged 'tax-return'"
    ""
    "Type 'APPROVE' to apply retention changes:"
    [User: APPROVE]
    "✅ Applied retention changes"
    "📝 Logged to $PAI_HOME/MEMORY/RECORDSMANAGER/taxonomy-updates.jsonl"
```

**CRITICAL SAFEGUARDS:**
- **Single Source of Truth**: All taxonomies MUST come from `src/skills/RecordsManager/Config/taxonomies.yaml`
- **DO NOT invent tags** - Agents must NEVER suggest tags not in TaxonomyExpert
- **DO NOT bypass CLI** - Direct API calls or UI edits FORBIDDEN (breaks compliance)
- **Atomic transactions** - All changes rollback on failure
- **Audit trail** - All changes logged to MEMORY/RECORDSMANAGER/

**Why This Matters:**
Taxonomy changes affect compliance. Incorrect retention periods, invented tags, or bypassing the CLI can cause:
- Legal compliance violations (incorrect retention enforcement)
- Failed audits (tags without legal citations)
- Data inconsistency (documents tagged with undefined categories)
- Broken rollback (partial state if errors occur)

---

## Taxonomy Expert System

The TaxonomyExpert provides country-specific record keeping knowledge:

### Supported Countries

- **Australia** (default)
  - ATO tax record requirements
  - Australian Consumer Law retention
  - State-specific legal document retention
  - **NEW: Trust document requirements (unit, discretionary, family trusts)**

- **United States**
  - IRS tax record requirements
  - Federal and state retention guidelines
  - Industry-specific requirements

- **United Kingdom**
  - HMRC self-assessment requirements
  - FCA insurance documentation
  - Companies House records

### Entity Types

**Household:**
- Financial: Tax, bank statements, investments
- Medical: Records, receipts, insurance
- Insurance: Home, contents, vehicle, health, life
- Legal: Contracts, wills, powers of attorney
- Education: Transcripts, certificates
- Household: Utilities, warranties, manuals

**Corporate:**
- Financial: Invoices, receipts, expenses, revenue
- Legal: Contracts, agreements, licenses
- HR: Employee records, payroll, leave
- Compliance: Audit reports, certificates, permits
- Corporate: Board resolutions, shareholder records

**Trusts:**
- **Unit Trusts** (NEW)
  - Unit registry and ownership records
  - Trust deed and variations
  - Distribution statements
  - Unitholder agreements
  - ABN/TFN documentation

- **Discretionary Trusts** (NEW)
  - Trust deed and variations
  - **Trustee resolutions (pre-EOFY requirement)**
  - Distribution minutes documenting allocations
  - Beneficiary declarations
  - ABN/TFN documentation

- **Family Trusts** (NEW)
  - Trust deed and variations
  - **Family Trust Election (FTE)** - 5+ year retention from FTE date
  - Trustee resolutions (pre-EOFY)
  - Distribution minutes
  - Beneficiary declarations
  - ABN/TFN documentation

**Projects:**
- Planning: Project plans, proposals
- Deliverables: Outputs, artifacts
- Communications: Meeting notes, emails
- Documentation: Specs, requirements
- Lessons: Retrospectives, learnings

---

## Hierarchical Taxonomy System

The Records Manager now supports **hierarchical taxonomies** with a 4-level structure for precise document classification:

### Structure

**Level 1: Function** → **Level 2: Service** → **Level 3: Activity** → **Level 4: DocumentType**

```
HealthManagement/
├── MedicalCare/
│   ├── Consultations/
│   │   ├── Medical Receipt
│   │   ├── Referral Letter
│   │   └── Specialist Referral
│   ├── Prescriptions/
│   │   ├── Prescription
│   │   └── Medication Receipt
│   └── TestResults/
│       ├── Pathology Report
│       └── Imaging Report
└── DentalCare/
    └── Consultations/
        ├── Dental Invoice
        └── Treatment Plan
```

### TaxonomyExpert Methods

**Navigation Methods** (Function → Service → Activity → DocumentType):
```typescript
// Get all functions for an entity type
const functions = expert.getFunctions('household');
// Returns: [{ name: 'HealthManagement', keywords: [...], services: {...} }, ...]

// Get services for a function
const services = expert.getServices('household', 'HealthManagement');
// Returns: [{ name: 'MedicalCare', keywords: [...], activities: {...} }, ...]

// Get activities for a service
const activities = expert.getActivities('household', 'HealthManagement', 'MedicalCare');
// Returns: [{ name: 'Consultations', documentTypes: [...], retention: {...} }, ...]

// Get document types for an activity
const docTypes = expert.getDocumentTypesForActivity(
  'household',
  'HealthManagement',
  'MedicalCare',
  'Consultations'
);
// Returns: ['Medical Receipt', 'Referral Letter', 'Specialist Referral']

// Get retention rules for an activity
const retention = expert.getRetentionForActivity(
  'household',
  'HealthManagement',
  'MedicalCare',
  'Consultations'
);
// Returns: { AUS: { years: 7, authority: 'ATO requirement...' }, USA: { years: 6, ... } }
```

**Path Validation and Autocomplete:**
```typescript
// Validate a complete taxonomy path
const validation = expert.validatePath('household', 'HealthManagement/MedicalCare/Consultations');
// Returns: { valid: true, resolved: { function: 'HealthManagement', service: 'MedicalCare', activity: 'Consultations', documentTypes: [...], retention: {...} } }

// Autocomplete with fuzzy matching
const autocomplete = expert.autocomplete('household', 'health/med', { limit: 5 });
// Returns: { suggestions: ['HealthManagement/MedicalCare'], types: ['service'], remaining: 2 }

// Search by keyword
const results = expert.searchByKeyword('household', 'medical');
// Returns: [{ function: 'HealthManagement', service: 'MedicalCare', activity: 'Consultations', matchType: 'keyword', relevance: 7 }, ...]
```

**Tag and Path Generation:**
```typescript
// Generate hierarchical tags for paperless-ngx
const tags = expert.generateHierarchicalTags(
  'household',
  'HealthManagement',
  'MedicalCare',
  'Consultations'
);
// Returns: ['HealthManagement', 'MedicalCare', 'Consultations', 'medical', 'doctor', 'clinic']

// Generate storage path
const path = expert.generateStoragePath(
  'household',
  'HealthManagement',
  'MedicalCare',
  'Consultations'
);
// Returns: '/Household/Health Management/Medical Care/Consultations'
```

**Helper Methods:**
```typescript
// Get all document types across entire hierarchy (flat view)
const allDocTypes = expert.getAllDocumentTypes('household');
// Returns: ['Medical Receipt', 'Referral Letter', 'Tax Return', 'Invoice', ...]

// Check if hierarchical mode is available
if (expert.isHierarchicalAvailable()) {
  // Use hierarchical methods
} else {
  // Fall back to flat taxonomy
}

// Get current taxonomy mode
const mode = expert.getTaxonomyMode();
// Returns: 'hierarchical' | 'flat' | 'hybrid'
```

### Usage in Workflows

**Upload Workflow with Hierarchical Classification:**
```typescript
// User uploads a medical receipt
const expert = new TaxonomyExpert('AUS', 'household');

// Option 1: Let expert suggest from filename/content
const suggestion = expert.suggestMetadata('Medical-Receipt-DrSmith-2024.pdf');

// Option 2: Navigate hierarchy interactively
const functions = expert.getFunctions('household');
// User selects: HealthManagement

const services = expert.getServices('household', 'HealthManagement');
// User selects: MedicalCare

const activities = expert.getActivities('household', 'HealthManagement', 'MedicalCare');
// User selects: Consultations

const docTypes = expert.getDocumentTypesForActivity('household', 'HealthManagement', 'MedicalCare', 'Consultations');
// User selects: Medical Receipt

// Generate tags and path
const tags = expert.generateHierarchicalTags('household', 'HealthManagement', 'MedicalCare', 'Consultations');
const storagePath = expert.generateStoragePath('household', 'HealthManagement', 'MedicalCare', 'Consultations');

// Upload to paperless-ngx with hierarchical metadata
await client.uploadDocument(filePath, {
  tags: tags,
  document_type: 'Medical Receipt',
  storage_path: storagePath,
});
```

**Retention Checking with Hierarchical Rules:**
```typescript
// Check retention for specific activity
const retention = expert.getRetentionForActivity(
  'household',
  'HealthManagement',
  'MedicalCare',
  'Consultations'
);

console.log(`Keep for ${retention.AUS.years} years`);
console.log(`Legal basis: ${retention.AUS.authority}`);
```

### Benefits of Hierarchical Taxonomies

1. **Precision**: 4-level classification vs flat tags
2. **Discoverability**: Navigate by category, not search
3. **Consistency**: Structured paths enforce organization
4. **Scalability**: Add services/activities without tag explosion
5. **Compliance**: Retention rules at activity level

---

## Configuration

Required environment variables (set in `$PAI_DIR/.env`):

```bash
# Paperless-ngx connection
MADEINOZ_RECORDMANAGER_PAPERLESS_URL="https://paperless.example.com"
MADEINOZ_RECORDMANAGER_PAPERLESS_API_TOKEN="your-api-token-here"

# Records Manager settings
MADEINOZ_RECORDMANAGER_RECORDS_COUNTRY="Australia"  # Your country for compliance
MADEINOZ_RECORDMANAGER_RECORDS_DEFAULT_DOMAIN="household"  # household | corporate | projects
```

---

## Integration with Other Skills

### Works Well With

- **pai-brightdata-skill**: Fetch documents from web sources before uploading
- **pai-research-skill**: Investigate record keeping requirements for specific situations
- **pai-osint-skill**: Background research on document sources or parties

### NEW Capabilities

**Trust Document Management:**
- Validate trust document completeness against ATO requirements
- Track Family Trust Election retention (5 years from FTE date)
- Generate trustee resolution templates for pre-EOFY compliance
- Calculate trust distributions based on unit holdings
- Suggest tags for trust documents automatically

**Workflow Automation:**
- Analyze document patterns and recommend automated workflows
- Create paperless-ngx workflows for auto-tagging
- Review workflow effectiveness and match rates
- Test workflows before deployment
- Explain workflow architecture and matching logic

**Dynamic Entity Creation:**
- Add new entities anytime (household, corporate, trusts, projects)
- Interactive entity configuration with type-specific questions
- Automatic creation of tags, storage paths, and custom fields
- Entity registry for tracking all managed entities
- Support for unlimited entities per installation

### Use Cases

**Household Record Keeping:**
- Upload tax documents with automatic tagging
- Organize insurance policies by type and renewal date
- Find medical receipts for tax deductions
- Check retention before shredding old documents

**Corporate Compliance:**
- Ensure invoice retention meets tax requirements
- Tag contracts by department and expiration
- Organize employee records by retention period
- Audit trail for document deletions

**Project Management:**
- Organize project documents by phase
- Tag deliverables with project metadata
- Archive completed projects systematically
- Find related documents across projects

**Trust Management (NEW):**
- Set up family trust with entity tags and storage paths
- Validate trust document completeness before EOFY
- Check FTE retention compliance (5 years from FTE date)
- Generate trustee resolution templates
- Automate tagging of trust-related documents
- Create workflows for trust document classification

---

## Safety Principles

1. **Deletion is catastrophic** - Always requires explicit approval
2. **Retention is legal** - Country-specific requirements are authoritative
3. **Tags are permanent** - Well-tagged documents are findable documents
4. **Search is king** - Structure for finding, not just storing
5. **Compliance matters** - Retention rules have legal weight

---

## Troubleshooting

### Common Issues

**Problem:** "Country not supported, falling back to Australia"

**Solution:** Taxonomies available for Australia, United States, United Kingdom. For other countries, contribute your country's guidelines!

**Problem:** "Cannot reach paperless-ngx API"

**Solution:** Verify MADEINOZ_RECORDMANAGER_PAPERLESS_URL includes protocol (https://) and instance is running

**Problem:** "API authentication failed"

**Solution:** Regenerate API token in paperless-ngx with correct permissions

**Problem:** "No tags suggested"

**Solution:** Document type or filename may not match known patterns. Manually tag first few to build patterns.

---

## Credits

- **Original concept**: madeinoz67 - developed for personal document management
- **Taxonomy sources**: National archives of Australia, IRS, HMRC
- **Inspired by**: paperless-ngx community best practices

---

## Version History

### 1.2.0 (2026-01-20)
- **NEW:** `status` CLI command for comprehensive connection testing
- **NEW:** StatusCheck workflow for skill-based system verification
- **ENHANCED:** VERIFY.md with "check status" final verification step

### 1.0.0 (2025-01-17)
- **NEW:** TrustExpert with ATO-compliant trust management (unit, discretionary, family trusts)
- **NEW:** WorkflowExpert for paperless-ngx workflow automation and analysis
- **NEW:** EntityCreator for dynamic multi-entity support
- **ENHANCED:** PaperlessClient with correspondents, storage paths, custom fields, bulk operations
- **ENHANCED:** TaxonomyExpert with trust-specific document types and retention rules
- Multi-entity support (manage unlimited entities per installation)
- Interactive entity creation with type-specific configuration
- Automated workflow recommendations based on document patterns
- Trust document validation and compliance checking
- Initial release
- Paperless-ngx API integration
- Taxonomy expert for AU, US, UK
- Deletion confirmation workflow
- CLI tool with upload, search, organize, tag, info, retention commands
