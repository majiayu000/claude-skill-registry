---
name: cc-table-driven-methods
description: "Replace complex conditional logic with table lookups. CHECKER mode identifies opportunities where if/else chains or inheritance hierarchies should become tables. APPLIER mode designs table structure, access method (direct/indexed/stair-step), and key transformations. Use when writing 4+ if/else branches, switch statements keep growing, subclasses differ only in data not behavior, or data changes without code changes. Triggers on: too many if statements, switch growing, subclass per type, customer-controlled format, data-driven behavior, lookup table, mapping data to actions."
---

# Skill: cc-table-driven-methods

## STOP - Table vs Logic

- **4+ if/else branches for same classification?** → Convert to table
- **Subclass differs only in data, not behavior?** → Use table, not inheritance
- **Data changes without code changes needed?** → Table is mandatory

---

## CRISIS TRIAGE (1 minute)

**Code review flagged complex logic? Quick assessment:**

1. **Count branches** - If 3+ similar if/else branches for same classification → table candidate
2. **Check volatility** - Does this data change without code changes needed? → table candidate
3. **Look for subclass proliferation** - One subclass just to change a value? → table candidate

**When tables clearly win:**
- Character classification (letter/digit/punctuation)
- Days per month
- Insurance rates by demographic
- Message format parsing
- Grade ranges

---

## Key Definitions

### Table-Driven Method
A scheme that allows you to look up information in a table rather than using logic statements to figure it out.

### Direct Access Table
Access table element directly using a key. Simplest form. Example: `charType = charTypeTable[inputChar]`

### Indexed Access Table
Use primary data to look up key in index table, then use that key for main table. Trades space for direct-access capability with sparse keys.

### Stair-Step Access Table
Entries valid for ranges rather than distinct points. Loop through range boundaries to find category.

### Fudging Lookup Keys
Techniques for making data work as table keys when it doesn't map directly. Includes duplicating info, transforming keys, isolating transformations in routines.

---

## Table Access Method Decision Flowchart

```
+---------------------------+
| Can data key directly     |
| into table?               |
| (e.g., month 1-12)        |
+-----------+---------------+
            |
     +------+------+
     |             |
    YES           NO
     |             |
     v             v
+---------+   +---------------------------+
| DIRECT  |   | Large sparse keyspace?    |
| ACCESS  |   | (e.g., 4-digit part #s,   |
+---------+   | only 100 items)           |
              +-----------+---------------+
                          |
                   +------+------+
                   |             |
                  YES           NO
                   |             |
                   v             v
              +---------+   +---------------------------+
              | INDEXED |   | Valid for ranges?         |
              | ACCESS  |   | (e.g., grade cutoffs,     |
              +---------+   | probability distributions)|
                            +-----------+---------------+
                                        |
                                 +------+------+
                                 |             |
                                YES           NO
                                 |             |
                                 v             v
                            +-----------+  +-----------+
                            | STAIR-STEP|  | Reconsider|
                            | ACCESS    |  | table fit |
                            +-----------+  +-----------+
```

---

## Modes

### CHECKER
Purpose: Identify opportunities to replace logic with tables
Triggers:
  - "review this conditional logic"
  - "is this if chain too complex"
  - "should I use a table here"
  - "audit my switch statement"
Non-Triggers:
  - "design a table solution" -> APPLIER
  - "review my class hierarchy" -> cc-routine-and-class-design
Checklist: **See [checklists.md](./checklists.md)**
Output Format:
  | Location | Current Logic | Table Opportunity | Access Method |
  |----------|--------------|-------------------|---------------|
Severity:
  - OPPORTUNITY: Logic could be replaced with table (complexity > 3 branches)
  - CONSIDER: May benefit from table (volatile data, growing branches)
  - OK: Logic is appropriate (simple, genuinely polymorphic)

### APPLIER
Purpose: Design and implement table-driven solutions
Triggers:
  - "convert this to a table"
  - "design table-driven solution"
  - "replace these if statements with table"
  - "implement table lookup"
Non-Triggers:
  - "is this a good table candidate" -> CHECKER
  - "review my table implementation" -> general code review
Produces:
  - Table structure design
  - Access method selection
  - Key transformation routines
  - Migration from logic to data
Constraints:
  - Isolate key transformations in routines (p.424)
  - Consider external data for volatile tables (p.421)
  - Address both issues: access method AND what to store

---

## When Tables Beat Logic

| Situation | Logic Approach | Table Approach | Winner |
|-----------|---------------|----------------|--------|
| Character classification | 20+ range checks | Single array lookup | Table |
| Days per month | 12-branch if/else | 12-element array | Table |
| Insurance rates (age/gender/status) | Deeply nested ifs | Multi-dimensional array | Table |
| Message format parsing | 20 routines/subclasses | Format description table | Table |
| Grade calculation | 5-branch if chain | Stair-step lookup | Table |
| Simple 2-way decision | Single if/else | 2-element array | Logic |
| Genuinely polymorphic behavior | - | - | OOP |

**Complexity Threshold:** When you're writing the 4th if/else branch for the same classification, consider tables.

---

## When OOP Inheritance is NOT the Answer

> "The fact that a design uses inheritance and polymorphism doesn't make it a good design." (p.423)

**Anti-Pattern: Subclass per variant**
- Creating FloatingPointField, IntegerField, StringField, etc. subclasses
- Each subclass differs only in data, not behavior
- Rote OOP can require MORE code than table-driven approach

**Table Alternative:**
```cpp
// Table of objects - one line replaces 20 routines
AbstractField* field[Field_Last+1];
field[Field_FloatingPoint] = new FloatingPointField();
field[Field_Integer] = new IntegerField();
// ...
field[fieldType].ReadAndPrint(fieldName, fileStatus);
```

**When OOP IS appropriate:** When behavior genuinely varies polymorphically, not just data values.

---

## Red Flags - Consider Table-Driven Instead

**Logic Explosion:**
- Writing 4th if-else branch for same classification
- Switch statement keeps growing with new cases
- Deeply nested conditionals for combinations

**Data Masquerading as Code:**
- Creating subclass just to change a data value
- Customer-controlled format with frequent changes
- Hardcoded values that "might change"

**Duplication:**
- Index calculation duplicated in multiple places
- Same classification logic repeated across functions
- Multiple switch statements on same discriminator

**All of these mean: Put knowledge in data, not code.**

---

## Rationalization Counters

| Excuse | Reality |
|--------|---------|
| "OOP inheritance is the proper design" | Inheritance isn't automatically better. Well-designed table can be simpler than copious subclasses. |
| "Logic is clearer than tables" | Only for simple cases. As complexity grows, tables become clearer. |
| "It's just a few if statements" | "Few" grows. Tables scale better and are easier to modify. |
| "Tables are harder to debug" | Tables separate data from logic, making each easier to verify independently. |
| "I need different behavior per type" | Can behavior be encoded as data? (action codes, routine references) |
| "But the table needs setup code" | Setup code runs once; if-chains execute every call. |
| "It's only N branches now" | The threshold keeps moving. "Just 5" becomes 20. Act at 4+. |
| "Tables are premature optimization" | YAGNI to justify never refactoring. Pattern is already here. |
| "We need the type safety of subclasses" | Modern pattern matching provides type safety without explosion. |
| "This behavior might diverge later" | Speculative polymorphism. Add complexity when needed, not before. |
| "The team doesn't know tables" | Teach the pattern. Don't lock team into suboptimal approaches. |
| "OOP version is more testable" | Tables are testable via lookup function with boundary cases. |

---

## Pressure Testing Scenarios

### Scenario 1: Growing Switch
**Situation:** Switch statement has 8 cases, requirement adds 9th.
**Wrong Response:** Add another case. "It's just one more."
**REQUIRED Response:** Evaluate: Is this data-driven behavior? If pattern will continue growing, convert to table now.

### Scenario 2: Customer-Controlled Format
**Situation:** Message format changes frequently based on customer requirements.
**Wrong Response:** Code each format variant.
**REQUIRED Response:** Make format data-driven. New formats = new table entries, no code changes.

### Scenario 3: Subclass Explosion
**Situation:** Creating 20 subclasses for 20 message types.
**Wrong Response:** "This is proper OOP design."
**REQUIRED Response:** Question: Does each subclass have different BEHAVIOR or just different DATA? If data, use table.

### Scenario 4: Range Classification
**Situation:** Classifying values into categories (A/B/C/D/F grades).
**Wrong Response:** `if (score >= 90) ... else if (score >= 80) ...`
**REQUIRED Response:** Use stair-step table. Easier to modify cutoffs.

---

## Table Design Guidance

### What to Store in Tables

1. **Data** - Direct values (days per month, rates, limits)
2. **Action codes** - Enum/constant indicating what action to take
3. **Routine references** - Function pointers, lambdas, method references

### Fudging Keys - Three Approaches

1. **Duplicate information** - Straightforward but wastes space, risks inconsistency
2. **Transform the key** - `max(min(66, Age), 17)` to clamp range
3. **Isolate in routine** - `KeyFromAge(age)` for consistent transformation

**Always isolate key transformations in their own routines** - eliminates inconsistent transformations, makes modifications easier.

### Stair-Step Implementation

```
' Grade lookup with stair-step
Dim rangeLimit() As Double = { 50.0, 65.0, 75.0, 90.0, 100.0 }
Dim grade() As String = { "F", "D", "C", "B", "A" }

gradeLevel = 0
studentGrade = "A"  ' Default to top grade
While (studentGrade = "A") And (gradeLevel < maxGradeLevel)
   If studentScore < rangeLimit(gradeLevel) Then
      studentGrade = grade(gradeLevel)
   End If
   gradeLevel = gradeLevel + 1
Wend
```

**Subtleties:**
- Watch endpoints - make sure top of each range is covered
- Be careful with `<` vs `<=`
- Consider binary search for large lists
- Consider indexed access for speed (trade space for time)

---

## External Table Data

**When to externalize:**
- Data changes without code changes needed
- Customer-configurable behavior
- A/B testing, feature flags
- Localization data

**How:** Store table data in external file (JSON, YAML, config), read at runtime.

**Tradeoff:** Adds I/O and parsing overhead. Use for genuinely volatile data.

---


---

## Chain

| After | Next |
|-------|------|
| Table implemented | cc-routine-and-class-design (CHECKER) |
