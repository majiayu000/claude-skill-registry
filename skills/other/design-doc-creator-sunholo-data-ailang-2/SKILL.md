---
name: Design Doc Creator
description: Create AILANG design documents in the correct format and location. Use when user asks to create a design doc, plan a feature, or document a design. Handles both planned/ and implemented/ docs with proper structure.
---

# Design Doc Creator

Create well-structured design documents for AILANG features following the project's conventions.

## Quick Start

**Most common usage:**
```bash
# User says: "Create a design doc for better error messages"
# This skill will:
# 1. Ask for key details (priority, version target)
# 2. Create design_docs/planned/better-error-messages.md
# 3. Fill template with proper structure
# 4. Guide you through customization
```

## When to Use This Skill

Invoke this skill when:
- User asks to "create a design doc" or "write a design doc"
- User says "plan a feature" or "design a feature"
- User mentions "document the design" or "create a spec"
- Before starting implementation of a new feature
- After completing a feature (to move to implemented/)

## Available Scripts

### `scripts/create_planned_doc.sh <doc-name> [version]`
Create a new design document in `design_docs/planned/`.

**Version Auto-Detection:**
The script automatically detects the current AILANG version from `CHANGELOG.md` and suggests the next version folder. This prevents accidentally placing docs in wrong version folders.

**Usage:**
```bash
# See current version and suggested target
.claude/skills/design-doc-creator/scripts/create_planned_doc.sh
# Output: Current AILANG version: v0.5.6
#         Suggested next version: v0_5_7

# Create doc in planned/ root (no version)
.claude/skills/design-doc-creator/scripts/create_planned_doc.sh m-dx2-better-errors

# Create doc in next version folder (recommended)
.claude/skills/design-doc-creator/scripts/create_planned_doc.sh reflection-system v0_5_7
```

**What it does:**
- Detects current version from CHANGELOG.md
- Suggests next patch version for targeting
- Creates design doc from template
- Places in correct directory (planned/ or planned/VERSION/)
- Fills in creation date
- Shows version context in output

### `scripts/move_to_implemented.sh <doc-name> <version>`
Move a design document from planned/ to implemented/ after completion.

**Usage:**
```bash
.claude/skills/design-doc-creator/scripts/move_to_implemented.sh m-dx1-developer-experience v0_3_10
```

**What it does:**
- Finds doc in planned/
- Copies to implemented/VERSION/
- Updates status to "Implemented"
- Updates last modified date
- Provides template for implementation report
- Keeps original until you verify and commit

## Workflow

### Creating a Planned Design Doc

**1. Gather Requirements**

Ask user:
- What feature are you designing?
- What version is this targeted for? (e.g., v0.4.0)
- What priority? (P0/P1/P2)
- Estimated effort? (e.g., 2 days, 1 week)
- Any dependencies on other features?

**⚠️ CRITICAL: Audit for Systemic Issues FIRST**

**Before writing a design doc for a bug fix, ALWAYS ask: "Is this part of a larger pattern?"**

**The Anti-Pattern (incremental special-casing):**
```
v1: Add feature for case A
v2: Bug! Add special case for B
v3: Bug! Add special case for C
v4: Bug! Add special case for D
...forever patching
```

**The Pattern to Follow (unified solutions):**
```
v1: Bug report for case B
    BEFORE writing design doc:
    1. Search for similar code paths
    2. Check if A, C, D have same gap
    3. Design ONE fix covering ALL cases
v2: Unified fix - no future bugs in this area
```

**Concrete Example (M-CODEGEN-UNIFIED-SLICE-CONVERTERS, Dec 2025):**
```
Bug reported: [SolarPlanet] return type panics

❌ Quick fix design doc: Add ConvertToSolarPlanetSlice
   (Will need ConvertToAnotherRecordSlice later...)

✅ Systemic design doc: Audit ALL slice types
   Found: []float64 ALSO broken!
   Found: []*ADTType partially broken!
   One unified fix covers all 3 gaps.
```

**Analysis Checklist (do BEFORE writing design doc):**
- [ ] Is this a one-off or part of a pattern?
- [ ] Search codebase for similar code paths
- [ ] Check if other types/cases have the same gap
- [ ] Look at git history - has this area been patched repeatedly?
- [ ] Design fix to cover ALL cases, not just the reported one

**🔍 Use `ailang docs search` to Check Existing Work:**

Before creating a design doc, search for existing implementations:

```bash
# Check if feature already implemented
ailang docs search --stream implemented "feature keywords"

# Check if design doc already planned
ailang docs search --stream planned "feature keywords"

# Use neural search for semantic matching (requires Ollama, slow ~20-30s)
ailang docs search --stream planned --neural "semantic description of feature"

# Search with JSON output for programmatic use
ailang docs search --stream implemented --json "keywords"
```

**Example workflow:**
```bash
# Before creating "lazy embeddings" design doc:
$ ailang docs search --stream implemented "embedding cache"
🔍 SimHash search: "embedding cache"
   Scanned: 42 docs

No matching documents found.
# ✅ Safe to create - not implemented yet

$ ailang docs search --stream planned "lazy embedding"
🔍 SimHash search: "lazy embedding"
   Scanned: 28 docs

1. design_docs/planned/v0_5_11/m-doc-sem-lazy-embeddings.md (0.85)
# ⚠️ Already planned - review existing doc first
```

**Key flags:**
- `--stream implemented` - Only search implemented/ directory
- `--stream planned` - Only search planned/ directory
- `--neural` - Use semantic embeddings (finds conceptually similar docs, **slow: ~20-30s**)
- `--limit N` - Return top N results
- `--json` - JSON output for scripting

**Performance note:** SimHash search (without `--neural`) is instant. Only use `--neural` when keyword matching isn't finding what you need.

**Warning Signs of Fragmented Design:**
- Multiple maps tracking similar things (`adtSliceTypes`, `recordTypes`...)
- Switch statements with growing case lists
- Functions named `handleX`, `handleY`, `handleZ` instead of unified `handle`
- Bug fixes that add `|| specialCase` conditions

**When these signs appear:** Expand scope of design doc to unify the system.

**⚠️ IMPORTANT: Keep AILANG's Vision in Mind**

**AI-first DX = Minimize Syntactic Entropy**

The goal of every feature is to make AILANG the most **machine-decidable**, **context-efficient**, and **deterministic** language for AI coders.

Before writing a design doc, verify that the proposed feature **strictly improves one or more** of the following metrics — and **does not degrade any**:

| Principle | Definition | Design-time Test |
|-----------|------------|------------------|
| ✅ **Reduce Syntactic Noise** | Remove or infer repetitive scaffolding (imports, effect declarations, boilerplate) | "Can an AI express the same intent with fewer tokens or less redundancy?" |
| ✅ **Preserve Semantic Clarity** | Keep meaning explicit and compositional even when syntax is inferred | "Would another AI (or static checker) interpret this code identically?" |
| ✅ **Increase Determinism** | Ensure identical inputs produce identical ASTs and effects. Avoid implicit state, random order, or hidden magic. | "Could this feature be fully round-tripped through the compiler?" |
| ✅ **Lower Token Cost** | Minimize the number of tokens and transformations needed for the AI to express intent and the compiler to verify it | "Does this feature shorten the conversational path from intent → executable?" |

### 🧭 Implementation Guidance

**Score the proposed feature across these axes:**

| Axis | −1 (hurts) | 0 (neutral) | +1 (helps) |
|------|------------|-------------|------------|
| Syntactic Noise | adds boilerplate | — | removes boilerplate |
| Semantic Clarity | adds ambiguity | — | clearer, self-describing |
| Determinism | introduces nondeterminism | — | increases reproducibility |
| Token Cost | increases context size | — | lowers token footprint |

**Decision rule:**
- Net score **> +1**: Move forward to draft
- Net score **≤ 0**: Reject or redesign

### 💡 Examples

| Feature | Score | Why |
|---------|-------|-----|
| ✅ Entry-module Prelude (`print`) | **+3** | Removes boilerplate (+1), Deterministic injection (+1), Token savings (+1) |
| ✅ Auto-cap inference (`!{IO}`) | **+2** | Syntactic noise ↓ (+1), Semantic clarity maintained (0), Token cost ↓ (+1) |
| ❌ Global mutable state | **−2** | Violates determinism (−2) |
| ⚠️ Optional type annotations | **±0** | Only if inference remains stable and predictable |

### 🧠 Conceptual Frame

**Think of every feature as a compression algorithm for code intent.**

The better the compression, the lower the entropy, and the more efficiently an AI can operate in that linguistic medium.

### What AILANG Is NOT Optimized For

- ❌ IDE features (autocomplete, hover, refactoring)
- ❌ Human concurrency patterns (CSP channels → static task graphs)
- ❌ Familiar syntax from other languages (if it adds entropy)

### Reference Documents

- [VISION_BENCHMARKS.md](../../../benchmarks/VISION_BENCHMARKS.md) - Vision goals and success metrics
- [Example Parity & Vision Alignment](../../../design_docs/planned/v0_3_15/example-parity-vision-alignment.md) - AI-first DX philosophy detailed
- [Auto-Capability Inference](../../../design_docs/planned/20251013_auto_caps_capability_inference.md) - Example of entropy reduction

**2. Choose Document Name**

**Naming conventions:**
- Use lowercase with hyphens: `feature-name.md`
- For milestone features: `m-XXX-feature-name.md` (e.g., `m-dx2-better-errors.md`)
- Be specific and descriptive
- Avoid generic names like `improvements.md`

**3. Run Create Script**

```bash
# If version is known (most cases)
.claude/skills/design-doc-creator/scripts/create_planned_doc.sh feature-name v0_4_0

# If version not decided yet
.claude/skills/design-doc-creator/scripts/create_planned_doc.sh feature-name
```

**4. Customize the Template**

The script creates a comprehensive template. Fill in:

**Header section:**
- Feature name (replace `[Feature Name]`)
- Status: Leave as "Planned"
- Target: Version number (e.g., v0.4.0)
- Priority: P0 (High), P1 (Medium), or P2 (Low)
- Estimated: Time estimate (e.g., "3 days", "1 week")
- Dependencies: List prerequisite features or "None"

**Problem Statement:**
- Describe current pain points
- Include metrics if available (e.g., "takes 7.5 hours")
- Explain who is affected and how

**Goals:**
- Primary goal: One-sentence main objective
- Success metrics: 3-5 measurable outcomes

**Solution Design:**
- Overview: High-level approach
- Architecture: Technical design
- Implementation plan: Break into phases with tasks
- Files to modify: List new/changed files with LOC estimates

**Examples:**
- Show before/after code or workflows
- Make examples concrete and runnable

**Success Criteria:**
- Checkboxes for acceptance tests
- Include "All tests passing" and "Documentation updated"

**Timeline:**
- Week-by-week breakdown
- Realistic estimates (2x your initial guess!)

**5. Review and Commit**

```bash
git add design_docs/planned/feature-name.md
git commit -m "Add design doc for feature-name"
```

### Moving to Implemented

**When to move:**
- Feature is complete and shipped
- Tests are passing
- Documentation is updated
- Version is tagged/released

**1. Run Move Script**

```bash
.claude/skills/design-doc-creator/scripts/move_to_implemented.sh feature-name v0_3_14
```

**2. Add Implementation Report**

The script provides a template. Add:

**What Was Built:**
- Summary of actual implementation
- Any deviations from plan

**Code Locations:**
- New files created (with LOC)
- Modified files (with +/- LOC)

**Test Coverage:**
- Number of tests
- Coverage percentage
- Test file locations

**Metrics:**
- Before/after comparison table
- Show improvements achieved

**Known Limitations:**
- What's not yet implemented
- Edge cases not handled
- Performance limitations

**3. Update design_docs/README.md**

Add entry under appropriate version:

```markdown
### v0.3.14 - Feature Name (October 2024)
- Brief description of what shipped
- Key improvements
- [CHANGELOG](../CHANGELOG.md#v0314)
```

**4. Commit Changes**

```bash
git add design_docs/implemented/v0_3_14/feature-name.md design_docs/README.md
git commit -m "Move feature-name design doc to implemented (v0.3.14)"
git rm design_docs/planned/feature-name.md
git commit -m "Remove feature-name from planned (moved to implemented)"
```

## Design Doc Structure

See [resources/design_doc_structure.md](resources/design_doc_structure.md) for:
- Complete template breakdown
- Section-by-section guide
- Best practices for each section
- Common mistakes to avoid

## Best Practices

### 1. Be Specific

**Good:**
```markdown
**Primary Goal:** Reduce builtin development time from 7.5h to 2.5h (-67%)
```

**Bad:**
```markdown
**Primary Goal:** Make development easier
```

### 2. Include Metrics

**Good:**
```markdown
**Current State:**
- Development time: 7.5 hours per builtin
- Files to edit: 4
- Type construction: 35 lines
```

**Bad:**
```markdown
**Current State:**
- Development takes a long time
```

### 3. Break Into Phases

**Good:**
```markdown
**Phase 1: Core Registry** (~4 hours)
- [ ] Create BuiltinSpec struct
- [ ] Implement validation
- [ ] Add unit tests

**Phase 2: Type Builder** (~3 hours)
- [ ] Create DSL methods
- [ ] Add fluent API
- [ ] Test with existing builtins
```

**Bad:**
```markdown
**Implementation:**
- Build everything
```

### 4. Link to Examples

**Good:**
```markdown
See existing M-DX1 implementation:
- design_docs/implemented/v0_3_10/M-DX1_developer_experience.md
- internal/builtins/spec.go
```

**Bad:**
```markdown
Similar to other features
```

### 5. Realistic Estimates

**Rule of thumb:**
- 2x your initial estimate (things always take longer)
- Add buffer for testing and documentation
- Include time for unexpected issues

**Good:**
```markdown
**Estimated**: 3 days (6h implementation + 4h testing + 2h docs + buffer)
```

**Bad:**
```markdown
**Estimated**: Should be quick, maybe 2 hours
```

## Document Locations

```
design_docs/
├── planned/              # Future features
│   ├── feature.md        # Unversioned (version TBD)
│   └── v0_4_0/           # Targeted for v0.4.0
│       └── feature.md
└── implemented/          # Completed features
    ├── v0_3_10/          # Shipped in v0.3.10
    │   └── feature.md
    └── v0_3_14/          # Shipped in v0.3.14
        └── feature.md
```

**Version folder naming:**
- Use underscores: `v0_3_14` not `v0.3.14`
- Match CHANGELOG.md tags exactly
- Create folder when first doc needs it

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (workflow overview)
2. **Execute as needed**: Scripts create/move docs
3. **Load on demand**: `resources/design_doc_structure.md` (detailed guide)

## Notes

- All design docs should follow the template structure
- Update CHANGELOG.md when features ship (separate from design doc)
- Link design docs from README.md under version history
- Keep design docs focused - split large features into multiple docs
- Use M-XXX naming for milestone/major features
