---
name: jlcpcb
description: 'Search the JLCPCB electronic components database (~7 million parts)
  for hardware/electronics projects. Use when the user needs to: (1) Find electronic
  components (resistors, capacitors, ICs, connector'
---

---
name: jlcpcb
description: Search the JLCPCB electronic components database (~7 million parts) for hardware/electronics projects. Use when the user needs to: (1) Find electronic components (resistors, capacitors, ICs, connectors, etc.), (2) Look up specific part numbers or manufacturers, (3) Find alternatives or equivalents for components, (4) Check component availability and stock at JLCPCB, (5) Get component specifications (package type, description, etc.), or (6) Search for parts for PCB assembly projects.
---

# JLCPCB Parts Finder

Search the JLCPCB electronic components database for hardware/electronics projects.

## Database Location

Database: `~/.jlcpcb-db/cache.sqlite3`

If missing, user should download from https://yaqwsx.github.io/jlcparts/

## Query Script

Use `~/.claude/skills/jlcpcb/query.js` for all database queries.

### List categories:
```bash
node ~/.claude/skills/jlcpcb/query.js list-categories
```

### Search parts:
```bash
node ~/.claude/skills/jlcpcb/query.js search-parts <category_id> [keyword] [limit]
```

**Examples:**
```bash
# Search for 3.5mm audio jacks
node ~/.claude/skills/jlcpcb/query.js search-parts 208 "3.5" 10

# Search for LDO regulators
node ~/.claude/skills/jlcpcb/query.js search-parts 111 "LDO" 15

# List all parts in a category (no keyword)
node ~/.claude/skills/jlcpcb/query.js search-parts 208 "" 20
```

## Common Categories

Quick reference for frequently used categories:

- **Audio Connectors**: 208
- **Linear Voltage Regulators**: 130
- **LDO Regulators**: 111, 120
- **PMIC - Current & Power Monitors & Regulators**: 512

For other categories, use `list-categories` to find the appropriate ID.

## Workflow

1. **Understand request** - What component does the user need?
2. **Find category**:
   - If known, proceed to search
   - If unknown, list categories to find the right one
3. **Search parts** with category ID and optional keyword
4. **Present results**:
   - Part number (C-prefix LCSC number)
   - Manufacturer
   - Description
   - Package type
   - Stock availability
   - Detail page URL for each part

## Output Format

Results from query.js are formatted as:
```
C{lcsc}: {mfr} - {description} ({package}, Stock: {stock})
   → https://jlcpcb.com/partdetail/C{lcsc}
```

Example:
```
C5155561: PJ-393-8P - 3.5mm Headphone Jack 1A -20℃~+70℃ 20V Gold Phosphor Bronze SMD Audio Connectors (SMD, Stock: 1995)
   → https://jlcpcb.com/partdetail/C5155561
```

**Important:** Always include the URL in your response so users can view detailed specifications and datasheets.

## Tips

- Start with broader keywords if specific searches return no results
- Part numbers may vary (e.g., "7812" vs "LM7812")
- Results are sorted by stock (descending) - highest stock first
- Limit initial searches to 10-20 results to avoid overwhelming output
- For DIY projects, suggest through-hole over SMD when appropriate
- Always show stock availability in recommendations

## SQL Reference

The query script uses these SQL patterns:

**With keyword:**
```sql
SELECT lcsc, mfr, description, package, stock
FROM components
WHERE category_id = ? AND (mfr LIKE ? OR description LIKE ?)
ORDER BY stock DESC LIMIT ?
```

**Without keyword:**
```sql
SELECT lcsc, mfr, description, package, stock
FROM components
WHERE category_id = ?
ORDER BY stock DESC LIMIT ?
```

Alternative: Use sqlite3 CLI directly if needed:
```bash
sqlite3 ~/.jlcpcb-db/cache.sqlite3 "SELECT id, category, subcategory FROM categories LIMIT 10"
```
