---
name: tdd-workflow
description: Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# TDD İş Akışı

> Önce testleri yaz, sonra kodu.

---

## 1. TDD Döngüsü

```
🔴 KIRMIZI (RED) → Başarısız olan testi yaz
       ↓
🟢 YEŞİL (GREEN) → Geçmek için minimum kodu yaz
       ↓
🔵 YENİDEN DÜZENLE (REFACTOR) → Kod kalitesini iyileştir
       ↓
    Tekrarla...
```

---

## 2. TDD'nin Üç Kuralı

1. Sadece başarısız olan bir testi geçmek için üretim kodu yazın
2. Sadece başarısızlığı göstermek için yeterli test yazın
3. Sadece testi geçmek için yeterli kod yazın

---

## 3. KIRMIZI (RED) Aşaması Prensipleri

### Ne Yazılmalı

| Odak | Örnek |
|-------|---------|
| Davranış | "iki sayıyı toplamalı" |
| Uç durumlar | "boş girdiyi işlemeli" |
| Hata durumları | "geçersiz veri için hata fırlatmalı" |

### KIRMIZI Aşaması Kuralları

- Test önce başarısız olmalı
- Test adı beklenen davranışı tanımlamalı
- Test başına bir doğrulama (ideal olarak)

---

## 4. YEŞİL (GREEN) Aşaması Prensipleri

### Minimum Kod

| Prensip | Anlamı |
|-----------|---------|
| **YAGNI** | Buna İhtiyacın Olmayacak (You Aren't Gonna Need It) |
| **En basit şey** | Geçmek için minimumu yaz |
| **Optimizasyon yok** | Sadece çalışmasını sağla |

### YEŞİL Aşaması Kuralları

- Gereksiz kod yazma
- Henüz optimize etme
- Testi geç, fazlasını değil

---

## 5. YENİDEN DÜZENLE (REFACTOR) Aşaması Prensipleri

### Ne İyileştirilmeli

| Alan | Eylem |
|------|--------|
| Yineleme (Duplication) | Ortak kodu çıkar |
| İsimlendirme | Niyeti netleştir |
| Yapı | Organizasyonu iyileştir |
| Karmaşıklık | Mantığı basitleştir |

### YENİDEN DÜZENLEME Kuralları

- Tüm testler yeşil kalmalı
- Küçük artımlı değişiklikler
- Her yeniden düzenlemeden sonra commit et

---

## 6. AAA Deseni

Her test şunları izler:

| Adım | Amaç |
|------|---------|
| **Düzenle (Arrange)** | Test verilerini ayarla |
| **Etki Et (Act)** | Test edilen kodu çalıştır |
| **Doğrula (Assert)** | Beklenen sonucu doğrula |

---

## 7. TDD Ne Zaman Kullanılır

| Senaryo | TDD Değeri |
|----------|-----------|
| Yeni özellik | Yüksek |
| Hata düzeltme | Yüksek (önce test yaz) |
| Karmaşık mantık | Yüksek |
| Keşifsel (Exploratory) | Düşük (spike yap, sonra TDD) |
| UI düzeni | Düşük |

---

## 8. Test Önceliklendirmesi

| Öncelik | Test Türü |
|----------|-----------|
| 1 | Mutlu yol (Happy path) |
| 2 | Hata durumları |
| 3 | Uç durumlar |
| 4 | Performans |

---

## 9. Anti-Desenler

| ❌ Yapma | ✅ Yap |
|----------|-------|
| KIRMIZI aşamasını atla | Önce testin başarısız olduğunu gör |
| Testleri sonra yaz | Testleri önce yaz |
| Başlangıçta aşırı mühendislik | Basit tut |
| Çoklu doğrulamalar | Test başına bir davranış |
| Uygulamayı test et | Davranışı test et |

---

## 10. AI-Destekli TDD

### Çoklu Ajan Deseni

| Ajan | Rol |
|-------|------|
| Ajan A | Başarısız testler yaz (KIRMIZI) |
| Ajan B | Geçmek için uygula (YEŞİL) |
| Ajan C | Optimize et (YENİDEN DÜZENLE) |

---

> **Unutmayın:** Test, spesifikasyondur. Eğer bir test yazamıyorsanız, gereksinimi anlamamışsınız demektir.
