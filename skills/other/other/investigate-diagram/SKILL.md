---
name: investigate-diagram
description: Generate dependency diagrams from code or architecture. Traces code-level dependencies (hooks, queries, providers, components) or maps high-level system architecture. Outputs Mermaid diagrams in markdown or FigJam via Figma MCP. Use when the user asks to map dependencies, visualize relationships, create a dependency diagram, diagram an architecture, or trace how systems connect.
---

# Dependency Diagram Generator

Generate dependency diagrams at any level — from code-level hook/query tracing to high-level architecture maps.

## Phase 1 — Gather Requirements

Use AskQuestion to collect:

### 1. Scope detection

| Scope | When to use | Examples |
|---|---|---|
| **Code-level** | Tracing function/hook/component dependencies | "Map dependencies of useQueryUserAccounts", "What calls AccountProvider?" |
| **Architecture-level** | Mapping services, teams, integrations | "Diagram the Payroll system", "Map Risk Engineering architecture" |

If ambiguous, ask which scope the user intends.

### 2. Entry points

- **Code-level**: function names, hook names, component names, or file paths
- **Architecture-level**: system, team, or domain name

### 3. Tracing options (code-level only)

Ask with multi-select:

| Option | What it traces |
|---|---|
| Hook calls | `useX()` calls inside function bodies |
| GraphQL queries | `useQuery`, `useSuspenseQuery`, `useMutation` with document imports |
| Context providers | React context providers consumed |
| HOC wrappers | `withX()` higher-order components |
| All of the above | Everything |

Default: **All of the above**

### 4. Depth (code-level only)

| Option | Behavior |
|---|---|
| Bounded (default: 3) | Trace up to N levels |
| Full tree | Trace until no more dependencies found |
| Immediate only | Direct parents/children only |

### 5. Output format

| Option | Requirement |
|---|---|
| **Mermaid in markdown** (default) | None |
| **FigJam via Figma MCP** | Requires Figma MCP connected — verify with ToolSearch |

### 6. Output location

Suggest a filename based on entry points, e.g. `dependency-graph-useQueryUserAccounts.md`.

---

## Phase 2 — Research

### Code-level: Trace Dependencies

Launch parallel explore subagents to trace the graph in both directions from each entry point.

#### Tracing parents (what does this symbol depend on?)

For each file, look for:

- **Hook calls**: `useX(...)` calls → find definition files
- **GraphQL documents**: imports of `*Document` passed to query/mutation hooks
- **Context reads**: `useContext(XContext)` or custom context hooks
- **Direct imports**: named imports from other project files (not node_modules)

#### Tracing children (what consumes this symbol?)

Search the codebase for:

- **Import references**: grep for the export name across `.ts`/`.tsx` files
- **Hook consumers**: files that call `useX()` where X is the traced symbol
- **Provider wrappers**: files that render `<XProvider>` or use `withX()` HOC

#### Classifying nodes

| Type | How to identify |
|---|---|
| `graphql-query` | Fires a query/mutation via document import |
| `data-hook` | Custom hook that fires a GraphQL query |
| `context-provider` | Exports a React context Provider |
| `composition-hook` | Custom hook calling other hooks, no query |
| `component` | React component (JSX return) |
| `hoc` | Higher-order component (`withX`) |
| `deprecated` | Has `@deprecated` JSDoc tag |

#### Data per node

```
- id: sanitized name for Mermaid
- label: display name
- file: relative file path
- type: one of the types above
- query_name: (if graphql-query) the operation name
- query_fields: (if graphql-query) root fields summary
- edges_to: list of { target_id, label }
```

### Architecture-level: Research the System

Run documentation search and codebase exploration in parallel.

#### Documentation search

If Glean MCP is available, search for:

- Architecture docs, tech specs, strategy docs
- Team formation / org docs
- Service ownership and on-call docs
- Integration docs (vendor partnerships, platform dependencies)

Run multiple searches with different keyword angles for broad coverage.

#### Codebase exploration

Search for:

- **Team config files**: `config/teams/**/<team>.yml` for owned gems, Kafka topics, feature flags, Sidekiq queues, service ownership — the single most information-dense source
- **Pack/module structure**: `packs/product_services/<domain>/` directories, `package.yml`, sub-pack organization
- **Service classes and models**: domain models, service objects under the team's Ruby module namespace
- **External integrations**: `*_client` gems and API wrappers listed in `owned_gems`
- **Messaging infrastructure**: Kafka producer/consumer definitions, Sidekiq workers
- **GraphQL subgraphs**: `graphql_service_list.json` for subgraphs owned by the domain
- **CLAUDE.md files**: `**/CLAUDE.md` files contain structured domain knowledge

#### Synthesize into categories

Organize findings into: Pods/Teams, Services/Systems, Shared Infrastructure, External Vendors, Platform Dependencies, Key Flows.

---

## Phase 3 — Verify Terminology

**STOP — present findings to user before proceeding.**

A wrong label is worse than a missing one. For every node you plan to include:

1. Search for the **exact name** in both docs and code
2. If docs and code use different terms, note both and let the user pick
3. If you cannot find a term in either source, **do not include it**

Present a terminology summary table:

| Planned Label | Found in Code? | Found in Docs? | Notes |
|---|---|---|---|

Wait for user confirmation before continuing.

---

## Phase 4 — Negotiate Scope

**STOP — present the plan to user before proceeding.**

Present:

### Node count and arrow budget

- 15-20 arrows for simple diagrams
- Up to 25 for complex ones
- Beyond 25: propose splitting into focused sub-diagrams

### Layout

**Code-level**: Top-down (`graph TD`) with rows grouped by node type.

Row assignment:
1. Find roots (no parents in traced set) and leaves (no children)
2. Layer 0 = GraphQL queries (always top if present)
3. Remaining: layer = 1 + max(layer of all parents)
4. Group into subgraphs by layer

Row naming by dominant type:

| Type | Row label |
|---|---|
| `graphql-query` | "GraphQL Queries" |
| `data-hook` (root) | "Root Data Hooks" |
| `context-provider` | "Context Providers" |
| `data-hook` (leaf) | "Data-Fetching Hooks" |
| `composition-hook` | "Composition Hooks" |
| `component` | "Components" |

**Architecture-level**: Offer layout choice:

| Layout | Best for |
|---|---|
| **Horizontal flow** (LR, default) | Data flowing through a system |
| **Ownership map** | What each team owns, minimal arrows |
| **Integration map** | External boundaries and vendor connections |
| **Decision flow** | End-to-end workflow with branch points |

Wait for user approval before generating.

---

## Phase 5 — Generate Diagram

Based on the output format chosen in Phase 1, read the corresponding guide and follow its rules:

- **Mermaid in markdown** → read [output-mermaid.md](output-mermaid.md) for syntax rules, style palette, templates, and output file structure
- **FigJam via Figma MCP** → read [output-figjam.md](output-figjam.md) for FigJam constraints, Figma MCP usage, and templates

Each guide is self-contained — it has layout rules, edge conventions, templates for both code-level and architecture-level diagrams, and output instructions specific to that format.

---

## Phase 6 — Audit

After generating, audit every label. Categorize:

| Severity | Definition | Action |
|---|---|---|
| **Wrong** | Refers to something that doesn't exist or misattributes a relationship | Must fix |
| **Imprecise** | Correct but uses a paraphrase instead of the official term | Flag for user |
| **Inferred** | Relationship you believe exists but can't trace to a specific source | Flag with caveat |
| **Verified** | Confirmed in code, docs, or both | Note the source |

Check:

- **Node labels**: Does this name appear in docs or code? Is any acronym expansion correct?
- **Edge labels**: Is this a real, documented relationship? Watch for fabricated queue names or generic labels like "sends data"
- **Missing nodes**: Are there systems/hooks visible in code that aren't on the diagram?
- **Structural accuracy**: Are nodes in the correct groups/layers?

Present audit as a table: Label | Severity | Source | Notes

---

## Phase 7 — Iterate

Most diagrams take 2-3 rounds. Common patterns:

| Request | How to handle |
|---|---|
| "Arrows are messy" | Reduce count, reorder node declarations, suggest manual rearrangement |
| "What does X mean?" | Explain and cite source. If inferred, say so immediately |
| "This is called Y, not X" | Fix. User correction always wins. Verify in code |
| "Add/remove X" | Regenerate with change. Re-audit affected labels |
| "Split this up" | Break into focused diagrams, each standalone |
| "Trace deeper into X" | Re-run Phase 2 scoped to that node, extend the existing graph |

---

## Reference

- [Output guide: Mermaid in markdown](output-mermaid.md)
- [Output guide: FigJam via Figma MCP](output-figjam.md)
- [Example output: account context dependency graph](dependency-graph-example.md)
