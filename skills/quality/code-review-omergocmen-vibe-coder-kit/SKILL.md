---
name: code-review
description: >
  Systematic code review skill covering both requesting a review (pre-commit checklist)
  and receiving and responding to review feedback. Checks code quality, security,
  test coverage, architectural alignment, and documentation before any code is committed.
---

<!--
  TÜRKÇE AÇIKLAMA
  ───────────────
  Bu skill, yazılan kodun commit'lenmeden veya push'lanmadan önce sistematik
  biçimde incelenmesini sağlar. Hem "review isteği hazırlama" (requesting) hem de
  "review feedback'ini yanıtlama" (receiving) süreçlerini kapsar.
  Kod kalitesi, güvenlik, test coverage, mimari uyum ve dokümantasyon kontrol edilir.

  NE ZAMAN: Commit öncesi (kendi kendine review), PR açmadan önce, büyük değişikliklerde.
  ÇIKTI:    Review checklist raporu, yanıtlanmış feedback listesi, düzeltilmiş kod.
-->


# Code Review Skill

## İki Mod

Bu skill iki farklı durumda devreye girer:

| Mod | Ne Zaman | Ne Yapar |
|-----|----------|----------|
| **A — Pre-Commit Review** | Commit öncesi, kendi kendinle | Checklist çalıştır, commit'e hazır mı karar ver |
| **B — Feedback Response** | Başkası review yaptı, feedback geldi | Her yorumu sınıflandır, yanıtla, düzelt |

---

## MOD A: Pre-Commit Review (Kendi Kendine)

### 1. Diff'i Çek ve Analiz Et

```bash
git diff HEAD          # staged olmayan değişiklikler
git diff --staged      # staged değişiklikler
git diff main...HEAD   # branch'in tüm değişiklikleri
```

Her değişen dosyayı gözden geçir. PR'da yorum almak istemediğin şeyleri şimdi düzelt.

---

### 2. Checklist — Sırayla Uygula

#### 🔴 Kritik (bunlar varsa commit yok)

- [ ] Hardcoded secret, API key, password var mı?
  ```bash
  git grep -i "password\|secret\|api_key\|token" -- '*.ts' '*.js' '*.py' '*.env'
  ```
- [ ] SQL injection vektörü var mı? (raw query + user input)
- [ ] Authentication veya authorization bypass riski var mı?
- [ ] Testler geçiyor mu?
  ```bash
  npm test
  ```
- [ ] Build kırılıyor mu?
  ```bash
  npm run build
  ```
- [ ] Başka modülleri kıran breaking change var mı? (notify et)

#### 🟡 Önemli (bunlar varsa ya düzelt ya bilinçli geç)

- [ ] Yeni public fonksiyon/endpoint'in JSDoc veya tipi var mı?
- [ ] Hata yönetimi yapıldı mı? (try-catch, error boundary, 404/500 handling)
- [ ] Konsola debug log bırakıldı mı? (`console.log`, `print`, `debugger`)
- [ ] Yeni env variable varsa `.env.example`'a eklendi mi?
- [ ] Herhangi bir TODO veya FIXME bırakıldı mı? (bilinçliyse ticket numarası ekle)
- [ ] Code coverage düştü mü?
  ```bash
  npm test -- --coverage
  ```
- [ ] Yeni bağımlılık eklendiyse güvenlik kontrolü yapıldı mı?
  ```bash
  npm audit
  ```

#### 🔵 Kalite (mükemmel kod için)

- [ ] Fonksiyon isimleri ne yaptıklarını anlatıyor mu?
- [ ] Bir fonksiyon birden fazla şey yapıyor mu? (bölmeli)
- [ ] Kod kopyalandı mı? (copy-paste → extract to function)
- [ ] Magic number veya string var mı? (constant'a extract et)
- [ ] Tip kullanımı yeterince katı mı? (`any` var mı?)

---

### 3. Review Kartı Oluştur

Commit mesajının yanına veya PR açıklamasına eklemek için:

```markdown
## Self-Review Özeti

**Değişiklik:** <ne yaptım, neden>
**Test Durumu:** ✅ Tüm testler geçiyor / ⚠️ X test skip edildi (gerekçe: ...)
**Checklist:**
  - 🔴 Kritik: Temiz
  - 🟡 Önemli: [varsa not]
  - 🔵 Kalite: [varsa not]

**Özellikle dikkat çekilmek istenen:**
- <reviewer'ın bakmasını istediğin yer>

**Bilinçli atınan kısayollar (deliberate shortcuts):**
- <varsa gerekçesiyle>
```

---

## MOD B: Feedback Response (Başkasının Review'ı)

### 1. Her Yorumu Sınıflandır

Gelen her review yorumu için:

```
[KRITIK]  → Blokerlık eder, merge edilemez — hemen düzelt
[ÖNEMLI]  → Güçlü öneri, iyi gerekçen yoksa uygula
[ÖNERI]   → Takdire bağlı, açık tartışma gerekebilir
[SORU]    → Bilgi isteği — açıkla veya kod ile düzelt
[NIT]     → Küçük stil/isimlendirme, senin tercihine bağlı
```

### 2. Her Yorumu Yanıtla

**Hiçbir yorum cevapsız bırakılmaz.**

```markdown
Yorum: "Bu fonksiyonun timeout'u yok, servis yanıt vermezse ne olur?"
→ Sınıf: [KRİTİK]
→ Cevap: "Haklısın. 5 saniyelik timeout + retry ekledim. T3 commit'inde görebilirsin."
→ Aksiyon: Düzeltildi ✅

Yorum: "Belki burada Map yerine Set kullanabilirsin"
→ Sınıf: [ÖNERİ]
→ Cevap: "Set burada doğru olur, key'e ihtiyacımız yok. Değiştirdim."
→ Aksiyon: Düzeltildi ✅

Yorum: "Bu isimlendirme bana semantik gelmiyor"
→ Sınıf: [NIT]
→ Cevap: "Anladım mantığını ama `processUserData` yerine `normalizeUserInput` daha açıklayıcı — değiştirdim."
→ Aksiyon: Düzeltildi ✅
```

### 3. Düzeltmeleri Grupla ve Commit At

Her düzeltme grubunu ayrı bir commit olarak at (`github` skill commit standardına göre):

```bash
# Her düzeltme ayrı commit
git commit -m "fix: add timeout and retry to userService.fetchProfile"
git commit -m "refactor: use Set instead of Map in deduplication logic"
git commit -m "refactor: rename processUserData to normalizeUserInput"
```

### 4. Re-Review İste

Tüm düzeltmeler tamamlandığında review'ı güncelle:

```markdown
## Düzeltme Özeti

Toplam yorum: 8
- Düzeltildi: 7
- Reddedildi (gerekçeyle): 1 → "NIT yorumu: mevcut isimlendirme proje konvansiyonuyla uyumlu"

Önemli değişiklikler:
- Timeout + retry mekanizması eklendi (güvenlik açısından kritik)
- 2 refactor (netlik için)

Re-review için hazır.
```

---

## Kurallar

- **Kırmızı item varsa commit yok.** İstisna yok.
- **"Sonra düzeltilir" yasak.** Ya şimdi düzelt ya da ticket aç, ticket numarasını koda ekle.
- **Her review yorumu yanıtlanır.** "Tamam" veya sessizlik kabul edilmez — ya "düzelttim" ya "katılmıyorum, çünkü..."
- **Review kendini kandırmak için değil, kodu korumak için.** Checklist'i hızlıca geçiştirme.
- **Gelen feedback kişisel değil.** Yorum koda yapılıyor, sana değil.
