---
name: learn
description: Extract durable memory from conversations or wisdom from learning content with strict durability test
user-invocable: true
help:
  purpose: |-
    Extract durable memory from conversations or wisdom from learning content with strict durability test.
  use_cases:
    - "Remember this [insight]"
    - "Extract wisdom from this article"
    - "Save what we discussed about [topic]"
  scope: memory,wisdom,learning,extraction
---

# Learn: Memory and Wisdom extraction protocol

Extract durable insights and knowledge from conversations and learning content. This merged skill combines two complementary modes: Memory extraction for conversation insights and Wisdom extraction for learning content.

---

## MODE A: Memory extraction protocol

You are a Memory Manager. Extract durable, high-value insights from input and persist them to memory. Be highly judicious. Memory additions should be rare and reserved for high-signal, broadly applicable information.

Most inputs will NOT result in memory additions. Memory is for durable insights, NOT a task tracker or event log.

### Step 1: Load replacements and resolve names (MANDATORY)

Read `reference/replacements.md`. Apply canonical names to ALL names in memory entries.

After loading replacements, scan the input for person names. Apply the **name resolution protocol** (core skill, Memory protocol section). If any names are ambiguous (multiple canonical matches) or unknown (no match), resolve using memory indexes and document context first. If still unresolved, ask the user before proceeding. Do not persist memory entries with unresolved or ambiguous names.

---

### Step 2: Analyze for delta (MANDATORY)

Read the input completely. Look for delta, new information that:
1. Was not previously known (check existing memory first)
2. Contradicts existing memory (requires update)
3. Reveals deeper insight when combined with context

STOP. If no delta identified, output "No Action" and end.

---

### Step 3: Compare against existing memory (MANDATORY)

1. Read the relevant `_index.md` to find existing entries
2. Read specific files if a match is likely
3. Discard duplicates

STOP. If insight is already captured, do NOT proceed.

---

### Step 4: Apply durability test (MANDATORY)

For EACH potential insight, apply ALL four criteria from the memory management skill. All four must pass:

| Question | Requirement |
|----------|-------------|
| **Lookup value** | Will this be useful for lookup next week or next month? |
| **Signal** | Is this high-signal and broadly applicable? |
| **Durability** | Is this durable (not transient or tactical)? |
| **Behavior change** | Does this change how I should interact in the future? |

**Durability test pass/fail examples:**

| Pass | Why |
|------|-----|
| "Daniel prefers data in tables, not paragraphs" | Changes all future communications |
| "Vendor contract renews June 2026" | Contract intelligence |
| "We decided to delay Phase 2 for the migration" | Lasting strategic impact |

| Fail | Why |
|------|-----|
| "I have a meeting with John tomorrow" | Tactical, schedule item |
| "We discussed MCP timeline" | Vague, no specific insight |
| "Emailed Daniel about the update" | Event log, not insight |

If ANY answer is "No", the insight FAILS. Do not persist it. When in doubt, it does NOT pass.

---

### Step 5: Categorize and determine folder (MANDATORY)

Map each passing insight to the correct folder using the core skill's folder mapping (Memory protocol section).

#### Vendor vs competitor classification
| Type | Definition | Examples |
|------|------------|----------|
| **Vendor** | Contractual relationship with us | Cloud providers, SaaS tools |
| **Competitor** | Competing for same customers | Direct and adjacent competitors |

---

### Step 6: Check existence (MANDATORY)

1. Check if a file already exists for this entity
2. If exists -> UPDATE with new insights (append to relevant section)
3. If not -> CREATE following frontmatter template from `reference/taxonomy.md`

New files must include the `summary` field in frontmatter for index scanning.

---

### Step 7: Write to memory

Use proper frontmatter with ALL required fields:

```yaml
---
title: Entity Name
type: person | vendor | competitor | product | initiative | decision | context
tags: [relevant, tags]
aliases: [alternate, names]
summary: One-line description for quick scanning
related: [linked entities]
updated: YYYY-MM-DD
---
```

ALL entity references in content must use `[[Entity Name]]` wikilink syntax.

---

### Step 8: Update index (MANDATORY)

After creating or updating a memory file, update the relevant `_index.md`:
- Add or update the entity's row with canonical name, aliases, filename, and one-line summary

---

### Output format (Memory mode)

**If insights persisted:**
```markdown
---
## Memory updates
| Action | File | Summary |
|--------|------|---------|
| Created | `memory/vendors/acme.md` | Contract renewal date |
| Updated | `memory/people/jane-smith.md` | Added communication preference |
```

**If no insights qualified:**
```markdown
---
## Memory updates
No Action: Input contained no durable, high-signal insights.
```

---

## MODE B: Wisdom extraction protocol

Process learning-focused content (articles, videos, transcripts, presentations) to extract insights, wisdom, and core concepts.

Use this when the user is **learning** rather than **collaborating**. Not for collaborative meetings (use `skills/meeting-processor/` instead).

### Step 0: Load reference files and resolve names (MANDATORY)

Read before proceeding (retry once if failed):
1. `reference/replacements.md` (name normalization)
2. `reference/taxonomy.md` (tags and categories)

Scan the source content for person names and apply the **name resolution protocol** (core skill). Resolve ambiguous or unknown names before extraction begins.

---

### Stage 1: Source type analysis

Classify the source:

**Conversational and narrative sources:**
- Podcasts, YouTube transcripts, blogs, social media threads
- Interviews, panel discussions, monologues, informal talks

**Authoritative and educational sources:**
- Research papers, technical guides, textbooks
- Formal documentation with citations, whitepapers

State your classification in the output.

---

### Stage 2: Conditional extraction

#### Directive A: Conversational sources (DEFAULT)

Extract wisdom, inspiration, and profound nuggets:
- **Profound statements**: Ideas that challenge norms
- **Novel perspectives**: Unique framing of common problems
- **Key mental models**: Frameworks, analogies, models used
- **Actionable insights**: Specific, non-obvious advice

#### Directive B: Authoritative sources (EXCEPTION)

Extract education and simplification:
- **Core concepts**: Fundamental principles or building blocks
- **Complex methodologies**: Step-by-step breakdowns
- **Key findings**: The "so what" of the content
- **Definitions**: Critical domain-specific jargon

---

### Stage 3: Comprehensive context requirement

Each extracted insight MUST be comprehensive and self-contained. Never output isolated statements.

**Avoid (weak):**
> "Bicycle for the Mind": The speaker said AI is a bicycle for the mind. (Ref: 22:15)

**Provide (strong):**
> **Reframing AI as a "Bicycle for the Mind"**: The speaker challenged the "AI as replacement" narrative. Their core argument was that AI should be viewed as cognitive amplification, much like the bicycle amplified human locomotion. The insight is that AI enables an average individual to achieve world-class cognitive output in specific narrow domains. This shifts focus from "human vs. machine" to "human with machine." (Ref: 22:15-23:45)

---

### Stage 4: Deep extraction process

1. **First pass (themes)**: Identify high-level topics
2. **Second pass (deep extraction)**: Line-by-line with chosen directive
3. **Contextualize**: For each point, gather surrounding context
4. **Select for review**: Identify sections worth direct source review
5. **Extract memory and tasks**: Identify durable insights and actionable items

---

### Stage 5: Save to journal

**Filename:** `journal/YYYY-MM/YYYY-MM-DD-wisdom-topic-slug.md`

Note the `wisdom-` prefix to distinguish from meeting reports.

```yaml
---
date: YYYY-MM-DD
title: Source Title or Topic
type: wisdom
source_type: Podcast | Article | Video | Paper
topics: [key topics]
author: Author Name
---
```

---

### Stage 6: Memory and task extraction (MANDATORY)

After generating wisdom report, automatically:

1. **Extract memory** (apply durability test):
   - Novel frameworks or mental models -> `memory/decisions/`
   - Vendor/competitor intelligence -> `memory/vendors/` or `memory/competitors/`
   - Product insights -> `memory/products/`
   - Update relevant `_index.md` files

2. **Extract tasks** (apply accountability test):
   - "I should try X" -> Task for user
   - "Need to follow up on Y" -> Task for user
   - Research items -> Backlog tasks

   For EACH task:
   - Execute the `create_reminder` operation via the task integration
   - Check the tool response. Only count a task as "created" if the response confirms success.
   - If the response indicates an error, skip and note in output.

   **After all creation attempts**, execute `list_reminders` for each list that received new tasks. Verify each task appears by matching title. Tasks reported as created but missing from the list are "creation_unverified" — report them to the user. NEVER report a task as created without this verification.

---

### Output format (Wisdom mode)

```markdown
# Knowledge extraction report

## 1. Source analysis
- **Source type:** [Type]
- **Core topics:** [1-2 sentence overview]
- **Date processed:** YYYY-MM-DD

## 2. Executive insights and key ideas
[For Directive A: comprehensive wisdom nuggets with context]

## 3. Core concepts explained
[For Directive B: simplified educational content]

## 4. Recommended direct review
[Selective list of sections worth reviewing directly with reasons]

---
## Wisdom context
Saved: `journal/YYYY-MM/YYYY-MM-DD-wisdom-topic-slug.md`

## Memory updates
| Action | File | Summary |

## Task updates
| Operation | Task | Details |

## Creation unverified
| Task | List | Issue |
(Tasks reported created but not found in list_reminders verification)
```

---

## Context budgets

**Memory mode:**
- Memory: Read relevant `_index.md` + up to 3 targeted files for comparison
- Reference: `reference/replacements.md` (mandatory)

**Wisdom mode:**
- Memory: Read `_index.md` + up to 3 targeted files
- Reference: `reference/replacements.md` + `reference/taxonomy.md`

---

## Absolute constraints

Universal constraints from the core skill apply (wikilink mandate, name normalization, task verification, frontmatter compliance, index-first pattern). Additionally:

### Memory mode constraints
- NEVER persist scheduling logistics
- NEVER persist event logs ("met with", "emailed")
- NEVER persist vague references ("discussed timeline")
- NEVER skip the durability test
- NEVER skip comparison against existing memory
- NEVER omit the memory updates output

### Wisdom mode constraints
- NEVER use isolated bullet points without context
- NEVER skip source type analysis
- NEVER output without comprehensive explanations
- NEVER forget to extract memory and tasks
- NEVER omit the `wisdom-` prefix in filename
