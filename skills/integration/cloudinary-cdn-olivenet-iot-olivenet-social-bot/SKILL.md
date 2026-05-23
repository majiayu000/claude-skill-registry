---
name: cloudinary-cdn
description: Video CDN yonetimi. Use when uploading videos for Instagram Reels.
---

# Cloudinary CDN

Instagram Reels icin public URL gerekli. Yerel video dosyalarini Cloudinary'ye yukleyip public URL aliyoruz.

## Quick Reference

| Fonksiyon | Amac |
|-----------|------|
| configure_cloudinary() | SDK'yi baslat |
| upload_video_to_cloudinary() | Video yukle |
| delete_from_cloudinary() | Video sil |

## Kullanim

```python
from app.cloudinary_helper import upload_video_to_cloudinary

result = await upload_video_to_cloudinary(
    video_path="/path/to/video.mp4",
    folder="olivenet-reels"
)

if result["success"]:
    public_url = result["url"]  # Instagram Reels icin kullan
```

## Return Format

```python
# Basarili
{
    "success": True,
    "url": "https://res.cloudinary.com/cloud/video/upload/v123/olivenet-reels/xyz.mp4",
    "public_id": "olivenet-reels/xyz",
    "duration": 8.5,
    "format": "mp4"
}

# Hata
{
    "success": False,
    "error": "File not found: /path/to/video.mp4"
}
```

## Reels Pipeline Akisi

```
1. Veo/Sora -> video.mp4 (yerel dosya)
2. upload_video_to_cloudinary() -> public URL
3. Instagram API -> create container with URL
4. Instagram API -> publish container
5. (opsiyonel) delete_from_cloudinary() -> temizlik
```

## Silme

```python
from app.cloudinary_helper import delete_from_cloudinary

result = await delete_from_cloudinary("olivenet-reels/xyz")
if result["success"]:
    print("Silindi")
```

## Environment

```bash
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Notlar

- Async upload icin thread pool kullaniliyor
- overwrite=True: Ayni isimde dosya varsa ustune yaz
- secure=True: HTTPS URL'ler
- resource_type="video": Video olarak isle

## Dosya

`app/cloudinary_helper.py`
