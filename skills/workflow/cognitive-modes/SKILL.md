---
name: cognitive-modes
description: Gorev tipine gore dusunme modu secimi. 5 mod -- analytical (derin analiz), creative (yaratici cozum), systematic (adim adim), rapid (hizli aksiyon), debug (hata izleme). Her mod farkli prompt stratejisi ve karar agaci kullanir.
---

# Cognitive Modes

Her gorev ayni dusunme sekli gerektirmez. Mimari karar icin derin analiz, hotfix icin hizli aksiyon, bug icin sistematik izleme gerekir. Yanlis mod = yanlis sonuc.

## 5 Dusunme Modu

### 1. ANALYTICAL (Derin Analiz)

```
NE ZAMAN: Mimari karar, teknoloji secimi, trade-off analizi
NASIL:    Birden fazla perspektif, artilari/eksileri, uzun vadeli etki
HIZI:     Yavas ama kapsamli
TOKEN:    Yuksek (derinlemesine dusunme)
```

**Davranis:**
- Her secenegi en az 3 acidan degerlendir
- Uzun vadeli sonuclari dusun (6 ay, 1 yil)
- "Neden" sorusunu en az 3 kez sor (5 Whys)
- Karar oncesi risk analizi yap
- Alternatif yaklasimlari listele

**Ornek gorevler:**
- "Monolith mi microservice mi?"
- "Hangi database kullanmaliyiz?"
- "Auth sistemi nasil tasarlanmali?"
- "Bu refactoring yapilmali mi?"

**Prompt pattern:**
```
Bu karari ANALYTICAL modda degerlendir:
1. En az 3 secenek belirle
2. Her secenegin 3+ artisi ve 3+ eksisini listele
3. Uzun vadeli etkileri degerlendir
4. Risk analizi yap
5. Net oneri ver (nedenle birlikte)
```

---

### 2. CREATIVE (Yaratici Cozum)

```
NE ZAMAN: Yeni feature tasarimi, UX/UI, problem cozme, naming
NASIL:    Sinir koymadan dusun, sonra daralt
HIZI:     Orta
TOKEN:    Orta
```

**Davranis:**
- Ilk 5 fikri YARGILAMA, sadece uret
- Farkli alanlardan analoji kullan
- "Ya su olsa?" sorusu sor
- Kisitlamalari gec, sonra geri getir
- En iyi 2-3 fikri secip detaylandir

**Ornek gorevler:**
- "Bu feature'i nasil tasarlayalim?"
- "Kullanici deneyimini nasil iyilestirelim?"
- "Bu API'nin ismi ne olmali?"
- "Onboarding akisi nasil olmali?"

**Prompt pattern:**
```
Bu gorevi CREATIVE modda ele al:
1. En az 5 farkli yaklasim uret (yargilama)
2. Her birini tek cumlede acikla
3. En ilginc 2-3'unu sec
4. Secilenleri detaylandir
5. Final oneri ver
```

---

### 3. SYSTEMATIC (Adim Adim)

```
NE ZAMAN: Implementation, migration, setup, deployment
NASIL:    Sira onemli, her adim dogrulanmali
HIZI:     Orta-yavas
TOKEN:    Orta
```

**Davranis:**
- Gorevi numarali adimlara bol
- Her adimi tamamla, SONRA sonrakine gec
- Her adim sonrasi dogrulama yap
- Adimlar arasi bagimliliklari belirle
- Hata durumunda hangi adima donulecegini belirt

**Ornek gorevler:**
- "Database migration yap"
- "CI/CD pipeline kur"
- "Yeni modul ekle"
- "Production deployment yap"

**Prompt pattern:**
```
Bu gorevi SYSTEMATIC modda yap:
1. Adimlari sirala (bagimliliklariyla)
2. Her adim icin basari kriteri belirle
3. Sirayla ilerle, adim atlama
4. Her adim sonrasi dogrula
5. Hata durumunda rollback plani hazirla
```

---

### 4. RAPID (Hizli Aksiyon)

```
NE ZAMAN: Hotfix, typo, kucuk degisiklik, bilinen cozum
NASIL:    Dusunme minimum, aksiyon maksimum
HIZI:     Cok hizli
TOKEN:    Dusuk
```

**Davranis:**
- Analiz YAPMA, direkt coz
- Tek dosya, tek degisiklik
- Review atlama (kucuk degisiklik)
- 3 satirdan fazla aciklama YAPMA
- Bitti de, devam et

**Ornek gorevler:**
- "Bu typo'yu duzelt"
- "console.log'u sil"
- "Import ekle"
- "Degiskeni yeniden adlandir"

**Prompt pattern:**
```
RAPID mod: Duzelt ve bitir. Aciklama gereksiz.
```

---

### 5. DEBUG (Hata Izleme)

```
NE ZAMAN: Bug investigation, hata analizi, neden calismıyor
NASIL:    Hipotez -> test -> eleme -> sonuc
HIZI:     Degisken (basit bug = hizli, karmasik = yavas)
TOKEN:    Degisken
```

**Davranis:**
- Once BELIRTILERI topla (hata mesaji, log, davranis)
- Hipotez listesi olustur (en olasilisi once)
- Her hipotezi SISTEMATIK test et
- Eleme yontemiyle daralt
- Root cause buldugunda KANITLA
- Fix once, test sonra

**Ornek gorevler:**
- "Bu API neden 500 donuyor?"
- "Login calismıyor"
- "Build basarisiz"
- "Test flaky"

**Prompt pattern:**
```
DEBUG mod:
1. Belirtiler: [hata mesaji, log, davranis]
2. Hipotezler: [en olasi -> en az olasi]
3. Test plani: [her hipotez icin bir test]
4. Bulgular: [ne bulundu]
5. Root cause: [kesin neden]
6. Fix: [cozum]
```

## Otomatik Mod Secimi

| Tetikleyici Kelimeler | Mod |
|----------------------|-----|
| "tasarla", "mimari", "sec", "karar", "karsilastir" | ANALYTICAL |
| "olustur", "tasarla", "fikir", "nasil olsa", "isim" | CREATIVE |
| "implement", "ekle", "kur", "migrate", "deploy" | SYSTEMATIC |
| "duzelt", "sil", "degistir", "rename", "typo" | RAPID |
| "calismıyor", "hata", "bug", "neden", "500", "fail" | DEBUG |

## Mod Gecisleri

Bazen gorev icinde mod degistirmek gerekir:

```
ANALYTICAL → SYSTEMATIC
  Karar alindi, simdi implement et

DEBUG → RAPID
  Root cause bulundu, basit fix yeterli

DEBUG → ANALYTICAL
  Root cause karmasik, mimari degisiklik gerekiyor

CREATIVE → SYSTEMATIC
  Tasarim onaylandi, adim adim implement et

SYSTEMATIC → DEBUG
  Bir adim basarisiz oldu, neden?
```

## Token Etkisi

| Mod | Ortalama Token | Maliyet (Sonnet) |
|-----|---------------:|------------------:|
| RAPID | 500-2K | $0.01-0.03 |
| DEBUG | 3K-20K | $0.05-0.30 |
| SYSTEMATIC | 5K-30K | $0.08-0.45 |
| CREATIVE | 3K-15K | $0.05-0.22 |
| ANALYTICAL | 10K-50K | $0.15-0.75 |

RAPID mod kullanarak gereksiz ANALYTICAL mod'dan kacinmak **%80+ token tasarrufu** saglar.

## vibecosystem Entegrasyonu

- **smart-model-routing skill**: Mod + model birlikte secilir (ANALYTICAL=Opus, RAPID=Sonnet)
- **token-budget skill**: Mod secimi maliyet etkisini gosterir
- **planner agent**: ANALYTICAL mod ile plan yapar
- **spark agent**: RAPID mod ile hizli fix yapar
- **sleuth agent**: DEBUG mod ile investigate eder
- **architect agent**: ANALYTICAL + CREATIVE modlari birlikte kullanir
- **kraken agent**: SYSTEMATIC mod ile TDD implement eder
