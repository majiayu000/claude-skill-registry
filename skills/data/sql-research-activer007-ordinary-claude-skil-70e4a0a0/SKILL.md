---
name: sql-research
description: Guide for researching SQL syntax and behavior for database backends. Use when you need to research how a SQL function, command, or feature works in a specific database before implementing it in dbplyr.
---

# SQL Research Skill

Use this skill when researching SQL syntax and behavior for any database backend before implementing translations or features in dbplyr.

## When to use this skill

- Before implementing any SQL translation for a database backend
- When you need to understand SQL syntax, behavior, or edge cases
- When documenting database-specific SQL features
- Before writing SQL-generating code in dbplyr

## Critical principle

**SQL correctness is paramount in dbplyr.** You MUST complete research and documentation BEFORE implementing any SQL-related code.

## Research workflow

### 1. Search for official documentation

Use WebSearch to find official documentation for "{dialect} {function/command}":

- **Prioritize official database documentation** and reputable sources
- Search for syntax, behavior, edge cases, and version-specific differences
- Look for:
  - Function signatures and argument types
  - Return types and behavior
  - NULL handling
  - Type coercion rules
  - Limitations or restrictions
  - Differences across database versions

### 2. Document your findings

Create `research/{dialect}-{command}.md` with the following structure:

```markdown
# {Dialect} - {Function/Command}

## Summary
[1-2 sentence summary focused on R-to-SQL translation]

## Syntax
[Minimal syntax examples from official sources]

## Key behaviors
[Only behaviors that matter for dbplyr translation]

## Limitations
[Only restrictions that affect dbplyr usage]

## Sources
- [Source name](URL)
- [Source name](URL)
```

**Documentation guidelines:**
- Keep it minimal and focused on dbplyr use cases
- Include only what's relevant to translating R code to SQL
- ALL citations with URLs are REQUIRED (no exceptions)
- NO comparisons with other databases
- Use concrete examples from official sources
- Keep it as concise as possible

### 3. Verify your research

Cross-reference multiple sources when:
- Documentation seems incomplete or unclear
- Behavior differs across database versions
- Edge cases aren't well documented
- Official docs contradict community sources

**Best practices:**
- Check at least 2-3 authoritative sources
- Note any version-specific differences
- Document uncertainties or ambiguities
- When in doubt, test with actual database if possible

### 4. Proceed to implementation

Only after completing research and documentation should you:
- Implement SQL translations
- Write SQL-generating code
- Add tests for the functionality

## Example research files

### Minimal example

```markdown
# PostgreSQL - POSITION

## Summary
Returns the starting position of a substring within a string (1-indexed).

## Syntax
POSITION(substring IN string)

## Key behaviors
- Returns integer position (1-indexed)
- Returns 0 if substring not found
- Case-sensitive by default
- NULL if any argument is NULL

## Sources
- [PostgreSQL String Functions](https://www.postgresql.org/docs/current/functions-string.html)
```

### Complex example

```markdown
# SQL Server - STRING_AGG

## Summary
Concatenates string values with a specified separator, optionally ordering results.

## Syntax
STRING_AGG(expression, separator) [WITHIN GROUP (ORDER BY order_expression)]

## Key behaviors
- Available in SQL Server 2017+ (compatibility level 110+)
- Returns NULL for empty groups
- Separator must be a literal or variable, not an expression
- WITHIN GROUP clause is optional but commonly used for deterministic ordering
- Maximum output length is 2GB

## Limitations
- Not available in SQL Server 2016 or earlier
- Cannot use with DISTINCT (use subquery instead)
- Separator cannot be a computed expression

## Sources
- [SQL Server STRING_AGG](https://docs.microsoft.com/en-us/sql/t-sql/functions/string-agg-transact-sql)
- [Compatibility requirements](https://docs.microsoft.com/en-us/sql/t-sql/functions/string-agg-transact-sql#compatibility-support)
```

## Common research patterns

### String functions
- Character encoding and collation
- 0-indexed vs 1-indexed positions
- NULL handling
- Regular expression support and syntax

### Date/time functions
- Date/time types and precision
- Timezone handling
- Format strings and conventions
- Interval arithmetic

### Aggregate functions
- NULL handling in aggregates
- Empty group behavior
- DISTINCT support
- Window function variants

### Window functions
- OVER clause syntax
- Frame specifications (ROWS vs RANGE)
- Partitioning and ordering
- Function-specific restrictions

## Checklist

Before completing SQL research:

- [ ] Searched official database documentation
- [ ] Identified syntax and key behaviors
- [ ] Documented edge cases and limitations
- [ ] Created research file in `research/{dialect}-{function}.md`
- [ ] Included ALL source URLs
- [ ] Kept documentation minimal and focused
- [ ] Cross-referenced multiple sources if needed
- [ ] Ready to proceed with implementation

## Tips

- **Start broad, then narrow**: Search for the general command first, then dig into specifics
- **Use official docs first**: Official documentation is most authoritative
- **Check version availability**: Many SQL features are version-specific
- **Note NULL behavior**: NULL handling often differs across databases
- **Document what matters**: Focus on dbplyr translation needs, not general SQL education
- **Keep it short**: Research docs should be scannable reference material, not tutorials
