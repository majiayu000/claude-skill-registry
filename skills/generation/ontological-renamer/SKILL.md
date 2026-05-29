---
name: ontological-renamer
description: Renames projects and content with dense, meaningful ontological titles that describe essence and function. Combines 3-4 words using separator conventions (- for compound/close words, -- for distant concepts). Provides translations to Latin and Greek. Use when naming projects, repositories, systems, or concepts.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags: [naming, ontology, taxonomy, branding, translation]
---

# Ontological Renamer

Create dense, meaningful names for projects, systems, and concepts using ontological principles and classical language translations.

## When to Use

- Naming new projects or repositories
- Renaming existing systems
- Creating brand identities
- Naming concepts, patterns, or frameworks
- Building taxonomies and vocabularies

## Naming Methodology

### Step 1: Identify Essence

What IS the thing? (noun/subject)

```
Questions:
- What category does it belong to?
- What is its fundamental nature?
- What metaphor best describes it?

Examples:
- A collection → repository, vault, archive
- A process → engine, forge, factory
- A connection → bridge, link, weave
```

### Step 2: Identify Function

What does it DO? (verb/action)

```
Questions:
- What transformation does it perform?
- What problem does it solve?
- What capability does it provide?

Examples:
- Creates → forge, builder, generator
- Connects → bridge, link, mesh
- Organizes → lattice, matrix, graph
```

### Step 3: Identify Domain

What CONTEXT does it operate in?

```
Questions:
- What field or industry?
- What system or ecosystem?
- What users or actors?

Examples:
- AI/ML → agent, model, neural
- Development → code, build, deploy
- Knowledge → wisdom, expertise, craft
```

### Step 4: Combine

Form a 3-4 word compound that reads like a dense sentence.

```
Pattern: [Domain]-[Function]--[Essence]-[Modifier]

Examples:
- agent-skill--knowledge-forge
- code-craft--pattern-vault
- data-weave--insight-engine
```

## Separator Conventions

### Single Hyphen (-)

Use for magnetically close concepts that form a compound:

```
skill-bundle      → "bundle of skills" (compound noun)
agent-powered     → "powered by agents" (adjective)
code-craft        → "craft of coding" (compound noun)
knowledge-base    → "base of knowledge" (compound noun)
```

### Double Hyphen (--)

Use for conceptual distance or category separation:

```
agent-skills--knowledge-engine
├── agent-skills   (what it contains)
└── knowledge-engine (what it is)

frontend-toolkit--design-system
├── frontend-toolkit (domain)
└── design-system (function)
```

### Decision Matrix

| Relationship | Separator | Example |
|--------------|-----------|---------|
| Adjective + Noun | - | `smart-agent` |
| Noun + Noun (compound) | - | `skill-bundle` |
| Category + Instance | -- | `dev-tools--linter` |
| Domain + Function | -- | `ml-ops--model-registry` |
| What + How | -- | `data--transform-engine` |

## Word Selection Rules

### Ignore These Words

When forming names, filter out:

```
Articles: a, an, the
Prepositions: of, for, to, in, on, by, with
Conjunctions: and, or, but
```

### Prefer Strong Words

```
Strong Nouns:
✓ forge, vault, engine, lattice, codex
✗ thing, stuff, helper, manager

Active Verbs:
✓ forge, weave, craft, build
✗ do, make, handle, process

Specific Terms:
✓ authentication, pipeline, schema
✗ security, flow, structure
```

### Domain-Specific Vocabulary

| Domain | Strong Words |
|--------|--------------|
| AI/Agents | agent, model, neural, inference, swarm |
| Development | code, build, deploy, pipeline, stack |
| Data | schema, query, transform, pipeline |
| Security | vault, shield, guard, sentinel |
| Knowledge | codex, archive, wisdom, expertise |

## Classical Translations

### Translation Approach

1. Identify root concepts in English
2. Find Latin/Greek equivalents
3. Combine following classical morphology
4. Verify pronunciation and semantic accuracy

### Common Roots

| English | Latin | Greek |
|---------|-------|-------|
| skill | ars, artis | technē |
| knowledge | scientia | epistēmē, gnōsis |
| agent | agens, agentis | praktōr |
| forge | fabrica | chalkeion |
| vault | camera | thalamos |
| codex | codex | biblos |
| mastery | magisterium | epistasia |
| bundle | fasciculus | desmos |
| craft | ars | technē |
| power | potestas | dynamis |

### Translation Examples

```
skill-codex--agent-mastery
├── Latin: artium-codex--agentis-magisterium
└── Greek: technōn-biblos--praktoros-epistasia

agent-skill--knowledge-forge
├── Latin: ars-agentis--scientia-fabrica
└── Greek: technē-praktor--epistēmē-chalkeion
```

## Name Generation Process

### Example: AI Skills Repository

**Context:** A repository of skills that extend AI agent capabilities.

**Step 1: Essence**
- It's a collection (repository, vault, archive)
- It contains skills (capabilities, expertise)
- It's curated (codex, library)

**Step 2: Function**
- Extends capabilities (augment, enhance)
- Provides knowledge (expertise, mastery)
- Bundles together (bundle, collection)

**Step 3: Domain**
- AI agents (agent, autonomous)
- Skills/capabilities (skill, craft, art)
- Knowledge systems (knowledge, wisdom)

**Step 4: Generate Candidates**

```
1. agent-skill--knowledge-forge
   "A forge of knowledge for agent skills"

2. skill-codex--agent-mastery
   "A codex of skills for agent mastery"

3. capability-weave--agent-loom
   "A loom that weaves agent capabilities"

4. praxis-bundle--agent-expertise
   "A bundle of practical expertise for agents"

5. craft-matrix--agent-powers
   "A matrix of crafts that power agents"
```

**Step 5: Evaluate**

| Name | Clarity | Memorability | Domain Fit |
|------|---------|--------------|------------|
| skill-codex--agent-mastery | High | High | High |
| agent-skill--knowledge-forge | High | Medium | High |
| capability-weave--agent-loom | Medium | Medium | Medium |

**Winner:** `skill-codex--agent-mastery`

### Example: Authentication Library

**Context:** A library for handling user authentication.

**Candidates:**

```
1. auth-guard--access-sentinel
   "A sentinel guarding access through authentication"

2. identity-forge--credential-vault
   "A vault of credentials from an identity forge"

3. login-shield--session-keeper
   "A shield and keeper of login sessions"
```

## Output Format

When generating names, provide:

```yaml
naming_proposal:
  context: "Brief description of what's being named"

  candidates:
    - name: "english-compound--name"
      meaning: "What this name conveys"
      latin: "latin-translation"
      greek: "greek-translation"
      pros: ["list", "of", "strengths"]
      cons: ["list", "of", "weaknesses"]

  recommendation:
    name: "recommended-name"
    rationale: "Why this is the best choice"
```

## Anti-Patterns

### Avoid These

```
❌ Generic Names
   my-project, cool-tool, awesome-thing

❌ Overloaded Terms
   manager, handler, service, util

❌ Acronyms Without Meaning
   XYZPT, QWERT

❌ Too Long
   super-advanced-machine-learning-based-intelligent-agent-system

❌ Unclear Separators
   agent_skill-knowledge--forge (mixing _ and -)
```

### Prefer These

```
✓ Evocative Metaphors
   forge, vault, weave, lattice

✓ Domain-Specific Terms
   codex, praxis, schema

✓ Clear Compound Structure
   skill-bundle, knowledge-forge

✓ Balanced Length (2-5 words)
   agent-skill--knowledge-forge
```

## References

- `references/naming-patterns.md` — Compound naming patterns
- `references/separator-conventions.md` — Detailed separator rules
- `references/translation-guide.md` — Latin/Greek translation guidance
- `references/workflow-integration.md` — Ecosystem integration
- `assets/word-roots.md` — Common Latin/Greek roots

## Related Skills

- **documentation-generator**: For documenting named concepts
- **brand-guidelines**: For visual identity to match names
