---
name: redis_expert
router_kit: FullStackKit
description: Redis caching stratejileri, Pub/Sub ve veri yapıları (Streams, Lists, Hashes).
metadata:
  skillport:
    category: database
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, redis expert, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - in-memory
---

# 🔴 Redis Expert

> Düşük gecikmeli veri depolama, önbellekleme ve mesajlaşma çözümleri.

---

*Redis Expert v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Redis Best Practices](https://redis.io/docs/manual/best-practices/) & [Caching Strategies (AWS)](https://aws.amazon.com/caching/best-practices/)

### Aşama 1: Data model & Structure
- [ ] **Type Selection**: Veriye uygun tipi (String, Hash, List, Set, Sorted Set) seç.
- [ ] **Naming**: Anahtar (Key) isimlendirme standartlarını (`app:module:id`) belirle.
- [ ] **TTL**: Her anahtar için mutlaka bir yaşam süresi (Expiration) tanımla.

### Aşama 2: Caching Strategy
- [ ] **Cache Aside**: Uygulamanın önce Redis'e bakıp yoksa DB'den çekip Redis'i güncellemesini sağla.
- [ ] **Invalidation**: DB güncellendiğinde ilgili Redis anahtarını silme/güncelleme mantığını kur.

### Aşama 3: Advanced Patterns
- [ ] **Pub/Sub**: Servisler arası anlık mesajlaşma için kanalları kullan.
- [ ] **Atomic Ops**: Race conditionları engellemek için `INCR` veya Lua scriptlerini kullan.
- [ ] **Streams**: Yüksek hacimli olay akışlarını (Event sourcing) yönet.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Redis belleği dolarsa "Eviction Policy" (Örn: Lru) hazır mı? |
| 2 | Büyük veriler (Big Keys) performansı yavaşlatıyor mu? |
| 3 | Bağlantılar (Connections) havuz (Pool) üzerinden mi yönetiliyor? |
