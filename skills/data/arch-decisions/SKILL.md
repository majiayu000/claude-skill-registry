---
name: arch-decisions
description: '> ADR, database selection ve capacity planning.'
---

---
name: arch_decisions
router_kit: DevOpsKit
description: ADR template, database selection, capacity planning ve scalability.
metadata:
  skillport:
    category: thinking
    tags: [arch decisions, architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - arch-patterns
---

# 📋 Architecture Decisions

> ADR, database selection ve capacity planning.

---

## 📝 ADR Template

```markdown
# ADR-001: Database Selection

## Status: Accepted

## Context
[Problem açıklaması]

## Decision
PostgreSQL kullanacağız.

## Consequences
### Positive
- ACID compliance
### Negative
- Horizontal scaling zor

## Alternatives
- MongoDB: Rejected - JOINs için uygun değil
```

---

## 🗄️ Database Selection

| SQL | NoSQL |
|-----|-------|
| Complex JOINs | Flexible schema |
| ACID | High throughput |
| Transactions | Horizontal scale |

---

## 📊 Capacity Planning

```markdown
DAU: 1M users
Requests: 20/user/day = 20M/day
RPS: 20M / 86400 = ~230 RPS
Peak: 230 × 3 = ~700 RPS
```

---

*Architecture Decisions v1.0*

## 🔄 Workflow

> **Kaynak:** [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)

### Aşama 1: Problem Identification
- [ ] **Context**: Problemi ve etkilerini net tanımla.
- [ ] **Constraints**: Kısıtlamaları (Bütçe, Zaman, Teknoloji) belirle.
- [ ] **Options**: En az 2 alternatif çözüm yolu belirle.

### Aşama 2: Proposal (Status: Proposed)
- [ ] **Draft**: ADR şablonunu doldur.
- [ ] **RFC**: Takımdan yorum iste (Pull Request veya Toplantı).
- [ ] **Evaluation**: Alternatifleri kriterlere göre puanla (Pros/Cons).

### Aşama 3: Decision (Status: Accepted/Rejected)
- [ ] **Consensus**: Kararı netleştir ve statüyü güncelle.
- [ ] **Implications**: Kararın uzun vadeli etkilerini (Consequences) yaz.
- [ ] **Commit**: ADR dosyasını repoya ekle.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Problem ve alternatifler net mi? |
| 2 | Takım görüşü alındı mı? |
| 3 | Kararın "Consequences" bölümü dürüstçe yazıldı mı? |
