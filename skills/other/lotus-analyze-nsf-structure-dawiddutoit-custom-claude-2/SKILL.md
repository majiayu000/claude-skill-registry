---
name: lotus-analyze-nsf-structure
description: |
  Analyzes Lotus Notes NSF database file structure, data models, views, forms, and relationships.
  Use when understanding NSF database composition, mapping field structures, identifying data dependencies,
  extracting schema information, or assessing data migration scope.
allowed-tools:
  - Read
  - Bash
  - Grep
---

Works with NSF file metadata analysis, view/form specifications, field type mappings, and database relationship documentation.
# Analyze Lotus Notes NSF Structure

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#examples)

**How to Implement** → [Step-by-Step](#instructions) | [Expected Outcomes](#quick-start)

**Reference** → [Requirements](#requirements) | [Related Skills](#see-also)

## Purpose

This skill helps you reverse-engineer and document Lotus Notes NSF database structures. NSF (Lotus Notes Storage Format) files contain complex nested structures with views, forms, fields, and relationships that must be understood before migration. This skill guides you through systematic analysis of these structures to create accurate migration maps.

## When to Use

Use this skill when you need to:

- **Understand NSF database composition** - Reverse-engineer forms, views, and field structures
- **Map field structures** - Document field types, validation rules, and computed formulas
- **Identify data dependencies** - Discover relationships between forms and databases
- **Extract schema information** - Create migration maps for target system design
- **Assess migration scope** - Determine complexity and effort for NSF database migration
- **Document legacy systems** - Create comprehensive documentation of Notes database structures

This skill is essential for any Lotus Notes migration project as it provides the foundation for understanding what data and structures need to be migrated.

## Quick Start

To analyze an NSF database structure:

1. Gather NSF file metadata or documentation (design notes, database properties)
2. Map the data model: identify forms, fields, and field types
3. Document views: list views, selection criteria, column definitions
4. Identify relationships: reference fields, lookup tables, embedded databases
5. Create a migration map linking NSF structures to target system equivalents

## Instructions

### Step 1: Extract NSF File Properties

Locate NSF documentation or design information:
- Database title and description
- Creation date and last modified date
- Database type (standard application, template, reference database)
- Replica ID (indicates database copies/replication)
- Access control list (ACL) structure

*Note: Direct NSF parsing requires specialized tools. If you have NSF files, extract metadata via Lotus Notes Designer or Domino API documentation.*

**Check for:**
- `.CLF` index files accompanying NSF files
- Database design notes in Domino documentation
- Schema exports from Lotus Notes Design elements

### Step 2: Map Forms and Fields

Document all forms in the NSF database:

For each form, record:
- Form name and internal name
- Form purpose (document type)
- All fields with:
  - Field name (API name)
  - Display name
  - Field type (Text, Number, DateTime, RichText, Reference, Computed, Formula)
  - Field length/constraints
  - Computed formula (if applicable)
  - Default values
  - Validation rules

Create a structured mapping:

```
Form: "Order"
  Fields:
    - OrderID (Text, 20 chars, Unique key)
    - OrderDate (DateTime, Required)
    - Supplier (Reference → SupplierDatabase.Supplier form)
    - Items (RichText, embedded table)
    - Status (Text, dropdown: Draft/Approved/Shipped)
    - CalculatedAmount (Number, Formula: Sum(Items[*].Amount))
```

### Step 3: Document Views and Selection Criteria

For each view in the database:

- View name and hierarchy (category)
- Selection formula (what documents appear)
- Columns displayed with sort order and grouping
- Access restrictions
- Specialized view types (calendar, timeline, etc.)

Example view documentation:

```
View: "Orders by Supplier"
  Selection: SELECT @IsAvailable(Supplier)
  Columns:
    - Supplier (grouped, sorted A-Z)
    - OrderDate (sorted descending)
    - OrderID (unique key)
    - Status
  Access: All users can read
```

### Step 4: Identify Data Relationships

Map dependencies between forms and databases:

- **Reference fields**: Fields that link to other documents
  - Source form/field
  - Target database and form
  - Is link bidirectional?
  - How are orphaned references handled?

- **Embedded databases**: Are smaller databases embedded in documents?
  - Location (main document or response documents)
  - Structure of embedded data

- **External lookups**: Do formulas reference external databases?
  - Which databases are queried
  - Lookup key and result fields
  - Caching strategy

Document as relationship graph:

```
Order form
  ├─ Supplier reference → SupplierDatabase.Supplier
  │   └─ Used for: Name lookup, discount calculation
  ├─ Items (embedded table)
  │   └─ Each row has: ItemCode (ref to Catalog), Quantity, Price
  └─ Approver (reference) → StaffDatabase.Employee
```

### Step 5: Create Migration Mapping

For each NSF structure element, define the target system equivalent:

```
NSF Structure              → Target System Pattern
─────────────────────────   ───────────────────────
Form: Order               → Entity: Order (database table/model)
Field: OrderID (unique)   → Column: order_id (primary key)
Field: Supplier (ref)     → Column: supplier_id (foreign key)
Field: Items (embedded)   → Related table: OrderItems (one-to-many)
View: Orders by Supplier  → Query/API: GET /orders?supplier={id}
RichText field            → Column: description (text/html)
Computed field            → Derived property or trigger
```

### Step 6: Document Special Patterns

Note migration-specific considerations:

- **Rich Text fields**: How much formatting is required post-migration?
  - Plain text extraction vs. HTML/markdown conversion
  - Embedded images, attachments handling

- **Replication fields**: Are Replica IDs, DocumentUNID, or similar critical?
  - Do audit trails require preserving creation/modification metadata?

- **Variable Reference Substitution (VRS)**: Any fields use VRS patterns?
  - Document which fields are affected
  - Map VRS substitutions to target system config

- **Workflow/automation**: Are any computed fields or validation formulas critical logic?
  - Can they be converted to database triggers, stored procedures, or API logic?

## Examples

### Example 1: Simple Reference Database Structure

```
Database: Supplier Master
Forms:
  - Supplier (main form)
    Fields: SupplierID, Name, Contact, Status, Terms
Views:
  - All Suppliers (SELECT @IsAvailable(SupplierID))
  - Active Only (SELECT Status = "Active")
  - By Category (grouped by SupplierCategory)

Migration:
  → Table: suppliers (columns: id, name, contact, status, terms)
  → API endpoints: GET /suppliers, GET /suppliers/{id}
  → Indexes: suppliers(status), suppliers(supplier_category)
```

### Example 2: Complex Application with Embedded Data

```
Database: Order Management
Forms:
  - Order (main form)
    Fields:
      - OrderID (unique key, Text)
      - OrderDate (DateTime)
      - Supplier (Reference → Supplier form in SupplierMaster)
      - Status (computed: if(ApprovedDate > "", "Approved", "Draft"))
      - Items (embedded table with columns: ItemCode, Qty, Price)
      - Notes (RichText)

Views:
  - Orders Pending (SELECT Status = "Draft")
  - Orders by Supplier (grouped by Supplier, sorted by OrderDate desc)

Migration:
  → Table: orders (id, order_date, supplier_id, status, notes_html)
  → Table: order_items (order_id, item_code, quantity, price)
  → Foreign key: orders.supplier_id → suppliers.id
  → View query: SELECT * FROM orders WHERE status='Draft' ORDER BY order_date DESC
  → Rich text conversion: Apply HTML converter to notes field
```

## Requirements

- **Lotus Notes Design Documentation**: Access to NSF database design specifications
  - Can be obtained from Lotus Notes Designer or Domino Server
  - Export as design notes or documentation files

- **Project Context**: Understanding of source and target systems
  - What data is critical for migration?
  - Which fields can be transformed vs. which must be preserved as-is?

- **Optional Tools**: For deep NSF analysis
  - Domino Designer (for live NSF inspection)
  - NSF analysis scripts (if available in your environment)
  - Previous migration documentation from similar projects

## See Also

- [lotus-migration](../lotus-migration/SKILL.md) - Comprehensive Lotus Notes to new system migration overview
- [lotus-replace-odbc-direct-writes](../lotus-replace-odbc-direct-writes/SKILL.md) - Replacing ODBC direct database access with API patterns
- [lotus-convert-rich-text-fields](../lotus-convert-rich-text-fields/SKILL.md) - Converting rich text formatting to standard formats
