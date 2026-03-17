---
name: flux-image
description: FLUX.2 Pro gorsel uretimi. Use when generating AI images for posts.
---

# FLUX.2 Pro Image Generation

## Quick Reference

| Fonksiyon | Amac |
|-----------|------|
| generate_image_flux() | Gorsel uret |
| get_credits() | Kredi sorgula |

## Kullanim

```python
from app.flux_helper import generate_image_flux

result = await generate_image_flux(
    prompt="Professional IoT sensor, modern tech style",
    width=1024,
    height=1024,
    output_format="png"
)

if result["success"]:
    image_path = result["image_path"]
```

## Parametreler

| Param | Default | Aciklama |
|-------|---------|----------|
| prompt | required | Ingilizce prompt |
| width | 1024 | Genislik (px) |
| height | 1024 | Yukseklik (px) |
| output_format | "png" | png veya jpeg |
| max_wait_seconds | 120 | Timeout |

## API Akisi

```
1. POST /flux-2-pro -> task_id al
2. GET /get_result?id=task_id (polling, 2s aralik)
3. Status: Ready -> image URL indir
4. Dosyaya kaydet -> image_path don
```

## Return Format

```python
# Basarili
{
    "success": True,
    "image_path": "/opt/olivenet-social-bot/outputs/flux_20241225_123456.png",
    "duration": 45.2,
    "file_size": 1234567,
    "cost": 4.0  # credits
}

# Hata
{
    "success": False,
    "error": "Content Moderated"
}
```

## Status Degerleri

| Status | Anlam |
|--------|-------|
| Ready | Basarili, image URL mevcut |
| Error | Genel hata |
| Content Moderated | Icerik engellendi |
| Request Moderated | Istek engellendi |

## Prompt Tips

- Ingilizce yaz
- Detayli sahne aciklamasi
- Stil belirt: "professional", "photorealistic", "modern tech"
- IoT/teknoloji icin: sensor, dashboard, LED, cable, industrial

## Ornek Prompt

```
Professional IoT sensor device mounted on greenhouse wall,
green LED indicator blinking, modern agricultural technology,
morning sunlight, shallow depth of field, photorealistic
```

## Environment

```bash
BFL_API_KEY=your_black_forest_labs_api_key
```

## Dosya

`app/flux_helper.py`
