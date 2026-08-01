---
name: plan-work
description: '> Kodlamadan önce kapsamlı planlama ve araştırma rehberi.'
---

---
name: plan_work
router_kit: ManagementKit
description: Koddan önce planlama, repo araştırması, risk analizi ve implementation plan oluşturma rehberi.
metadata:
  skillport:
    category: planning
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, plan work, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - design
---

# 📋 Plan Work

> Kodlamadan önce kapsamlı planlama ve araştırma rehberi.

---

## 📋 İçindekiler

1. [Planlama Süreci](#1-planlama-süreci)
2. [Repo Araştırması](#2-repo-araştırması)
3. [Risk Analizi](#3-risk-analizi)
4. [Implementation Plan](#4-implementation-plan)
5. [Clarifying Questions](#5-clarifying-questions)

---

## 1. Planlama Süreci

### Planlama Akışı
```
Görev Alındı
    │
    ▼
┌─────────────────────────┐
│  1. Gereksinim Analizi  │
│  (Ne isteniyor?)        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  2. Repo Araştırması    │
│  (Mevcut durum?)        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  3. Seçenek Analizi     │
│  (Alternatifler?)       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  4. Risk Değerlendirme  │
│  (Potansiyel sorunlar?) │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  5. Plan Oluşturma      │
│  (Adımlar ve timeline)  │
└─────────────────────────┘
```

### Planlama Checklist
```checklist
- [ ] Gereksinimler tam olarak anlaşıldı mı?
- [ ] Mevcut kod yapısı incelendi mi?
- [ ] Bağımlılıklar belirlendi mi?
- [ ] Alternatif yaklaşımlar değerlendirildi mi?
- [ ] Riskler tanımlandı mı?
- [ ] Test stratejisi belirlendi mi?
```

---

## 2. Repo Araştırması

### Kod Yapısı Analizi
```bash
# Dizin yapısını anla
tree -L 2 src/

# İlgili dosyaları bul
find . -name "*.ts" | xargs grep -l "searchTerm"

# Bağımlılıkları kontrol et
cat package.json | jq '.dependencies'
```

### Sorulması Gereken Sorular
| Alan | Sorular |
|------|---------|
| **Mimari** | Hangi pattern kullanılıyor? (MVC, Clean Architecture?) |
| **State** | State management nasıl? (Redux, Zustand, Context?) |
| **API** | REST mi GraphQL mi? Endpoint yapısı nasıl? |
| **Test** | Test framework ne? Coverage hedefi? |
| **Stil** | ESLint/Prettier config var mı? |

### Mevcut Kod Patterns
```
# Ararken bakılacaklar:
- Similar features (nasıl implement edilmiş?)
- Error handling patterns
- Validation patterns
- Logging conventions
- Naming conventions
```

---

## 3. Risk Analizi

### Risk Kategorileri

| Kategori | Örnek Riskler | Mitigation |
|----------|--------------|------------|
| **Teknik** | Performans, scalability | POC, benchmark |
| **Bağımlılık** | Breaking changes, deprecated API | Version pinning |
| **Zaman** | Underestimation | Buffer time ekle |
| **Scope** | Feature creep | Clear requirements |
| **Entegrasyon** | 3rd party API | Fallback stratejisi |

### Risk Değerlendirme Template
```markdown
## Risk: [Risk Adı]

**Olasılık:** Düşük / Orta / Yüksek
**Etki:** Düşük / Orta / Yüksek
**Açıklama:** ...

**Mitigation:**
1. ...
2. ...

**Contingency Plan:**
Eğer risk gerçekleşirse: ...
```

---

## 4. Implementation Plan

### Plan Template
```markdown
# Implementation Plan: [Feature Name]

## Özet
Kısa açıklama

## Scope
### Dahil:
- ...

### Hariç:
- ...

## Teknik Yaklaşım
1. Adım 1
2. Adım 2
3. ...

## Dosya Değişiklikleri
- `src/components/X.tsx` - Yeni component
- `src/api/Y.ts` - API endpoint

## Bağımlılıklar
- Package A (v1.2.3)
- Package B

## Timeline
| Adım | Süre | Açıklama |
|------|------|----------|
| Setup | 1h | Initial setup |
| Core | 4h | Core implementation |
| Test | 2h | Unit tests |

## Test Stratejisi
- Unit tests: ...
- Integration tests: ...
- Manual QA: ...
```

### Estimation Guidelines
| Complexity | Süre | Örnek |
|------------|------|-------|
| Trivial | < 1h | Config değişikliği |
| Small | 1-4h | Basit component |
| Medium | 4-8h | Feature modülü |
| Large | 1-3 gün | Yeni sistem |
| XL | 1+ hafta | Major refactor |

---

## 5. Clarifying Questions

### Sorulması Gereken Sorular
```markdown
## Gereksinimler
- Kullanıcı hikayesi tam mı?
- Edge case'ler düşünüldü mü?
- Error durumları tanımlandı mı?

## Tasarım
- UI/UX mockup var mı?
- Responsive davranış bekleniyor mu?
- Accessibility gereksinimleri?

## Teknik
- Performans hedefi var mı?
- Backward compatibility gerekli mi?
- Migration stratejisi gerekli mi?

## Timeline
- Deadline var mı?
- Phased delivery mümkün mü?
```

### Question Template
```
Uygulamaya başlamadan önce birkaç sorum var:

1. [Soru 1]
2. [Soru 2]
3. [Soru 3]

Bu bilgiler, en uygun yaklaşımı belirlememize yardımcı olacak.
```

---

## 6. AoT Etiket Yapısı

Planlama sürecinde bu XML yapısını kullan:

```xml
<thinking>
  Görevi analiz et. Gereksinimleri listele.
  Kod yazmadan önce tam olarak anla.
</thinking>

<plan>
  ## Adımlar
  1. [Araştırma adımı]
  2. [Tasarım adımı]
  3. [Uygulama adımı]
  4. [Test adımı]
</plan>

<reflection>
  Bu plan yeterli mi?
  Eksik bir şey var mı?
  Riskler değerlendirildi mi?
</reflection>
```

---

*Plan Work v2.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [RFC Process (IETF inspired)](https://en.wikipedia.org/wiki/Request_for_Comments) & [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)

### Aşama 1: Problem Definition (The "Why")
- [ ] **Context**: Sorun nedir? Neden şimdi çözüyoruz? (Business value).
- [ ] **Requirements**: Functional (Ne yapacak?) ve Non-functional (Hız, Güvenlik?) gereksinimleri netleştir.
- [ ] **Anti-Goals**: Neyi *yapmayacağız*? (Scope creep önleme).

### Aşama 2: Solution Design (The "How")
- [ ] **Alternatives**: En az 2 yaklaşıma bak (Option A vs Option B). Trade-off analizi yap.
- [ ] **Architecture**: High-level diyagram (Mermaid) çiz. Veri akışını göster.
- [ ] **Data Model**: DB şeması veya API kontrat değişikliklerini tasarla.

### Aşama 3: Revision & Committment
- [ ] **Risk Assessment**: "En kötü ne olabilir?" (Rollback planı).
- [ ] **Estimation**: T-shirt size (S/M/L) veya gün bazlı tahmin yap.
- [ ] **Review**: Tasarımı ekiple paylaş (RFC/Design Doc Review) ve onay al.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Bilinmeyenler (Unknowns) listelendi mi? |
| 2 | Bu çözüm teknik borç yaratıyor mu? Eğer evetse, planlı mı? |
| 3 | Güvenlik ve Gizlilik (Privacy) etkileri formu dolduruldu mu? |
