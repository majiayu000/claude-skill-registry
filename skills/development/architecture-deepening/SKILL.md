---
name: architecture-deepening
description: "Proactive architecture improvement: find shallow modules, propose deepening opportunities, design conversation."
user-invocable: true
command: architecture-deepening
context: fork
allowed-tools:
  - Agent
  - Bash
  - Read
  - Glob
  - Grep
routing:
  triggers:
    - deepen architecture
    - find shallow modules
    - architecture improvement
    - module depth analysis
    - deepening opportunities
    - improve module interfaces
    - reduce complexity
    - architecture deepening
  not_for: "small-scope refactors ('tidy this up', 'reorganize without changing behaviour', 'messy code in one file') — those route to workflow refactor; architecture-deepening is for module-interface analysis across the codebase, not local cleanup"
  pairs_with:
    - full-repo-review
    - adr-consultation
    - codebase-overview
  complexity: Medium
  category: analysis
---

# Architecture Deepening

Find shallow modules and propose deepening opportunities. Not a code review -- does not find bugs or style violations. Finds modules where the interface is too close to the implementation, where users must understand internals to use the API, and where small interface changes would absorb disproportionate complexity.

**When to use**: After codebase onboarding, before a major feature push, when new contributors report confusion, or when "how do I use this?" questions recur.

**Differs from full-repo-review**: Full-repo-review finds defects. This skill finds structural improvement opportunities. Pair well: run full-repo-review first to fix defects, then architecture-deepening to raise the bar.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Phase 1, module analysis, vocabulary terms | `vocabulary.md` | Shared architecture vocabulary: module, depth, seam, leverage, locality, deletion test |
| Phase 2, interface alternatives, parallel exploration | `interface-design.md` | Parallel sub-agent pattern for exploring alternative interfaces |
| Phase 2-3, dependency analysis, testing strategy | `deepening-strategies.md` | Dependency categorization, safe deepening patterns, testing strategies |

## Instructions

Execute all three phases in order. Each phase has a gate. The user is a collaborator -- present findings, get input, refine together.

Language-agnostic. Vocabulary and strategies apply to Go, Python, TypeScript, or any codebase with module boundaries.

### Phase 1: EXPLORE

**Goal**: Identify shallow modules -- where the interface exposes too much implementation detail.

**Step 1: Scope the codebase**

If user specified a directory/package, start there. Otherwise, scan for module boundaries.

```bash
find . -name "go.mod" -o -name "package.json" -o -name "pyproject.toml" -o -name "__init__.py" -o -name "index.ts" -o -name "mod.rs" 2>/dev/null | head -50

# Exported symbols per package (Go)
grep -rn "^func [A-Z]" --include="*.go" | cut -d: -f1 | sort | uniq -c | sort -rn | head -20

# Public exports (TypeScript)
grep -rn "^export " --include="*.ts" --include="*.tsx" | cut -d: -f1 | sort | uniq -c | sort -rn | head -20
```

**Step 2: Apply shallowness signals**

Read `references/vocabulary.md` for full vocabulary. A module is shallow when:
- Interface nearly as complex as implementation (high surface-area-to-depth ratio)
- Users must read source to understand how to call it
- Setup requires knowledge of internal state
- Error messages expose implementation details
- Multiple modules must coordinate for a single logical operation

Score each: **HIGH** (clear shallowness, high-leverage fix), **MEDIUM** (some shallowness, moderate leverage), **LOW** (minor, low impact).

**Step 3: Identify seams**

For HIGH-scored modules, identify seams -- natural boundaries where the module could absorb more responsibility. See `references/vocabulary.md` for seam types (data, protocol, temporal).

**Gate**: At least 3 candidates with shallowness scores and seam analysis. If fewer than 3, document why and proceed.

---

### Phase 2: PRESENT CANDIDATES

**Goal**: Show findings, explore interface alternatives for top candidates.

**Step 1: Present findings table**

```markdown
| Module | Depth Score | Shallowness Signal | Seam | Leverage |
|--------|------------|-------------------|------|----------|
| pkg/config | HIGH | Users must know YAML structure to use API | Data seam | High -- 12 callers |
| internal/auth | MEDIUM | Token refresh logic leaks to callers | Protocol seam | Medium -- 4 callers |
```

For each: what it does today, why it is shallow (cite specific interface elements), where the seam is, the leverage (how many callers benefit).

**Step 2: Get user input**

Ask which candidates to explore. Do not proceed to interface design without confirmation -- the user knows codebase priorities better.

**Step 3: Explore interface alternatives**

Read `references/interface-design.md` and `references/deepening-strategies.md`. Design 2-3 alternative interfaces per candidate:
- New interface signature (function names, parameters, return types)
- What moves behind the interface (what callers no longer need to know)
- Deletion test result: what caller code can be deleted
- Trade-offs: flexibility lost, edge cases needing escape hatches

**Gate**: At least 2 alternatives per selected candidate. User confirmed candidates. Each alternative includes deletion test result.

---

### Phase 3: DESIGN CONVERSATION

**Goal**: Grill the chosen approach until the best deepening emerges. Collaborative design, not presentation.

**Step 1: Challenge each alternative**

- **Locality**: Does this keep related things together or scatter responsibility?
- **Escape hatches**: What happens when a caller needs old flexibility? Clean override path or workarounds?
- **Migration**: Incremental adoption or all-or-nothing?
- **Testing**: How to test the deepened module? See `references/deepening-strategies.md`.
- **Second-order effects**: Does deepening here create new shallowness elsewhere?

**Step 2: Iterate until convergence**

Continue until:
- Agreement on a specific approach, OR
- User decides current structure is acceptable after examining alternatives

No fixed round count. Each round should narrow the design space. If not converging, surface it: "We have been going back and forth on X -- should we pick one, or is this a sign the deepening is not worth it?"

**Step 3: Document the decision**

```markdown
## Deepening Decision: {module name}

**Current interface**: {what callers see today}
**Proposed interface**: {what callers would see after}
**What moves behind the interface**: {details callers no longer manage}
**Deletion test**: {what caller code can be removed}
**Migration path**: {incremental adoption plan}
**Trade-offs accepted**: {flexibility traded for simplicity}
**Next step**: {specific first action -- "create ADR", "prototype in branch", "discuss with team"}
```

If user wants to formalize, suggest pairing with `adr-consultation`.

**Gate**: Design conversation completed. Decision documented with all fields. Next step identified.

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No shallow modules found | Well-structured or too small codebase | Valid outcome. Suggest re-running after next major feature. |
| Too many candidates | Pervasive shallowness | Focus on 5 highest-leverage (most callers benefit). Split into sessions by subsystem. |
| User disagrees with assessment | Model misjudged boundaries or caller patterns | Ask user to explain design intent. Complexity may be intentional (performance, backward compatibility). |
| Design conversation does not converge | Fundamental trade-off disagreement | Surface explicitly. Suggest prototyping both in separate branches. |

---

## References

- [Vocabulary](references/vocabulary.md) -- Shared architecture vocabulary: module, depth, seam, leverage, locality, deletion test
- [Interface Design](references/interface-design.md) -- Patterns for exploring alternative interfaces
- [Deepening Strategies](references/deepening-strategies.md) -- Dependency categorization and testing strategies for safe deepening
