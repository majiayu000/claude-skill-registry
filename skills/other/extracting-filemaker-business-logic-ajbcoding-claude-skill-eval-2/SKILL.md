---
name: extracting-filemaker-business-logic
description: Use when analyzing FileMaker DDR to extract calculations, custom functions, and business logic for PostgreSQL import processes or maintenance scripts - focuses on understanding and adapting FileMaker logic rather than direct schema migration
---

# Extracting FileMaker Business Logic

## Overview

FileMaker DDR reports contain calculation fields, custom functions, and business logic embedded in scripts. This skill helps you extract, understand, and adapt that logic for PostgreSQL implementations—typically for import processes, data transformations, and maintenance scripts.

**Key principle**: PostgreSQL implementations will often be more efficient than direct translations. Use FileMaker logic to understand *what* the business rules are, then implement them idiomatically in PostgreSQL.

## When to Use

Use this skill when:
- Extracting calculation logic from FileMaker DDR for import scripts
- Understanding business rules embedded in FileMaker calculations
- Adapting FileMaker custom functions to PostgreSQL functions
- Creating PostgreSQL maintenance scripts based on FileMaker script logic
- Documenting business logic that exists only in FileMaker

Do NOT use for:
- Direct 1:1 database migration (most PostgreSQL designs will differ)
- FileMaker UI/layout logic (not relevant to PostgreSQL)
- Simple field mappings (use standard ETL tools)

## DDR Files and Structure

**Detailed DDR**: `{ProjectName}_ddr/{DatabaseName}.html` (5-20MB file)
- Contains complete calculation formulas
- Lists all custom functions with code
- Documents scripts step-by-step
- Shows field definitions and relationships

**Example from user's project**:
- File: `/Users/anthonybyrnes/PycharmProjects/Python419/AugustServer_ddr/AugustServer.html`
- Size: 9.7MB
- Contains: 148 custom functions, 362 scripts, calculation fields

## Finding Calculations in DDR

### Calculation Fields

In DDR HTML, calculation fields appear in field definitions:

```
Field Name: wtu_calculation
Type: Calculation
Result Type: Number
Formula:
  contacthours * units * csfactor
```

**XPath pattern** (adjust based on actual DDR structure):
```python
from lxml import etree

tree = etree.parse("AugustServer_ddr/AugustServer.html", etree.HTMLParser())

# Find calculation fields
calc_fields = tree.xpath('//td[contains(text(), "Calculation")]/parent::tr')

for field_row in calc_fields:
    field_name = field_row.xpath('./td[1]/text()')[0]
    formula = field_row.xpath('./following-sibling::tr//text()')
```

### Scripts (Critical Source of Business Logic)

**Important**: Many "calculated" values are actually set by FileMaker scripts, not calculation fields. Scripts often contain the most complex business logic.

**Look for scripts that**:
- SetField steps (e.g., "Set Field [ClassInstance::wtu; ...]")
- Loop through records performing calculations
- Names containing "Calculate", "Update", "Process", "Compute"
- Triggered by imports or scheduled tasks

**Example**: The WTU field may appear as a Number field (not Calculation), but scripts like "419F - Loop WTU Contact Hours" contain the actual calculation logic.

```
Script: 419F - Loop WTU Contact Hours - c courses
Steps:
  If [Units ≠ "-"]
    Set Field [ClassInstance::wtu; ACCU * Workload_Weight_Factor]
    Set Field [ClassInstance::contactHours; ACCU * contact_hours_per_unit]
  End If
```

**Extraction tip**: Search DDR for field names (e.g., "wtu") to find all scripts that reference them.

### Custom Functions

Custom functions section (anchor: `#valCustomFunctionsSectionAnchor_`):

```
Function Name: GenerateUUID
Parameters: none
Formula:
  Upper(Get(UUID))
```

Look for patterns in custom function names:
- Prefix conventions (e.g., `CF_`, `Calc_`)
- Purpose indicators (`Validate_`, `Format_`, `Calculate_`)

## Understanding FileMaker Calculation Syntax

### Common FileMaker Functions → PostgreSQL Equivalents

| FileMaker | PostgreSQL | Notes |
|-----------|------------|-------|
| `Get(UUID)` | `gen_random_uuid()` or `uuid_generate_v4()` | FileMaker UUIDs are uppercase |
| `Upper(text)` | `UPPER(text)` | Direct equivalent |
| `Left(text, n)` | `LEFT(text, n)` | Direct equivalent |
| `Right(text, n)` | `RIGHT(text, n)` | Direct equivalent |
| `Position(search, text, start, occurrence)` | `POSITION(search IN text)` | PostgreSQL simpler, use SUBSTRING for start/occurrence |
| `Substitute(text, search, replace)` | `REPLACE(text, search, replace)` | Direct equivalent |
| `Let([var1 = value; var2 = value]; expression)` | `WITH vars AS (...)` or function variables | FileMaker's scoped variables |
| `Case(test1; result1; test2; result2; default)` | `CASE WHEN test1 THEN result1 WHEN test2 THEN result2 ELSE default END` | Similar structure |
| `If(test; trueResult; falseResult)` | `CASE WHEN test THEN trueResult ELSE falseResult END` | Or use `IF` in PL/pgSQL |
| `GetField(fieldName)` | Dynamic SQL or CASE statement | FileMaker allows dynamic field references |
| `Count(relationship::field)` | `SELECT COUNT(*) FROM related_table WHERE...` | Relationship counts become subqueries |
| `Sum(relationship::field)` | `SELECT SUM(field) FROM related_table WHERE...` | Aggregate from related table |

### FileMaker Operators

- `&` (concatenation) → `||` in PostgreSQL
- `≠` or `!=` → `<>` or `!=` in PostgreSQL
- `and`, `or`, `not` → `AND`, `OR`, `NOT` in PostgreSQL
- `¶` (paragraph return) → `E'\n'` in PostgreSQL

## Extraction Workflow

### Step 1: Identify Business Logic Locations

Scan DDR for (in priority order):
- [ ] **Scripts that manipulate data** (SetField, Loop, calculations) - often the PRIMARY source
- [ ] Calculation fields in tables you're importing
- [ ] Custom functions referenced by calculations/scripts
- [ ] Auto-enter calculations (default values with logic)
- [ ] Validation calculations (field constraints)

**Critical**: Check scripts FIRST. Many fields appear as "Number" or "Text" but are actually calculated by scripts.

### Step 2: Document Calculation Purpose

For each calculation field:
```markdown
**Field**: ClassInstance.wtu
**Purpose**: Calculate weighted teaching units for workload reporting
**Formula**: `contacthours * units * csfactor`
**Dependencies**: contacthours, units, csfactor fields
**Used by**: WTU reports, faculty workload calculations
**Implementation**: PostgreSQL VIEW or calculated during import
```

### Step 3: Adapt to PostgreSQL Idioms

**FileMaker approach** (calculation field):
```
// FileMaker calculation field
Case(
  enrollment_total = 0; "Empty";
  enrollment_total < class_capacity * 0.5; "Low";
  enrollment_total >= class_capacity; "Full";
  "Adequate"
)
```

**PostgreSQL approach** (CASE expression in VIEW):
```sql
CREATE OR REPLACE VIEW class_status AS
SELECT
  id,
  class_nbr,
  CASE
    WHEN enrollment_total = 0 THEN 'Empty'
    WHEN enrollment_total < class_capacity * 0.5 THEN 'Low'
    WHEN enrollment_total >= class_capacity THEN 'Full'
    ELSE 'Adequate'
  END AS status
FROM classinstance;
```

**Or as import script logic** (Python):
```python
def calculate_class_status(enrollment_total, class_capacity):
    """Adapted from FileMaker ClassInstance.status calculation"""
    if enrollment_total == 0:
        return 'Empty'
    elif enrollment_total < class_capacity * 0.5:
        return 'Low'
    elif enrollment_total >= class_capacity:
        return 'Full'
    else:
        return 'Adequate'

# Use during import
cursor.execute("""
    UPDATE classinstance
    SET enrollment_status = %s
    WHERE id = %s
""", (calculate_class_status(row['enrollment_total'], row['class_capacity']), row['id']))
```

### Step 4: Handle Custom Functions

**FileMaker custom function**:
```
Function: GenerateUUID
Parameters: none
Code:
  Upper(Get(UUID))
```

**PostgreSQL equivalent** (in existing codebase pattern):
```python
def generate_uuid():
    """Generate uppercase UUID matching FileMaker format"""
    return str(uuid.uuid4()).upper()
```

Reference: `program_catalog_parser.py:116-120`

## Common Patterns

### Pattern 1: Aggregates from Relationships

**FileMaker**:
```
// Count related records
Count(ClassAssign::id)

// Sum from related table
Sum(Enrollment::units)
```

**PostgreSQL** (import script):
```python
# Calculate during import
cursor.execute("""
    SELECT COUNT(*)
    FROM classassign
    WHERE id_classinstance = %s
""", (classinstance_id,))
assign_count = cursor.fetchone()[0]

# Or as a VIEW
CREATE VIEW classinstance_summary AS
SELECT
    ci.id,
    COUNT(ca.id) as assignment_count,
    SUM(e.units) as total_enrollment_units
FROM classinstance ci
LEFT JOIN classassign ca ON ca.id_classinstance = ci.id
LEFT JOIN enrollment e ON e.id_classinstance = ci.id
GROUP BY ci.id;
```

### Pattern 2: Conditional Logic

**FileMaker**:
```
Let([
  base = contacthours * units;
  factor = Case(
    component = "LAB"; 1.5;
    component = "LEC"; 1.0;
    1.0
  )
];
  base * factor
)
```

**PostgreSQL function**:
```sql
CREATE OR REPLACE FUNCTION calculate_wtu(
    contact_hours NUMERIC,
    units NUMERIC,
    component_type TEXT
) RETURNS NUMERIC AS $$
DECLARE
    base NUMERIC;
    factor NUMERIC;
BEGIN
    base := contact_hours * units;

    factor := CASE component_type
        WHEN 'LAB' THEN 1.5
        WHEN 'LEC' THEN 1.0
        ELSE 1.0
    END;

    RETURN base * factor;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

### Pattern 3: Text Parsing/Formatting

**FileMaker**:
```
// Extract course code from title
Let([
  spacePos = Position(" "; course_title; 1; 1)
];
  Left(course_title; spacePos - 1)
)
```

**PostgreSQL** (import script):
```python
def extract_course_code(course_title):
    """Extract course code from title (FileMaker logic)"""
    space_pos = course_title.find(' ')
    if space_pos > 0:
        return course_title[:space_pos]
    return course_title

# Or SQL function
CREATE OR REPLACE FUNCTION extract_course_code(course_title TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN SPLIT_PART(course_title, ' ', 1);
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

## Script Logic Extraction

FileMaker scripts often contain:
- **Data transformation logic** → PostgreSQL functions or Python import scripts
- **Validation rules** → CHECK constraints or application validation
- **Business workflows** → Application layer logic
- **UI automation** → Ignore for PostgreSQL

**Focus on extracting**:
- SetField steps (data updates)
- If/Else logic (conditional rules)
- Loop structures (batch processing)
- Calculation expressions used in scripts

## Integration with Import Processes

When building import scripts:

```python
# Reference: program_catalog_parser.py patterns

def process_catalog_entry(row, catalog_year):
    """
    Process catalog entry with business logic adapted from FileMaker.

    FileMaker calculation: catalog_year format "2024-2025"
    FileMaker custom function: ConvertToAY("2024-2025") → "24-25"
    """
    # Adapt FileMaker's year conversion logic
    ay_short = catalog_year[2:4] + '-' + catalog_year[7:9]

    # Get AY record (FileMaker relationship equivalent)
    cursor.execute("SELECT id FROM ay WHERE ay = %s", (ay_short,))
    id_ay = cursor.fetchone()[0]

    # Apply business rule (from FileMaker calculation)
    if row['total_units'] is None:
        # FileMaker: If(IsEmpty(total_units); Calculate_Default_Units; total_units)
        total_units = calculate_default_units(row)
    else:
        total_units = row['total_units']

    return {
        'id_ay': id_ay,
        'total_units': total_units,
        # ... other fields
    }
```

## Common Mistakes

**Mistake 1: Literal Translation**
- Don't translate FileMaker calculations character-by-character
- Understand the business rule, then implement idiomatically in PostgreSQL

**Mistake 2: Ignoring Context**
- Calculation fields may reference global fields or UI state
- Determine if logic is data-based (extract) or UI-based (ignore)

**Mistake 3: Missing Dependencies**
- Custom functions may call other custom functions
- Extract the full dependency chain

**Mistake 4: Over-Engineering**
- Simple calculations don't need PostgreSQL functions
- Calculate during import if logic is only used once

**Mistake 5: Skipping Documentation**
- Document the business purpose, not just the formula
- Future maintainers need to understand *why*, not just *what*

**Mistake 6: Only Checking Calculation Fields**
- Scripts often contain the primary business logic
- Check SetField steps in scripts for complex calculations
- A "Number" field type doesn't mean it's not calculated

## Common Rationalizations to Avoid

| Rationalization | Reality |
|-----------------|---------|
| "The field is type Number, so it's not calculated" | FileMaker scripts often calculate and set Number/Text fields. Check scripts that reference the field. |
| "I'll just look at calculation fields" | Most complex logic is in scripts (SetField steps), not calculation field types. Scripts are the PRIMARY source. |
| "This is too complex to extract, I'll rebuild from scratch" | You'll miss critical business rules. Extract the logic first, then refactor for PostgreSQL. |
| "I can translate this literally to PostgreSQL" | FileMaker idioms differ from PostgreSQL. Understand the business rule, then implement idiomatically. |
| "I don't need to document this, the code is self-explanatory" | Business context gets lost. Document WHY the calculation exists, not just WHAT it does. |
| "I'll skip the custom functions for now" | Custom functions contain reusable business logic. Extract them early; they'll be referenced throughout. |
| "This global field must be in PostgreSQL" | Global fields are UI/session state, not database state. Handle in application layer, not schema. |
| "I can figure out relationships from field names alone" | FileMaker relationships include conditions. Check DDR relationship definitions for filtering rules. |

## Checklist for Logic Extraction

When extracting FileMaker business logic:

- [ ] Locate DDR detailed HTML file
- [ ] Identify calculation fields in relevant tables
- [ ] Document purpose and dependencies for each calculation
- [ ] List custom functions used by calculations
- [ ] Extract custom function code and dependencies
- [ ] Map FileMaker functions to PostgreSQL equivalents
- [ ] Decide: PostgreSQL function, VIEW, or import script logic?
- [ ] Implement with idiomatic PostgreSQL patterns
- [ ] Test with sample data from FileMaker
- [ ] Document business rules separately from code

## Real-World Example

From user's existing codebase:

```python
# program_catalog_parser.py:41-70
def get_ay_id(conn, catalog_year: str) -> Optional[str]:
    """
    Get AY id from catalog_year string.

    Converts full format "2025-2026" to short format "25-26"
    and looks up corresponding AY record.

    This logic was adapted from FileMaker calculation that
    performed similar year format conversion in catalog imports.
    """
    # Convert "2025-2026" to "25-26" (FileMaker custom function logic)
    try:
        ay_short = catalog_year[2:4] + '-' + catalog_year[7:9]
    except IndexError:
        logger.error(f"Invalid catalog_year format: {catalog_year}")
        return None

    with conn.cursor() as cur:
        cur.execute("SELECT id FROM ay WHERE ay = %s", (ay_short,))
        result = cur.fetchone()

        if not result:
            logger.warning(f"AY not found for catalog_year: {catalog_year}")
            return None

        return result[0]
```

This function adapted FileMaker's year conversion logic for use in PostgreSQL import scripts.
