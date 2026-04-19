---
name: brand-identity
description: Voice framework, visual identity standards, color palette management, typography specs, brand consistency
---

# Brand Identity

Marka kimligini olusturma ve koruma rehberi. Tutarlilik her seydir.

## Voice Framework

### Voice vs Tone

| Kavram | Tanim | Ornek |
|--------|-------|-------|
| Voice | Markanin kalici kisilik ozellikleri | "Profesyonel ama samimi" |
| Tone | Duruma gore degisen ifade bicimi | Hata mesajinda: empatik, basaride: kutlamaci |

### Personality Traits Matrisi

Markanin 4 eksenini tanimla:

| Eksen | Sol Uc | Sag Uc | Senin Pozisyon (1-5) |
|-------|--------|--------|----------------------|
| Formalite | Resmi, kurumsal | Samimi, konusma dili | ? |
| Enerji | Sakin, olculu | Heyecanli, enerjik | ? |
| Mizah | Ciddi, agirbasli | Eglenceli, espirili | ? |
| Teknik | Basit, herkes icin | Uzman, teknik dil | ? |

### Voice Checklist

- [ ] 3-5 kelimelik voice tanimi var (orn: "Guvenilir, samimi, net")
- [ ] Her voice ozelliginin "yapma" karsiligi var
- [ ] Ornek cumleler var (ana sayfa, hata mesaji, onboarding)
- [ ] Tone varyasyonlari tanimli (basari, hata, bekleme, bilgi)

## Visual Identity Standards

### Logo Kullanim Kurallari

| Kural | Detay |
|-------|-------|
| Clear space | Logo etrafinda min logo yuksekligi kadar bosluk |
| Min boyut | Dijitalde min 24px yukseklik |
| Arka plan | Hangi renklerde kullanilabilir, hangilerinde degil |
| Varyasyonlar | Full color, monochrome, reversed (dark bg) |
| Yasaklar | Stretch etme, renk degistirme, efekt ekleme |

### Color Palette Management

#### 3-Katman Token Mimarisi

```
LAYER 1: Primitive (Ham renkler)
  blue-500: #3b82f6
  blue-600: #2563eb
  gray-100: #f3f4f6

LAYER 2: Semantic (Anlam tasiyan)
  color-primary: {blue-600}
  color-danger: {red-600}
  color-surface: {white}
  color-text: {gray-900}

LAYER 3: Component (Kullanim yeri)
  button-primary-bg: {color-primary}
  button-primary-hover: {blue-700}
  card-bg: {color-surface}
  input-border: {gray-300}
```

#### Palette Kurallari

| Kural | Detay |
|-------|-------|
| Ana renkler | Max 3 (primary, secondary, accent) |
| Notral tonlar | 1 gray skalasi (50-950) |
| Durum renkleri | Success (yesil), Warning (sari), Danger (kirmizi), Info (mavi) |
| Dark mode | Her semantic token'in dark varyanti |
| Kontrast | Tum text/bg kombinasyonlari WCAG AA (4.5:1) |

### Typography Specifications

| Kullanim | Font | Agirlik | Boyut | Satir Yuksekligi |
|----------|------|---------|-------|-----------------|
| Display | Primary | Bold (700) | 48-72px | 1.1 |
| H1 | Primary | Semibold (600) | 36-48px | 1.2 |
| H2 | Primary | Semibold (600) | 24-36px | 1.25 |
| H3 | Primary | Medium (500) | 20-24px | 1.3 |
| Body | Primary | Regular (400) | 16px | 1.5 |
| Small | Primary | Regular (400) | 14px | 1.4 |
| Caption | Primary | Regular (400) | 12px | 1.3 |
| Code | Mono | Regular (400) | 14px | 1.5 |

#### Font Pairing Rehberi

| Baslik | Govde | Karakter |
|--------|-------|----------|
| Inter | Inter | Notr, profesyonel |
| Cal Sans | Inter | Modern, teknoloji |
| Playfair Display | Source Sans | Luks, editoryal |
| Space Grotesk | DM Sans | Yaratici, modern |
| Fraunces | Work Sans | Sicak, organik |

### Iconography

| Kural | Detay |
|-------|-------|
| Stil tutarliligi | Tek icon seti sec (Lucide, Heroicons, Phosphor) |
| Boyut skalasi | 16, 20, 24, 32px (text ile orantili) |
| Cizgi kalinligi | Set icinde tutarli (1.5px veya 2px) |
| Filled vs Outlined | Birini sec, karistirma |

## Brand Consistency Checklist

### Dijital Urunler
- [ ] Primary font tanimli ve yuklendi
- [ ] Color token'lari CSS variable olarak tanimli
- [ ] Logo tum varyasyonlarda mevcut (SVG)
- [ ] Favicon ve og:image marka tutarli
- [ ] Button, input, card stilleri tutarli
- [ ] Hata mesajlari marka voice'una uygun
- [ ] Empty state illust/copy marka ile uyumlu
- [ ] Loading animasyonu marka ile uyumlu
- [ ] 404 sayfasi marka ile uyumlu

### Iletisim
- [ ] Email template'leri marka tutarli
- [ ] Bildirim mesajlari voice rehberine uygun
- [ ] Onboarding akisi marka tonunda
- [ ] Dokumantasyon stili tutarli

## Islem Akisi

1. **Kesfet**: Marka degerlerini, hedef kitleyi, rakipleri analiz et
2. **Tanimla**: Voice, renk, tipografi, ikon standartlarini belirle
3. **Dokumante et**: Token'lari, kurallari, ornekleri yaz
4. **Uygula**: Design system'e entegre et
5. **Denetle**: Tutarlilik kontrolu yap, sapmalari duzelt
