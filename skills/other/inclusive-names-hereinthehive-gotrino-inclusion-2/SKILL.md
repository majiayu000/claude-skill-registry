---
name: inclusive-names
description: Generate culturally diverse names for examples, mock data, and test fixtures. Includes edge-case names that catch bugs.
allowed-tools: Read, Write, Edit
user-invocable: true
---

# Inclusive Names Generator

Generate culturally diverse names for use in examples, mock data, and test fixtures.

## Philosophy

Names in examples signal who you built your product for. But diverse names aren't just about representation—they're also **better test data**.

> "If your tests only use 'John Smith', you're not testing your code. You're testing the happy path."

Names with apostrophes, diacritics, single words, and non-Latin characters catch real bugs that simple Western names miss.

## Reference

Read for name lists and guidelines:
- `references/diverse-names.md` - Names by region, gender-neutral options, edge cases

## Usage

The user may request:
- A specific number of names
- Names for a specific purpose (test users, example customers, documentation)
- Names to replace existing Western-only examples
- Edge-case names for robust testing
- A mix for a specific file or fixture

## Generation Guidelines

### Diversity Principles

1. **Mix regions** - Don't cluster all names from one region
2. **Vary gender presentation** - Include names across the spectrum
3. **Include gender-neutral options** - Sam, Jordan, Alex, Morgan, Taylor, Priya, Yuki
4. **Respect naming conventions** - Some cultures put family name first
5. **Context matters** - Match diversity to the example's context
6. **Avoid stereotyping** - Don't pair names with assumed ethnicities in occupations

### Edge Cases to Include

Always include some names that test code robustness:

| Type | Examples | What It Tests |
|------|----------|---------------|
| Apostrophes | O'Brien, N'Golo, D'Angelo | String escaping, SQL injection |
| Diacritics | José, Müller, Björk, François | Unicode handling, encoding |
| Single names | Suharto, Madonna, Pelé | Required field assumptions |
| Long names | Wolfeschlegelsteinhausenbergerdorff | Field length limits, UI overflow |
| Non-Latin | 田中太郎, Иванов, محمد | Character encoding, font support |
| Hyphenated | García-López, Smith-Jones | Parsing, display formatting |
| Particles | Ludwig van Beethoven, Leonardo da Vinci | Sorting algorithms |

## Output Formats

Provide names in the format the user needs:

**Simple list:**
```
Amara Okafor
Wei Chen
María García-López
Yuki Tanaka
Jordan O'Brien
```

**JSON fixtures:**
```json
[
  { "name": "Amara Okafor", "email": "amara.o@example.com" },
  { "name": "José François", "email": "jose.f@example.com" },
  { "name": "田中太郎", "email": "tanaka.t@example.com" }
]
```

**With flexible name fields (recommended):**
```javascript
const TEST_USERS = [
  { givenName: 'Amara', familyName: 'Okafor', displayName: 'Amara Okafor' },
  { givenName: 'Wei', familyName: 'Chen', displayName: 'Chen Wei' },
  { givenName: 'Suharto', familyName: null, displayName: 'Suharto' },
];
```

**Edge-case focused:**
```javascript
const EDGE_CASE_NAMES = [
  "O'Brien",           // Apostrophe
  "José García",       // Diacritics
  "Suharto",           // Single name
  "李明",              // Non-Latin
  "Smith-Jones",       // Hyphenated
  "Wolfeschlegelstein" // Long (truncated for display)
];
```

## Integration

If the user wants to replace names in existing files:
1. Show current names found
2. Suggest diverse replacements (including edge cases)
3. Preview changes
4. Apply with Edit tool after user approval

## Quick Reference

**Need 5 diverse names fast?**
```
Amara Okafor (West Africa)
Wei Chen (East Asia)
Priya Sharma (South Asia)
María García (Latin America)
Jordan O'Brien (gender-neutral + apostrophe)
```

**Need edge cases for testing?**
```
O'Brien, José, Müller, 田中, Suharto, García-López
```
