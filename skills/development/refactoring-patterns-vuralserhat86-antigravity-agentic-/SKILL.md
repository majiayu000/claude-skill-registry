---
name: refactoring_patterns
router_kit: FullStackKit
description: Common refactoring patterns - Extract, Rename, Move ve code smell çözümleri.
metadata:
  skillport:
    category: quality
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, refactoring patterns, software engineering, standards, testing, utilities, version control, workflow]      - refactoring-strategies
---

# 🔄 Refactoring Patterns

> Common refactoring patterns ve code smell çözümleri.

---

## 🎯 Altın Kural

> **Davranışı DEĞİŞTİRME, sadece yapıyı iyileştir**

```
Before: Input X → [Code A] → Output Y
After:  Input X → [Code B] → Output Y (AYNI!)
```

---

## 🔍 Code Smells

| Smell | Çözüm |
|-------|-------|
| Long Method | Extract Method |
| Large Class | Extract Class |
| Duplicate Code | Extract + Reuse |
| Long Parameter List | Parameter Object |
| Feature Envy | Move Method |
| Data Clumps | Extract Class |

---

## 📦 Extract Method

```typescript
// ❌ Before
function processOrder(order) {
  // 20 lines of validation
  // 30 lines of calculation
  // 15 lines of formatting
}

// ✅ After
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order);
  return formatOutput(total);
}
```

---

## 🔄 Replace Conditional with Polymorphism

```typescript
// ❌ Before
function getPrice(type) {
  if (type === 'premium') return 100;
  if (type === 'basic') return 50;
  return 30;
}

// ✅ After
const pricing = { premium: 100, basic: 50, free: 30 };
const getPrice = (type) => pricing[type] ?? 30;
```

---

*Refactoring Patterns v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Refactoring.guru](https://refactoring.guru/refactoring/techniques) & [Martin Fowler - Refactoring](https://martinfowler.com/books/refactoring.html)

### Aşama 1: Preparation (Safety First)
- [ ] **Red-Green-Refactor**: Testin var mı? Yoksa önce test yaz ("Characterization Tests"), sonra refactor et.
- [ ] **Small Steps**: Değişiklikleri atomik commitler halinde yap. Her adımda testleri çalıştır.
- [ ] **Backup**: VCS (Git) üzerinde temiz bir dalda çalış.

### Aşama 2: Applying Patterns
- [ ] **Simplification**: Karmaşık koşulları `Decompose Conditional` veya `Replace Nested Conditional with Guard Clauses` ile basitleştir.
- [ ] **Abstraction**: `Extract Method` ve `Extract Class` ile sorumlulukları (SRP) ayır. `Primitive Obsession` varsa Value Object'e çevir.
- [ ] **Modernization**: `var` -> `const/let`, `for` -> `map/filter`, Callback -> Async/Await dönüşümlerini uygula (Dil özelliklerini kullan).

### Aşama 3: Verification & Cleanup
- [ ] **Regression Testing**: Mevcut fonksiyonların bozulmadığını doğrula.
- [ ] **Dead Code**: Kullanılmayan kodları (Dead Code) acımasızca sil. Yorum satırına alma, sil (Git geçmişinde var zaten).
- [ ] **Naming**: Değişken ve fonksiyon isimlerini, kodun ne yaptığını değil "neden" yaptığını anlatacak şekilde güncelle.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Refactoring sırasında yeni özellik eklendi mi? (KESİNLİKLE HAYIR. İki şapka kuralı: Ya Refactor yap ya Feature ekle). |
| 2 | Kodun okunabilirliği arttı mı? (Cognitive Complexity düştü mü?). |
| 3 | Test kapsamı (Coverage) korundu mu? |
