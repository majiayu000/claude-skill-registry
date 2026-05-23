---
name: ui-ux-patterns
description: 50+ named UX rules with numeric thresholds, 30+ UI styles catalog, industry anti-patterns, pre-delivery checklist
---

# UI/UX Patterns

Somut, olculebilir UX kurallari ve stil rehberi. Tahmin degil, sayi var.

## Priority Kategorileri

| Oncelik | Kategori | Seviye |
|---------|----------|--------|
| 1 | Accessibility | CRITICAL |
| 2 | Navigation & Wayfinding | HIGH |
| 3 | Forms & Input | HIGH |
| 4 | Typography & Readability | HIGH |
| 5 | Color & Contrast | HIGH |
| 6 | Layout & Spacing | MEDIUM |
| 7 | Motion & Animation | MEDIUM |
| 8 | Data Display | MEDIUM |
| 9 | Feedback & States | MEDIUM |
| 10 | Charts & Visualization | LOW |

## Named UX Rules (Sayisal Esiklerle)

### Accessibility (CRITICAL)

| Kural | Esik | Aciklama |
|-------|------|----------|
| touch-target-size | min 44x44pt (iOS), 48x48dp (Android) | Dokunma alani minimum boyutu |
| color-contrast-normal | 4.5:1 | Normal text kontrast orani (WCAG AA) |
| color-contrast-large | 3:1 | Buyuk text (18px+ bold, 24px+) kontrast |
| color-contrast-enhanced | 7:1 | AAA seviye kontrast |
| focus-indicator | 2px+ visible ring | Klavye focus gostergesi |
| text-resize | 200% zoom, icerik kaybolmamali | Browser zoom destegi |
| animation-respect | prefers-reduced-motion | Animasyon tercihi |

### Navigation & Wayfinding

| Kural | Esik | Aciklama |
|-------|------|----------|
| navigation-depth | max 3 seviye | Derinlik siniri |
| breadcrumb-threshold | 2+ seviye derinlikte goster | Breadcrumb gorunurlugu |
| back-button-always | Her alt sayfada | Geri donme garantisi |
| search-visibility | 5+ nav item varsa arama ekle | Arama esigi |
| menu-item-limit | 7 +/- 2 (5-9 arasi) | Miller's Law |

### Forms & Input

| Kural | Esik | Aciklama |
|-------|------|----------|
| form-field-limit | max 7 field/step | Tek adimda alan siniri |
| label-position | ustte, sola dayali | Label pozisyonu |
| error-proximity | hata mesaji input'un 8px altinda | Hata mesaji konumu |
| password-strength | min 8 karakter + indicator | Sifre gosterge |
| autosave-interval | 30 saniyede bir | Otomatik kayit |
| input-height | min 44px | Girdi alani yuksekligi |
| placeholder-not-label | Asla placeholder'i label olarak kullanma | Placeholder kurali |

### Typography & Readability

| Kural | Esik | Aciklama |
|-------|------|----------|
| body-font-size | min 16px (mobile), 14px (desktop) | Govde yazi boyutu |
| line-height | 1.4-1.6x font size | Satir yuksekligi |
| line-length | 45-75 karakter | Ideal satir uzunlugu |
| heading-hierarchy | h1 > h2 > h3, atlama yapma | Baslik hiyerarsisi |
| paragraph-spacing | 1.5x line-height | Paragraf arasi bosluk |
| font-weight-contrast | min 2 kademe fark (400 vs 600) | Agirlik kontrasti |

### Color & Contrast

| Kural | Esik | Aciklama |
|-------|------|----------|
| max-brand-colors | 3 ana + 2 accent | Renk paleti siniri |
| status-colors | Yesil=basari, Kirmizi=hata, Sari=uyari, Mavi=bilgi | Durum renkleri |
| color-not-alone | Renk + icon/text birlikte | Renk tek bilgi tasiyici olmamali |
| dark-mode-contrast | Ayri kontrast kontrolu | Dark mode icin ozel kontrol |

### Motion & Animation

| Kural | Esik | Aciklama |
|-------|------|----------|
| duration-micro | 100-150ms | Hover, toggle, checkbox |
| duration-standard | 150-300ms | Modal, dropdown, tab switch |
| duration-complex | 300-500ms | Page transition, expand |
| stagger-sequence | 30-50ms aralik | Liste animasyon gecikme |
| easing-enter | ease-out | Goruntuye giren eleman |
| easing-exit | ease-in | Goruntudan cikan eleman |
| easing-move | ease-in-out | Pozisyon degisimi |
| no-bounce | Ease fonksiyonu kullan | Bounce animasyon kullanma |

### Layout & Spacing

| Kural | Esik | Aciklama |
|-------|------|----------|
| content-max-width | 1200-1440px | Icerik maksimum genislik |
| card-padding | min 16px, ideal 24px | Kart ic boslugu |
| section-gap | 32-64px | Bolum arasi bosluk |
| grid-gutter | 16-24px | Grid arasi bosluk |
| mobile-padding | min 16px kenar | Mobil kenar boslugu |
| z-index-scale | dropdown:10, modal:50, toast:100 | Z-index katmanlama |

### Feedback & States

| Kural | Esik | Aciklama |
|-------|------|----------|
| loading-indicator | 300ms sonra goster | Loading gecikme esigi |
| skeleton-screen | 1s+ yukleme suresi | Skeleton gosterim esigi |
| toast-duration | 3-5 saniye (bilgi), kalici (hata) | Bildirim suresi |
| empty-state | Her listede bos durum tasarla | Bos durum zorunlulugu |
| success-feedback | Her eylem sonrasi onay | Basari geri bildirimi |
| error-recovery | Her hatada cozum yolu sun | Hata kurtarma |

## UI Stil Katalogu

| Stil | Ozellik | Ne Zaman Kullan |
|------|---------|-----------------|
| Minimalism | Az eleman, cok bosluk, monokrom | SaaS, portfolyo, landing |
| Flat Design | 2D, golgesiz, temiz cizgiler | Dashboard, admin panel |
| Material Design | Elevation, grid, bold color | Android, Google ekosistemi |
| Glassmorphism | Yari saydam, blur, frost-cam efekti | Hero section, card overlay |
| Neumorphism | Soft shadow, ic/dis golge, monokrom | Hesap makinesi, player, niche UI |
| Neubrutalism | Kalin border, bold renk, raw tipografi | Yaratici portfolio, startup landing |
| Brutalism | Ham, stilize edilmemis, web-punk | Sanat, deneysel projeler |
| Bento Grid | Asimetrik grid, kart tabanli layout | Dashboard, ozellik vitrin |
| Liquid Glass | Refraction efekti, saydam katmanlar | Premium urun, Apple esintili UI |
| Skeuomorphism | Gercek obje taklidi | Oyun, muzik, niche app |
| Claymorphism | 3D, yumusak, kilit hamuru efekti | Egitim, cocuk uygulamasi |
| Aurora UI | Gradient-agirlikli, koyu arka plan | Fintech, crypto, premium |
| Retro/Pixel | 8-bit estetik, piksel font | Oyun, nostalji temalik |
| Organic/Blob | Yumusak formlar, dogal renkler | Saglik, wellness, organik urun |
| Data-Dense | Kompakt layout, cok veri, kucuk font | Bloomberg terminal, analytics |
| Card-Based | Her icerik bir kart, taranabilir | E-commerce, sosyal medya, listing |
| Split-Screen | Ekran ikiye bolunmus, kontrast | Landing, karsilastirma, portfolio |
| Monochrome | Tek renk tonlari, minimalist | Luks marka, editoryal |
| Gradient-Heavy | Canli gecisler, enerji, modernlik | SaaS marketing, startup |
| Dark-First | Koyu tema oncelikli, neon aksan | Developer tool, media, oyun |

## Industry-Specific Rehber

| Sanayi | Onerilen Stil | YAPMA |
|--------|---------------|-------|
| SaaS / B2B | Minimalism, Flat, Card-Based | Glassmorphism (kafa karistirir), Neumorphism |
| E-commerce | Card-Based, Flat | Dark-First (urun gorunmuyor), Brutalism |
| Healthcare | Flat, Organic, Accessible | Neon renkler, karisik layout, kucuk font |
| Fintech | Data-Dense, Aurora, Flat | Oyunsu eleman, belirsiz ikonlar |
| Education | Card-Based, Claymorphism, Organic | Data-Dense (ogrenciyi bunaltir) |
| Media / News | Card-Based, Bento Grid | Glassmorphism (okunurluk duser) |
| Developer Tools | Dark-First, Monochrome, Data-Dense | Neumorphism, abart animasyon |
| Gaming | Skeuomorphism, Retro, Gradient | Minimalism (sikici), corporate stil |
| Luxury / Fashion | Monochrome, Split-Screen, Minimalism | Bento Grid, Claymorphism |

## Pre-Delivery UX Checklist

### Accessibility (Zorunlu)
- [ ] Tum resimler icin anlamli alt text
- [ ] Kontrast orani: normal text 4.5:1, buyuk text 3:1
- [ ] Keyboard ile tam navigasyon (Tab, Enter, Escape)
- [ ] Focus indicator gorunur (outline kaldirma)
- [ ] Touch target min 44x44pt
- [ ] Screen reader ile test edildi
- [ ] prefers-reduced-motion destegi
- [ ] lang attribute `<html>` tag'inde

### Forms
- [ ] Her input'un label'i var (placeholder != label)
- [ ] Hata mesajlari input'un hemen altinda
- [ ] Inline validation (submit beklemeden)
- [ ] Required field belirtilmis
- [ ] Autofill/autocomplete calisiyor

### States
- [ ] Loading state (skeleton veya spinner)
- [ ] Empty state (bos liste/tablo icin)
- [ ] Error state (hata durumu UI'i)
- [ ] Success feedback (islem onay)
- [ ] Disabled state (tiklanamazligi belli)
- [ ] Hover state (clickable elemanlarda)
- [ ] Active/selected state

### Responsive
- [ ] 320px genislikte kirilma yok
- [ ] 1920px genislikte bosluk fazla degil
- [ ] Touch cihazda hover-dependent icerik yok
- [ ] Yatay scroll yok (tasma kontrolu)
- [ ] Font boyutlari mobilde okunabilir (min 16px)

### Performance
- [ ] LCP < 2.5s
- [ ] CLS < 0.1
- [ ] INP < 200ms
- [ ] Resimler lazy-loaded
- [ ] Font FOUT/FOIT yok (font-display: swap)

### Genel
- [ ] Tutarli spacing (4px/8px grid)
- [ ] Tutarli border-radius
- [ ] Dark mode token'lari dogru
- [ ] 404 sayfasi var
- [ ] Favicon ve meta taglar
