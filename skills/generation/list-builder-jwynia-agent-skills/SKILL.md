---
name: list-builder
description: Build comprehensive randomization lists for creative entropy. Use when you need to create or expand lists of story elements (professions, locations, objects, names, etc.) for use with entropy tools. Leverages research sources like Kiwix/Wikipedia to build lists with good variety and size.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# List Builder: Entropy List Curation Skill

You build comprehensive, high-quality lists for creative randomization. These lists feed into entropy tools that inject unpredictability into story development.

## Core Principle

**Good entropy lists have three properties:**
1. **Size** — Large enough (50-200+ items) to feel genuinely random
2. **Variety** — Spans the full possibility space, not just obvious examples
3. **Specificity** — Concrete enough to spark ideas, not vague categories

LLMs are good at research, categorization, and quality control. Scripts are good at storage and random selection. This skill bridges them.

## Dataset Maturity Levels

See [references/dataset-quality-criteria.md](references/dataset-quality-criteria.md) for complete criteria.

| Level | Size | Status | Use Case |
|-------|------|--------|----------|
| **Starter** | 10-30 | Quick example | Prototyping, demos |
| **Functional** | 30-75 | Usable but limited | Personal projects |
| **Production** | 75-150 | Ready for regular use | Client work, published tools |
| **Comprehensive** | 150+ | Reference quality | Definitive resource |

**Key metrics:**
- **Size:** Large enough for genuine randomness
- **Variety:** Covers all relevant dimensions (see criteria doc)
- **Specificity:** Concrete enough to spark ideas (20-60 char average)
- **Freshness:** >30% items that surprise (not first-thought)

**Current built-in lists are Starter/Functional level.** This skill exists to build them up to Production.

## List Quality Criteria

### What Makes a Good List Item

**Good:** "Elevator inspector" (specific, unexpected, sparks questions)
**Bad:** "Office worker" (generic, expected, no hooks)

**Good:** "Self-storage facility at midnight" (specific time, atmosphere implied)
**Bad:** "Building" (too vague to use)

**Good:** "They're solving a completely different case that uses same evidence" (specific collision mechanism)
**Bad:** "They get in the way" (no mechanism, just effect)

### Variety Dimensions

When building a list, ensure coverage across relevant dimensions:

**Professions:**
- Industries (medical, legal, construction, arts, service, tech)
- Status levels (entry-level to expert)
- Visibility (public-facing vs. behind-scenes)
- Unusual vs. common
- Historical vs. modern vs. emerging

**Locations:**
- Public vs. private
- Indoor vs. outdoor
- Urban vs. rural vs. suburban
- Time of day implications
- Emotional valence (creepy, mundane, sacred, liminal)

**Character traits:**
- Positive vs. negative vs. neutral
- Visible vs. hidden
- Self-aware vs. blind spots
- Stable vs. situational

## Research Process

### Step 1: Define the List
- What category of things?
- What will it be used for?
- What makes an item useful vs. useless?
- Target size (minimum 50, ideally 100+)

### Step 2: Seed with Obvious Examples
Start with 10-20 items that come to mind immediately. These are the "available" options—the ones that would occur to anyone. They're valid but not sufficient.

### Step 3: Research for Variety
Use available sources to expand beyond obvious:

**Kiwix/Wikipedia:**
- Category pages (e.g., "Category:Occupations")
- List articles (e.g., "List of unusual deaths")
- Related articles that branch into unexpected territory

**Pattern: Dimensional expansion**
- Pick a dimension the seed list lacks
- Research specifically in that dimension
- Add 10-20 items that fill the gap

### Step 4: Filter for Quality
Remove items that are:
- Too vague to be useful
- Too similar to existing items
- Culturally specific without being interesting
- Requiring too much explanation

### Step 5: Format for Use
Output as JSON array for use with entropy.ts:

```json
{
  "list_name": [
    "Item one",
    "Item two",
    "Item three"
  ]
}
```

## Available Tools

### validate-list.ts
Analyzes a list for quality and variety.

```bash
deno run --allow-read scripts/validate-list.ts list.json

# Check specific list in a file
deno run --allow-read scripts/validate-list.ts data.json professions
```

**Reports:**
- Total count
- Duplicate check
- Average item length (too short = vague, too long = unwieldy)
- Variety assessment (if dimensions specified)

### merge-lists.ts
Combines multiple list sources, deduplicates, and formats.

```bash
deno run --allow-read scripts/merge-lists.ts source1.json source2.json --output combined.json
```

## Research Prompts

When you need to research a specific category, use prompts like:

**For professions:**
"Find 20 professions in [industry] that most people don't know exist. Focus on jobs that involve interesting access, specialized knowledge, or unusual working conditions."

**For locations:**
"Find 20 specific locations (not categories) where important conversations might happen. Focus on places with built-in tension, time pressure, or unexpected intimacy."

**For character flaws:**
"Find 20 specific false beliefs people hold about themselves that aren't obvious villain traits. Focus on beliefs that feel protective but are actually limiting."

## Example: Building a Professions List

### Starting Seed (obvious)
- Doctor, lawyer, teacher, police officer, firefighter...

### Dimensional Gap Analysis
- Missing: Niche technical jobs
- Missing: Service jobs with unusual access
- Missing: Jobs that involve secrets
- Missing: Jobs most people don't know exist

### Research Expansion
Kiwix search: "List of occupations" → Category pages → specific unusual jobs

**Add from research:**
- Elevator inspector (access to buildings)
- Crime scene cleaner (aftermath, not crime)
- Ethical hacker (knows vulnerabilities)
- Cult deprogrammer (understands manipulation)
- Foley artist (creates reality from nothing)
- Patent examiner (sees innovations before public)

### Quality Filter
Remove:
- "Businessperson" (too vague)
- "TikTok influencer" (too trendy, will date)
- "Alchemist" (wrong era unless fantasy)

### Final Check
- 80+ items? ✓
- Multiple industries? ✓
- Mix of status levels? ✓
- Unexpected options? ✓

## Integration with Entropy Tools

Lists built with this skill go into:
- `story-sense/data/` for fiction-specific lists
- Can be loaded via `entropy.ts --file`

**Naming convention:**
- `[category]-[specificity].json`
- Examples: `professions-unusual.json`, `locations-liminal.json`, `objects-evidence.json`

## What You Do

1. Clarify what list is needed and how it will be used
2. Seed with obvious examples
3. Research to expand variety
4. Filter for quality
5. Format as JSON
6. Validate with tools
7. Document the list's intended use

## What You Don't Do

- Generate random items (that's what the entropy script does)
- Create lists without research (leads to obvious-only items)
- Include items that require extensive explanation
- Prioritize quantity over quality (100 good items > 500 mediocre ones)

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found or no entry for this skill, **ask the user first**:
   - "Where should I save output from this list-builder session?"
   - Suggest: `data/` or `story-sense/data/` for entropy lists
4. Store the user's preference:
   - In `context/output-config.md` if context network exists
   - In `.list-builder-output.md` at project root otherwise

### Primary Output

For this skill, persist:
- **The list itself** - JSON format for entropy.ts use
- **Research sources** - where items came from
- **Dimensional analysis** - what variety dimensions are covered
- **Usage documentation** - what the list is for

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Final list (JSON) | Discussion of list purpose |
| Research sources | Iteration on items |
| Quality analysis | Real-time feedback |
| Documentation | Category refinement |

### File Naming

Pattern: `{category}-{specificity}.json`
Example: `professions-unusual.json`
