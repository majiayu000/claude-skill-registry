---
name: code-review
description: '> Etkili kod inceleme ve kalite kontrol rehberi.'
---

---
name: code_review
router_kit: FullStackKit
description: PR review, code smell detection, best practice kontrolü. ⚠️ Kod incelerken kullan. Deliverable kontrolü için → quality-validator, doküman review için → peer-review.
metadata:
  skillport:
    category: quality
    tags: [architecture, automation, best practices, clean code, code review, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - code-smell
---

# 🔍 Code Review

> Etkili kod inceleme ve kalite kontrol rehberi.

---

## 📋 İçindekiler

1. [Review Checklist](#1-review-checklist)
2. [Code Smell Detection](#2-code-smell-detection)
3. [PR Best Practices](#3-pr-best-practices)
4. [Review Comments](#4-review-comments)

---

## 1. Review Checklist

### Fonksiyonellik
```checklist
- [ ] Kod istenen işi yapıyor mu?
- [ ] Edge case'ler handle ediliyor mu?
- [ ] Error handling yeterli mi?
- [ ] Input validation var mı?
```

### Kod Kalitesi
```checklist
- [ ] DRY prensibi uygulanmış mı?
- [ ] Single Responsibility takip ediliyor mu?
- [ ] Naming conventions tutarlı mı?
- [ ] Magic numbers/strings yok mu?
```

### Güvenlik
```checklist
- [ ] SQL injection riski var mı?
- [ ] XSS riski var mı?
- [ ] Sensitive data expose edilmiş mi?
- [ ] Authentication/authorization doğru mu?
```

### Performans
```checklist
- [ ] N+1 query problemi var mı?
- [ ] Gereksiz re-render var mı?
- [ ] Memory leak riski var mı?
- [ ] Büyük dosya/data handling doğru mu?
```

---

## 2. Code Smell Detection

### Yaygın Code Smell'ler

| Smell | Açıklama | Çözüm |
|-------|----------|-------|
| **Long Method** | >20 satır fonksiyon | Extract Method |
| **Large Class** | >300 satır class | Extract Class |
| **Long Parameter List** | >3 parametre | Parameter Object |
| **Duplicate Code** | Tekrarlayan bloklar | Extract Method/Class |
| **Dead Code** | Kullanılmayan kod | Sil |
| **Magic Numbers** | Açıklamasız değerler | Constants |
| **Deep Nesting** | >3 seviye if/loop | Early return, Extract |
| **God Class** | Her şeyi yapan class | Single Responsibility |

### Algılama Komutları
```bash
# ESLint complexity check
npx eslint . --rule 'complexity: ["error", 10]'

# SonarQube
sonar-scanner

# Code coverage
npm run test:coverage
```

---

## 3. PR Best Practices

### İdeal PR Boyutu
- **Küçük**: <200 satır (ideal)
- **Orta**: 200-400 satır
- **Büyük**: >400 satır (bölünmeli)

### PR Açıklama Template
```markdown
## Özet
Kısa açıklama

## Değişiklik Tipi
- [ ] Bug fix
- [ ] Yeni özellik
- [ ] Refactoring
- [ ] Breaking change

## Test
- Test X yapıldı
- Test Y sonucu: başarılı

## Screenshots (UI değişikliği varsa)
```

### Commit Messages
```
feat: Add user authentication
fix: Resolve memory leak in cache
refactor: Extract validation logic
docs: Update API documentation
test: Add unit tests for user service
chore: Update dependencies
```

---

## 4. Review Comments

### Etkili Yorum Yazma
```
❌ Kötü: "Bu yanlış"
✅ İyi: "Bu yaklaşım X durumunda hata verebilir. Y alternatifini düşünebilir misin?"

❌ Kötü: "Bunu değiştir"
✅ İyi: "suggestion: Bu fonksiyon extract edilse okunabilirlik artar"
```

### Yorum Prefixleri
| Prefix | Anlam |
|--------|-------|
| `blocking:` | Merge edilemez, düzeltilmeli |
| `suggestion:` | Öneri, isteğe bağlı |
| `question:` | Açıklama gerekiyor |
| `nitpick:` | Minor, önemsiz |
| `praise:` | İyi iş! |

---

*Code Review v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Google Engineering Practices](https://google.github.io/eng-practices/review/reviewer/)

### Aşama 1: Triage (Ön Kontrol)
- [ ] **CI Checks**: Testler geçmiş mi? Lint hatası var mı?
- [ ] **Scope**: PR çok mu büyük? (>400 satır ise bölmesini iste).
- [ ] **Description**: "Ne" ve "Neden" açıkça anlatılmış mı?

### Aşama 2: Deep Dive
- [ ] **Logic**: Kodun algoritması doğru ve verimli mi?
- [ ] **Architecture**: Mevcut mimari desenlere uyuyor mu?
- [ ] **Test**: Yeni özellikler için test yazılmış mı?

### Aşama 3: Feedback
- [ ] **Comments**: Yapıcı, nazik ve net yorumlar yaz (`suggestion:`, `question:`).
- [ ] **Decision**: Approve, Request Changes veya Comment.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | PR açıklaması boş ise reddedildi mi? |
| 2 | Breaking change varsa versiyonlamaya dikkat edildi mi? |
| 3 | Yorumlar kişiye değil koda mı yönelik? |
