---
name: meeting-schema-validation
description: Use when processing meeting transcripts - validates YAML frontmatter has required fields (date, type, customer, participants) and proper naming convention
allowed-tools: Read, Grep
---

# Meeting Schema Validation

## Purpose

Ensure all meeting transcripts maintain consistent schema for:
- Reliable meeting synthesis
- Accurate customer attribution
- Proper temporal filtering
- Searchable meeting archives

## When to Use This Skill

Activate automatically when:
- Processing new meeting transcripts
- `meeting-synthesis` skill loads meeting files
- User adds meetings to `datasets/meetings/`
- Validating meeting data integrity
- Any workflow depends on meeting transcript structure

## Required Schema

### YAML Frontmatter Requirements

**All meetings must begin with:**

```yaml
---
date: "YYYY-MM-DD"
type: "sales" | "product" | "customersuccess" | "onboarding" | "strategy" | "ops" | "marketing" | "general"
customer: "Company Name"  # Primary customer/company
companies: ["Company A", "Company B"]  # All companies involved
participants: ["Person Name", "Another Person"]
granola_folder: "Sales" | "Product" | "CustomerSuccess" | etc.
granola_url: "https://app.granola.so/notes/..."
meeting_note_id: "uuid-format-string"
tags: ["2025Q3", "keyword", "topic"]
---
```

**Required fields:**
- `date`: ISO format YYYY-MM-DD
- `type`: One of the defined meeting types
- `customer`: Primary customer/company name
- `companies`: Array of all involved companies
- `participants`: Array of participant names

**Optional but recommended:**
- `granola_folder`: Source folder (for tracking)
- `granola_url`: Link to original notes
- `meeting_note_id`: Unique identifier (UUID)
- `tags`: Searchable keywords and quarters

### File Naming Convention

**Required format:**
```
YYYY-MM-DD_{type}_{titleSlug}_{companyOrFunctionSlug}_{participantsSlug}.md
```

**Examples:**
```
2025-10-15_sales_discovery-call_prettyboy_jenna-mike.md
2025-10-14_product_feature-planning_internal_jay-sarah.md
2025-10-13_customersuccess_qbr_compoundstudio_alex.md
```

**Components:**
1. `YYYY-MM-DD`: Meeting date (matches frontmatter `date` field)
2. `{type}`: Meeting type (matches frontmatter `type` field)
3. `{titleSlug}`: Kebab-case title describing meeting topic
4. `{companyOrFunctionSlug}`: Company name or internal function (kebab-case)
5. `{participantsSlug}`: Key participants (kebab-case, abbreviated)

### Required Content Sections

**All meetings must contain these sections:**

```markdown
## ⬇️ AI Summary
[Executive summary of key points and outcomes]

## ⬇️ Action Items
- [ ] Action item 1
- [ ] Action item 2

## ⬇️ Full Transcript
[Raw transcript or detailed notes]

## ⬇️ Links
- [Link to related resource]
```

**Section order is standardized** (aids parsing and synthesis)

### Directory Structure

**Meetings organized by:**
```
datasets/meetings/
├── Customers/
│   └── {CustomerName}/
│       └── {YYYY}/
│           └── MM-DD_{type}_{title}_{customer}_{participants}.md
└── Internal/
    └── {Function}/  # Product, CS, Sales, Marketing, Ops
        └── {YYYY}/
            └── MM-DD_{type}_{title}_{function}_{participants}.md
```

**Examples:**
```
datasets/meetings/Customers/PrettyBoy/2025/10-15_sales_discovery-call_prettyboy_jenna-mike.md
datasets/meetings/Internal/Product/2025/10-14_product_feature-planning_internal_jay-sarah.md
```

## Validation Process

### 1. Load Meeting File

Read meeting from:
- `datasets/meetings/Customers/{Customer}/{YYYY}/{filename}.md`, OR
- `datasets/meetings/Internal/{Function}/{YYYY}/{filename}.md`

### 2. Validate YAML Frontmatter

**Check required fields exist:**
```
✓ date present and format YYYY-MM-DD?
✓ type present and valid value?
✓ customer present (non-empty string)?
✓ companies present and array?
✓ participants present and array?
```

**Validate field formats:**
- `date`: Regex `^\d{4}-\d{2}-\d{2}$`
- `type`: Must be one of: sales, product, customersuccess, onboarding, strategy, ops, marketing, general
- `customer`: Non-empty string
- `companies`: Array with at least one entry
- `participants`: Array with at least one entry
- `tags`: Array (if present)
- `meeting_note_id`: UUID format (if present)
- `granola_url`: Valid URL (if present)

### 3. Validate File Naming

**Extract components from filename:**
```regex
^(\d{4}-\d{2}-\d{2})_([a-z]+)_([a-z0-9-]+)_([a-z0-9-]+)_([a-z0-9-]+)\.md$
```

**Validate consistency:**
- Date in filename matches frontmatter `date`?
- Type in filename matches frontmatter `type`?
- Filename uses kebab-case throughout?
- Filename follows YYYY-MM-DD prefix pattern?

### 4. Validate Content Sections

**Check required sections exist:**
```
✓ ## ⬇️ AI Summary
✓ ## ⬇️ Action Items
✓ ## ⬇️ Full Transcript
✓ ## ⬇️ Links
```

**Validation method:**
```bash
grep -q "## ⬇️ AI Summary" meeting.md
grep -q "## ⬇️ Action Items" meeting.md
grep -q "## ⬇️ Full Transcript" meeting.md
grep -q "## ⬇️ Links" meeting.md
```

### 5. Validate Directory Placement

**Check file is in correct directory:**
- Customer meetings → `datasets/meetings/Customers/{CustomerName}/{YYYY}/`
- Internal meetings → `datasets/meetings/Internal/{Function}/{YYYY}/`

**Consistency checks:**
- Directory customer name matches frontmatter `customer`?
- Directory year matches frontmatter `date` year?
- Directory function matches meeting context (for internal meetings)?

### 6. Generate Report

**If all pass:**
```markdown
# Meeting Schema Validation: PASS

**File**: 2025-10-15_sales_discovery-call_prettyboy_jenna-mike.md

✓ YAML frontmatter complete: All required fields present
✓ Field formats valid:
  - date: 2025-10-15 (valid ISO format)
  - type: sales (valid type)
  - customer: PrettyBoy (present)
  - companies: ["PrettyBoy"] (array, 1 entry)
  - participants: ["Jenna Smith", "Mike Johnson"] (array, 2 entries)
✓ Filename format valid: YYYY-MM-DD_{type}_{title}_{customer}_{participants}.md
✓ Filename consistency: Date and type match frontmatter
✓ Required sections present: AI Summary, Action Items, Full Transcript, Links
✓ Directory placement valid: Customers/PrettyBoy/2025/

**Status**: Meeting schema validated
```

**If any fail:**
```markdown
# Meeting Schema Validation: FAIL

**File**: 2025-10-15_discovery_prettyboy.md

✗ YAML frontmatter incomplete:
  - Missing field: `participants`
  - Missing field: `companies`

✗ Filename format invalid:
  - Expected: YYYY-MM-DD_{type}_{title}_{customer}_{participants}.md
  - Actual: 2025-10-15_discovery_prettyboy.md
  - Missing: {participants} component

✗ Required sections missing:
  - Missing: ## ⬇️ Action Items

✗ Directory placement incorrect:
  - File location: datasets/meetings/2025-10-15_discovery_prettyboy.md
  - Expected: datasets/meetings/Customers/PrettyBoy/2025/

**Required fixes**:
1. Add missing frontmatter fields: participants, companies
2. Rename file to include all components
3. Add missing section: ## ⬇️ Action Items
4. Move file to correct directory: Customers/PrettyBoy/2025/

**Status**: NEEDS_FIX
```

### 7. Block or Approve

**If PASS:**
- Meeting can be used in synthesis workflows
- Schema integrity confirmed
- Ready for processing

**If FAIL:**
- Meeting blocked from synthesis
- Workflows depending on this meeting flagged
- Must address violations before use

## Integration with Workflows

### Meeting Synthesis Integration

**Invoked by:**
- `meeting-synthesis` skill (before processing meetings)
- `product-planning` workflow (validates meetings in time window)
- `cs-prep` workflow (validates customer meeting collection)

**Blocking behavior:**
- If schema validation fails → meeting skipped from synthesis
- User notified of schema violations
- Invalid meetings logged for manual review

### Manual Validation

**Direct usage:**
User can validate existing meetings:
```
"Validate meeting schema for datasets/meetings/Customers/PrettyBoy/2025/10-15_sales_discovery-call_prettyboy_jenna-mike.md"
```

## Auto-Correction

**For minor issues, offer auto-correction:**

**Correctable issues:**
- Missing `companies` array: Auto-populate from `customer` field
- Missing `tags` array: Auto-generate from `date` (e.g., "2025Q3") and `type`
- Incorrect directory: Suggest correct path and offer to move

**Non-correctable issues:**
- Missing required fields (`date`, `type`, `customer`, `participants`)
- Invalid field formats
- Missing required sections
→ These require manual fixes

## Success Criteria

Meeting schema validated when:
- All required frontmatter fields present and valid
- Filename follows naming convention
- Filename consistent with frontmatter
- All required sections present
- File in correct directory
- Validation report shows PASS status

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `participants` field | Add array of participant names |
| Invalid `type` value | Use one of defined types (sales, product, etc.) |
| Date format "10/15/2025" | Use ISO format: "2025-10-15" |
| Filename missing components | Include all: date_type_title_customer_participants |
| Wrong directory | Move to Customers/{Name}/{YYYY}/ or Internal/{Function}/{YYYY}/ |

## Related Skills

- **meeting-synthesis**: Uses validated meetings for signal extraction
- **source-integrity**: Complementary validation for other source types
- **product-planning**: Depends on valid meeting schema

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|----------------|---------|
| "Missing field is optional" | Required fields are mandatory. |
| "Close enough" on naming | Follow convention exactly. |
| "Will fix schema later" | Fix now or skip from synthesis. |
| "Manual meetings don't need schema" | All meetings follow schema. |
