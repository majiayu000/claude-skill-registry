---
name: template-system
description: HTML infographic templates. Use when creating carousel slides or infographics.
---

# Template System

Instagram post ve carousel icin HTML infographic sablonlari. Playwright ile PNG'ye render edilir.

## 11 Template

| Template | Amac | Kullanim |
|----------|------|----------|
| dashboard-infographic | Panel/dashboard gorunumu | Metrik gosterimi |
| feature-grid-infographic | Grid layout ozellikler | Feature listeleme |
| timeline-infographic | Zaman cizelgesi | Surec/tarihce |
| before-after-infographic | Donusum gosterimi | Karsilastirma |
| comparison-infographic | Yan yana karsilastirma | vs. icerikleri |
| quote-infographic | Alinti/soz | Motivasyon |
| billboard-infographic | Buyuk baslik | Dikkat cekici |
| big-number-infographic | Buyuk sayi/istatistik | %75 gibi rakamlar |
| process-infographic | Adim adim surec | How-to |
| checklist-infographic | Kontrol listesi | Todo/checklist |
| visual-template | Genel sablon | Fallback |

## Rendering

```python
from app.renderer import render_html_to_png, save_html_and_render

# Direkt render
png_path = await render_html_to_png(
    html_content=html_string,
    width=1080,
    height=1080
)

# HTML + PNG kaydet
html_path, png_path = await save_html_and_render(
    html_content=html_string,
    base_name="carousel_slide_1"
)
```

## Boyutlar

| Tip | Boyut | Kullanim |
|-----|-------|----------|
| Instagram Post | 1080x1080 | Kare post |
| Instagram Story | 1080x1920 | Dikey story |
| Carousel Slide | 1080x1080 | Her slide |

## Tasarim Sabitleri (OLIVENET_DESIGN)

### Renkler
```css
/* Ana Renkler - visual-guidelines.md ve templates ile senkron */
--olive-900: #1a2e1a;  /* En koyu arka plan */
--olive-800: #243524;  /* Koyu arka plan */
--olive-700: #2d4a2d;  /* Primary button */
--olive-600: #3a5f3a;  /* Hover durumlari */
--olive-500: #4a7c4a;  /* Ana marka rengi */
--olive-400: #5e9a5e;  /* Vurgu elementleri */
--olive-300: #7ab87a;  /* Acik vurgular */
--olive-200: #a3d4a3;  /* Hafif arka planlar */
--olive-100: #d1e8d1;  /* Cok acik arka plan */
--olive-50: #e8f4e8;   /* En acik arka plan */

/* Vurgu */
--sky-500: #0ea5e9;    /* Teknoloji mavisi */
--sky-400: #38bdf8;    /* Acik mavi vurgu */
--sky-300: #7dd3fc;    /* Hafif mavi vurgu */

/* Sektor Renkleri */
--emerald-500: #10b981;  /* Tarim/Sera */
--amber-500: #f59e0b;    /* Enerji */
--violet-500: #8b5cf6;   /* Kestirimci Bakim */
```

### Font
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
font-weight: 700; /* Basliklar */
font-weight: 400; /* Body */
```

### Boyutlar
```css
/* Font Sizes */
--h1: 80px;
--h2: 56px;
--h3: 40px;
--body: 32px;
--small: 24px;

/* Border Radius */
--radius-base: 10px;
--radius-card: 16px;
--radius-cta: 24px;
--radius-button: 8px;
```

## Carousel Akisi

```
1. Creator.create_carousel_content(topic)
   -> 5+ slide HTML array

2. Her slide icin:
   render_html_to_png(slide_html)
   -> PNG dosyasi

3. Upload to CDN (imgbb)
   -> Public URL array

4. Instagram carousel API
   -> post_carousel_to_instagram(urls, caption)
```

## Template Data Binding

Her template JSON data alir:

```python
# Dashboard ornegi
data = {
    "title": "IoT Dashboard",
    "subtitle": "Gercek Zamanli Izleme",
    "metrics": [
        {"label": "Sicaklik", "value": "24°C"},
        {"label": "Nem", "value": "65%"}
    ]
}
```

## Dosyalar

- `templates/*.html` - 11 template dosyasi
- `app/renderer.py` - Playwright rendering
- `app/claude_helper.py` - Template generation (generate_*_html fonksiyonlari)
