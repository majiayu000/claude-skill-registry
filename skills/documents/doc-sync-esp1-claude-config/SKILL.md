---
name: doc-sync
description: Use when creating, updating, reorganizing, or synchronizing project documentation. Maintains consistency across the documentation index, functional requirement specs, and technical documentation. Use when changes are made to any documentation file, when creating new requirement or technical docs, when bootstrapping documentation for new projects, or when ensuring documentation hierarchy and cross-references remain accurate. IMPORTANT — Invoke this skill proactively after making successful code changes to keep documentation in sync, not just when explicitly asked.
---

# Doc Sync

Maintain synchronized, hierarchical project documentation following a structured system where high-level documents link to detailed specifications, requirement specs remain implementation-agnostic, and technical docs reference features appropriately.

**Key principle:** If code changed successfully and will be kept, docs should be updated to match **user-observable behavior**. Internal implementation details that don't affect how users interact with or understand the system don't require documentation updates.

Always invoke this skill before committing changes to version control.

**Do NOT invoke for:**
- Exploratory/debugging work that doesn't lead to changes
- Temporary experiments or proof-of-concepts
- Simple clarification questions
- **Internal code organization changes** — refactoring that doesn't change external behavior (e.g., moving dependencies between aliases, renaming internal variables)

## Documentation Structure

Project documentation follows this hierarchy (create only what's needed):

```
project-root/
├── README.md                           # Project intro, badges, quick links (minimal)
├── docs/
│   ├── index.md                        # Main documentation hub
│   ├── functional/                     # Functional requirement specifications
│   │   ├── index.md                    # Requirements overview (links to specs)
│   │   ├── feature-1.md
│   │   └── ...
│   └── technical/                      # Technical documentation
│       ├── index.md                    # Technical docs overview
│       ├── architecture.md             # System design (optional)
│       ├── development.md              # Dev setup, build, test (optional)
│       ├── operational.md              # Deploy, monitor, manage (optional)
│       └── ...component docs...
```

### Flexible File vs Directory Structure

Only create documentation that exists. Don't create empty files or directories.

For any topic, start with a single file when content is simple:
- `docs/technical/architecture.md`
- `docs/technical/development.md`

Expand to a directory with index.md when content grows complex:
- `docs/technical/architecture/index.md` + subtopic files
- `docs/technical/development/index.md` linking to subtopics
- `docs/technical/operational/index.md` — deployment, monitoring, management

## Core Principles

1. **No Duplication — Single Source of Truth**
   - Each piece of information should exist in EXACTLY ONE appropriate place
   - Higher-level docs provide summaries and links, NOT duplicate content
   - **NEVER copy-paste content between documents** — use links and references instead
   - **NEVER duplicate information from source files** — especially version numbers, configuration values, or data that lives in code
   - Source code documentation is authoritative for function/module docs — technical docs should link to generated API docs rather than duplicate

2. **Appropriate Placement**
   - **Functional specs** (`docs/functional/*`) describe WHAT features do and WHY they exist
   - **Technical docs** (`docs/technical/*`) describe HOW things are implemented
   - **Index docs** (`index.md` files) summarize and link, don't duplicate
   - **README.md** provides minimal project intro, links to `docs/index.md`
   - When adding content, ask: "What is the MOST SPECIFIC appropriate place for this?"

3. **Separation of Concerns**
   - **Functional specs** MUST NOT contain implementation details
   - **Technical docs** MAY reference features from functional specs
   - Index documents provide structure and navigation, not primary content

4. **Hierarchical Linking**
   - `README.md` → `docs/index.md` → `docs/functional/index.md` and `docs/technical/index.md` → specific docs
   - Cross-references between functional and technical docs are encouraged
   - Links replace duplication — always prefer linking over copying

5. **Bidirectional Consistency**
   - When any document changes, update all documents that reference or are referenced by it
   - Propagate changes up and down the documentation hierarchy

6. **Source Code is Primary Documentation**
   - Well-named functions, parameters, and data structures are the first layer of documentation
   - Comments explain intent, not what the code does
   - For code-level documentation conventions, consult language-specific editing skills

7. **Procedural Instructions Hierarchy**
   - Prefer the most deterministic form: executable scripts/commands > checklists/decision trees > prose

## Anti-Duplication Workflow

**Before adding ANY documentation content:**

1. **Check if it already exists elsewhere** — search across all docs, determine if you should update that location or link to it
2. **Determine the single best location** — feature requirements → `docs/functional/`, implementation details → `docs/technical/`, dev setup → `docs/technical/development.md`
3. **Use links instead of duplication** — write it ONCE in the most appropriate place, other documents link to it
4. **Consolidate when you find duplication** — identify which location is most appropriate, keep content there, replace duplicates with links

**Example:**

Bad — same content in index and detail file:
```markdown
# docs/functional/index.md
## Image Viewer
The image viewer allows users to view images with zoom and pan controls...
[3 paragraphs]
```

Good — single source with linking:
```markdown
# docs/functional/index.md
## Image Viewer
Interactive image viewing with zoom, pan, and navigation controls.
See [image-viewer.md](image-viewer.md) for detailed requirements.
```

## Workflows

### When Updating Existing Documentation

1. **Identify the document type** being modified
2. **Determine impact scope** — search for documents that link TO and FROM this document
3. **Update all affected documents** — parent summaries, child details, cross-references
4. **Verify consistency** — check links, descriptions, separation of concerns

### When Creating New Documentation

1. **Determine document placement** — functional spec → `docs/functional/`, technical doc → `docs/technical/`
2. **Create the document** with clear filename (kebab-case), appropriate content
3. **Update parent documents** — add links in relevant index files
4. **Create cross-references** — link between functional and technical docs

### When Reviewing Existing Documentation

1. **Audit current state** — list all docs, find duplicates, identify misplaced content
2. **Plan reorganization** — map files to target locations, identify consolidation opportunities
3. **Execute reorganization** — move/rename files, create index files, update cross-references
4. **Clean up content** — remove duplication, enforce separation of concerns, condense verbose content
5. **Verify conformance** — all links valid, no orphaned files, no duplicate content

### When Documents Don't Exist

1. **Assess what exists** — README, docs/ directory, informal documentation
2. **Create missing structure** (only what's needed) — `docs/`, `docs/functional/`, `docs/technical/`
3. **Generate core documents** in order: README.md → `docs/index.md` → category indexes
4. **Populate with initial content** from existing code, comments, or informal docs
5. **Incrementally add detailed docs** as features and implementation docs are needed

## Content Guidelines

### Link Formatting
`**[Feature Name](file.md)** - description`

### Writing Style: Concise But Clear

- Use bullet points over paragraphs when listing information
- Start with the essential point, add details only if necessary
- Prefer short sentences (10-15 words)
- Cut introductory phrases, marketing language, obvious statements
- Use active voice and direct language

### Document Templates

**README.md** — 1-2 sentences on what the project does + link to `docs/index.md`

**docs/index.md** — Overview, quick start, links to functional and technical docs

**docs/functional/index.md** — Vision (1-2 sentences), features list with one-line descriptions + links

**docs/functional/*.md** — Overview, user value, requirements (descriptive names, NO numeric IDs), acceptance criteria, NO implementation details

**docs/technical/index.md** — Development environment (first), stack, design/architecture, modules, deployment (last)

**docs/technical/*.md** — Purpose, key functions, algorithms, code references (file:line)

**docs/technical/development.md** — Prerequisites, quick start, commands reference, workflows, troubleshooting

For a detailed checklist when reviewing documentation, see `references/review-checklist.md`.

## Examples

### Adding a new authentication feature

1. **Create functional spec**: `docs/functional/authentication.md` — what auth is needed and why, NO implementation details
2. **Update `docs/functional/index.md`** — add link and brief description
3. **Create technical doc**: `docs/technical/auth-implementation.md` — reference the functional spec, detail technical decisions
4. **Update `docs/technical/index.md`** — add link

### Updating an existing feature spec

1. **Make changes** to the functional spec
2. **Check parent index** — update description if summary changed
3. **Check technical docs** — find docs that reference this spec
4. **Update technical docs** if requirements change affects implementation
5. **Verify `docs/index.md`** still accurately describes project scope

### Adding development instructions

1. **Add to `docs/technical/development.md`** — commands, workflows, troubleshooting
2. **Update `docs/technical/index.md`** — add link if not present
3. **Do NOT duplicate** — don't copy command definitions from `bb.edn`, reference source of truth
