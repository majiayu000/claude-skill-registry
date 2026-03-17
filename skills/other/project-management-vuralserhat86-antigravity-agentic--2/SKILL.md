---
name: project_management
router_kit: ManagementKit
version: 1.0.0
type: knowledge
description: This skill should be used when creating or updating PROJECT.md files, planning sprints, defining project goals, or managing project scope. It provides templates and best practices for PROJECT.md-first development.
keywords: project.md, milestone, sprint, roadmap, planning, goals, scope, constraints, project management, okr, smart goals
auto_activate: true
allowed-tools: [Read, Write, Edit, Grep, Glob]
metadata:
  skillport:
    category: auto-healed
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - project_management
---

# Project Management Skill

PROJECT.md-first project management, goal setting, scope definition, and sprint planning.

## When This Skill Activates


- Creating or updating PROJECT.md files
- Defining project goals and scope
- Planning sprints or milestones
- Validating alignment with goals
- Project roadmap creation
- Keywords: "project.md", "goals", "scope", "sprint", "milestone", "roadmap"


---

## Core Concepts

### Overview

This skill provides comprehensive guidance on project management. For detailed patterns and implementation examples, see the documentation files in `docs/`.

**Key Topics**:
- Detailed methodologies and best practices
- Implementation patterns and examples
- Common pitfalls and anti-patterns
- Cross-references to related skills

**See**: Documentation files in `docs/` directory for complete details


---

## Quick Reference

| Topic | Details |
|-------|---------|
| Detailed Guide 1 | `docs/detailed-guide-1.md` |
| Detailed Guide 2 | `docs/detailed-guide-2.md` |
| Detailed Guide 3 | `docs/detailed-guide-3.md` |

---

## Progressive Disclosure

This skill uses progressive disclosure to prevent context bloat:

- **Index** (this file): High-level concepts and quick reference (<500 lines)
- **Detailed docs**: `docs/*.md` files with implementation details (loaded on-demand)

**Available Documentation**:
- `docs/detailed-guide-1.md` - Detailed implementation guide
- `docs/detailed-guide-2.md` - Detailed implementation guide
- `docs/detailed-guide-3.md` - Detailed implementation guide

---

## Cross-References

**Related Skills**:
- See PROJECT.md for complete skill dependencies

**Related Tools**:
- See documentation files for tool-specific guidance


---

## Key Takeaways

1. Research existing patterns before implementing
2. Follow established best practices
3. Refer to detailed documentation for implementation specifics
*Project Management v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Linear Method](https://linear.app/method) & [Shape Up (Basecamp)](https://basecamp.com/shapeup)

### Aşama 1: Planning (Cycle & Scope)
- [ ] **PROJECT.md**: Projenin "Single Source of Truth" dosyası. Hedefler, kapsam ve "Non-Goals" (Yapılmayacaklar) burada netleşir.
- [ ] **Cycle Planning**: 2 haftalık Sprint'ler yerine, teslim odaklı "Cycle"lar (Cool-down süresi ile) planla.
- [ ] **Appetite**: "Bu iş ne kadar sürer?" yerine "Bu işe ne kadar zaman ayırmak istiyoruz?" (Betting) yaklaşımını kullan.

### Aşama 2: Executive (Async-First)
- [ ] **Daily Updates**: Toplantı yerine, asenkron daily check-in (Standup botu veya metin) kullan.
- [ ] **Issue Triage**: Gelen bug/feature isteklerini hemen "Inbox"tan (Triage) uygun duruma (Backlog/Icebox/Next Cycle) taşı.
- [ ] **Decision Log**: Kritik kararları (ADR - Architecture Decision Records) yazılı olarak kaydet, sözlü bırakma.

### Aşama 3: Review & Retrospective
- [ ] **Demo**: Cycle sonunda çalışan yazılımı demo yap (Deploy edilmiş link üzerinden).
- [ ] **Retro**: "Ne iyi gitti?", "Ne kötü gitti?" yerine "Süreci nasıl iyileştiririz?" odaklı aksiyonlar al.
- [ ] **Cleanup**: Tamamlanan işleri arşivle, kalanları bir sonraki Cycle'a taşıma (re-evaluate et).

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | PROJECT.md güncel mi? (Kod ile senkronize mi?) |
| 2 | "Blocked" olan işler 24 saatten uzun süre bekledi mi? |
| 3 | Cycle Time (İşe başlama -> Bitiş) hedeflenen sürede mi? |

