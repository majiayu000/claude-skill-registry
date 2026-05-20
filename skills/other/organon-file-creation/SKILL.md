---
name: organon-file-creation
description: Creates new organon files (ETHOS.md, PHILOSOPHY.md, PROTOCOL.md, README.md) with correct structure, frontmatter, scope inheritance, and bidirectional references. Use when adding a new domain, feature, component, or scope that needs organon documentation. Replaces ad-hoc file creation with validated workflow.
protocol_id: PROTO-ORG-6
protocol_file: organon/protocols/PROTOCOLS.md
tools: [organon-generate, organon-validate, organon-verify]
loads:
  - book-llms/templates.md
  - book-llms/scopes.md
  - book-llms/frontmatter-system.md
  - book-llms/ETHOS.md
  - CLAUDE.md
---

# Organon File Creation Workflow

> Implements PROTO-ORG-6 from `organon/protocols/PROTOCOLS.md`. Creates valid organon files with correct placement, structure, and references.

---

## When to Use This Skill

Use this skill when:
- **Adding a new domain** that needs its own ETHOS.md
- **Adding a new feature** organon (cross-cutting capability)
- **Creating PHILOSOPHY.md** for design rationale
- **Creating PROTOCOL.md** for step-by-step procedures
- **Adding a new scope directory** that needs a README.md router

**Purpose:** Ensure every organon file is created correctly from the start — right location, right structure, right frontmatter, right inheritance.

---

## Context Loading

1. Load templates and structure:
   - Read `book-llms/templates.md` (copy-paste scaffolds for each artifact type)
   - Read `book-llms/scopes.md` (scope classification: product, domain, feature, component)
   - Read `book-llms/frontmatter-system.md` (complete YAML frontmatter schema)
2. Load quality standards:
   - Read `book-llms/ETHOS.md` (meta-organon constraints — what every organon must follow)
   - Read `CLAUDE.md` (project-level constraints)
3. Load parent scope:
   - Read the parent scope's ETHOS.md (new file must inherit, never contradict)

---

## Steps

### Step 1: Classify Scope

Determine the scope of the new file:

| Scope | Question It Answers | Characteristics |
|-------|-------------------|-----------------|
| **product** | "What is this project?" | Top-level, inherits from meta-organon only |
| **domain** | "What business concepts exist?" | Bounded context, ≥3 unique concepts, own lifecycle |
| **feature** | "What can users do?" | Cross-cutting capability, used by multiple domains |
| **component** | "Where is the code?" | Code module, dependency relationships |
| **methodology** | "How do we work?" | Process documentation, separate from product |

**Decision heuristic:** Has ≥3 unique concepts + lifecycle → domain. Crosses multiple domains → feature. Users think in code terms → component.

### Step 2: Check Parent Scope

Load the parent scope's ETHOS.md. The new file must:
- **Inherit** all parent constraints (never relax them)
- **Add** constraints specific to this scope
- **Reference** the parent in `inherits_from` frontmatter field

### Step 3: Select Template

Based on the artifact type, load the correct template from `book-llms/templates.md`:

| Artifact | Template Section | Required Sections |
|----------|-----------------|-------------------|
| ETHOS.md | Ethos Template | Identity (IS/IS NOT), Invariants, Principles, Decision Heuristics |
| PHILOSOPHY.md | Philosophy Template | The Problem, The Bet, Design Decisions, Trade-offs |
| PROTOCOL.md | Protocol Template | Goal, Preconditions, Steps, Verification, Recovery |
| README.md | README Router Template | Contents table with paths, types, descriptions |

### Step 4: Determine File Placement

Follow Pattern A (dedicated `organon/` directory):

```
organon/
├── domains/
│   └── <domain-name>/
│       ├── ETHOS.md
│       ├── PHILOSOPHY.md
│       └── README.md
├── features/
│   └── <feature-name>/
│       ├── ETHOS.md
│       └── README.md
└── protocols/
    └── PROTOCOLS.md
```

For product-level scope: place directly in `organon/`.

### Step 5: Generate Frontmatter

Fill in all required fields:

```yaml
---
type: [constraints|rationale|procedures|navigation]
scope: [product|domain|feature|component|methodology]
name: [kebab-case-name]
version: "1.0"
summary: [One-sentence, max 200 chars]
token_estimate: [number, ~12 tokens/line]
# Type-specific fields (e.g., invariants_count for constraints)
inherits_from: [parent-scope-names]
load_priority: [high|medium|low]
audience: [llm, human]
---
```

Use `organon generate` if available to auto-generate frontmatter scaffold.

### Step 6: Write Content

Follow the template's section structure exactly:

**For ETHOS.md:**
- Write ≥3 IS statements (specific, not generic)
- Write ≥3 IS NOT statements (real boundaries)
- Write ≥3 invariants with enforcement mechanisms
- Write ≥3 prioritized principles (lower number wins)
- Write ≥5 decision heuristics (situation → action)

**For PHILOSOPHY.md:**
- Write problem statement with root causes
- Write the bet (falsifiable hypothesis)
- Write ≥5 trade-offs with rationale
- Write ≥3 alternatives considered

**For PROTOCOL.md:**
- Write clear goal statement
- Write ≥3 preconditions
- Write numbered steps with decision points
- Write verification checklist
- Write recovery table

**For README.md:**
- Keep under 100 lines (router, not content)
- Include contents table with all children

### Step 7: Validate

```bash
cd packages/tools && npx organon validate <path-to-new-file>
```

Runs all 4 validation stages:
1. **Schema** — frontmatter structure is valid
2. **Content** — required sections present
3. **References** — file paths resolve
4. **Relationships** — inheritance chain is valid

### Step 8: Check Bidirectional References

If the new file references other organon files, ensure those files reference back:
- If creating a protocol with `workflow: <name>`, ensure the workflow has `protocol_id` matching
- If setting `inherits_from: [parent]`, ensure parent exists
- If setting `related_files`, ensure those files exist

```bash
cd packages/tools && npx organon verify --gate triplets
```

---

## Verification

- [ ] `organon validate` passes all 4 stages
- [ ] File is in the correct directory per scope classification
- [ ] Frontmatter has all required fields (type, scope, name, version, summary, token_estimate)
- [ ] Section headings match the template for this artifact type
- [ ] Parent scope constraints are inherited, not contradicted
- [ ] Bidirectional references are complete (no orphans)

---

## Error Recovery

| Failure | Recovery Action |
|---------|-----------------|
| Wrong scope classification | Re-read `book-llms/scopes.md`. Apply the decision heuristic (≥3 concepts → domain, cross-cutting → feature). |
| `organon validate` schema stage fails | Check frontmatter against `book-llms/frontmatter-system.md`. Common issues: missing required field, wrong type enum value. |
| `organon validate` content stage fails | Re-read template from `book-llms/templates.md`. Add missing sections. |
| Parent scope contradiction | Remove or weaken the contradicting constraint. Child scopes can only add, never relax. |
| Missing template section | Re-read the template. Every section in the template is required unless explicitly marked optional. |
| Bidirectional reference broken | Add the missing back-reference in the target file. Run `organon verify --gate triplets` to confirm. |
| File placed in wrong directory | Move file to correct location per Pattern A. Update any references to the old path. |
