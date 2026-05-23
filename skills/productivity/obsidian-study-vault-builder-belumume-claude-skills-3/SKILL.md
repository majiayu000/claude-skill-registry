---
name: obsidian-study-vault-builder
description: Build comprehensive, mobile-compatible Obsidian study vaults from academic course materials with checkpoint-based workflow, error pattern recognition, and quality assurance. Battle-tested patterns from 828KB/37-file projects. Works across all subjects - CS, medicine, business, self-study.
version: 2.1.0
tags:
  - obsidian
  - education
  - knowledge-management
  - markdown
  - study-materials
  - academic
---

# Obsidian Study Vault Builder

> **Comprehensive patterns for building exam-ready study vaults in Obsidian**

Build structured, mobile-compatible academic study vaults with systematic error prevention, quality assurance, and efficiency patterns extracted from real-world projects.

**⚠️ IMPORTANT: See REFERENCE.md for complete battle-tested patterns from 828KB/37-file vault projects.**

## When to Use This Skill

Invoke when building academic study materials in Obsidian for:
- Final exam preparation (any subject)
- Course knowledge organization (CS, medicine, business, law, etc.)
- Self-study material structuring
- Technical documentation vaults
- Large-scale study projects (10+ files, 200KB+)

**Works across all subjects:**
- Computer Science (algorithms, data structures, systems)
- Medicine (anatomy, pharmacology, pathology)
- Business (finance, marketing, operations)
- STEM (physics, chemistry, engineering)
- Humanities (history, literature, philosophy)

---

## Core Methodology

### Checkpoint-Based Workflow (Critical)

**Never generate all chapters upfront.** Use progressive validation:

1. **Chapter 1 Generation** → STOP
2. **User Review** → Approve format, structure, quality
3. **Chapters 2-N** → Continue with validated pattern
4. **Final QA** → Systematic verification

**Why this matters:**
- Catches format issues before they multiply across 30+ files
- Validates approach matches user needs early
- Adjusts course when cheap (Chapter 1) vs expensive (Chapter 8)
- Prevents 5+ hours of rework

**Time breakdown:** Chapter 1 (~30 min) → Review (~15 min) → Remaining (~90 min) → QA (~30 min) = **2.5 hours vs 80 hours manual**

### Memory File Hierarchy

Three-level context structure (see REFERENCE.md for details):
- **Level 1:** Root vault (`CLAUDE.md`)
- **Level 2:** Subject folder (`School/CLAUDE.md`)
- **Level 3:** Course project (`School/algorithms/CLAUDE.md`)

---

## Universal Obsidian Features (Mobile-First)

✅ **Use only:** Mermaid diagrams, LaTeX math, standard callouts, internal links, tables, code blocks
❌ **Never use:** Dataview queries, custom callouts, plugins

**See REFERENCE.md for complete patterns.**

---

## Error Pattern Recognition (8 Patterns)

### Pattern 1: Unicode Corruption in Mermaid
- **Symptom:** Diagrams fail to render
- **Diagnosis:** `grep -r "≤\|≥\|∞\|∈\|≠\|→" *.md`
- **Fix:** Replace with ASCII (`<=`, `>=`, `infinity`, `in`, `!=`, `->`)

### Pattern 2: Broken Tables (LaTeX Pipes)
- **Diagnosis:** `grep -r "| \$.*|.*\$" *.md`
- **Fix:** Escape pipes: `|` → `\|`

### Pattern 3: Missing Collapsible Solutions
- **Diagnosis:** `grep -A 5 "## Problem" practice-problems.md | grep -v "\[!example\]-"`
- **Fix:** Use `> [!example]- Solution`

### Pattern 4-8: See REFERENCE.md
- Inconsistent navigation
- Missing learning objectives
- Inconsistent TOC
- Empty core concepts
- Broken cross-references

**Complete systematic fix approach in REFERENCE.md.**

---

## Content Quality Patterns

### Applied Understanding (Not Memorization)

**Good questions:**
- "Design [system] for [context]. Current [problem]. Describe solution to achieve [goal]. Analyze trade-offs and justify."

**Adapts to subject:**
- CS: Algorithm design scenarios
- Medicine: Case-based diagnosis
- Business: Strategic analysis
- Physics: Experimental design

### Comprehensive Coverage
Every topic from source materials must appear. Validation: cross-reference source outline with vault TOC.

### Cross-Reference Pattern
Link related concepts everywhere with `[[links]]`.

**See REFERENCE.md for complete examples.**

---

## Standard Vault Structure

```
course-name/
├── 00-overview/          # Course map, schedule, strategy
├── 01-chapter-name/      # Core concepts, quick-ref, practice
├── cross-chapter/        # Comparisons, patterns, catalog
└── mock-exams/           # Practice tests + solutions
```

---

## Quality Assurance (Summary)

Before marking complete:
- [ ] Structural consistency (navigation, objectives, TOC)
- [ ] Content completeness (all topics covered)
- [ ] Format correctness (no Unicode in Mermaid, LaTeX pipes escaped)
- [ ] Mobile compatibility (no plugins)
- [ ] Assessment alignment (practice matches exam style)

**See REFERENCE.md for complete 50+ item checklist.**

---

## Common Anti-Patterns

1. **"I'll Fix It Later"** → Fix immediately
2. **Generating Without Checkpoints** → Chapter 1 → Review → Continue
3. **Forgetting Mobile Users** → Universal features only
4. **Surface-Level Practice** → Scenario-based with reasoning

---

## Success Metrics

**Typical project:**
- Files: 30-40
- Size: 600-900KB
- Coverage: 100% of source topics
- Rendering errors: 0
- Time saved: 80+ hours
- Practice problems: 80-100
- Mock exams: 2-3

---

## Integration Patterns

### Task Agents for Large Analysis
For 100+ pages of materials, use Task tool with subagent_type=Explore.

### Git Workflow
```bash
git commit -m "Initial vault structure"
git commit -m "Complete Chapter 1 (checkpoint)"
git commit -m "Complete: Study vault (37 files, 828KB)"
```

---

## Additional Resources

**See REFERENCE.md for:**
- Complete Obsidian universal features documentation
- Detailed Mermaid diagram patterns (flowcharts, mind maps, graphs, recursion trees)
- Detailed LaTeX notation patterns with table escaping
- Collapsible solution complete templates
- Full 50+ item quality assurance checklist with examples
- Subject-specific adaptation examples (CS, medicine, business, humanities)
- Complete step-by-step workflow example
- Error pattern recognition (all 8 patterns with examples)
- Systematic fix approach (5-step process)
- Communication patterns that work
- Anti-patterns to avoid
- Time investment breakdowns

---

**Battle-tested on:**
- 37-file academic vaults
- 828KB comprehensive coverage
- Multiple subjects (CS, engineering, business)
- Zero rendering errors achieved
- ~80 hours manual work saved per project

**Ready to build exam-ready study vaults across any subject with systematic quality assurance.**
