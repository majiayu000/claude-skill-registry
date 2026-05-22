---
name: debugging_methodology
router_kit: FullStackKit
description: Sistematik debugging döngüsü - reproduce, isolate, hypothesize, fix.
metadata:
  skillport:
    category: quality
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, debugging methodology, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - debugging-tools
---

# 🔍 Debugging Methodology

> Sistematik hata ayıklama döngüsü.

---

## 🔄 Debugging Döngüsü

```
REPRODUCE → UNDERSTAND → ISOLATE → HYPOTHESIZE → TEST → FIX → REFLECT
```

---

## 1️⃣ Reproduce
```markdown
### Tekrarlama Raporu
- Hata: [Açıklama]
- Adımlar: 1. ... 2. ... 3. → Hata
- Ortam: [OS, Node, Browser]
- Tekrarlanabilirlik: [%100 / %50 / Nadiren]
```

---

## 2️⃣ 5 Whys

```markdown
Problem: Login çalışmıyor
1. Neden? → API 401 dönüyor
2. Neden? → Token geçersiz
3. Neden? → Token expire
4. Neden? → Refresh çalışmıyor
5. Neden? → Endpoint değişmiş
```

---

## 3️⃣ Binary Search (git bisect)

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run npm test
```

---

## 4️⃣ Hipotez Listesi

| # | Hipotez | Olasılık | Test |
|---|---------|----------|------|
| 1 | Null pointer | %40 | console.log |
| 2 | Race condition | %30 | timeout ekle |

---

*Debugging Methodology v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Scientific Method in Debugging](https://queue.acm.org/detail.cfm?id=1839676)

### Aşama 1: Incident Response (Triage)
- [ ] **Log**: Hata mesajını ve call stack'i kaydet.
- [ ] **Reproduce**: Hatayı lokalde veya test ortamında en az 1 kez tekrar et.
- [ ] **Environment**: Versiyon farklarını (Prod vs Dev) kontrol et.

### Aşama 2: Root Cause Analysis (RCA)
- [ ] **Bisection**: Sorunun başladığı commit'i bul (`git bisect`).
- [ ] **Isolation**: Sistemi parçalara ayırarak hatayı izole et (Unit Test yaz).
- [ ] **Hypothesis**: En olası nedenleri listele ve Binary Search ile ele.

### Aşama 3: Resolution & Prevention
- [ ] **Fix**: En az müdahale ile sorunu çözen kodu yaz.
- [ ] **Verify**: Hem fix'i hem de regression (yan etki) olmadığını test et.
- [ ] **Post-Mortem**: "Neden oldu?" ve "Nasıl önlenir?" sorularını yanıtla.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | "Bende çalışıyor" tuzağına düşüldü mü? (Ortam farkı kontrolü) |
| 2 | Fix yaparken test yazıldı mı? (TDD) |
| 3 | Benzer hatalar başka yerde var mı tarandı mı? |
