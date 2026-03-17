---
name: fhirpath
description: Expert guidance for writing FHIRPath expressions - a path-based navigation and extraction language for FHIR data. Use this skill when writing FHIRPath expressions, navigating FHIR resource trees, filtering collections, performing date/time arithmetic, using FHIRPath functions, writing FHIR invariants, or understanding FHIRPath operators. Trigger keywords include "FHIRPath", "fhirpath", "path expression", "FHIR navigation", "where()", "select()", "exists()", "ofType()", "resolve()", "FHIR invariant", "collection filtering", "FHIRPath function".
---

# FHIRPath

FHIRPath is a path-based navigation and extraction language for hierarchical data models, used extensively in FHIR and CQL. All operations return collections.

## Path Navigation

```
Patient.name.given              // Navigate to given names
Patient.name[0].given           // First name's given (0-based indexing)
Patient.name.first().given      // Equivalent using first()
Observation.value.ofType(Quantity).unit  // Filter by type then navigate
```

Prefix with type name to restrict context: `Patient.name.given` only works on Patient resources.

## Literals

| Type     | Examples                                                         |
| -------- | ---------------------------------------------------------------- |
| Boolean  | `true`, `false`                                                  |
| Integer  | `42`, `-5`                                                       |
| Decimal  | `3.14159`                                                        |
| String   | `'hello'`, `'urn:oid:1.2.3'` (single quotes, use `\'` to escape) |
| Date     | `@2024-01-15`, `@2024-01`, `@2024` (partial dates allowed)       |
| DateTime | `@2024-01-15T14:30:00Z`, `@2024-01-15T14:30:00+10:00`, `@2024T`  |
| Time     | `@T14:30:00`, `@T14:30`                                          |
| Quantity | `10 'mg'`, `4 days`, `100 '[degF]'` (UCUM units in quotes)       |

## Collections

- All values are collections (even single items)
- Empty collection: `{ }`
- Collections are ordered, non-unique, 0-indexed
- Empty propagates through most operations

## Key Functions

### Existence

```
name.exists()                           // true if any names
name.exists(use = 'official')           // true if any official names
name.all(given.exists())                // true if all names have given
telecom.where(system='phone').empty()   // true if no phone telecoms
name.count()                            // number of names
```

### Filtering and Projection

```
name.where(use = 'official')                    // Filter by criteria
entry.select(resource as Patient)               // Project/transform
name.select(given.first() + ' ' + family)       // Combine fields
telecom.distinct()                              // Remove duplicates
item.repeat(item)                               // Recursive traversal (unique)
expansion.repeat(contains)                      // Navigate tree structures
```

### Subsetting

```
name[0]           // First item (0-based)
name.first()      // First item
name.last()       // Last item
name.tail()       // All but first
name.skip(2)      // Skip first 2
name.take(3)      // Take first 3
name.single()     // Error if not exactly one
```

### Combining

```
name.given | name.family     // Union (removes duplicates)
a.union(b)                   // Same as |
a.combine(b)                 // Merge without removing duplicates
a.intersect(b)               // Items in both
a.exclude(b)                 // Items in a but not b
```

### Type Operations

```
value is Quantity                    // Type check (returns Boolean)
value as Quantity                    // Cast (empty if wrong type)
entry.resource.ofType(Patient)       // Filter collection by type
```

### String Functions

```
'hello'.length()                     // 5
'hello'.substring(1, 3)              // 'ell'
'hello'.startsWith('he')             // true
'hello'.endsWith('lo')               // true
'hello'.contains('ell')              // true (different from contains operator)
'hello'.indexOf('l')                 // 2
'HELLO'.lower()                      // 'hello'
'hello'.upper()                      // 'HELLO'
'a-b-c'.replace('-', '_')            // 'a_b_c'
'abc'.matches('[a-z]+')              // true (partial match)
'abc'.matchesFull('[a-z]+')          // true (full match)
'a,b,c'.split(',')                   // {'a', 'b', 'c'}
('a' | 'b' | 'c').join(',')          // 'a,b,c'
'  hello  '.trim()                   // 'hello'
```

### Math Functions (STU)

```
(-5).abs()              // 5
1.5.ceiling()           // 2
1.5.floor()             // 1
1.5.round()             // 2
1.5.truncate()          // 1
2.power(3)              // 8.0
9.sqrt()                // 3.0
2.718.ln()              // ~1.0
100.log(10)             // 2.0
0.exp()                 // 1.0
```

### Conversion

```
'42'.toInteger()              // 42
42.toString()                 // '42'
'3.14'.toDecimal()            // 3.14
'true'.toBoolean()            // true (also 't', 'yes', 'y', '1')
'2024-01-15'.toDate()         // @2024-01-15
'10:30:00'.toTime()           // @T10:30:00
'5 mg'.toQuantity()           // 5 'mg'
value.convertsToInteger()     // true if conversion would succeed
```

### Date/Time Component Extraction (STU)

```
@2024-03-15.yearOf()                          // 2024
@2024-03-15.monthOf()                         // 3
@2024-03-15.dayOf()                           // 15
@2024-03-15T10:30:45.123.hourOf()             // 10
@2024-03-15T10:30:45.123.minuteOf()           // 30
@2024-03-15T10:30:45.123.secondOf()           // 45
@2024-03-15T10:30:45.123.millisecondOf()      // 123
@2024-03-15T10:30:00+10:00.timezoneOffsetOf() // 10.0
@2024-03-15T10:30:00.dateOf()                 // @2024-03-15
@2024-03-15T10:30:00.timeOf()                 // @T10:30:00
```

### Utility

```
now()                                 // Current DateTime
today()                               // Current Date
timeOfDay()                           // Current Time
iif(condition, true-result, else)     // Conditional (short-circuit)
coalesce(a, b, c)                     // First non-empty (STU)
trace('label', projection)            // Debug logging
defineVariable('name', expr)          // Define variable for later use (STU)
```

### Aggregates (STU)

```
(1 | 2 | 3).sum()                     // 6
(1 | 2 | 3).min()                     // 1
(1 | 2 | 3).max()                     // 3
(1 | 2 | 3).avg()                     // 2.0
values.aggregate($this + $total, 0)   // Custom aggregation
```

## Operators

### Equality

```
a = b       // Equal (empty if either empty)
a ~ b       // Equivalent (false if precisions differ, case-insensitive for strings)
a != b      // Not equal
a !~ b      // Not equivalent
```

### Comparison

```
a > b       // Greater than
a < b       // Less than
a >= b      // Greater or equal
a <= b      // Less or equal
```

Comparison with different date/time precisions returns empty: `@2024-01 > @2024-01-15` → `{ }`

### Boolean

```
a and b     // Three-valued AND
a or b      // Three-valued OR
a xor b     // Exclusive OR
a implies b // Implication
not()       // Negation (function, not operator)
```

Three-valued logic: `true and { }` → `{ }`, `false and { }` → `false`

### Math

```
5 + 3       // Addition (also string concatenation)
5 - 3       // Subtraction
5 * 3       // Multiplication
5 / 3       // Division (always Decimal)
5 div 3     // Integer division
5 mod 3     // Modulo
'a' & 'b'   // String concat (empty → empty string)
```

### Collections

```
item in collection       // Membership
collection contains item // Containership (converse of in)
a | b                    // Union
```

### Precedence (high to low)

1. `.` (path), `[]` (indexer)
2. Unary `+`, `-`
3. `*`, `/`, `div`, `mod`
4. `+`, `-`, `&`
5. `is`, `as`
6. `|`
7. `>`, `<`, `>=`, `<=`
8. `=`, `~`, `!=`, `!~`
9. `in`, `contains`
10. `and`
11. `xor`, `or`
12. `implies`

## Date/Time Arithmetic

Add/subtract time-valued quantities from dates/times:

```
@2024-01-15 + 1 month       // @2024-02-15
@2024-01-31 + 1 month       // @2024-02-29 (last day of month)
@2024-03-15 - 10 days       // @2024-03-05
now() - 1 year              // One year ago
```

Calendar duration keywords: `year(s)`, `month(s)`, `week(s)`, `day(s)`, `hour(s)`, `minute(s)`, `second(s)`, `millisecond(s)`

UCUM definite durations (`'a'`, `'mo'`, `'d'`) are NOT equivalent for arithmetic above seconds.

## Environment Variables

```
%ucum        // UCUM URL (http://unitsofmeasure.org)
%context     // Original evaluation context
%`custom`    // Custom variables (backtick-delimited)
```

## Singleton Evaluation

When a function expects a single item but receives a collection:

- Single item → use it
- Single item convertible to Boolean → use as Boolean
- Empty → return empty
- Multiple items → ERROR

## Common Patterns

### Safe navigation with existence checks

```
name.where(use = 'official').exists() implies name.where(use = 'official').given.exists()
```

### Conditional logic

```
iif(gender = 'male', 'M', iif(gender = 'female', 'F', 'U'))
```

### Fallback values

```
coalesce(name.where(use='official'), name.where(use='usual'), name.first())
```

### Reference resolution (FHIR-specific)

```
subject.resolve().ofType(Patient).birthDate
generalPractitioner.all(resolve() is Practitioner)
```

### Working with CodeableConcept

```
code.coding.where(system = 'http://snomed.info/sct').code
code.coding.exists(system = 'http://loinc.org' and code = '12345-6')
```

### Recursive navigation

```
Questionnaire.repeat(item)            // All nested items
ValueSet.expansion.repeat(contains)   // All expansion concepts
```

### Type-safe polymorphic access

```
Observation.value.ofType(Quantity).value > 100
(Observation.value as Quantity).value > 100
```

## FHIR Invariants

FHIRPath is used to define constraints in FHIR profiles:

```
// Name must have family or given
name.family.exists() or name.given.exists()

// If dosage exists, it must have timing or asNeeded
dosage.exists() implies (dosage.timing.exists() or dosage.asNeeded.exists())

// All references must be resolvable as Practitioner
performer.all(resolve() is Practitioner)
```

## Pitfalls

1. **Multiple items in singleton context**: `Patient.name.given + ' ' + Patient.name.family` fails if multiple names
2. **Equality with empty**: `{ } = { }` returns `{ }`, not `true`
3. **Date precision**: `@2024 = @2024-01` returns `{ }` (unknown)
4. **String contains vs collection contains**: `.contains('x')` is string function; `contains x` is operator
5. **Case sensitivity**: FHIRPath keywords are case-sensitive; type names depend on model
6. **Indexing**: Collections are 0-based (first element is `[0]`)
