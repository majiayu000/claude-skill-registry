---
name: staged-content-refinement
model: reasoning
description: Consolidate and refine extracted skills and docs from multiple projects into unified, project-agnostic patterns. Use when staging folder has content from multiple projects ready for consolidation. Triggers on "refine staged content", "consolidate staged skills", "process staging", "merge extracted patterns".
---

# Staged Content Refinement

Process extracted skills and docs from multiple projects into consolidated, project-agnostic patterns.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install refinement
```


---

## Before Starting

1. Verify staging has content from multiple projects:
   - `ai/staging/skills/` — Extracted skills
   - `ai/staging/docs/` — Extracted methodology docs

2. Load quality criteria: [`../extraction/references/skill-quality-criteria.md`](../extraction/references/skill-quality-criteria.md)

---

## Refinement Process

### Phase 1: Inventory

Scan all staged content and catalog what exists.

**For skills:**
```
ai/staging/skills/
├── [project-a]-[category]/
├── [project-b]-[category]/
└── ...
```

**For docs:**
```
ai/staging/docs/
├── [project-a]-summary.md
├── [project-a]-design-system.md
├── [project-b]-summary.md
└── ...
```

**Create inventory:**

| Source Project | Type | Content | Common Patterns? |
|----------------|------|---------|------------------|
| project-a | skill | design-system | Yes - colors, typography |
| project-b | skill | design-system | Yes - similar token structure |
| project-a | doc | summary | Methodology insights |

---

### Phase 2: Pattern Analysis

Identify patterns that appear across multiple projects.

**Look for:**

1. **Design system patterns** (highest priority)
   - Common token structures
   - Similar aesthetic approaches
   - Shared color/typography patterns

2. **Architecture patterns**
   - Similar folder structures
   - Common component organization
   - Shared data flow patterns

3. **Workflow patterns**
   - Common Makefile targets
   - Similar CI/CD approaches
   - Shared dev setup patterns

4. **Methodology insights**
   - Decision-making patterns
   - Trade-offs that appear repeatedly
   - Common anti-patterns discovered

**Questions to answer:**

- What patterns appear in 2+ projects?
- What's project-specific vs generalizable?
- What methodology insights can update the main docs?

---

### Phase 2.5: Conflict Detection

Before consolidating, check for conflicts with existing skills.

**Scan existing skills:**
```bash
ls ai/skills/*/
```

**For each staged skill, check:**

| Check | How |
|-------|-----|
| Duplicate name | Does a skill with same name exist in `ai/skills/`? |
| Similar purpose | Does description overlap with existing skill? |
| Overlapping triggers | Do "When to Use" triggers conflict? |

**Conflict resolution:**

| Conflict Type | Resolution |
|---------------|------------|
| Exact duplicate | Skip staged skill, keep existing |
| Similar but better | Update existing skill with new insights |
| Similar but different | Keep both, clarify distinct purposes |
| No conflict | Proceed with promotion |

**Run overlap check:**
```
/check-overlaps
```

**Document conflicts:**
- Note which existing skills overlap
- Decide: merge into existing vs create new
- Update existing skills if merging

---

### Phase 3: Consolidation

Merge similar patterns into unified, project-agnostic skills.

**For each pattern group:**

1. **Identify the core** — What's common across all instances?
2. **Strip project specifics** — Remove project names, specific values
3. **Generalize** — Make it applicable to any project
4. **Enhance** — Add insights learned from seeing multiple implementations

**Example consolidation:**

```
Staged:
├── project-a-design-system/  (retro-futuristic tokens)
├── project-b-design-system/  (video game UI tokens)
└── project-c-design-system/  (minimal dark tokens)

Consolidated:
└── design-system-patterns/   (how to build distinctive design systems)
    - Token structure patterns
    - Aesthetic direction documentation
    - Common anti-patterns across projects
```

**Consolidation rules:**

| Scenario | Action |
|----------|--------|
| Same pattern, different values | Create pattern skill with examples |
| Same pattern, same approach | Merge into single skill |
| Unique pattern, high value | Keep as standalone skill |
| Unique pattern, low value | Archive or discard |

---

### Phase 4: Methodology Updates

Extract insights to update the main methodology docs.

**Review staged docs for:**

1. **New patterns** not in current methodology
2. **Refinements** to existing approaches
3. **Anti-patterns** discovered across projects
4. **Decision rationale** worth capturing

**Update locations:**

| Insight Type | Update Location |
|--------------|-----------------|
| Design philosophy | `docs/METHODOLOGY.md` → Design & Visual Philosophy |
| Tech patterns | `docs/TECH-STACK.md` → Patterns to Extract |
| Workflow improvements | `docs/WORKFLOW.md` |
| Architecture patterns | `docs/ARCHITECTURE.md` |

---

### Phase 5: Promotion

Move refined skills to active locations.

**Skill promotion:**
```bash
# From staging to active
mv ai/staging/skills/[refined-skill]/ ai/skills/[refined-skill]/
```

**Doc updates:**
- Update main docs with methodology insights
- Archive or delete processed staging content

**Post-promotion:**
- Verify skills have proper descriptions
- Test skill activation with sample prompts
- Clean up staging folder

---

### Phase 6: Testing

After promotion, verify skills work correctly.

**Activation testing:**
For each promoted skill, test that it activates on expected triggers:

```
Test: "I need to [trigger from When to Use]"
Expected: Skill should be suggested/activated
```

**Quality verification:**
- [ ] Description triggers correctly
- [ ] Code examples are valid and runnable
- [ ] NEVER Do section is actionable
- [ ] Related skills are linked correctly

**Rollback if issues:**
```bash
# If skill has problems, move back to staging
mv ai/skills/[category]/[skill]/ ai/staging/skills/
```

**Document test results:**
- Note any activation issues
- Record false positives (activates when shouldn't)
- Record false negatives (doesn't activate when should)

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| Staging empty | Nothing to refine; run extraction first |
| No common patterns | Promote as individual skills if quality passes |
| Merge conflict | Document conflict, keep both versions temporarily |
| Quality check fails | Return to Phase 3 to improve skill |
| Activation test fails | Revise description keywords |

---

## Output Locations

**Refined skills go to:**
```
ai/skills/           # Cursor-specific skills
ai/skills/           # Claude Code skills (if applicable)
```

**Methodology updates go to:**
```
docs/
├── METHODOLOGY.md        # Philosophy and approach
├── TECH-STACK.md         # Technology patterns
├── ARCHITECTURE.md       # Skill/agent architecture
└── WORKFLOW.md           # Processes
```

**Staging cleanup:**
```
ai/staging/skills/        # Clear after processing
ai/staging/docs/          # Clear after processing
ai/archive/               # (optional) Keep for reference
```

---

## Consolidation Examples

### Design Systems

**Before (3 project-specific skills):**
- `project-a-design-system` — Retro-futuristic tokens
- `project-b-design-system` — Video game UI tokens  
- `project-c-design-system` — Cyberpunk terminal tokens

**After (1 consolidated skill):**
- `distinctive-design-systems` — How to create design systems with personality
  - Token structure patterns
  - Aesthetic documentation approach
  - Anti-patterns (generic bootstrap, "clean" without personality)
  - Examples from different aesthetic directions

### Architecture

**Before (multiple docs):**
- `project-a-architecture.md`
- `project-b-architecture.md`

**After:**
- Update `docs/ARCHITECTURE.md` with common patterns
- Create skill only if patterns are unique enough

---

## NEVER Do

- **NEVER keep project-specific details** in consolidated skills
- **NEVER create redundant skills** — Merge similar patterns
- **NEVER skip methodology updates** — Insights should flow back to docs
- **NEVER promote low-quality skills** — Must pass quality criteria
- **NEVER leave staging cluttered** — Clean up after processing

---

## Quality Check

Before finishing refinement:

- [ ] All staged content reviewed?
- [ ] Conflict detection completed (Phase 2.5)?
- [ ] Common patterns identified and consolidated?
- [ ] Consolidated skills are project-agnostic?
- [ ] Methodology docs updated with insights?
- [ ] Refined skills promoted to active locations?
- [ ] Activation testing completed (Phase 6)?
- [ ] Staging folder cleaned up?

---

## Related Skills

- **Agent:** [`ai/agents/refinement/`](../../agents/refinement/) — Autonomous refinement workflow
- **Command:** [`/refine-staged`](../../commands/refinement/refine-staged.md) — Quick refinement command
- **Command:** [`/promote-skill`](../../commands/refinement/promote-skill.md) — Single skill promotion
- **Previous step:** [`ai/skills/extraction/`](../extraction/) — Pattern extraction
- **Quality criteria:** [`../extraction/references/skill-quality-criteria.md`](../extraction/references/skill-quality-criteria.md)
