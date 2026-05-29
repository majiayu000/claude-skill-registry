---
name: recent-changes
description: Son degisiklikler logu. Check when debugging or understanding recent fixes.
---

# Recent Changes

Son onemli degisiklikler ve fix'ler.

## Son Commit'ler

### Logo Overlay Devre Disi (23df9bb)
- Nano banana gorusellerinde logo overlay kaldirildi

### Instagram Container Timeout (b51a6c1)
- Container status kontrolunde retry mekanizmasi eklendi
- Max 30 deneme, 10s aralik

### Nano Banana Prompt Optimizasyonu (ea18ef4)
- Gunluk icerik promptlari iyilestirildi

### Telegram Markdown + DB Fix (1d0d08c)
- escape_markdown() fonksiyonu duzeltildi
- NULL constraint hatalari giderildi

## Bilinen Sorunlar

| Sorun | Cozum |
|-------|-------|
| Video timeout | `generate_video_smart()` kullan |
| Carousel aspect ratio | Tum slide'lar 1080x1080 |
| Telegram parse error | Markdown karakterlerini escape et |
| Instagram rate limit | 0.3s delay ekle |
| None.upper() | `(text or "").upper()` |

## Onemli Dosyalar

| Dosya | Aciklama |
|-------|----------|
| app/agents/creator.py | Icerik uretimi |
| app/telegram_pipeline.py | Bot handlers |
| app/database/models.py | Schema |
| app/scheduler/pipeline.py | Pipeline logic |

## Git Komutlari

```bash
git log --oneline -10           # Son 10 commit
git show <hash>                 # Commit detayi
git diff HEAD~1                 # Son degisiklik
```

## Deep Links

- `TROUBLESHOOTING.md` - Detayli sorun giderme
- `ARCHITECTURE.md` - Sistem mimarisi
