---
context: fork
description: Create Book note with knowledge compounding through spawned Concept/Pattern/Theme nodes
model: sonnet
---

# /book

Create a Book note with reading tracking and knowledge compounding through spawned Concept/Pattern/Theme nodes. Works for both quick capture and comprehensive PDF processing.

## Usage

```
/book <title>
/book <title> by <author>
/book <title> --status reading
/book <title> --spawn                    # Identify concepts/patterns/themes to spawn
/book <title> --spawn "Data Contracts"   # Spawn single specific node
/book <title> --spawn --concepts-only    # Only spawn Concepts
/book <title> --spawn --patterns-only    # Only spawn Patterns
/book <title> --spawn --themes-only      # Only spawn Themes
/book <title> --spawn --preview          # Preview content before creating
/book <title> --spawn --force            # Re-analyse, ignore existing spawned nodes
/book <title> --spawn --enrich           # Use web search to enrich definitions
/book <title> --pdf <path>               # Process PDF with knowledge extraction
```

## Modes

| Mode            | Trigger             | Model  | Description                                    |
| --------------- | ------------------- | ------ | ---------------------------------------------- |
| **Quick**       | `/book <title>`     | Haiku  | Fast capture for reading tracking              |
| **Spawn**       | `--spawn`           | Sonnet | Identify and create spawned knowledge nodes    |
| **Incremental** | `--spawn "Name"`    | Sonnet | Spawn a single specific node                   |
| **Preview**     | `--spawn --preview` | Sonnet | Preview nodes before creation                  |
| **PDF Process** | `--pdf <path>`      | Sonnet | Full PDF extraction with knowledge compounding |
| **Update**      | On existing book    | Sonnet | Add spawned nodes to existing Book note        |

## Instructions

### Mode 1: Quick Capture (Haiku)

For simple reading tracking without knowledge extraction.

1. **Parse the input**:
   - Extract book title (required)
   - Extract author if provided with "by"
   - Extract optional flags: `--status`, `--rating`, `--format`

2. **Create the note** at root: `Book - <Title>.md`

3. **Populate basic frontmatter** (see template below)

4. **Report creation**:
   ```
   Created: Book - <Title>.md
   Status: <status>
   Tip: Use `/book <title> --spawn` to identify concepts and patterns to extract
   ```

---

### Mode 2: Knowledge Spawn (Sonnet)

For identifying and creating standalone knowledge nodes from a book.

#### Step 1: Read Existing Content

If the book note already exists, read it to understand the content.

```
Read: Book - <Title>.md
```

If the book note doesn't exist, use web search to gather information about the book's content and key contributions.

#### Step 2: Check for Existing Spawned Nodes (Idempotent Handling)

**IMPORTANT:** Before analysing for candidates, check if this book already has spawned nodes.

```
Read the book note frontmatter for `spawnedNodes` field
```

| Situation                              | Action                                         |
| -------------------------------------- | ---------------------------------------------- |
| No existing `spawnedNodes`             | Proceed with full analysis                     |
| Has `spawnedNodes` + no `--force` flag | Skip existing, analyse for NEW candidates only |
| Has `spawnedNodes` + `--force` flag    | Re-analyse all, may update existing nodes      |

When running incrementally:

- Report: "Found X existing spawned nodes, checking for new candidates..."
- Only present NEW candidates that aren't already spawned
- Append new nodes to `spawnedNodes` (don't replace)

#### Step 3: Check Vault for Existing Coverage

**CRITICAL:** Before proposing spawn candidates, search the vault to avoid duplicates.

For each potential candidate:

1. **Exact match search:**

   ```
   Glob "Concept - {{candidate name}}*"
   Glob "Pattern - {{candidate name}}*"
   Glob "Theme - {{candidate name}}*"
   ```

2. **Partial/related match search:**

   ```
   Grep "{{candidate term}}" --glob "*.md" --output_mode files_with_matches
   ```

3. **SQLite FTS search (if available):**
   ```
   /q {{candidate term}}
   ```

**Decision Matrix:**

| Search Result                                       | Action                                                  |
| --------------------------------------------------- | ------------------------------------------------------- |
| Exact match exists                                  | **Link** to existing node, don't spawn                  |
| Partial coverage (mentioned but not dedicated node) | Offer to **enrich** existing or spawn new               |
| Related concept exists                              | Add to `nodeRelationships`, may still spawn if distinct |
| No coverage                                         | Add to **spawn candidates**                             |

Report search results:

```
Vault Coverage Check:
- "Data Mesh" → No existing node ✓ (will spawn)
- "Data Product" → Found Concept - Data Product Anatomy.md (will link, not spawn)
- "Self-Serve Platform" → Mentioned in 3 notes but no dedicated node ✓ (will spawn)
```

#### Step 4: Analyse Content for Candidates

Identify knowledge candidates with metadata:

1. **Core Concepts** (What is X?)
   - Technical terms needing explanation
   - Domain concepts referenced elsewhere
   - Frameworks or models introduced
   - **Capture:** Name, definition, source chapters, confidence level

2. **Patterns** (How to do X)
   - Architectural patterns described in detail
   - Design patterns with problem/solution structure
   - Process patterns for development or architecture
   - **Capture:** Name, intent, source chapters, confidence level

3. **Themes** (Cross-cutting concerns)
   - Paradigm shifts (e.g., "Decentralisation", "Platform Thinking")
   - Strategic directions spanning multiple concepts
   - Philosophical underpinnings
   - **Capture:** Name, scope, source chapters, confidence level

For each candidate, determine:

| Field               | Description                                   |
| ------------------- | --------------------------------------------- |
| `name`              | Node title                                    |
| `type`              | Concept, Pattern, or Theme                    |
| `definition`        | 1-2 sentence definition                       |
| `sourceChapters`    | Which chapters cover this (array of numbers)  |
| `sourcePages`       | Page range if known (string)                  |
| `sourcePrimary`     | Is this book THE authoritative source?        |
| `confidence`        | Derived from source quality (see rules below) |
| `relatedCandidates` | Other candidates this relates to              |

#### Step 5: Determine Confidence Levels

**Confidence Inheritance Rules:**

| Source Quality     | Criteria                                                    | Spawned Confidence |
| ------------------ | ----------------------------------------------------------- | ------------------ |
| **Authoritative**  | Author coined/invented the term, book is THE primary source | `high`             |
| **Deep treatment** | Dedicated chapter(s), comprehensive coverage                | `high`             |
| **Substantial**    | Multiple sections, detailed explanation                     | `medium`           |
| **Referenced**     | Mentioned, explained briefly                                | `medium`           |
| **Brief mention**  | Passing reference, assumes prior knowledge                  | `low`              |

**Examples:**

- "Data Mesh" in Dehghani's book → `high` (she coined it)
- "Data Mesh" in a survey book → `medium` (secondary source)
- "Microservices" in a Data Mesh book → `medium` (referenced, not primary topic)

#### Step 6: Map Inter-Node Relationships

Before presenting candidates, map how they relate to EACH OTHER:

| From                 | To           | Relationship Type       |
| -------------------- | ------------ | ----------------------- |
| Data Product         | Data Mesh    | "component of"          |
| Data Quantum         | Data Product | "implements"            |
| Self-Serve Platform  | Data Mesh    | "enables"               |
| Federated Governance | Data Mesh    | "governs"               |
| Data Contracts       | Data Product | "defines interface for" |

This ensures spawned nodes link to siblings, not just back to the source book.

#### Step 7: Present Candidates with Options

Use AskUserQuestion with full context:

```
Question: "Which knowledge nodes should I create from '{{Book Title}}'?"
Header: "Spawn Nodes"
Options:
  1. "All recommended ({{N}} nodes)" (Recommended)
     Description: "{{X}} Concepts, {{Y}} Patterns, {{Z}} Themes"
  2. "Concepts only ({{X}} nodes)"
     Description: "{{list concept names}}"
  3. "Patterns only ({{Y}} nodes)"
     Description: "{{list pattern names}}"
  4. "Themes only ({{Z}} nodes)"
     Description: "{{list theme names}}"
  5. "Let me choose"
     Description: "I'll select specific nodes"
```

If user selects "Let me choose", use multiSelect question listing each candidate with its type and confidence.

#### Step 7b: Preview Mode (if --preview flag)

If `--preview` is requested, before creating each node show:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Preview: Concept - Data Product

> **Definition:** The smallest unit of analytical data that can be
> independently deployed, consumed, and governed as a product.

**Source:** Chapters 3, 11-14 | **Confidence:** high

**Key Characteristics:**
- Discoverable, addressable, understandable
- Owned by a domain team with product thinking
- Has defined interfaces (input/output ports)

**Related Nodes:**
- [[Concept - Data Mesh]] (component of)
- [[Concept - Data Quantum]] (implemented by)
- [[Pattern - Data Contracts]] (interfaces defined by)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Options: [Create] [Skip] [Edit Definition]
```

Use AskUserQuestion for each preview with Create/Skip/Edit options.

#### Step 8: Web Enrichment (if --enrich flag)

If `--enrich` is requested, for each approved candidate:

```
WebSearch: "{{concept name}} definition {{author name if relevant}}"
```

Use results to:

- Confirm/refine the definition
- Add related concepts not covered in the book
- Identify authoritative external sources
- Note any contradicting viewpoints

Add enrichment to the spawned node:

```yaml
# In spawned node frontmatter
enrichedFrom:
  - url: "{{source URL}}"
    retrieved: { { DATE } }
```

#### Step 9: Create Spawned Nodes

For each approved candidate, create the appropriate node type using templates below.

**Creation Order:**

1. Themes first (broadest scope)
2. Concepts second (foundational)
3. Patterns last (apply concepts)

This ensures nodes can reference each other correctly.

**For each node:**

1. Create file with appropriate template
2. Populate all fields including:
   - `sourceBook`, `sourceChapters`, `sourcePages`, `sourcePrimary`
   - `confidence` based on inheritance rules
   - `nodeRelationships` including sibling nodes AND source book
3. Verify bidirectional links

#### Step 10: Update Book Note

Add/update the book's frontmatter and body:

**Frontmatter:**

```yaml
spawnedNodes:
  - "[[Concept - {{Name}}]]"
  - "[[Pattern - {{Name}}]]"
  - "[[Theme - {{Name}}]]"
```

**Body - Add "Spawned Knowledge" section:**

```markdown
## Spawned Knowledge

This book is a primary source for the following knowledge nodes:

### Themes

| Node          | Description     |
| ------------- | --------------- |
| [[Theme - X]] | {{description}} |

### Core Concepts

| Node            | Description     | Chapters |
| --------------- | --------------- | -------- |
| [[Concept - X]] | {{description}} | Ch. 2-3  |

### Implementation Patterns

| Node            | Description     | Chapters |
| --------------- | --------------- | -------- |
| [[Pattern - X]] | {{description}} | Ch. 10   |
```

#### Step 11: Completion Report

Report:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Book Spawn Complete: {{Book Title}}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Book Note:** Book - {{Title}}.md

**Spawned Knowledge Nodes:**

Themes ({{N}}):
- Theme - X — {{description}}

Concepts ({{N}}):
- Concept - X — {{description}} (Ch. 2-3, high confidence)
- Concept - Y — {{description}} (Ch. 5, medium confidence)

Patterns ({{N}}):
- Pattern - X — {{description}} (Ch. 10)

**Linked to Existing:**
- [[Concept - Existing]] — Added as related concept

**Skipped (Already Exist):**
- "Data Product Anatomy" → Linked to existing Concept - Data Product Anatomy.md

**Key Takeaways:**
- {{takeaway 1}}
- {{takeaway 2}}
- {{takeaway 3}}

**Suggested Next Books:**
- [[Book - Related Book 1]] — {{why relevant}}
- [[Book - Related Book 2]] — {{why relevant}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Mode 3: Incremental Spawn

When user specifies a single node: `/book "Data Mesh" --spawn "Data Contracts"`

1. Read existing book note
2. Search vault for existing "Data Contracts" coverage
3. If not found, create single Concept or Pattern (determine type from context)
4. Update book's `spawnedNodes` field (append)
5. Report single node creation

---

### Mode 4: PDF Processing (Sonnet)

For full book PDF extraction with knowledge compounding.

1. **Process PDF** using docling (see `/pdf-to-page` skill)
2. **Extract metadata**: author, publisher, ISBN, page count, TOC
3. **Create Book note** with full structure
4. **Run spawn workflow** (Steps 2-11 above)
5. **Link bidirectionally**

---

## Templates

### Book Note Template

**Filename:** `Book - {{Title}}.md`
**Location:** Vault root

```markdown
---
type: Book
pillar: node
title: "{{title}}"
aliases:
  - "{{short title}}"
created: {{DATE}}
modified: {{DATE}}
tags:
  - {{relevant hierarchical tags}}

# Book Metadata
author: {{author}}
coAuthors: []
editor: null
isbn: null
publisher: null
publishedYear: null
pages: null
genre: [{{non-fiction, technology, etc.}}]
series: null
seriesNumber: null

# Reading Tracking
readingStatus: {{to-read|reading|completed|abandoned|reference}}
startDate: null
finishDate: null
rating: null
rereadCount: 0
format: {{physical|kindle|pdf|audiobook}}

# Content
coreThesis: "{{1-2 sentence main contribution}}"
keyTakeaways:
  - "{{takeaway 1}}"
  - "{{takeaway 2}}"
  - "{{takeaway 3}}"
favouriteQuotes: []

# Source & Links
source: owned
goodreadsUrl: null
amazonUrl: null
attachedPdf: null

# Knowledge Compounding
spawnedNodes:
  - "[[Concept - {{Concept 1}}]]"
  - "[[Pattern - {{Pattern 1}}]]"
  - "[[Theme - {{Theme 1}}]]"

# Relationships
nodeRelationships:
  - "[[Concept - {{Related existing concept}}]]"
entityRelationships:
  - "[[Person - {{Author if notable}}]]"
  - "[[Organisation - {{Publisher or company}}]]"
relatedBooks:
  - "[[Book - {{Related book}}]]"
recommendedBy: null

# Quality
summary: "{{one-line summary}}"
confidence: high
freshness: current
source: primary
verified: true
reviewed: {{DATE}}
keywords:
  - {{keyword1}}
  - {{keyword2}}
---

# {{title}}

> **Author**: {{author}}
> **Status**: {{status}}
> **Rating**: {{star rating if provided}}
> **Source**: [[Attachments/{{pdf if attached}}|PDF]]

## Core Thesis

{{1-2 paragraphs explaining the main argument or contribution}}

## Why Read This Book?

{{2-3 sentences on relevance and value}}

## Key Takeaways

{{For each major insight, provide context}}

### 1. {{Takeaway Title}}

{{Explanation with context from the book}}

### 2. {{Takeaway Title}}

{{Explanation with context}}

## Book Structure

{{Part/Chapter outline with brief descriptions}}

### Part I: {{Title}}

- **Chapter 1**: {{Title}} - {{brief description}}
- **Chapter 2**: {{Title}} - {{brief description}}

## Key Concepts

| Concept       | Description          |
| ------------- | -------------------- |
| {{concept 1}} | {{brief definition}} |
| {{concept 2}} | {{brief definition}} |

## Favourite Quotes

> "{{quote 1}}"
> — p. {{page}}

> "{{quote 2}}"
> — p. {{page}}

## Spawned Knowledge

This book is a primary source for the following knowledge nodes:

### Themes

| Node                 | Description     |
| -------------------- | --------------- |
| [[Theme - {{Name}}]] | {{description}} |

### Core Concepts

| Node                   | Description     | Chapters  |
| ---------------------- | --------------- | --------- |
| [[Concept - {{Name}}]] | {{description}} | Ch. {{N}} |

### Implementation Patterns

| Node                   | Description     | Chapters  |
| ---------------------- | --------------- | --------- |
| [[Pattern - {{Name}}]] | {{description}} | Ch. {{N}} |

## Relevance to Your Work

{{How this relates to Solutions Architecture, your projects, or current work. Include links to related vault content.}}

## Related

- [[Book - {{Related book}}]] — {{relationship}}
- {{wiki-links to related vault notes}}

## Chapter Notes

### Chapter 1: {{Title}}

{{User's notes - leave blank for user}}
```

---

### Spawned Concept Template

**Filename:** `Concept - {{Name}}.md`
**Location:** Vault root

Create for "What is X?" knowledge - definitions, frameworks, models.

```markdown
---
type: Concept
pillar: node
title: "{{Name}}"
aliases:
  - "{{alternative names}}"
created: { { DATE } }
modified: { { DATE } }
tags:
  - { { relevant hierarchical tags } }

# Source Provenance
sourceBook: "[[Book - {{Source Book}}]]"
sourceChapters: [{ { chapter numbers } }]
sourcePages: "{{page range}}"
sourcePrimary: { { true if this book is THE authoritative source } }

# Relationships
nodeRelationships:
  - "[[Book - {{Source Book}}]]"
  - "[[Concept - {{Sibling concept from same book}}]]"
  - "[[Pattern - {{Related pattern}}]]"
entityRelationships: []

# Quality
description: "{{1-2 sentence definition}}"
summary: "{{one-line summary}}"
confidence: { { high|medium|low based on inheritance rules } }
freshness: current
source: { { primary if sourcePrimary else secondary } }
verified: false
reviewed: { { DATE } }
keywords:
  - { { keyword1 } }
  - { { keyword2 } }
---

# {{Name}}

> **Definition:** {{Clear, concise definition}}

## Overview

{{2-3 paragraphs explaining the concept, derived from the book but written to be standalone}}

## Key Characteristics

- {{characteristic 1}}
- {{characteristic 2}}
- {{characteristic 3}}

## Examples

{{Real-world examples from the book or added for clarity}}

## Why It Matters

{{Business/technical impact, relevance to architecture work}}

## Related Concepts

- [[Concept - {{Sibling 1}}]] — {{relationship}}
- [[Concept - {{Sibling 2}}]] — {{relationship}}
- [[Pattern - {{Related pattern}}]] — {{relationship}}

## Sources

- [[Book - {{Source Book}}]] — Ch. {{chapters}} ({{primary source | secondary source}})
- {{Additional references if known}}
```

---

### Spawned Pattern Template

**Filename:** `Pattern - {{Name}}.md`
**Location:** Vault root

Create for "How to do X" knowledge - approaches, architectures, solutions.

```markdown
---
type: Pattern
pillar: node
title: "{{Name}}"
aliases: []
created: { { DATE } }
modified: { { DATE } }
tags:
  - { { relevant hierarchical tags } }
patternType: architecture | integration | data | security | process

# Source Provenance
sourceBook: "[[Book - {{Source Book}}]]"
sourceChapters: [{ { chapter numbers } }]
sourcePages: "{{page range}}"
sourcePrimary: { { true|false } }

# Relationships
nodeRelationships:
  - "[[Book - {{Source Book}}]]"
  - "[[Concept - {{Related concept}}]]"
  - "[[Pattern - {{Sibling pattern}}]]"
entityRelationships: []

# Quality
description: "{{1-2 sentence description}}"
summary: "{{one-line summary}}"
confidence: { { high|medium|low } }
freshness: current
verified: false
reviewed: { { DATE } }
---

# {{Name}}

> **Intent:** {{What problem does this pattern solve?}}

## Context

{{When to use this pattern}}

## Problem

{{The specific challenge this addresses}}

## Solution

{{How the pattern works}}

## Implementation

{{Key steps or components}}

## Consequences

**Benefits:**

- {{benefit 1}}
- {{benefit 2}}

**Trade-offs:**

- {{trade-off 1}}
- {{trade-off 2}}

## Examples

{{Real-world examples from the book}}

## Related Patterns

- [[Pattern - {{Sibling}}]] — {{relationship}}
- [[Concept - {{Related concept}}]] — {{relationship}}

## Sources

- [[Book - {{Source Book}}]] — Ch. {{chapters}}
```

---

### Spawned Theme Template

**Filename:** `Theme - {{Name}}.md`
**Location:** Vault root

Create for cross-cutting concerns, paradigm shifts, strategic directions.

```markdown
---
type: Theme
pillar: node
title: "{{Name}}"
aliases: []
created: { { DATE } }
modified: { { DATE } }
tags:
  - { { relevant hierarchical tags } }
scope: { { enterprise|department|project|domain } }

# Source Provenance
sourceBook: "[[Book - {{Source Book}}]]"
sourceChapters: [{ { chapter numbers } }]
sourcePrimary: { { true|false } }

# Relationships
nodeRelationships:
  - "[[Book - {{Source Book}}]]"
  - "[[Concept - {{Manifestation of this theme}}]]"
  - "[[Pattern - {{Implements this theme}}]]"
entityRelationships: []

# Quality
description: "{{1-2 sentence description}}"
summary: "{{one-line summary}}"
confidence: { { high|medium|low } }
freshness: current
verified: false
reviewed: { { DATE } }
keywords:
  - { { keyword1 } }
  - { { keyword2 } }
---

# {{Name}}

> **Essence:** {{One sentence capturing the core of this theme}}

## Overview

{{2-3 paragraphs explaining the theme and its significance}}

## Why This Theme Matters

{{Business/strategic impact, why this is a cross-cutting concern}}

## Manifestations

This theme appears in several forms:

### As Concepts

- [[Concept - {{X}}]] — {{how this concept embodies the theme}}
- [[Concept - {{Y}}]] — {{how this concept embodies the theme}}

### As Patterns

- [[Pattern - {{X}}]] — {{how this pattern implements the theme}}
- [[Pattern - {{Y}}]] — {{how this pattern implements the theme}}

## Tensions & Trade-offs

{{What this theme trades off against, competing concerns}}

## Evolution

{{How this theme has evolved or is evolving in the industry}}

## Related Themes

- [[Theme - {{Related}}]] — {{relationship}}

## Sources

- [[Book - {{Source Book}}]] — Primary exposition
- {{Additional sources}}
```

---

## Knowledge Compounding Guidelines

### When to Spawn a Concept Node

✅ **DO spawn** when:

- Technical terms that need standalone explanation (e.g., "Data Mesh", "Microservices")
- Frameworks or models introduced by the book (e.g., "SOLID Principles", "CAP Theorem")
- Domain concepts that will be referenced from multiple notes
- Definitions that should persist as reusable knowledge
- The book is THE primary source for this term

❌ **DON'T spawn** when:

- Already covered by existing vault Concept (link instead)
- Too narrow or book-specific without broader applicability
- Simple terms that don't need standalone treatment
- Only briefly mentioned without sufficient detail

### When to Spawn a Pattern Node

✅ **DO spawn** when:

- Architectural patterns described in detail (e.g., "Strangler Fig", "Event Sourcing")
- Design patterns with clear problem/solution structure
- Reusable approaches applicable beyond this book's context
- Process patterns for software development or architecture

❌ **DON'T spawn** when:

- Already covered by existing vault Pattern (link instead)
- Book-specific examples without generalised applicability
- Patterns only briefly mentioned without sufficient detail

### When to Spawn a Theme Node

✅ **DO spawn** when:

- Paradigm shifts (e.g., "Decentralisation", "Product Thinking")
- Cross-cutting concerns spanning multiple concepts
- Strategic directions that inform multiple patterns
- Philosophical underpinnings of an approach

❌ **DON'T spawn** when:

- Too abstract to be actionable
- Just a label for a collection (use MOC instead)
- Already captured as a broader existing Theme

### Typical Spawn Counts

| Book Type                                | Themes | Concepts | Patterns |
| ---------------------------------------- | ------ | -------- | -------- |
| Technical deep-dive (e.g., "Data Mesh")  | 1-3    | 5-10     | 3-7      |
| Survey book (e.g., "Fundamentals of...") | 2-4    | 10-20    | 5-10     |
| Practical guide (e.g., "Building...")    | 1-2    | 3-7      | 5-15     |
| Business/strategy book                   | 2-4    | 3-5      | 1-3      |

---

## Confidence Inheritance Quick Reference

| Source Indicator                         | Confidence |
| ---------------------------------------- | ---------- |
| Author coined/created the term           | `high`     |
| Book is THE definitive source            | `high`     |
| Dedicated chapter(s) on the topic        | `high`     |
| Substantial coverage (multiple sections) | `medium`   |
| Referenced and explained                 | `medium`   |
| Brief mention, assumes prior knowledge   | `low`      |

---

## Status Values

| Status      | When to Use                      |
| ----------- | -------------------------------- |
| `to-read`   | On reading list, haven't started |
| `reading`   | Currently reading                |
| `completed` | Finished reading                 |
| `abandoned` | Started but won't finish         |
| `reference` | Reference book, dip in as needed |

## Rating Scale

| Rating | Meaning                     |
| ------ | --------------------------- |
| 5      | Life-changing, will re-read |
| 4      | Excellent, highly recommend |
| 3      | Good, worth reading         |
| 2      | Okay, some useful bits      |
| 1      | Not recommended             |

---

## Quality Standards

- **Always** check vault for existing coverage before spawning (Step 3)
- **Always** determine confidence based on source quality (Step 5)
- **Always** map inter-node relationships (Step 6)
- **Create spawned nodes** for knowledge that warrants standalone treatment
- **Link bidirectionally** - Book references spawned nodes, spawned nodes reference Book AND siblings
- **Provide meaningful analysis** - not just metadata extraction
- **Extract minimum 3 key takeaways** for substantive books
- **Use UK English** throughout
- **Use hierarchical tags** (e.g., `technology/aws` not just `aws`)
- **Include source provenance** (chapters, pages, primary flag)

---

## Example: Data Mesh Book

For "Data Mesh" by Zhamak Dehghani (author coined the paradigm):

**Themes:**

- `Theme - Decentralisation.md` - Shift from centralised to federated ownership
- `Theme - Product Thinking for Data.md` - Treating data as a product

**Concepts:**

- `Concept - Data Mesh.md` - The paradigm itself (high confidence, Ch. 1-5)
- `Concept - Data Product.md` - Core building block (high confidence, Ch. 3, 11-14)
- `Concept - Data Quantum.md` - Smallest deployable unit (high confidence, Ch. 9)
- `Concept - Federated Computational Governance.md` - Governance approach (high confidence, Ch. 5)
- `Concept - Domain Data Archetypes.md` - Source-aligned, aggregate, consumer-aligned (high confidence, Ch. 2)

**Patterns:**

- `Pattern - Self-Serve Data Platform.md` - Platform design pattern (high confidence, Ch. 4, 10)
- `Pattern - Data Contracts.md` - Producer-consumer agreements (high confidence, Ch. 14)
- `Pattern - Multiplane Data Platform.md` - Platform architecture (high confidence, Ch. 10)

All nodes:

- Link back to `Book - Data Mesh.md`
- Link to sibling nodes (e.g., Data Product → Data Mesh, Data Quantum)
- Have `sourcePrimary: true` (Dehghani is the authority)
- Have `confidence: high` (definitive source)

---

## Integration with /pdf-to-page

When using `/pdf-to-page` with `--book` flag, this skill's knowledge compounding is automatically applied:

1. PDF processed with docling
2. Book note created with extracted content
3. Knowledge candidates identified
4. User prompted to approve spawned nodes
5. Concept/Pattern/Theme nodes created
6. Bidirectional links established

---

## Troubleshooting

| Issue                            | Solution                                           |
| -------------------------------- | -------------------------------------------------- |
| "Already spawned" false positive | Use `--force` to re-analyse                        |
| Vault search too slow            | Use `/q` (SQLite) instead of Grep                  |
| Too many candidates              | Filter with `--concepts-only` or `--patterns-only` |
| Want to add one more concept     | Use `/book "Title" --spawn "Concept Name"`         |
| Preview taking too long          | Skip preview, approve all, edit after              |
