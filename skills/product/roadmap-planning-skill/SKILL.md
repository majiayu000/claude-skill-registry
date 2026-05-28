---
document_name: "roadmap-planning.skill.md"
location: ".claude/skills/roadmap-planning.skill.md"
codebook_id: "CB-SKILL-ROADMAP-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for creating and maintaining product roadmaps"
skill_metadata:
  category: "product-management"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "Project goals defined"
    - "Requirements gathered"
category: "skills"
status: "active"
tags:
  - "skill"
  - "roadmap"
  - "product-management"
ai_parser_instructions: |
  This skill defines procedures for roadmap planning.
  Section markers: === SECTION ===
  Procedure markers: === PROCEDURE: NAME ===
---

# Roadmap Planning Skill

=== PURPOSE ===

This skill provides procedures for creating and maintaining product roadmaps. The roadmap is the source of truth for feature planning and prioritization.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(product-manager) @ref(CB-AGENT-PM-001) | Primary skill for roadmap work |

---

=== PREREQUISITES ===

Before using this skill:
- [ ] Project goals defined (@ref(CB-BIZ-GOALS-001))
- [ ] Requirements gathered
- [ ] Stakeholder input available

---

=== PROCEDURE: Create Roadmap ===

**Location:** `devdocs/business/roadmap.md`

**Steps:**
1. Define roadmap timeframe (quarters/months)
2. Align with business goals
3. Prioritize features using MoSCoW
4. Group features into milestones
5. Define dependencies between features
6. Get stakeholder alignment
7. Document in roadmap file

**Roadmap Format:**
```markdown
# Product Roadmap

## Vision
[High-level product vision]

## Q1 2026 - Theme: [Theme Name]

### Milestone: [Name] (v1.1.0)
**Target:** [Date]
**Goals:**
- [Goal 1]
- [Goal 2]

**Features:**
| Feature | Priority | Status | Epic |
|---------|----------|--------|------|
| [Name] | Must Have | Planned | #123 |
| [Name] | Should Have | Planned | #124 |

### Milestone: [Name] (v1.2.0)
...

## Q2 2026 - Theme: [Theme Name]
...
```

---

=== PROCEDURE: Milestone Planning ===

**Purpose:** Define and scope milestones

**Steps:**
1. Define milestone goal/theme
2. Select features for milestone
3. Estimate total scope
4. Identify dependencies
5. Set target date (coordinate with Delivery Lead)
6. Create GitHub milestone
7. Link issues to milestone

**Milestone Sizing Guidelines:**
- Small: 1-2 weeks, 3-5 issues
- Medium: 2-4 weeks, 5-10 issues
- Large: 4-8 weeks, 10-20 issues

---

=== PROCEDURE: Roadmap Review ===

**Purpose:** Keep roadmap current

**Frequency:** Monthly

**Steps:**
1. Review completed milestones
2. Update status of in-progress items
3. Re-prioritize based on learnings
4. Add new features from requirements
5. Remove or defer low-priority items
6. Communicate changes to stakeholders
7. Log changes in buildlog with `#micro-decision`

---

=== PROCEDURE: Priority Framework ===

**Purpose:** Consistent prioritization

**Frameworks:**
1. **MoSCoW** - Must/Should/Could/Won't
2. **RICE** - Reach, Impact, Confidence, Effort
3. **Value vs Effort** - Quick wins, big bets, fill-ins, money pits

**RICE Scoring:**
```
Score = (Reach × Impact × Confidence) / Effort

Reach: Users affected (number)
Impact: Effect per user (0.25-3)
Confidence: Certainty (0-100%)
Effort: Person-months
```

---

=== PROCEDURE: Dependency Mapping ===

**Purpose:** Identify feature dependencies

**Steps:**
1. List all planned features
2. For each feature, identify:
   - Technical dependencies
   - Feature dependencies
   - External dependencies
3. Create dependency graph
4. Identify critical path
5. Flag blocked items

**Notation:**
- `→` depends on
- `↔` mutual dependency
- `⊗` external blocker

---

=== ANTI-PATTERNS ===

### Over-Planning
**Problem:** Detailed roadmap for 12+ months
**Solution:** Detail for 1-2 quarters, themes for further out

### No Flexibility
**Problem:** Rigid roadmap that doesn't adapt
**Solution:** Regular reviews, embrace change

### Missing Dependencies
**Problem:** Features blocked by undocumented dependencies
**Solution:** Explicit dependency mapping

### Stakeholder Misalignment
**Problem:** Roadmap doesn't reflect stakeholder needs
**Solution:** Regular stakeholder reviews

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(requirements-gathering) | Requirements feed roadmap |
| @skill(issue-management) | Roadmap items become issues |
| @skill(release-management) | Roadmap guides releases |
