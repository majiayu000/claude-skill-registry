---
name: okyline
description: >
  Expert assistant for the Okyline schema language. Okyline enables JSON data 
  validation by example, where constraints are expressed inline on field names. 
  Use when creating, editing, or converting JSON Schema, Avro, or other schema 
  formats to Okyline, or when answering questions about Okyline syntax and features.
  This skill should be triggered whenever the user mentions Okyline, references 
  .oky files, or asks about example-driven JSON schema validation.
---

# Okyline Schema Language v1.1.0

Okyline is a declarative language for describing and validating JSON structures using inline constraints on field names. Schemas are valid JSON documents with real example values.

# Okyline skill version : 1.6.1

## ⚠️ Before any schema generation

**MANDATORY**: Read the reference files BEFORE producing an Okyline schema:

1. `references/syntax-reference.md` — complete syntax of constraints
2. `references/internal-references.md` — $defs and $ref
3. `references/conditional-directives.md` — if conditional logic
4. `references/expression-language.md` — if $compute is necessary

Never generate a schema based solely on this SKILL.md file.
The examples here are a summary, not an exhaustive reference.

## $ref: minimal usage

DO NOT use `$defs`/`$ref` unless:
1. Recursion (mandatory)
2. Explicit user request

Default → everything inline in `$oky`.


## Core Syntax

```
"fieldName | constraints | label": exampleValue
```

- **fieldName**: JSON field name
- **constraints**: Validation rules (space-separated)
- **label**: Optional human-readable description
- **exampleValue**: Determines the inferred type

If a label is present without constraints, use `| |`:

  ❌ `"acheteur|Client"` → "Client" parsed as constraint!
  ✅ `"acheteur| |Client"` → "Client" is the label

## Minimal Schema Structure

```json
{
  "$oky": {
    "name|@ {2,50}|User name": "Alice",
    "email|@ ~$Email~": "alice@example.com",
    "age|(18..120)": 30
  }
}
```

## Essential Constraints

| Symbol | Meaning | Example |
|--------|---------|---------|
| `@` | Required field | `"name\|@": "Alice"` |
| `?` | Nullable (can be null) | `"middle\|?": "John"` |
| `{min,max}` | String length | `"code\|{5,10}": "ABC123"` |
| `(min..max)` | Numeric range | `"age\|(18..65)": 30` |
| `('a','b')` | Enum values | `"status\|('ACTIVE','INACTIVE')": "ACTIVE"` |
| `~pattern~` | Regex or format | `"email\|~$Email~": "a@b.com"` |
| `[min,max]` | Array size | `"tags\|[1,5]": ["eco"]` |
| `[*]` | Array (no size constraint) | `"items\|[*]": [1, 2]` |
| `->` | Element validation constraint | `"tags\|[*] -> {2,10}": ["eco"]` |
| `!` | Unique elements | `"codes\|[*]!": ["A","B"]` |
| `#` | Key field (for object uniqueness) | `"id\|#": 123` |
| `$ref` | Reference to definition (type indicator, not a validation constraint) | `"address\|$ref": "&Address"` |


### Contraintes numériques ouvertes

Quand une seule borne est nécessaire, utiliser les opérateurs de comparaison :

| Syntaxe | Signification | Exemple |
|---------|---------------|---------|
| `(>0)` | Strictement positif | `"quantity\|(>0)": 5` |
| `(>=0)` | Positif ou zéro | `"price\|(>=0)": 29.99` |
| `(<100)` | Strictement < 100 | `"percentage\|(<100)": 50` |
| `(<=100)` | ≤ 100 | `"score\|(<=100)": 85` |

❌ Ne jamais inventer de syntaxe avec borne manquante : `(0..)`, `(..100)`
✅ Utiliser les comparaisons : `(>=0)`, `(<=100)`

❌ Ne jamais inventer borne manquante : `(0..99999999)`, `(-99999999..100)`
✅ Utiliser les comparaisons : `(>=0)`, `(<=100)`


⚠️ **INVALID SYNTAX** — Okyline does NOT support open ranges:
- ❌ `(0..)`, `(..100)`, `(1..*)`, `(0..*)`
- These will cause validation errors

### Taille de collection illimitée

Utiliser `*` pour indiquer "pas de limite" :

| Syntaxe | Signification |
|---------|---------------|
| `[*]` | Tableau sans contrainte de taille |
| `[1,*]` | Au moins 1 élément, pas de maximum |
| `[~pattern~:*]` | Map avec clés validées, nombre d'entrées illimité |

❌ Ne jamais omettre une borne : `[1,]`, `[~pattern~:]`
✅ Utiliser `*` explicitement : `[1,*]`, `[~pattern~:*]`


## Built-in Formats

Use with `~$FormatName~`: `$Date`, `$DateTime`, `$Time`, `$Email`, `$Uri`, `$Uuid`, `$Ipv4`, `$Ipv6`, `$Hostname`

## Type Inference Rules

- Type is inferred from example value (no explicit declarations)
- `42` → Integer, `3.14` → Number, `"text"` → String, `true` → Boolean
- Arrays must have at least one element for type inference
- **`null` cannot be used as example** — no type can be inferred. Use `?` for nullable fields with a real example value:

❌ `"middleName|?": null`
✅ `"middleName|?{1,50}": "Marie"`

❌ `"discount|?(0..100)": null`
✅ `"discount|?(0..100)": 15`

### Decimal Values Ending in .00

JSON serializers drop trailing zeros: `78.00` becomes `78`. 
To preserve decimal precision in examples, wrap in quotes:

❌ `"amount": 78.00`   → Serialized as 78, type inferred as Integer
✅ `"amount": "78.00"` → Preserved, type inferred as Number

This only affects decimals with zero fractional parts (.00, .0).
Regular decimals (45.5) and integers (10) are unaffected.

## Reusable Definitions — `$defs` and `$ref`

Okyline supports **internal references** to promote reuse and consistency.

### `$defs` — Definition Repository

`$defs` is placed at root level (alongside `$oky`) and contains reusable schema fragments:

```json
{
  "$oky": {
    "person": {
      "address | $ref": "&Address",
      "contact | $ref @": "&Email"
    }
  },
  "$defs": {
    "Address": {
      "street|@ {2,100}": "12 rue du Saule",
      "city|@ {2,100}": "Lyon"
    },
    "Email|~$Email~ {5,100}": "user@example.com"
  }
}
```

Definitions can be **objects** or **scalars** (with constraints in the key).

### Reference Syntax — `&Name`

References use `&` prefix: `&Address`, `&Email`, `&Person`

### Property-Level Reference — `field | $ref`

A field uses another schema as its type:

```json
"address | $ref @": "&Address"        // Required address
"backup | $ref ?": "&Address"         // Optional, nullable
"emails | $ref [1,5]": ["&Email"]     // Array of 1-5 emails
```

**Structural constraints** (`@`, `?`, `[min,max]`, `!`) are defined locally at each usage.
**Value constraints** (`{min,max}`, `(min..max)`, `~pattern~`) are inherited from the definition.

### Important: `$ref` vs `->` for arrays

`$ref` and `->` serve different purposes:
- `$ref` = type indicator (what the elements ARE) — comes BEFORE `->`
- `->` = validation constraints (rules elements must satisfy) — comes AFTER `$ref`

For arrays of referenced types, `$ref` is placed with the array constraint, never after `->`:
```json
// Correct syntax
"items|[*] $ref": ["&Item"]                    // Array of Item references
"items|[1,10] $ref": ["&Item"]                 // Array of 1-10 Item references  
"items|[*] $ref -> {2,50}": ["&Item"]          // With additional element constraint

// Wrong syntax - $ref must never be after ->
❌ "items|[*] -> $ref": ["&Item"]
```

### Object-Level Reference — Inheritance

Include all fields from a base schema:

```json
{
  "$oky": {
    "Article": {
      "$ref": "&Auditable",
      "title|@ {1,200}": "Mon article"
    }
  },
  "$defs": {
    "Auditable": {
      "createdAt|@ ~$DateTime~": "2025-01-01T00:00:00Z",
      "updatedAt|@ ~$DateTime~": "2025-01-01T00:00:00Z"
    }
  }
}
```

Multiple inheritance: `"$ref": ["&Auditable", "&Deletable"]`

### Modifying Inherited Fields

| Directive | Usage | Description |
|-----------|-------|-------------|
| `$remove` | `"$remove": ["field1", "field2"]` | Exclude inherited fields |
| `$override` | `"field \| $override ...": value` | Replace inherited definition |
| `$keep` | `"$keep": ["&A.field"]` | Resolve collision in multiple inheritance |

## $compute Context Rules

Expressions in `$compute` must be **attached to a field** using `|(%ComputeName)` syntax. The expression is evaluated in the **context of the parent object** of the annotated field.

❌ Unattached compute (never evaluated):
```json
"$compute": { "Valid": "total == sum(items, price)" }
```

✅ Attached to a field:
```json
"total|(%Valid)": 100.0
```

❌ Wrong context - using absolute paths in array element validation:
```json
"lignes|[*]": [{ "montantHT|(%Check)": 500 }],
"$compute": { "Check": "lignes[*].montantHT == lignes[*].quantite * lignes[*].prix" }
```

✅ Correct - references are relative to parent (the current array element):
```json
"$oky":{
   "lignes|[*]": [{ "quantite": 5, "prix": 100, "montantHT|(%Check)": 500 }]
},
"$compute": { "Check": "montantHT == quantite * prix" }
```

## Schema Design Workflow

1. Start with `{"$oky": { ... }}`
2. Identify reusable structures → define in `$defs`
3. Write example JSON with realistic values
4. Add `@` to required fields
5. Add constraints progressively: length, range, format, enums
6. Use `$ref` for reusable types
7. Add conditional logic if needed (`$appliedIf`, `$requiredIf`)
8. Add computed validations if needed (`$compute`)

## Reference Files

For detailed syntax and features, consult these references:

- **Constraint syntax & patterns**: See [references/syntax-reference.md](references/syntax-reference.md)
- **Conditional directives**: See [references/conditional-directives.md](references/conditional-directives.md)
- **Expression language ($compute)**: See [references/expression-language.md](references/expression-language.md)
- **Internal references ($defs, $ref)**: See [references/internal-references.md](references/internal-references.md)

## Quick Patterns

```json
// Required email
"email|@ ~$Email~": "user@example.com"

// Required string 2-50 chars
"name|@ {2,50}": "Alice"

// Optional number range
"discount|(0..100)": 15

// Enum from nomenclature
"status|@ ($STATUS)": "ACTIVE"

// Array of unique strings, 1-10 items, each 2-20 chars
"tags|@ [1,10] -> {2,20}!": ["eco", "bio"]

// Required but nullable
"middleName|@ ?{1,50}": "Marie"

// Map with pattern keys
"translations|[~^[a-z]{2}$~:10]": {"en": "Hello", "fr": "Bonjour"}

// Reference to definition (required)
"address | $ref @": "&Address"

// Array of referenced type ($ref before ->, never after)
"items | $ref @ [1,100]": ["&OrderItem"]

// Array of referenced type with element constraint
"codes | $ref [1,10] -> {2,20}": ["&Code"]

// Object inheritance
"$ref": "&Auditable"

// Multiple inheritance
"$ref": ["&Auditable", "&Deletable"]
```

## Document Metadata (Optional) - Must be generated in this order

```json
{
  "$okylineVersion": "1.1.0",
  "$version": "1.0.0",
  "$id": "my-schema",
  "$title": "My Schema",
  "$description": "Schema description",
  "$additionalProperties": false,
  "$oky": {
    ...
  },
  "$defs": { ... },
  "$format": { "Code": "^[A-Z]{3}-\\d{4}$" },
  "$compute": { "Total": "price * quantity" },
  "$nomenclature": { "STATUS": "ACTIVE,INACTIVE" }
}


**`$id` format**: Only letters, digits, underscores and dots allowed. Pattern: `^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)*$`
 ❌ `"personne-vehicules"` (hyphen not allowed)
 ✅ `"personne.vehicules"` or `"personne_vehicules"`
```

## Common Mistakes to Avoid

- Missing `$oky` wrapper
- Empty arrays (need at least one element)
- Confusing `[1,10]` (array size) with `-> {1,10}` (element constraint)
- Forgetting to escape backslashes in regex (`\d` → `\\d`)
- Defining `$compute` expressions without attaching them to fields with `|(%Name)`
- Using absolute paths in `$compute` instead of relative references to parent context
- Using `$ref` without the `&` prefix (correct: `"&Address"`, wrong: `"Address"`)
- Object-level `$ref` targeting a scalar definition (must target object schema)
- Redefining an inherited field without using `$override`
- Creating circular object-level references (A includes B includes A)
- Placing `$defs` inside `$oky` (must be at root level)
- Using empty brackets `[]` for arrays — use `[*]` or omit size constraint entirely
- Applying element constraints (enum, length, range) directly to array field instead of using `->`:
  ❌ `"permis|@ ('A','B','C')[]": ["B"]`
  ✅ `"permis|@ -> ('A','B','C')": ["B"]`
  ✅ `"permis|@ [1,5] -> ('A','B','C')": ["B"]`
  - Using hyphens in `$id` — only letters, digits, underscores and dots are allowed
- Applying element constraints (enum, length, range) directly to array field instead of using `->`:
  ❌ `"permis|@ ('A','B','C')[]": ["B"]`
  ✅ `"permis|@ -> ('A','B','C')": ["B"]`
  ✅ `"permis|@ [1,5] -> ('A','B','C')": ["B"]`
- Placing `$ref` after `->` for arrays of references (`$ref` is a type indicator, not a validation constraint):
  ❌ `"children|[*] -> $ref": ["&Node"]`
  ✅ `"children|[*] $ref": ["&Node"]`
  ✅ `"children|[1,10] $ref -> {2,50}": ["&Node"]`
- Using open-ended range syntax `(0..)` or `(..100)` — these don't exist!
  ❌ `"price|(0..)": 29.99`
  ✅ `"price|(>=0)": 29.99`
 - Using multiple value constraint blocks `(...)` on the same field:
  ❌ `"montantTTC|@ (>=0) (%LigneTTC)": 4320`
  ✅ `"montantTTC|@ (%LigneTTC)": 4320`
 - Using null as an example value, even with ? Okyline needs a valid example to infer the type.:
  ❌ `"name|? ": null`
  ✅ `"name|? ": "Charles"`
 - Using decimal number example terminant par .00 sans " ".
   ❌ `"amount|? ": 800.00`
  ✅ `"amount|? ": "800.00"`
  
  When a field uses `$compute`, ALL value constraints must be inside the compute expression:
```json
  "$compute": {
    "LigneTTC": "montantTTC >= 0 && montantTTC == montantNetHT + montantTVA"
  }
```

## ⚠️ Erreurs silencieuses (pas d'erreur syntaxe, mais problème à la validation)

- [ ] Décimales en `.00` → `"150.00"` (sinon inféré comme Integer)
- [ ] Exemple `null` → impossible d'inférer le type
- [ ] Tableau vide `[]` → impossible d'inférer le type des éléments
- [ ] `"champ|Label"` → "Label" interprété comme contrainte (utiliser `"champ| |Label"`)
