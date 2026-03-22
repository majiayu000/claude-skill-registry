---
name: data-context
description: "This skill should be used when the user asks to 'set up data analysis for our database', 'extract tribal knowledge about dataset', 'generate data skill', 'document this dataset', 'what does this column mean', 'create data dictionary', 'help me understand this data schema', 'capture domain knowledge about our data', or needs to create a reusable data context skill from dataset expertise."
user-invocable: false
---

# Data Context Extractor

Extract tribal knowledge about a dataset or database and generate a reusable data context skill.

<EXTREMELY-IMPORTANT>
## The Iron Law of Data Context

**YOU MUST interview the user before generating ANY skill content. This is not negotiable.**

You MUST NOT:
- Generate a data context skill from schema alone
- Skip entity disambiguation
- Assume metric definitions without confirmation
- Output a skill without user review of each section

**If you're about to write a skill based on your assumptions, STOP. Interview first.**
</EXTREMELY-IMPORTANT>

## Two Modes

### 1. Bootstrap Mode
**Trigger:** No existing data context skill for this project/dataset.

Create a new data context skill from scratch by interviewing the user about their data.

### 2. Iteration Mode
**Trigger:** Existing data context skill exists, user wants to add a new domain or update.

Read existing skill, identify gaps, interview for the new domain, merge into existing skill.

## Integration with Existing Data Access Skills

Before interviewing, check for existing data access skills that already encode tribal knowledge:

```
1. READ existing skills: /wrds, /lseg-data, or any project-local data skills
2. IDENTIFY what they already cover (table names, filters, field mappings, gotchas)
3. DO NOT re-document what existing skills handle
4. FOCUS the interview on the project-specific layer:
   - Which specific tables/fields from WRDS or LSEG does THIS study use?
   - How are identifiers linked across sources? (permno ↔ gvkey, RIC ↔ ISIN ↔ cusip)
   - What sample filters define the study universe? (date range, exchange, firm type)
   - What derived variables or transformations are project-specific?
```

The generated data context skill should **reference** existing skills rather than duplicate them:

```markdown
## Data Sources

| Source | Skill | Tables/Fields Used |
|--------|-------|--------------------|
| WRDS | `/wrds` | comp.funda (at, lt, ceq), crsp.msf (ret, prc) |
| LSEG | `/lseg-data` | TR.F.TotRevenue, TR.GICSSector |
| Local | DuckDB | data/processed/merged_panel.parquet |

For connection details and critical filters, see the referenced skills.
```

## The Interview Process

```
1. DISCOVER data sources
   → What databases/files/APIs? Connection details?
   → For each: what dialect? (PostgreSQL, DuckDB, SQLite, Snowflake, etc.)
   → IMPORTANT: If user mentions WRDS or LSEG, read the corresponding skill first
     and ask only about project-specific usage, not general access patterns

2. MAP entities
   → What are the core entities? (users, transactions, products, etc.)
   → How do they relate? (foreign keys, join paths)
   → CRITICAL: Disambiguate entity names
     - "user" vs "account" vs "customer" — are these the same?
     - "order" vs "transaction" vs "purchase" — clarify overlaps
     - Document the canonical name and any aliases

3. DEFINE key metrics
   → What are the business-critical metrics?
   → For each metric:
     - Exact definition (SQL or formula)
     - Known edge cases
     - Common misinterpretations
     - Time grain (daily, monthly, etc.)

4. DOCUMENT data hygiene
   → Known data quality issues
   → Fields that lie (e.g., "created_at" that's actually "imported_at")
   → Nulls that mean something specific
   → Enums/codes that need translation
   → Date ranges with reliable data vs backfill periods

5. CAPTURE common gotchas
   → Joins that explode (many-to-many lurking as one-to-many)
   → Filters that are always needed (e.g., "WHERE is_deleted = false")
   → Time zones and their traps
   → Slowly changing dimensions
   → Tables that look useful but aren't (deprecated, partial, test data)

6. COLLECT common query patterns
   → Frequently needed aggregations
   → Standard date filters or cohort definitions
   → Boilerplate CTEs that everyone copies
```

## Interview Style

Ask questions in batches of 3-5. Don't overwhelm with everything at once.

**Round 1: Data Sources**
- What data sources does this project use? (WRDS, LSEG, local files, other databases?)
- For known sources (WRDS/LSEG): which specific tables and fields do you pull?
- For local data: what formats (parquet, CSV, SQLite, DuckDB)? Where stored?
- How do you link identifiers across sources? (permno, gvkey, cusip, ISIN, RIC)

**Round 2: Core Entities** (after Round 1 answers)
- What are the main entities in this data?
- Walk me through how [Entity A] relates to [Entity B]
- Are there any entity names that are ambiguous or have aliases?

**Round 3: Metrics & Definitions** (after Round 2 answers)
- What metrics does your team track most?
- For [Metric]: what's the exact calculation? Any edge cases?
- Are there metrics people commonly get wrong?

**Round 4: Data Quality & Gotchas** (after Round 3 answers)
- What are the known data quality issues?
- Any fields that are misleading or have surprising behavior?
- What's the most common mistake new analysts make with this data?

**Round 5: Common Patterns** (after Round 4 answers)
- What queries do you find yourself writing repeatedly?
- Any standard filters or cohort definitions everyone uses?
- What boilerplate would save the most time?

## Output: Generated Skill

After the interview, generate a skill with this structure:

```
project-name/
├── .claude/
│   └── skills/
│       └── data-context/
│           ├── SKILL.md          # Main skill file
│           └── references/
│               ├── entities.md   # Entity definitions and relationships
│               ├── metrics.md    # Metric definitions with SQL/formulas
│               └── gotchas.md    # Data quality issues and common pitfalls
```

### SKILL.md Template

```markdown
---
name: [project]-data-context
description: "Data context for [project]. Entity definitions, metric calculations, data quality notes, and common patterns for [data domain]."
---

# [Project] Data Context

## Data Sources

| Source | Skill/Dialect | Tables/Fields Used |
|--------|---------------|--------------------|
| [WRDS] | `/wrds` | [specific tables and fields for this project] |
| [LSEG] | `/lseg-data` | [specific fields for this project] |
| [Local] | [DuckDB/CSV/Parquet] | [file paths or database] |

For connection details and critical filters, see the referenced skill. This context covers only project-specific usage.

## Entity Map

[Entity relationship summary — which entities exist, how they connect]

See `references/entities.md` for full definitions.

## Key Metrics

[Top 3-5 metrics with brief definitions]

See `references/metrics.md` for exact calculations and edge cases.

## Critical Gotchas

[Top 3-5 gotchas that catch analysts]

See `references/gotchas.md` for full list.

## Common Patterns

[Frequently used query snippets or data access patterns]
```

### Generating the References

For each reference file, include:
- **entities.md**: Entity name, aliases, primary key, important fields, relationships, common joins
- **metrics.md**: Metric name, definition (SQL/formula), edge cases, common misinterpretations, time grain
- **gotchas.md**: Issue description, why it happens, how to detect, how to handle

## Exit Gate

Before writing skill files, execute this gate:

1. **IDENTIFY**: All 5 interview rounds completed
2. **RUN**: Read back each generated section to the user
3. **READ**: Verify entities, metrics, gotchas sections all have substantive content (not placeholders)
4. **VERIFY**: User approved each section via explicit confirmation
5. **CLAIM**: Only generate skill files after ALL checks pass

**Skipping this gate produces a skill based on your assumptions, not the user's knowledge. That skill will mislead every future analysis.**

## Verification

Before finalizing the skill:

1. **Read back** each section to the user for confirmation
2. **Test** at least one metric definition against actual data if possible
3. **Check** entity relationships match what the user described
4. **Confirm** the gotchas list captures what the user considers most important

## Iteration Mode Details

When adding to an existing data context skill:

1. Read the existing skill files
2. Identify what's already documented
3. Interview for the NEW domain only (don't re-interview existing content)
4. Merge new content into existing files, maintaining consistent formatting
5. Flag any conflicts with existing definitions (e.g., metric redefinition)

## Where to Place the Output

- **Project-specific**: `.claude/skills/data-context/` in the project root
- The generated skill becomes available to all future Claude sessions in that project
- Subagents spawned by `ds-delegate` will have access to it automatically

## Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I can infer the metrics from column names" | Column names are labels, not business logic. `revenue` could be gross, net, or recognized. | Ask the user for the exact definition and edge cases |
| "The schema tells me everything I need" | Schema captures structure, not semantics. It can't tell you which fields lie or which joins explode. | Interview the user — schema is the starting point, not the answer |
| "I'll fill in the gotchas section later" | Gotchas are the most valuable part. Later means never — you'll ship a skill that misleads every analysis. | Capture gotchas during the interview while context is fresh |
| "The entity relationships are obvious from foreign keys" | Foreign keys show connections, not business rules. A `user_id` FK doesn't tell you users can have multiple active accounts. | Verify every relationship with the user, especially cardinality |
| "I already know this domain well enough" | Your training data is not this user's data. Their dataset has specific quirks you cannot guess. | Interview anyway — it takes 10 minutes and prevents weeks of wrong analysis |

### Drive-Aligned Framing

**Skipping the domain expert interview is NOT HELPFUL — every downstream analysis inherits your wrong assumptions about the data.** Pattern-matching from column names is not domain understanding.

| Shortcut | Consequence |
|----------|-------------|
| Skipping the interview | You skip the interview to save time. The generated skill has wrong assumptions — every analysis using it produces wrong results. Your shortcut corrupted the entire pipeline. |
| Generating from schema alone | You inferred metric definitions from column names. Three teams used your skill. All three published wrong numbers. Your inference was misinformation. |

## Red Flags - STOP If You Think:

| Thought | Reality |
|---------|---------|
| "I can infer this metric from the schema" | Schema doesn't capture business logic. Ask the user. |
| "This entity relationship is obvious" | Obvious relationships hide gotchas. Verify with user. |
| "I'll fill in the gotchas later" | Gotchas are the most valuable part. Capture them now. |
| "The user said 'standard SQL'" | There's no such thing as standard SQL in practice. Get the dialect. |
| "I'll skip the read-back, it looks right" | Your version ≠ their mental model. Always read back. |
| "I should document how to connect to WRDS" | `/wrds` already covers that. Document project-specific tables and filters only. |
| "Let me add the LSEG field prefixes" | `/lseg-data` already covers that. Document which fields THIS project uses. |
