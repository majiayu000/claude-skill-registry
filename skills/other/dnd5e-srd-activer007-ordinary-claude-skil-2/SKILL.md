---
name: dnd5e-srd
description: Retrieval-augmented generation (RAG) skill for the D&D 5e System Reference Document (SRD). Use when answering questions about D&D 5e core rules, spells, combat, equipment, conditions, monsters, and other SRD content. This skill provides agentic search-based access to the SRD split into page-range markdown files.
---

# D&D 5e SRD RAG

This skill provides search-based retrieval access to the Dungeons & Dragons 5th Edition System Reference Document (SRD), organized by page ranges as markdown files in the `references/` directory.

## When to Use This Skill

Use this skill whenever answering questions about D&D 5e SRD content, including:
- Core rules and gameplay procedures
- Ability checks, saving throws, and skill use
- Combat, actions, conditions, and movement
- Classes, backgrounds, equipment, and magic items
- Spells and spellcasting
- Creatures and stat blocks included in the SRD

## Search Strategy

Follow this agentic search process for D&D 5e SRD queries:

### 1. Identify Relevant Page Ranges

The SRD is organized by page ranges. Use this file index to locate content:

**Important: Always use the Python search tool (`scripts/search_with_positions.py`) to get exact character positions for source citations.**

#### File Index (by page range)

Note: Topics below follow your provided outline and are aligned to the actual file splits; where a topic spans multiple files, it's marked as continued.

- `DND5eSRD_001-018.md`: Intro through Character Creation
- `DND5eSRD_019-035.md`: Barbarian, Bard, Cleric (start)
- `DND5eSRD_036-046.md`: Cleric/Druid, Fighter, Monk (start)
- `DND5eSRD_047-063.md`: Monk, Paladin, Ranger, Rogue
- `DND5eSRD_064-076.md`: Sorcerer, Warlock, Wizard (start)
- `DND5eSRD_077-086.md`: Wizard, Origins, Feats
- `DND5eSRD_087-103.md`: Equipment
- `DND5eSRD_104-120.md`: Spells
- `DND5eSRD_121-137.md`: Spells
- `DND5eSRD_138-154.md`: Spells
- `DND5eSRD_155-175.md`: Spells
- `DND5eSRD_176-191.md`: Rules Glossary (part)
- `DND5eSRD_192-203.md`: Gameplay Toolbox, Magic Items (start, part 1)
- `DND5eSRD_204-229.md`: Gameplay Toolbox, Magic Items (continued)
- `DND5eSRD_230-252.md`: Magic Items (continued)
- `DND5eSRD_253-272.md`: Monsters intro + early entries
- `DND5eSRD_273-292.md`: Monsters
- `DND5eSRD_293-312.md`: Monsters
- `DND5eSRD_313-332.md`: Monsters
- `DND5eSRD_333-364.md`: Monsters / Animals (continued)

### 2. Search Using the Python Tools

Primary method: use the search + expand workflow for accurate positions and structured context.

```bash
# Step 1: Search to find content with exact character positions
python /skills/dnd5e-srd/scripts/search_with_positions.py "search term" --all

# Step 2: If you need more context, expand specific result(s)
python /skills/dnd5e-srd/scripts/expand_context.py "search term" --result 3 --mode section --all

# Examples
# Search combat-related terms
python /skills/dnd5e-srd/scripts/search_with_positions.py "grapple" --all

# Search spells and expand result #1 by section
python /skills/dnd5e-srd/scripts/expand_context.py "fireball" --result 1 --mode section --all

# Search specific page ranges
python /skills/dnd5e-srd/scripts/search_with_positions.py "longsword" --pages 200-300

# Batch expand multiple results
python /skills/dnd5e-srd/scripts/expand_context.py "Attack" --results 1,3,5 --mode paragraph --all
```

The search tool returns:
- Filename
- Character range (start-end positions)
- Matched text with context
- Ready-to-use citation format: `[filename, chars START-END]`

The expand tool returns:
- Expanded text (paragraph, section, or entire document)
- Heading breadcrumb trail
- Original match position within the expansion
- Expansion bounds and metadata

### 3. Expand Context When Needed

After searching, expand results that need deeper context:
- Use `--mode paragraph` for surrounding text
- Use `--mode section` to get the full rule section with headings
- Use `--results 1,3,5` to batch expand multiple results

### 4. Multi-hop Queries

For questions requiring multiple pieces of information:
1. Break down the query into components
2. Search for each component separately
3. Synthesize the information from multiple sources

### 5. Provide Accurate Answers with Source Citations

After retrieving information:
- Quote or paraphrase the exact rules as needed
- **Always cite sources using the character position format**: `[filename, chars START-END]`
- Include multiple sources when relevant
- Cite at the end of the relevant information, not inline

Citation examples:
```
The spell Fireball deals 8d6 fire damage on a failed save. [DND5eSRD_293-312.md, chars 12000-12100]

A grapple check uses Athletics vs. the target's escape DC (see Conditions). [DND5eSRD_087-103.md, chars 5400-5600]
```

## References Directory Structure

The `references/` directory contains the SRD split into page-range files.
Files are named `DND5eSRD_XXX-YYY.md` where `XXX-YYY` is the page range.

To list all files:
```bash
ls -lh /skills/dnd5e-srd/references/
```

To find which file contains specific content:
```bash
grep -l "search term" /skills/dnd5e-srd/references/*.md
```

## Python Tools

### 1. Search Tool (`search_with_positions.py`)

Features:
- Searches SRD reference files with regex-based term matching
- Returns precise character ranges for each match
- Includes contextual text around matches
- Supports filtering by page ranges or specific files

Usage:
```bash
# Basic search across all files
python scripts/search_with_positions.py "term" --all

# Search specific page range
python scripts/search_with_positions.py "term" --pages 200-300

# Control output
python scripts/search_with_positions.py "term" --all --max-results 10 --context 200

# Case-sensitive search
python scripts/search_with_positions.py "Attack" --all --case-sensitive
```

### 2. Context Expansion Tool (`expand_context.py`)

Features:
- Expands specific search results with boundary-aware modes
- Modes: `paragraph` (default), `section`, `section-only`, `char`, `document`
- Provides heading breadcrumb trails for context
- Supports batch expansion and JSON output

Usage:
```bash
# Expand a specific search result by section
python scripts/expand_context.py "fireball" --result 3 --mode section --all-search

# Expand multiple results at once
python scripts/expand_context.py "Attack" --results 1,3,5 --mode paragraph --all-search

# Direct expansion from known file position
python scripts/expand_context.py --file "DND5eSRD_121-137.md" --position 1234 --mode section

# JSON output for machine processing
python scripts/expand_context.py "wizard" --result 1 --all-search --format json
```

## Best Practices

- **Use the Python tools**: search first, then expand for deeper context
- **Always cite sources** with `[filename, chars START-END]`
- **Leverage structure**: use `--mode section` to get full rules and headings
- **Be specific**: search for exact SRD terminology
- **Check multiple files**: related rules may span multiple ranges
- **Handle ambiguity**: present possible interpretations with citations

## Notes

- Files are organized by page ranges (e.g., 001-018, 019-035)
- Some files are large (up to 120K+); prefer targeted searches
- This skill includes SRD content only; not supplements or non-SRD material


