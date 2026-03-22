---
name: living-design-documents
description: |
  Create and maintain structured design documentation that drives development.
  Use for new projects, design decisions, growing complexity, or when audit is due. Triggers: "design docs", "LDD", "core decisions", "taxonomy", "parked decisions".
license: MIT
metadata:
  author: KemingHe
  version: "1.0.0"
---

# Living Design Documents

Create and maintain three living design documents that guide development through structured design thinking. Core Decisions capture load-bearing policies. Taxonomy provides detailed specifications. Parked holds deferred analysis. Documents graduate upward as maturity increases.

**Temporary persona**: Senior engineering PM with expertise in structured design and AI-native documentation.

## When to Use This Skill

- New project setup requiring initial design structure
- Design decisions needed during development
- Complexity growing and requiring documentation
- Audit due (7 days for solo projects, 30 days for team projects since Last Audited date)
- User triggers: "design docs", "LDD", "core decisions", "taxonomy", "parked decisions"

## Asset Resolution

1. Check `./assets/design-*-template.md` (skill-local)
2. If not found, search `**/design-*-template.md` in repository
3. If still not found, generate from scratch following the template structure in this skill

## Simple vs Complex Project Adaptation

Templates default to simple project pattern. Adapt based on project complexity:

| Project Type | Core Decisions | Taxonomy | Parked |
| :--- | :--- | :--- | :--- |
| **Simple** (single-focus) | `design-core-decisions.md` | `design-taxonomy.md` | `design-parked.md` |
| **Complex** (multi-component) | `design-core-decisions.md` | `design-taxonomy-[component].md` | `design-parked-[component].md` |

**Detection heuristics**:

- Simple: <5 major components, single team, focused purpose
- Complex: 5+ components, multiple teams, or distinct bounded contexts

**Template adaptation examples for complex projects**:

| Element | Simple (template default) | Complex (agent adapts) |
| :--- | :--- | :--- |
| Taxonomy filename | `design-taxonomy.md` | `design-taxonomy-api.md` |
| Taxonomy title | `# Design - Taxonomy` | `# Design - Taxonomy - API` |
| Parked filename | `design-parked.md` | `design-parked-api.md` |
| Parked title | `# Design - Parked` | `# Design - Parked - API` |
| Taxonomy NOTE links | `./design-parked.md` | `./design-parked-api.md`, `./design-taxonomy-database.md` |
| Parked NOTE links | `./design-taxonomy.md` | `./design-taxonomy-api.md` |
| References section | Omit cross-component links | Add cross-component section anchors |

Core Decisions is always singular - no component suffix regardless of project complexity.

## Process

### Step 1: Detect Context

Search for existing design documents to determine if this is a new or existing project.

- Search for `docs/design-*.md` in the repository
- If found: This is an existing project - proceed to Step 2 (Gather)
- If not found: This is a new project - proceed to Step 2 (Bootstrap)

### Step 2: Bootstrap or Gather

**For new projects (Bootstrap)**:

1. Determine project complexity and propose document granularity:
   - Simple projects: Single files (`design-core-decisions.md`, `design-taxonomy.md`, `design-parked.md`)
   - Complex projects: Core Decisions always singular; Taxonomy and Parked may be component-specific (`design-taxonomy-[component].md`, `design-parked-[component].md`)
2. If component-specific needed, propose component names based on project context (e.g., "api", "database", "auth")
3. Present proposals to user for confirmation
4. Create all three documents with resolved templates

**For existing projects (Gather)**:

1. Read all existing `docs/design-*.md` files
2. Gather design input from user (new decisions, content to add/update, questions to address)
3. Note current Last Audited dates to determine if audit refresh is needed

### Step 3: Classify Content

Determine where new content belongs based on maturity and role:

| Document Type | Content Criteria | Graduation Path |
| :--- | :--- | :--- |
| **Core Decisions** | One-or-two-sentence policy; load-bearing (breaking it requires major refactor); settled and stable | Terminal - content stays here |
| **Taxonomy** | Detailed specification; defined structure; complete analysis; actively referenced by implementation | Graduates FROM Parked when analysis complete; graduates TO Core when becomes load-bearing |
| **Parked** | Deferred analysis; future considerations; not yet analyzed deeply; implementation-level details too granular for current planning | Graduates TO Taxonomy when analysis complete |

**Graduation triggers**:

- **Parked -> Taxonomy**: Analysis is complete, structure is defined, ready for active reference
- **Taxonomy -> Core Decisions**: Decision has become load-bearing (breaking it requires major refactor), can be expressed as one-or-two-sentence policy

### Step 4: Generate Open Questions

**THE CORE VALUE OF THIS SKILL**: Generate valuable open questions that catch surprises before and during development, well before production.

**Dynamic follow-up strategy**:

- Questions must be contextually relevant to current design focus
- I.e. do NOT ask about authentication when planning frontend button components
- I.e. do NOT ask about database schemas when planning CI/CD pipelines
- Follow up on existing open questions that relate to the current work
- Archive or remove questions once answered and absorbed into design docs

**Question quality guidelines**:

- Questions should reveal hidden complexity, constraints, or trade-offs
- Focus on "what could go wrong" and "what assumptions are we making"
- Prioritize questions that would change the design if answered differently
- Include questions about operational concerns (monitoring, debugging, rollback)
- Consider cross-team dependencies and communication needs

**Placement**:

- Mandatory: Top-level "Open Questions" section at end of each document
- Optional: Subsection-level "Open Questions" for detailed components in Taxonomy

### Step 5: Generate/Update Documents

Populate or update documents following resolved templates from `./assets/`. Apply graduation rules when content matures.

**Document creation for new projects**:

- `docs/design-core-decisions.md` (singular, one per project)
- `docs/design-taxonomy.md` or `docs/design-taxonomy-[component].md` (component-specific if needed)
- `docs/design-parked.md` or `docs/design-parked-[component].md` (component-specific if needed)

**Template resolution**: Check `./assets/` for `design-core-decisions-template.md`, `design-taxonomy-[component]-template.md`, and `design-parked-[component]-template.md`. If not found, search repository or generate from scratch following the structures below.

**Core Decisions structure**: Metadata block with Last Updated, Project Type (solo/team), Last Audited; one-paragraph summary; NOTE block with related docs; categories with one-or-two-sentence policies in decision/rationale tables; Open Questions section; References section.

**Taxonomy structure**: Metadata with Last Updated; component purpose; NOTE block; subcomponent sections with detailed specs; per-subcomponent Related Issues sections (`### [Subcomponent] - Related Issues`) with mandatory 2-5 word descriptions; optional subsection Open Questions; mandatory doc-level Open Questions; References with section anchors.

**Parked structure**: Metadata with Last Updated; purpose statement; NOTE block; level 2 heading per topic with detail content and `**Revisit when**: [trigger]`; mandatory Open Questions section.

### Step 6: Validate

Perform validation checks on all generated/updated documents:

| Validation Rule | Check | Action if Failed |
| :--- | :--- | :--- |
| **Line count** | Count total lines per document | <200 ideal; 200-500 recommend split; >500 must split into multiple component-specific documents |
| **Heading uniqueness** | All headings unique within document | Rename duplicate headings with disambiguating context |
| **Link integrity** | All cross-refs resolve to valid anchors | Fix broken links, update anchor references |
| **Audit dates** | Last Updated and Last Audited present | Core Decisions needs both; Taxonomy and Parked need Last Updated only |
| **Audit freshness** | Last Audited within threshold | 7 days (solo), 30 days (team) - flag if overdue, trigger audit |
| **Metadata complete (Core)** | Project Type field present | Core Decisions must declare solo or team |
| **Cross-ref direction (Core)** | Core Decisions content has inward-only refs | Remove outbound refs from Core Decisions content (decision tables, policies) - content must be self-contained; NOTE block for navigation is permitted |
| **Related Issues format (Taxonomy)** | `### [Subcomponent] - Related Issues` sections present | Add section after each subcomponent with proper heading format |
| **Open Questions present** | Each document has top-level "Open Questions" section | Add section if missing |
| **GDC compliance** | All documents follow GDC rules | Fix violations (smart quotes, emojis, `*asterisk*` italics, bullets, prose wrapping, unresolved placeholders) |

### Step 7: Recommend Issue Creation

When design content describes actionable work items, strongly recommend using the `issue-creation` skill.

**Indicators for issue creation**:

- Parked items with clear "revisit when" triggers that are now met
- Open questions that require research or investigation
- Taxonomy sections that describe unimplemented features
- Core Decisions that require tooling or enforcement mechanisms

**Recommendation approach**: "This looks like it would benefit from tracking as an issue. Would you like me to use the issue-creation skill to create [bug report/feature request/task] for [specific item]?"

## Output Format

Present all generated or updated design documents as complete markdown code blocks, specify/remove "- [Component]" based on context:

```markdown
# Design - Core Decisions

[Full document content]
```

```markdown
# Design - Taxonomy - [Component]

[Full document content]
```

```markdown
# Design - Parked - [Component]

[Full document content]
```

## General Doc Constraints

Apply to all generated output. If a discovered template deviates from any rule (e.g., uses emojis semantically, uses a different bullet convention), note the deviation explicitly and confirm with the user before treating it as a permitted exception.

- **Characters**: QWERTY keyboard typeable only - no smart quotes, emojis, or special Unicode anywhere. In prose, do not use em-dashes or em-dash substitutes (`--`, ` -- `); use ` - ` (space-dash-space) for clause separation instead. Exception: `↑` for ToC navigation.
- **Inline formatting**: Use `_underscore_` for italics, not `*single-star*`. Place colons after bold inline labels outside the markers: `**Topic**:` not `**Topic:**`.
- **Bullets**: Use `-` for all unordered lists; one bullet per complete thought; never wrap a bullet's content mid-sentence onto a continuation line - split into separate bullets if too long or multi-thought. Nested sub-bullets for component grouping are permitted. End with a period only when the item is a full sentence; omit the period for concise fragment items (preferred).
- **Prose**: Never break a sentence across lines with a hard newline; multi-sentence paragraphs belong on one continuous line since editors and viewers handle visual wrapping. Exception: commit message bodies use one sentence per line for `git log` readability.
- **Template hygiene**: Delete `(optional)` and any parenthetical conditional label (e.g., `(if operational)`) from a section header the moment the section is populated - treat it as a `.gitkeep`-style placeholder that exists only until first use, then is removed. Omit the entire section (header and body) when unused. Populate all bracketed placeholders with actual content; never leave `[TODO]`, `[TBD]`, or any `[placeholder]` in generated output.
- **Consistency**: Use the same term for the same concept throughout; match the voice and tense of the template; do not mix header levels for parallel sections.
- **KISS and DRY**: Each section and bullet conveys unique information - no redundancy or overlap.

> General Doc Constraints v1.1.0 - KemingHe/common-devx

## Skill Constraints

- **Line limits**: <200 lines ideal per document; 200-500 recommend splitting into separate component-specific documents; >500 must split or move detailed sections to Parked
- **Audit intervals**: 7 days for solo projects, 30 days for team projects from Last Audited date; flag when overdue
- **Core Decisions cross-refs**: Content has inward references only - decision tables and policies never reference out to Taxonomy or Parked; NOTE block for navigation is permitted
- **Heading uniqueness**: All headings must be unique within a single document to enable unambiguous anchor linking
- **Open Questions**: Mandatory top-level section in all documents; optional at subsection level in Taxonomy for detailed components
- **Graduation paths**: Parked -> Taxonomy when analysis complete; Taxonomy -> Core Decisions when decision becomes load-bearing
- **Cross-document linking**: Use markdown anchor links (`[text](./file.md#section-heading)`); expect dense cross-referencing; skill maintains link integrity during updates
- **Component naming**: Agent proposes component names if not provided by user; user confirms before document creation
- **Issue creation**: Strongly recommend `issue-creation` skill when content describes actionable work items
- **GDC compliance**: All generated documents must follow General Doc Constraints rules
- **Template population**: Resolve all `[placeholders]`; remove `(optional)` markers when sections are used; omit entire unused sections
- **Cross-refs in templates**: Design document templates always include cross-refs to the other two design doc types in the opening NOTE block
- **Last Audited format**: Always `YYYY-MM-DD by [Author]` format; update on every audit pass

## Graduation Decision Matrix

| Current Location | Content Characteristics | Graduation Target | Trigger Conditions |
| :--- | :--- | :--- | :--- |
| Parked | Deferred analysis, incomplete structure, future considerations | Taxonomy | Analysis complete, structure defined, ready for active reference by implementation |
| Parked | N/A | Core Decisions | Skip Taxonomy if immediately load-bearing and can be one-or-two-sentence policy |
| Taxonomy | Detailed spec, actively referenced | Core Decisions | Becomes load-bearing (breaking requires major refactor), distillable to one-or-two-sentence policy |
| Taxonomy | Detailed spec, no longer relevant | Remove/Archive | Decision reversed, component deprecated, or moved out of scope |
| Core Decisions | Load-bearing policy | Terminal | Content stays in Core Decisions permanently |

## Validation Checklist

Before presenting output to user, verify:

- [ ] Core Decisions has complete metadata: Last Updated, Project Type (solo/team), Last Audited
- [ ] Taxonomy and Parked have Last Updated metadata
- [ ] Audit freshness: Core Decisions Last Audited within 7 days (solo) or 30 days (team)
- [ ] Cross-reference NOTE blocks present in all documents with valid links
- [ ] All headings are unique within each document
- [ ] Taxonomy has `### [Subcomponent] - Related Issues` sections after each subcomponent
- [ ] Related Issues use format: `[#N](link) - 2-5 word description`
- [ ] No placeholder text (`[TODO]`, `[TBD]`, `[placeholder]`) remains in generated output
- [ ] No `(optional)` or conditional markers remain in populated sections
- [ ] Line counts within thresholds (<200 ideal, 200-500 recommend split, >500 must split)
- [ ] Core Decisions content has no outbound cross-refs (NOTE block for navigation is permitted)
- [ ] Open Questions section present at doc level in all documents
- [ ] GDC compliance: no smart quotes, no emojis, `_underscore_` italics only, `-` bullets, no prose line breaks
- [ ] Markdown anchor links use kebab-case (GitHub/GitLab standard)

## Examples

### Good Example: Core Decisions Entry

```markdown
## Settled Decisions

| Decision | Rationale |
| :--- | :--- |
| Separate repo (`iac-adoption-skills`) | Audience divergence from common-devx; independent iteration cadence |
| Apache 2.0 per-skill LICENSE | Enterprise-friendly patent grant; aligns with HashiCorp ecosystem |
```

### Good Example: Taxonomy Entry

```markdown
## Skill Categories

| Prefix | Category | Purpose |
| :--- | :--- | :--- |
| `orchestrator-` | Orchestrator | Generic workflow logic with self-discovery; sequences skills via frontmatter |
| `workflow-` | Workflow | Executes a specific step in the adoption process; independently invocable |
| `research-` | Research | Produces and maintains domain knowledge; dual-mode (operate + self-update) |
```

### Good Example: Parked Entry

```markdown
## File Organization Patterns

Component naming uses `[component].tf`, `[component]-[subcomponent].tf`, max 3 levels. Locals split into separate `[component]-locals.tf` when large. File split threshold approximately 200 lines or 3+ logically distinct resource groups (needs validation).

**Revisit when**: Building `workflow-iac-capture` (generates `.tf` files)
```

### Bad Example: Missing Open Questions

```markdown
# Design - Taxonomy - API

> **Last Updated**: 2026-03-19 by Keming He

[Content sections here]

[Document ends without Open Questions section]
```

Missing the mandatory "Open Questions" section. Every design document must have this section, even if empty initially.

### Bad Example: Core Decisions with Outbound Refs

```markdown
## Settled Decisions

| Decision | Rationale |
| :--- | :--- |
| See [API patterns](./design-taxonomy.md#api-patterns) | Detailed in Taxonomy |
```

Core Decisions should never reference out to other documents. Rewrite as self-contained one-or-two-sentence policy: "REST API uses resource-based URLs with standard HTTP methods."

### Bad Example: Unresolved Placeholders

```markdown
## [Topic Name]

[Implementation detail here]

**Revisit when**: [TBD]
```

Never leave placeholder text. Replace `[Topic Name]` with actual topic, `[TBD]` with concrete trigger condition. All bracketed placeholders must be populated in generated output.
