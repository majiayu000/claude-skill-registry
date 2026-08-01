---
name: dataverse-schema-design
description: This skill provides guidance on designing Dataverse table schemas and
  data models. Use when users ask about "Dataverse table design", "Dataverse schema",
  "Dataverse relationships", "Dataverse columns", "data modeling Dataverse", "Dataverse
  best practices", or need help designing their data structure.
---

# dataverse-schema-design

This skill provides guidance on designing Dataverse table schemas and data models. Use when users ask about "Dataverse table design", "Dataverse schema", "Dataverse relationships", "Dataverse columns", "data modeling Dataverse", "Dataverse best practices", or need help designing their data structure.

## Table Design Fundamentals

### Naming Conventions
- **Table prefix**: Use publisher prefix (e.g., `new_`, `cr123_`)
- **Table names**: PascalCase, singular (e.g., `new_Project`, `new_Task`)
- **Column names**: prefix_columnname (e.g., `new_projectname`, `new_startdate`)

### Create Table with SDK
```python
# Basic table
client.create_table("new_Project", {
    "new_ProjectName": "string",      # Text column
    "new_Description": "string",       # Multi-line text
    "new_Budget": "decimal",           # Currency/decimal
    "new_StartDate": "datetime",       # Date and time
    "new_IsActive": "bool",            # Yes/No
    "new_Priority": Priority           # Choice/enum
})
```

## Column Types

### Text Columns
```python
# Single line (max 4000 chars)
"new_Name": "string"

# Multi-line text (memo)
"new_Description": "string"  # Will be nvarchar(max)
```

### Number Columns
```python
# Integer
"new_Quantity": "int"

# Decimal (with precision)
"new_Amount": "decimal"  # Default precision

# Currency (use decimal with formatting)
"new_Budget": "decimal"
```

### Date/Time Columns
```python
# Date and time
"new_StartDate": "datetime"

# Date only (format in app)
"new_DueDate": "datetime"
```

### Boolean Columns
```python
# Yes/No
"new_IsActive": "bool"
"new_IsApproved": "bool"
```

### Choice (Picklist) Columns
```python
from enum import IntEnum

class Status(IntEnum):
    DRAFT = 1
    SUBMITTED = 2
    APPROVED = 3
    REJECTED = 4

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Create table with choices
client.create_table("new_Request", {
    "new_Name": "string",
    "new_Status": Status,
    "new_Priority": Priority
})
```

## Relationship Patterns

### One-to-Many (1:N)
Parent table has many child records.

```
Account (1) ←→ (N) Contact
└── An account has many contacts

Project (1) ←→ (N) Task
└── A project has many tasks
```

**Implementation:**
- Create lookup column on child table
- Reference parent using `@odata.bind`

```python
# Create contact linked to account
contact = {
    "firstname": "John",
    "lastname": "Doe",
    "parentcustomerid_account@odata.bind": f"/accounts({account_id})"
}
client.create("contact", contact)
```

### Many-to-Many (N:N)
Records in both tables can relate to multiple records in the other.

```
Account (N) ←→ (N) Contact
└── Contacts can be related to multiple accounts
```

**Note:** N:N relationships require creating an intersection entity via the UI or advanced API calls.

### Self-Referential
Table references itself (e.g., employee hierarchy).

```
Employee
├── new_ManagerId → Employee
└── Parent employee record
```

## Schema Design Best Practices

### Do's
1. **Plan before creating** - Design schema on paper first
2. **Use meaningful names** - Clear, descriptive column names
3. **Add descriptions** - Document purpose of each column
4. **Set required fields** - Enforce data quality
5. **Use appropriate types** - Don't store numbers as text
6. **Create indexes** - On frequently filtered columns
7. **Use lookups** - Instead of duplicating data

### Don'ts
1. **Don't over-normalize** - Balance between normalization and performance
2. **Don't use reserved names** - Avoid system column names
3. **Don't create wide tables** - Split into related tables if >100 columns
4. **Don't store calculated data** - Use calculated columns instead
5. **Don't ignore security** - Plan field-level security early

## Common Schema Patterns

### Master-Detail
```
Account (Master)
├── new_AccountNumber
├── new_Name
└── Contacts (Detail)
    ├── new_FirstName
    ├── new_LastName
    └── _parentcustomerid_value (FK)
```

### Status Workflow
```
new_Request
├── new_Name
├── new_Status (Draft → Submitted → Approved/Rejected)
├── new_SubmittedOn
├── new_ApprovedBy
└── new_ApprovedOn
```

### Audit Trail
```
new_Order
├── new_OrderNumber
├── new_Status
├── createdon (system)
├── createdby (system)
├── modifiedon (system)
└── modifiedby (system)
```

## Adding Columns to Existing Tables

```python
# Add new columns
client.create_columns("new_Project", {
    "new_CompletionPercentage": "int",
    "new_ActualEndDate": "datetime"
})

# Remove columns
client.delete_columns("new_Project", ["new_OldColumn"])
```

## References

- See `references/table-design.md` for detailed patterns
- See `references/relationships.md` for relationship examples
- See `references/performance.md` for optimization tips
