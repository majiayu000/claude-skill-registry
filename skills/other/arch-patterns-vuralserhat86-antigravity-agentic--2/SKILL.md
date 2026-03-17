---
name: arch_patterns
router_kit: FullStackKit
description: Architecture patterns - monolith vs microservices, layered, event-driven, CQRS.
metadata:
  skillport:
    category: thinking
    tags: [arch patterns, architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - arch-decisions
---

# 🏗️ Architecture Patterns

> Sistem mimarisi pattern'ları.

---

## ⚠️ Bu Skill vs `design-patterns`

| Bu Skill | `design-patterns` |
|----------|-------------------|
| **Sistem** mimarisi | **UI/UX** tasarım |
| Microservices, CQRS | Z-index, shadows |
| Database, scaling | Animation, spacing |

> **Kural:** Backend/sistem → bu skill, Frontend/UI → `design-patterns`

---

## ⚖️ Monolith vs Microservices

| Aspect | Monolith | Microservices |
|--------|----------|---------------|
| Complexity | Düşük | Yüksek |
| Scaling | Tüm uygulama | Service bazlı |
| Team Size | Küçük | Büyük |

**Seç:**
- Monolith: Küçük takım, MVP, hızlı iteration
- Microservices: Büyük takım, bağımsız deploy

---

## 📚 Layered Architecture

```
Presentation → Application → Domain → Infrastructure
```

---

## ⚡ Event-Driven

```
Producer → Event Broker → Consumer
           (Kafka/SQS)
```

---

## 📊 CQRS

```
Command Service → Write DB
                    ↓ Events
Query Service ← Read DB
```

---

## 🧩 Modular Monolith

```
Modules separated by boundaries within a single deployable unit.
Good for: Teams growing from startup to scale-up phase.
Prevents "Distributed Monolith" chaos.
```

---

*Architecture Patterns v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Software Architecture Guide](https://martinfowler.com/architecture/)

### Aşama 1: Requirements Analysis
- [ ] **Functional**: Ne yapacak? (E-ticaret, Blog, IoT)
- [ ] **Non-Functional**: Scalability, Latency, Consistency ihtiyacı.
- [ ] **Constraints**: Takım boyutu, bütçe, timeline.

### Aşama 2: Complexity Assesment
- [ ] **Domain Complexity**: Karmaşıksa -> DDD + Layered/Hexagonal.
- [ ] **Scale Complexity**: Yüksek trafik -> Event-Driven / Microservices.
- [ ] **Data Complexity**: Raporlama ağırsa -> CQRS.

### Aşama 3: Pattern Selection
- [ ] **Default**: Modular Monolith ile başla.
- [ ] **Scale-out**: Bağımsız scale gereken modülleri ayır (Microservices).
- [ ] **Real-time**: Event-Driven ekle.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Gereksinimler net (NFRs belirlendi) |
| 2 | Seçilen pattern probleme uygun (Over-engineering değil) |
| 3 | Takım bu mimariyi yönetebilir |
