---
name: sync_core
router_kit: FullStackKit
description: Multi-file sync - atomic changes, dependency tracking ve conflict resolution.
metadata:
  skillport:
    category: development
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, sync core, testing, utilities, version control, workflow]      - refactoring-patterns
---

# 🔄 Sync Core

> Multi-file synchronization ve atomic changes.

---

## 📋 Atomic Change Principle

```markdown
Birden fazla dosya değişikliği gerektiğinde:
1. Tüm değişiklikleri önceden planla
2. Sıralı değişiklik yap
3. Her adımda build/test çalıştır
4. Tek commit'te birleştir
```

---

## 🔗 Dependency Tracking

```typescript
// Değişiklik yapmadan önce etkilenen dosyaları bul
// import/export chain'i takip et

// file-a.ts
export const API_URL = 'https://api.example.com';

// file-b.ts
import { API_URL } from './file-a';

// Değişiklik: API_URL → Tüm import'ları güncelle
```

---

## ⚠️ Change Order

```
1. Types/Interfaces (önce)
2. Utils/Helpers
3. Services
4. Components (son)
```

---

## ✅ Checklist

- [ ] Tüm dosyalar belirlendi
- [ ] Sıralama doğru
- [ ] Her adımda test
- [ ] Tek commit

## 🔄 Workflow

> **Kaynak:** [Conventional Commits](https://www.conventionalcommits.org/) & [Trunk Based Development - Syncing](https://trunkbaseddevelopment.com/)

### Aşama 1: Impact Analysis & Planning
- [ ] **Dependency Mapping**: Değişiklik yapılacak dosyanın (örn: Interface) tüm bağımlılıklarını (Import chain) çıkar.
- [ ] **Change Set Isolation**: Değişiklikleri mantıksal gruplara (Types -> Services -> UI) ayır.
- [ ] **Conflict Prediction**: Aynı dosyalarda çalışan başka PR/dal olup olmadığını kontrol et.

### Aşama 2: Sequential Update & Sync
- [ ] **Core-First Sync**: Önce temel veri yapılarını (Types/Constants) güncelle ve derleme (compilation) hatalarını gider.
- [ ] **Business Logic Update**: Services ve Controller katmanlarını yeni veri yapılarına göre senkronize et.
- [ ] **UI/Component Alignment**: Props ve View katmanını güncelleyerek döngüyü tamamla.

### Aşama 3: Verification & Atomic Commit
- [ ] **Cross-Module Testing**: Değişen tüm modüllerin birbirleriyle uyumlu çalıştığını entegrasyon testleriyle doğrula.
- [ ] **Linter/Build Check**: Tüm projede build hataları veya dangling imports kalmadığından emin ol.
- [ ] **Atomic Submission**: Tüm senkronize değişiklikleri tek ve anlamlı bir "Conventional Commit" (fix: sync...) ile gönder.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Değişiklikler "Breaking Change" içeriyor mu? (Versiyonlama kontrolü) |
| 2 | Tek bir dosya değişikliğiyle sistem "Inconsistent" hale geliyor mu? |
| 3 | Tüm import yolları (Alias/Relative) doğru güncellendi mi? |

---
*Sync Core v1.5 - With Workflow*
